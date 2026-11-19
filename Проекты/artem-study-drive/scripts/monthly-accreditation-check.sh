#!/usr/bin/env bash
# Месячная проверка госаккредитации 09.02.07 на сайте КИПУ.
# Обновлено: 2026-11-19
set -euo pipefail

ROOT="${HOME}/Documents/Проекты/artem-study-drive"
LOG="${HOME}/logs/artem-accreditation.log"
mkdir -p "$(dirname "$LOG")"

{
  echo "=== $(date '+%Y-%m-%dT%H:%M:%S%z') artem accreditation monthly ==="
  node "${ROOT}/scripts/accreditation-monitor.mjs" "$@"
  echo "=== done exit=$? ==="
} >>"$LOG" 2>&1
