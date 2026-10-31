#!/usr/bin/env python3
"""JK-B2A8S20P BLE через Bumble HCI USER (Pi 3 / BCM43438 UART).

Обновлено: 2026-10-31

Корневая проблема Pi3: Wi‑Fi и BT на одном чипе (BCM43438A1). В dmesg —
«Frame reassembly failed (-84)»; линк живёт 1–3 с (HCI reason 8/62), полного
кадра 0x02 (~300 B) часто не хватает. Wi‑Fi ОТКЛЮЧАТЬ НЕЛЬЗЯ (гараж = интернет).

Стратегия:
- без GATT discover;
- write только FFE2@0x10 (FFE1@0x12 сыпет AT\\r\\n);
- после первого JK-заголовка больше не TX — только слушать;
- короткий connect, мало попыток;
- Wi‑Fi только txpower↓ в обёртке, никогда radio off.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import struct
import sys
import time
from datetime import datetime
from pathlib import Path

import bumble.device as bumble_device
from bumble.core import PhysicalTransport
from bumble.device import Device, Peer
from bumble.hci import Address, OwnAddressType
from bumble.transport import open_transport

# Узкое окно скана + длинный supervision (мс в API Bumble)
bumble_device.DEVICE_DEFAULT_CONNECT_SCAN_INTERVAL = 80
bumble_device.DEVICE_DEFAULT_CONNECT_SCAN_WINDOW = 40
bumble_device.DEVICE_DEFAULT_CONNECTION_SUPERVISION_TIMEOUT = 8000

MAC_DEFAULT = "C8:47:80:53:0F:B6"
FFE2_WRITE = 0x10
FFE1_CCCD = 0x13


def csum(data: bytes) -> int:
    return sum(data) & 0xFF


def req(cmd: int = 0x96) -> bytes:
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
    idx = frame.find(b"\x55\xaa\xeb\x90\x02")
    if idx < 0 or len(frame) < idx + 180:
        return None
    d = frame[idx:]
    cells: list[float] = []
    for i in range(32):
        off = 6 + i * 2
        if off + 1 >= len(d):
            break
        mv = u16(d, off)
        if 1500 < mv < 4500:
            cells.append(round(mv * 0.001, 3))
    o = 32  # JK02_32S
    sample = {
        "pack_V": round(u32(d, 118 + o) * 0.001, 3),
        "current_A": round(i32(d, 126 + o) * 0.001, 3),
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


def frame_types(raw: bytes) -> list[int]:
    out: list[int] = []
    i = 0
    while True:
        j = raw.find(b"\x55\xaa\xeb\x90", i)
        if j < 0 or j + 5 > len(raw):
            break
        out.append(raw[j + 4])
        i = j + 5
    return out


def save_rx(raw: bytes) -> None:
    if not raw:
        return
    try:
        Path("/home/pi/jk4s-ble/logs").mkdir(parents=True, exist_ok=True)
        Path("/home/pi/jk4s-ble/logs/last_rx.bin").write_bytes(raw)
        Path("/home/pi/jk4s-ble/logs/last_rx.hex").write_text(raw.hex(" "), encoding="utf-8")
        Path("/tmp/jk4s_last_rx.bin").write_bytes(raw)
        Path(f"/home/pi/jk4s-ble/logs/rx-{int(time.time())}.bin").write_bytes(raw)
    except Exception:
        pass


async def wait_adv(device: Device, addr: str, seconds: float = 8.0) -> bool:
    target = addr.upper().replace("-", ":")
    found = asyncio.Event()

    def on_adv(advertisement) -> None:
        try:
            a = str(advertisement.address).upper().replace("-", ":").split("/")[0]
            if a == target or target in a:
                print(f"ADV {a}", file=sys.stderr, flush=True)
                found.set()
        except Exception:
            pass

    device.on("advertisement", on_adv)
    await device.start_scanning(filter_duplicates=True, scan_interval=80, scan_window=40)
    try:
        try:
            await asyncio.wait_for(found.wait(), timeout=seconds)
            return True
        except asyncio.TimeoutError:
            print("ADV timeout — connect всё равно", file=sys.stderr, flush=True)
            return False
    finally:
        await device.stop_scanning()
        await asyncio.sleep(0.05)


async def once(device: Device, addr: str, *, skip_adv: bool = False) -> dict:
    if not skip_adv:
        await wait_adv(device, addr, seconds=8.0)

    peer_addr = Address(addr, Address.PUBLIC_DEVICE_ADDRESS)
    print("connecting…", file=sys.stderr, flush=True)
    connection = await device.connect(
        peer_addr,
        transport=PhysicalTransport.LE,
        own_address_type=OwnAddressType.PUBLIC,
        timeout=25.0,
    )
    print("CONNECTED", connection.handle, file=sys.stderr, flush=True)
    disconnected = asyncio.Event()
    disc_reason: list = []

    def on_disc(reason=None):
        disc_reason.append(reason)
        print("DISCONNECTED", reason, file=sys.stderr, flush=True)
        disconnected.set()

    connection.on("disconnection", on_disc)
    # Не update_parameters — на Cypress часто reason 62.

    peer = Peer(connection)
    client = peer.gatt_client
    buf = bytearray()
    got_jk = asyncio.Event()

    def on_value(value: bytes) -> None:
        raw = bytes(value)
        if not raw or raw in (b"AT\r\n", b"OK\r\n", b"ERROR\r\n"):
            return
        # отрезать ведущие AT\r\n в том же куске
        if raw.startswith(b"AT\r\n"):
            raw = raw[4:]
            if not raw:
                return
        buf.extend(raw)
        print(f"+{len(raw)} total={len(buf)}", file=sys.stderr, flush=True)
        if b"\x55\xaa\xeb\x90" in buf:
            got_jk.set()

    for h in (0x12, 0x10, 0x05, 0x03, 0x11, 0x13):
        client.notification_subscribers.setdefault(h, set()).add(on_value)

    # CCCD без response; ошибка не фатальна
    try:
        await peer.write_value(FFE1_CCCD, struct.pack("<H", 0x0001), with_response=False)
        print(f"CCCD @{FFE1_CCCD:#x}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"CCCD skip: {e}", file=sys.stderr, flush=True)

    async def ask(cmd: int) -> None:
        if disconnected.is_set():
            return
        try:
            await peer.write_value(FFE2_WRITE, req(cmd), with_response=False)
            print(f"TX 0x{cmd:02x} → ffe2@{FFE2_WRITE:#x}", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"TX fail: {e}", file=sys.stderr, flush=True)

    async def listen(max_s: float) -> None:
        t0 = time.time()
        while time.time() - t0 < max_s and not disconnected.is_set():
            sample = parse_jk02_32s(bytes(buf))
            if sample and sample.get("cell_count", 0) >= 4:
                return
            await asyncio.sleep(0.08)

    # Быстрый путь: сразу cell info 0x96; если пошёл JK-поток — больше не пинаем
    await asyncio.sleep(0.1)
    if not disconnected.is_set():
        await ask(0x96)
        try:
            await asyncio.wait_for(got_jk.wait(), timeout=2.5)
            print("JK header seen — listen only", file=sys.stderr, flush=True)
            await listen(max_s=6.0)
        except asyncio.TimeoutError:
            if not disconnected.is_set():
                await ask(0x97)
                await listen(max_s=4.0)
            if not disconnected.is_set() and b"\x55\xaa\xeb\x90\x02" not in buf:
                await ask(0x96)
                await listen(max_s=5.0)

    raw = bytes(buf)
    save_rx(raw)
    sample = parse_jk02_32s(raw)
    types = frame_types(raw)
    print(f"rx={len(raw)} types={types} disc={disc_reason}", file=sys.stderr, flush=True)

    try:
        if not disconnected.is_set():
            await connection.disconnect()
    except Exception:
        pass

    if not sample:
        head = raw[:64].hex(" ") if raw else ""
        raise RuntimeError(
            f"no JK02 frame rx={len(raw)} types={types} disc={disc_reason} head={head}"
        )
    return sample


async def run(addr: str, attempts: int) -> dict:
    last_err: BaseException | None = None
    async with await open_transport("hci-socket:0") as (source, sink):
        device = Device.with_hci("Pi3-JK4S", "F0:F1:F2:F3:F4:F6", source, sink)
        await device.power_on()
        await asyncio.sleep(0.25)
        for i in range(1, attempts + 1):
            print(f"=== attempt {i}/{attempts} ===", file=sys.stderr, flush=True)
            try:
                return await once(device, addr, skip_adv=(i > 1))
            except BaseException as e:
                if isinstance(e, (KeyboardInterrupt, SystemExit)):
                    raise
                last_err = e
                print(f"FAIL {type(e).__name__}: {e}", file=sys.stderr, flush=True)
                await asyncio.sleep(2.5 if i < attempts else 0)
    raise RuntimeError(str(last_err) if last_err else "failed")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("addr", nargs="?", default=MAC_DEFAULT)
    ap.add_argument("-n", "--attempts", type=int, default=3)
    ap.add_argument("-o", "--out", default="")
    args = ap.parse_args()
    sample = asyncio.run(run(args.addr, args.attempts))
    snap = {
        "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
        "mac": args.addr,
        "name": "AKB-4S-230",
        "online": True,
        "mode": mode_of(sample),
        "charge_mos": "On" if sample.get("charge_mos") else "Off",
        "discharge_mos": "On" if sample.get("discharge_mos") else "Off",
        "balancer": sample.get("balance_action"),
        **sample,
    }
    text = json.dumps(snap, ensure_ascii=False, indent=2)
    print(text)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(json.dumps({"online": False, "error": str(e)}), flush=True)
        raise SystemExit(1) from e
