#!/bin/bash
# Инвертор «Зарядка» 10.1.30.81 — обход XKeen (Guest Policy0): трафик logger напрямую в ISP.
# Правка /opt/etc/xray/configs/05_routing.json на офисном Keenetic (Entware, SSH :222).
set -euo pipefail

INV_IP="${ZARYADKA_IP:-10.1.30.81}"
ROUTER="${KEENETIC_OFFICE_ENTWARE:-192.168.1.1}"
SSH_PORT="${KEENETIC_ENTWARE_SSH:-222}"
SSH_PASS="${KEENETIC_ENTWARE_PASS:-keenetic}"
ROUTING="/opt/etc/xray/configs/05_routing.json"

ssh_entware() {
	sshpass -p "${SSH_PASS}" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=12 \
		-p "${SSH_PORT}" "root@${ROUTER}" "$@"
}

if ! ssh_entware "test -f '${ROUTING}'"; then
	echo "ERROR: ${ROUTING} не найден на ${ROUTER}" >&2
	exit 1
fi

if ssh_entware "grep -q '${INV_IP}/32' '${ROUTING}'"; then
	echo "OK: bypass ${INV_IP} уже в ${ROUTING}"
else
	echo ">> backup + добавить source ${INV_IP}/32 → direct"
	ssh_entware "cp '${ROUTING}' '${ROUTING}.bak-zaryadka-\$(date +%Y%m%d-%H%M%S)'"
	ssh_entware "python3 - <<'PY'
import json
p='${ROUTING}'
ip='${INV_IP}/32'
with open(p) as f: cfg=json.load(f)
rules=cfg.setdefault('routing',{}).setdefault('rules',[])
if not any(r.get('source')==[ip] for r in rules):
    # после private/direct ip, перед catch-all vless
    ins=1
    for i,r in enumerate(rules):
        if r.get('outboundTag')=='vless-reality' and 'source' not in r and 'ip' not in r:
            ins=i; break
    rules.insert(ins, {'type':'field','source':[ip],'outboundTag':'direct'})
with open(p,'w') as f: json.dump(cfg,f,indent=2)
print('updated', p)
PY"
fi

echo ">> xkeen -restart"
timeout 30 ssh_entware "xkeen -restart" | tail -3
echo "Готово: ${INV_IP} → direct (минуя VLESS)."
