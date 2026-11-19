#!/usr/bin/env bash
# User-systemd: раз в месяц — проверка госаккредитации 09.02.07 + email при изменении.
# Обновлено: 2026-11-19
set -euo pipefail

UNIT_DIR="${HOME}/.config/systemd/user"
ROOT="${HOME}/Documents/Проекты/artem-study-drive"
FULL="${ROOT}/scripts/monthly-accreditation-check.sh"
mkdir -p "$UNIT_DIR"
chmod +x "$FULL"
chmod +x "${ROOT}/scripts/accreditation-monitor.mjs" 2>/dev/null || true

cat > "${UNIT_DIR}/artem-study-accreditation.service" << EOF
[Unit]
Description=Учёба Артём: месячная проверка госаккредитации 09.02.07
After=network-online.target

[Service]
Type=oneshot
Environment=HOME=${HOME}
Environment=LANG=ru_RU.UTF-8
ExecStart=/bin/bash ${FULL}
EOF

cat > "${UNIT_DIR}/artem-study-accreditation.timer" << 'EOF'
[Unit]
Description=Учёба Артём: аккредитация 09.02.07 — 1-е число месяца 10:00 MSK

[Timer]
OnCalendar=*-*-01 10:00:00
Persistent=true
Unit=artem-study-accreditation.service

[Install]
WantedBy=timers.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now artem-study-accreditation.timer
echo "OK: artem-study-accreditation.timer — 1-е число, 10:00 MSK"
systemctl --user list-timers 'artem-study-accreditation*' --no-pager
echo "Лог: ${HOME}/logs/artem-accreditation.log"
echo "Снимок: ${ROOT}/data/accreditation-snapshot.json"
echo "Сводка: ${ROOT}/data/00_Аккредитация_09.02.07.md"
echo "Вручную: node ${ROOT}/scripts/accreditation-monitor.mjs"
echo "Письмо при изменениях → mishock24@gmail.com"
