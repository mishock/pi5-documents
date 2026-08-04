#!/usr/bin/env bash
# Полное отключение автомониторинга бензина (таймеры + конфиг).
# Включение обратно только вручную: GDEBENZ_FUEL_ENABLE_TIMER=1 bash scripts/install-gdebenz-fuel-timer.sh
set -euo pipefail
PROJECT="/home/pi/Documents/Проекты/ai_assistant"
CFG="${PROJECT}/data/gdebenz-fuel.json"
PYTHON="${PROJECT}/venv/bin/python3"

systemctl --user disable --now gdebenz-fuel.timer gdebenz-qr-monitor.timer 2>/dev/null || true
systemctl --user stop gdebenz-fuel.service gdebenz-qr-monitor.service 2>/dev/null || true
systemctl --user daemon-reload

if [[ -f "$CFG" ]]; then
  "$PYTHON" - <<'PY'
import json
from pathlib import Path
p = Path("/home/pi/Documents/Проекты/ai_assistant/data/gdebenz-fuel.json")
cfg = json.loads(p.read_text(encoding="utf-8"))
cfg["monitoring_disabled"] = True
cfg["alert_email"] = ""
for chat in (cfg.get("chats") or {}).values():
    if isinstance(chat, dict):
        chat["enabled"] = False
        chat.pop("qr_pending", None)
p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK: monitoring_disabled=true, chats off, alert_email cleared")
PY
fi

echo "OK: gdebenz-fuel.timer и gdebenz-qr-monitor.timer отключены"
systemctl --user is-enabled gdebenz-fuel.timer gdebenz-qr-monitor.timer 2>&1 || true
