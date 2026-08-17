#!/usr/bin/env python3
"""Home Assistant helper: queue ANT24C MOS/balancer commands, read switch state."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

CMD = Path("/config/host_status/ant24c_cmd.json")
RES = Path("/config/host_status/ant24c_cmd_result.json")
SNAP = Path("/config/host_status/ant24c.json")
KEYS = {
    "charge": "charge_on",
    "discharge": "discharge_on",
    "balancer": "balancer_on",
}


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def cmd_state(target: str) -> None:
    data = _load(SNAP)
    print("on" if data.get("online") and data.get(KEYS[target]) else "off")


def set_cmd(target: str, on: bool) -> int:
    cmd_id = f"{time.time():.6f}"
    payload = {"id": cmd_id, "target": target, "on": on, "ts": time.time()}
    CMD.parent.mkdir(parents=True, exist_ok=True)
    tmp = CMD.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload) + "\n")
    tmp.replace(CMD)
    deadline = time.time() + 18
    while time.time() < deadline:
        rec = _load(RES)
        if rec.get("id") == cmd_id:
            if rec.get("ok"):
                return 0
            print(rec.get("error") or "BMS command failed", file=sys.stderr)
            return 1
        time.sleep(0.2)
    print("timeout waiting for ANT24C logger", file=sys.stderr)
    return 1


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: ant24c_switch.py state <charge|discharge|balancer>", file=sys.stderr)
        print("       ant24c_switch.py <charge|discharge|balancer> <0|1>", file=sys.stderr)
        return 2
    if argv[1] == "state":
        if len(argv) < 3 or argv[2] not in KEYS:
            print("unknown target", file=sys.stderr)
            return 2
        cmd_state(argv[2])
        return 0
    target = argv[1]
    if target not in KEYS or len(argv) < 3:
        print("unknown target", file=sys.stderr)
        return 2
    on = argv[2].lower() in ("1", "on", "true", "yes")
    return set_cmd(target, on)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
