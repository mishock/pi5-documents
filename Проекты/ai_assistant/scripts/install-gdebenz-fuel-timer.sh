#!/usr/bin/env bash
# Таймер user-systemd: мониторинг ГдеБЕНЗ → Telegram (по чатам с /gdebenz on).
set -euo pipefail
UNIT_DIR="${HOME}/.config/systemd/user"
PROJECT="/home/pi/Documents/Проекты/ai_assistant"
PYTHON="${PROJECT}/venv/bin/python3"
SCRIPT="${PROJECT}/gdebenz_fuel.py"
LOG="${HOME}/logs/fuel-gdebenz/monitor.log"
ENABLE_TIMER="${GDEBENZ_FUEL_ENABLE_TIMER:-0}"

mkdir -p "${HOME}/logs/fuel-gdebenz" "${UNIT_DIR}"

cat > "${UNIT_DIR}/gdebenz-fuel.service" << EOF
[Unit]
Description=GdeBENZ fuel watch (crowd map alerts)
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=${PROJECT}
Environment=HOME=${HOME}
ExecStart=/usr/bin/env bash -c '${PYTHON} ${SCRIPT} --monitor >> ${LOG} 2>&1'
EOF

cat > "${UNIT_DIR}/gdebenz-fuel.timer" << 'EOF'
[Unit]
Description=Run GdeBENZ fuel watch every 30 minutes

[Timer]
OnBootSec=3min
OnUnitActiveSec=30min
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl --user daemon-reload
if [[ "$ENABLE_TIMER" == "1" ]]; then
  systemctl --user enable --now gdebenz-fuel.timer
  echo "OK: gdebenz-fuel.timer enabled (каждые 30 мин)"
  systemctl --user list-timers gdebenz-fuel.timer --no-pager
else
  systemctl --user disable --now gdebenz-fuel.timer 2>/dev/null || true
  systemctl --user disable --now gdebenz-qr-monitor.timer 2>/dev/null || true
  echo "OK: gdebenz-fuel.timer / gdebenz-qr-monitor.timer disabled (по умолчанию с 2026-08-04)"
fi
echo "Лог: ${LOG}"
echo "Полное отключение: bash ${PROJECT}/scripts/disable-gdebenz-fuel-monitor.sh"
echo "В боте: /gdebenz — разовая сводка; автопуш выключен (monitoring_disabled)"
