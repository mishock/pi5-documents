#!/usr/bin/env bash
# Добавить SSH-ключ Артёма на все малинки mesh.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PUB="$ROOT/credentials/artem_ed25519.pub"
[[ -f "$PUB" ]] || { echo "Нет $PUB — сначала generate или ssh-keygen" >&2; exit 1; }
PUBLINE="$(cat "$PUB")"
MARKER="artem-shpak-cursor-agent"

add_key() {
  local host="$1" user="${2:-pi}"
  ssh -o BatchMode=yes -o ConnectTimeout=15 "${user}@${host}" "
    grep -qF '$MARKER' ~/.ssh/authorized_keys 2>/dev/null || echo '$PUBLINE' >> ~/.ssh/authorized_keys
    chmod 600 ~/.ssh/authorized_keys
    echo OK $host
  " 2>/dev/null || echo "SKIP $host"
}

add_key pi3 pi
add_key 127.0.0.1 pi   # Pi 5 local
# Kali — домашняя LAN (через Pi 3)
PUBLINE="$(cat "$PUB")"
ssh -o BatchMode=yes pi3 "ssh -o BatchMode=yes -o ConnectTimeout=8 kali@10.0.20.42 \"grep -qF '$MARKER' ~/.ssh/authorized_keys 2>/dev/null || echo '$PUBLINE' >> ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys; echo OK kali-lan\"" 2>/dev/null || echo "SKIP kali (offline)"

echo "Готово."
