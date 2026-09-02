#!/usr/bin/env bash
# Сборка gem_bmc_can_emu (Arduino Nano + MCP2515)
set -euo pipefail

FW_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FW_NAME="gem_bmc_can_emu"
FW_HEX="$FW_DIR/$FW_NAME.hex"
FW_INO="$FW_DIR/$FW_NAME.ino"
LIB_DIR="$FW_DIR/lib"

export PATH="${HOME}/.local/bin:${PATH}"
CLI="${ARDUINO_CLI:-}"
for c in "${HOME}/.local/bin/arduino-cli" /tmp/arduino-cli/arduino-cli; do
  [[ -x "$c" ]] && CLI="$c" && break
done

FQBN="${ARDUINO_FQBN:-arduino:avr:nano:cpu=atmega328}"

[[ -f "$FW_INO" ]] || { echo "Нет скетча: $FW_INO"; exit 1; }
[[ -x "$CLI" ]] || { echo "Нужен arduino-cli: $CLI"; exit 1; }

mkdir -p "$FW_DIR/build"
echo "Сборка: $FW_NAME → $FQBN"
"$CLI" compile -b "$FQBN" "$FW_DIR" \
  --libraries "$LIB_DIR" \
  --output-dir "$FW_DIR/build"

for cand in "$FW_DIR/build/$FW_NAME.ino.hex" "$FW_DIR/$FW_NAME.ino.hex"; do
  if [[ -f "$cand" ]]; then
    cp -f "$cand" "$FW_HEX"
    echo "Собрано: $FW_HEX"
    exit 0
  fi
done
echo "arduino-cli не создал hex — см. $FW_DIR/build/"
exit 1
