#!/usr/bin/env bash
# С Pi 5: упаковать credentials + скрипт и положить на Pi 3 для скачивания с ПК Артёма.
#   bash Проекты/artem-cursor-agent/scripts/deploy-via-pi3.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${PI3_SSH_HOST:-pi3}"
REMOTE_DIR="/home/pi/artem-cursor-agent"
PKG="/tmp/artem-cursor-agent-bundle.tar.gz"

echo "==> Сборка пакета..."
tar -czf "$PKG" \
  -C "$ROOT" \
  scripts/install-cursor-agent-windows.ps1 \
  credentials/artem_ed25519 \
  credentials/artem_ed25519.pub \
  credentials/cursor-api-key.txt \
  README.md 2>/dev/null || tar -czf "$PKG" -C "$ROOT" scripts credentials README.md

echo "==> Деплой на ${HOST}:${REMOTE_DIR}..."
ssh -o BatchMode=yes -o ConnectTimeout=20 "$HOST" "mkdir -p '$REMOTE_DIR'"
scp -o BatchMode=yes "$PKG" "${HOST}:${REMOTE_DIR}/bundle.tar.gz"
scp -o BatchMode=yes "$ROOT/scripts/install-cursor-agent-windows.ps1" "${HOST}:${REMOTE_DIR}/"

ssh -o BatchMode=yes "$HOST" "cd '$REMOTE_DIR' && tar -xzf bundle.tar.gz && chmod 700 credentials && chmod 600 credentials/* && ls -la"

echo ""
echo "OK. На ПК Артёма (PowerShell, NetBird Connected):"
echo "  scp -r pi@100.102.186.61:~/artem-cursor-agent %USERPROFILE%\\Downloads\\artem-cursor-agent"
echo "  cd %USERPROFILE%\\Downloads\\artem-cursor-agent"
echo "  powershell -ExecutionPolicy Bypass -File install-cursor-agent-windows.ps1"
