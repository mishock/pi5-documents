#!/usr/bin/env bash
# Белый список IP агента (Pi 5 / NetBird) на Keenetic office + electro.
# Разрешает Джарвису доступ ко всем сегментам без isolate-private блокировок.
#
# IP агента:
#   10.1.30.126  — Pi 5 (ELEKTRO_, статический DHCP)
#   100.102.159.200 — NetBird Pi 5
#
# Usage: bash Документы/.cursor/scripts/install-jarvis-agent-router-access.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
KEEN="${ROOT}/.cursor/scripts/keenetic-ssh.sh"
AGENT_IP="${JARVIS_AGENT_IP:-10.1.30.126}"
AGENT_NB="${JARVIS_AGENT_NETBIRD:-100.102.159.200}"
GW_ELECTRO="${JARVIS_ELECTRO_GW:-10.1.30.1}"
# Устройства только в Guest офиса (ELTAVR_), не в ELEKTRO_
OFFICE_GUEST_HOSTS="${JARVIS_OFFICE_GUEST_HOSTS:-10.1.30.81}"

run() {
	local router="$1"
	shift
	local cmd="$*"
	echo ">> ${router}: ${cmd}"
	env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY bash "${KEEN}" "${router}" "${cmd}" 2>&1 \
		| grep -v '^\[K' | grep -v '^$' || true
}

save() {
	local router="$1"
	shift
	env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY bash "${KEEN}" "${router}" save "$*" 2>&1 \
		| grep -v '^\[K' | tail -1 || true
}

ensure_acl_rule() {
	local router="$1"
	local list="$2"
	local rule="$3"
	# Keenetic сохраняет маски как 255.255.255.255, не /32
	local ip_part="${rule#permit ip }"
	ip_part="${ip_part#permit tcp }"
	ip_part="${ip_part#permit icmp }"
	local src="${ip_part%%/*}"
	if env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY bash "${KEEN}" "${router}" 'show running-config' 2>/dev/null \
		| grep -A30 "access-list ${list}" | grep -Fq "${src}"; then
		echo "OK ${router} ${list}: ${rule}"
	else
		run "${router}" "access-list ${list} ${rule}"
	fi
}

ensure_access_group() {
	local router="$1"
	local iface="$2"
	local dir="$3"
	local list="$4"
	local needle="ip access-group ${list} ${dir}"
	if env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY bash "${KEEN}" "${router}" 'show running-config' 2>/dev/null \
		| grep -Fq "${needle}"; then
		echo "OK ${router} ${iface} ${dir} ${list}"
	else
		run "${router}" "interface ${iface} ip access-group ${list} ${dir}"
	fi
}

setup_jarvis_acl() {
	local router="$1"
	shift
	local -a ifaces=("$@")
	ensure_acl_rule "${router}" jarvis-agent "permit ip ${AGENT_IP}/32 0.0.0.0/0"
	ensure_acl_rule "${router}" jarvis-agent "permit tcp ${AGENT_IP}/32 0.0.0.0/0"
	ensure_acl_rule "${router}" jarvis-agent "permit ip ${AGENT_NB}/32 0.0.0.0/0"
	ensure_acl_rule "${router}" jarvis-agent "permit icmp ${AGENT_IP}/32 0.0.0.0/0"
	ensure_acl_rule "${router}" jarvis-agent "permit icmp ${AGENT_NB}/32 0.0.0.0/0"
	ensure_acl_rule "${router}" jarvis-agent "permit ip ${AGENT_IP}/32 10.1.30.0/24"
	ensure_acl_rule "${router}" jarvis-agent "permit ip ${AGENT_NB}/32 10.1.30.0/24"
	ensure_acl_rule "${router}" jarvis-agent "permit ip ${AGENT_IP}/32 192.168.1.0/24"
	for iface in "${ifaces[@]}"; do
		ensure_access_group "${router}" "${iface}" in jarvis-agent
		ensure_access_group "${router}" "${iface}" out jarvis-agent
	done
}

echo "=== jarvis-agent ACL: office ==="
setup_jarvis_acl office Bridge0 Bridge1 Home ISP

echo "=== office: no isolate-private (ACL не обходит isolate-private) ==="
if env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY bash "${KEEN}" office 'show running-config' 2>/dev/null | grep -q '^isolate-private'; then
	save office 'no isolate-private'
else
	echo "OK office: isolate-private уже выключен"
fi

echo "=== office: guest-isolation (Guest → Home блок, кроме интернета) ==="
ensure_acl_rule office guest-isolation "deny ip 0.0.0.0/0 192.168.1.0/24"
ensure_acl_rule office guest-isolation "deny ip 0.0.0.0/0 10.10.0.0/24"
ensure_acl_rule office guest-isolation "permit ip 0.0.0.0/0 0.0.0.0/0"
ensure_access_group office Bridge1 out guest-isolation

echo "=== office: Pi MAC permit ==="
save office "ip hotspot host 2c:cf:67:78:b4:55 permit"

echo "=== jarvis-agent ACL: electro ==="
setup_jarvis_acl electro Bridge0 Bridge1 Bridge2 ISP

for host in ${OFFICE_GUEST_HOSTS}; do
	rule="ip route ${host} 192.168.1.1 ISP"
	if env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY bash "${KEEN}" electro 'show running-config' 2>/dev/null | grep -Fq "${rule}"; then
		echo "OK electro: ${rule}"
	else
		save electro "${rule}"
	fi
done

echo "=== Pi 5: host-маршруты к офисному Guest (перекрытие 10.1.30.0/24) ==="
ROUTE_DIR="/etc/jarvis-agent-routes"
sudo mkdir -p "${ROUTE_DIR}"
sudo tee "${ROUTE_DIR}/office-guest.conf" >/dev/null <<EOF
# Джарвис: устройства только на офисном Guest (не в ELEKTRO_)
${OFFICE_GUEST_HOSTS}
EOF
sudo tee /etc/systemd/system/jarvis-agent-routes.service >/dev/null <<EOF
[Unit]
Description=Jarvis agent host routes (office Guest overlap)
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
Environment=GW=${GW_ELECTRO}
EnvironmentFile=-${ROUTE_DIR}/office-guest.conf
ExecStart=/bin/bash -c 'while read -r ip; do [[ "\$ip" =~ ^# ]] && continue; [[ -z "\$ip" ]] && continue; ip route replace "\$ip/32" via "\$GW" dev wlan0 2>/dev/null || true; done < ${ROUTE_DIR}/office-guest.conf'

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now jarvis-agent-routes.service

echo "=== Проверка ==="
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY ping -c 1 -W 3 192.168.1.1 >/dev/null && echo "office 192.168.1.1: OK" || echo "office 192.168.1.1: FAIL"
for host in ${OFFICE_GUEST_HOSTS}; do
	if env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY ping -c 1 -W 4 "${host}" >/dev/null 2>&1; then
		echo "office guest ${host}: OK"
	else
		echo "office guest ${host}: FAIL (ping)"
	fi
done
echo "Готово. ACL: jarvis-agent + guest-isolation на office; jarvis-agent на electro."
