#!/usr/bin/env bash
# User-systemd: раз в неделю — полная проверка Drive + сайт + справочник.
set -euo pipefail

UNIT_DIR="${HOME}/.config/systemd/user"
ROOT="${HOME}/Documents/Проекты/artem-study-drive"
FULL="${ROOT}/scripts/weekly-drive-check.sh"
mkdir -p "$UNIT_DIR"
chmod +x "$FULL"
chmod +x "${ROOT}/scripts/"*.mjs "${ROOT}/scripts/"*.sh 2>/dev/null || true

cat > "${UNIT_DIR}/artem-study-drive-check.service" << EOF
[Unit]
Description=Учёба Артём: еженедельная проверка (Drive + сайт + справочник)
After=network-online.target

[Service]
Type=oneshot
Environment=HOME=${HOME}
Environment=GOOGLE_MCP_PROXY=socks5h://127.0.0.1:10808
ExecStart=/bin/bash ${FULL}
EOF

cat > "${UNIT_DIR}/artem-study-drive-check.timer" << 'EOF'
[Unit]
Description=Учёба Артём: еженедельно, понедельник 09:00 MSK

[Timer]
OnCalendar=Mon *-*-* 09:00:00
Persistent=true
Unit=artem-study-drive-check.service

[Install]
WantedBy=timers.target
EOF

systemctl --user disable --now artem-study-quick-check.timer 2>/dev/null || true
systemctl --user daemon-reload
systemctl --user enable --now artem-study-drive-check.timer
echo "OK: artem-study-drive-check.timer — понедельник 09:00 (раз в неделю)"
systemctl --user list-timers 'artem-study-*' --no-pager
echo "Лог: ${HOME}/logs/artem-study-drive.log"
echo "Справочник: 00_Справочник_КИПУ_Артём.md"
