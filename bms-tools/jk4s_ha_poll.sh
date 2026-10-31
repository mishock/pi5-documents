#!/bin/bash
# Разовый опрос JK АКБ 4S с Pi5 (кнопка HA) → SSH Pi3 → Bumble → scp JSON.
# Обновлено: 2026-10-31
# После опроса BLE обязательно отключается (cleanup в run_once на Pi3).
# Wi‑Fi в гараже НЕ глушить. Таймер периодического опроса не трогать (disabled).
set -uo pipefail

HA_HOST_STATUS="/home/pi/Documents/Проекты/Apple HomeKit accessory/home_assistant/config/host_status"
REQ="${HA_HOST_STATUS}/jk4s_poll.request"
STATUS="${HA_HOST_STATUS}/jk4s_poll_status.txt"
LOCK="/tmp/jk4s-ha-poll.lock"
DEST_JSON="${HA_HOST_STATUS}/jk4s.json"
PI3_HOST="${JK4S_PI3_HOST:-pi3}"
ATTEMPTS="${JK4S_ATTEMPTS:-2}"
SSH_OPTS=(-o ConnectTimeout=12 -o BatchMode=yes -o StrictHostKeyChecking=accept-new)

stamp() { date '+%Y-%m-%d %H:%M:%S %z'; }

write_status() {
  local state="$1"
  local detail="${2:-}"
  printf '%s\n' "$state|$detail|$(stamp)" >"$STATUS"
}

cleanup_req() {
  rm -f "$REQ" 2>/dev/null || true
}

if ! mkdir "$LOCK" 2>/dev/null; then
  write_status "busy" "уже идёт опрос"
  cleanup_req
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null || true; cleanup_req' EXIT

write_status "running" "SSH ${PI3_HOST}, попыток=${ATTEMPTS}"
echo "[jk4s-ha-poll] start $(stamp) attempts=$ATTEMPTS host=$PI3_HOST"

# Короткий опрос на Pi3 от root (HCI USER /dev/vhci → EPERM без sudo).
# run_once сам рвёт BLE в trap cleanup + bluetoothctl disconnect.
REMOTE_CMD="sudo env JK4S_ATTEMPTS=${ATTEMPTS} /home/pi/jk4s-ble/run_once.sh"
force_ble_off() {
  ssh "${SSH_OPTS[@]}" "$PI3_HOST" \
    'pkill -9 -f jk4s_bumble_probe.py 2>/dev/null || true; bluetoothctl disconnect C8:47:80:53:0F:B6 >/dev/null 2>&1 || true; echo ble_off' \
    || true
}

if ! ssh "${SSH_OPTS[@]}" "$PI3_HOST" "$REMOTE_CMD"; then
  force_ble_off
  write_status "error" "нет кадра 0x02 (Cypress); BLE отключён; прошлый снимок сохранён"
  echo "[jk4s-ha-poll] probe failed; BLE forced off"
  exit 1
fi

# Забрать снимок на HA (Pi5).
if scp "${SSH_OPTS[@]}" \
  "${PI3_HOST}:/home/pi/jk4s-ble/jk4s.json" \
  "$DEST_JSON"; then
  force_ble_off
  online=$(python3 -c "import json;print(json.load(open('$DEST_JSON')).get('online'))" 2>/dev/null || echo "?")
  pack=$(python3 -c "import json;d=json.load(open('$DEST_JSON'));print(d.get('pack_V'))" 2>/dev/null || echo "?")
  write_status "ok" "online=${online} pack_V=${pack}; BLE отключён"
  echo "[jk4s-ha-poll] ok online=$online pack_V=$pack"
  exit 0
fi

force_ble_off
write_status "error" "scp jk4s.json failed; BLE отключён"
echo "[jk4s-ha-poll] scp failed"
exit 1
