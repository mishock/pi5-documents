#!/bin/bash
# Разовый опрос JK АКБ 4S (AKB-4S-230) через Bumble.
# Обновлено: 2026-10-31
# ЖЁСТКО: Wi‑Fi НЕ отключать (гараж = основной интернет). Только txpower↓.
set -uo pipefail
VENV=/home/pi/jk4s-ble/.venv
PROBE=/home/pi/jk4s-ble/jk4s_bumble_probe.py
OUT=/home/pi/jk4s-ble/jk4s.json
MAC=C8:47:80:53:0F:B6
ATTEMPTS="${JK4S_ATTEMPTS:-3}"

OLD_TX=""
MASKED=0
if command -v iwconfig >/dev/null; then
  OLD_TX=$(iwconfig wlan0 2>/dev/null | awk -F'=' '/Tx-Power/{print $2}' | awk '{print $1}')
  iwconfig wlan0 txpower 5 2>/dev/null || true
fi

cleanup() {
  # ЖЁСТКО: после опроса BLE от батареи отключить
  pkill -9 -f jk4s_bumble_probe.py 2>/dev/null || true
  hciconfig hci0 down 2>/dev/null || true
  if [[ "$MASKED" -eq 1 ]]; then
    systemctl unmask bluetooth 2>/dev/null || true
  fi
  systemctl start bluetooth 2>/dev/null || true
  sleep 1
  bluetoothctl power on >/dev/null 2>&1 || true
  bluetoothctl disconnect "$MAC" >/dev/null 2>&1 || true
  if [[ -n "${OLD_TX:-}" ]]; then
    iwconfig wlan0 txpower "$OLD_TX" 2>/dev/null || iwconfig wlan0 txpower 31 2>/dev/null || true
  else
    iwconfig wlan0 txpower 31 2>/dev/null || true
  fi
  # Wi‑Fi radio всегда on
  nmcli radio wifi on 2>/dev/null || true
}
trap cleanup EXIT

echo "stop bluetoothd (Wi‑Fi stays ON)…"
systemctl stop bluetooth 2>/dev/null || true
systemctl mask bluetooth 2>/dev/null && MASKED=1 || true
killall -9 bluetoothd btmon 2>/dev/null || true
pkill -9 -f jk4s_bumble_probe.py 2>/dev/null || true
sleep 1
hciconfig hci0 down 2>/dev/null || true
rfkill unblock bluetooth 2>/dev/null || true
rfkill unblock wifi 2>/dev/null || true
sleep 0.5

echo "probe attempts=$ATTEMPTS…"
"$VENV/bin/python" "$PROBE" "$MAC" -n "$ATTEMPTS" -o "$OUT"
RC=$?
echo "probe rc=$RC"
if [[ $RC -eq 0 ]]; then
  cp -f "$OUT" /home/pi/Raspberry_Pi_3_HomePortable/ha_config/host_status/jk4s.json 2>/dev/null || true
  head -40 "$OUT"
fi
exit $RC
