#!/usr/bin/env bash
# Быстрая проверка (без Drive): сайт + успеваемость + справочник.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="${HOME}/logs/artem-study-drive.log"
mkdir -p "$(dirname "$LOG")"

export GOOGLE_MCP_PROXY="${GOOGLE_MCP_PROXY:-socks5h://127.0.0.1:10808}"

{
  echo "=== $(date '+%Y-%m-%dT%H:%M:%S%z') artem-study quick check ==="
  cd /home/pi/Projects/google-mcp
  node "${ROOT}/scripts/site-monitor.mjs"
  node "${ROOT}/scripts/academic-monitor.mjs"
  node "${ROOT}/scripts/knowledge-sync.mjs"
  echo "=== quick done ==="
} >>"$LOG" 2>&1
