#!/usr/bin/env python3
"""Чтение поля jk4s.json для Home Assistant command_line.

Обновлено: 2026-10-31
Нет значения → exit 1 (sensor unavailable). Не печатать пустую строку.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SNAP = Path("/config/host_status/jk4s.json")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: jk4s_read.py <key|cell_N>", file=sys.stderr)
        return 2
    key = sys.argv[1]
    try:
        data = json.loads(SNAP.read_text(encoding="utf-8"))
    except Exception:
        return 1

    if key.startswith("cell_") and key[5:].isdigit():
        idx = int(key[5:]) - 1
        cells = data.get("cells_V")
        if not isinstance(cells, list) or idx < 0 or idx >= len(cells):
            return 1
        value = cells[idx]
        if value is None:
            return 1
        print(value)
        return 0

    value = data.get(key)
    if value is None:
        return 1
    print(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
