#!/usr/bin/env bash
# Сборка прошивки GEM BMC emu для PB MCU01 H503A
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if ! command -v pio >/dev/null 2>&1; then
  echo "Нужен PlatformIO: pip install platformio"
  exit 1
fi
pio run -e generic_h503cbtx "$@"

BIN="$ROOT/.pio/build/generic_h503cbtx/firmware.bin"
REL="$ROOT/releases"
if [[ -f "$BIN" ]]; then
  mkdir -p "$REL"
  cp -f "$BIN" "$REL/gem_bmc_can_emu_h503_v4.2.bin"
  echo "Артефакт: $REL/gem_bmc_can_emu_h503_v4.2.bin ($(wc -c < "$BIN") B)"
fi
