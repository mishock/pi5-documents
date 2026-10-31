#!/bin/bash
# Периодический опрос JK АКБ 4S через Bumble HCI USER → JSON для HA.
# Обновлено: 2026-10-31
set -euo pipefail

BASE="${JK4S_BASE:-/home/pi/jk4s-ble}"
VENV="${JK4S_VENV:-$BASE/.venv}"
PY="$VENV/bin/python"
PROBE="${JK4S_PROBE:-$BASE/jk4s_bumble_probe.py}"
MAC="${JK4S_MAC:-C8:47:80:53:0F:B6}"
INTERVAL="${JK4S_INTERVAL:-60}"
OUT_LOCAL="${JK4S_HA_JSON:-$BASE/jk4s.json}"
OUT_PI3_HA="${JK4S_HA_JSON_REMOTE:-/home/pi/Raspberry_Pi_3_HomePortable/ha_config/host_status/jk4s.json}"
SCP_TARGET="${JK4S_SCP_TARGET:-pi@100.102.159.200:/home/pi/Documents/Проекты/Apple HomeKit accessory/home_assistant/config/host_status/jk4s.json}"
STATE="$BASE/jk4s_state.json"
ATTEMPTS="${JK4S_ATTEMPTS:-5}"

mkdir -p "$BASE/logs" "$(dirname "$OUT_LOCAL")" "$(dirname "$OUT_PI3_HA")"

log() { echo "$(date '+%Y-%m-%dT%H:%M:%S%z') $*"; }

prepare_hci() {
  systemctl stop bluetooth 2>/dev/null || true
  killall bluetoothd btmon 2>/dev/null || true
  sleep 0.5
  hciconfig hci0 down 2>/dev/null || true
  sleep 0.5
  rfkill unblock bluetooth 2>/dev/null || true
}

restore_bt() {
  hciconfig hci0 down 2>/dev/null || true
  sleep 0.3
  systemctl start bluetooth 2>/dev/null || true
  sleep 1
  bluetoothctl power on >/dev/null 2>&1 || true
}

update_extrema() {
  # лёгкий extrema через python
  "$PY" - "$OUT_LOCAL" "$STATE" <<'PY'
import json, sys
from pathlib import Path
snap_path, state_path = Path(sys.argv[1]), Path(sys.argv[2])
try:
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
except Exception:
    raise SystemExit(0)
state = {}
if state_path.exists():
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        state = {}
v = snap.get("pack_V")
mode = snap.get("mode") or "idle"
if isinstance(v, (int, float)):
    if state.get("pack_v_min") is None or v < state["pack_v_min"]:
        state["pack_v_min"] = v
    if state.get("pack_v_max") is None or v > state["pack_v_max"]:
        state["pack_v_max"] = v
prev = state.get("prev_mode")
if prev == "charge" and mode != "charge" and isinstance(v, (int, float)):
    state["last_charge_peak_V"] = v
if prev == "discharge" and mode != "discharge" and isinstance(v, (int, float)):
    state["last_discharge_floor_V"] = v
state["prev_mode"] = mode
snap["pack_v_min"] = state.get("pack_v_min")
snap["pack_v_max"] = state.get("pack_v_max")
snap["last_charge_peak_V"] = state.get("last_charge_peak_V")
snap["last_discharge_floor_V"] = state.get("last_discharge_floor_V")
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
snap_path.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
PY
}

publish_copies() {
  cp -f "$OUT_LOCAL" "$OUT_PI3_HA" 2>/dev/null || true
  if [[ -n "$SCP_TARGET" ]]; then
    scp -o ConnectTimeout=8 -o BatchMode=yes "$OUT_LOCAL" "$SCP_TARGET" >/dev/null 2>&1 || true
  fi
}

log "jk4s bumble logger start mac=$MAC interval=${INTERVAL}s"
while true; do
  prepare_hci
  set +e
  "$PY" "$PROBE" "$MAC" -n "$ATTEMPTS" -o "$OUT_LOCAL" 2>"$BASE/logs/probe.err"
  rc=$?
  set -e
  restore_bt
  if [[ $rc -eq 0 && -s "$OUT_LOCAL" ]]; then
    update_extrema
    publish_copies
    log "OK $(python3 -c "import json;d=json.load(open('$OUT_LOCAL'));print(d.get('pack_V'),'V',d.get('soc'),'%','mode',d.get('mode'))" 2>/dev/null || echo ok)"
  else
    log "FAIL rc=$rc $(tail -c 200 "$BASE/logs/probe.err" 2>/dev/null | tr '\n' ' ')"
    # при ошибке не затираем last-good числа — только online/error если файл битый
  fi
  sleep "$INTERVAL"
done
