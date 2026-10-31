# JK АКБ 4S 230Ah — BLE logger (Pi 3)

Обновлено: 2026-10-31

- BMS: JK-B2A8S20P, BLE-имя **AKB-4S-230**, MAC `C8:47:80:53:0F:B6`
- Логгер: `jk4s_ble_logger.py` (на Pi 3: `/home/pi/jk4s-ble/`)
- Сервис: `jk4s-ble-logger.service`
- Снимок HA (Pi 5): `Проекты/Apple HomeKit accessory/home_assistant/config/host_status/jk4s.json`
- Дашборд: **JK АКБ 4S 230Ah** (`/jk-akb-4s-230/home`)

Проверка на Pi 3:

```bash
sudo systemctl status jk4s-ble-logger.service
tail -f /home/pi/jk4s-ble/logs/../ # journalctl -u jk4s-ble-logger -f
cat /home/pi/jk4s-ble/jk4s.json
```
