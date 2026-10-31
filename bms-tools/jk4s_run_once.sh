#!/bin/bash
# Разовый опрос JK АКБ 4S через Bumble. Обновлено: 2026-10-31
set -uo pipefail
VENV=/home/pi/jk4s-ble/.venv
PROBE=/home/pi/jk4s-ble/jk4s_bumble_probe.py
OUT=/home/pi/jk4s-ble/jk4s.json
MAC=C8:47:80:53:0F:B6

OLD_TX=""
MASKED=0
if command -v iwconfig >/dev/null; then
  OLD_TX=$(iwconfig wlan0 2>/dev/null | awk -F'=' '/Tx-Power/{print $2}' | awk '{print $1}')
  iwconfig wlan0 txpower 8 2>/dev/null || true
fi

cleanup() {
  pkill -9 -f jk4s_bumble_probe.py 2>/dev/null || true
  hciconfig hci0 down 2>/dev/null || true
  if [[ "$MASKED" -eq 1 ]]; then
    systemctl unmask bluetooth 2>/dev/null || true
  fi
  systemctl start bluetooth 2>/dev/null || true
  sleep 1
  bluetoothctl power on >/dev/null 2>&1 || true
  if [[ -n "${OLD_TX:-}" ]]; then
    iwconfig wlan0 txpower "$OLD_TX" 2>/dev/null || iwconfig wlan0 txpower 31 2>/dev/null || true
  else
    iwconfig wlan0 txpower 31 2>/dev/null || true
  fi
}
trap cleanup EXIT

echo "stop+mask bluetoothd…"
systemctl stop bluetooth 2>/dev/null || true
systemctl mask bluetooth 2>/dev/null && MASKED=1 || true
killall -9 bluetoothd btmon 2>/dev/null || true
pkill -9 -f jk4s_bumble_probe.py 2>/dev/null || true
sleep 2
hciconfig hci0 down 2>/dev/null || true
rfkill unblock bluetooth 2>/dev/null || true
sleep 1

echo "probe…"
"$VENV/bin/python" "$PROBE" "$MAC" -n 5 -o "$OUT"
RC=$?
echo "probe rc=$RC"
if [[ $RC -eq 0 ]]; then
  cp -f "$OUT" /home/pi/Raspberry_Pi_3_HomePortable/ha_config/host_status/jk4s.json
  scp -o ConnectTimeout=8 -o BatchMode=yes "$OUT" \
    "pi@100.102.159.200:/home/pi/Documents/Проекты/Apple HomeKit accessory/home_assistant/config/host_status/jk4s.json" || true
  head -50 "$OUT"
fi
exit $RC
