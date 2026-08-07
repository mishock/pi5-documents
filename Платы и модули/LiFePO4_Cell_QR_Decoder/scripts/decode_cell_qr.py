#!/usr/bin/env python3
"""Декодирование заводского QR / Data Matrix ячейки LiFePO4 через онлайн-сервисы."""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

SOURCES = [
    {
        "id": "basen",
        "name": "Basen",
        "url": "https://www.basengroup.com/index.php?m=decode&f=index&v=decode",
        "referer": "https://www.basengroup.com/Service/QR-DECODER/",
    },
    {
        "id": "xihopower",
        "name": "Xiho Power",
        "url": "https://www.xihopower.com/index.php?m=decode&f=index&v=decode",
        "referer": "https://www.xihopower.com/ru/qr-decoder/Cell_QR_Decoder/",
    },
]

# Локальный разбор по GB-трассировке (дополняет ответ сайтов)
MFR = {
    "001": "CATL",
    "02Y": "EVE",
    "04Q": "EVE Power",
    "081": "REPT",
    "08I": "REPT",
    "08B": "Lishen",
    "02C": "Lishen",
    "0AL": "Ganfeng",
    "0B5": "CALB",
    "OB5": "CALB",
    "0IJ": "Hithium",
    "03H": "Gotion",
    "07H": "Higee",
    "0F4": "BYD",
}
PTYPE = {"C": "ячейка", "M": "модуль", "P": "pack"}
CHEM = {
    "A": ("NiMH", 1.2),
    "B": ("LiFePO4", 3.2),
    "C": ("LiMn2O4", 3.0),
    "D": ("LiCoO2", 3.7),
    "E": ("NMC/тернар", 3.7),
    "F": ("суперконденсатор", None),
    "G": ("LTO", 2.3),
    "Z": ("другое", None),
}
# Коды спецификации EVE / общие (как в публичных декодерах)
SPEC = {
    "64": ("LF90K", 90),
    "65": ("LF105", 105),
    "66": ("LF280", 280),
    "68": ("LF50", 50),
    "6C": ("LF100L", 100),
    "6D": ("LF100MA", 100),
    "71": ("LF280N", 280),
    "72": ("LF230", 230),
    "73": ("LF304", 304),
    "75": ("LF173", 173),
    "76": ("LF280K", 280),
    "24": ("302Ah", 302),
    "31": ("280Ah", 280),
    "37": ("L173F230", 230),
}

DAY_MAP = {
    **{str(i): i for i in range(1, 10)},
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    "G": 16,
    "H": 17,
    "J": 18,
    "K": 19,
    "L": 20,
    "M": 21,
    "N": 22,
    "P": 23,
    "R": 24,
    "S": 25,
    "T": 26,
    "U": 27,
    "V": 28,
    "X": 29,
    "Y": 30,
    "Z": 31,
}


def normalize_code(raw: str) -> str:
    s = re.sub(r"[\s\-_/\\|]+", "", raw.strip().upper())
    # частые OCR-ошибки
    return s


def validate_shape(code: str) -> list[str]:
    notes: list[str] = []
    if len(code) not in (19, 24, 26):
        notes.append(f"длина {len(code)} (ожидается 24, реже 19/26)")
    else:
        notes.append(f"длина {len(code)} — ок")
    if len(code) >= 4:
        if code[3] in "CPM":
            notes.append(f"4-й символ «{code[3]}» — ок (C/P/M)")
        else:
            notes.append(
                f"4-й символ «{code[3]}» — подозрительно (нужен C/P/M; возможно перепутаны половины)"
            )
    return notes


def parse_local(code: str) -> dict[str, Any]:
    out: dict[str, Any] = {"code": code}
    if len(code) < 17:
        return out
    mfr_c, ptype_c, chem_c = code[0:3], code[3], code[4]
    spec_c = code[5:7] if len(code) >= 7 else ""
    trace = code[7:14] if len(code) >= 14 else ""
    date_c = code[14:17]
    serial = code[17:24] if len(code) >= 24 else code[17:]

    out["manufacturer_code"] = mfr_c
    out["manufacturer_local"] = MFR.get(mfr_c, "неизвестно")
    out["product_type_code"] = ptype_c
    out["product_type_local"] = PTYPE.get(ptype_c, "неизвестно")
    chem = CHEM.get(chem_c)
    out["chemistry_code"] = chem_c
    if chem:
        out["chemistry_local"], out["voltage_local_v"] = chem
    out["spec_code"] = spec_c
    if spec_c in SPEC:
        model, cap = SPEC[spec_c]
        out["model_local"] = model
        out["capacity_local_ah"] = cap
    out["trace"] = trace
    out["date_code"] = date_c
    out["serial"] = serial

    # дата
    ych, mch, dch = date_c[0], date_c[1], date_c[2]
    year = month = day = None
    if ych.isalpha():
        year = 2020 + (ord(ych) - ord("A"))
    elif ych.isdigit() and ych != "0":
        year = 2010 + int(ych)
    if mch.isalpha() and mch in "ABC":
        month = 10 + (ord(mch) - ord("A"))
    elif mch.isdigit() and mch != "0":
        month = int(mch)
    day = DAY_MAP.get(dch)
    if year and month and day:
        out["production_date_local"] = f"{day:02d}.{month:02d}.{year}"
        out["production_date_iso"] = f"{year:04d}-{month:02d}-{day:02d}"
    return out


def fetch_source(src: dict[str, str], code: str, timeout: float = 25.0) -> dict[str, Any]:
    qs = urllib.parse.urlencode({"code": code})
    url = f"{src['url']}?{qs}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Referer": src["referer"],
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
        fields = parse_html_fields(data.get("res") or "")
        return {
            "ok": True,
            "http_ok": True,
            "api_code": data.get("code"),
            "raw_res": data.get("res"),
            "fields": fields,
            "error": None,
        }
    except Exception as exc:  # noqa: BLE001 — нужен полный отчёт по источникам
        return {
            "ok": False,
            "http_ok": False,
            "api_code": None,
            "raw_res": None,
            "fields": {},
            "error": str(exc),
        }


def parse_html_fields(fragment: str) -> dict[str, str]:
    if not fragment or "Invalid" in fragment:
        return {}
    text = html_lib.unescape(fragment)
    fields: dict[str, str] = {}
    for m in re.finditer(
        r"<dt>\s*([^<:]+)\s*:?\s*</dt>\s*<dd>\s*(.*?)\s*</dd>",
        text,
        flags=re.I | re.S,
    ):
        key = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(":")
        val = re.sub(r"<[^>]+>", "", m.group(2))
        val = re.sub(r"\s+", " ", val).strip()
        if key and val:
            fields[key] = val
    # статусные строки
    for m in re.finditer(
        r'id="(iscode|islength)"[^>]*>\s*([^<]+)',
        text,
        flags=re.I,
    ):
        fields[m.group(1)] = m.group(2).strip()
    return fields


LABEL_RU = {
    "Manufacturer": "Производитель",
    "Product Type": "Тип изделия",
    "Battery Type": "Химия / тип АКБ",
    "Nominal Capacity": "Номинальная ёмкость",
    "Nominal Voltage": "Номинальное напряжение",
    "Production Date": "Дата производства",
    "Product series": "Серия",
    "Product Attribute": "Атрибут",
    "Subsidiary": "Подразделение",
    "Address": "Адрес",
    "Manufacturer Website": "Сайт производителя",
    "Recycled": "Вторичка / recycled",
}


def merge_fields(results: list[dict[str, Any]]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for r in results:
        for k, v in (r.get("fields") or {}).items():
            if k.startswith("is"):
                continue
            if not v or v.lower() in {"unknown", "n/a", "-"}:
                continue
            if k not in merged:
                merged[k] = v
            elif v not in merged[k] and len(v) > len(merged[k]):
                # более подробное значение
                merged[k] = f"{merged[k]} | {v}"
            elif v not in merged[k]:
                merged[k] = f"{merged[k]} | {v}"
    return merged


def format_report(code: str, local: dict[str, Any], sources: dict[str, Any]) -> str:
    merged = merge_fields(list(sources.values()))
    lines: list[str] = []
    lines.append(f"Код: `{code}`")
    shape = validate_shape(code)
    lines.append("Проверка формата: " + "; ".join(shape))
    lines.append("")
    lines.append("Характеристики (максимум из сайтов + локальный разбор):")

    # приоритет: сайты, потом локально
    ordered_keys = [
        "Manufacturer",
        "Product Type",
        "Battery Type",
        "Nominal Capacity",
        "Nominal Voltage",
        "Production Date",
        "Product series",
        "Product Attribute",
        "Subsidiary",
        "Address",
        "Manufacturer Website",
        "Recycled",
    ]
    shown = set()
    for k in ordered_keys:
        if k in merged:
            lines.append(f"- {LABEL_RU.get(k, k)}: {merged[k]}")
            shown.add(k)
    for k, v in merged.items():
        if k not in shown:
            lines.append(f"- {LABEL_RU.get(k, k)}: {v}")

    # дополнения локально, если сайты молчат
    extras = []
    if "Manufacturer" not in merged and local.get("manufacturer_local"):
        extras.append(
            f"Производитель (локально): {local['manufacturer_local']} ({local.get('manufacturer_code')})"
        )
    cap_txt = str(merged.get("Nominal Capacity", ""))
    if local.get("model_local") and local["model_local"] not in cap_txt:
        extras.append(
            f"Модель (локально по коду {local.get('spec_code')}): "
            f"{local['model_local']}"
            + (
                f", {local['capacity_local_ah']} А·ч"
                if local.get("capacity_local_ah")
                else ""
            )
        )
    if local.get("serial"):
        extras.append(f"Серийный номер: {local['serial']}")
    if local.get("trace"):
        extras.append(f"Трассировка (линия/заказ/завод): {local['trace']}")
    if local.get("production_date_local") and "Production Date" not in merged:
        extras.append(f"Дата (локально): {local['production_date_local']}")
    if extras:
        lines.append("")
        lines.append("Дополнительно:")
        for e in extras:
            lines.append(f"- {e}")

    lines.append("")
    lines.append("Источники:")
    for sid, r in sources.items():
        if r.get("ok") and r.get("fields"):
            lines.append(f"- {SOURCES_BY_ID[sid]['name']}: OK")
        elif r.get("ok"):
            lines.append(f"- {SOURCES_BY_ID[sid]['name']}: ответ пустой / invalid")
        else:
            lines.append(f"- {SOURCES_BY_ID[sid]['name']}: ошибка ({r.get('error')})")
    lines.append("- Gobel / Hakadi: вручную в браузере (с Pi часто Cloudflare 403)")
    return "\n".join(lines)


SOURCES_BY_ID = {s["id"]: s for s in SOURCES}


def decode(code_raw: str, save_dir: Path | None = None) -> dict[str, Any]:
    code = normalize_code(code_raw)
    local = parse_local(code)
    sources: dict[str, Any] = {}
    for src in SOURCES:
        sources[src["id"]] = fetch_source(src, code)
    payload = {
        "checked_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "code": code,
        "code_raw": code_raw,
        "validation": validate_shape(code),
        "local": local,
        "sources": {
            sid: {
                "ok": r.get("ok"),
                "error": r.get("error"),
                "fields": r.get("fields"),
            }
            for sid, r in sources.items()
        },
        "merged": merge_fields(list(sources.values())),
        "report_ru": format_report(code, local, sources),
    }
    if save_dir is not None:
        save_dir.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Z0-9]+", "_", code)[:48]
        path = save_dir / f"decode_{safe}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        payload["saved_to"] = str(path)
    return payload


def main() -> int:
    ap = argparse.ArgumentParser(description="Декод QR ячейки LiFePO4")
    ap.add_argument("code", nargs="?", help="24-символьный код (или из stdin)")
    ap.add_argument("--json", action="store_true", help="полный JSON в stdout")
    ap.add_argument(
        "--save",
        action="store_true",
        help="сохранить JSON в notes/",
    )
    args = ap.parse_args()
    raw = args.code or sys.stdin.read()
    if not raw or not raw.strip():
        print("Укажите код ячейки", file=sys.stderr)
        return 2
    base = Path(__file__).resolve().parents[1]
    save_dir = base / "notes" if args.save else None
    result = decode(raw, save_dir=save_dir)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["report_ru"])
        if result.get("saved_to"):
            print(f"\nСохранено: {result['saved_to']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
