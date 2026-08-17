# ANT BMS-ANT24C — локальный лог

Опрос Classic SPP (`AA:BB:CC:91:23:45`) каждые **5 мин**.

- CSV: `logs/ant24c.csv`
- События циклов: `logs/ant24c_cycles.jsonl` (`charge_cut` / `discharge_cut` + пик/пол напряжения)
- Снимок для HA: `Проекты/Apple HomeKit accessory/home_assistant/config/host_status/ant24c.json`

Сервисы: `ant24c-rfcomm.service`, `ant24c-logger.service`.

Home Assistant: отдельный дашборд **ANT BMS24C** в боковом меню (`/ant-bms-24c/home`).

Управление MOSFET / балансиром: HA пишет `host_status/ant24c_cmd.json`, логгер (единственный владелец `/dev/rfcomm0`) шлёт legacy `A5 A5` (пароль F1–F4, заряд FA, разряд F9, балансир FC, apply FF).
