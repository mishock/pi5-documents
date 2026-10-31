#!/usr/bin/env python3
"""JK-B2A8S20P BLE через Bumble HCI USER (обход BlueZ/Cypress на Pi 3).

Обновлено: 2026-10-31
Требования: bluetoothd stop, hci0 DOWN, root. UUID FFE1.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from datetime import datetime

import bumble.device as bumble_device
from bumble.core import PhysicalTransport, UUID
from bumble.device import Device, Peer
from bumble.hci import Address, OwnAddressType
from bumble.transport import open_transport

# Сосуществование с Wi‑Fi
bumble_device.DEVICE_DEFAULT_CONNECT_SCAN_INTERVAL = 100
bumble_device.DEVICE_DEFAULT_CONNECT_SCAN_WINDOW = 30
bumble_device.DEVICE_DEFAULT_CONNECTION_SUPERVISION_TIMEOUT = 4000

FFE1 = UUID("FFE1")
MAC_DEFAULT = "C8:47:80:53:0F:B6"


def is_uuid(ch_uuid, short: str) -> bool:
    u = str(ch_uuid).upper()
    return ch_uuid == UUID(short) or f"0000{short.upper()}" in u


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


async def wait_adv(device: Device, addr: str, seconds: float = 20.0) -> bool:
    """Скан ADV; при таймауте всё равно пробуем connect (как Daly)."""
    target = addr.upper().replace("-", ":")
    found = asyncio.Event()

    def on_adv(advertisement) -> None:
        try:
            a = str(advertisement.address).upper().replace("-", ":")
            # Bumble часто даёт "XX:YY:…/P" или "/R"
            a_clean = a.split("/")[0]
            if a_clean == target or target in a:
                print(f"ADV {a}", file=sys.stderr, flush=True)
                found.set()
        except Exception:
            pass

    device.on("advertisement", on_adv)
    await device.start_scanning(
        filter_duplicates=True,
        scan_interval=100,
        scan_window=30,
    )
    try:
        try:
            await asyncio.wait_for(found.wait(), timeout=seconds)
            return True
        except asyncio.TimeoutError:
            print("ADV timeout — connect всё равно", file=sys.stderr, flush=True)
            return False
    finally:
        await device.stop_scanning()
        await asyncio.sleep(0.15)


async def once(device: Device, addr: str) -> dict:
    await wait_adv(device, addr, seconds=18.0)

    peer_addr = Address(addr, Address.PUBLIC_DEVICE_ADDRESS)
    print("connecting…", file=sys.stderr, flush=True)
    connection = await device.connect(
        peer_addr,
        transport=PhysicalTransport.LE,
        own_address_type=OwnAddressType.PUBLIC,
        timeout=40.0,
    )
    print("CONNECTED", connection.handle, file=sys.stderr, flush=True)
    disconnected = asyncio.Event()
    disc_reason: list = []

    def on_disc(reason=None):
        disc_reason.append(reason)
        print("DISCONNECTED", reason, file=sys.stderr, flush=True)
        disconnected.set()

    connection.on("disconnection", on_disc)

    # Минимальная пауза: JK сыпет notify сразу — надо быстро найти FFE1 и подписаться
    try:
        await asyncio.wait_for(disconnected.wait(), timeout=0.6)
        raise RuntimeError(f"early disconnect {disc_reason}")
    except asyncio.TimeoutError:
        print("STABLE", file=sys.stderr, flush=True)

    peer = Peer(connection)
    buf = bytearray()

    def on_value(value: bytes) -> None:
        buf.extend(bytes(value))
        print(f"+{len(value)} total={len(buf)}", file=sys.stderr, flush=True)

    # Только сервис FFE0 — быстрее полного discover
    notify_c = write_c = None
    for attempt in range(4):
        if disconnected.is_set():
            raise RuntimeError(f"disc during discover: {disc_reason}")
        try:
            await asyncio.wait_for(
                peer.discover_services([UUID("FFE0")]),
                timeout=12,
            )
            for service in peer.services:
                # только FFE0 — иначе discover всех сервисов рвёт линк (notify flood)
                if not is_uuid(service.uuid, "FFE0"):
                    continue
                await asyncio.wait_for(service.discover_characteristics(), timeout=8)
                for ch in service.characteristics:
                    print(" CHAR", ch.uuid, ch.properties, file=sys.stderr, flush=True)
                    if is_uuid(ch.uuid, "FFE1"):
                        notify_c = ch
                        if write_c is None:
                            write_c = ch
                    elif is_uuid(ch.uuid, "FFE2"):
                        write_c = ch
            if notify_c and write_c:
                break
        except Exception as e:
            print(f"discover attempt {attempt+1}: {type(e).__name__} {e}", file=sys.stderr, flush=True)
            await asyncio.sleep(0.6)
    else:
        # fallback: полный discover
        await asyncio.wait_for(peer.discover_services(), timeout=15)
        for service in peer.services:
            await service.discover_characteristics()
            for ch in service.characteristics:
                if is_uuid(ch.uuid, "FFE1"):
                    notify_c = ch
                    if write_c is None:
                        write_c = ch
                elif is_uuid(ch.uuid, "FFE2"):
                    write_c = ch

    if not notify_c or not write_c:
        raise RuntimeError("no FFE1 characteristic")

    await notify_c.subscribe(on_value)
    await asyncio.sleep(0.25)

    async def ask(cmd: int) -> None:
        payload = req(cmd)
        for target in (write_c, notify_c):
            if target is None:
                continue
            try:
                await target.write_value(payload, with_response=False)
                print(f"TX 0x{cmd:02x} → {target.uuid}", file=sys.stderr, flush=True)
                return
            except Exception as e:
                print(f"write {target.uuid} fail: {e}", file=sys.stderr, flush=True)

    # На Pi5 0x02 шёл потоком после 0x97/длительного коннекта; 0x96 часто даёт 0x01.
    for cmd in (0x96, 0x97, 0x96, 0x96):
        if disconnected.is_set():
            break
        await ask(cmd)
        await asyncio.sleep(0.8)

    # Ждём 0x02 до 18 с, пока линк жив
    t0 = time.time()
    while time.time() - t0 < 18.0:
        if b"\x55\xaa\xeb\x90\x02" in buf:
            break
        if disconnected.is_set():
            break
        # периодически пинаем cell info
        if int(time.time() - t0) in (5, 10, 14):
            await ask(0x96)
            await asyncio.sleep(0.3)
        await asyncio.sleep(0.15)

    # добрать хвост кадра 0x02
    if b"\x55\xaa\xeb\x90\x02" in buf:
        last = len(buf)
        stable = 0
        for _ in range(50):
            await asyncio.sleep(0.08)
            if len(buf) == last:
                stable += 1
                if stable >= 6:
                    break
            else:
                last = len(buf)
                stable = 0

    raw = bytes(buf)
    # отладка: сохранить сырой BLE-буфер
    try:
        Path = __import__("pathlib").Path
        Path("/home/pi/jk4s-ble/logs").mkdir(parents=True, exist_ok=True)
        Path("/home/pi/jk4s-ble/logs/last_rx.bin").write_bytes(raw)
        Path("/home/pi/jk4s-ble/logs/last_rx.hex").write_text(raw.hex(" "), encoding="utf-8")
    except Exception:
        pass

    sample = parse_jk02_32s(raw)
    if not sample:
        # любой JK header (0x01 settings / 0x02 cell / 0x03 device)
        idx = raw.find(b"\x55\xaa\xeb\x90")
        print(
            f"parse miss idx={idx} head={raw[:80].hex(' ') if raw else ''}",
            file=sys.stderr,
            flush=True,
        )
        if idx >= 0 and len(raw) > idx + 5 and raw[idx + 4] != 0x02:
            # дождаться/запросить ещё раз cell info
            try:
                await write_c.write_value(req(0x96), with_response=False)
                await asyncio.sleep(3.0)
                raw = bytes(buf)
                sample = parse_jk02_32s(raw)
            except Exception:
                pass
    try:
        if not disconnected.is_set():
            await connection.disconnect()
    except Exception:
        pass
    if not sample:
        raise RuntimeError(f"no JK02 frame rx={len(raw)} disc={disc_reason}")
    return sample


async def run(addr: str, attempts: int) -> dict:
    last_err: Exception | None = None
    async with await open_transport("hci-socket:0") as (source, sink):
        device = Device.with_hci("Pi3-JK4S", "F0:F1:F2:F3:F4:F6", source, sink)
        await device.power_on()
        await asyncio.sleep(0.4)
        for i in range(1, attempts + 1):
            print(f"=== attempt {i}/{attempts} ===", file=sys.stderr, flush=True)
            try:
                sample = await once(device, addr)
                return sample
            except Exception as e:
                last_err = e
                print(f"FAIL {type(e).__name__}: {e}", file=sys.stderr, flush=True)
                await asyncio.sleep(4.0 if i < attempts else 0)
    raise RuntimeError(str(last_err) if last_err else "failed")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("addr", nargs="?", default=MAC_DEFAULT)
    ap.add_argument("-n", "--attempts", type=int, default=6)
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
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(json.dumps({"online": False, "error": str(e)}), flush=True)
        raise SystemExit(1) from e
