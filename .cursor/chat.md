## Фокус (14:32, 2026-10-26) — Пушкина 29: оформление схемы плитка/асфальт

PDF переоформлен: шапка с акцентом, карточки легенды, рамка плана, подписи зон с цветной полосой. Редакция 2026-10-26. Файлы: `Пушкина_29/Приложение 1 - Схема зон покрытия (плитка-асфальт) - Пушкина 29.pdf`, генератор `scripts/generate_coverage_scheme_pdf.py`. Drive sync OK (`exit=0`).

## Фокус (13:40, 2026-10-26) — Пушкина 29: обрезка по красному контуру

Схема ЗУ3 обрезана строго по красному контуру из Прил.2. PDF обновлён, `DRAW_ZONES=False`. Drive sync.

## Фокус (13:32, 2026-10-26) — Пушкина 29: схема ЗУ3 из Прил.2

PDF пересобран из `Приложение 2 - Чертёж территории` (ЗУ3, поворот −48°, без плитки/асфальта). Файл: `Пушкина_29/Приложение 1 - Схема зон покрытия (плитка-асфальт) - Пушкина 29.pdf`. Генератор: `DRAW_ZONES=False`. Drive sync OK.

## Фокус (13:07, 2026-10-26) — Пушкина 29: схема плитка/асфальт

Новый PDF: `Пушкина_29/Приложение 1 - Схема зон покрытия (плитка-асфальт) - Пушкина 29.pdf` (2 л., ред. 2026-10-26). Генератор: `Пушкина_29/scripts/generate_coverage_scheme_pdf.py`. Старая схема сноса 08.10 не тронута. Drive sync: OAuth `invalid_grant` — на Drive не ушло. Обращение по плитке vs 08.10 — другая тема (покрытие, не снос).

## Фокус (12:59, 2026-10-26) — Пушкина 29: обращение по плитке

Изучен DOCX `Пушкина_29/Обращение по плитке - Пушкина 29.docx`: коллективное обращение в Администрацию Симферополя (26.10.2026) против сплошного асфальта; просьба — комбинированное покрытие (плитка + асфальт). Уполномоченная: Валюкевич Н.Г., кв. 18. Подписи: 11 собственников. Приложение 1 в тексте — схема; в папке есть PDF-схемы.

## Фокус (12:26, 2026-10-26) — M350 START: виноват #76

Владелец выключил **#76** (macro scan) — станок заработал. При #76=1 перед пуском сканируется вся УП → на больших файлах «молчит». Заметка обновлена: `…/notes/START_SILENT_20261026.md`.

## Фокус (12:20, 2026-10-26) — M350 не стартует УП

Настройки START/E-stop/софт-лимитов **OK** (как в бэкапе). В `coordinate`: маш. X≈−25.8 / Z≈83.6 при лимитах X≥−1, Z≤3.05 → блок старта. Нужны RESET + HOME. Заметка: `Платы и модули/M350_CNC_Controller/notes/START_SILENT_20261026.md`.

## Фокус (11:42, 2026-10-26) — Daly BLE с Pi 5 OK

К `73:C1:42:10:00:15` подключаемся через Bumble HCI USER (`scripts/daly_ble_connect.sh`). Прочитано: 17S, 21°C, V=11.4 / SOC=0 (проверить пакет). Док: `notes/BLE_PI5.md`. BlueZ/Cypress → 0x3e; ретраи + низкий duty scan.

## Фокус (09:50, 2026-10-26) — Daly Smart BMS

Папка: `Платы и модули/BMS/Daly_BMS_7-17S_200A/` — 7–17S, 200 A, BT `DL-73C142001510`, мануалы Old Series + UART протокол. Индекс BMS и module-docs-priority обновлены.

## Уточнение (20:07, 2026-10-23) — схема Аникеева

Сухой контакт **параллелим** (оба Gen Signal ВКЛ). Сила: **один автомат с ГУ → оба INV**. PDF/md обновлены. Выезд ~15:00.

## Фокус (19:56, 2026-10-23) — автозапуск TSS ↔ 2× Deye 20K

**ДГУ:** ТСС TQc 22TS ST / АД-16С-Т400-1РКМ5, 16 кВт, S/N DG030000022116.
**Инверторы:** 2× Deye SUN-20K-SG05LP3-EU-SM2 (мануал на Pi 5).
**Готово:** чеклист + PDF; DIN 40/41 = Remote Start (тест на объекте); Gen Signal только Master; Rated 14000 W.

- `Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/notes/АВТОЗАПУСК_ГЕНЕРАТОР_TSS_2xDeye20K.md`
- `…/generated/АВТОЗАПУСК_TSS_TQc22_2xDeye20K.pdf`
- `Платы и модули/Дизельные_генераторы/TSS_TQc_22TS_ST_АД-16С-Т400/`

## Пометка даты при правках (15:45, 2026-10-23)

**Правило (alwaysApply):** `.cursor/rules/date-stamp-on-changes.mdc` — при любой правке ставить `YYYY-MM-DD` (шапка md, редакция PDF, CHANGELOG). Запрошено пользователем 2026-10-23.

## JK SoftAP CAN RX флеш (11:27, 2026-10-23)

`jk_ble_pylon_deye` **v0.1.6**: лог CAN RX → LittleFS `/canrx.dat` (128 кадров, flush ~1 с), переживает отключение питания. Релиз: `firmware/jk_ble_pylon_deye/releases/jk_ble_pylon_deye_v0.1.6.bin`. После USB: Serial `canlog` или веб.

## Офис XKeen VPN (10:14, 2026-10-23)

ELTAVR_VPN: xray был убит OOM (~245 МБ на 512 МБ Giga). Поднят; `GOMEMLIMIT=100MiB` + policy bufferSize + cron watchdog `/opt/bin/xkeen-watchdog.sh`. Скрипт: `.cursor/scripts/install-office-xkeen-oom-guard.sh`. Док: `keenetic-routers.md` § OOM.

## JK SoftAP captive (10:05, 2026-10-23)

v0.1.1: при подключении к `JK-DEYE` сразу HTML настроек (DNS * + generate_204/hotspot-detect). Прошито FLASH_OK.

## JK BLE → Deye Pylon CAN (09:55, 2026-10-23)

Прошивка `Платы и модули/ESP32-S3-RS485-CAN/firmware/jk_ble_pylon_deye/` v0.1.0: JK-B2A20S20P по BLE → CAN Pylon 500k → Deye 6.6K; SoftAP `JK-DEYE`/`jk-deye-cfg` → веб (MAC + скан BLE). Сборка Docker SUCCESS. Релизы `…/releases/jk_ble_pylon_deye_v0.1.0{,_0x0}.bin`. На Deye: Lithium + Pylon. **Прошито** `/dev/ttyACM0` FLASH_OK (09:58).

## ESP BMC MIN v0.4.6 — без WiFi/BLE/сайта (16:56, 2026-10-21)

MIN: `radioForceOff()` при старте; нет web_ui/NimBLE в сборке; Serial `Radio: WiFi OFF, BLE OFF, SoftAP/web NONE`. Прошито MCP. Релизы `…/releases/gem_bmc_esp32c3_v0.4.6_{MCP2515,TJA1050}.bin`.

## ESP BMC LED v0.4.5b (16:50, 2026-10-21)

После v0.4.4 LED «поморгал и потух». Фикс: фаза по millis, CAN OK = в основном ON + пауза 150 мс/с; старт 4 вспышки + 1.5 с сплошной. Serial: `LED=ON(pin=0)`. Прошито MCP `FLASH_OK` (`v0.4.5b`). Релизы: `firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_esp32c3_v0.4.5_{MCP2515,TJA1050}.bin`.

## Remote Control Pi5 — gmail (15:30, 2026-10-21)

Worker **Документы на Pi5** снова online под **mishock24@gmail.com**. Было: auth.json/API key слетели → Authentication required; на телефоне Cloud + No Computers, CursorDocs=ПК Disconnected (icloud).
Фикс: восстановил `~/.config/cursor/auth.json` + `CURSOR_API_KEY` в `cursor-worker.env`; enroll google-oauth2; `desktopBridge=true`; RC cloud ON.
Телефон: Runtime → **Документы на Pi5**, репо `mishock/pi5-documents`. ПК icloud отдельно.

## ESP BMC — модуль MCP2515 (14:51, 2026-10-21)

На стенде и в машине у пользователя **MCP2515**, не синий TJA1050-only. Прошивка: `gem_bmc_esp32c3_v0.4.2_MCP2515.bin` / `ENV=esp32c3_can_min_mcp bash scripts/flash-can-min.sh`.

## ESP32-C3 MIN v0.4.1 — P1820 (14:09, 2026-10-21)

**524254 31 = P1820** checksum Traction Battery Status (`0CFF0EF3`). Фикс: стабильный EF3 + XOR; `0CFF10F3` AE→AF. Релизы `gem_bmc_esp32c3_v0.4.1_{TJA1050,MCP2515}.bin`. **Не прошито** — ESP не на USB.

## Фокус (13:03, 2026-10-21) — Deye Ак-Як 33: шаблон ЭЛЬТАВР записан

**INV** `2607253382` · logger `1538096135` · plant `62828303` Online.
**Записано и перечитано:** Batt-V **235 Ah** (факт на объекте) · Float 55 / Absorb 56 / EQ 56 · заряд 100 A / разряд 140 A · Activate OFF · Grid Charge 50 A · Gen Start 48 V / 40 A · Gen Force OFF · Low Power + MPPT ON.
**Grid Start 52 V:** enable выкл (как в шаблоне) — 00E4 остаётся 49 В.
**Заметка:** `…/notes/DEYE_CLOUD_AK_YAK_33_НАСТРОЙКИ.md`.

## Фокус (10:14, 2026-10-21) — Deye Cloud Ак-Як 33

**Аккаунт:** mishock24@gmail.com · станция **Simferopol Ak-Yak 33** · plantId **62828303** · 6.6 kWp · **Online**.
**Привязано:** Wi‑Fi logger **1538096135** (Auto-adding). Инвертор **2607253382**.
**Заметка:** `Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/DEYE_CLOUD_AK_YAK_33.md`.

## Фокус (15:57, 2026-10-20) — Deye ГУ: заряд только с Gen Force

**Причина:** без Force Deye берёт GEN только если АКБ ≤ **Gen Start**. Start низкий → заряд «только с Force».
**Фикс:** поднять Start выше текущего В АКБ **или** Force ВКЛ на время ручного ГУ.
**PDF обновлён:** `…/generated/НАСТРОЙКА_ГЕНЕРАТОРА_Deye6.6K_Load_и_заряд_АКБ.pdf` (§6 FAQ).

## Фокус (15:19, 2026-10-20) — Deye 6.6: PDF настройки ГУ

**Сценарий:** ГУ → Load + заряд АКБ; стоп заряда без отключения ГУ.
**PDF:** `…/generated/НАСТРОЙКА_ГЕНЕРАТОРА_Deye6.6K_Load_и_заряд_АКБ.pdf`.

## Фокус (13:46, 2026-10-20) — Must неисправный → PDF для СЦ

**Drive:** «Неисправный инвертор Must» (`1yqfe13z8Le_DgJHst6iGThGPQWp0O0Gj`).
**Видео:** `IMG_3651.MOV` — не стартует; сеть+нагрузка+АКБ; без PV/ГУ; мигает LCD; запах гари; ПК/USB не коннектится.
**Модель:** PV18-4024 PRO II · S/N **009000001400028**.
**PDF:** `Описание_неисправности_Must_PV18-4024_PRO_II_для_СЦ.pdf` на Drive (`1P7DXwD7ohhhCwGMqhojVS0JJJrKQiYIp`) и локально `…/Must_PV18-4024_PRO_II/notes/service_fault_2026-10-20/`.

## Фокус (11:18, 2026-10-20) — Must PV18-4024 USB

**Симптом:** не включается, LCD мигает; USB к Pi 5.
**Pi:** CH340 `1a86:7523` → `/dev/ttyUSB0` (с 11:08), порт свободен.
**Modbus:** нет ответа (все baud/slave) — MCU не отвечает.
**Вывод:** USB на Pi в порядке; старт — BAT 24 V + ON/OFF; при 14=Li без BMS на COM — мигает иконка АКБ → USE.
**Заметка:** `Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/notes/USB_DIAG_2026-10-20.md`.

## Фокус (18:08, 2026-10-19) — Клиент 3 Deye + БК

**Drive:** «Видео от клиента 3» (`1YY1IBnegnfZ8-H9vrZnHHqul4aQAfclq`).
**Голос:** 8 дней на сети; Deye «залил» в АКБ ~8–10 кВт·ч при ~100 Вт разряда; по BMS никто не греется; то же на стенде в синем цеху (~50 Вт).
**Фото:** АКБ ЭЛЬТАВР 99 % / 54 В ок; Deye заряжено ~9,3 / разряжено ~0,3 кВт·ч.
**Делать:** сверить ток Deye vs JK; выкл/лимит Grid Charge при полном; не менять БК без замера.
**Локально:** `…/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/client3_2026-10-19/`.

## Фокус (13:25, 2026-10-18) — Клиент 2 Deye F56

**Drive:** «Видео и фото клиента 2» (`1qLf6JiXp_0zc5Tz9LWPzJQUbCh_aDCff`).
**Проблема:** без сети F56; на Deye АКБ 30,1/0/9 В при JK 53 В 96 %. С сетью работает.
**Делать:** замер BAT-клемм vs BMS, DC автомат/кабели, Discharge MOS JK, пороги Shutdown; сброс через сеть+заряд.
**Локально:** `…/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/client2_2026-10-18/`.

## Фокус (12:56, 2026-10-18) — Deye 6.6 + генератор, видео клиента

**Drive:** папка «Видео от клиента» (`1emZ3rj2TDzz3ft_4m223aRtr7_Z6YnIp`), файл `8819367418405371637.MP4`.
**Суть:** на LCD был **SmartLoad Output** — поэтому ГУ не на дисплее. Нужно **Generator Input**, выкл SmartLoad; **Gen Charge** в Batt Set2; **Gen connect to grid input** выкл, если ГУ на клеммах GEN.
**Локально:** `Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/video_client_2026-10-18/`.

## Фокус (15:33, 2026-10-16) — Target Unavailable на телефоне

**Причина:** переключение runtime у Cloud-агента на другой репо. Worker только `mishock/pi5-documents`.
**Сделано:** репо создан/запушен public; worker online; debug видит «Документы на Pi5».
**Как с телефона:** новый агент → repo `mishock/pi5-documents` → машина «Документы на Pi5».

## Фокус (15:19, 2026-10-16) — Remote Control ON

**Сделано:** облако `remoteControlEnabled=true`, `allowPrivateWorkers=true`; enroll auth0; desktopBridge=true; worker `Документы на Pi5` online.
**Проверено:** `systemctl --user is-active cursor-self-hosted-worker cursor-redsocks` → active; Private worker started.
**Телефон:** Cursor app / cursor.com/agents → worker «Документы на Pi5». Окно Agents на Pi5 не закрывать.
**Док:** `REMOTE_CONTROL.md`

## Фокус (12:24, 2026-10-12) — Adion, русский мануал

Русское руководство Adion Expert 6 kW Twin возвращено: `Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/downloads/ADION_AXPERT_KING_II_6.0kW_TWIN-B_manual_RU.pdf`. Байтный дубликат EN удалён.

## Фокус (18:11, 2026-10-13) — Camera E1 мануал в базе

Официальный PDF V7 + `TECH_SUMMARY.md` (угол обзора 101° диагональ; гориз/верт не в мануале): `Платы и модули/Aqara_Camera_E1_CH-C01E/`.

## Фокус (11:27, 2026-10-12) — Camera E1 жива

Ребут был из-за BL616: на USB то был, то нет. Пользователь прогрел модуль паяльной станцией, камера в сети `10.1.30.56` (`Camera-E1-E147`), прошивка по-прежнему 4.0.2. `bms-serial-ws` всё ещё disabled, пока UART камеры на `/dev/ttyUSB0`.

## Фокус (09:20, 2026-10-12) — Camera E1, ребут из-за Wi‑Fi

CH-C01E: USB-порт пустой, чип Bouffalo не виден, `wlan0` нет, `blevent` делает `reboot -f`. Карта с OTA видна, до прошивки не доходит. Питание по наклейке 5 В / 2 А. `bms-serial-ws` всё ещё disabled. Заметка: `Платы и модули/Aqara_Camera_E1_CH-C01E/notes/UART_BOOTLOOP_2026-10-12.md`.

## Фокус (09:05, 2026-10-12) — прошивка E1 на флешке

На `AQE1OTA` (`/dev/sda1`, снята) лежит OTA `lumi.camera.acn006` 4.5.20_0020, `ota.bin`, MD5 `a22216a432d80e2b0b5b89872be1e088`. Камера видит только microSD, автопрошивки в `fw_manager.sh` нет. Копия: `Платы и модули/Aqara_Camera_E1_CH-C01E/downloads/`.

## Фокус (08:55, 2026-10-12) — Camera E1 UART

CH-C01E на `/dev/ttyUSB0` 115200 сама ребутится: `entry_facmd=true` → `reboot`, цикл ~20 с. U-Boot без паузы, login нет. `bms-serial-ws` снят с этого порта (disabled). Заметка: `Платы и модули/Aqara_Camera_E1_CH-C01E/notes/UART_BOOTLOOP_2026-10-12.md`. Снять флаг можно только кнопкой сброса на камере или прошивкой.

## Фокус (14:20, 2026-10-06) — Коммуналка: тарифы
- Сделано: «Тариф» + мини-график истории тарифов на 5 карточках (`Проекты/komunalka/tariffs.js`, `data/tariffs.json`, `GET /api/tariffs`, рендер SVG в `app.js`).
- Проверено: API по 5 службам, графики в браузере `http://10.1.30.126:8000/`.
- Осталось: при желании — таймаут voda 120→180 с (первый прогон 94 с).

## Фокус (12:45, 2026-09-30) — карты файлов BMS

В каждой папке BMS теперь `README.md` «что где лежит» (ANT, PB, B2A); в стандарт модуля §5.1 добавлен README.md-карта — делать для всех новых модулей.

## Фокус (12:35, 2026-09-30) — папка BMS + ANT

Новая группа `Платы и модули/BMS/` (индекс `README.md`): перенесены `JK_PB1A16S10P`, `JK_B2A20S20P`, новая `ANT_BMS_16ZNJ6-16S-130A` (этикетка SN 8XGALATH3863M66R, TTL/BLE; spec ANT16S + схема 16S, 8 картинок, esphome-ant-bms @87d89bd, PINOUT/TECH_SUMMARY/INSTANCE). У ANT нет DRY и нагрева. Пути в правилах (module-docs-priority §5, separate-folder-per-topic «BMS»), chat/HANDOFF и перекрёстных .md обновлены. `bms-tools/` не переносил — из неё работает `ant24c-logger.service`. Осталось: BLE-имя/версия ANT из приложения, скорость TTL (19200/9600).

## Фокус (12:20, 2026-09-30) — подогрев через ESP32

**У B2A20S20P нет HT−** (пользователь). Сделан ESPHome-термостат: `Платы и модули/BMS/JK_B2A20S20P/firmware/esphome_heater/` (`jk-heater.yaml`, `build.sh`, README). ESP32-S3 читает BMS по UART P5 (GPIO43/44), GPIO6 → DC-SSR ≥100 В; нагреватель B+ → предохр. → термовыкл. → нагреватель → SSR → **P−**. Логика: min(T1,T2)<старт 3 °C → вкл, ≥стоп 10 °C → выкл; SOC≥30 %; T≥20 °C / нет данных 30 с → выкл; лимит 3 ч + пауза 30 мин; веб-страница с порогами. Сборка Docker ESPHome 2026.9.1 — OK (RAM 29,7 %, Flash 10,2 %), кэш `~/.cache/esphome-docker`. **Не прошито** (S3 занят GEM). Осталось: купить SSR/DC-DC/нагреватель, прошить, тест.

## Фокус (12:20, 2026-09-30)

**Подогрев АКБ через JK BMS:** `Платы и модули/BMS/JK_B2A20S20P/notes/HEATING.md` (+ схема `pic/heating_wiring_B-series_JK_guide_p3.png`). HT− → нагреватель 48 В → NC-термовыключатель → предохранитель 10 А → B+; ≤7 А (200 Вт ≈ 14,6 Ом); пороги LiFePO4 +2/+5 заряд, нагрев +3…5/+10. Нагрев стартует только при холоде + зарядке. У B2A опция H под вопросом (оранжевый провод); у PB1A16S10P штатно P10. Ссылки добавлены в PINOUT обеих. Осталось: проверить провод HT−, версию прошивки, ёмкость/S пакета.

## Фокус (12:10, 2026-09-30)

**JK-B2A20S20P — фото торца:** ревизия V19 (мануал `downloads/manuals/JK-B2AxxS-15P-20P-User-Manual-V19.1.1.pdf`), порты CAN&RS485/UART/显示屏/并联/报警. **Реле — через P8 报警** (активный выход пищалки, 1 GND / 2 VCC, напряжение не документировано → замерить, реле через оптрон). PINOUT/TECH_SUMMARY/INSTANCE переписаны. PB1A16S10P: номинал DRY 30 В / 1 А добавлен в PINOUT. Осталось: замер P8 при тревоге.

## Фокус (11:45, 2026-09-30)

**JK-B2A20S20P:** новая папка `Платы и модули/BMS/JK_B2A20S20P/` (этикетка SN 605146M2D000705, мануал B-серии, протоколы UART/BLE/CAN, 4 картинки, PINOUT, TECH_SUMMARY, notes/INSTANCE). Вывод: у B-серии **нет сухих контактов**; реле — только P7 HT− (если есть опция нагрева) или ESP32/Pi по UART P5 / BLE. У PB1A16S10P реле через DRY (2 канала). Осталось: фото торца платы (есть ли P4/P7), версия из приложения. **11:50:** сохранён `syssi/esphome-jk-bms` @6a59290 → `…/JK_B2A20S20P/extracted/esphome-jk-bms-main-6a59290/` (памятка `notes/ESPHOME_JK_BMS.md`); дубли `downloads/protocols` и zip удалены, ссылки → `extracted/…/docs/`.

## Фокус (10:30)

**GEM BMC на ESP32-S3-RS485-CAN v0.2.1 (BLE+Wi‑Fi, captive portal — веб проверен с iPhone):** `Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/` — env по умолчанию `esp32s3_rs485can`: CAN v4 + реле + BLE к ANT-BLE24C (живой SOC в 0CFF0EF3; нет BMS — hold 15 с → 100 %) + SoftAP `GEM-BMC` 192.168.4.1 + USB-консоль mac/proto/status; запасная `_min` v0.1.1 без радио. Прошито и проверено на столе: SOC 81 % с BMS, failover hold→emul→ANT OK, 141 TX/с gap 10 мс. README/PINOUT переписаны. Фиксы: свежесть BLE ≤5 с (было ~30 с до 100 %), веб показывает то, что в CAN, interlock pull-down + init до реле. Не проверено: машина.

## Фокус (10:15)

**ESP32-S3-RS485-CAN перенесён:** `Проекты/ESP32-S3-RS485-CAN/` → `Платы и модули/ESP32-S3-RS485-CAN/` (Docker, scripts, firmware рядом с документацией). `.dockerignore` исключает downloads/pic/notes. Проверено: compose build (кэш), `pio.sh run` SUCCESS, esptool `flash_id` из контейнера по `/dev/ttyACM0` OK. Плата ещё **не прошита** board_test.

## ESP32-C3 BMC emu → TJA1050 (10:00, 2026-09-30)

**MIN v0.4.0 / full v0.7.0:** CAN через встроенный TWAI + TJA1050: VCC 5V, TX→GPIO4, RX→делитель 1k/2k→GPIO5 (C3 не 5V-tolerant). `include/can_gem.h` — выбор драйвера; MCP2515 = env `*_mcp`. releases: `gem_bmc_esp32c3_v0.4.0_TJA1050.bin` + `_MCP2515.bin` (остальное удалено). **Не прошито** — ESP не подключена: `bash …/gem_bmc_can_emu_esp32c3/scripts/flash-can-min.sh`.

## Фокус (09:41, 2026-09-30)

**H503 BMC emu v4.3.0 — TJA1050:** VCC 5V, TX→B7, RX→B8 (FT). Исправлен баг: после секунды TX-ошибок loop() навсегда останавливал CAN+interlock. Bus-off recovery, RX-диаг. Бинарь `…/gem_bmc_can_emu_h503/releases/gem_bmc_can_emu_h503_v4.3.0.bin`. **Прошито** 09:45; TX/RX переставлены — снифер подтвердил, кадры идут (09:53).

## Фокус (29.09)

**Клиент Мирное:** `Проекты/Мирное_Никольская_10/` — адрес с. Мирное ул. Никольская 10; инвертор SUN-20K SN **2607224129**; АКБ RW-F16; блокнот `notes/БЛОКНОТ.md`; Solarman Pro — collector SN дописать.

## Фокус (29.09, 3x)

**Deye 3× RW-F16 — отдельный PDF:** `Платы и модули/Солнечные_инверторы/Deye_RW-F16/generated/Deye_SUN-20K_3xRW-F16_Installation_Setup_RU.pdf` (7 стр.; №1+№2 → узел → BAT1, №3 → BAT2; связь PCS №1→BMS, OUT→IN №1–№2–№3; 942 Ah, Max A 300 А, потолок 350 А). Генератор общий для 2x/3x: `Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_rwf16_system_pdf.py` (старый `generate_2x_rwf16_pdf.py` удалён). 2x PDF не изменился по смыслу. Проверено визуально pdftoppm.

## Фокус (08:07, 29.09)

**Deye 2× RW-F16 — один PDF:** `Платы и модули/Солнечные_инверторы/Deye_RW-F16/generated/Deye_SUN-20K_2xRW-F16_Installation_Setup_RU.pdf` (7 стр.: блок ОБЯЗАТЕЛЬНО связь PCS→BMS инвертора / OUT→IN, схема, монтаж, меню §5, запуск, чек-лист, ошибки). Удалены отдельные Menu_Settings 2x, общий RW-F16 PDF, Full_System_Guide 2x (был 320 А). Генератор один: `Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_2x_rwf16_pdf.py`.

## Фокус (16:15)

**HA Pi3 «Loading data»:** HA и сеть Pi5↔Pi3 в норме; NetBird ПК `komputer-252-19` (0.71.2) ↔ Pi3 (0.79.0) флапает раз в 1–2 с (с 03.09, тысячи в сутки), relay не поднимается. Обход: прокси `http://10.1.30.126:8124` → HA Pi3 (`pi3-ha-proxy.service`, user). Настоящий фикс — обновить NetBird на ПК.

## Фокус (16:00)

**Графики HA без игл (Pi5 + Pi3):** CPU — сглаживание в `publish_cpu_temp.sh` (EMA + мёртвая зона 1 °C, `LC_ALL=C`) и оси 20–85 °C; Pi3 — Bybit без нулей (`availability`), ось среднего расхода от 0. HA Pi3 проверен: API OK, ворота/реле/счётчик на месте; недоступные `pi3_undervoltage*` — сироты реестра с июля. Бэкап Pi3: `~/backups/graphs-20260928/`.

## Фокус (15:50)

**Pi5 HA ANT BMS24C — иглы на графиках:** дребезг BMS (54.0↔54.1 В, 83↔84 %, шум тока ±0.3 А) на автошкале. В `packages/ant24c.yaml` мёртвая зона у `*_graph`, в `dashboards/ant-bms-24c.yaml` фиксированные оси (46–55 В, ±10 А, 0–100 %). HA перезапущен, конфиг валиден.

## Фокус (13:53)

**Deye RW-F16 `generated/` → 2 АКБ:** новые PDF `Deye_SUN-20K_2xRW-F16_Installation_Setup_RU.pdf` (схема №1→BAT1, №2→BAT2, BMS PCS№1→инвертор, OUT№1→IN№2; 6 стр.) и `..._Menu_Settings_RU.pdf` (628 Ah, Mode 00, Max A 240 А, потолок 250 А = 2×автомат 125 А). Генераторы в `Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_{2x_rwf16,menu_settings_2x}_pdf.py`. 3x-копия убрана из RW-F16/generated (оригинал в SUN-20K/generated). Осталось: старый `..._2xRW-F16_Full_System_Guide_RU.pdf` советует 320 А — расходится; на Drive не заливал.

## Фокус (13:35)

**Pi3 HA электросчётчик гаража:** «пила» на графике — `initial: 59.21` сбрасывал значение при каждом рестарте HA, ввод из UI не шёл в CSV. Убран `initial`, автоматизация UI→CSV (комп/телефон), синхронизация при старте, валидация опечаток, CSV восстановлен (последнее 25.09 = 87.05), история БД выровнена. Бэкап Pi3: `~/backups/garage-meter-20260928/`.

## Фокус (08:50)

**PlatformIO в Docker:** `Проекты/ESP32-S3-RS485-CAN/` — образ `esp32-s3-rs485-can-pio` (PIO 6.1.19, espressif32 7.0.1 в образе), `scripts/pio.sh|flash.sh|monitor.sh|detect.sh`, прошивка `firmware/board_test` (CAN listen-only 250k, RS485 9600, RTC). Сборка OK (S3 и чужой C3 через `-d`). Сеть host (bridge вешал загрузки). Прошивка по USB не проверена — платы нет на USB.

## Фокус (08:30)

**Модуль ESP32-S3-RS485-CAN (Waveshare):** папка `Платы и модули/ESP32-S3-RS485-CAN/` — схема, демо (распаковано), даташиты ESP32-S3, 10 картинок, `PINOUT.md` (GPIO из таблицы схемы: CAN 15/16, RS485 17/18/EN21, RTC I2C 38/39 INT40), `TECH_SUMMARY.md`. Добавлен в список §5 `module-docs-priority.mdc`.

## Фокус (20:50)

**Pi3 HA + switch (без INMP441):** восстановлены все 6 реле CH3…CH8 в `switch/app/config.py`; I2S/inmp441-dmic отключены в boot; switch Up, HomeKit `10.0.20.56:51826`; HA `switch.vykliuchatel_3…8`, `cover.vorota`, `camera.garage_camera`. S3 камера unavailable (офлайн).

## Фокус (17:55)

**VIN `19B04000LSE012`:** по «Учет работ» — NMC-сдвоенная Сочи рефрижиратор; АКБ **300 А·ч**, зарядка **40 А**. Точный вольтаж в Google Sheets **не указан**; мануал Як: силовая **72–110 В**, борт **12 В**.

## Фокус (17:50)

**eltavr-bot «Поиск по VIN»:** молчал из‑за зависания polling (CLOSE-WAIT к xray 10809 после 502). Перезапуск обработал очередь; VIN `19B04000LSE012` → Як-К / NMC Сочи. В `bot.py` — pool/timeouts + автопоиск VIN.

## Фокус (14:55)

**Hyperion EOS 0606i:** прошивка **недоступна** (только NET/DUO). На USB — **LAWICEL CANUSB** (`ttyUSB0`, SN LW0GQ135), не кабель Data Port. Док: `Платы и модули/Hyperion_EOS_0606i/`.

## Фокус (10:48)

**krimsvet.ru починен:** `/favicon.ico` 200; иконки вместо 1MB-баннеров; в `bundles.json` телефон `+79789858707` (как на сайте). Правки залиты по FTP на REG.RU `www/krimsvet.ru/`.

## Фокус (10:39)

**krimsvet.ru:** сайт **работает** (HTTP 200, nginx на REG.RU `37.140.192.181`). SSL до 2027-01-17. Статика `styles.css`/`app.js` OK. Локальной папки проекта в `Documents/Проекты` не найдено (деплой на хостинге с 2026-07-02).

## Фокус (15:15)

**M350 CNC Controller** на eth0 Pi 5: IP `192.168.31.99`, SMB1 шары `CNCDISK`/`SYSDISK`. Документация: `Платы и модули/M350_CNC_Controller/`. На шаре есть `ELTAVR_CNC/AKB`.

## Фокус (10:45)

**Солнечные панели:** создана `Платы и модули/Солнечные_инверторы/Солнечные_панели/` — Trina **TSM-NED9R.28** (445–470 Вт) и Jinko **JKM605-630N-66HL4M-BDV** (605–630 Вт); даташиты переименованы в `downloads/`, сводки в `TECH_SUMMARY.md`. Дубликат Jinko (одинаковый md5) не копировался.

## Фокус (10:01)

**Диск Pi5:** NVMe 117G → **86G занято (77%)**, свободно **~26G**. Не критично. Главное: Cursor snapshots (~6G server + ~1.6G config), `.cursor-server` 7.7G, Docker ~8G, кэши ~5G (playwright 1.9G), toolchain Arduino/PIO/Gradle/Codex. Журналы ОК (~196M).

## Фокус (15:30)

**Deye 6× SUN-6.6K:** грид не шёл без кода — **перепутаны фазы L2↔L3** vs B/C на LCD. После обмена фаз 2 и 3 — заработало. Роли Master 1/3/5, Slave 2/4/6 были верные.

## Фокус (14:29)

**Deye 6× SUN-6.6K (2 на фазу):** U на LCD ≠ замыкание Grid. Чеклист: Master+Slave на каждой фазе, угол=физика L1/L2/L3, DIP ON×6, SN 01–06, Grid Type Single Phase 230 V / 50 Hz, коды F29/F35/F41/F42/F47/F48. Док: `…/Deye_SUN-6.6K-OG03LP1-EU-AM2/РУКОВОДСТВО_RU.md` §5.4.

## Фокус (16:23)

**CAN лог power_cycle:** 2 OFF VCM (~9 с @+59, ~12 с @+175). **BMC ESP (EF3) рвётся раньше VCM** → машина гаснет. Питать ESP стабильно 5 В. `notes/CAN_POWER_CYCLE_20260918.md`.

## Фокус (15:56)

**520545 / 520546 / 520549 FMI4** остались — это **поворотники + CHMSL** (VCM), не CAN BMC. 520553 (reverse) ушёл. Дальше: Clear DTC + 12 В aux / K5·K12·лампы. Note: `notes/DTC_520545_520546_520549_LIGHTS.md`.

## Фокус (15:53)

**DTC 520553/520545/520546/520549 FMI4** = лампы (reverse/turn/CHMSL) Voltage Low — не CAN-счётчики BMC. Часто от просадки 12 В при ребуте ESP/реле. **MIN v0.3.2:** реле сразу ON, CAN через 1.5 с. Стереть DTC после KEY OFF→ON.

## Фокус (15:48)

**ESP MIN v0.3.1:** CAN + реле X3 (K5/K12/VCM, K7←interlock), **без BLE/Wi‑Fi**. Бин `releases/gem_bmc_can_min_esp32c3_v0.3.1.bin`.

## Фокус (15:45)

**ESP MIN v0.3.0:** тупо CAN-эмулятор — без BLE/Wi‑Fi/реле. Env `esp32c3_can_min` (default). TX **141/с fail=0**. Бин: `firmware/.../releases/gem_bmc_can_min_esp32c3_v0.3.0.bin`. Flash: `scripts/flash-can-min.sh`.

## Фокус (15:40)

**ESP v0.6.14:** машина гасла — ESP **ребутилась** (USB over-current/disconnect) + MCP TX залипал. Фикс: TX watchdog, soft recover, SPI 4МГц; на Pi — udev против ModemManager. **Питать ESP не от слабого USB.**

## Фокус (15:18)

**ESP v0.6.13:** DTC **524273 31 / 524237 31** = P1824/P1827. Фикс: не пропускать слоты счётчиков; SoftAP выкл; EF3 = pure v4. Проверить на машине: OFF→ON, стереть DTC.

## Фокус (15:07)

**ESP BMC v0.6.12:** `ANT_BLE_ENABLE=0` — скан/коннект к BMS выкл; CAN эмуляция 100%+54V; SoftAP/реле остаются. Бин меньше (~816 KB). Flash baud 115200. Включить BLE позже: `-DANT_BLE_ENABLE=1`.

## Фокус (14:57)

**ESP BMC v0.6.11:** ошибки на приборке — не ребут, а **блокирующий BLE-скан** (~6 с тишины CAN) + пачка 4×100ms в 3 TXB. Фикс: async scan, CAN FreeRTOS prio=5, фазы 100ms, Serial из loop. Smoke: TX **141/с fail=0 gapMax=10ms**. Бин: `firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.11.bin`. На машине — сбросить DTC/ключ OFF-ON и проверить приборку.

## Фокус (13:17)

**Диск Pi5:** NVMe 117G → **95G занято (86%)**, свободно ~17G. Главное: Cursor snapshots (~11G + ~6G), `.cursor-server` 9.2G, toolchain (Arduino/PIO/Gradle/Codex), кэши. Docker ~8–14G, журналы в норме (~191M).

## Фокус (11:58)

**Перепроверка v0.6.10:** ESP CAN FAIL=0, эмуляция 100%/54V OK; с MAC 92 — ANT 96%. HA `ant24c-logger` active, но Classic `91:23:45` сейчас **не в эфире** (Host down) — BLE `92:23:45` виден. Сервисы подняты, ждут Classic.

## Фокус (11:06)

**ESP v0.6.10:** без BMS эмуляция **SOC=100% + U=54.0 В + I=0** в EF3 (hold 15 с после обрыва). HA logger active.

## Фокус (10:59)

**HA ANT logger возвращён:** `ant24c-rfcomm` + `ant24c-logger` active (MAC `AA:BB:CC:91:23:45`). ESP от BMS отключён.

## Фокус (10:50)

**ESP v0.6.9:** оба протокола ANT — **legacy** (DBDB) / **modern** (7EA1) / **auto**; выбор в SoftAP http://192.168.4.1/ (NVS). Smoke: proto=legacy, SOC=96% ANT, TX fail=0.

## Фокус (10:45)

**ESP BMC v0.6.8 — безотказность подтверждена:** soak 55с+120с PASS; TX ok≈113/s fail=0; ANT BLE без disconnect; SOC=96% U=54.0V в EF3; reinit/ALLTXBUSY=0. Pi `ant24c-logger` всё ещё stopped (эксклюзив BLE). Артефакт: `firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.8.bin`.

## Фокус (10:35)

**ESP v0.6.7:** в CAN `0CFF0EF3` подмешиваются живые **U/I/SOC** с ANT (byte0 SOC, b2–3 ток от 0x048E, b4–5 U мВ BE, b7 XOR). Карта: `notes/CAN_BUS_MAP.md`. Проверить на приборке GEM.

## Фокус (10:22)

**ESP ANT BLE починен (v0.6.6):** причина — слали modern `7E A1`, а ANT-BLE24C отвечает на legacy `DB DB` → `AA 55 AA FF` (как HA `ant24c_logger`). Serial: `SOC=96% ANT`, U=54.0V. Pi logger всё ещё **stopped**. Вернуть: `sudo systemctl start ant24c-rfcomm ant24c-logger`.

## Фокус (14:57)

**ESP32-C3 + MCP2515:** пользователь подтвердил — **CAN работает** (v0.6.0). Эталон для BMC SA=0xF3 @250k.

## Фокус (12:37)

**Deye F41:** при 3ф по 1 шт. на фазу — **Master на всех трёх** (A/B/C), не Slave на №2/№3. PDF обновлён.

## Фокус (10:32)

**Deye 3ф × 3:** PDF чеклист LCD — `Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/LCD_НАСТРОЙКА_3Ф_3шт.pdf` (№1 Master A/01, №2 Slave B/02, №3 Slave C/03).

## Фокус (10:36)

**ESP32-C3 BMC:** CAN **MCP2515 SPI** вместо TWAI/VP230. Собрано **v0.6.0** / can_min **v0.2.0**. Пины: SCK4 MISO5 MOSI6 CS7. ESP в USB сейчас нет — прошить после подключения.

## Фокус (10:00)

**Uno + CAN Shield:** `gem_bmc_can_emu` прошит. MCP2515 **CS=D10**, кварц **16 МГц** (не D9 — пад/клон). Serial: `MCP2515 OK`. Снифер @250k → `0CFF0EF3` (через ~3 с после старта).

## Фокус (09:58)

**Uno + CAN-BUS Shield V1.2:** `gem_bmc_can_emu` прошит (CS=**D9**, `MCP_16MHZ`, 250k). Снифер → `0CFF0EF3`.

## Фокус (09:49)

**H503 v4.2.2 прошита** (ST-Link, OpenOCD `halt`+write; dump==bin). Снифер @250k → `0CFF0EF3`. Питание SWD ~2.87 V — лучше дать стабильные 3.3 V.

## Фокус (09:43)

**H503 BMC emu:** тишина на снифере — баг прошивки: FDCAN kernel default **HSE (выкл)** + NBTP не под 50 МГц. Фикс **v4.2.2** (PLL1Q + 250k) собран → `releases/gem_bmc_can_emu_h503_v4.2.2.bin`. Нужна перепрошивка.

## Фокус (16:44)

**Снифер тишина:** ESP `can_simple` **TX ok≈10/s**, но **RX=0** — свой кадр через CRX не приходит → проблема **VP230/CANH-L/GND/120Ω/CRX**, не софт снифера. Sniffer переведён на **MCP_8MHZ** (перепрошить Uno).

## Фокус (16:40)

**ESP can_simple:** простой генератор `0x18FFE001` @250k NO_ACK, 10 Гц, payload SEQ+DEADBEEF. Serial: TX ok≈10/s. Снифер: искать этот ID.

## Фокус (16:11)

**CAN_Sniffer:** не ловил шину — mcp_can после `begin()` в **LOOPBACK**. Фикс: `setMode(MCP_NORMAL)`, прошито. Дефолт 250k.

## Фокус (16:06)

**CAN_Sniffer_Shield_LCD:** дефолт **250 kbps**; собрано и прошито на Uno `/dev/ttyACM0`. Backup `20260916T160625`.

## Фокус (14:36)
ESP **v0.5.0 NORMAL** (CAN v4=Pi + реле). Bench NO_ACK снят — он мог глушить шину/приборку.

## Фокус (14:20)
Стенд Pi↔ESP: прошивка **v0.4.1-bench NO_ACK**, can0 250k. F3 на can0 пока нет — нужна проводка CANH/CANL/GND. Монитор: `ai-tmux log esp-f3-watch`.

## Фокус (14:09)
ESP BMC **v0.4.0** прошит: CAN = Pi v4 + реле X3 (GPIO0/1/2/3, interlock GPIO10). На шине F3 пока нет — TWAI TX без ACK (SN65).

## Фокус (14:02)
ESP32-C3 GEM BMC: код v4 = H503/Pi (EF3 идентичен). На дисплее 0% — **кадры F3 не на шине**: Serial `TWAI TX fails`, candump F3=0. Прошивка **v0.3.7** (пины TX=4 RX=5). Нужна проводка SN65 (CTX/CRX/CANH/L/GND/3V3).


## Фокус (2026-09-16)

**SILA VM II 6.2K — 13S применён:** через i.Solar `setParam` (SN `96342504111477`): C.V/Float **54.0**, Re-Discharge **53.0**, Under **42**, EQ **выкл**, EQV **54.0**, MCG **10 A**. Скрипт `…/SILA_VM_II_Premium_Plus_6.2K/scripts/isolar-apply-13s.sh`.

## Фокус (2026-09-16)

**SILA VM II Premium+ 6.2K** (SN `96342504111477`, i.Solar): АКБ **литий-ион 13S**. C.V **54.0** (или 54.6), Float **53.5–54.0**, Under **42–43**, EQ **выкл**. Старый снимок 56.4 — под LFP 16S, для 13S нельзя. Памятка: `Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/notes/USER_13S_LION_SETTINGS.md`.

## Фокус (2026-09-16)

**i.Solar / Adion Battery User — литий 13S:** C.V **54.0** (или 54.6), Float **53.5–54.0**, Under **42–43**, Re-Charge **46–47**, Re-Discharge **52–53**, equalization **выкл**. Текущие 56.4/58.4 — опасно. Памятка: `Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/notes/USER_13S_LION_SETTINGS.md`.

## Фокус (2026-09-15 15:59)

**Aqara CH-H01 3D65 — ЭТАЛОН:** всё ок. `flip=3` + сток `osd_orig`. Не трогать OSD-шрифты.

## Фокус (2026-09-15 15:41)

**Aqara CH-H01 3D65:** `flip=3` + сток OSD `osd_orig` — пользователь подтвердил, timestamp правильно. Шрифты не крутить.

## Фокус (2026-09-15 14:45)

**Aqara CH-H01 3D65:** timestamp OSD — **зеркало L↔R** (`osd_mirror`), `flip=3`. Картинка вверх ногами под подвес — ок.

## Фокус (2026-09-15 14:40)

**Aqara CH-H01 3D65:** камера будет **висеть вверх ногами**. `flip=3` + OSD `osd_flip180` (глифы). На столе картинка/дата вверх ногами — норма; после подвеса оба прямые. Live без VPN/Private Relay.

## Фокус (2026-09-14 21:28)

**USB VID/PID:** на Pi5 один внешний девайс — **LAWICEL CANUSB** `0403:6001`, SN `LW0GQ135` → `/dev/ttyUSB0`. Второго USB-UART (CH340/CP2102/другой FTDI) нет — это не адаптер CH-H01.

## Фокус (2026-09-14 21:26)

**USB «UART»:** пользователь сказал, что UART подключён постоянно. На Pi5 по факту только **LAWICEL CANUSB** (`0403:6001`, serial `LW0GQ135` → `/dev/ttyUSB0`). USB-UART камеры CH-H01 не виден. Job `aqara-motion-fix` мёртв. Камера `10.0.20.16` ping OK.

## Фокус (2026-09-14 21:24)

**Бот ЭЛЬТАВР (`Проекты/telegram_bot`):** после ребута Pi5 не отвечал — контейнер не был запущен; прямой Telegram TimedOut. Сейчас `eltavr-bot` Up, proxy `http://127.0.0.1:10809`, polling OK. Проверка: `docker ps --filter name=eltavr-bot`; `docker logs --tail 30 eltavr-bot`.

## Фокус (2026-09-14 21:14)

**Aqara CH-H01 motion:** на Pi5 сейчас только **LAWICEL CANUSB** (`/dev/ttyUSB0`). USB-UART камеры нет — `uart_wait_fix_motion` остановлен. Нужен USB-UART к камере + power-cycle, иначе patch по UART невозможен.

## Фокус (2026-09-14 21:09)

**Pi5 reboot:** по запросу пользователя (восстановление UART CH-H01). После бута oneshot `aqara-motion-resume-once` → `aqara-motion-fix` (bool patch + audio/motion). Проверка: `ai-tmux log aqara-motion-fix`.

## Фокус (2026-09-14)

**Aqara CH-H01 motion:** камера `10.0.20.16` пингуется, **UART shell мёртв**. В tmux `aqara-motion-fix` ждёт power-cycle → зальёт motion bool patch + `fix_audio_motion_config.sh`. В Home: Allow Recording / уведомления о движении. Скрипт: `Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/uart_wait_fix_motion.py`.


## Фокус (2026-09-12)

**Bybit:** live API через Tor на VPN_Server (US exit блокировал). Сервис `bybit-tor-tunnel`, helper `bybit-http.py`. Баланс ~61.4 USDT.

## Фокус (2026-09-10)

**Aqara G2H DC8B HomeKit:** `hap.dat.org` залит (1 МБ). QR наклейки `X-HM://00HERHL8OBE1X` → код `485-97-192`, setup ID **`BE1X`** (не WAXZ с EE74). UART сейчас без RX — скрипт `scripts/uart_fix_homekit_be1x.py --wait-boot --reboot` в tmux `aqara-be1x`. Нужен power-cycle камеры.

egram:** только пополнение / TP / успешный BUY (`notify_positive_only`).



## Фокус (2026-06-18)



**UFW Pi 5:** `restore-pi5-ufw.sh` + `pi5-restore-ufw.service`. ZeroTier удалён (2026-06-19): `purge-zerotier.sh`.



**Проект komunalka:** Экор — до 5 кнопок счетов с **датой периода** (метрика `Чеки`); сумма к оплате из выписки. Жилсервис — fetch-логин. Чеки всех карточек — даты на кнопках.



## Фокус (2026-06-17)



**Проект EDM:** создан каркас `Проекты/EDM/` — simple Python, Docker, venv. Проверка: `docker compose up -d --build` → `EDM: запущено в режиме dev`.



## Фокус (2026-06-10)



**Сайт ЭЛЬТАВР (`/home/pi/www`):** админка Payload переделана в тёмный NobleUI-стиль — `theme: dark`, `admin-theme.css`, `AdminDashboardWelcome`, `AdminHeaderBar`, `AdminQuic
## 2026-09-30 — komunalka: Крымэнерго + формат дат
- Сделано: таймаут прокси Сайты для komunalka 300 с (`Проекты/Cursor Agent/api/sites_proxy.py`); energy — главная→Оплаты→История с ожиданием таблицы, лимит 180 с; газ ISO-дата → ДД.ММ.ГГГГ (`Проекты/komunalka/server.js`).
- Проверено: 5 прогонов energy через https :8767 — показание 20930 (18.09.2026), платёж 29.09.2026, 5 чеков; газ 29.09.2026.
- Осталось: при повторе смотреть `journalctl --user -u komunalka | grep "\[energy\]"`.
- Жилсервис: ЛК обновляется раз в месяц (22.09.2026); парсим `/pages/oborotka` (cookie jar) → последняя оплата август 2026, 2856.84 ₽; поле «Данные ЛК на».

## 2026-10-01 — Deye 6.6K + АКБ ЭЛЬТАВР (JK-B2A20S20P): «SOC падает»
- Сделано: видео клиента (кадры + whisper) и `.jkcfg` разобраны; вывод — АКБ полная (3,44 В/яч на Float 55,0 В), 93 % на JK = уход кулонометра, SOC-100% 3,50 В не достигается; BMS↔Deye связи нет.
- Файлы: `Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/diag_2026-10-01_АКБ_SOC/`, `Платы и модули/BMS/JK_B2A20S20P/scripts/decode_jkcfg.py`, `…/notes/configs/*.jkcfg`.
- Осталось: клиенту выставить SOC-100% 3,43 В, проверить ток клещами, настройки Battery Setup Deye.
- 2026-10-01 доп.: шаблон настроек Deye 6.6K под АКБ ЭЛЬТАВР 230 Ач — `…/Deye_SUN-6.6K-OG03LP1-EU-AM2/generated/ШАБЛОН_НАСТРОЕК_Deye6.6K_АКБ_ЭЛЬТАВР_48V230Ah.pdf` (генератор `scripts/generate_battery_template_pdf.py`, 3 стр.).
- 2026-10-01 доп.: готовый `.jkcfg` для производства — `Платы и модули/BMS/JK_B2A20S20P/notes/configs/ELTAVR_48V230Ah_16S_template/20261001T105320-JK-B2A20S20P-19.34.jkcfg` (сборка `scripts/make_jkcfg.py`), копия в Загрузках ПК. Импорт в приложение JK ещё не проверен на живой BMS.

- 2026-10-01: HA ANT BMS24C — display_precision напряжений (пакет 1 знак, ячейки 3). Реестр + dashboards/ant-bms-24c.yaml. HA перезапущен, OK.
- 2026-10-01: HA card-mod 4.2.1 (www + extra_module_url); ANT «Сейчас» — разброс ячеек, красный >20 мВ.
- 2026-10-01: HA ANT «Ячейки» — max красный, min синий (font color в markdown).

- 2026-10-05 M350_CNC_Controller: прошивка V1 2024-12-12 → 2026-09-09 (бэкап backups/20261005_0837, slib-g.nc пользователя сохранён, rus/msg2 слиты), #141 3000→0. USB Wi-Fi RT5370 не поддерживается прошивкой — запрос FOINNC github issue #4; совет — Wi-Fi мост на Ethernet. См. notes/FIRMWARE_UPDATE_20261005.md
- 2026-10-05 M350: из FB-группы добавлены CAM-макросы cam20–35 (щуп Savelev ×8, обработка Al Tie ×8), параметры #1200–#1341; старые cam10–19 не тронуты; бэкап backups/20261005_cam_before; ждёт перезагрузки контроллера. См. notes/CAM_ADDONS_20261005.md
- 2026-10-05 M350: cam36 «Резьбофрезерование», cam37 «Выравнивание стола» (Н. Звягинцев, FB), параметры #1342–#1367; бэкап backups/20261005_cam36_before; свободны cam38–39; нужна перезагрузка контроллера.
- 2026-10-05 M350: #141 возвращён 3000 (подача XY к фикс. датчику в своём slib-g; утренний 0 был ошибкой). cam38 «Z0 щуп + датчик», cam39 «Калибровка щупа» (свои, scripts/cam_templates). #76=Нет → после перезагрузки поставить Да. Все слоты cam10–39 заняты.
- 2026-10-05 M350: cam10–19 заменены улучшенными макросами щупа (scripts/m350-cam10-19.py, симулятор m350-cam-sim.py 20/20 OK); старые в backups/20261005_my_cam10-19; нужна перезагрузка контроллера. См. notes/CAM10-19_NEW_20261005.md
- 2026-10-05 M350: ревизия CAM — исправлены и залиты cam20–27,32,33 (scripts/m350-cam-fix.py, сим `m350-cam-sim.py --fix` OK), оригиналы в backups/20261005_my_cam10-19; перезагрузка не нужна. notes/CAM_REVIEW_20261005.md
- 2026-10-05 M350: cam28,31–35 защита шаг Z=0, cam31–33 наклонное врезание; 30 новых картинок cam10–39.bmp (scripts/m350-cam-pics.py, старые backups/20261005_pics_before). Видны после перезагрузки контроллера.
- 2026-10-05 M350: медленный переезд к датчику длины из дальнего угла — в O502 `G53 … A B C` тащил ось B (ведомый Y, лимит #222=1000) к 0; заменено на `G91 G00 X[#10-#880] Y[#11-#881] F#641`, залито, cmp OK, бэкап backups/20261005_o502_before. Первая версия (+6 байт) сломала хоуминг Y (O503 после O502, смещения кэшируются при загрузке) — перезалито той же длины. Затем O9053 (все G53) — G00 без F и A/B/C, #63/#67/#68 2000→3000 (нужна перезагрузка). notes/O502_SLOW_TRAVEL_FIX_20261005.md
- 2026-10-05 M350: паспорт станка `Платы и модули/M350_CNC_Controller/MACHINE.md` (поле 296×433×133, двойной Y = 4-я ось «B», IN8 щуп, IN20 датчик длины, OUT18 обдув M176/M177).

- 2026-10-05 16:28 M350: выходы по фото/владельцу — OUT19 обдув датчика (M176, #789=19), OUT20 СОЖ+обдув (M8, #730=20; M3 #715=20 тоже); K1 = вкл/выкл OUT20 + LED #1944, K2 = OUT19 + LED #1945 — подтверждено. Параметры #789/#730 — после перезагрузки. Док: `Платы и модули/M350_CNC_Controller/MACHINE.md`.
- 2026-10-07: PDF шаблона BMS — `Платы и модули/BMS/JK_B2A20S20P/generated/ШАБЛОН_НАСТРОЕК_JK-B2A20S20P_АКБ_ЭЛЬТАВР_48V230Ah.pdf` (из самих .jkcfg, `scripts/generate_jk_template_pdf.py`).
- 2026-10-07: QR в PDF BMS → .jkcfg на Drive (публично по ссылке) `https://drive.google.com/uc?export=download&id=1KBDWBKG9-xKxeI-49krTs6hIi_DT1BET`; `scripts/upload_jkcfg_drive.py`, ID в `drive.json`. QR проверен zbar, скачивание без входа — md5 совпал.

- 2026-10-07: Hikvision DS-2CD2122FWD-IS — UART-консоль на Pi5 (/dev/ttyUSB0 115200, psh), камера OK, IP 192.168.1.64, нужен IP из 10.1.30.0/24. Док: `Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md`.
- 2026-10-07: Hikvision → IP 10.1.30.64 (статический, шлюз 10.1.30.1), веб/RTSP доступны.
- 2026-10-07: Hikvision прошита до V5.5.82 build 190909 (TFTP через загрузчик), IP 10.1.30.64, активирована в веб; пароль у пользователя — вписать в README.
- 2026-10-07: HA Pi5 — camera.elektrotsekh (Hikvision 10.1.30.64), добавлен stream:, карточка на «Обзор».
- 2026-10-07: HA камера электроцеха → интеграция Hikvision (+ binary_sensor.elektrotsekh_dvizhenie), push на iPhone (packages/hikvision_elektrotsekh.yaml), в мосту HomeKit «HASS Bridge» как камера с датчиком движения (снят exclude_accessory_mode). LED-табло исключено из зоны детекции.
- 2026-10-07: HA — ESP Camera (офис) убрана с главной и из кэша HomeKit Controller (скрипты pairing оставлены).
- 2026-10-08: Пушкина_29 — обращение + приложение 1: снос только **С1**; **С2 полностью исключён**; кирпичная клумба **П** — «(не трогать!)», параллельна дому и заканчивается на уровне **Д1**. Стойки бельевой сушилки под снос — **8 шт.**, новая между Т1 и О1. Обращение на 2 страницы; в таблице 12 жильцов, добавлена **Меджитова А.Н., кв. 10**, Аверина **Е.И.**; Drive sync OK.
- 2026-10-08: Пушкина_29 — схема двора по чертежу территории (ЗУ3, Д1–Д4, ЛЭП О1–О2). В обращении, схеме и названии приложения №2 используется формулировка «чертёж территории». Зеркало: `Проекты/drive-folder-sync/`, Drive `1Xd2ZT-t8eLIL6HVaHR4G-yjs-GOnuWbN`.

## 2026-10-26 — Пушкина_29 схема ЗУ3
- Приложение 1: вырез по **чёрному контуру** со скрина Paint (`notes/zu3_black_contour_guide_2026-10-26.jpg`).
- PDF обновлён, Drive sync OK. Плитка/асфальт пока не нанесены.
- Скрипт: `Пушкина_29/scripts/generate_coverage_scheme_pdf.py`

