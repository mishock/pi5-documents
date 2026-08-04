"""Мониторинг ГдеБЕНЗ: город в Telegram, пуш при появлении бензина или очереди."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import fuel_sources
import gdebenz_client
import fuel_hub
from fuel_sources.qr_crimea import detect_qr_region, format_qr_help
from fuel_sources.qr_request import cancel_pending, obtain_qr, pending_status, process_pending_monitors
from gdebenz_notify import notify_fuel_alert

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "data" / "gdebenz-fuel.json"
STATE_PATH = PROJECT_ROOT / "data" / "gdebenz-fuel-state.json"
ENV_PATH = PROJECT_ROOT / ".env"
MSK = ZoneInfo("Europe/Moscow")

STATUS_LABEL = {
    "ok": "есть",
    "queue": "очередь",
    "low": "мало",
    "no": "нет",
    "limit": "лимит",
    None: "нет отметок",
    "": "нет отметок",
}

STATUS_EMOJI = {
    "ok": "🟢",
    "queue": "🟠",
    "low": "🟡",
    "no": "🔴",
    "limit": "🔵",
    None: "⚪",
    "": "⚪",
}

ALERT_STATUSES = frozenset({"ok", "queue"})
ACTIVE_STATUSES = frozenset({"ok", "queue", "low", "limit", "no"})
FUEL_ALIASES = {
    "92": "92",
    "аи-92": "92",
    "аи92": "92",
    "95": "95",
    "аи-95": "95",
    "аи95": "95",
    "98": "98",
    "дт": "dt",
    "dt": "dt",
    "дизель": "dt",
    "diesel": "dt",
    "газ": "gas",
    "пропан": "gas",
    "суг": "gas",
}

DEFAULT_CONFIG: dict[str, Any] = {
    "fresh_minutes": 45,
    "quiet_start": 23,
    "quiet_end": 7,
    "default_city": "Симферополь",
    "alert_email": "",
    "monitoring_disabled": False,
    "sources": ["gdebenz", "gdebenz.su", "azs-crimea", "atan"],
    "chats": {},
}

DEFAULT_CITY: dict[str, Any] = {
    "city": "Симферополь",
    "lat": 44.9521459,
    "lon": 34.1024858,
    "bbox": [44.8908263, 34.0289229, 45.0042505, 34.1989159],
}
CRIMEA_REGION = {
    "city": "Крым (регион)",
    "lat": 45.0,
    "lon": 34.1,
    "bbox": [44.3, 32.15, 46.2, 36.45],
}

DEFAULT_FUELS: list[str] = ["92", "95"]
VALID_FUELS = frozenset({"92", "95", "98", "100", "dt", "gas", "all"})

FUEL_DISPLAY = {
    "92": "АИ-92",
    "95": "АИ-95",
    "98": "АИ-98",
    "100": "АИ-100",
    "dt": "ДТ",
    "gas": "газ",
}


def load_env() -> None:
    if not ENV_PATH.is_file():
        return
    for line in ENV_PATH.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.is_file():
        return json.loads(json.dumps(default))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    return json.loads(json.dumps(default))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def load_config() -> dict[str, Any]:
    cfg = load_json(CONFIG_PATH, DEFAULT_CONFIG)
    cfg.setdefault("fresh_minutes", 45)
    cfg.setdefault("quiet_start", 23)
    cfg.setdefault("quiet_end", 7)
    cfg.setdefault("sources", list(DEFAULT_CONFIG["sources"]))
    cfg.setdefault("chats", {})
    cfg.setdefault("alert_email", "")
    cfg.setdefault("monitoring_disabled", False)
    return cfg


def monitoring_is_disabled(cfg: dict[str, Any] | None = None) -> bool:
    """Глобальный стоп автопоиска/пушей (почта + Telegram)."""
    data = cfg if cfg is not None else load_config()
    return bool(data.get("monitoring_disabled"))


def config_sources(cfg: dict[str, Any], bbox: list[float]) -> list[str]:
    raw = cfg.get("sources") or DEFAULT_CONFIG["sources"]
    if isinstance(raw, list) and raw:
        return [str(s) for s in raw]
    return fuel_sources.default_sources(bbox)


def fetch_city_stations(chat: dict[str, Any], cfg: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    bbox = chat.get("bbox") or []
    if len(bbox) != 4:
        return [], {}
    lat1, lon1, lat2, lon2 = [float(x) for x in bbox]
    return fuel_sources.fetch_stations_merged(
        lat1,
        lon1,
        lat2,
        lon2,
        sources=config_sources(cfg, bbox),
    )


def save_config(cfg: dict[str, Any]) -> None:
    save_json(CONFIG_PATH, cfg)


def load_state() -> dict[str, Any]:
    return load_json(STATE_PATH, {})


def save_state(state: dict[str, Any]) -> None:
    save_json(STATE_PATH, state)


def now_msk() -> datetime:
    return datetime.now(MSK)


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=MSK)
        except ValueError:
            continue
    return None


def normalize_fuel(value: str) -> str:
    key = value.strip().lower().replace(" ", "")
    return FUEL_ALIASES.get(key, key)


def norm_status(value: str | None) -> str:
    if not value:
        return ""
    key = value.strip().lower()
    if key in ("yes", "ok", "есть", "естьтопливо"):
        return "ok"
    if key in ("queue", "очередь"):
        return "queue"
    if key in ("low", "мало"):
        return "low"
    if key in ("no", "нет", "empty"):
        return "no"
    if key in ("limit", "лимит"):
        return "limit"
    return key


def parse_fuels_list(text: str) -> list[str]:
    if not text:
        return []
    found: list[str] = []
    raw = text.lower().replace(" ", "")
    for token in re.split(r"[,;/+|]+", raw):
        if not token:
            continue
        if token in ("дт", "dt", "diesel", "дизель"):
            if "dt" not in found:
                found.append("dt")
        elif "газ" in token or "пропан" in token or "суг" in token or token == "gas":
            if "gas" not in found:
                found.append("gas")
        else:
            for m in re.findall(r"92|95|98|100", token):
                if m not in found:
                    found.append(m)
    return found


def format_fuels_human(fuels: list[str]) -> str:
    if not fuels:
        return "марка не указана"
    return " · ".join(FUEL_DISPLAY.get(f, f.upper()) for f in fuels)


def format_confidence(value: float | int | None) -> str:
    if value is None:
        return ""
    try:
        pct = int(round(float(value) * 100))
    except (TypeError, ValueError):
        return ""
    return f"уверенность {pct}%"


def format_age(value: str | None) -> str:
    ts = parse_ts(value)
    if not ts:
        return ""
    delta = now_msk() - ts
    mins = int(delta.total_seconds() // 60)
    if mins < 1:
        return "только что"
    if mins < 60:
        return f"{mins} мин назад"
    hours = mins // 60
    if hours < 24:
        return f"{hours} ч назад"
    return ts.strftime("%d.%m %H:%M")


def parse_fuel_filter(value: str | list[str] | None) -> list[str]:
    """Список марок для фильтра; пустой список = все марки."""
    if value is None:
        return list(DEFAULT_FUELS)
    if isinstance(value, list):
        out = [normalize_fuel(str(v)) for v in value if str(v).strip()]
        if not out or "all" in out:
            return []
        return [f for f in out if f in VALID_FUELS and f != "all"] or list(DEFAULT_FUELS)
    text = str(value).strip().lower()
    if not text or text == "all":
        return []
    if text in ("бензин", "бенз", "92+95", "92,95", "92/95", "92 95"):
        return list(DEFAULT_FUELS)
    parts = re.split(r"[,+/|\s]+", text)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        f = normalize_fuel(part)
        if f == "all":
            return []
        if f in VALID_FUELS and f not in out:
            out.append(f)
    return out or list(DEFAULT_FUELS)


def format_fuel_filter_label(fuels: list[str]) -> str:
    if not fuels:
        return "все марки"
    return " + ".join(FUEL_DISPLAY.get(f, f.upper()) for f in fuels)


def chat_fuel_filter(chat: dict[str, Any]) -> list[str]:
    return parse_fuel_filter(chat.get("fuel", DEFAULT_FUELS))


def fuel_matches_filter(station_fuels: list[str], filter_fuels: list[str]) -> bool:
    if not filter_fuels:
        return True
    if not station_fuels:
        return True
    return any(f in station_fuels for f in filter_fuels)


def fuel_matches_list(fuels: list[str], fuel: str) -> bool:
    return fuel_matches_filter(fuels, parse_fuel_filter(fuel))


def fuel_matches(fuels_now: str, fuel: str) -> bool:
    return fuel_matches_filter(parse_fuels_list(fuels_now), parse_fuel_filter(fuel))




def expand_bbox(bbox: list[float], pad: float = 0.025) -> list[float]:
    """Расширить область (~2–3 км) — Nominatim иногда обрезает крайние АЗС."""
    lat1, lon1, lat2, lon2 = [float(x) for x in bbox]
    return [lat1 - pad, lon1 - pad, lat2 + pad, lon2 + pad]

def geocode_city(name: str) -> dict[str, Any]:
    qs = urllib.parse.urlencode(
        {
            "q": name,
            "format": "json",
            "limit": 5,
            "featuretype": "city",
        }
    )
    req = urllib.request.Request(
        f"https://nominatim.openstreetmap.org/search?{qs}",
        headers={"User-Agent": "ai-assistant-gdebenz/1.0 (mishock24@gmail.com)"},
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        rows = json.loads(resp.read().decode("utf-8", errors="replace"))
    if not rows:
        raise ValueError(f"Город «{name}» не найден (Nominatim)")
    row = rows[0]
    for candidate in rows:
        if candidate.get("type") == "city":
            row = candidate
            break
    bb = [float(x) for x in row["boundingbox"]]
    # Nominatim: south, north, west, east
    lat1, lat2, lon1, lon2 = bb[0], bb[1], bb[2], bb[3]
    lat = float(row["lat"])
    lon = float(row["lon"])
    city = row.get("name") or name
    try:
        gde_city = gdebenz_client.reverse_city(lat, lon)
        if gde_city:
            city = gde_city
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        pass
    return {
        "city": city,
        "lat": lat,
        "lon": lon,
        "bbox": expand_bbox([lat1, lon1, lat2, lon2]),
        "display_name": row.get("display_name", city),
    }


def geocode_cities_union(raw_names: str) -> dict[str, Any]:
    names = [x.strip() for x in re.split(r"[;,|]+", raw_names) if x.strip()]
    if len(names) < 2:
        raise ValueError("Нужно указать минимум 2 города: /gdebenz города Симферополь, Бахчисарай")
    geos = [geocode_city(name) for name in names]
    bboxes = [g["bbox"] for g in geos]
    lat1 = min(float(b[0]) for b in bboxes)
    lon1 = min(float(b[1]) for b in bboxes)
    lat2 = max(float(b[2]) for b in bboxes)
    lon2 = max(float(b[3]) for b in bboxes)
    lat = sum(float(g["lat"]) for g in geos) / len(geos)
    lon = sum(float(g["lon"]) for g in geos) / len(geos)
    city_title = ", ".join(g["city"] for g in geos)
    return {
        "city": city_title,
        "lat": lat,
        "lon": lon,
        "bbox": [lat1, lon1, lat2, lon2],
        "display_name": f"Группа городов: {city_title}",
        "scope": "cities",
        "cities": [g["city"] for g in geos],
    }


def chat_cfg(cfg: dict[str, Any], chat_id: int) -> dict[str, Any]:
    default = dict(DEFAULT_CITY)
    default.update(
        {
            "enabled": False,
            "fuel": "92,95",
            "interval_min": 30,
            "scope": "city",
        }
    )
    return cfg.setdefault("chats", {}).setdefault(str(chat_id), default)


def is_quiet_hours(cfg: dict[str, Any]) -> bool:
    start = int(cfg.get("quiet_start", 23))
    end = int(cfg.get("quiet_end", 7))
    hour = now_msk().hour
    if start == end:
        return False
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end


def station_label(st: dict[str, Any]) -> str:
    brand = (st.get("brand") or st.get("name") or "АЗС").strip()
    addr = (st.get("addr") or "").strip()
    return f"{brand}, {addr}" if addr else brand


def summarize_stations(
    stations: list[dict[str, Any]],
    *,
    fuels_filter: list[str],
    fresh_minutes: int,
) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {
        "ok": [],
        "queue": [],
        "low": [],
        "limit": [],
        "no": [],
        "unknown": [],
    }
    cutoff = now_msk() - timedelta(minutes=fresh_minutes)
    for st in stations:
        status = norm_status(st.get("status"))
        if status not in groups:
            groups["unknown"].append(st)
            continue
        fuels = parse_fuels_list(st.get("fuels_now") or st.get("fuelsNow") or "")
        if not fuel_matches_filter(fuels, fuels_filter):
            continue
        updated = parse_ts(st.get("updated") or st.get("last_at"))
        if updated and updated < cutoff and status in ALERT_STATUSES:
            continue
        st = dict(st)
        st["status"] = status
        groups[status].append(st)
    return groups


def collect_fuel_stats(stations: list[dict[str, Any]]) -> dict[str, int]:
    """Сколько АЗС с отметками по каждой марке (среди активных статусов)."""
    stats: dict[str, int] = {k: 0 for k in ("92", "95", "98", "100", "dt", "gas")}
    for st in stations:
        status = norm_status(st.get("status"))
        if status not in ACTIVE_STATUSES or status == "no":
            continue
        fuels = parse_fuels_list(st.get("fuels_now") or st.get("fuelsNow") or "")
        if not fuels:
            continue
        for f in fuels:
            if f in stats:
                stats[f] += 1
    return stats


def enrich_station(st: dict[str, Any], *, with_recent: bool = False) -> dict[str, Any]:
    """Подтянуть детали, уверенность, марки, последние комментарии."""
    if st.get("source") not in (None, "", "gdebenz"):
        return st
    osm_id = st.get("osm_id")
    if not osm_id or str(osm_id).startswith("azsc_"):
        return st
    merged = dict(st)
    merged["status"] = norm_status(merged.get("status"))
    try:
        detail = gdebenz_client.fetch_station_detail(str(osm_id))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        detail = {}
    if detail:
        merged["status"] = norm_status(detail.get("status", merged.get("status")))
        merged["fuels_now"] = detail.get("fuelsNow", merged.get("fuels_now", ""))
        merged["updated"] = detail.get("updated", merged.get("last_at"))
        merged["confidence"] = detail.get("confidenceBase")
        merged["confirmations"] = detail.get("confirmations")
        merged["confirmations_fresh"] = detail.get("confirmationsFresh")
        merged["limited"] = bool(detail.get("limited"))
        merged["fresh_conflict"] = detail.get("freshConflict")
        merged["prices"] = detail.get("pricesNow") or {}
        merged["views"] = detail.get("views")
    if with_recent:
        try:
            merged["recent"] = gdebenz_client.fetch_recent_comments(str(osm_id), limit=3)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            merged["recent"] = []
    return merged


def latest_driver_note(st: dict[str, Any]) -> str:
    for item in st.get("recent") or []:
        detail = (item.get("detail") or "").strip()
        if detail:
            return detail
    conflict = st.get("fresh_conflict")
    if isinstance(conflict, dict):
        c_status = norm_status(conflict.get("status"))
        age = conflict.get("ageMin")
        if c_status and age is not None:
            label = STATUS_LABEL.get(c_status, c_status)
            return f"спорная отметка: {label}, {age} мин"
    if st.get("conflict"):
        return f"расхождение: {st.get('conflict')}"
    return ""


def format_station_rich(st: dict[str, Any]) -> list[str]:
    label = station_label(st)
    emoji = STATUS_EMOJI.get(st.get("status"), "⛽")
    fuels = parse_fuels_list(st.get("fuels_now") or st.get("fuelsNow") or "")
    parts = [f"{emoji} {label}"]
    sub: list[str] = []
    if fuels:
        sub.append(format_fuels_human(fuels))
    age = format_age(st.get("updated") or st.get("last_at"))
    if age:
        sub.append(age)
    conf = format_confidence(st.get("confidence"))
    if conf:
        sub.append(conf)
    conf_n = st.get("confirmations_fresh") or st.get("confirmations")
    if conf_n:
        sub.append(f"подтв. {conf_n}")
    if st.get("limited"):
        sub.append("лимит на отпуск")
    note = latest_driver_note(st)
    if sub:
        parts.append("   " + " · ".join(sub))
    if note:
        parts.append(f"   💬 {note}")
    return parts


def format_status_text(chat: dict[str, Any], cfg: dict[str, Any], *, fast: bool = False) -> str:
    """Сводка по всем источникам из FUEL_SOURCES.md."""
    return fuel_hub.build_status_report(chat, cfg, fast=fast)


def station_snapshot(st: dict[str, Any]) -> dict[str, Any]:
    fuels = parse_fuels_list(st.get("fuels_now") or st.get("fuelsNow") or "")
    return {
        "status": norm_status(st.get("status")),
        "fuels_now": ",".join(fuels) if fuels else (st.get("fuels_now") or ""),
        "fuels_list": fuels,
        "updated": st.get("updated") or st.get("last_at") or "",
        "label": station_label(st),
        "confidence": st.get("confidence"),
        "limited": st.get("limited"),
        "note": latest_driver_note(st),
    }


def detect_alerts(
    prev: dict[str, Any],
    current: dict[str, dict[str, Any]],
    *,
    fuels_filter: list[str],
    fresh_minutes: int,
) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []
    cutoff = now_msk() - timedelta(minutes=fresh_minutes)
    for osm_id, snap in current.items():
        status = snap.get("status") or ""
        if status not in ALERT_STATUSES:
            continue
        fuels_list = snap.get("fuels_list") or parse_fuels_list(snap.get("fuels_now", ""))
        if not fuel_matches_filter(fuels_list, fuels_filter):
            continue
        updated = parse_ts(snap.get("updated"))
        if updated and updated < cutoff:
            continue
        old = (prev.get("stations") or {}).get(osm_id, {})
        old_status = old.get("status") or ""
        if old_status == status and old.get("updated") == snap.get("updated"):
            continue
        if old_status in ALERT_STATUSES and old_status == status:
            continue
        alerts.append(
            {
                "osm_id": osm_id,
                "status": status,
                "label": snap.get("label", osm_id),
                "fuels_now": snap.get("fuels_now", ""),
                "fuels_list": fuels_list,
                "updated": snap.get("updated", ""),
                "confidence": snap.get("confidence"),
                "limited": snap.get("limited"),
                "note": snap.get("note", ""),
                "kind": "new_ok" if status == "ok" else "new_queue",
            }
        )
    return alerts


def format_alert(chat: dict[str, Any], alert: dict[str, Any]) -> str:
    emoji = STATUS_EMOJI.get(alert["status"], "⛽")
    fuels_filter = chat_fuel_filter(chat)
    lines = [
        f"{emoji} ГдеБЕНЗ · {chat.get('city', '?')}",
        "",
    ]
    if alert["status"] == "ok":
        lines.append("Появился бензин (отметка водителей):")
    else:
        lines.append("Формируется очередь (отметка водителей):")
    lines.append(f"  {alert['label']}")
    fuels_list = alert.get("fuels_list") or parse_fuels_list(alert.get("fuels_now", ""))
    if fuels_list:
        lines.append(f"  В продаже: {format_fuels_human(fuels_list)}")
    elif fuels_filter:
        lines.append(f"  Фильтр чата: {format_fuel_filter_label(fuels_filter)}")
    else:
        lines.append("  Марки: не указаны водителями")
    if alert.get("updated"):
        age = format_age(alert["updated"])
        lines.append(f"  Время: {alert['updated']}" + (f" ({age})" if age else ""))
    conf = format_confidence(alert.get("confidence"))
    if conf:
        lines.append(f"  {conf.capitalize()}")
    if alert.get("limited"):
        lines.append("  ⚠️ Лимит на отпуск")
    if alert.get("note"):
        lines.append(f"  💬 {alert['note']}")
    lines.extend(
        [
            "",
            "Краудсорсинг — не официальные данные. Проверьте на месте.",
            "https://gdebenz.ru/",
        ]
    )
    return "\n".join(lines)


def send_telegram(chat_id: int, text: str) -> bool:
    load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        logging.error("TELEGRAM_BOT_TOKEN не задан")
        return False
    chunk = 3500
    ok = True
    for i in range(0, len(text), chunk):
        body = urllib.parse.urlencode(
            {"chat_id": chat_id, "text": text[i : i + chunk]}
        ).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=body,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
            ok = ok and bool(data.get("ok"))
        except OSError as exc:
            logging.error("telegram send failed chat=%s: %s", chat_id, exc)
            ok = False
    return ok




def run_qr_monitor() -> int:
    """Напоминания по очереди QR до 21:00 МСК."""
    cfg = load_config()
    if monitoring_is_disabled(cfg):
        logging.info("qr-monitor skipped: monitoring_disabled")
        return 0
    sent = process_pending_monitors(cfg, send_fn=send_telegram)
    if sent:
        save_config(cfg)
    logging.info("qr-monitor done, reminders=%s", sent)
    return sent


def run_monitor(*, force: bool = False) -> int:
    cfg = load_config()
    if monitoring_is_disabled(cfg):
        logging.info("monitor skipped: monitoring_disabled")
        return 0
    state = load_state()
    if is_quiet_hours(cfg) and not force:
        logging.info("quiet hours, skip monitor")
        return 0

    sent = 0
    now = now_msk()
    for chat_id_s, chat in cfg.get("chats", {}).items():
        if not chat.get("enabled"):
            continue
        interval = max(5, int(chat.get("interval_min", 30)))
        last_check = parse_ts(chat.get("last_check"))
        if not force and last_check and now - last_check < timedelta(minutes=interval):
            continue

        bbox = chat.get("bbox") or []
        if len(bbox) != 4:
            logging.warning("chat %s: bbox not set", chat_id_s)
            continue

        try:
            results = fuel_hub.collect_all_stations(chat, cfg, fast=True)
        except Exception as exc:
            logging.error("multi-source fetch failed chat=%s: %s", chat_id_s, exc)
            continue

        chat_state = state.setdefault(chat_id_s, {"stations": {}, "sources": {}})
        alerts = fuel_hub.detect_multi_alerts(
            chat_state,
            results,
            fuels_filter=chat_fuel_filter(chat),
            fresh_minutes=int(cfg.get("fresh_minutes", 45)),
        )

        chat["last_check"] = now.strftime("%Y-%m-%d %H:%M:%S")
        merged = fuel_hub.merge_state(chat_state, results)
        chat_state["stations"] = merged["stations"]
        chat_state["sources"] = merged["sources"]

        if alerts:
            for alert in alerts[:5]:
                msg = fuel_hub.format_multi_alert(chat, alert)
                if notify_fuel_alert(cfg, chat, int(chat_id_s), msg, send_telegram):
                    sent += 1
            if len(alerts) > 5:
                notify_fuel_alert(
                    cfg,
                    chat,
                    int(chat_id_s),
                    f"… и ещё {len(alerts) - 5} новых отметок. /gdebenz — сводка.",
                    send_telegram,
                )

    save_config(cfg)
    save_state(state)
    logging.info("monitor done, alerts_sent=%s", sent)
    return sent


def format_config_text(chat: dict[str, Any]) -> str:
    bbox = chat.get("bbox") or []
    bbox_s = (
        f"{bbox[0]:.3f}…{bbox[2]:.3f} lat, {bbox[1]:.3f}…{bbox[3]:.3f} lon"
        if len(bbox) == 4
        else "не задан"
    )
    fuels_filter = chat_fuel_filter(chat)
    fuel_s = format_fuel_filter_label(fuels_filter)
    return "\n".join(
        [
            "⚙️ ГдеБЕНЗ — настройки чата",
            f"Город: {chat.get('city', 'Симферополь')} (по умолчанию Симферополь)",
            f"Режим: {chat.get('scope', 'city')}",
            f"Мониторинг: {'вкл' if chat.get('enabled') else 'выкл'}",
            f"Интервал: {chat.get('interval_min', 10)} мин",
            f"Топливо: {fuel_s}",
            f"Область: {bbox_s}",
            f"Последняя проверка: {chat.get('last_check') or '—'}",
            "",
            "Команды:",
            "/gdebenz — сводка (город, марки, уверенность)",
            "/gdebenz город <название> — другой город",
            "/gdebenz города <г1, г2> — несколько городов (общий bbox)",
            "/gdebenz регион крым — весь полуостров",
            "/gdebenz сброс — снова Симферополь",
            "/gdebenz on | off",
            "/gdebenz топливо 92,95 | 95 | дт | all",
            "/gdebenz интервал 10",
            "/gdebenz источники",
            "/gdebenz qr — справка · /gdebenz qr получить — заявка до 21:00",
        ]
    )


def handle_telegram_command(token: str, chat_id: int, arg: str, *, fast: bool = False) -> str:
    """Обработка /gdebenz … — возвращает текст ответа (отправляет вызывающий)."""
    cfg = load_config()
    chat = chat_cfg(cfg, chat_id)
    parts = arg.split() if arg else []
    if not parts:
        save_config(cfg)
        return format_status_text(chat, cfg, fast=fast)

    sub = parts[0].lower()
    rest = " ".join(parts[1:]).strip()

    if sub in ("on", "вкл", "start", "старт"):
        if monitoring_is_disabled(cfg):
            return (
                "⏸ Автомониторинг бензина отключён глобально "
                "(по запросу: без поиска, почты и Telegram-пушей).\n"
                "Разовую сводку: /gdebenz"
            )
        chat["enabled"] = True
        save_config(cfg)
        return (
            f"✅ Мониторинг ГдеБЕНЗ включён для {chat.get('city', 'Симферополь')}.\n"
            f"Проверка каждые {chat.get('interval_min', 10)} мин.\n"
            f"Пуш: бензин (есть) или очередь · марки и уверенность в сообщении.\n"
            "/gdebenz — полная сводка"
        )

    if sub in ("off", "выкл", "stop", "стоп"):
        chat["enabled"] = False
        save_config(cfg)
        return "⏸ Мониторинг ГдеБЕНЗ выключен для этого чата."

    if sub in ("status", "cfg", "config", "настройки", "статус"):
        save_config(cfg)
        return format_config_text(chat)

    if sub in ("city", "город", "гор"):
        if not rest:
            return (
                f"Сейчас: {chat.get('city', 'Симферополь')}\n"
                "Пример: /gdebenz город Краснодар\n"
                "Сброс на Симферополь: /gdebenz сброс"
            )
        try:
            geo = geocode_city(rest)
        except (ValueError, urllib.error.URLError, TimeoutError) as exc:
            return f"Не удалось найти город: {exc}"
        chat.update(geo)
        chat["scope"] = "city"
        chat.pop("cities", None)
        save_config(cfg)
        header = (
            f"📍 Город: {chat['city']}\n"
            f"{geo.get('display_name', '')}\n\n"
        )
        return header + fuel_hub.build_status_report(chat, cfg, fast=fast)

    if sub in ("cities", "города"):
        if not rest:
            return (
                "Пример: /gdebenz города Симферополь, Бахчисарай, Севастополь\n"
                "Соберу общий bbox и покажу АЗС по всей зоне."
            )
        try:
            geo = geocode_cities_union(rest)
        except (ValueError, urllib.error.URLError, TimeoutError) as exc:
            return f"Не удалось собрать список городов: {exc}"
        chat.update(geo)
        save_config(cfg)
        header = (
            f"📍 Режим городов: {chat['city']}\n"
            f"{geo.get('display_name', '')}\n\n"
        )
        return header + fuel_hub.build_status_report(chat, cfg, fast=fast)

    if sub in ("region", "регион"):
        region = rest.strip().lower()
        if region not in ("крым", "crimea", "рк", "республикакрым"):
            return "Сейчас поддержан регион: /gdebenz регион крым"
        chat.update(dict(CRIMEA_REGION))
        chat["scope"] = "region"
        chat["cities"] = ["Симферополь", "Севастополь", "Бахчисарай", "Ялта", "Евпатория", "Керчь", "Феодосия"]
        save_config(cfg)
        return (
            "📍 Режим: весь Крым (общий bbox)\n"
            "/gdebenz — сводка по полуострову (включая межгород)."
        )

    if sub in ("reset", "сброс", "default"):
        chat.update(dict(DEFAULT_CITY))
        chat["scope"] = "city"
        chat.pop("cities", None)
        save_config(cfg)
        return (
            f"📍 Снова по умолчанию: {DEFAULT_CITY['city']}\n"
            "/gdebenz — сводка · /gdebenz on — пуш"
        )

    if sub in ("fuel", "топливо", "бенз", "марка"):
        if not rest:
            cur = format_fuel_filter_label(chat_fuel_filter(chat))
            return (
                f"Сейчас: {cur}\n"
                "По умолчанию: АИ-92 + АИ-95\n"
                "Примеры: /gdebenz топливо 92,95 · /gdebenz топливо 95 · all"
            )
        if rest.strip().lower() in ("бензин", "бенз", "default", "дефолт"):
            chat["fuel"] = "92,95"
            save_config(cfg)
            return "Фильтр: АИ-92 + АИ-95 (по умолчанию)"
        fuels = parse_fuel_filter(rest)
        if not fuels and rest.strip().lower() != "all":
            return "Марки: 92, 95, 98, 100, дт, газ, all (можно несколько: 92,95)"
        chat["fuel"] = rest.strip().lower() if rest.strip().lower() == "all" else ",".join(fuels)
        save_config(cfg)
        return f"Фильтр топлива: {format_fuel_filter_label(fuels)}"


    if sub in ("qr", "кюар", "код", "qr-код", "qrкод"):
        rest_l = rest.lower().strip()
        obtain_words = ("получить", "заказать", "запросить", "запрос", "order", "get", "obtain")
        if any(rest_l == w or rest_l.startswith(w + " ") for w in obtain_words):
            rest_args = rest
            for w in obtain_words:
                if rest_l.startswith(w):
                    rest_args = rest[len(w):].strip()
                    break
            city = chat.get("city", "Симферополь")
            result = obtain_qr(city, rest_args, chat, queue=True)
            save_config(cfg)
            return result.message
        if rest_l in ("отмена", "cancel", "стоп", "stop"):
            save_config(cfg)
            return cancel_pending(chat)
        if rest_l in ("очередь", "статус", "status", "pending"):
            save_config(cfg)
            return pending_status(chat)
        if rest_l in ("готово", "рег", "регистрация", "done", "ok", "да"):
            key = detect_qr_region(chat.get("city", ""))
            chat["qr_registered_at"] = datetime.now(MSK).strftime("%Y-%m-%d %H:%M")
            chat["qr_region"] = key or ""
            chat.pop("qr_pending", None)
            chat.pop("qr_pending_notified_at", None)
            save_config(cfg)
            return (
                "✅ Отметила: QR получен / регистрация пройдена.\n"
                "Перед заправкой сверьте карту и сводку /gdebenz.\n"
                "Следующий код — по правилам региона (обычно раз в 7 дней)."
            )
        if rest_l in ("сброс", "reset", "нет"):
            chat.pop("qr_registered_at", None)
            chat.pop("qr_region", None)
            chat.pop("qr_pending", None)
            chat.pop("qr_pending_notified_at", None)
            save_config(cfg)
            return "Отметка регистрации QR сброшена."
        city_for_qr = rest if rest else chat.get("city", "Симферополь")
        save_config(cfg)
        help_text = format_qr_help(city_for_qr, chat)
        return help_text + "\n\nЗапросить за вас: /gdebenz qr получить [михаил|анна] [92|95]"

    if sub in ("sources", "источники", "src"):
        bbox = chat.get("bbox") or []
        return fuel_hub.build_sources_status(
            cfg,
            bbox=[float(x) for x in bbox] if len(bbox) == 4 else None,
        )

    if sub in ("interval", "интервал", "период"):
        if not rest or not rest.isdigit():
            return f"Сейчас: {chat.get('interval_min', 10)} мин\nПример: /gdebenz интервал 10"
        val = max(5, min(60, int(rest)))
        chat["interval_min"] = val
        save_config(cfg)
        return f"Интервал проверки: {val} мин"

    if sub in ("check", "проверка", "сейчас"):
        save_config(cfg)
        return format_status_text(chat, cfg, fast=False)

    save_config(cfg)
    return (
        "Команды ГдеБЕНЗ:\n"
        "/gdebenz — сводка (марки, уверенность, очереди)\n"
        "/gdebenz on — пуш в чат\n"
        "/gdebenz город … · /gdebenz города г1,г2 · /gdebenz регион крым · /gdebenz сброс\n"
        "/gdebenz топливо 92,95 | 95 | all · /gdebenz qr · /gdebenz интервал 10 · /gdebenz настройки"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Мониторинг ГдеБЕНЗ для ai_assistant")
    parser.add_argument("--monitor", action="store_true", help="Прогон мониторинга (cron/timer)")
    parser.add_argument("--qr-monitor", action="store_true", help="Напоминания QR-заявок до 21:00")
    parser.add_argument("--status", action="store_true", help="Текстовая сводка в stdout")
    parser.add_argument("--chat-id", type=int, default=0, help="chat_id для --status")
    parser.add_argument("--force", action="store_true", help="Игнорировать quiet hours и интервал")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s gdebenz-fuel %(message)s",
    )

    if args.qr_monitor:
        run_qr_monitor()
        return 0

    if args.monitor:
        run_monitor(force=args.force)
        return 0

    if args.status:
        cfg = load_config()
        chat_id = args.chat_id
        if not chat_id:
            chats = cfg.get("chats", {})
            chat_id = int(next(iter(chats))) if chats else 0
        chat = chat_cfg(cfg, chat_id)
        print(format_status_text(chat, cfg))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
