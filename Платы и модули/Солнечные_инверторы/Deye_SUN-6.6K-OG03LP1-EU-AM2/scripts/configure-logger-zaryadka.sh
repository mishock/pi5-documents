#!/bin/bash
# Настройка Wi‑Fi logger «Зарядка» (10.1.30.81) — режим сбора, TCP :8899, перезапуск.
# Пароль: PWD с наклейки модуля (не хранить в репозитории).
set -euo pipefail

HOST="${LOGGER_HOST:-10.1.30.81}"
USER="${LOGGER_USER:-admin}"
PASS="${LOGGER_PASS:?Задайте LOGGER_PASS (PWD с наклейки Wi‑Fi-модуля)}"
BASE="http://${HOST}:80"

auth=(-u "${USER}:${PASS}")

post_restart() {
	local data="$1"
	curl -sf "${auth[@]}" "${BASE}/do_cmd.html" -d "${data}" >/dev/null
	curl -sf "${auth[@]}" "${BASE}/success.html" -d 'HF_PROCESS_CMD=RESTART' >/dev/null
	echo "OK: ${data%%&*}… → restart"
	sleep 25
}

echo "=== Logger ${HOST} ==="
curl -sf "${auth[@]}" "${BASE}/status.html" | grep -oE 'var (cover_ver|webdata_sn|cover_sta_ssid|cover_sta_ip)=[^;]*' || true

echo "--- working mode: Data collection ---"
post_restart 'yz_tmode=cmd'

echo "--- UART 9600 8N1 ---"
post_restart 'uart_setting_baud=9600&uart_setting_data=databit_8&uart_setting_parity=none&uart_setting_stop=stopbit_1&uart_setting_fc=NFC'

echo "--- internal TCP server :8899 ---"
post_restart 'net_setting_pro=TCP&net_setting_cs=SERVER&net_setting_port=8899&net_setting_to=300'

echo "--- optional: inv_tp (Deye) ---"
if [[ -n "${LOGGER_INV_TP:-}" ]]; then
	post_restart "inv_tp=${LOGGER_INV_TP}"
fi

echo "--- check port 8899 ---"
if timeout 3 bash -c "echo >/dev/tcp/${HOST}/8899" 2>/dev/null; then
	echo "8899: OPEN"
else
	echo "8899: CLOSED (прошивка M5434 — локальный TCP может быть отключён)"
fi

curl -sf "${auth[@]}" "${BASE}/status.html" | grep -oE 'var (status_a|status_b|webdata_now_p|webdata_pv_type)=[^;]*' || true
