# Handoff (кратко)

## Текущий фокус

- **Режим QR LiFePO4 (2026-08-07):** кидать код/фото → макс. поля; `Платы и модули/LiFePO4_Cell_QR_Decoder/scripts/decode_cell_qr.py`.

- **LiFePO4 QR (2026-08-07):** `Платы и модули/LiFePO4_Cell_QR_Decoder/` — декодеры Gobel/Hakadi/Xiho; пример `04QCB72…` = EVE LF230 230Ач 15.12.2025.

- **Kali БК 5″ (2026-08-07):** **запущен** — `ui/bc.py` в tmux `bc`; KKL `/dev/vag-kkl`→ttyUSB0. Старт: `start_bc.sh`.

- **Kali приборка LIVE (2026-08-07):** `ui/dashboard.py` + K-line `obd_feed`; старт `scripts/start_dashboard.sh`; нужен KKL `/dev/vag-kkl` + зажигание ON.

- **Kali приборка DEMO 5″ (2026-08-07):** `~/Projects/cluster_pi/ui/dashboard_demo.py` — тест на HDMI 800×480; старт `scripts/start_dashboard_demo.sh`.

- **SILA VM II Premium+ 6.2K (2026-08-06):** `Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/` — VP-MH-PLUS/Axpert OEM; RU только `РУКОВОДСТВО_RU.md`; EN в downloads.

- **Deye 6.6K (2026-08-06):** только SUN-6.6K-OG03LP1-EU-AM2; обязательный RU — `РУКОВОДСТВО_RU.md`; чужие инструкции удалены.

- **Deye SUN-6.6K-OG03LP1-EU-AM2 (2026-08-06):** модель пользователя; `Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/` — 6.6 кВт, АКБ 40–60 В, заряд/разряд 140 А, 2×MPPT, DC 200 А.

- **EZGO ошибки (2026-08-06):** шпаргалка `Платы и модули/Электрокары/EZGO_Club_Car/FAULT_CODES.md` (мигания LED ST Shuttle); extract — `notes/FAULT_CODES_EXTRACT.md`.
- **EZGO схемы (2026-08-06):** `Электрокары/EZGO_Club_Car/` — SM 612342 + Parts 620365 + ST400 614281; схемы в PDF — `WIRING_REFERENCE.md` (PNG-превью не храним; Owner 605693 удалён).
- **GEM ошибки (2026-08-06):** шпаргалка `Платы и модули/Электрокары/Polaris_GEM_e6_2017/FAULT_CODES.md`; полный DTC — `notes/DTC_FULL_TABLE.md`.
- **Солнечные инверторы (2026-08-06):** общая папка `Платы и модули/Солнечные_инверторы/` — MUST / Deye / Adion / сводка токов; новые модели — подпапки туда же (`README.md`).
- **Электрокары (2026-08-06):** общая папка `Платы и модули/Электрокары/` — GEM + E-Z-GO; новые модели (Club Car…) — подпапки туда же (`README.md`).
- **EZGO / Club Car:** `Платы и модули/Электрокары/EZGO_Club_Car/` — ST Shuttle 4/6 E SM 612342; Club Car пока пусто.
- **GEM e6 распиновка:** `Платы и модули/Электрокары/Polaris_GEM_e6_2017/WIRING_REFERENCE.md`.
- **GEM мануалы (постоянно):** https://brandfolder.com/waev/service-support (Waev Service & Support). Эталон e6 2017: `Платы и модули/Электрокары/Polaris_GEM_e6_2017/` (SM **9940314 R02**). Другая модель GEM → Brandfolder + новая подпапка в `Электрокары/`.
- **Deye OG03 (2026-08-06):** `Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/` — EN manual OG03; RU официальной нет; RU SolarCrown SG01 в downloads.

- **Бензин (2026-08-04):** автопоиск/мониторинг/почта/Telegram — **отключены**. Таймеры gdebenz disabled; `monitoring_disabled: true`. Разовая `/gdebenz` ок; `/gdebenz on` не включает авто.

- **Pi5 HA CPU temp (2026-08-04):** график залипал из-за cron с пробелами; теперь systemd timer `pi5-ha-cpu-temp.timer`. Проверка: обновить дашборд Pi 5.

- **HA Sites (2026-08-04):** `/auth/*` проксируется в HA; Not Found на вкладке исправлен. Проверка: обновить Home Assistant в PWA.

- **EDM (2026-08-04):** `edm-web` снова active после reboot. Удалён вредный `home-pi-Documents.mount` (ordering cycle). Проверка: `systemctl is-active edm-web`; `curl http://127.0.0.1:8080/`; PWA Сайты → EDM.


- **Инструкции Эльтавр (2026-08-03):** локально `Инструкции Эльтавр/` (PDF+HTML). Drive — после reauth google-mcp.
- **Инструкция монитор Эльтавр (2026-08-03):** PDF+HTML на почту mishock24@gmail.com. Drive upload ждёт reauth google-mcp (invalid_grant).
- **VPN Apple TV (2026-08-01):** в 3x-ui клиент `appletv` (inbound `vless-reality`). Подписка: `https://89.127.199.6:2096/sub/5101960c-1fb4-4c31-b125-fff1e6e29a6b`. Клиент на ТВ: Happ. См. `vpn-guide.md`.

- **Documents / Remote Control (2026-07-29):** канон `/home/pi/Documents`; `/home/pi/Документы` — симлинк. Remote Control worker `total=1`. Проверка: `bash ~/bin/mount-pi5-documents.sh && systemctl --user is-active ai-assistant-telegram cursor-self-hosted-worker`.

- **Pi 3 гараж (2026-07-28 21:03):** online, `ssh pi3`, NetBird `100.102.186.61`, LAN `10.0.20.56`.

- **Начальник:** Владимир Шуликов → `vladimirshulikov2@gmail.com` (правило `.cursor/rules/boss-shulikov.mdc`). «Отправь начальнику» = ему.

- **MUST PH1100 12кВт (2026-07-29):** модель **PH11-12KL3-EU**. Папка: `Платы и модули/Солнечные_инверторы/Must_PH1100_12kW/`. Основная инструкция — русский PDF `downloads/MUST_PH1100_PH11-12KL3-EU_Руководство_RU.pdf` (EN в archive). АКБ 2×230Ач параллель (460Ач), 2×ANT 170А; к MUST 1×50/70; C63×2.


- **Kali 5″ HDMI (2026-07-27):** Pi Zero 2 W — 800×480 + XPT2046 OK (fb 800x480, ADS7846, lightdm). Доки: `Платы и модули/HDMI_5inch_800x480_XPT2046/`.

## Быстрые проверки

- `ssh -J pi3 kali@10.0.20.42 'cat /sys/class/graphics/fb0/virtual_size; grep . /sys/class/input/input*/name; systemctl is-active lightdm'`
- Калибровка тача: `xinput_calibrator` / `swapxy` в dtoverlay

## Ранее

# Handoff (кратко)

## Текущий фокус

- **Начальник:** Владимир Шуликов → `vladimirshulikov2@gmail.com` (правило `.cursor/rules/boss-shulikov.mdc`). «Отправь начальнику» = ему.

- **MUST PV18-4024 PRO II (2026-07-25):** Modbus USB `/dev/ttyUSB0` 19200 slave 4. **Новый инвертор:** `must-apply-working.sh` → verify **20/20 OK**. LCD-only — вручную (`WORKING_PROFILE.md`). RTC по USB не выставляется — WatchPower с ПК.

## Быстрые проверки

- USB: `lsusb | grep 303a:1001` → `/dev/ttyACM0`
- Пересборка/заливка: `PIO_ENV=esp32-c6-touch-lcd bash …/scripts/{build,flash}.sh`
- BMS: TX→GPIO7, RX←GPIO6, 3.3 V, 19200

## Ранее

- **ANT BMS web v2.5.4 (2026-07-09):** runtime-парсер расширен под `--297D...`/`+...`; разбор событий стабилен для таких логов.
- **ANT BMS web v2.5.1 (2026-07-09):** графики получили понятные оси и min/max-статистику по каждому ряду; время теперь явно видно на горизонтальной шкале.
- **ANT BMS web v2.5.0 (2026-07-09):** в веб-конфигураторе реализована визуализация SystemLog из файла (upload + графики в UI), endpoint `/api/systemlog/analyze` работает на реальном логе.
- **ANT BMS visual analytics (2026-07-09):** добавлен скрипт `Проекты/Arduino/firmware/ANT_BMS/scripts/visualize_system_log.py`; для `SystemLog_20260709_122623.txt` сгенерированы графики и `events.csv` в `Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/`.
- **ANT BMS web v2.4.9 (2026-07-09):** scan добирает имена устройств через bluetoothctl fallback; в списке должны появляться имена как в телефоне.
- **ANT BMS web v2.4.8 (2026-07-09):** исправлено имя устройств в scan-листе: Alias=MAC больше не считается именем, добавлены понятные подписи для безымянных BLE устройств.
- **ANT BMS log review (2026-07-09):** в `Проекты/Arduino/firmware/ANT_BMS/SystemLog_20260709_122623.txt` выявлены серии UV/дисбаланса (ячейки 12/14/15), частые `CHGOverCurWarning` до ~130A и MOS термокачание `79–80°C` (`Protect/Recover`); часть записей дублируется и содержит нулевые поля (`TotalV/MinUnitV=0`), учитывать как возможный шум логгера.

- **ANT BMS web v2.4.7 (2026-07-09):** scan показывает весь BLE-эфир (убран фильтр по `ANT`/MAC), обновлены тексты списка устройств, версии app `2.4.7`, cache `v12`.

- **ANT BMS web v2.4.6 (2026-07-09):** улучшен дизайн ячеек на «Состоянии», русифицированы типовые ошибки/защиты, ускорен вход в «Параметры» (без блокирующей автозагрузки; чтение по кнопке). Версии: app `2.4.6`, cache `v11`.
- **Arduino a20014 v26 ANT (2026-07-07):** `Проекты/Arduino/firmware/Eltavr_firmware/a20014_v26_ant` — форк v7; эталон `a20014_plata_monitora/`. Hex: `releases/app/a20014_v26_9600.hex`. ANT: `../../ANT_BMS/PROTOCOL_ANT_BMS.md`.
- **RS485 ANT BMS (2026-07-08):** на Pi 5 не удалось получить ответ по UART на `ttyAMA0/serial0` при legacy запросах `5A5A...` и новом `7E A1` handshake (ответа нет, похоже BMS не активирована/не в нужном режиме или другой протокол/baud).
- **TTL ANT BMS (2026-07-08):** на USB‑TTL `ttyUSB0` при 9600/19200/115200 (пассивно и legacy live `5A5A 00 00 00 00`) — ответов нет (0 bytes).
- **ANT BLE (2026-07-08):** по `bluetoothctl` удалось подключиться к `9B:FD:E9:52:AB:0A` — `Connected: yes` (GATT без проверки).
- **ANT BMS web v2.4.1 (2026-07-09):** исправлены дубли подписей параметров во всех вкладках; контекстные названия формируются из `field` в `i18n-ru.js`; SW cache `v7`.
- **ANT BMS web v2.4.2 (2026-07-09):** исправлен сломанный CSS-блок `busy-overlay` (дизайн страницы больше не «плывёт»), `SOC`-таблица переименована в уникальные строки `SOC 100%..0%`, добавлен auto-reconnect после краткого BLE-обрыва (frontend+backend); SW cache `v8`, app `2.4.2`.
- **ANT BMS web v2.4.3 (2026-07-09):** убран долгий hang `Connecting BLE`: вызовы `bluetoothctl/hciconfig` теперь с timeout, connect fail-fast до ~45с (6 попыток), UI timeout `/api/connect` 50с, SW cache `v9`, app `2.4.3`.
- **ANT BMS web v2.4.5 (2026-07-09):** ускорен BLE connect до максимально быстрого режима: если сессия уже активна с тем же MAC — мгновенный возврат, connect дедлайн ~20с, 3 попытки, сокращены ожидания `Connected/ServicesResolved`, UI timeout 25с, SW cache `v10`.
- **Cursor Agent PWA / WS т