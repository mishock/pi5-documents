## Фокус (2026-08-07, режим QR LiFePO4)

**Режим:** пользователь кидает код/фото QR ячейки → ответ с макс. характеристиками.
**Скрипт:** `Платы и модули/LiFePO4_Cell_QR_Decoder/scripts/decode_cell_qr.py`
**Сервисы:** Basen + Xiho (авто); Gobel/Hakadi — вручную/если доступны.

## Фокус (2026-08-07, Kali БК MFA)

**UI:** наружная t° (G2), ОЖ (G3), мгновенный/средний расход (Δ бака+одо), trip km/min.
**Проверено:** out 35°C, ОЖ 74°C, бак ~20 л; avg/inst — после движения.
**Файлы на Kali:** `~/Projects/cluster_pi/ui/{bc,obd_feed}.py`

## Фокус (2026-08-07, LiFePO4 QR)

**Папка:** `Платы и модули/LiFePO4_Cell_QR_Decoder/`.
**Пример:** `04QCB72JB8800JFCF0021605` → EVE LF230, 230Ач, 3.2В, 15.12.2025.
**Сервисы:** Gobel / Hakadi / Xiho (+ Basen API).

## Фокус (2026-08-07, Kali БК K-line)

**Диагноз:** KKL OK; приборка **0x17** live; двигатель **0x01 SIMOS** (B5/95) без measuring blocks.
**БК:** feed=`cluster`, tmux `bc`; формула k7=`0.01*a*b`.

## Фокус (2026-08-07, Kali БК запущен)

**Статус:** `ui/bc.py` запущен на Kali (tmux `bc`), DISPLAY=:0.
**Старт:** `bash ~/Projects/cluster_pi/scripts/start_bc.sh`
**KKL:** `/dev/vag-kkl` → ttyUSB0 (FTDI) подключён.

## Фокус (2026-08-07, Kali БК MFD готов)

**Сделано:** `ui/bc.py` стиль color MFD (скорость крупно + сетка 2×3), live на Kali `:0`.
**Старт:** `bash ~/Projects/cluster_pi/scripts/start_bc.sh`
**Скрин:** отправлен на mishock24@gmail.com (локально не храним).

## Фокус (2026-08-07, Kali БК 5″)

**UI:** `kali:~/Projects/cluster_pi/ui/bc.py` — борткомпьютер (не стрелки).
**Старт:** `bash ~/Projects/cluster_pi/scripts/start_bc.sh`
**Данные:** `ui/obd_feed.py` → ECU 0x01 (RPM/ОЖ/V/дроссель/DTC). Нужен KKL.

## Фокус (2026-08-07, Kali приборка LIVE K-line)

**Проект:** `kali:~/Projects/cluster_pi`
**UI:** `ui/dashboard.py` + `ui/obd_feed.py` — опрос ECU 0x01 (RPM/ОЖ/V/дроссель/DTC).
**Старт:** `bash ~/Projects/cluster_pi/scripts/start_dashboard.sh`
**Нужно:** `/dev/vag-kkl` + зажигание ON. Сейчас адаптер на Kali не виден (USB пустой).

## Фокус (2026-08-07, Kali приборка DEMO 5″)

**Проект на Kali:** `~/Projects/cluster_pi` (уже был).
**Тест UI:** `ui/dashboard_demo.py` + `scripts/start_dashboard_demo.sh` — fullscreen 800×480 pygame, демо без OBD.
**Запуск:** `bash ~/Projects/cluster_pi/scripts/start_dashboard_demo.sh` (DISPLAY=:0).
**Проверено:** окно «Audi A4 B5 · Y921OE · DEMO» 800×480 на экране Kali.

# Контекст чата (живой)

## Фокус (2026-08-06, EZGO схемы/мануалы)

**Папка:** `Платы и модули/Электрокары/EZGO_Club_Car/`.
**Главный repair:** SM **612342** (схемы F/L). Доп.: Parts **620365**, ST400 SM **614281** (справочно). Owner 605693 удалён.
**Индекс схем:** `WIRING_REFERENCE.md` (только PDF, без PNG-превью).

## Фокус (2026-08-06, SILA VM II Premium+ 6.2K)

**Папка:** `Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/`.
**Обязательный RU:** `РУКОВОДСТВО_RU.md` (официального RU PDF нет).
**Скачано:** EN User Manual + Spec SILA VP-MH-PLUS; фото шильдика/корпуса в `pic/`.

## Фокус (2026-08-06, Deye только 6.6K + RU)

**Модель:** SUN-6.6K-OG03LP1-EU-AM2.
**Обязательная инструкция:** `Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/РУКОВОДСТВО_RU.md`.
**Удалены:** PDF других серий (SG SolarCrown / deye.uz). EN-серийные PDF — только исходники в downloads/.

## Фокус (2026-08-06, Deye SUN-6.6K)

**Модель пользователя:** `SUN-6.6K-OG03LP1-EU-AM2` (off-grid, 48 В, 140 А, 2×MPPT).
**Папка:** `Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/`.
**Обновлено:** `TECH_SUMMARY.md`, `PINOUT.md`; строка в `Инверторы_сводка_токи_заряда/TECH_SUMMARY.md`.

## Фокус (2026-08-06, EZGO FAULT_CODES)

**Шпаргалка:** `Платы и модули/Электрокары/EZGO_Club_Car/FAULT_CODES.md` — мигания LED контроллера ST Shuttle (отдельно от GEM).
**Архив extract:** `notes/FAULT_CODES_EXTRACT.md`; raw: `notes/raw/`.

## Фокус (2026-08-06, GEM FAULT_CODES)

**Шпаргалка:** `Платы и модули/Электрокары/Polaris_GEM_e6_2017/FAULT_CODES.md` — VEH FAULT (SPN/FMI), частые DTC, LED станции, A-коды.
**Полная таблица:** `notes/DTC_FULL_TABLE.md`. LED зарядки: `notes/CHARGING_STATION_LED.md`.

## Фокус (2026-08-06, Солнечные инверторы — общая папка)

**Родитель:** `Платы и модули/Солнечные_инверторы/` (`README.md`).
**Внутри:** Deye, Must PH1100 / PV18-4024 / PV18-8048, Adion Expert Twin, сводка токов заряда. Новые инверторы — сюда же отдельной подпапкой.

## Фокус (2026-08-06, Электрокары — общая папка)

**Родитель:** `Платы и модули/Электрокары/` (`README.md`).
**Внутри:** `Polaris_GEM_e6_2017/`, `EZGO_Club_Car/`. Новые Club Car / LSV — сюда же отдельной подпапкой.

## Фокус (2026-08-06, EZGO / Club Car)

**Папка:** `Платы и модули/Электрокары/EZGO_Club_Car/`.
**Мануал:** `downloads/EZGO_ST_Shuttle_4-6_E_Service_and_Repair_Manual.pdf` (P/N 612342, 196 стр., ST Shuttle 4/6 E).
**Доки:** `TECH_SUMMARY.md`, `PINOUT.md` (J1/J2 контроллера), `pic/`.
**Club Car:** материалов пока нет.

## Фокус (2026-08-06, GEM BMC)

**BMC распиновка:** SM §8.29–8.30 → `Платы и модули/Электрокары/Polaris_GEM_e6_2017/WIRING_REFERENCE.md`.

## Фокус (2026-08-06, Deye OG03)

**Папка:** `Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/` — off-grid SUN-(3–6.6)K-OG03LP1-EU-AM1/AM2.
**EN:** `downloads/Deye_SUN-3-6.6K-OG03LP1-EU-AM_UserManual_EN.pdf` (49 стр.).
**RU на OG03:** официальной нет; ближайшая RU — `downloads/Deye_SUN-5-8K_SolarCrown_Инструкция_RU.pdf` (гибрид SG01, не OG).
**Доки:** `TECH_SUMMARY.md`, `PINOUT.md`, `notes/RU_manual_search.md`.

## Фокус (2026-08-04, бензин отключён)

**Сделано:** автомониторинг бензина, почта и Telegram-пуши выключены.
**Таймеры:** `gdebenz-fuel.timer`, `gdebenz-qr-monitor.timer` — disabled.
**Конфиг:** `Проекты/ai_assistant/data/gdebenz-fuel.json` → `monitoring_disabled: true`.
**Проверка:** `systemctl --user list-timers --all | grep -i gdebenz` → пусто; `python3 …/gdebenz_fuel.py --monitor` → skipped.



## Фокус (2026-08-04, HA Обзор Object not found)

**Жёлтые «Объект не найден»:** карточки `camera.esp_camera` / flash / identify — камера offline (`10.1.30.129`), сущностей нет.
**Сделано:** lovelace → markdown-инструкция + history-graph CPU; ESP Camera HK отключён в yaml/config_entries.
**Проверка:** обновить `http://10.1.30.126:8123/lovelace/default_view` (Ctrl+F5).


## Фокус (2026-08-04, Pi5 HA CPU temp график)

**Проблема:** плоский график 38.4 °C (живые ~47 °C). Pi3 — нормальные колебания.
**Причина:** cron без кавычек на путь с пробелами `Apple HomeKit accessory` → скрипт не запускался, `cpu_temp.txt` с 31.07.
**Сделано:** `pi5-ha-cpu-temp.timer`, `~/bin/pi5-ha-publish-cpu-temp.sh`, cron убран; HA перезапущен, sensor → 48.3.
**Проверка:** `systemctl list-timers pi5-ha-cpu-temp.timer`; `cat …/host_status/cpu_temp.txt`; дашборд `http://10.1.30.126:8123/pi5-monitor/monitor`.


## Фокус (2026-08-04, Cursor Agent HA «Сайты»)

**Проблема:** Home Assistant → `{"detail":"Not Found"}` (OAuth на `/auth/authorize` корня PWA).
**Сделано:** `api/sites_proxy.py` — ловушка `/auth/*`, Location rewrite, shim location/a; MVP перезапущен.
**Проверка:** `curl -sk https://127.0.0.1:8767/auth/authorize?...` → 200 HTML; клиент 10.1.30.41 тянет `/sites/ha/auth/*` OK.
**IP Pi5:** `10.1.30.126` (не .125).


## Фокус (2026-08-04, EDM / Cursor Agent «Сайты»)

**Проблема:** вкладка EDM — `127.0.0.1:8080` недоступен после reboot.
**Причина:** `home-pi-Documents.mount` → ordering cycle на `local-fs.target` → `edm-web` не стартовал.
**Сделано:** unit mount удалён (бэкап `.cursor/backups/`); `edm-web` active, `Restart=always`; прокси `:8767/sites/edm/` → 200.
**Проверка:** `systemctl is-active edm-web`; `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/`.



## Фокус (2026-08-06, Polaris GEM e6)

**Папка:** `Платы и модули/Polaris_GEM_e6_2017/` — VIN 5ACA6AGA3H0002115, e6, VCM+BMC.
**Главное:** SM **9940314 R02** (2016–2023); Brandfolder https://brandfolder.com/waev/service-support
**Распиновка:** `WIRING_REFERENCE.md` + `notes/wiring_extract/` — готов отвечать по пинам/цветам/сигналам.
**Диагностика ПК:** Digital Wrench только дилерский.


## Фокус (2026-08-04, Инструкции Эльтавр)



**Папка:** `Инструкции Эльтавр/` — PDF + HTML «нет данных на мониторе» (Як/Дилижанс), pic/, scripts/, notes/.



## Фокус (2026-08-03, Drive инструкция монитор)



**Файлы:** `Инструкции Эльтавр/downloads/Диагностика_нет_данных_на_мониторе_Як_Дилижанс.pdf` + HTML-исходник.

**Почта:** отправлены вложением на mishock24@gmail.com.

**Drive:** OAuth google-mcp `invalid_grant` — нужна повторная авторизация в Cursor desktop (MCP google), затем залить в `J.A.R.V.I.S — файлы` (`1wiKoyX27z3BxLuaDKG3oq_31nuAT2wLz`).



## Фокус (2026-08-03, ADION Expert 6kW)



**Инвертор:** `Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/` — USB `/dev/hidraw0`, заливка рабочего профиля **22 OK** (2026-08-03). LCD вручную: 10=OnL, 16=UCb, 33=EdS, 39=AEN, 28=SIG.



## Фокус (2026-08-03, инструкции сервиса Эльтавр)



**PDF:** `Инструкции Эльтавр/downloads/Диагностика_нет_данных_на_мониторе_Як_Дилижанс.pdf` — диагностика «нет данных на мониторе», Як/Дилижанс. Исходник HTML + `scripts/build-diagnostika-monitor-pdf.sh`.



## Фокус (2026-08-01, VPN Apple TV)



**3x-ui:** клиент **`appletv`** добавлен в inbound `vless-reality`. Подписка `https://89.127.199.6:2096/sub/5101960c-1fb4-4c31-b125-fff1e6e29a6b`. На ТВ — Happ (VLESS Reality). Обновлён `vpn-guide.md`.





## Фокус (2026-07-31, MUST PV18-4024 PRO II)



**Активный модуль:** `Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/` — MUST **24 V / 4 kW**, off-grid. АКБ **460 Ah** + ANT BMS **без** связи с инвертором. S/N 009000001400008. Чеклист: `НАСТРОЙКА_ЭКСПЛУАТАЦИЯ.md`. Рабочий профиль USB: `applied-settings/WORKING_PROFILE.md`, скрипты в `scripts/`.



**Пульт PWA (2026-07-29):** после миграции Documents bridge был на `/home/pi/Документы` — починено: `.env` + `settings.py` → `/home/pi/Documents`, MVP перезапущен, smoke OK.



**Аудит Documents (2026-07-29):** симлинк OK; batch-fix 35+ скриптов/systemd/cron на `/home/pi/Documents`. Скрипты: `.cursor/scripts/fix-documents-paths.sh`, `audit-documents-paths.sh`.



## Фокус (2026-07-29, Documents пути)



**Воркспейс Pi 5:** канон `/home/pi/Documents` (ASCII, Remote Control). Симлинк `/home/pi/Документы` → `Documents`. Старый bind-mount отключён; вложенная копия `Documents/Документы` удалена. Скрипт: `.cursor/scripts/fix-documents-paths.sh`. Worker: `total=1`, `ai-assistant-telegram` active.



## Фокус (2026-07-28, Pi3 гараж)



**Pi 3 (гараж):** SSH OK через `pi3` / NetBird `100.102.186.61` (`pi.netbird.cloud`). LAN `wlan0` `10.0.20.56`. Uptime ~2 дня.





## Фокус (2026-07-29, MUST PH1100)



**Инвертор:** `Платы и модули/Солнечные_инверторы/Must_PH1100_12kW/` — **2×230 А·ч** + **2× ANT 170 А**, без CAN.  

Настройки меню АКБ: `notes/НАСТРОЙКИ_АКБ.md`. Work Mode — как на ЖК: `notes/GRID_MODE_КРЫМ.md` (Load First Mode; Zero-Export вкл; Feeder Backflow и PV Excess to Utility выкл). (User-defined, 460 А·ч, заряд 140 А, разряд 210 А).



Похожие инверторы: `Adion_Expert_6kW_Twin`, `Must_PV18-4024_PRO_II`, `Must_PV18-8048_PRO_II` — добавлены README/notes без правок старых файлов.



**Правило папок:** документация/модули → `Платы и модули/<Имя>/`; софт → `Проекты/<Имя>/`. `.cursor/rules/separate-folder-per-topic.mdc`.



## Фокус (2026-07-28, MUST PH1100 кабели по мануалу)



Выписка Chart 3-2/3-3: АКБ **0 AWG / 53,49 мм²**, болт **M10**, кольцо Ø**10,5**/юбка **15,3 мм**, **24,5 Н·м**; GRID/LOAD **6 мм²**, момент **1,2 Н·м**, автоматы **63 A**; DC breaker мануал **300 A**. Файлы: `Платы и модули/Солнечные_инверторы/Must_PH1100_12kW_3Ph/КАБЕЛИ_ПО_МАНУАЛУ.md`, PDF в `downloads/`.



## Фокус (2026-07-28, MUST 12 кВт 3ф)



**Комплектация монтажа** гибрида MUST ~12 кВт трёхфазный (ориентир PH1100-12KL3-EU): автоматы C32 4P, кабель AC 5×6, АКБ 95 мм² + предохранитель 250–300 A, PV 4–6 мм² Voc&lt;800 В. Файл: `MUST_12kW_3ф_комплектация.md`. Режим: пока без панелей (сеть+АКБ).



## Фокус (2026-07-27, Kali 5″ HDMI)



**Kali / Pi Zero 2 W:** дисплей 5″ HDMI 800×480 + XPT2046 настроен. HDMI forced, fb 800×480, тач ADS7846, `lightdm` + `graphical.target`. Модуль: `Платы и модули/HDMI_5inch_800x480_XPT2046/`. Бэкапы на Kali: `/boot/firmware/*bak-hdmi5-*`.



## Фокус (2026-07-25, MUST PV18-4024 PRO II)



**Модуль:** `Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/` — MUST **24 V / 4 kW**, off-grid. АКБ **460 Ah** + ANT BMS **без** связи с инвертором. Шильдик S/N 009000001400008. Чеклист: `НАСТРОЙКА_ЭКСПЛУАТАЦИЯ.md`.



**USB → Pi 5 (2026-07-25):** эталон `inverter_working.*` (16:13), профиль 20 рег. **Новый инвертор:** заливка 16:18 — OK=13, skip=6; verify **20/20 OK** (20117=225 после стабилизации шины). LCD-only (152xx, прог. 41 Must New и др.) — вручную по `WORKING_PROFILE.md`.



**USB → Pi 5 (2026-07-31):** второй инвертор `/dev/ttyUSB0`, заливка + `--fix` → **verify 20/20 OK**, АКБ ~26 V при заливке.



## Фокус (2026-07-23, модуль ADION инвертор)



**База модулей:** добавлен `Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/` — ADION AXPERT KING II 6kW TWIN-B ON-LINE (OEM Axpert King II TWIN). PDF инструкции, PINOUT, TECH_SUMMARY, 2 pic из мануала.



## Фокус (2026-07-22, ANT_LCD → ESP32-C6)



**ANT_LCD C6:** откат LVGL → **`TftColorDisplay`** (3D-батарея, метрики, страница ячеек, press-edge тач). LVGL удалён. Прошито `/dev/ttyACM0` (~389 KB).



**База модулей:** добавлен `Платы и модули/ESP32-C6-Touch-LCD-1.47/` — PINOUT, TECH_SUMMARY, схема, demo (57 MB), 2D/3D, фото.



## Фокус (2026-07-09, анализ SystemLog ANT BMS)



**Лог `SystemLog_20260709_122623.txt`:** подтверждены повторяющиеся UV/дисбалансные события (ячейки 12/14/15), множественные `CHGOverCurWarning` до ~130A и термокачание MOS `79–80°C` с частым `MOSHighTempProtect/Recover`; в логе много дублированных/неконсистентных записей (в т.ч. нулевые `TotalV/MinUnitV`), что похоже на шум/сбои телеметрии при тяжёлом режиме.



**Визуализация лога:** добавлен скрипт `Проекты/Arduino/firmware/ANT_BMS/scripts/visualize_system_log.py`, сгенерированы графики и CSV в `Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/` (ток, min/max ячеек, разброс, температуры, топ событий, проблемные ячейки).



## Фокус (2026-07-07)



**Arduino a20014 v26 ANT:** активный проект `Проекты/Arduino/firmware/Eltavr_firmware/a20014_v26_ant` (форк v7). Эталон v7/v13: `a20014_plata_monitora/`. Сборка v26: `bash scripts/build-release-9600.sh` → `a20014_v26_9600.hex`.



**RS485 ANT BMS (2026-07-08):** на Pi 5 не удалось получить ответ по UART на `ttyAMA0/serial0` при legacy запросах `5A5A...` и новом `7E A1` handshake (похоже, BMS не в нужном режиме/не активирована или другой протокол/baud).



**TTL ANT BMS (2026-07-08):** подключила BMS через USB‑TTL к `ttyUSB0`; проверка при `9600/19200/115200` (пассивно и legacy live `5A 5A 00 00 00 00`) — **ответов нет (0 bytes)**.



**ANT BLE (2026-07-08):** по `bluetoothctl` удалось подключиться к `9B:FD:E9:52:AB:0A` — `Connected: yes`.



## Фокус (2026-07-09, ANT BMS веб v2.3.9)



**ANT BMS web_configurator v2.3.9:** connect через D-Bus+GLib pump (без bluetoothctl connect), до 10 попыток — **работает** (~20 с, 16 рег.). Жёлтый индикатор = идёт connect до 70 с.



## Фокус (2026-07-09, ANT BMS веб v2.4.1)



**ANT BMS web_configurator v2.4.1:** исправлен перевод параметров во всех вкладках — убраны дубли «Защита/Восстановление/Предупреждение», добавлен контекст по полю (напр. «Заряд перегрев: порог защиты»). SW-кэш поднят до `v7`.



## Фокус (2026-07-09, ANT BMS веб v2.4.2)



**ANT BMS web_configurator v2.4.2:** устранён сломанный CSS-блок `busy-overlay` (стабильный phone-like дизайн), подписи `V_SOC_Tab_*` стали уникальными (`SOC 100%..0%`), добавлено авто-восстановление BLE при кратком обрыве (backend quick reconnect + frontend auto reconnect). SW-кэш `v8`.



## Фокус (2026-07-09, ANT BMS веб v2.4.3)



**ANT BMS web_configurator v2.4.3:** устранено долгое зависание `Connecting BLE` — обёртки `bluetoothctl/hciconfig` теперь с timeout, connect работает в fail-fast (до ~45с, 6 попыток), фронт таймаут `/api/connect` 50с, SW-кэш `v9`.



## Фокус (2026-07-09, ANT BMS веб v2.4.5)



**ANT BMS web_configurator v2.4.5:** максимальное ускорение connect — быстрый возврат при уже активной BLE-сессии с тем же MAC, дедлайн connect ~20с, 3 попытки, сокращённые окна `Connected/ServicesResolved`, UI timeout `/api/connect` 25с, SW-кэш `v10`.



## Фокус (2026-07-09, ANT BMS веб v2.3.8)



**ANT BMS web_configurator v2.3.8:** на скрине MAC `90:FD` (опечатка) → автозамена на `9B:FD`. Жёлтый = connect, красный = ошибка. Сейчас BlueZ: `le-connection-abort-by-local` даже без телефона — BMS рвёт link на GATT. Проверено: scan видит `9B:FD:E9:52:AB:0A`, connect падает. Рекомендация: BT off на телефоне 1 мин + обесточить BMS 10 с + «Сканировать» → выбрать из списка.



## Фокус (2026-07-09, ANT BMS веб v2.3.2)



**ANT BMS web_configurator v2.3.2:** фикс зависания UI при connect — BLE в отдельном потоке, connect не блокирует `/api/health`. Ошибка connect теперь с бэкенда (не «таймаут 40 с»). Сейчас BMS `9B:FD:E9:52:AB:0A` отвечает `le-connection-abort-by-local` — закрыть ANT на телефоне.



## Фокус (2026-07-09, ANT BMS веб v2.3)



**ANT BMS web_configurator v2.3.0:** структура вкладок по мануалу §1–§4 (подменю Параметры/Моё, команды §3, RSSI, SW-кэш). Порт **8788**.



## Фокус (2026-07-09, ANT BMS веб v2.2)



**ANT BMS web_configurator v2.2.0:** русский UI по мануалу antbms.vip — меню параметров, группы управления, справка. Порт **8788**, `ant-bms-web.service`. PWA: Сайты → BMS.



## Фокус (2026-07-09)



**Cursor Agent / iOS Safari (11:00):** v66 — убран mixed-content (HTTPS страница больше не пытается открыть `ws://`), чат снова на `wss://` от origin; добавлен idle-timeout 50с на сервере для зависших сокетов. Открывать: `https://91.215.61.76:8767/app/` и сделать hard refresh.



## Фокус (2026-07-08)



**Cursor Agent / вкладка «Сайты» (2026-07-08, 23:01):** исправлена ошибка `Не удалось загрузить список сайтов: Load failed` на телефоне при открытии WAN без порта `91.215.61.76`. В `pwa/app.js` добавлен авто-fallback на `:8767/:8766` и повтор `GET /api/sites`; обновлён SW cache `v60` (`pwa/sw.js`, `pwa/index.html`). Проверка: `https://91.215.61.76:8767/app/sw.js` отдаёт `cursor-agent-pwa-v60`, `app.js?v=20260708-sites-fix`.



**ГдеБЕНЗ:** fast `/gdebenz` (~1 с), полная `/gdebenz проверка`; источники из `data/gdebenz-fuel.json` (gdebenz, gdebenz.su, azs-crimea, atan, toplivo.tbank.ru). `toplivo.tbank.ru` переведён с probe на реальный API `/api/v1/stations` (bbox), данные Т-Банка участвуют в `есть/очередь`. Добавлены режимы `/gdebenz регион крым` и `/gdebenz города ...` (общий bbox), плюс метка `межгород`. В сводке чата показываются только `есть` и `очередь` (без блока `нет топлива`). Добавлен блок `⚠️ Источники со сбоями`, повторный опрос при полном сетевом отказе и fallback между зеркалами gdebenz.ru/gdebenz.su. Бот перезапущен.



## Фокус (2026-07-07, пауза)



**ГдеБЕНЗ в ai_assistant:** `/gdebenz` — сводка; `/gdebenz on` — пуш при бензине/очереди; город/топливо/интервал в чате. Таймер `gdebenz-fuel.timer` (5 мин). Конфиг `data/gdebenz-fuel.json`.



**Bybit авто trailing SL (профиль B):** включён — BE +3%, trail −3% от пика, фикс. TP +4% снят. SOL/ADA: SL −7% до роста. Конфиг: `Документы/.cursor/data/bybit-auto-confirm.json`. Лог: `~/bybit-auto-trader.log`.



## Фокус (2026-07-02)



**Cursor Agent PWA v1.7 (дизайн):** рефреш UI — палитра Cursor, aurora, glass header/composer, аватары в чате, typing dots, hero-метрики на «Статус», группы подсказок. SW v54. Ctrl+F5.



**3x-ui VPN:** клиент **Аня** добавлен в inbound `vless-reality` (подписка `https://89.127.199.6:2096/sub/16e97685-4d04-4b13-b29c-e10f893468ed`). См. `vpn-guide.md`.



**PWA «Сайты» → 3x-ui VPN:** после входа редирект уходил на `/q6om…/` вместо прокси — исправлено в `api/sites_proxy.py` (Location, `/panel` paths, iframe-shim). Перезапуск `cursor-agent-mvp.service`. Ctrl+F5 в браузере.



## Фокус (2026-07-01)



**SSH/Wi‑Fi Pi 5:** keepalive sshd 60 с; wlan0-watchdog 5 мин; fix-wlan0 — 3 пинга + fallback 8.8.8.8.



## Фокус (2026-06-29)



**Cursor Agent PWA — VPN_Server:** `ssh VPN_Server` (89.127.199.6, vpnuser); API `GET /api/vpn-server/status`; `.cursor/VPN_SERVER.md`. **Сайты:** вкладка **VPN** → `vpn_panel` (3x-ui `:37702`).



**Cursor Agent PWA — голос:** `https://10.1.30.126:8767/app/` (LAN), WAN `https://91.215.61.76:8767/app/`. Проброс :8767 на electro+office. CA для Windows: `/Eltavr-Cursor-Agent-CA.crt`.



**Cursor Agent PWA / Сайты / HA:** whitelist `/config`, shim iframe. Pi **10.1.30.126**. SW **v41**. Ctrl+F5 после обновления.



**Cursor Agent PWA — статус:** исправлен `GET /api/status` (импорт `SITE_TARGETS`); вкладка «Статус» снова работает. SW **v42**.



## Фокус (2026-06-28)



**Cursor Agent PWA — мобильное превью фото:** на телефоне превью прикреплённого фото перекрывало панель ввода (кнопка «Отправить» не видна). Исправлено в `Проекты/Cursor Agent/pwa/` — закреплён `composer-fixed`, компактные чипы превью (3rem), лимит высоты панели, `syncComposerHeight` после загрузки миниатюр. Кэш SW: **v17** (`sw.js`), `app.js?v=20260628-3`. На телефоне: перезагрузить вкладку / очистить данные сайта. Ошибка «не вернул ответ» — отдельно, таймаут сервера на Pi.



## Фокус (2026-06-26)



**web_config_bms:** TLS через локальный CA (`Eltavr BMS Web CA`), cert с SAN `10.1.30.126`. CA: `https://10.1.30.126:8443/Eltavr-BMS-CA.crt` — установить в Windows (доверенные корневые). Деплой: `sudo FORCE_CERTS=1 bash install-pi.sh`.



**Проект Cursor Agent:** Pi 5 + `cursor-sdk` на `Документы/` — PWA/Siri (`Проекты/Cursor Agent/`). Порт **8766**. **Автозапуск:** `cursor-agent-pi.service` + `cursor-agent-mvp.service` (`bash scripts/install-systemd-pi5.sh`).



## Фокус (2026-06-24)



**komunalka / Крымгазсеть:** задолженность — парсинг **«Задолженность … руб.»** (`server.js`).



**komunalka / Крымэнерго:** при параллельном refresh на Pi данные срывались; теперь **последовательный** обход, ожидание SPA после входа, полная перезапись метрик в UI (`app.js?v=20260624-1`). Проверка: **1566.39 ₽**, показание **20213** (24.06.2026).



## Фокус (2026-06-23)



**Bybit push:** **выключен** — `bybit-watch.timer` и `bybit-auto-trader.timer` disabled; `notify_telegram: false`. По запросу: `/bybit`, `/bybit_full`, `/bybit_ideas` в боте.



**Зачистка:** сняты остатки legacy mesh VPN и старого workspace ассистента. Docker ~14G. **Лимиты логов:** journald 200M, Docker 10m×3, logrotate ~/logs.



## Фокус (2026-06-22)



**BMS (отложено):** закладки ESPHome — [syssi/esphome-ant-bms](https://github.com/syssi/esphome-ant-bms), [syssi/esphome-jk-bms](https://github.com/syssi/esphome-jk-bms). Памятка: `.cursor/bms-esphome-refs.md`.



**Time Capsule File Browser:** `ha-filebrowser-timecapsule` :8092, дашборд HA с паролями на странице. Установка: `install-timecapsule-filebrowser.sh` на Pi3.



**Time Capsule A1470:** TimeCapsuleSMB v2.2.7 на `10.0.20.1`, doctor PASS, Samba 4.24.3. Pi 3 smbnetfs → SMB3, HA `/media/timecapsule` OK.



## Фокус (2026-06-21)



**Bybit авто:** ~54$ в обороте — ADA TP @0.166, SOL TP @76.75 (+4%), ETH продан. Таймер 30 мин, карт-бланш `deploy_all`. **Telegram:** только пополнение / TP / успешный BUY (`notify_positive_only`).



## Фокус (2026-06-18)



**UFW Pi 5:** `restore-pi5-ufw.sh` + `pi5-restore-ufw.service`. ZeroTier удалён (2026-06-19): `purge-zerotier.sh`.



**Проект komunalka:** Экор — до 5 кнопок счетов с **датой периода** (метрика `Чеки`); сумма к оплате из выписки. Жилсервис — fetch-логин. Чеки всех карточек — даты на кнопках.



## Фокус (2026-06-17)



**Проект EDM:** создан каркас `Проекты/EDM/` — simple Python, Docker, venv. Проверка: `docker compose up -d --build` → `EDM: запущено в режиме dev`.



## Фокус (2026-06-10)



**Сайт ЭЛЬТАВР (`/home/pi/www`):** админка Payload переделана в тёмный NobleUI-стиль — `theme: dark`, `admin-theme.css`, `AdminDashboardWelcome`, `AdminHeaderBar`, `AdminQuickNav` в `payload.config.ts`. Проверка: `http://10.1.30.126/admin` → 200.



## Фокус (2026-06-11)



**Pi 3 Time Capsule в HA:** `media_dirs.timecapsule`, rw mount, дашборд `timecapsule-media`. Health-check smbnetfs **выключен**.



## Фокус (2026-06-09)



**Pi 3 HA:** **2026.6.1**. Garage Camera OK. Реле CH3–8 синхрон с iPhone. **Детекция движения (гараж)** — выкл по умолчанию и при каждом старте HA. OSD откачен.



**Pi 3 гараж — Garage Camera:** прошивка исправлена (двойной HomeKit init при Wi‑Fi reconnect, GPIO0 reset отключён). **HA:** одна запись `Garage Camera` ID `44:D7:94:D6:07:0C`, `camera.garage_camera` **idle**, snapshot JPEG OK. **Не добавлять вручную** через «Обнаруженные» — только `reset-and-pair-garage-camera.sh`. Прошивка без сброса pairing: `flash-via-pi3.sh` (полный erase: `ERASE_FLASH=1`).



## Фокус (2026-06-08)



**Arduino ESP32-CAM (офис):** `firmware/esp32-homekit-camera` — Wi‑Fi ELEKTRO_ `10.1.30.49`, код `111-11-111`. **В HA Pi 5:** `camera.esp_camera`.



**Сайт Эльтавр (Pi 5):** `http://10.1.30.126`, `/home/pi/www`. **Прод VPS — не трогать.** Исправлены ссылки zakupki.gov.ru у клиентов (прямые карточки контрактов вместо `searchString`).



## Фокус (2026-07-02)

Домен/хостинг: подобраны варианты по цене и рейтингу (черновая подборка, с источниками из веб-поиска).



## Фокус (2026-07-09, ANT BMS веб v2.3.5)



**ANT BMS web_configurator v2.3.5:** connect fail-fast (~35 с), перед connect делается disconnect, улучшены ошибки BLE (GATT not resolved/abort-by-local). Скан быстрый, но BMS всё ещё часто занята телефоном.



## Фокус (2026-07-09, ANT BMS веб v2.4.6)



**ANT BMS web_configurator v2.4.6:** вкладка «Состояние» приведена ближе к APK (ячейки аккуратнее), `Protect/Warning` в realtime русифицированы, вход в «Параметры» ускорен (убран блокирующий авто-read/auto-L5, загрузка по кнопке в нужной категории). SW-кэш `v11`.



## Фокус (2026-07-09, ANT BMS веб v2.4.7)



**ANT BMS web_configurator v2.4.7:** в BLE-сканере снят фильтр по имени/префиксу MAC — теперь в списке видны все BLE-устройства в эфире, включая не-ANT. SW-кэш `v12`.



## Фокус (2026-07-09, ANT BMS веб v2.4.8)



**ANT BMS web_configurator v2.4.8:** исправлено отображение имён BLE в сканере — MAC больше не показывается как имя (если BlueZ подставил Alias=MAC). Для безымянных устройств выводятся подписи `ANT BMS (без имени)` / `BLE устройство (без имени)`.



## Фокус (2026-07-09, ANT BMS веб v2.4.9)



**ANT BMS web_configurator v2.4.9:** имена BLE в scan дополнены fallback из `bluetoothctl devices`, чтобы список совпадал с телефоном (если D-Bus не дал Name).



## Фокус (2026-07-09, ANT BMS веб v2.5.0)



**ANT BMS web_configurator v2.5.0:** добавлена загрузка `SystemLog_*.txt` и визуализация в `Моё → Графики SystemLog` (ток, пакет, min/max ячеек, дельта, температуры, топ событий, проблемные позиции ячеек). API: `POST /api/systemlog/analyze`.



## Фокус (2026-07-09, ANT BMS веб v2.5.1)



**ANT BMS web_configurator v2.5.1:** графики SystemLog доработаны: добавлены шкалы X/Y с делениями и подписями, отображение времени под графиком, а также min/max по сериям на каждом графике.



## Фокус (2026-07-09, ANT BMS веб v2.5.4)



**SystemLog runtime:** парсер поддерживает значения с префиксом `--`/`+` (например `--297D6H21M19S`), чтобы даты на графиках строились корректно по runtime.



## 2026-07-28 20:56

- Предварительная закупка MUST → mishock24@gmail.com (тема: Предварительная закупка — MUST 12 кВт 3ф).

- Источник: Платы и модули/Солнечные_инверторы/Must_PH1100_12kW/ЗАКУПКА.md



## Начальник (2026-07-28)



- Алиас **«начальник»** = Владимир Шуликов → `vladimirshulikov2@gmail.com`

- Правило: `.cursor/rules/boss-shulikov.mdc`

- По просьбе «отправь начальнику» — слать туда без уточнений.



## 2026-07-29 08:10 — шильдик



- Подтверждена модель **PH11-12KL3-EU** → `Платы и модули/Солнечные_инверторы/Must_PH1100_12kW/notes/ШИЛЬДИК.md`

- Корректировка закупки: GRID **C63**, LOAD **C32** (bypass 60 / 30 A). АКБ по-прежнему ANT 170 A.



## 2026-07-29 08:12 — инструкция RU

- Основной PDF: `Платы и модули/Солнечные_инверторы/Must_PH1100_12kW/downloads/MUST_PH1100_PH11-12KL3-EU_Руководство_RU.pdf`

- PH11-12KL3-EU = PH1100-12KL3-EU; EN → archive_EN; таблица АКБ 10 мм² = ошибка перевода.



## 2026-07-29 08:23 — 2×230 А·ч

- Перерасчёт: `notes/ПЕРЕСЧЁТ_2x230.md`, обновлены ЗАКУПКА/КОМПЛЕКТУЮЩИЕ.

- Параллель 460 А·ч; 2×ANT; к MUST 1×50/70; разряд 200–220 А.



## Drive — Музыка (2026-08-03)



Корневая папка **Музыка** (`13NyXdhAcvKhaOzDy3oacqvOcnEwtYrlz`). Треки туда, не в J.A.R.V.I.S.

## Музыка → только Drive (2026-08-04)

Скачанные треки — в Drive «Музыка» (подпапки артистов). **Без Telegram.**

## Музыка — только Drive (2026-08-04)

На Pi 5 mp3 **не хранить**: tmp → Drive «Музыка» → удалить. Без Telegram.
- GEM e6 2017: с gemcar.com скачан Owner’s Manual 2017 EN; схем/service нет (только owner).