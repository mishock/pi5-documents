#!/usr/bin/env bash
# Заливка через ST-Link (SWD) или dfu-util (USB-C boot0)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PROTO="${1:-stlink}"
pio run -e generic_h503cbtx -t upload --upload-protocol "$PROTO"
