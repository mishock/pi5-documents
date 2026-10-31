#!/bin/bash
# Разовый опрос JK с HA Pi3 (кнопка). Обновлено: 2026-10-31
# После опроса BLE отключается. Wi‑Fi не глушить.
set -uo pipefail
HA_HS=/home/pi/Raspberry_Pi_3_HomePortable/ha_config/host_status
REQ=$HA_HS/jk4s_poll.request
STATUS=$HA_HS/jk4s_poll_status.txt
LOCK=/tmp/jk4s-ha-poll-pi3.lock
ATTEMPTS=${JK4S_ATTEMPTS:-3}

stamp(){ date '+%Y-%m-%d %H:%M:%S %z'; }
write_status(){ printf '%s\n' "$1|$2|$(stamp)" >"$STATUS"; }
cleanup(){ rmdir "$LOCK" 2>/dev/null || true; rm -f "$REQ" 2>/dev/null || true; }
force_ble_off(){
  pkill -9 -f jk4s_bumble_probe.py 2>/dev/null || true
  bluetoothctl disconnect C8:47:80:53:0F:B6 >/dev/null 2>&1 || true
}

if ! mkdir "$LOCK" 2>/dev/null; then
  write_status busy "уже идёт опрос"
  rm -f "$REQ" 2>/dev/null || true
  exit 0
fi
trap cleanup EXIT

write_status running "локальный опрос, попыток=$ATTEMPTS"
echo "[jk4s-ha-poll-pi3] start $(stamp)"

if ! sudo env JK4S_ATTEMPTS="$ATTEMPTS" /home/pi/jk4s-ble/run_once.sh; then
  force_ble_off
  write_status error "нет кадра 0x02; BLE отключён; прошлый снимок сохранён"
  exit 1
fi

cp -f /home/pi/jk4s-ble/jk4s.json "$HA_HS/jk4s.json"
# зеркало на Pi5 HA (если сеть есть)
/home/pi/jk4s-ble/publish_ha.sh >/dev/null 2>&1 || true
force_ble_off
online=$(python3 -c "import json;print(json.load(open('$HA_HS/jk4s.json')).get('online'))" 2>/dev/null || echo "?")
pack=$(python3 -c "import json;print(json.load(open('$HA_HS/jk4s.json')).get('pack_V'))" 2>/dev/null || echo "?")
write_status ok "online=$online pack_V=$pack; BLE отключён"
exit 0
