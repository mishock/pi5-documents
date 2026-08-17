#!/usr/bin/env python3
"""Poll ANT BMS-ANT24C over RFCOMM, log cycles, publish snapshot for Home Assistant."""
from __future__ import annotations

import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import serial

MAC = os.environ.get("ANT24C_MAC", "AA:BB:CC:91:23:45")
RFCOMM = os.environ.get("ANT24C_RFCOMM", "/dev/rfcomm0")
RFCOMM_N = os.environ.get("ANT24C_RFCOMM_N", "0")
INTERVAL = float(os.environ.get("ANT24C_INTERVAL", "300"))
FAIL_SLEEP = float(os.environ.get("ANT24C_FAIL_SLEEP", "15"))
IDLE_A = float(os.environ.get("ANT24C_IDLE_A", "1.0"))

BASE = Path(os.environ.get("ANT24C_BASE", "/home/pi/Documents/bms-tools"))
LOG_DIR = BASE / "logs"
STATE_PATH = BASE / "ant24c_state.json"
CSV_PATH = LOG_DIR / "ant24c.csv"
EVENTS_PATH = LOG_DIR / "ant24c_cycles.jsonl"
HA_JSON = Path(
    os.environ.get(
        "ANT24C_HA_JSON",
        "/home/pi/Documents/Проекты/Apple HomeKit accessory/home_assistant/config/host_status/ant24c.json",
    )
)
CMD_PATH = Path(os.environ.get("ANT24C_CMD_JSON", str(HA_JSON.parent / "ant24c_cmd.json")))
CMD_RESULT = Path(os.environ.get("ANT24C_CMD_RESULT", str(HA_JSON.parent / "ant24c_cmd_result.json")))
PASSWORD = os.environ.get("ANT24C_PASSWORD", "12345678")

CHARGE = {
    0: "Off",
    1: "On",
    2: "OV protect",
    3: "OC protect",
    4: "Battery full",
    5: "Total overpressure",
    6: "Batt OT",
    7: "MOS OT",
    8: "Abnormal current",
    9: "Balance line drop",
    10: "Board OT",
    15: "Manual off",
}
DISCH = {
    0: "Off",
    1: "On",
    2: "UV protect",
    3: "OC protect",
    5: "Pack UV",
    6: "Batt OT",
    7: "MOS OT",
    8: "Abnormal current",
    9: "Balance line drop",
    10: "Board OT",
    12: "Short",
    15: "Manual off",
}

BALANCER = {
    0: "Off",
    1: "Limit",
    2: "Charge delta",
    3: "OT",
    4: "Auto",
    10: "Board OT",
}

CHG_CUT = {2, 4, 5}  # OV / full / pack OV
DSG_CUT = {2, 5, 12}  # UV / pack UV / short

# Legacy A5 A5: ESPHome ant_bms_old (big-endian value bytes)
ADDR_PASS = (0xF1, 0xF2, 0xF3, 0xF4)
ADDR_DSG_MOS = 0xF9
ADDR_CHG_MOS = 0xFA
ADDR_BALANCER = 0xFC
ADDR_APPLY = 0xFF


def u16(d: bytes, i: int) -> int:
    return (d[i] << 8) | d[i + 1]


def i32(d: bytes, i: int) -> int:
    v = (u16(d, i) << 16) | u16(d, i + 2)
    return v - 0x100000000 if v & 0x80000000 else v


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def bind_rfcomm() -> None:
    subprocess.run(["rfcomm", "release", RFCOMM_N], capture_output=True)
    time.sleep(0.4)
    subprocess.run(["rfcomm", "bind", RFCOMM_N, MAC, "1"], check=False)
    time.sleep(1.2)


def open_serial() -> serial.Serial:
    if not Path(RFCOMM).exists():
        bind_rfcomm()
    ser = serial.Serial(RFCOMM, 19200, timeout=0.25, write_timeout=2)
    time.sleep(0.3)
    return ser


def poll(ser: serial.Serial, wait: float = 2.0) -> bytes | None:
    ser.reset_input_buffer()
    ser.write(bytes([0xDB, 0xDB, 0, 0, 0, 0]))
    ser.flush()
    t0 = time.time()
    buf = bytearray()
    while time.time() - t0 < wait:
        n = ser.in_waiting
        if n:
            buf += ser.read(n)
        elif len(buf) >= 140:
            break
        else:
            time.sleep(0.02)
    if len(buf) >= 140 and buf[:4] == b"\xaa\x55\xaa\xff":
        return bytes(buf[:140])
    return None


def parse(frame: bytes) -> dict:
    n = frame[123]
    cells = [u16(frame, 6 + i * 2) for i in range(n)]
    chg, dsg, bal = frame[103], frame[104], frame[105]
    current = round(i32(frame, 70) * 0.1, 2)
    pack = round(u16(frame, 4) * 0.1, 2)
    return {
        "pack_V": pack,
        "current_A": current,
        "soc": frame[74],
        "remain_Ah": round(((u16(frame, 79) << 16) | u16(frame, 81)) * 1e-6, 3),
        "capacity_Ah": round(((u16(frame, 75) << 16) | u16(frame, 77)) * 1e-6, 3),
        "charge_mos_code": chg,
        "charge_mos": CHARGE.get(chg, str(chg)),
        "discharge_mos_code": dsg,
        "discharge_mos": DISCH.get(dsg, str(dsg)),
        "balancer_code": bal,
        "balancer": BALANCER.get(bal, str(bal)),
        "cell_min_V": round(min(cells) / 1000, 3),
        "cell_max_V": round(max(cells) / 1000, 3),
        "cell_delta_mV": max(cells) - min(cells),
        "cell_count": n,
    }


def classify(sample: dict) -> str:
    i = sample["current_A"]
    if sample["charge_mos_code"] in CHG_CUT:
        return "charge_cut"
    if sample["discharge_mos_code"] in DSG_CUT:
        return "discharge_cut"
    if abs(i) < IDLE_A:
        return "idle"
    # ANT: отрицательный ток = заряд (как в SystemLog других плат)
    return "charging" if i < 0 else "discharging"


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except json.JSONDecodeError:
            pass
    return {
        "pack_v_min": None,
        "pack_v_max": None,
        "last_charge_peak_V": None,
        "last_charge_peak_at": None,
        "last_discharge_floor_V": None,
        "last_discharge_floor_at": None,
        "session": None,
        "session_start_V": None,
        "session_start_at": None,
        "session_ext_V": None,
        "prev_mode": None,
        "prev_chg": None,
        "prev_dsg": None,
        "balancer_enabled": None,
        "last_cmd": None,
    }


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def emit_event(kind: str, sample: dict, extra: dict | None = None) -> None:
    rec = {
        "ts": now_iso(),
        "event": kind,
        "pack_V": sample["pack_V"],
        "current_A": sample["current_A"],
        "soc": sample["soc"],
        "charge_mos": sample["charge_mos"],
        "discharge_mos": sample["discharge_mos"],
    }
    if extra:
        rec.update(extra)
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS_PATH.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def append_csv(sample: dict, mode: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    new = not CSV_PATH.exists()
    with CSV_PATH.open("a") as f:
        if new:
            f.write(
                "ts,pack_V,current_A,soc,remain_Ah,mode,charge_mos,discharge_mos,"
                "cell_min_V,cell_max_V,cell_delta_mV\n"
            )
        f.write(
            f"{now_iso()},{sample['pack_V']},{sample['current_A']},{sample['soc']},"
            f"{sample['remain_Ah']},{mode},{sample['charge_mos']},{sample['discharge_mos']},"
            f"{sample['cell_min_V']},{sample['cell_max_V']},{sample['cell_delta_mV']}\n"
        )


def write_ha(sample: dict, mode: str, state: dict, online: bool) -> None:
    HA_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "online": online,
        "ts": now_iso(),
        "mode": mode if online else "offline",
        "pack_V": sample.get("pack_V"),
        "current_A": sample.get("current_A"),
        "soc": sample.get("soc"),
        "remain_Ah": sample.get("remain_Ah"),
        "charge_mos": sample.get("charge_mos"),
        "discharge_mos": sample.get("discharge_mos"),
        "balancer": sample.get("balancer"),
        "charge_on": sample.get("charge_mos_code") == 1,
        "discharge_on": sample.get("discharge_mos_code") == 1,
        "balancer_on": (
            state.get("balancer_enabled")
            if state.get("balancer_enabled") is not None
            else bool(sample.get("balancer_code"))
        ),
        "last_cmd": state.get("last_cmd"),
        "cell_min_V": sample.get("cell_min_V"),
        "cell_max_V": sample.get("cell_max_V"),
        "cell_delta_mV": sample.get("cell_delta_mV"),
        "pack_v_min": state.get("pack_v_min"),
        "pack_v_max": state.get("pack_v_max"),
        "last_charge_peak_V": state.get("last_charge_peak_V"),
        "last_discharge_floor_V": state.get("last_discharge_floor_V"),
        "session": state.get("session"),
        "session_start_V": state.get("session_start_V"),
        "session_ext_V": state.get("session_ext_V"),
    }
    tmp = HA_JSON.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False) + "\n")
    tmp.replace(HA_JSON)


def update_cycles(sample: dict, mode: str, state: dict) -> None:
    v = sample["pack_V"]
    if state["pack_v_min"] is None or v < state["pack_v_min"]:
        state["pack_v_min"] = v
    if state["pack_v_max"] is None or v > state["pack_v_max"]:
        state["pack_v_max"] = v

    prev = state.get("prev_mode")
    prev_chg = state.get("prev_chg")
    prev_dsg = state.get("prev_dsg")

    if mode in ("charging", "discharging") and prev not in ("charging", "discharging"):
        state["session"] = mode
        state["session_start_V"] = v
        state["session_start_at"] = now_iso()
        state["session_ext_V"] = v
        emit_event(f"{mode}_start", sample, {"start_V": v})
    if mode == "charging":
        state["session_ext_V"] = max(state.get("session_ext_V") or v, v)
    if mode == "discharging":
        state["session_ext_V"] = min(state.get("session_ext_V") or v, v)

    # Отсечка заряда по MOS (OV / full) — «до какого напряжения поднялась и отключилась»
    if prev_chg not in CHG_CUT and sample["charge_mos_code"] in CHG_CUT:
        peak = state.get("session_ext_V") if state.get("session") == "charging" else v
        peak = max(peak or v, v)
        state["last_charge_peak_V"] = peak
        state["last_charge_peak_at"] = now_iso()
        emit_event(
            "charge_cut",
            sample,
            {
                "peak_V": peak,
                "start_V": state.get("session_start_V"),
                "reason": sample["charge_mos"],
            },
        )
        state["session"] = None
    # Отсечка разряда по MOS (UV)
    if prev_dsg not in DSG_CUT and sample["discharge_mos_code"] in DSG_CUT:
        floor = state.get("session_ext_V") if state.get("session") == "discharging" else v
        floor = min(floor or v, v)
        state["last_discharge_floor_V"] = floor
        state["last_discharge_floor_at"] = now_iso()
        emit_event(
            "discharge_cut",
            sample,
            {
                "floor_V": floor,
                "start_V": state.get("session_start_V"),
                "reason": sample["discharge_mos"],
            },
        )
        state["session"] = None

    if mode == "idle" and prev in ("charging", "discharging"):
        extra = {
            "start_V": state.get("session_start_V"),
            "ext_V": state.get("session_ext_V"),
        }
        emit_event(f"{prev}_end", sample, extra)
        if prev == "charging" and state.get("session_ext_V") is not None:
            state["last_charge_peak_V"] = state["session_ext_V"]
            state["last_charge_peak_at"] = now_iso()
        if prev == "discharging" and state.get("session_ext_V") is not None:
            state["last_discharge_floor_V"] = state["session_ext_V"]
            state["last_discharge_floor_at"] = now_iso()
        state["session"] = None

    state["prev_mode"] = mode
    state["prev_chg"] = sample["charge_mos_code"]
    state["prev_dsg"] = sample["discharge_mos_code"]


def legacy_write_be(addr: int, value: int) -> bytes:
    hi, lo = (value >> 8) & 0xFF, value & 0xFF
    chk = (addr + hi + lo) & 0xFF
    return bytes([0xA5, 0xA5, addr, hi, lo, chk])


def send_write(ser: serial.Serial, addr: int, value: int, pause: float = 0.18) -> None:
    ser.reset_input_buffer()
    ser.write(legacy_write_be(addr, value))
    ser.flush()
    time.sleep(pause)
    if ser.in_waiting:
        ser.read(ser.in_waiting)


def authenticate(ser: serial.Serial) -> None:
    pw = (PASSWORD.encode("ascii", errors="ignore") + b"00000000")[:8]
    for i, addr in enumerate(ADDR_PASS):
        send_write(ser, addr, (pw[i * 2] << 8) | pw[i * 2 + 1])
    send_write(ser, ADDR_APPLY, 0)


def apply_control(ser: serial.Serial, target: str, on: bool) -> None:
    authenticate(ser)
    val = 1 if on else 0
    if target == "charge":
        send_write(ser, ADDR_CHG_MOS, val)
    elif target == "discharge":
        send_write(ser, ADDR_DSG_MOS, val)
    elif target == "balancer":
        send_write(ser, ADDR_BALANCER, val)
    else:
        raise ValueError(f"unknown target {target}")
    send_write(ser, ADDR_APPLY, 0)
    time.sleep(0.35)


def write_cmd_result(payload: dict) -> None:
    CMD_RESULT.parent.mkdir(parents=True, exist_ok=True)
    tmp = CMD_RESULT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False) + "\n")
    tmp.replace(CMD_RESULT)


def take_cmd() -> dict | None:
    if not CMD_PATH.exists():
        return None
    taken = CMD_PATH.with_suffix(".taken")
    try:
        CMD_PATH.replace(taken)
    except FileNotFoundError:
        return None
    try:
        data = json.loads(taken.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        write_cmd_result({"ok": False, "error": f"bad cmd file: {exc}"})
        return None
    finally:
        try:
            taken.unlink(missing_ok=True)
        except OSError:
            pass
    if not isinstance(data, dict) or "target" not in data:
        write_cmd_result({"ok": False, "id": None, "error": "cmd must have target"})
        return None
    return data


def refresh_snapshot(ser: serial.Serial, state: dict) -> dict | None:
    frame = poll(ser, wait=2.0)
    if not frame:
        return None
    sample = parse(frame)
    mode = classify(sample)
    update_cycles(sample, mode, state)
    save_state(state)
    write_ha(sample, mode, state, True)
    return sample


def process_cmd(ser: serial.Serial | None, state: dict) -> dict | None:
    cmd = take_cmd()
    if not cmd:
        return None
    cmd_id = cmd.get("id")
    target = str(cmd.get("target", "")).strip().lower()
    on = bool(cmd.get("on"))
    rec = {
        "id": cmd_id,
        "target": target,
        "on": on,
        "ts": now_iso(),
        "ok": False,
        "error": None,
    }
    print(f"cmd {target} {'on' if on else 'off'} id={cmd_id}", flush=True)
    if ser is None or not getattr(ser, "is_open", False):
        rec["error"] = "BMS serial offline"
        state["last_cmd"] = rec
        write_cmd_result(rec)
        return rec
    if target not in ("charge", "discharge", "balancer"):
        rec["error"] = f"unknown target {target}"
        state["last_cmd"] = rec
        write_cmd_result(rec)
        return rec
    try:
        apply_control(ser, target, on)
        if target == "balancer":
            state["balancer_enabled"] = on
        rec["ok"] = True
        sample = refresh_snapshot(ser, state)
        if sample:
            rec["charge_mos"] = sample.get("charge_mos")
            rec["discharge_mos"] = sample.get("discharge_mos")
            rec["balancer"] = sample.get("balancer")
    except Exception as exc:
        rec["error"] = f"{type(exc).__name__}: {exc}"
        print(f"cmd error: {rec['error']}", flush=True)
    state["last_cmd"] = rec
    save_state(state)
    write_cmd_result(rec)
    return rec


def sleep_checking_cmd(seconds: float, ser, state: dict) -> bool:
    t_end = time.time() + seconds
    while time.time() < t_end:
        if process_cmd(ser, state) is not None:
            return True
        time.sleep(0.25)
    return False


def main() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    ser = None
    fails = 0
    print(f"ant24c logger start mac={MAC} interval={INTERVAL}s", flush=True)
    while True:
        try:
            if ser is None or not ser.is_open:
                try:
                    if ser:
                        ser.close()
                except Exception:
                    pass
                ser = open_serial()
            if process_cmd(ser, state) is not None:
                # Immediately re-poll so HA switch state matches MOS/balancer.
                pass
            frame = poll(ser)
            if not frame:
                fails += 1
                if fails >= 3:
                    print("reconnect after empty polls", flush=True)
                    try:
                        ser.close()
                    except Exception:
                        pass
                    ser = None
                    bind_rfcomm()
                    fails = 0
                write_ha({}, "offline", state, False)
                sleep_checking_cmd(FAIL_SLEEP, ser, state)
                continue
            fails = 0
            sample = parse(frame)
            mode = classify(sample)
            update_cycles(sample, mode, state)
            save_state(state)
            append_csv(sample, mode)
            write_ha(sample, mode, state, True)
            print(
                f"{now_iso()} {mode} {sample['pack_V']}V {sample['current_A']}A "
                f"soc={sample['soc']} chg={sample['charge_mos']} dsg={sample['discharge_mos']} "
                f"bal={sample['balancer']}",
                flush=True,
            )
        except Exception as exc:
            print(f"error: {type(exc).__name__}: {exc}", flush=True)
            try:
                if ser:
                    ser.close()
            except Exception:
                pass
            ser = None
            write_ha({}, "offline", state, False)
            time.sleep(2)
            bind_rfcomm()
            continue
        sleep_checking_cmd(INTERVAL, ser, state)


if __name__ == "__main__":
    main()
