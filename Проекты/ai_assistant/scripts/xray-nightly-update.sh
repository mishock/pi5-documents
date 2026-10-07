#!/usr/bin/env bash
# Ночное обновление Xray (VPS 3x-ui + клиент Pi 5) и двойная проверка.
# Лог: ~/logs/xray-nightly-update.log
set -euo pipefail

LOG="${HOME}/logs/xray-nightly-update.log"
mkdir -p "${HOME}/logs"
exec >>"$LOG" 2>&1

SOCKS="socks5h://127.0.0.1:10808"
HTTP_PROXY_LOCAL="http://127.0.0.1:10809"
VPS_IP="89.127.199.6"
XRAY_BIN="/usr/local/bin/xray"
XRAY_UNIT="xray.service"
PROXY_UNIT="cursor-proxy-http.service"
PI_UID=1000
PI_RUNTIME="/run/user/${PI_UID}"

log() { echo "[$(date -Is)] $*"; }

load_api_env() {
  if [[ -f "${HOME}/.config/xray-panel.env" ]]; then
    # shellcheck disable=SC1091
    source "${HOME}/.config/xray-panel.env"
  fi
  if [[ -z "${XUI_API_TOKEN:-}" && -f "${HOME}/Documents/vpn-guide.md" ]]; then
    XUI_API_TOKEN="$(grep -E '^\| API Token \|' "${HOME}/Documents/vpn-guide.md" | sed -n 's/.*`\([^`]*\)`.*/\1/p' | head -1)"
  fi
  XUI_API_BASE="${XUI_API_BASE:-https://89.127.199.6:37702/q6omE9HRd1U9d6t4XH}"
  if [[ -z "${XUI_API_TOKEN:-}" ]]; then
    log "ERROR: нет XUI_API_TOKEN (~/.config/xray-panel.env или vpn-guide.md)"
    exit 1
  fi
}

xui_post() {
  local path="$1"
  curl -sk --max-time 600 -X POST \
    -H "Authorization: Bearer ${XUI_API_TOKEN}" \
    -H "Content-Type: application/json" \
    "${XUI_API_BASE}${path}" \
    -d "${2:-{}}"
}

xui_get() {
  local path="$1"
  curl -sk --max-time 120 \
    -H "Authorization: Bearer ${XUI_API_TOKEN}" \
    "${XUI_API_BASE}${path}"
}

panel_xray_version() {
  xui_get "/panel/api/server/status" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(d.get('obj',{}).get('xray',{}).get('version',''))
"
}

panel_xray_state() {
  xui_get "/panel/api/server/status" | python3 -c "
import json,sys
d=json.load(sys.stdin)
x=d.get('obj',{}).get('xray',{})
print(x.get('state',''), x.get('errorMsg',''))
"
}

pick_target_version() {
  xui_get "/panel/api/server/getXrayVersion" | python3 -c "
import json,sys
d=json.load(sys.stdin)
arr=d.get('obj') or []
print(arr[0] if arr else 'latest')
"
}

update_vps_xray() {
  local cur target
  cur="$(panel_xray_version)"
  target="$(pick_target_version)"
  log "VPS Xray: текущая=${cur:-?} цель=${target:-latest}"
  if [[ -z "$target" ]]; then
    target="latest"
  fi
  local want="${target#v}"
  if [[ -n "$cur" && "$cur" == "$want" ]]; then
    log "VPS: уже на ${cur}, только restart"
    xui_post "/panel/api/server/restartXrayService" | head -c 500
    echo
    return 0
  fi
  log "VPS: installXray/${target} ..."
  xui_post "/panel/api/server/installXray/${target}" | head -c 800
  echo
  sleep 15
  for _ in $(seq 1 30); do
    read -r st err <<<"$(panel_xray_state)"
    if [[ "$st" == "running" && -z "$err" ]]; then
      log "VPS: xray running после install"
      return 0
    fi
    sleep 10
  done
  log "WARN: VPS xray не running после install (state=${st} err=${err})"
  return 1
}

update_pi5_xray_binary() {
  local tmp="/tmp/xray-linux-arm64-nightly"
  log "Pi5: обновление бинарника xray (teddysun/xray:latest)"
  docker image inspect teddysun/xray:latest >/dev/null 2>&1 || docker pull teddysun/xray:latest
  cid="$(docker create teddysun/xray:latest)"
  docker cp "${cid}:/usr/bin/xray" "$tmp"
  docker rm "$cid" >/dev/null
  chmod +x "$tmp"
  "$tmp" version | head -2 || { log "ERROR: новый бинарник не запускается"; return 1; }
  if [[ -x "$XRAY_BIN" ]]; then
    cp -a "$XRAY_BIN" "${XRAY_BIN}.bak.$(date +%Y%m%d%H%M%S)"
  fi
  sudo install -m 755 "$tmp" "$XRAY_BIN"
  rm -f "$tmp"
  sudo /usr/local/bin/fix-xray-config.sh
  sudo systemctl restart "$XRAY_UNIT"
  sleep 3
  log "Pi5: $(xray version | head -1)"
}

user_systemctl() {
  sudo -u pi env \
    XDG_RUNTIME_DIR="$PI_RUNTIME" \
    DBUS_SESSION_BUS_ADDRESS="unix:path=${PI_RUNTIME}/bus" \
    HOME="/home/pi" \
    systemctl --user "$@"
}

remediate() {
  log "REMEDIATE: fix config + restart xray/proxy + VPS restart"
  sudo /usr/local/bin/fix-xray-config.sh || true
  sudo systemctl restart "$XRAY_UNIT" || true
  sleep 2
  user_systemctl restart "$PROXY_UNIT" || true
  user_systemctl restart cursor-agent-mvp.service || true
  xui_post "/panel/api/server/restartXrayService" >/dev/null || true
  sleep 5
}

proxy_ok() {
  curl -sS --max-time 15 --proxy "$SOCKS" "https://api.ipify.org" | grep -q .
}

proxy_vps_ip() {
  local ip
  ip="$(curl -sS --max-time 15 --proxy "$SOCKS" "https://api.ipify.org" || true)"
  [[ "$ip" == "$VPS_IP" ]]
}

http_proxy_ok() {
  curl -sS --max-time 15 -x "$HTTP_PROXY_LOCAL" "https://api.ipify.org" | grep -q .
}

verify_once() {
  local tag="$1"
  local ok=0
  systemctl is-active --quiet "$XRAY_UNIT" || { log "FAIL[$tag] $XRAY_UNIT"; ok=1; }
  ss -ltn 2>/dev/null | grep -q '127.0.0.1:10808' || { log "FAIL[$tag] SOCKS 10808"; ok=1; }
  proxy_ok || { log "FAIL[$tag] SOCKS ipify"; ok=1; }
  proxy_vps_ip || { log "FAIL[$tag] SOCKS IP != VPS"; ok=1; }
  user_systemctl is-active --quiet "$PROXY_UNIT" || { log "FAIL[$tag] $PROXY_UNIT"; ok=1; }
  http_proxy_ok || { log "WARN[$tag] HTTP proxy 10809 (не критично)"; }
  read -r st err <<<"$(panel_xray_state)"
  [[ "$st" == "running" && -z "$err" ]] || { log "FAIL[$tag] VPS xray state=${st} err=${err}"; ok=1; }
  log "VERIFY[$tag] Pi5=$(xray version 2>/dev/null | head -1) VPS=$(panel_xray_version) SOCKS_IP=$(curl -sS --max-time 10 --proxy "$SOCKS" https://api.ipify.org 2>/dev/null || echo '?')"
  return "$ok"
}

notify_fail() {
  if command -v "${HOME}/bin/jarvis-need-user.sh" >/dev/null 2>&1; then
    "${HOME}/bin/jarvis-need-user.sh" "Xray nightly update FAIL" "См. ${LOG}" || true
  fi
}

main() {
  log "========== xray-nightly-update START =========="
  load_api_env
  set +e
  update_vps_xray
  vps_rc=$?
  set -e
  update_pi5_xray_binary

  if ! verify_once "pass1"; then
    remediate
    verify_once "pass1-retry" || true
  fi
  sleep 45
  if ! verify_once "pass2"; then
    remediate
    if ! verify_once "pass2-retry"; then
      log "ERROR: проверка не прошла после remediate"
      notify_fail
      exit 1
    fi
  fi
  log "========== xray-nightly-update OK =========="
}

main "$@"
