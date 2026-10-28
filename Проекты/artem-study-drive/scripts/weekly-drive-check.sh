#!/usr/bin/env bash
# Еженедельная проверка папки «Учёба Артём» на Google Drive.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="${HOME}/logs/artem-study-drive.log"
mkdir -p "$(dirname "$LOG")"

export GOOGLE_MCP_PROXY="${GOOGLE_MCP_PROXY:-socks5h://127.0.0.1:10808}"
GMCP="/home/pi/Projects/google-mcp"
SCRIPT="${ROOT}/scripts/drive-check.mjs"

{
  echo "=== $(date '+%Y-%m-%dT%H:%M:%S%z') artem-study weekly check ==="
  cd "$GMCP"
  node "$SCRIPT"
  node "${ROOT}/scripts/site-monitor.mjs"
  node "${ROOT}/scripts/academic-monitor.mjs"
  node "${ROOT}/scripts/knowledge-sync.mjs"
  echo "=== done ==="
} >>"$LOG" 2>&1
