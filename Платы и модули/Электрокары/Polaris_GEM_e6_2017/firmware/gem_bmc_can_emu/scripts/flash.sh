#!/usr/bin/env bash
# Заливка gem_bmc_can_emu на Nano (через tools из Проекты/Arduino)
set -euo pipefail

FW_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FW_HEX="$FW_DIR/gem_bmc_can_emu.hex"
ARDUINO_ROOT="/home/pi/Documents/Проекты/Arduino"
ARDUINO_BOARD="${ARDUINO_BOARD:-nano}"
BOARD_SCRIPTS="$ARDUINO_ROOT/boards/$ARDUINO_BOARD/scripts"

if [[ ! -f "$FW_HEX" ]]; then
  echo "Нет hex: $FW_HEX — сначала: bash $(dirname "$0")/build.sh"
  exit 1
fi
if [[ ! -x "$BOARD_SCRIPTS/flash-hex.sh" ]]; then
  echo "Нет flash-hex: $BOARD_SCRIPTS/flash-hex.sh"
  exit 1
fi
exec bash "$BOARD_SCRIPTS/flash-hex.sh" "$FW_HEX"
