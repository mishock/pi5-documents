# JK АКБ 4S 230Ah — BLE → Home Assistant (Pi 3 → Pi 5)

Обновлено: 2026-10-31 (дашборд на Pi3)

- BMS: JK-B2A8S20P, BLE-имя **AKB-4S-230**, MAC `C8:47:80:53:0F:B6`
- На Pi 3: `/home/pi/jk4s-ble/` (venv + `jk4s_bumble_probe.py` + `run_once.sh`)
- Снимок HA (Pi 5): `Проекты/Apple HomeKit accessory/home_assistant/config/host_status/jk4s.json`
- Дашборд: **JK АКБ 4S 230Ah** (`/jk-akb-4s-230/home`)
- Пакет: `…/config/packages/jk4s.yaml`

## Где смотреть

**Канон UI — HA на Pi 3** (`http://10.0.20.56:8123/jk-akb-4s-230/home`).
В боковой панели: **JK АКБ 4S 230Ah** (иконка батареи).
Пакет/дашборд: `~/Raspberry_Pi_3_HomePortable/ha_config/{packages,dashboards}/`.
Кнопка опроса локально: `jk4s-ha-poll-pi3.path` → `ha_poll_local.sh`.

Зеркало на Pi5 HA тоже есть, но основной — Pi3.

## Кнопка короткого опроса (рекомендуемый режим)

Периодический таймер **disabled** (Wi‑Fi в гараже не глушить; Cypress рвёт BLE).

1. В HA нажать **«Опросить батарею»** (`input_button.jk4s_poll`).
2. HA пишет `host_status/jk4s_poll.request`.
3. systemd `jk4s-ha-poll.path` → `jk4s_ha_poll.sh` (Pi 5) → SSH `sudo …/run_once.sh` на Pi 3.
4. После опроса BLE **обязательно отключается** (cleanup + `bluetoothctl disconnect`).
5. Статус: `sensor.jk4s_poll_state` / `sensor.jk4s_poll_status`.

Проверка на Pi 5:

```bash
systemctl status jk4s-ha-poll.path
date '+%s' > "…/host_status/jk4s_poll.request"
journalctl -u jk4s-ha-poll.service -f
cat "…/host_status/jk4s_poll_status.txt"
```

## Жёсткие правила

- Wi‑Fi в гараже **никогда** не отключать (`garage-wifi-never-off.mdc`).
- Не путать с ANT BMS24C — в гараже только JK AKB-4S-230.
- Кадр `0x02` на встроенном BT Pi 3 нестабилен (HCI -84 / disconnect 8); при неудаче прошлый снимок в HA сохраняется.
