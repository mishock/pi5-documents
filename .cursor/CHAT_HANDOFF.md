## Пушкина_29 — обращение и схема двора (2026-10-08)
- Стабильно: `Пушкина_29/Обращение - Пушкина 29.docx` и `Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf`; под снос только С1, С2 нигде не упоминается, кирпичная клумба П — «не трогать», параллельна дому и заканчивается на уровне центра Д1.
- Обращение визуально проверено: 2 страницы, вся таблица подписей на второй; рамки заданы явно в OOXML и видны в мобильных просмотрщиках. Схема сохранена в исходном оформлении, без белой заплатки.
- Проверка: `unzip -p "Пушкина_29/Обращение - Пушкина 29.docx" word/document.xml | grep -o С2` и `pdftotext "Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf" - | grep С2` — пусто. После правок запускать `bash Проекты/drive-folder-sync/scripts/run-sync.sh`.

## Xray — ночное автообновление (2026-10-07)
- Таймер: `xray-nightly-update.timer` → **00:20 MSK** (`Persistent`, + до 2 мин jitter).
- Скрипт: `~/bin/xray-nightly-update.sh` (VPS `installXray` + Pi5 бинарник, **2× verify**, remediate).
- Лог: `~/logs/xray-nightly-update.log`. Установка: `Проекты/ai_assistant/scripts/install-xray-nightly-update-timer.sh`.

## VPN 3x-ui — клиент Владимир (2026-10-07)
- Стабильно: inbound `vless-reality`, email `Владимир`, flow `xtls-rprx-vision`, комментарий «Владимир Шуликов».
- Подписка: `https://89.127.199.6:2096/sub/9a690f7c-0051-4544-8be4-d83a7578a471` (Hiddify / v2rayN / v2rayNG).
- Док: `vpn-guide.md` (таблицы клиентов и подписок).

## Камера Hikvision электроцеха → HA + Apple «Дом» (2026-10-07)
- Стабильно: камера 10.1.30.64 (admin, прошивка 190909); HA `camera.elektrotsekh` + `binary_sensor.elektrotsekh_dvizhenie`; push — `packages/hikvision_elektrotsekh.yaml`; в HomeKit «HASS Bridge» камера с датчиком движения (`exclude_accessory_mode` снят в `core.config_entries`).
- Проверка: `curl -s -o /dev/null -w '%{http_code}' http://10.1.30.64/`; диагностика HomeKit entry `02271e20a06a7af8829f703427537a32` — аксессуар «Камера электроцех» (службы 110 + 85).

## Коммуналка — тарифы + графики (2026-10-06)
- Стабильно: `komunalka.service` :8000, PWA `/sites/komunalka/` (таймаут прокси 300 с). История тарифов копится в `Проекты/komunalka/data/tariffs.json`.
- Проверка: `curl -s http://127.0.0.1:8000/api/tariffs | head -c 300`; `systemctl --user is-active komunalka.service`.

## M350 ЧПУ — прошивка 2026-09-09 + CAM cam20–37 (2026-10-05)

- Фокус: `Платы и модули/M350_CNC_Controller/` (IP 192.168.31.99, SMB1). Доп. CAM cam20–39 (cam38 Z0 щуп+датчик длины, cam39 калибровка щупа). #141=3000 (свой slib-g, подача XY к датчику). Перезагружен 10:04, #141=3000 и #76=Да активны. ОЗУ 57 МБ (scripts/m350-proc.sh). cam10–19 заменены улучшенными (notes/CAM10-19_NEW_20261005.md, откат backups/20261005_my_cam10-19) — ждёт перезагрузки контроллера. Ревизия 2026-10-05: cam20–27,32,33 исправлены (notes/CAM_REVIEW_20261005.md, сим `m350-cam-sim.py --fix`). Картинки cam10–39 новые (m350-cam-pics.py), Al Tie: защита шаг Z=0 + врезание 3°. O502 (slib-g): переезд к датчику без A/B/C (правка той же длины — иначе ломается хоуминг Y O503 до перезагрузки) — ось B = ведомый Y с лимитом 1000 мм/мин тормозила ход из дальнего угла (notes/O502_SLOW_TRAVEL_FIX_20261005.md, откат backups/20261005_o502_before); O9053 без F/ABC, G00 3000 (backups/20261005_rapid_before); DM856 SW3 ON 5.6A; ускорение G00 300, Z 1500/800 (backups/20261005_accel_before); проверка: `cmp` slib-g.nc с generated/o502_fix.
- Доки: `notes/CAM_ADDONS_20261005.md`, `notes/FIRMWARE_UPDATE_20261005.md`. Сборка: `scripts/m350-cam-addons.py`.
- Проверка: `smbclient -N -s /tmp/m350-fb/smb.conf //192.168.31.99/CNCDISK -c 'cd CAM; ls'` (30 макросов, NT1).

## GEM ESP32-C3 BMC emu MIN v0.4.0 — TJA1050 (2026-09-30)

- Проводка: VCC→5V, GND, TX→GPIO4, RX→1k→GPIO5 (+2k на GND), CANH p14, CANL p13; 120 Ω в жгуте снять.
- Прошивка: `bash firmware/gem_bmc_can_emu_esp32c3/scripts/flash-can-min.sh`; MCP2515: `ENV=esp32c3_can_min_mcp …`.
- Проверка Serial: `CAN TX ok/1s≈115 fail/1s=0 … st=RUN tec=0`.

## GEM H503 BMC emu v4.3.0 — TJA1050 (2026-09-30)

- Проводка: TJA1050 VCC→5V (не 3.3!), GND, TX→B7, RX→B8, CANH→X3 p14, CANL→X3 p13; 120 Ω на модуле в жгуте снять.
- Прошивка: `bash firmware/gem_bmc_can_emu_h503/scripts/flash.sh openocd` (ST-Link stlink-dap).
- Проверка: UART 115200 PA9 → `TX ok=~115 fail=0 | RX=…`; LED 1 Гц.

## Текущий фокус

- **Deye 6.6K OG03 + АКБ ЭЛЬТАВР 230 Ач / JK-B2A20S20P (2026-10-01):** SOC JK 98→93 % — уход кулонометра (ячейки 3,44 В < `SOC-100% Volt` 3,50 В), АКБ полная; связи BMS↔Deye нет. Разбор: `Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/diag_2026-10-01_АКБ_SOC/README.md`. Декодер: `python3 "Платы и модули/BMS/JK_B2A20S20P/scripts/decode_jkcfg.py" <file.jkcfg>`. Файлы с ПК: `scp -O 'pc:C:/Users/Михаил/Downloads/<имя>' .` Шаблон настроек: `…/Deye_SUN-6.6K-OG03LP1-EU-AM2/generated/ШАБЛОН_НАСТРОЕК_Deye6.6K_АКБ_ЭЛЬТАВР_48V230Ah.pdf` (пересборка `python3 scripts/generate_battery_template_pdf.py`). Готовый .jkcfg: `Платы и модули/BMS/JK_B2A20S20P/notes/configs/ELTAVR_48V230Ah_16S_template/` (`scripts/make_jkcfg.py`). PDF BMS: `Платы и модули/BMS/JK_B2A20S20P/generated/` (`scripts/generate_jk_template_pdf.py`). QR→Drive: `scripts/upload_jkcfg_drive.py` (ID в `notes/configs/ELTAVR_48V230Ah_16S_template/drive.json`).

- **BMS (2026-09-30):** все BMS в `Платы и модули/BMS/` (индекс `README.md`): `JK_PB1A16S10P`, `JK_B2A20S20P`, `ANT_BMS_16ZNJ6-16S-130A` (TTL/BLE, ESPHome `ant_bms`). `bms-tools/` в корне — живой сервис `ant24c-logger`, не переносить без остановки сервиса. Проверка: `ls "Платы и модули/BMS"`.

- **Подогрев АКБ через ESP32 (2026-09-30):** `Платы и модули/BMS/JK_B2A20S20P/firmware/esphome_heater/` — `bash build.sh` (сборка OK), `bash build.sh upload /dev/ttyACM0` (нужен `secrets.yaml`). Не прошито.

- **Подогрев АКБ JK (2026-09-30):** `Платы и модули/BMS/JK_B2A20S20P/notes/HEATING.md` — схема HT−/нагреватель/термовыключатель/предохранитель, пороги, тест. Проверка: `ls "Платы и модули/BMS/JK_B2A20S20P/notes"`.

- **JK-B2A20S20P (2026-09-30):** `Платы и модули/BMS/JK_B2A20S20P/` — ревизия V19; DRY нет, реле через порт **P8 报警** (VCC/GND пищалки, напряжение замерить, через оптрон) или ESP32 по UART P5 115200 3,3 В / BLE (`syssi/esphome-jk-bms`). Проверка: `ls "Платы и модули/BMS/JK_B2A20S20P"`.

- **GEM BMC S3-RS485-CAN v0.1.0 (2026-09-30):** `…/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/`, прошит на плату. Проверка: `bash scripts/flash.sh` → лог `ok/1s≈141`; на машине ждём `fail=0 tec=0`. CAN H/L → X3 p14/p13, джампер 120 Ω снят.
- **Deye RW-F16 2×/3× АКБ (2026-09-29):** PDF `Платы и модули/Солнечные_инверторы/Deye_RW-F16/generated/Deye_SUN-20K_{2x,3x}RW-F16_Installation_Setup_RU.pdf` (по одному на вариант). Пересборка обоих: `cd "Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts" && python3 generate_rwf16_system_pdf.py` (аргумент `2`/`3` — один).
- **GEM BMC S3 v0.2.0 (2026-09-30):** `Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/` — BLE→ANT SOC в CAN, Wi‑Fi `GEM-BMC`. Проверка: `bash scripts/flash.sh` (лог: `SOC=…% ANT | BLE conn`, ok+fail≈141); запасная `flash.sh --min`.
- **PlatformIO Docker (перенесён 2026-09-30):** `Платы и модули/ESP32-S3-RS485-CAN/` (раньше `Проекты/…`). Проверка: `bash scripts/pio.sh run` → SUCCESS; прошить: `bash scripts/flash.sh --monitor` (плата → /dev/ttyACM0).
- **ESP32-S3-RS485-CAN (2026-09-28):** документация в `Платы и модули/ESP32-S3-RS485-CAN/` (PINOUT, TECH_SUMMARY, schematic, demo). Проверка: `ls "Платы и модули/ESP32-S3-RS485-CAN"`.
- **Pi3 гараж (2026-09-26):** HA + switch как раньше, **без микрофона INMP441**. Boot: `i2s`/`inmp441-dmic` закомментированы. Switch: 6 реле CH3…CH8. Проверка: `ssh pi@100.102.186.61 'docker ps; curl -s -o /dev/null -w %{http_code} http://127.0.0.1:8123/'`.

## HA Pi3 через Pi5 (2026-09-28 16:15)

- **Стабильно:** `http://10.1.30.126:8124` → HA Pi3 (`systemctl --user status pi3-ha-proxy`). NetBird ПК↔Pi3 флапает (ПК 0.71.2) — обновить клиент на ПК.
- **Проверка:** `curl -s -o /dev/null -w '%{http_code}' http://10.1.30.126:8124/manifest.json`; флапы: `ssh pi3 'sudo grep -c "dFhcyrdF.*ICE disconnected" /var/log/netbird/client.log'`.

## Pi5 HA — ANT BMS24C графики (2026-09-28 15:50)

- **Стабильно:** `*_graph` с мёртвой зоной (0.15 В / 1.5 % / ±0.3 А), оси фиксированы; откат `agent-change-revert.sh` ID `20260928T154644`.
- **Проверка:** `docker logs homeassistant --since 10m | grep -i ant24c`; дашборд `http://10.1.30.126:8123/ant-bms-24c/home`.

## Pi3 HA — электросчётчик гаража (2026-09-28 13:35)

- **Стабильно:** CSV `ha_config/data/garage_electric_meter.csv` — источник истины; поле «Текущие показания» (любое устройство) → автоматизация → CSV; при старте HA значение берётся из CSV; `initial` убран.
- **Проверка:** `ssh pi@100.102.186.61 'tail -3 ~/Raspberry_Pi_3_HomePortable/ha_config/data/garage_electric_meter.csv'`; опечатка (меньше прошлого / >50 kWh/сутки) — откат + уведомление в HA.

## eltavr-bot

- **eltavr-bot** (`Проекты/telegram_bot/`): «Поиск по VIN» починен 2026-09-25 — был зависший polling к Telegram через `10809`. Проверка: `docker logs eltavr-bot --tail 30`, `pending_update_count` через getWebhookInfo.

## Hyperion EOS 0606i (2026-09-23 14:55)

- Модель `#HP-EOS0606i-C`: firmware update **нет** (только PC logging).
- На Pi5 USB: LAWICEL CANUSB → `/dev/ttyUSB0` (не Hyperion UART).
- Док: `Платы и модули/Hyperion_EOS_0606i/`.

## krimsvet.ru fix (2026-09-23 10:48)

- Было: `/favicon.ico` 404; `favicon.png`/`apple-touch-icon.png` ≈1MB (фото 1536×1024); в `bundles.json` meta.phone `+79787918507` ≠ сайт.
- Сделано по FTP (`www/krimsvet.ru/`): нормальные иконки + phone `+79789858707`.
- Хостинг: REG.RU u3565608 / server276; доступы в письме «Создан хостинг u3565608».

## krimsvet.ru (2026-09-23 10:39)

- Живой лендинг ЭЛЬТАВР: https://krimsvet.ru/ — HTTP 200, калькулятор на `app.js`.
- Хостинг: REG.RU (`ns1/ns2.hosting.reg.ru`, A `37.140.192.181`).
- Исходников в `Documents/Проекты` нет — править на хостинге или восстановить из бэкапа REG.RU.
- Мелочь: `/favicon.ico` → 404 (есть `/favicon.svg` и `/favicon.png`).

## Солнечные панели (2026-09-22 10:45)

- Папка: `Платы и модули/Солнечные_инверторы/Солнечные_панели/`
- Trina Vertex S+ **TSM-NED9R.28** 445–470 Вт → `Trina_TSM-NED9R.28_445-470W/`
- Jinko **JKM605-630N-66HL4M-BDV** 605–630 Вт → `Jinko_JKM605-630N-66HL4M-BDV/`
- Индекс: `Солнечные_панели/README.md`; родительский `Солнечные_инверторы/README.md` обновлён.

## Диск Pi5 (2026-09-22 10:01)

- NVMe: **86G / 117G (77%)**, свободно **~26G** (раньше было хуже: 86%/~17G).
- Крупное: Cursor snapshots (~7.7G), Docker ~8G, `.cache` 5.2G (playwright 1.9G), apt 1.3G, Arduino/PIO/Gradle/Codex.
- Безопасная чистка без ломки проектов: `apt clean`, pip cache, playwright, старые Cursor snapshots — по запросу.

## ESP BMC v0.6.13 — P1824/P1827 (2026-09-18 15:18)

- SPN **524273** FMI 31 = P1824 BMC Status Counter; **524237** FMI 31 = P1827 Charger Counter.
- Фикс: планировщик без `slot=now` (догон +=period); SoftAP off; pure EF3 без overlay.
- Бин: `…/releases/gem_bmc_can_emu_esp32c3_v0.6.13.bin`
- На машине: ключ OFF→ON, стереть VEH FAULT, проверить приборку.

## ESP BMC v0.6.12 — BLE BMS выкл (2026-09-18 15:07)

- `ANT_BLE_ENABLE=0` в platformio.ini: нет скана/коннекта к ANT.
- CAN + реле + SoftAP; эмуляция SOC=100% U=54V.
- Бин: `…/releases/gem_bmc_can_emu_esp32c3_v0.6.12.bin` (~816 KB).
- Flash: baud 115200 (460800 на этом USB давал I/O error).
- Включить BLE снова: `-DANT_BLE_ENABLE=1`.

## ESP BMC v0.6.11 — фикс DTC на приборке (2026-09-18 14:57)

- Причина: `NimBLEScan::start(sec,false)` блокировал loop → тишина CAN → P1824/P1827; плюс 4 кадра/100ms в 3 TXB MCP → fail.
- Фикс: async/continuous scan; CAN task prio=5; phased 0FF3/10/11/12; Serial не из CAN-задачи.
- Smoke USB: 24× `ok/1s=141 fail=0 gapMax=10–11ms`, RX~360 (шина живая).
- Бин: `Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.11.bin`
- На машине: ключ OFF→ON, ошибки должны уйти (или стереть сканером).

## ESP BMC v0.6.9 — dual ANT proto (2026-09-18 10:50)

- SoftAP: MAC + протокол (legacy / modern / auto) → NVS `ant_proto`.
- API: `POST /api/config` `{"mac":"…","proto":"legacy|modern|auto"}`.
- Текущая BMS ANT-BLE24C → **legacy**. Другая MaYi → **modern**.
- Бинарь: `…/releases/gem_bmc_can_emu_esp32c3_v0.6.9.bin`

## ESP BMC v0.6.8 — стабильность OK (2026-09-18 10:45)
- Диск Pi5: 86% (свободно ~17G); Cursor snapshots ~17G — кандидат на чистку.

- Прошивка: `…/firmware/gem_bmc_can_emu_esp32c3/` v0.6.8 (MCP Normal, ALLTXBUSY→reinit, hold last ANT 15с, legacy DBDB, EF3 overlay U/I/SOC).
- Проверено: Serial soak 55с + 120с → TX fail=0, disconnect=0, SOC=96% ANT.
- Pi BT logger: `ant24c-logger` / rfcomm **stopped** (не поднимать, пока ESP на BLE). Вернуть: `sudo systemctl start ant24c-rfcomm ant24c-logger`.
- SoftAP: SSID `GEM-BMC` / http://192.168.4.1/

## Deye F41 / 3ф × 3 (2026-09-17 12:37)

- **F41** = один из параллели в OFF. При 3ф по 1 шт.: на LCD **Master на всех трёх** (A/B/C, SN 01/02/03) — по EN §3.12; не Slave на №2/№3.
- PDF обновлён: `…/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/LCD_НАСТРОЙКА_3Ф_3шт.pdf`

## Deye 3ф × 3 — LCD чеклист (2026-09-17)

- PDF: `Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/LCD_НАСТРОЙКА_3Ф_3шт.pdf`
- №1 Master A/SN01 → L1; №2 Slave B/SN02 → L2; №3 Slave C/SN03 → L3; DIP Parallel ON; Grid Type = Single Phase 230 V / 50 Hz.

## CAN_Sniffer_Shield_LCD (2026-09-16 16:11)

- Баг: после `begin()` режим **LOOPBACK** → шину не видел.
- Фикс: `CAN.setMode(MCP_NORMAL)`; дефолт **250 kbps**; прошит Uno.

## CAN_Sniffer_Shield_LCD (2026-09-16)

- Дефолт скорости CAN: **250 kbps** (`currentSpeed = CAN_250KBPS`).
- Прошивка: `firmware/CAN_Sniffer_Shield_LCD/scripts/flash.sh` (Uno `/dev/ttyACM0`).

## Aqara CH-H01 3D65 — motion и хаб (2026-09-16)

- **Дома** (есть хаб + Apple TV в сети): всё OK, **включая motion sensor**.
- **Гараж** без Home-хаба в той же Wi‑Fi: плитка motion «не отвечает», пуш при детекции может приходить.
- Эталон камеры: `flip=3` + сток `osd_orig`. Bool-патч не включать без нужды.

## SILA 13S applied (2026-09-16)

- SN `96342504111477`: BVM/BVF **54.0**, BRD **53.0**, BVU **42**, EQ=0, EQV **54.0**, MCG **10**.
- Apply: `scripts/isolar-apply-13s.sh` (setParam без urlencode). Verify: `scripts/isolar-fetch-settings.sh`.

## SILA Battery 13S Li-ion (2026-09-16)

- Аппарат: **SILA VM II Premium+ 6.2K**, SN `96342504111477` (не Adion).
- Профиль User: C.V 54.0/54.6, Float 53.5–54.0, Under 42–43, EQ off.
- Док: `Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/notes/USER_13S_LION_SETTINGS.md`.
- Старый `check_Li_ANT_BMS` 56.4/54.0 — только для **LFP 16S**.

## i.Solar Battery 13S Li-ion (2026-09-16)

- Устройство `96342504111477` / WIFI2025031108713: заводские C.V 56.4 / EQ 58.4 **нельзя** на 13S.
- Профиль: C.V 54.0, Float 53.5–54.0, Under 42–43, EQ off. Док: `Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/notes/USER_13S_LION_SETTINGS.md`.
- Офисный Adion LiFePO₄ 16S (56/54/46) — **другой** профиль.

## Aqara CH-H01 3D65 — ЭТАЛОН OK (2026-09-15)

- **Статус:** всё ок на этом этапе (подтвердил пользователь 2026-09-15 ~15:41–15:59).
- `flip=3` (подвес вверх ногами), `osd=1`, bind **`/mnt/config/osd_orig` → `/etc/osd`** (сток).
- Timestamp читаемый — **шрифты OSD не крутить**.
- Live: Wi‑Fi AiNET, без VPN / Private Relay.
- SD: `/mnt/sdcard/record/`, `cover=1`.
- Док: `Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md`.


## Bybit API 403 → Tor (2026-09-12)
- **2026-09-14:** офисный Keenetic ребут → краткий даун ELTAVR_/XKeen; сейчас VLESS OK (`89.127.199.6`).

- **Причина:** xray exit = Dallas US; Bybit CloudFront режет US (+ прямой Крым тоже 403).
- **Fix:** Tor на VPN_Server (`tor@default`), туннель Pi5 `bybit-tor-tunnel.service` → `127.0.0.1:9051`.
- Скрипты: `bybit-http.py` (curl+SOCKS), `recv_window` 60s.
- Проверка: `python3 .cursor/scripts/bybit-balance.py` → live UNIFIED.
- Установка туннеля: `bash .cursor/scripts/install-bybit-tor-tunnel.sh`

## Aqara G2H Wi‑Fi QR / psk (2026-09-10)

- **Причина:** optical QR → битый `psk` в `/mnt/config/miio/wifi.conf` → штатный `wifi_start.sh` пишет только `/tmp/wpa_supplicant.conf`.
- **Fix:** hardened `/usr/bin/wifi_start.sh` (orig сохранён); `wifi.conf.good`; док `notes/WIFI_QR_PSK_CORRUPTION.md`.
- Скрипт: `Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/wifi_start_hardened.sh`.
- Камера в AiNET: `10.0.20.22`. Повторный оптический QR Wi‑Fi не нужен.

## Deye «Зарядка» / Solarman Pro (2026-09-10)

- Веб logger: WAN `:8081`, SN stick `1538281644`, инвертор `2607250740`.
- **Solarman Pro:** автологин невозможен (AWSC slider). Нужен ручной вход → добавить collector `1538281644`.
- Облако stick: `status_a/b` пустые; Server B на M5434 не сохраняется; XKeen bypass `10.1.30.81→direct` есть.
- Письмо пользователю: `jarvis-need-user` отправлено.

## Aqara G2H NOR (2026-09-09)

- В NOR `0x30000` записан **xz** U-Boot (срез FAT `UBOOT` с байта 64, 94656 байт). IPL `0x4000` = `IPL_` цел.
- Проверка на чипе: `hexdump -s 196608 /dev/mtd0` → `fd 37 7a 58`.
- Дальше: **вынуть FLASHKA**, цикл питания, UART 115200. С картой IPL грузит `UBOOT` с SD и NOR не смотрит.
- Док: `Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/NOR_UBOOT_XZ.md`

## Adion Expert 6kW Twin (2026-09-08) — **залит**

- S/N **96342510600141**, USB `/dev/hidraw0`, PI30.
- Профиль: `applied-settings/working_profile.commands` → User 56.0/54.0/46.0, заряд 80 A / сеть 30 A.
- Дамп: `Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/applied-settings/units/96342510600141.txt`
- LCD ещё руками: **28=SIG**, **10=OnL**, **16=UCb**, **33=EDS**, **39=AEN**.

## JK-PB1A16S10P (2026-09-08)

- Папка: `Платы и модули/BMS/JK_PB1A16S10P/`
- Экземпляр: SN `605146845007308`, BLE `A4:C1:38:0C:0B:28`, опция CEHMPRT (CAN, предзаряд, нагрев, сухой контакт, параллель, RS485, температура).
- Дальше: приложение JK BMS → химия / S / протокол / прошивка. К инвертору не подключать, пока не сверены пины CAN.
- Прошивки/протоколы: `Платы и модули/BMS/JK_PB1A16S10P/notes/FIRMWARE_AND_PROTOCOLS.md`. Файлы 069 V19.21 и V19.31 лежат локально. Не шить.

## Aqara ZNSXJ12LM — HomeKit нет (2026-09-08)

- Камера снова на `3.5.8_0062`, процесс `camera -M` жив, AiNET `10.0.20.22`.
- Пакет 2.2.3 не встаёт: нет `libdns_sd.so`. Кода HomeKit на ножке нет (QR = серийник).
- Док: `Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/G2_vs_G2H_FLASH.md`.

## Aqara G2 → HA Pi3 (2026-09-07)

- **Найдено:** `Camera-Hub-G2H-EAA1` `10.0.20.5` (ZNSXJ12LM) + `Camera-Hub-G2H-EE74` `10.0.20.6` (CH-H01).
- **Блокер:** обе в Apple Home (mDNS `paired`). Снять из «Дом» → код HomeKit → `bash ~/Raspberry_Pi_3_HomePortable/scripts/add-aqara-g2-camera-ha.sh КОД`.
- **Проверка после pairing:** `camera.aqara_g2` idle, зона garazh.

## ANT BMS24C графики (2026-09-07)

- Иголки убраны: hold-last в логгере + `*_graph` на дашборде + purge нулей из recorder.
- Проверка: обновить страницу ANT BMS24C в HA (`:8123`).


## 2026-09-07 PWA UUID
- Фикс resume `agent-<uuid>` → UUID; проверить: обновить PWA, отправить «ты тут?».
## ANT BMS V2 аккаунт (2026-09-07)

- **Логин:** mishock24@gmail.com · **uid:** 842247 · пароль в заметке
- **Заметка:** `Проекты/Arduino/firmware/ANT_BMS/notes/ANT_BMS_V2_ACCOUNT.md`
- Вход в приложении по почте; локальный веб без аккаунта: порт 8788

## Cursor Pi5 worker (2026-09-07) — **починен**

- **Причина:** worker без xray HTTP `:10809` → «Failed to reach the Cursor API» / restart loop
- **Фикс:** `~/.config/cursor-worker.env` (PROXY+NODE_OPTIONS), unit `cursor-self-hosted-worker.service`, `~/bin/cursor-pi5-worker-fix.sh`, IDE `http.proxy`
- **Проверка:** `systemctl --user is-active cursor-self-hosted-worker` → active; `cd ~/Documents && cursor-agent worker debug` → Non-privacy **1 wo

### ESP BMC (15:45)
Текущая прошивка: **MIN v0.3.0** pure CAN (нет BLE/WiFi). `scripts/flash-can-min.sh`.

## 2026-09-30 komunalka
- Стабильно: Крымэнерго обновляется через вкладку «Сайты» (прокси komunalka timeout 300 с); даты платежей в формате ДД.ММ.ГГГГ.
- Проверка: `journalctl --user -u komunalka.service | grep "\[energy\]"` — строка `оплаты: последний=…, чеков=5`.
