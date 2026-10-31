# JK АКБ 4S 230Ah — BLE → Home Assistant (только Pi 3)

Обновлено: 2026-10-31

- BMS: JK-B2A8S20P, BLE-имя **AKB-4S-230**, MAC `C8:47:80:53:0F:B6`
- На Pi 3: `/home/pi/jk4s-ble/` (venv + `jk4s_bumble_probe.py` + `run_once.sh` / `ha_poll_local.sh`)
- **HA только на Pi 3** — на Pi 5 дашборда/пакета JK **нет** (убрано 2026-10-31)

## Где смотреть

`http://10.0.20.56:8123/jk-akb-4s-230/home`  
Боковая панель: **JK АКБ 4S 230Ah** (иконка батареи).

Файлы на Pi3: `~/Raspberry_Pi_3_HomePortable/ha_config/packages/jk4s.yaml`,  
`…/dashboards/jk-akb-4s-230.yaml`, снимок `…/host_status/jk4s.json`.

Эталон в репо (не для Pi5 HA): `bms-tools/ha-pi3-jk4s/`.

## Кнопка короткого опроса

Периодический таймер **disabled**.

1. В HA Pi3 нажать **«Опросить батарею»**.
2. `jk4s_poll.request` → `jk4s-ha-poll-pi3.path` → `ha_poll_local.sh`.
3. После опроса BLE **отключается**.
4. Статус: `sensor.jk4s_poll_state` / `sensor.jk4s_poll_status`.

```bash
systemctl status jk4s-ha-poll-pi3.path
journalctl -u jk4s-ha-poll-pi3.service -n 40
```

## Жёсткие правила

- Wi‑Fi в гараже **никогда** не отключать.
- Не путать с ANT BMS24C (тот на Pi5).
- Кадр `0x02` на встроенном BT Pi3 нестабилен; при ошибке прошлый снимок сохраняется.
