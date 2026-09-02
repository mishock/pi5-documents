## GEM e6 BMC CAN (2026-09-02) — **работает**

- **Папка:** `Платы и модули/Электрокары/Polaris_GEM_e6_2017/`
- **Подтверждено:** CAN-эмулятор **v4** на неисправной (`5ACA6AGA3H0002115`) — приборка OK, **без DTC** (P1824/P1827 ушли)
- **Памятка:** `notes/BMC_CAN_EMULATOR_v4_OK.md`
- **Скрипт:** `scripts/can-bmc-emulate.py` · **запуск:** `can-setup.sh 250k` → `ai-tmux run gem-bmc-emu 'python3 …/can-bmc-emulate.py'`
- **Карта:** `notes/CAN_BUS_MAP.md` · эталон `logs/20260902-123304_working_key_off.log`
- **Дальше:** прошить H503 (`flash.sh stlink`), SN65HVD230 + реле X3 — `notes/BMC_EMULATOR_PLAN.md`

## Текущий фокус** папка https://drive.google.com/drive/folders/1kJfRYBl7QKTVLEWlw32nK_J_sG-dVb5V · сводка `Сводка_родительское_собрание_2026.md`. **Ожидается ~2026-09-01:** новый договор + документы по налоговому вычету → анализ и обновление сводки.
- **.cursorignore Arduino (2026-08-27):** убраны `Проекты/Arduino/` и `Arduino/` из ignore; значки запрета в explorer.
- **HA Pi5 (2026-08-24):** после reboot не стартовал из‑за `/dev/gpiochip0` (нет на 6.12). Убран из `home_assistant/docker-compose.yml`. UI `:8123` → 200.
- **RS485 ANT J75H (2026-08-24):** связь OK. `/dev/ttyAMA0` **9600**, modern `7E A1`. BMS `ANT@BLE16ZNUB-J75H` / hw `16ZNJARB170A`. Памятка: `Платы и модули/RS485_CAN_HAT/ANT_BMS_J75H_RS485.md`. Проверка: `python3 bms-tools/ant_bms_probe.py --port /dev/ttyAMA0 --baud 9600`.
- **MUST PV18-4024 PRO II (2026-08-20):** ещё один инвертор прошит рабочим профилем через USB `/dev/ttyUSB0`, Modbus `19200`, slave `4`. После `must-verify-profile.py --fix` — **20/20 OK**. Если снова не сойдётся `20117`, сразу запускать `python3 Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/scripts/must-verify-profile.py --fix`.
- **.cursorignore (2026-08-18):** `Платы и модули/` открыта для агента; `**/.cursor/` сужен до backups/data/build. Файл: `Documents/.cursorignore`.
- **MUST LP16-48100 (2026-08-18):** в инверторе 48 В — тип LI, протокол Must New (прог. 41), CAN DIP №11; Bulk **57.6 В**, ток **≤100 А** (лучше 50 А). Не к PV18-4024.

## Текущий фокус
- **Vega MT X LTE / Touareg GP (2026-08-18):** монтаж на **все 3 CAN**. PDF: `Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.pdf`. CAN1 Antrieb 500, CAN2 Komfort 100, CAN3 Infotainment 100. Gateway в комбинации J285.

## Текущий фокус
- **Vega MT X LTE PDF (2026-08-18):** в `Платы и модули/Vega_MT_X_LTE/` собран `INSTALL_Touareg_GP_2009_CASA.pdf` из HTML-версии инструкции; лежит рядом с `.md`.

## Текущий фокус
- **Vega MT X LTE / Touareg GP (2026-08-18):** создан модуль `Платы и модули/Vega_MT_X_LTE/` с исходной страницей, загрузками, фото, `PINOUT.md`, `TECH_SUMMARY.md`, `INSTALL_Touareg_GP_2009_CASA.md`. Стартовая схема для `Touareg GP 2009 CASA`: `+30`, масса, отдельный `IGN 15`, одна пара `CAN`; `K-Line` только при отдельной задаче.

## Текущий фокус
- **n8n (2026-08-17):** полностью удалён. Дашборд Малинка 5 — `Cursor Agent`, timer `pi5-dash-refresh`.
- **Ungate (2026-08-17):** туннель `https://stated-not-scholarships-allergy.trycloudflare.com` health 200; WAN `:47821` Keenetic OK; OAuth `:1455` всегда слушает. Повторный Login ChatGPT.
- **EmKit BMS (2026-08-17):** `:8443` больше не вешается на TLS-сканеры. Handshake в потоке, watchdog `web-config-bms-watch.timer`. Проверка: `curl -sk https://127.0.0.1:8443/` → 200; PWA `/sites/bms_emkit/`.
- **SSH WAN Malinka 5 (2026-08-14):** `ssh pi@91.215.61.76` (Keenetic office+electro :22). Скрипт `bash Документы/.cursor/scripts/install-pi5-ssh-wan-portforward.sh`. Алиас `pi5-wan`.
- **Ungate (2026-08-14):** `extension proxy timeout` — UI ждал старый хост. Закрыть вкладку Ungate и открыть снова.
- **Ungate (2026-08-14):** Analytics `Failed to fetch` на Remote SSH — прокси через extension host. После правки: Reload Window. API `:47821` живой.
- **БК Pico Audi (2026-08-14):** без машины, отладка UART0 JSON/KW1281. Экран: RPM / код / ОЖ. 16:06.
- **Mint Live USB (2026-08-14):** `10.10.0.85` `eltavr-mint`, user `mint`. С Pi 5: `ssh mint`. Windows на NVMe: пароли `Растислав` и `Admin` сброшены (пустые). HDD DATA без SAM.
- **Pico-Eval-Board (2026-08-14):** `Платы и модули/Pico-Eval-Board/` — PINOUT + TECH_SUMMARY; схема/демо скачаны. Pico в комплект не входит.
- **Дашборд Pi 5 (2026-08-17):** снимок без n8n — `Проекты/Cursor Agent/scripts/build-pi5-dash.py` → `data/pi5.html`; timer `pi5-dash-refresh`; PWA **Малинка 5** `/malinka-dash`.
- **n8n (2026-08-17):** удалён (Docker, MCP, Keenetic `:5679`, папка `Проекты/n8n`). Не поднимать.

## Текущий фокус
- **БК минимальный ЭБУ (2026-08-09):** `bc_ecu.py` — RPM/ОЖ/V; Kali `start_bc.sh`. V канал пока пустой.

## Текущий фокус
- **БК freeze (2026-08-09):** починен `_recv_block` + ЦЗ off; `cluster-bc` LIVE ~250мс. RPM с ЭБУ сейчас 0 — проверить при заведённом моторе.
- **ЭБУ 0x01 (2026-08-09):** SIMOS AHL **9600** бод; ident+MB (02/F4) работают. БК `engine_cl`.

- **FIS→MFA (2026-08-09):** pin ø **14.1** / trip 124.5 / fuel0≈37.6 на Kali (`data/mfa_state.json`); BC стартовал; **LIVE verify ждёт** (Kali offline). Проверка: `/tmp/bc_live.json` → avg=14.1, avg_spd~26, fuel~20.
- **A4 B5 КПП (2026-08-09):** завод АКПП 01N → МКПП владельцем; адрес 02 не опрашивать; OBD без CAN.
- **Коммуналка ежемесячно (постоянно):** новые чеки+показания каждый месяц; все чеки хранить; таймер `komunalka-drive-sync.timer`.
- **Коммуналка (2026-08-09):** Drive https://drive.google.com/drive/folders/1zbPCmouSU8yJhr-tGwe5BKfQsRqeN14b — в корне только 5 папок услуг (без файлов); CSV/PDF внутри папок. **Где счётчик — CSV в натуральных единицах (вода/газ м³, энергия кВт·ч); газ ~4.455 м³/сут, вода ~0.439 м³/сут. Скрипты `export-crimea-energy.mjs`, `export-all-services-to-drive.mjs` (`scrapeGas` → `?page=pokazaniya`). Жилсервис/экор — без CSV-сводки (нет счётчика), только PDF. Экор: type не только m.


## Текущий фокус
Двери БК — **ЦЗ 0x35** LIVE («все закрыты»). Comfort 0x46 нет. Handshake `~kb2`. Файлы на Kali: `~/Projects/cluster_pi/{kw1281_client.py,ui/doors.py,ui/obd_feed.py,data/door_map.json}`.

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
## Kali БК опрос (2026-08-07)
- Макс. частота: poll=0, G1 каждый цикл, G2↔G3, sleep 2ms ≈1.6 Hz
- Старт: `tmux … start_bc.sh` / `bash ~/Projects/cluster_pi/scripts/start_bc.sh`
