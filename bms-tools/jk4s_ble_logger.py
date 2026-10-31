#!/usr/bin/env python3
"""Опрос JK-B2A8S20P (АКБ 4S 12 В 230 А·ч) по BLE → JSON для Home Assistant.

Обновлено: 2026-10-31
MAC по умолчанию: C8:47:80:53:0F:B6 (AKB-4S-230), протокол JK02_32S.
"""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

from bleak import BleakClient, BleakScanner

MAC = os.environ.get("JK4S_MAC", "C8:47:80:53:0F:B6")
NAME_HINT = os.environ.get("JK4S_NAME", "AKB-4S-230")
INTERVAL = float(os.environ.get("JK4S_INTERVAL", "60"))
FAIL_SLEEP = float(os.environ.get("JK4S_FAIL_SLEEP", "20"))
CHAR = "0000ffe1-0000-1000-8000-00805f9b34fb"

BASE = Path(os.environ.get("JK4S_BASE", "/home/pi/jk4s-ble"))
LOG_DIR = BASE / "logs"
STATE_PATH = BASE / "jk4s_state.json"
CSV_PATH = LOG_DIR / "jk4s.csv"
HA_JSON = Path(
    os.environ.get(
        "JK4S_HA_JSON",
        str(BASE / "jk4s.json"),
    )
)
# Опционально: копия на Pi5 (тот же стиль, что ANT BMS24C)
HA_JSON_REMOTE = os.environ.get("JK4S_HA_JSON_REMOTE", "").strip()
HA_SCP_TARGET = os.environ.get(
    "JK4S_SCP_TARGET",
    "pi@100.102.159.200:/home/pi/Documents/Проекты/Apple HomeKit accessory/home_assistant/config/host_status/jk4s.json",
).strip()


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def csum(data: bytes) -> int:
    return sum(data) & 0xFF


def req(cmd: int) -> bytes:
    frame = bytearray(20)
    frame[0:5] = bytes([0xAA, 0x55, 0x90, 0xEB, cmd])
    frame[19] = csum(frame[:19])
    return bytes(frame)


def u16(d: bytes, i: int) -> int:
    return d[i] | (d[i + 1] << 8)


def i16(d: bytes, i: int) -> int:
    v = u16(d, i)
    return v - 0x10000 if v & 0x8000 else v


def u32(d: bytes, i: int) -> int:
    return u16(d, i) | (u16(d, i + 2) << 16)


def i32(d: bytes, i: int) -> int:
    v = u32(d, i)
    return v - 0x100000000 if v & 0x80000000 else v


def parse_jk02_32s(frame: bytes) -> dict | None:
    """Разбор кадра cell info 0x02 (JK02_32S, как ESPHome / FW 19.x)."""
    idx = frame.find(b"\x55\xaa\xeb\x90\x02")
    if idx < 0:
        return None
    d = frame[idx:]
    if len(d) < 180:
        return None

    cells: list[float] = []
    for i in range(32):
        off = 6 + i * 2
        if off + 1 >= len(d):
            break
        mv = u16(d, off)
        if 1500 < mv < 4500:
            cells.append(round(mv * 0.001, 3))

    # ESPHome: offset=16 для JK02_32S, затем offset *= 2 → 32
    o = 32
    pack_v = round(u32(d, 118 + o) * 0.001, 3)
    current = round(i32(d, 126 + o) * 0.001, 3)
    sample = {
        "pack_V": pack_v,
        "current_A": current,
        "mos_temp_C": round(i16(d, 112 + o) * 0.1, 1),
        "temp1_C": round(i16(d, 130 + o) * 0.1, 1),
        "temp2_C": round(i16(d, 132 + o) * 0.1, 1),
        "balance_A": round(i16(d, 138 + o) * 0.001, 3),
        "balance_action": int(d[140 + o]),
        "soc": int(d[141 + o]),
        "remain_Ah": round(u32(d, 142 + o) * 0.001, 3),
        "nominal_Ah": round(u32(d, 146 + o) * 0.001, 3),
        "cycles": int(u32(d, 150 + o)),
        "soh": int(d[158 + o]),
        "runtime_s": int(u32(d, 162 + o)),
        "charge_mos": bool(d[166 + o]),
        "discharge_mos": bool(d[167 + o]),
        "cells_V": cells,
        "cell_count": len(cells),
    }
    if cells:
        sample["cell_min_V"] = min(cells)
        sample["cell_max_V"] = max(cells)
        sample["cell_delta_mV"] = int(round((max(cells) - min(cells)) * 1000))
        sample["pack_from_cells_V"] = round(sum(cells), 3)
        # sanity: если pack из BMS нелепый — взять сумму ячеек
        if sample["pack_V"] < 5 or sample["pack_V"] > 20:
            sample["pack_V"] = sample["pack_from_cells_V"]
    return sample


def mode_of(sample: dict) -> str:
    a = float(sample.get("current_A") or 0)
    if a > 0.3:
        return "discharge"
    if a < -0.3:
        return "charge"
    return "idle"


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "pack_v_min": None,
        "pack_v_max": None,
        "last_charge_peak_V": None,
        "last_discharge_floor_V": None,
        "prev_mode": "offline",
    }


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def append_csv(sample: dict, mode: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    new = not CSV_PATH.exists()
    with CSV_PATH.open("a", encoding="utf-8") as f:
        if new:
            f.write(
                "ts,pack_V,current_A,soc,remain_Ah,mode,charge_mos,discharge_mos,"
                "cell_min_V,cell_max_V,cell_delta_mV,temp1_C,temp2_C,mos_temp_C\n"
            )
        f.write(
            f"{now_iso()},{sample.get('pack_V')},{sample.get('current_A')},{sample.get('soc')},"
            f"{sample.get('remain_Ah')},{mode},{int(bool(sample.get('charge_mos')))},"
            f"{int(bool(sample.get('discharge_mos')))},{sample.get('cell_min_V')},"
            f"{sample.get('cell_max_V')},{sample.get('cell_delta_mV')},"
            f"{sample.get('temp1_C')},{sample.get('temp2_C')},{sample.get('mos_temp_C')}\n"
        )


def publish(sample: dict | None, state: dict, online: bool, err: str | None = None) -> None:
    """Пишет снимок для HA. При offline — держит последние валидные числа (без нулей)."""
    last = state.get("last_good") or {}
    if online and sample:
        live = sample
        state["last_good"] = dict(sample)
    else:
        live = last

    def live_get(key, default=None):
        v = live.get(key, default)
        return v

    snap = {
        "ts": now_iso(),
        "mac": MAC,
        "name": NAME_HINT,
        "online": online,
        "error": err,
        "mode": mode_of(live) if live else "offline",
        "pack_V": live_get("pack_V"),
        "current_A": live_get("current_A"),
        "soc": live_get("soc"),
        "remain_Ah": live_get("remain_Ah"),
        "nominal_Ah": live_get("nominal_Ah"),
        "charge_mos": "On" if live_get("charge_mos") else ("Off" if live else None),
        "discharge_mos": "On" if live_get("discharge_mos") else ("Off" if live else None),
        "balancer": live_get("balance_action"),
        "balance_A": live_get("balance_A"),
        "cell_min_V": live_get("cell_min_V"),
        "cell_max_V": live_get("cell_max_V"),
        "cell_delta_mV": live_get("cell_delta_mV"),
        "cells_V": live_get("cells_V"),
        "cell_count": live_get("cell_count"),
        "temp1_C": live_get("temp1_C"),
        "temp2_C": live_get("temp2_C"),
        "mos_temp_C": live_get("mos_temp_C"),
        "cycles": live_get("cycles"),
        "soh": live_get("soh"),
        "pack_v_min": state.get("pack_v_min"),
        "pack_v_max": state.get("pack_v_max"),
        "last_charge_peak_V": state.get("last_charge_peak_V"),
        "last_discharge_floor_V": state.get("last_discharge_floor_V"),
    }
    HA_JSON.parent.mkdir(parents=True, exist_ok=True)
    tmp = HA_JSON.with_suffix(".tmp")
    tmp.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(HA_JSON)
    if HA_JSON_REMOTE:
        try:
            remote = Path(HA_JSON_REMOTE)
            remote.parent.mkdir(parents=True, exist_ok=True)
            remote.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"local remote copy fail: {e}", flush=True)
    if HA_SCP_TARGET:
        try:
            subprocess.run(
                [
                    "scp",
                    "-o",
                    "ConnectTimeout=8",
                    "-o",
                    "BatchMode=yes",
                    str(HA_JSON),
                    HA_SCP_TARGET,
                ],
                check=False,
                capture_output=True,
                timeout=25,
            )
        except Exception as e:
            print(f"scp fail: {e}", flush=True)


def update_extrema(state: dict, sample: dict, mode: str) -> None:
    v = sample.get("pack_V")
    if isinstance(v, (int, float)):
        if state.get("pack_v_min") is None or v < state["pack_v_min"]:
            state["pack_v_min"] = v
        if state.get("pack_v_max") is None or v > state["pack_v_max"]:
            state["pack_v_max"] = v
    prev = state.get("prev_mode")
    if prev == "charge" and mode != "charge" and isinstance(v, (int, float)):
        state["last_charge_peak_V"] = v
    if prev == "discharge" and mode != "discharge" and isinstance(v, (int, float)):
        state["last_discharge_floor_V"] = v
    state["prev_mode"] = mode


def btctl(*args: str) -> None:
    try:
        subprocess.run(
            ["bluetoothctl", *args],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except Exception:
        pass


def prepare_adapter() -> None:
    try:
        subprocess.run(["sudo", "hciconfig", "hci0", "up"], capture_output=True, timeout=10)
    except Exception:
        pass
    btctl("power", "on")
    btctl("agent", "on")
    btctl("default-agent")


async def fetch_once(timeout: float = 35.0, attempts: int = 4) -> dict:
    prepare_adapter()
    last_err: Exception | None = None

    for attempt in range(1, attempts + 1):
        buf = bytearray()

        def on_notify(_sender, data: bytearray) -> None:
            buf.extend(data)

        try:
            # сброс залипшего коннекта / trust
            btctl("disconnect", MAC)
            await asyncio.sleep(0.4)
            btctl("trust", MAC)
            # scan, чтобы BlueZ увидел устройство
            devices = await BleakScanner.discover(timeout=8.0)
            seen = any(d.address.upper() == MAC.upper() for d in devices)
            if not seen:
                # bluetoothctl scan иногда помогает на Pi 3
                btctl("scan", "on")
                await asyncio.sleep(6.0)
                btctl("scan", "off")
                await asyncio.sleep(0.3)
            # предварительный connect через bluetoothctl (стабильнее для JK)
            btctl("connect", MAC)
            await asyncio.sleep(1.2)

            async with BleakClient(MAC, timeout=timeout) as client:
                if not client.is_connected:
                    raise RuntimeError("not connected")
                await asyncio.sleep(0.4)
                await client.start_notify(CHAR, on_notify)
                await asyncio.sleep(0.3)
                await client.write_gatt_char(CHAR, req(0x96), response=False)
                t0 = time.time()
                while time.time() - t0 < 10.0:
                    await asyncio.sleep(0.15)
                    if b"\x55\xaa\xeb\x90\x02" in buf and len(buf) > 200:
                        last = len(buf)
                        stable = 0
                        for _ in range(30):
                            await asyncio.sleep(0.08)
                            if len(buf) == last:
                                stable += 1
                                if stable >= 5:
                                    break
                            else:
                                last = len(buf)
                                stable = 0
                        break
                try:
                    await client.stop_notify(CHAR)
                except Exception:
                    pass

            sample = parse_jk02_32s(bytes(buf))
            if not sample:
                raise RuntimeError(f"no JK02 frame (rx={len(buf)})")
            return sample
        except Exception as e:
            last_err = e
            print(f"attempt {attempt}/{attempts} fail: {e}", flush=True)
            btctl("disconnect", MAC)
            await asyncio.sleep(2.0 + attempt)

    raise RuntimeError(str(last_err) if last_err else "BLE fetch failed")


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    print(f"jk4s logger start mac={MAC} interval={INTERVAL}s → {HA_JSON}", flush=True)
    while True:
        try:
            sample = asyncio.run(fetch_once())
            mode = mode_of(sample)
            update_extrema(state, sample, mode)
            append_csv(sample, mode)
            publish(sample, state, online=True)
            save_state(state)
            print(
                f"{now_iso()} {mode} {sample['pack_V']}V {sample['current_A']}A "
                f"soc={sample['soc']} delta={sample.get('cell_delta_mV')}mV",
                flush=True,
            )
            time.sleep(INTERVAL)
        except Exception as e:
            print(f"{now_iso()} FAIL: {e}", flush=True)
            publish(None, state, online=False, err=str(e))
            save_state(state)
            time.sleep(FAIL_SLEEP)


if __name__ == "__main__":
    main()
