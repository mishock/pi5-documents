#!/usr/bin/env bash
# Одноразовый (и повторяемый) таймер: обновление Xray после полуночи MSK.
#   bash Проекты/ai_assistant/scripts/install-xray-nightly-update-timer.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_SRC="${ROOT}/scripts/xray-nightly-update.sh"
SCRIPT_DST="/home/pi/bin/xray-nightly-update.sh"
UNIT_NAME="xray-nightly-update"
ENV_FILE="/home/pi/.config/xray-panel.env"

install -m 755 "$SCRIPT_SRC" "$SCRIPT_DST"
mkdir -p /home/pi/logs /home/pi/.config

if [[ ! -f "$ENV_FILE" ]]; then
  token="$(grep -E '^\| API Token \|' /home/pi/Documents/vpn-guide.md 2>/dev/null | sed -n 's/.*`\([^`]*\)`.*/\1/p' | head -1 || true)"
  cat >"$ENV_FILE" <<EOF
# 3x-ui API (не коммитить). Источник: vpn-guide.md
XUI_API_BASE=https://89.127.199.6:37702/q6omE9HRd1U9d6t4XH
XUI_API_TOKEN=${token}
EOF
  chmod 600 "$ENV_FILE"
  chown pi:pi "$ENV_FILE"
fi

sudo tee "/etc/systemd/system/${UNIT_NAME}.service" >/dev/null <<EOF
[Unit]
Description=Nightly Xray update (VPS + Pi5) with double verify
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=oneshot
User=pi
Group=pi
Environment=HOME=/home/pi
WorkingDirectory=/home/pi
ExecStart=${SCRIPT_DST}
Nice=10

[Install]
WantedBy=multi-user.target
EOF

sudo tee "/etc/systemd/system/${UNIT_NAME}.timer" >/dev/null <<'EOF'
[Unit]
Description=Run Xray nightly update at 00:20 MSK

[Timer]
OnCalendar=*-*-* 00:20:00
Persistent=true
RandomizedDelaySec=120

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now "${UNIT_NAME}.timer"
systemctl list-timers "${UNIT_NAME}.timer" --no-pager
echo "OK: ${SCRIPT_DST} + timer ${UNIT_NAME}.timer (00:20 MSK, Persistent)"
