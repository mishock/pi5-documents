#!/usr/bin/env python3
"""Циклический спот-трейдер Bybit (Pi 5). Сигнал → buy → TP + SL → повтор.
Требует bybit-auto-confirm.json enabled."""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
CONFIRM_FILE = Path(
    os.environ.get(
        "BYBIT_AUTO_CONFIRM",
        "/home/pi/Documents/.cursor/data/bybit-auto-confirm.json",
    )
)
STATE_FILE = Path(
    os.environ.get(
        "BYBIT_AUTO_TRADER_STATE",
        "/home/pi/Documents/.cursor/data/bybit-auto-trader-state.json",
    )
)
MIN_USDT = float(os.environ.get("BYBIT_AUTO_MIN_USDT", "5"))
TP_PCT = float(os.environ.get("BYBIT_AUTO_TP_PCT", "4.0"))
SL_PCT = float(os.environ.get("BYBIT_AUTO_SL_PCT", "7.0"))
DRAWDOWN_ALERT_PCT = float(os.environ.get("BYBIT_AUTO_DRAWDOWN_ALERT_PCT", "5.0"))
# Только ликвидные пары. SUI оставлен до закрытия уже существующей позиции.
TRADE_COINS = {"BTC", "ETH", "SOL", "SUI"}
RESERVE_TO_USDT = {"ETH"}  # продаём в USDT перед входом в альты
QUIET_TZ = os.environ.get("BYBIT_AUTO_TZ", "Europe/Moscow")


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


_env = _load("bybit_load_env", ROOT / "bybit-load-env.py")
_env.apply()
_http = _load("bybit_http", ROOT / "bybit-http.py")
_pi5 = _load("pi5only", ROOT / "bybit-pi5-only.py")
_pi5.require_pi5()
_watch = _load("bybit_watch", ROOT / "bybit-watch.py")
_order = _load("bybit_spot_order", ROOT / "bybit-spot-order.py")

API_KEY = os.environ.get("BYBIT_API_KEY", "")
PRIV_PATH = os.environ.get("BYBIT_API_PRIVATE_KEY_PATH", "")
SECRET = os.environ.get("BYBIT_API_SECRET", "")
BASE = _order.BASE
RECV = os.environ.get("BYBIT_RECV_WINDOW", "60000")
SIGN_RSA = bool(PRIV_PATH and os.path.isfile(os.path.expanduser(PRIV_PATH)))
PRIV_KEY = os.path.expanduser(PRIV_PATH) if SIGN_RSA else None


def _halt(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


if not API_KEY or not (SIGN_RSA or SECRET):
    _halt("Bybit API не настроен")


def server_ms() -> int:
    with _http.urlopen(f"{BASE}/v5/market/time", timeout=15) as r:
        return int(json.load(r)["result"]["timeSecond"]) * 1000


def sign_get(endpoint: str, query: str) -> dict:
    ts = str(server_ms())
    param = f"{ts}{API_KEY}{RECV}{query}"
    if SIGN_RSA:
        proc = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", PRIV_KEY, "-binary"],
            input=param.encode(),
            capture_output=True,
            check=True,
        )
        sig = __import__("base64").b64encode(proc.stdout).decode().strip()
        sign_type = "2"
    else:
        proc = subprocess.run(
            ["openssl", "dgst", "-sha256", "-hmac", SECRET],
            input=param,
            capture_output=True,
            text=True,
            check=True,
        )
        sig = proc.stdout.split()[-1]
        sign_type = "1"
    url = f"{BASE}/v5/{endpoint}"
    if query:
        url += "?" + query
    headers = {
        "X-BAPI-API-KEY": API_KEY,
        "X-BAPI-TIMESTAMP": ts,
        "X-BAPI-SIGN": sig,
        "X-BAPI-RECV-WINDOW": RECV,
        "User-Agent": "bybit-auto-trader/1.0",
    }
    if SIGN_RSA:
        headers["X-BAPI-SIGN-TYPE"] = sign_type
    with _http.urlopen(urllib.request.Request(url, headers=headers), timeout=25) as r:
        return json.load(r)


def sign_post(endpoint: str, body: dict) -> dict:
    time.sleep(0.35)
    ts = str(server_ms())
    payload = json.dumps(body, separators=(",", ":"))
    param = f"{ts}{API_KEY}{RECV}{payload}"
    if SIGN_RSA:
        proc = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", PRIV_KEY, "-binary"],
            input=param.encode(),
            capture_output=True,
            check=True,
        )
        sig = __import__("base64").b64encode(proc.stdout).decode().strip()
        sign_type = "2"
    else:
        proc = subprocess.run(
            ["openssl", "dgst", "-sha256", "-hmac", SECRET],
            input=param,
            capture_output=True,
            text=True,
            check=True,
        )
        sig = proc.stdout.split()[-1]
        sign_type = "1"
    headers = {
        "Content-Type": "application/json",
        "X-BAPI-API-KEY": API_KEY,
        "X-BAPI-TIMESTAMP": ts,
        "X-BAPI-SIGN": sig,
        "X-BAPI-RECV-WINDOW": RECV,
        "User-Agent": "bybit-auto-trader/1.0",
    }
    if SIGN_RSA:
        headers["X-BAPI-SIGN-TYPE"] = sign_type
    req = urllib.request.Request(
        f"{BASE}/v5/{endpoint}",
        data=payload.encode(),
        headers=headers,
        method="POST",
    )
    with _http.urlopen(req, timeout=25) as r:
        return json.load(r)


def pct_from_conf(conf: dict, key: str, default: float) -> float:
    try:
        return float(conf.get(key, default))
    except (TypeError, ValueError):
        return default


def get_tp_sl_pcts(conf: dict) -> tuple[float, float]:
    return pct_from_conf(conf, "tp_pct", TP_PCT), pct_from_conf(conf, "sl_pct", SL_PCT)


def trail_enabled(conf: dict) -> bool:
    return bool(conf.get("trail_enable", False))


def update_entry_peak(st: dict, coin: str, entry: float, px: float) -> float:
    rec = st.setdefault("entries", {}).setdefault(coin, {})
    if not rec.get("entry"):
        rec["entry"] = entry
    peak = float(rec.get("peak") or rec.get("entry") or entry)
    peak = max(peak, px, entry)
    rec["peak"] = peak
    return peak


def compute_trail_sl(entry: float, peak: float, conf: dict) -> float:
    sl_pct = pct_from_conf(conf, "sl_pct", SL_PCT)
    be_pct = pct_from_conf(conf, "breakeven_pct", 3.0)
    be_lock = pct_from_conf(conf, "breakeven_lock_pct", 0.2)
    trail_start = pct_from_conf(conf, "trail_start_pct", 3.0)
    trail_dist = pct_from_conf(conf, "trail_distance_pct", 3.0)

    sl = price_from_entry(entry, sl_pct, up=False)
    gain_peak_pct = (peak / entry - 1) * 100 if entry > 0 else 0.0

    if gain_peak_pct >= be_pct:
        sl = max(sl, price_from_entry(entry, be_lock, up=True))
    if gain_peak_pct >= trail_start:
        sl = max(sl, peak * (1 - trail_dist / 100))
    return sl


def trail_mode_label(entry: float, peak: float, conf: dict) -> str:
    if entry <= 0:
        return "—"
    gain = (peak / entry - 1) * 100
    be_pct = pct_from_conf(conf, "breakeven_pct", 3.0)
    trail_start = pct_from_conf(conf, "trail_start_pct", 3.0)
    if gain >= trail_start:
        return "trailing"
    if gain >= be_pct:
        return "безубыток"
    return "начальный"


def _stop_trigger(order: dict | None) -> float:
    if not order:
        return 0.0
    return float(order.get("triggerPrice") or 0)


def _prices_close(a: float, b: float, tol_ratio: float = 0.002) -> bool:
    if a <= 0 or b <= 0:
        return False
    return abs(a - b) / b <= tol_ratio


def cancel_symbol_limit_sells(sym: str) -> None:
    d = sign_get("order/realtime", f"category=spot&symbol={sym}&openOnly=0")
    for o in (d.get("result") or {}).get("list") or []:
        if o.get("side") != "Sell":
            continue
        if o.get("orderStatus") not in ("New", "PartiallyFilled", "Untriggered"):
            continue
        trig = float(o.get("triggerPrice") or 0)
        if trig > 0 or o.get("stopOrderType"):
            continue
        if o.get("orderType") == "Limit":
            oid = o.get("orderId")
            if oid:
                _order.cancel_order(symbol=sym, order_id=str(oid))


def cancel_symbol_stop_sells(sym: str) -> None:
    d = sign_get("order/realtime", f"category=spot&symbol={sym}&openOnly=0")
    for o in (d.get("result") or {}).get("list") or []:
        if o.get("side") != "Sell":
            continue
        if o.get("orderStatus") not in ("New", "PartiallyFilled", "Untriggered"):
            continue
        trig = float(o.get("triggerPrice") or 0)
        if trig > 0 or o.get("stopOrderType"):
            oid = o.get("orderId")
            if oid:
                _order.cancel_order(symbol=sym, order_id=str(oid))


def place_stop_sell(
    sym: str,
    coin: str,
    qty: str,
    trigger_px: float,
    *,
    dry: bool,
) -> dict | None:
    if dry:
        return {"retCode": 0}
    return _order.place_stop_market_sell(
        symbol=sym,
        qty=qty,
        trigger_price=round_price(trigger_px),
        order_link_id=f"auto-sl-{coin.lower()}-{int(time.time())}",
    )


def place_tp_limit(
    sym: str,
    coin: str,
    qty: str,
    tp_px: float,
    entry: float,
    st: dict,
    *,
    dry: bool,
) -> dict | None:
    if dry:
        return {"retCode": 0}
    res = _order.place_order(
        symbol=sym,
        side="Sell",
        order_type="Limit",
        qty=qty,
        price=round_price(tp_px),
        order_link_id=f"auto-tp-{coin.lower()}-{int(time.time())}",
    )
    if res.get("retCode") == 0:
        st.setdefault("entries", {})[coin] = {
            "entry": entry,
            "tp": float(round_price(tp_px)),
            "source": "managed",
        }
    return res


def load_confirm() -> dict:
    if not CONFIRM_FILE.is_file():
        return {"enabled": False}
    return json.loads(CONFIRM_FILE.read_text(encoding="utf-8"))


def load_state() -> dict:
    if STATE_FILE.is_file():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_state(st: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    st["updated"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def wallet_rows() -> tuple[float, dict[str, float]]:
    data = sign_get("account/wallet-balance", "accountType=UNIFIED")
    if data.get("retCode") != 0:
        _halt(f"wallet-balance: {data.get('retMsg')}")
    acc = (data.get("result") or {}).get("list") or [{}]
    row = acc[0]
    avail = float(row.get("totalAvailableBalance") or 0)
    coins: dict[str, float] = {}
    for c in row.get("coin") or []:
        coin = c.get("coin")
        if not coin:
            continue
        # equity в единицах монеты: у BTC 0.0007 << 0.01 — старый порог eq>0.01
        # скрывал позицию и ломал trailing/SL.
        eq = float(c.get("equity") or c.get("walletBalance") or 0)
        if eq <= 0:
            continue
        usd = float(c.get("usdValue") or 0)
        if coin == "USDT" or coin in TRADE_COINS or usd >= 1.0:
            coins[coin] = eq
    return avail, coins


def open_sell_limits() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for sym in [f"{c}USDT" for c in TRADE_COINS]:
        d = sign_get("order/realtime", f"category=spot&symbol={sym}&openOnly=0")
        for o in (d.get("result") or {}).get("list") or []:
            if o.get("side") != "Sell":
                continue
            if o.get("orderStatus") not in ("New", "PartiallyFilled", "Untriggered"):
                continue
            trig = float(o.get("triggerPrice") or 0)
            if trig > 0 or o.get("stopOrderType"):
                continue
            if o.get("orderType") == "Limit":
                out[sym] = o
    return out


def open_stop_sells() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for sym in [f"{c}USDT" for c in TRADE_COINS]:
        d = sign_get("order/realtime", f"category=spot&symbol={sym}&openOnly=0")
        for o in (d.get("result") or {}).get("list") or []:
            if o.get("side") != "Sell":
                continue
            if o.get("orderStatus") not in ("New", "PartiallyFilled", "Untriggered"):
                continue
            trig = float(o.get("triggerPrice") or 0)
            if trig > 0 or o.get("stopOrderType"):
                out[sym] = o
    return out


def cancel_symbol_orders(sym: str) -> None:
    d = sign_get("order/realtime", f"category=spot&symbol={sym}&openOnly=0")
    for o in (d.get("result") or {}).get("list") or []:
        oid = o.get("orderId")
        if not oid:
            continue
        if o.get("orderStatus") in ("New", "PartiallyFilled", "Untriggered"):
            _order.cancel_order(symbol=sym, order_id=str(oid))


def resolve_entry(
    coin: str,
    sym: str,
    px: float,
    tp_pct: float,
    sells: dict[str, dict],
    st: dict,
) -> float:
    entries = st.setdefault("entries", {})
    rec = entries.get(coin) or {}
    if rec.get("entry"):
        return float(rec["entry"])
    if sym in sells:
        tp_px = float(sells[sym].get("price") or 0)
        if tp_px > 0:
            entry = tp_px / (1 + tp_pct / 100)
            entries[coin] = {"entry": entry, "tp": tp_px, "source": "inferred_tp"}
            return entry
    entries[coin] = {"entry": px, "source": "spot_now"}
    return px


def price_from_entry(entry: float, pct: float, *, up: bool) -> float:
    factor = 1 + pct / 100 if up else 1 - pct / 100
    return entry * factor


def manage_position(
    coin: str,
    sym: str,
    qty: float,
    conf: dict,
    st: dict,
    sells: dict[str, dict],
    stops: dict[str, dict],
    *,
    dry: bool,
    lines: list[str],
) -> bool:
    """TP/SL/trailing/soft-stop. True если позиция закрыта soft-stop."""
    tp_pct, sl_pct = get_tp_sl_pcts(conf)
    alert_pct = pct_from_conf(conf, "drawdown_alert_pct", DRAWDOWN_ALERT_PCT)
    px = spot_price(sym)
    entry = resolve_entry(coin, sym, px, tp_pct, sells, st)
    dd = (px / entry - 1) * 100 if entry > 0 else 0.0
    q = round_qty(sym, qty)
    _refresh_orders_if_qty_mismatch(coin, sym, q, sells, stops, dry=dry, lines=lines)

    if trail_enabled(conf):
        peak = update_entry_peak(st, coin, entry, px)
        target_sl = compute_trail_sl(entry, peak, conf)
        cur_trig = _stop_trigger(stops.get(sym))
        if cur_trig > 0:
            target_sl = max(target_sl, cur_trig)

        gain_now = (px / entry - 1) * 100 if entry > 0 else 0.0
        mode = trail_mode_label(entry, peak, conf)
        lines.append(
            f"📈 {coin}: {gain_now:+.1f}% · пик {round_price(peak)} · SL {round_price(target_sl)} ({mode})"
        )

        if sym in sells:
            lines.append(f"↻ {coin}: снят фикс. TP (режим trailing)")
            if not dry:
                cancel_symbol_limit_sells(sym)
            sells.pop(sym, None)

        stop_rec = stops.get(sym)
        if stop_rec and _order_qty_matches(stop_rec, q) and _prices_close(cur_trig, target_sl):
            lines.append(f"🛡️ {coin}: SL стоп @ {stop_rec.get('triggerPrice')}")
        else:
            if not dry and (stop_rec or sym in sells):
                cancel_symbol_stop_sells(sym)
            lines.append(f"🛡️ {coin}: SL → стоп @ {round_price(target_sl)}")
            if not dry:
                res = place_stop_sell(sym, coin, q, target_sl, dry=False)
                if res and res.get("retCode") != 0:
                    lines.append(f"  ⚠️ SL: {res.get('retMsg')}")
                else:
                    st.setdefault("entries", {})[coin] = {
                        "entry": entry,
                        "peak": peak,
                        "sl": float(round_price(target_sl)),
                        "source": "trail",
                    }

        soft_sl = target_sl
    else:
        sl_px = price_from_entry(entry, sl_pct, up=False)
        tp_px = price_from_entry(entry, tp_pct, up=True)
        soft_sl = sl_px

        if sym in sells:
            o = sells[sym]
            lines.append(f"⏳ {coin}: TP {o.get('qty')} @ {o.get('price')} (вход ~{round_price(entry)})")
        else:
            lines.append(f"📤 {coin}: нет TP → лимит +{tp_pct}% @ {round_price(tp_px)}")
            if not dry:
                res = place_tp_limit(sym, coin, q, tp_px, entry, st, dry=False)
                if res and res.get("retCode") != 0:
                    lines.append(f"  ⚠️ TP: {res.get('retMsg')}")

        if sym in stops:
            o = stops[sym]
            lines.append(f"🛡️ {coin}: SL стоп @ {o.get('triggerPrice')}")
        else:
            lines.append(f"🛡️ {coin}: нет SL → стоп −{sl_pct}% @ {round_price(sl_px)}")
            if not dry:
                res = place_stop_sell(sym, coin, q, sl_px, dry=False)
                if res and res.get("retCode") != 0:
                    lines.append(f"  ⚠️ SL: {res.get('retMsg')}")

    alerted = st.setdefault("drawdown_alerted", {})
    if dd <= -alert_pct and not alerted.get(coin):
        lines.append(f"📉 {coin}: просадка {dd:.1f}% от входа ~{round_price(entry)}")
        alerted[coin] = datetime.now(timezone.utc).isoformat()
    elif dd > -alert_pct and coin in alerted:
        alerted.pop(coin, None)

    soft = conf.get("soft_stop", True)
    if soft and px <= soft_sl and not dry:
        lines.append(
            f"⛔ {coin}: soft SL (цена {round_price(px)} ≤ {round_price(soft_sl)}) → market sell"
        )
        cancel_symbol_orders(sym)
        res = _order.place_order(
            symbol=sym,
            side="Sell",
            order_type="Market",
            qty=q,
            order_link_id=f"auto-softsl-{coin.lower()}-{int(time.time())}",
        )
        if res.get("retCode") == 0:
            st.setdefault("entries", {}).pop(coin, None)
            st.setdefault("drawdown_alerted", {}).pop(coin, None)
            return True
        lines.append(f"  ⚠️ soft SL: {res.get('retMsg')}")
    return False


def spot_price(symbol: str) -> float:
    d = _watch.api_get(f"market/tickers?category=spot&symbol={symbol}")
    return float(d["result"]["list"][0]["lastPrice"])


@dataclass
class Pick:
    symbol: str
    kind: str
    score: int


def best_buy_signal() -> Pick | None:
    # `limit_dip` — идея для отложенного лимитного ордера, но этот бот покупает
    # по рынку. Не превращаем такой сигнал в погоню за падающей ценой.
    priority = {"oversold_bounce": 0, "trend_up": 1}
    blockers = {"overheated", "funding_bear", "error"}
    candidates: list[Pick] = []
    for sym in _watch.WATCH:
        coin = sym.replace("USDT", "")
        if coin not in TRADE_COINS:
            continue
        signals = _watch.analyze_symbol(sym)
        # Любой конфликтный сигнал для пары отменяет вход, даже если рядом есть
        # перепроданность или тренд: это фильтр, а не просто низкий приоритет.
        if any(sig.kind in blockers for sig in signals):
            continue
        for sig in signals:
            if sig.kind not in priority:
                continue
            candidates.append(Pick(sym, sig.kind, priority[sig.kind]))
    if not candidates:
        return None
    candidates.sort(key=lambda p: (p.score, p.symbol))
    return candidates[0]


_LOT_STEP: dict[str, Decimal] = {}


def lot_step(symbol: str) -> Decimal:
    if symbol not in _LOT_STEP:
        d = _watch.api_get(f"market/instruments-info?category=spot&symbol={symbol}")
        step = (d.get("result") or {}).get("list", [{}])[0].get("lotSizeFilter", {}).get(
            "basePrecision", "0.0001"
        )
        _LOT_STEP[symbol] = Decimal(str(step))
    return _LOT_STEP[symbol]


def floor_qty(symbol: str, qty: float) -> str:
    """Округление вниз по basePrecision — иначе Insufficient balance."""
    step = lot_step(symbol)
    floored = (Decimal(str(qty)) / step).to_integral_value(rounding=ROUND_DOWN) * step
    text = format(floored, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def round_qty(symbol: str, qty: float) -> str:
    return floor_qty(symbol, qty)


def _order_qty_matches(order: dict, qty: str) -> bool:
    try:
        return Decimal(str(order.get("qty") or "0")) == Decimal(qty)
    except Exception:
        return str(order.get("qty") or "") == qty


def _refresh_orders_if_qty_mismatch(
    coin: str,
    sym: str,
    qty: str,
    sells: dict[str, dict],
    stops: dict[str, dict],
    *,
    dry: bool,
    lines: list[str],
) -> None:
    bad = False
    for bucket, label in ((sells, "TP"), (stops, "SL")):
        o = bucket.get(sym)
        if o and not _order_qty_matches(o, qty):
            bad = True
            lines.append(
                f"↻ {coin}: {label} qty {o.get('qty')} ≠ баланс {qty} — перевыставлю"
            )
    if bad and not dry:
        cancel_symbol_orders(sym)
        sells.pop(sym, None)
        stops.pop(sym, None)


def round_price(p: float) -> str:
    if p >= 1000:
        return f"{p:.1f}"
    if p >= 100:
        return f"{p:.2f}"
    if p >= 1:
        return f"{p:.2f}"
    return f"{p:.4f}".rstrip("0").rstrip(".")


def notify_tg(text: str) -> None:
    notify = ROOT / "bybit-telegram-notify.py"
    subprocess.run(
        [sys.executable, str(notify)],
        input=text.encode("utf-8"),
        capture_output=True,
        timeout=30,
    )


def _wallet_snapshot(avail: float, coins: dict[str, float]) -> dict:
    return {"avail": round(avail, 4), "coins": {k: round(v, 8) for k, v in coins.items()}}


def _detect_positive_events(
    report: str,
    prev: dict,
    curr: dict,
) -> list[str]:
    """События, о которых шлём Telegram: пополнение, TP, успешный BUY."""
    events: list[str] = []
    prev_c = prev.get("coins") or {}
    curr_c = curr.get("coins") or {}
    prev_usdt = float(prev_c.get("USDT") or prev.get("avail") or 0)
    curr_usdt = float(curr_c.get("USDT") or curr.get("avail") or 0)

    if "✅ BUY" in report:
        events.append("buy_ok")
    if any(l.startswith("💱") for l in report.splitlines()):
        events.append("reserve_to_usdt")

    for coin in TRADE_COINS:
        pq = float(prev_c.get(coin) or 0)
        cq = float(curr_c.get(coin) or 0)
        if pq > 0 and cq < pq * 0.4 and curr_usdt > prev_usdt + 0.3:
            events.append(f"exit_filled:{coin}")

    if "⛔" in report and "soft SL" in report:
        events.append("sl_soft")

    if (
        "✅ BUY" not in report
        and curr_usdt > prev_usdt + 0.5
        and not any(e.startswith("tp_filled:") for e in events)
        and "reserve_to_usdt" not in events
    ):
        events.append(f"deposit:+{curr_usdt - prev_usdt:.2f}USDT")

    return events


def should_notify_tg(report: str, conf: dict, prev: dict, curr: dict) -> bool:
    if conf.get("notify_telegram") is False:
        return False
    if conf.get("notify_positive_only") is False:
        return True
    events = _detect_positive_events(report, prev, curr)
    if conf.get("notify_sl", True) and (
        "⛔" in report or any(e.startswith("exit_filled:") for e in events) or "sl_soft" in events
    ):
        return True
    if "📉" in report and conf.get("notify_drawdown", True):
        return True
    if "⚠️" in report and "✅ BUY" not in report:
        return False
    return bool(events)


def _trade_limit_usdt(conf: dict, free: float) -> float:
    if conf.get("use_all_usdt") or conf.get("max_usdt_per_trade") in (None, "all"):
        return free
    try:
        return float(conf.get("max_usdt_per_trade") or 10)
    except (TypeError, ValueError):
        return min(free, 10.0)


def liquidate_reserves(conf: dict, coins: dict, *, dry: bool = False) -> list[str]:
    """Продаём ETH (и др. из RESERVE_TO_USDT) в USDT перед входом."""
    if not conf.get("use_eth") and not conf.get("deploy_all"):
        return []
    lines: list[str] = []
    for coin in RESERVE_TO_USDT:
        qty = coins.get(coin, 0)
        if qty <= 0:
            continue
        sym = f"{coin}USDT"
        px = spot_price(sym)
        if qty * px < 2:
            continue
        q = round_qty(sym, qty)
        lines.append(f"💱 {coin} → USDT market ~{qty * px:.1f}$")
        if dry:
            continue
        res = _order.place_order(
            symbol=sym,
            side="Sell",
            order_type="Market",
            qty=q,
            order_link_id=f"auto-liq-{coin.lower()}-{int(time.time())}",
        )
        if res.get("retCode") != 0:
            lines.append(f"  ⚠️ {coin}: {res.get('retMsg')}")
        else:
            time.sleep(1.5)
    return lines


def run_cycle(*, dry: bool = False) -> tuple[str, dict, dict]:
    conf = load_confirm()
    if not conf.get("enabled"):
        return "Авто-трейд выключен (bybit-auto-confirm.json).", {}, {}

    avail, coins = wallet_rows()
    prev_wallet = (load_state().get("wallet") or {})
    curr_wallet = _wallet_snapshot(avail, coins)
    liq = liquidate_reserves(conf, coins, dry=dry)
    if liq and not dry:
        avail, coins = wallet_rows()
        curr_wallet = _wallet_snapshot(avail, coins)
    free = min(avail, coins.get("USDT", avail))
    max_usdt = _trade_limit_usdt(conf, free)
    limit_label = "весь USDT" if max_usdt >= free - 0.01 else f"{max_usdt:.0f}"
    st = load_state()
    sells = open_sell_limits()
    stops = open_stop_sells()
    tp_pct, sl_pct = get_tp_sl_pcts(conf)
    if trail_enabled(conf):
        trail_dist = pct_from_conf(conf, "trail_distance_pct", 3.0)
        be_pct = pct_from_conf(conf, "breakeven_pct", 3.0)
        mode_line = (
            f"⚙️ trailing: BE +{be_pct}% / trail −{trail_dist}% от пика / SL −{sl_pct}% до BE"
        )
    else:
        mode_line = (
            f"⚙️ TP +{tp_pct}% / SL −{sl_pct}% / soft-stop "
            f"{'on' if conf.get('soft_stop', True) else 'off'}"
        )
    lines = [
        f"🤖 Bybit авто · {datetime.now(ZoneInfo(QUIET_TZ)).strftime('%d.%m %H:%M')}",
        mode_line,
    ]
    lines.extend(liq)

    # позиции в торгуемых альтах
    active: list[str] = []
    for coin in TRADE_COINS:
        qty = coins.get(coin, 0)
        if qty <= 0:
            st.setdefault("entries", {}).pop(coin, None)
            continue
        sym = f"{coin}USDT"
        px = spot_price(sym)
        usd = qty * px
        if usd < 2:
            continue
        active.append(coin)
        closed = manage_position(
            coin, sym, qty, conf, st, sells, stops, dry=dry, lines=lines
        )
        if closed and not dry:
            avail, coins = wallet_rows()
            curr_wallet = _wallet_snapshot(avail, coins)
            sells = open_sell_limits()
            stops = open_stop_sells()

    lines.append(f"💵 свободно ~{free:.2f} USDT (лимит {limit_label}/сделку)")

    # Явный allow_parallel в confirm важнее use_all_usdt (картбланш ≠ параллельные входы).
    if "allow_parallel" in conf:
        allow_parallel = bool(conf.get("allow_parallel"))
    else:
        allow_parallel = bool(conf.get("use_all_usdt"))
    if active and not allow_parallel:
        lines.append("Есть открытая позиция — новый вход только после её закрытия.")
        st["wallet"] = curr_wallet
        save_state(st)
        return "\n".join(lines), prev_wallet, curr_wallet

    if free < MIN_USDT:
        lines.append(f"Мало USDT (<{MIN_USDT}) — жду пополнения или TP.")
        st["wallet"] = curr_wallet
        save_state(st)
        return "\n".join(lines), prev_wallet, curr_wallet

    pick = best_buy_signal()
    if not pick:
        lines.append("Сигналов нет — держу USDT.")
        st["wallet"] = curr_wallet
        save_state(st)
        return "\n".join(lines), prev_wallet, curr_wallet

    spend = min(free, max_usdt)
    coin = pick.symbol.replace("USDT", "")
    lines.append(f"🟢 Сигнал {pick.symbol} [{pick.kind}] → BUY ~{spend:.2f} USDT")

    if dry:
        px = spot_price(pick.symbol)
        entry = px
        if trail_enabled(conf):
            sl = price_from_entry(entry, sl_pct, up=False)
            lines.append(f"(dry) market buy + trailing SL от −{sl_pct}% / BE +{conf.get('breakeven_pct', 3)}%")
        else:
            tp = price_from_entry(entry, tp_pct, up=True)
            sl = price_from_entry(entry, sl_pct, up=False)
            lines.append(
                f"(dry) market buy + TP @ {round_price(tp)} + SL @ {round_price(sl)}"
            )
        return "\n".join(lines), prev_wallet, curr_wallet

    buy = _order.place_order(
        symbol=pick.symbol,
        side="Buy",
        order_type="Market",
        quote_usdt=f"{spend:.2f}",
        order_link_id=f"auto-buy-{coin.lower()}-{int(time.time())}",
    )
    if buy.get("retCode") != 0:
        lines.append(f"⚠️ BUY: {buy.get('retMsg')}")
        st["wallet"] = curr_wallet
        save_state(st)
        return "\n".join(lines), prev_wallet, curr_wallet

    time.sleep(1.5)
    avail2, coins2 = wallet_rows()
    curr_wallet = _wallet_snapshot(avail2, coins2)
    qty = coins2.get(coin, 0)
    if qty <= 0:
        lines.append("BUY OK, но монета не видна в балансе — TP вручную.")
        st["wallet"] = curr_wallet
        save_state(st)
        return "\n".join(lines), prev_wallet, curr_wallet

    px = spot_price(pick.symbol)
    entry = px
    sl = price_from_entry(entry, sl_pct, up=False)
    q = round_qty(pick.symbol, qty)
    if trail_enabled(conf):
        sl_res = place_stop_sell(pick.symbol, coin, q, sl, dry=False)
        st["last_buy"] = {"symbol": pick.symbol, "usdt": spend, "kind": pick.kind}
        st.setdefault("entries", {})[coin] = {
            "entry": entry,
            "peak": entry,
            "sl": float(round_price(sl)),
            "source": "buy_trail",
        }
        if sl_res and sl_res.get("retCode") == 0:
            lines.append(f"✅ BUY + trailing SL @ {round_price(sl)} (без фикс. TP)")
        else:
            lines.append(f"✅ BUY, ⚠️ SL: {(sl_res or {}).get('retMsg')}")
    else:
        tp = price_from_entry(entry, tp_pct, up=True)
        sell = place_tp_limit(pick.symbol, coin, q, tp, entry, st, dry=False)
        sl_res = place_stop_sell(pick.symbol, coin, q, sl, dry=False)
        st["last_buy"] = {"symbol": pick.symbol, "usdt": spend, "kind": pick.kind}
        st.setdefault("entries", {})[coin] = {
            "entry": entry,
            "tp": float(round_price(tp)),
            "sl": float(round_price(sl)),
            "source": "buy",
        }
        if sell and sell.get("retCode") == 0 and sl_res and sl_res.get("retCode") == 0:
            lines.append(f"✅ BUY + TP {q} @ {round_price(tp)} + SL @ {round_price(sl)}")
        elif sell and sell.get("retCode") == 0:
            lines.append(f"✅ BUY + TP @ {round_price(tp)}, ⚠️ SL: {(sl_res or {}).get('retMsg')}")
        else:
            lines.append(f"✅ BUY, ⚠️ TP: {(sell or {}).get('retMsg')}")
    st["wallet"] = curr_wallet
    save_state(st)
    return "\n".join(lines), prev_wallet, curr_wallet


def main() -> int:
    dry = "--dry" in sys.argv
    tg = "--telegram" in sys.argv or os.environ.get("BYBIT_AUTO_TRADER_TELEGRAM") == "1"
    conf = load_confirm()
    report, prev_w, curr_w = run_cycle(dry=dry)
    print(report)
    if tg and not dry and should_notify_tg(report, conf, prev_w, curr_w):
        notify_tg(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
