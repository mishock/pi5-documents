#!/usr/bin/env python3
"""Probe ANT BMS over Bluetooth RFCOMM / SPP."""
import argparse
import struct
import time
import json
from datetime import timedelta

try:
    import serial
except ImportError:
    raise SystemExit("pyserial required")

CHARGE_MOSFET = {
    0x00: "Off", 0x01: "On", 0x02: "Overcharge protection",
    0x03: "Over current protection", 0x04: "Battery full",
    0x05: "Total overpressure", 0x06: "Battery over temperature",
    0x07: "MOSFET over temperature", 0x08: "Abnormal current",
    0x09: "Balanced line dropped string", 0x0A: "Motherboard over temperature",
    0x0C: "Open failed", 0x0D: "Discharge MOSFET abnormality",
    0x0E: "Waiting", 0x0F: "Manually turned off",
    0x10: "Two level exceed voltage", 0x11: "Low temperature protection",
    0x12: "Voltage difference exceeded", 0x14: "Self detect error",
}
DISCHARGE_MOSFET = {
    0x00: "Off", 0x01: "On", 0x02: "Overdischarge protection",
    0x03: "Over current protection", 0x04: "Two current exceeded",
    0x05: "Total pressure undervoltage", 0x06: "Battery over temperature",
    0x07: "MOSFET over temperature", 0x08: "Abnormal current",
    0x09: "Balanced line dropped string", 0x0A: "Motherboard over temperature",
    0x0B: "Charge MOSFET on", 0x0C: "Short circuit protection",
    0x0D: "Discharge MOSFET abnormality", 0x0E: "Open failed",
    0x0F: "Manually turned off", 0x10: "Two level low voltage",
    0x11: "Low temperature protection", 0x12: "Voltage difference exceeded",
    0x13: "Self detect error",
}
BATTERY_STATUS = {0: "Unknown", 1: "Idle", 2: "Charge", 3: "Discharge", 4: "Standby", 5: "Error"}
BALANCER = {
    0x00: "Off", 0x01: "Exceeds the limit equilibrium",
    0x02: "Charge differential pressure balance",
    0x03: "Balanced over temperature", 0x04: "Automatic equalization",
    0x0A: "Motherboard over temperature",
}
BATTERY_TYPES = {0xFAF1: "Ternary Lithium", 0xFAF2: "LiFePO4", 0xFAF3: "LTO", 0xFAF4: "Custom"}


def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF


def chksum_legacy(data: bytes) -> int:
    return sum(data) & 0xFFFF


def u16be(data, i):
    return (data[i] << 8) | data[i + 1]


def u32be(data, i):
    return (u16be(data, i) << 16) | u16be(data, i + 2)


def u16le(data, i):
    return data[i] | (data[i + 1] << 8)


def u32le(data, i):
    return u16le(data, i) | (u16le(data, i + 2) << 16)


def i16le(data, i):
    v = u16le(data, i)
    return v - 0x10000 if v & 0x8000 else v


def i32le(data, i):
    v = u32le(data, i)
    return v - 0x100000000 if v & 0x80000000 else v


def fmt_runtime(seconds: int) -> str:
    return str(timedelta(seconds=int(seconds)))


def hexdump(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)


def build_modern(function: int, address: int, value_or_len: int) -> bytes:
    # frame: 7E A1 func addr_hi/lo-or addr/value bytes, CRC over bytes[1:6], AA 55
    # status: 7E A1 01 00 00 BE CRC_L CRC_H AA 55
    frame = bytearray([0x7E, 0xA1, function & 0xFF])
    if function in (0x01,):  # status: address 0x0000, len 0xBE
        frame += bytes([(address >> 8) & 0xFF, address & 0xFF, value_or_len & 0xFF])
    elif function == 0x02:  # device info
        frame += bytes([(address >> 8) & 0xFF, address & 0xFF, value_or_len & 0xFF])
    else:
        frame += bytes([address & 0xFF, (value_or_len >> 8) & 0xFF, value_or_len & 0xFF])
    crc = crc16_modbus(bytes(frame[1:]))
    frame += bytes([crc & 0xFF, (crc >> 8) & 0xFF, 0xAA, 0x55])
    return bytes(frame)


def build_modern_status() -> bytes:
    # Exact as ESPHome: 7e a1 01 00 00 be [crc] aa 55
    frame = bytearray([0x7E, 0xA1, 0x01, 0x00, 0x00, 0xBE])
    crc = crc16_modbus(bytes(frame[1:]))
    frame += bytes([crc & 0xFF, (crc >> 8) & 0xFF, 0xAA, 0x55])
    return bytes(frame)


def build_modern_device_info() -> bytes:
    # 7e a1 02 6c 02 20 [crc] aa 55  (address little-endian 0x026c, len 0x20)
    # From BLE: send_(ANT_COMMAND_DEVICE_INFO, 0x026c, 0x20, false)
    # build_frame for BLE likely packs address as LE
    frame = bytearray([0x7E, 0xA1, 0x02, 0x6C, 0x02, 0x20])
    crc = crc16_modbus(bytes(frame[1:]))
    frame += bytes([crc & 0xFF, (crc >> 8) & 0xFF, 0xAA, 0x55])
    return bytes(frame)


def parse_legacy(data: bytes) -> dict:
    if len(data) < 140:
        raise ValueError(f"legacy frame too short: {len(data)}")
    if data[0:4] != b"\xAA\x55\xAA\xFF":
        raise ValueError(f"bad legacy header: {hexdump(data[:4])}")
    cells_n = data[123]
    cells = [u16be(data, 6 + i * 2) * 0.001 for i in range(cells_n)]
    temps = [struct.unpack(">h", data[91 + i * 2:93 + i * 2])[0] for i in range(6)]
    current = struct.unpack(">i", data[70:74])[0] * 0.1
    total_v = u16be(data, 4) * 0.1
    charge = data[103]
    discharge = data[104]
    balancer = data[105]
    max_cell = data[115]
    min_cell = data[118]
    result = {
        "protocol": "legacy",
        "total_voltage_V": round(total_v, 3),
        "current_A": round(current, 3),
        "power_W": int(struct.unpack(">i", data[111:115])[0]),
        "soc_pct": data[74],
        "capacity_setting_Ah": round(u32be(data, 75) * 1e-6, 3),
        "capacity_remaining_Ah": round(u32be(data, 79) * 1e-6, 3),
        "cycle_capacity_Ah": round(u32be(data, 83) * 1e-3, 3),
        "total_runtime_s": u32be(data, 87),
        "total_runtime": fmt_runtime(u32be(data, 87)),
        "temperatures_C": temps,
        "charge_mosfet": {"code": charge, "status": CHARGE_MOSFET.get(charge, "Unknown")},
        "discharge_mosfet": {"code": discharge, "status": DISCHARGE_MOSFET.get(discharge, "Unknown")},
        "balancer": {"code": balancer, "status": BALANCER.get(balancer, "Unknown")},
        "cells_V": [round(v, 3) for v in cells],
        "cell_count": cells_n,
        "max_cell": {"index": max_cell, "voltage_V": round(u16be(data, 116) * 0.001, 3)},
        "min_cell": {"index": min_cell, "voltage_V": round(u16be(data, 119) * 0.001, 3)},
        "avg_cell_V": round(u16be(data, 121) * 0.001, 3),
        "delta_cell_V": round(u16be(data, 116) * 0.001 - u16be(data, 119) * 0.001, 3),
        "discharge_mosfet_ds_V": round(u16be(data, 124) * 0.1, 2),
        "drive_voltage_discharge_V": round(u16be(data, 126) * 0.1, 2),
        "drive_voltage_charge_V": round(u16be(data, 128) * 0.1, 2),
        "balance_bitmask": f"0x{u32be(data, 132):08X}",
        "system_log": f"0x{u16be(data, 136):04X}",
        "raw_hex": hexdump(data[:140]),
    }
    return result


def parse_modern(data: bytes) -> dict:
    if len(data) < 10 or data[0:2] != b"\x7E\xA1":
        raise ValueError(f"bad modern header: {hexdump(data[:4])}")
    function = data[2]
    data_len = data[5]
    expected = 6 + data_len + 4
    if len(data) < expected:
        # maybe truncated but try parse with what we have
        pass
    if function == 0x12:
        hw = data[6:22].split(b"\x00")[0].decode("ascii", "replace")
        sw = data[22:38].split(b"\x00")[0].decode("ascii", "replace")
        return {"protocol": "modern_device_info", "hardware": hw, "software": sw, "raw_hex": hexdump(data)}
    if function != 0x11:
        return {"protocol": "modern_other", "function": function, "raw_hex": hexdump(data)}

    cells_n = data[9]
    temp_n = data[8]
    cells = [u16le(data, 34 + i * 2) * 0.001 for i in range(cells_n)]
    offset = cells_n * 2
    temps = [i16le(data, 34 + offset + i * 2) for i in range(temp_n)]
    mosfet_t = i16le(data, 34 + offset + temp_n * 2)
    bal_t = i16le(data, 36 + offset + temp_n * 2)
    base = 38 + offset + temp_n * 2  # aligns with ESPHome offsets after temps

    # Recompute using ESPHome style offsets from cell start
    # After cells: temps (temp_n), then mosfet temp, balancer temp
    # Then at 38+offset (where offset = cells*2 + temp_n*2 in their second offset):
    # Their code: offset = cells*2; then after temps offset = cells*2 + temp_n*2
    # total_voltage at 38+offset, etc.
    off = cells_n * 2 + temp_n * 2
    btype = u16le(data, 94 + off) if len(data) > 95 + off else 0
    result = {
        "protocol": "modern",
        "permissions": data[6],
        "battery_status": {"code": data[7], "status": BATTERY_STATUS.get(data[7], "Unknown")},
        "temp_sensor_count": temp_n,
        "cell_count": cells_n,
        "protection_bitmask": hexdump(data[10:18]),
        "warning_bitmask": hexdump(data[18:26]),
        "balancing_bitmask": hexdump(data[26:34]),
        "cells_V": [round(v, 3) for v in cells],
        "temperatures_C": temps,
        "mosfet_temperature_C": mosfet_t,
        "balancer_temperature_C": bal_t,
        "total_voltage_V": round(u16le(data, 38 + off) * 0.01, 3),
        "current_A": round(i16le(data, 40 + off) * 0.1, 3),
        "soc_pct": i16le(data, 42 + off),
        "soh_pct": u16le(data, 44 + off),
        "charge_mosfet": {
            "code": data[46 + off],
            "status": CHARGE_MOSFET.get(data[46 + off], "Unknown"),
        },
        "discharge_mosfet": {
            "code": data[47 + off],
            "status": DISCHARGE_MOSFET.get(data[47 + off], "Unknown"),
        },
        "balancer": {
            "code": data[48 + off],
            "status": BALANCER.get(data[48 + off], "Unknown"),
        },
        "capacity_setting_Ah": round(u32le(data, 50 + off) * 1e-6, 3),
        "capacity_remaining_Ah": round(u32le(data, 54 + off) * 1e-6, 3),
        "cycle_capacity_Ah": round(u32le(data, 58 + off) * 1e-3, 3),
        "power_W": i32le(data, 62 + off),
        "total_runtime_s": u32le(data, 66 + off),
        "total_runtime": fmt_runtime(u32le(data, 66 + off)),
        "balanced_cell_bitmask": f"0x{u32le(data, 70 + off):08X}",
        "max_cell": {"voltage_V": round(u16le(data, 74 + off) * 0.001, 3), "index": u16le(data, 76 + off)},
        "min_cell": {"voltage_V": round(u16le(data, 78 + off) * 0.001, 3), "index": u16le(data, 80 + off)},
        "delta_cell_V": round(u16le(data, 82 + off) * 0.001, 3),
        "avg_cell_V": round(u16le(data, 84 + off) * 0.001, 3),
        "discharge_mosfet_ds_V": round(u16le(data, 86 + off) * 0.1, 2) if len(data) > 87 + off else None,
        "drive_voltage_discharge_V": round(u16le(data, 88 + off) * 0.1, 2) if len(data) > 89 + off else None,
        "drive_voltage_charge_V": round(u16le(data, 90 + off) * 0.1, 2) if len(data) > 91 + off else None,
        "battery_type": BATTERY_TYPES.get(btype, f"0x{btype:04X}"),
        "total_discharging_capacity_Ah": round(u32le(data, 96 + off) * 1e-3, 3) if len(data) > 99 + off else None,
        "total_charging_capacity_Ah": round(u32le(data, 100 + off) * 1e-3, 3) if len(data) > 103 + off else None,
        "total_discharging_time": fmt_runtime(u32le(data, 104 + off)) if len(data) > 107 + off else None,
        "total_charging_time": fmt_runtime(u32le(data, 108 + off)) if len(data) > 111 + off else None,
        "raw_hex": hexdump(data),
    }
    return result


def open_port(path: str, timeout: float = 2.0):
    # Baud is ignored by RFCOMM but set for completeness
    ser = serial.Serial(path, baudrate=19200, timeout=timeout, write_timeout=2)
    time.sleep(0.8)
    ser.reset_input_buffer()
    return ser


def transact(ser, payload: bytes, read_time: float = 2.5, label: str = "") -> bytes:
    ser.reset_input_buffer()
    print(f"\n>>> TX [{label}] ({len(payload)}): {hexdump(payload)}")
    ser.write(payload)
    ser.flush()
    end = time.time() + read_time
    buf = bytearray()
    last = time.time()
    while time.time() < end:
        chunk = ser.read(ser.in_waiting or 1)
        if chunk:
            buf.extend(chunk)
            last = time.time()
            # stop early if we have a complete-looking frame
            if buf.startswith(b"\xAA\x55\xAA\xFF") and len(buf) >= 140:
                break
            if buf.startswith(b"\x7E\xA1") and len(buf) >= 10:
                # try length field
                if len(buf) >= 6:
                    expect = 6 + buf[5] + 4
                    if len(buf) >= expect:
                        break
        elif buf and time.time() - last > 0.4:
            break
        else:
            time.sleep(0.02)
    print(f"<<< RX ({len(buf)}): {hexdump(buf) if buf else '<empty>'}")
    return bytes(buf)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="/dev/rfcomm0")
    ap.add_argument("--out", default="/home/pi/Documents/bms-tools/ant_bms_dump.json")
    args = ap.parse_args()

    print(f"Opening {args.port} ...")
    ser = open_port(args.port)
    print("Port open.")

    results = {"responses": [], "parsed": []}

    probes = [
        ("legacy_status", bytes([0x5A, 0x5A, 0x00, 0x00, 0x01, 0x01])),
        ("legacy_ble_db", bytes([0xDB, 0xDB, 0x00, 0x00, 0x00, 0x00])),
        ("modern_status", build_modern_status()),
        ("modern_device_info", build_modern_device_info()),
        # JBD fallback just in case
        ("jbd_basic", bytes.fromhex("DD A5 03 00 FF FD 77")),
        ("jbd_cells", bytes.fromhex("DD A5 04 00 FF FC 77")),
        ("jbd_hw", bytes.fromhex("DD A5 05 00 FF FB 77")),
        # ASCII / other guesses
        ("ascii_help", b"help\r\n"),
        ("ascii_AT", b"AT\r\n"),
    ]

    for label, payload in probes:
        raw = transact(ser, payload, read_time=3.0, label=label)
        entry = {"label": label, "tx": hexdump(payload), "rx_len": len(raw), "rx": hexdump(raw)}
        results["responses"].append(entry)
        if not raw:
            continue
        try:
            if raw.startswith(b"\xAA\x55\xAA\xFF"):
                parsed = parse_legacy(raw)
                results["parsed"].append(parsed)
                print("PARSED LEGACY:", json.dumps({k: v for k, v in parsed.items() if k != "raw_hex"}, ensure_ascii=False, indent=2))
            elif raw.startswith(b"\x7E\xA1"):
                # may contain multiple frames
                i = 0
                while i < len(raw):
                    if raw[i:i+2] != b"\x7E\xA1":
                        i += 1
                        continue
                    if i + 6 > len(raw):
                        break
                    expect = 6 + raw[i+5] + 4
                    frame = raw[i:i+expect]
                    if len(frame) < 8:
                        break
                    parsed = parse_modern(frame)
                    results["parsed"].append(parsed)
                    print("PARSED MODERN:", json.dumps({k: v for k, v in parsed.items() if k != "raw_hex"}, ensure_ascii=False, indent=2))
                    i += max(expect, 1)
            elif raw.startswith(b"\xDD"):
                results["parsed"].append({"protocol": "jbd_raw", "raw_hex": hexdump(raw)})
                print("Got JBD-like response")
            else:
                # try decode ascii
                try:
                    txt = raw.decode("ascii")
                    print("ASCII:", repr(txt))
                    results["parsed"].append({"protocol": "ascii", "text": txt})
                except Exception:
                    pass
        except Exception as e:
            print(f"Parse error for {label}: {e}")
            entry["parse_error"] = str(e)

        time.sleep(0.3)

    ser.close()
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nSaved dump to {args.out}")
    print(f"Parsed frames: {len(results['parsed'])}")


if __name__ == "__main__":
    main()
