## Фокус (2026-09-07, Aqara G2 → HA Pi3)

**Модель:** ZNSXJ12LM · `Camera-Hub-G2H-EAA1` @ `10.0.20.5:45029`.
**Блокер:** камера спарена с **Apple Home** — HA pairing недоступен, пока не снять из «Дом».
**Готово:** скрипты `discover/pair/add-aqara-g2-camera-ha` на Pi3; док `Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/`.
**Дальше:** HomeKit-код → `bash scripts/add-aqara-g2-camera-ha.sh XXX-XX-XXX` на Pi3.

## Фокус (2026-09-07, ANT BMS графики)

**Проблема:** history-graph «иголки» 0↔54 В / 0↔100% при offline BMS.
**Сделано:** логгер hold-last; `ant24c_read.py` (exit 1); template `*_graph`; purge ~3900 нулей; дашборд на graph-сенсоры.
**Проверка:** `pack_voltage_graph`=54.0, `soc_graph`=98.0; zeros в истории = 0.
**Файлы:** `home_assistant/config/packages/ant24c.yaml`, `dashboards/ant-bms-24c.yaml`, `bms-tools/ant24c_logger.py`.

## Фокус (2026-09-07, Audi A4 B5 расходники)

**Сделано:** `Платы и модули/Audi_A4_B5/FILTERS_AND_WIPERS.md` — фильтры (масло/воздух/салон/топливо) + щётки 530 мм, OEM и Mann/Bosch/Mahle; **04E 115 561 H не подходит** на AHL.

## Фокус (2026-09-07, PWA UUID resume)

**Проблема:** PWA ошибка `Persistent-session chat ID must be a UUID` (id `agent-…`).
**Причина:** новый `cursor-agent` ждёт чистый UUID; в localStorage остался префикс `agent-`.
**Сделано:** normalize в `llm/cursor_cli_client.py` + PWA + WS; retry без resume; SW v74; MVP перезапущен.
**Проверка:** WS с `agent-179824f3-…` → ответ «ок», agent_id без префикса.
**Пользователю:** обновить страницу PWA (Ctrl+F5).

## Фокус (2026-09-07, ANT BMS V2 регистрация)

**Сделано:** аккаунт cloud ANT BMS V2 через email API; активация письма; login OK.
**Логин:** mishock24@gmail.com · **uid:** 842247 · заметка: `Проекты/Arduino/firmware/ANT_BMS/notes/ANT_BMS_V2_ACCOUNT.md`
**Важно:** в приложении входить по почте (SMS/+86 обходим email-register).

## Фокус (2026-09-07, RC не сохраняет тумблер)

**Суть:** облако `remoteControlEnabled=true` уже сохранено. Тумблер «Remote Control» в Glass — локальный enroll; при закрытии окна сбрасывается; enroll не пишется (gate/provider).
**Сделано:** `~/bin/cursor-rc-force-on.sh` (enroll keys + облако + прокси/Wayland); док `REMOTE_CONTROL.md`.
**Правило:** Agents не закрывать; не дёргать тумблер. Worker systemd отдельно online.

## Фокус (2026-09-07, Remote Control OFF)

**Проблема:** тумблер Remote Control сам OFF — IDE без прокси → `permission_denied` region → catch ставит OFF.
**Сделано:** `~/bin/cursor-with-proxy.sh` (`--proxy-server=10809`), desktop/shim/open-agents; `cursor-keep-awake` (fix argv); cloud `remoteControlEnabled=true`; worker active.
**Проверка:** новый лог `20260907T123037` без `failed to load remote control` / region на BC; xray принимает api2; keep-awake active.
**Важно:** запускать Cursor только через прокси-обёртку, не `/usr/share/cursor/cursor` напрямую.

## Фокус (2026-09-07, PWA чат)

**Проблема:** PWA `https://10.1.30.126:8767/app/` не отвечал («Ты тут?», «Фоновая задача…»).
**Причина:** cursor-sdk CreateAgent OK, но run → status=error ~90с (пустой result); CLI `cursor-agent -p` при этом работает.
**Сделано:** `CURSOR_LLM_BACKEND=cli`, `llm/cursor_cli_client.py`; lifespan без двойного bridge; proxy timeout fix.
**Проверка:** WS `/ws/chat` «Ты тут?» → ответ ~17с. Обновить страницу PWA / очистить чат.

## Фокус (2026-09-07, Telegram Cursor)

**Проблема:** в Telegram Cursor Agent не отвечал — у бота был только SOCKS для Telegram, `agent -p` без `HTTPS_PROXY` → HTTP 403.
**Сделано:** `HTTPS_PROXY=http://127.0.0.1:10809` в `Проекты/ai_assistant/.env` + unit; `setdefault` в `cursor_agent_client.py`; сервис перезапущен.
**Проверка:** `systemctl --user is-active ai-assistant-telegram`; `agent -p` с прокси → OK.

## Фокус (2026-09-07, Cursor Pi5)

**Проблема:** self-hosted worker `cursor-self-hosted-worker` падал каждые ~10 с — без `HTTPS_PROXY` API Cursor из РФ недоступен.
**Сделано:** в `~/.config/cursor-worker.env` + unit прокси `http://127.0.0.1:10809`; worker **active**, `worker debug` → **1 worker**. IDE: `http.proxy` в settings. PWA `:8766` health/bridge OK.
**Проверка:** `systemctl --user is-active cursor-self-hosted-worker cursor-proxy-http`; `cursor-agent worker debug`.

## Фокус (2026-09-04, GEM ESP32-C3 веб UI)

**Сделано:** v0.3 SoftAP `GEM-BMC` / `gem-bmc-cfg` → http://192.168.4.1/ — MAC ANT в NVS + статус реле/BLE/CAN. Прошито.
**Дальше:** телефон → WiFi GEM-BMC → задать MAC; проводка CAN/реле.

## Фокус (2026-09-04, GEM ESP32-C3 + реле)

**Сделано:** v0.2 — реле K5/K12/VCM/K7 + interlock как H503 (GPIO0/1/2/3 + GPIO10); сборка OK `releases/gem_bmc_can_emu_esp32c3_v0.2.bin`.
**Пины:** CAN 4/5; реле 0/1/2/3; IL 10; LED 8.
**Прошивка:** v0.2 залита на Super Mini (`/dev/ttyACM0`, esptool OK).
**Дальше:** проводка SN65 + реле/опто по PINOUT; закрыть ANT на телефоне; тест.

## Фокус (2026-09-04, GEM ESP32-C3 + ANT BLE)

**Сделано:** папка `firmware/gem_bmc_can_emu_esp32c3/` — TWAI CAN v4 + NimBLE→ANT (SOC/U), сборка **OK** (`releases/gem_bmc_can_emu_esp32c3_v0.1.bin`, 566 KB).
**Пины:** GPIO4 TX / GPIO5 RX → SN65HVD230; LED GPIO8.
**Важно:** overlay SOC/U в `0CFF0EF3` экспериментальный (шкала в логе не доказана); без BLE — чистый v4.
**Дальше:** прошить Super Mini, закрыть ANT на телефоне, тест на машине + уточнить карту байтов.

## Фокус (2026-09-03, MUST PV18-4024 — заливка)

**Сделано:** ещё один `Must_PV18-4024_PRO_II` по USB `/dev/ttyUSB0` — снимок + рабочий профиль.
**Проверено:** `must-verify-profile.py --fix` — **20/20 OK** (20117=225). АКБ при заливе **24.0 В**.
**Снимки сегодня:** `factory-settings/inverter_factory_20260903_130250.json`, ранее `…_111458.json`.
**Команды:** `bash …/Must_PV18-4024_PRO_II/scripts/must-apply-working.sh` → `python3 …/must-verify-profile.py --fix`.

## Фокус (2026-09-03, Deye SUN-20K + 3× RW-F16 PDF)

**Сделано:** PDF схема + инструкция Parallel Mode 2 (BAT1=№1+№2, BAT2=№3, CAN daisy-chain).
**Файл:** `Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/generated/Deye_SUN-20K_3xRW-F16_Installation_Setup_RU.pdf` (копия в `Deye_RW-F16/generated/`).
**Скрипт:** `…/scripts/generate_3x_rwf16_pdf.py`. Меню: Lithium Mode **00**, ёмкость **942 Ah**, ток **300 А**.

## Фокус (2026-09-02, GEM e6 BMC CAN — **OK**)

**Неисправная:** VIN `5ACA6AGA3H0002115` — CAN-эмулятор BMC **v4 работает**, **DTC нет** (подтверждено 2026-09-02).  
**Скрипт Pi:** `…/scripts/can-bmc-emulate.py` · **STM32 H503:** `…/firmware/gem_bmc_can_emu_h503/` · CAN: **SN65HVD230 (VP230)** на B7/B8 (см. PINOUT) · **Arduino legacy:** `…/firmware/gem_bmc_can_emu/`  
**Памятка:** `…/notes/BMC_CAN_EMULATOR_v4_OK.md` · карта `notes/CAN_BUS_MAP.md`  
**Запуск Pi:** `can-setup.sh --bitrate 250000` → `ai-tmux run gem-bmc-emu 'python3 …/can-bmc-emulate.py'`  
**Дальше:** прошить H503 (`flash.sh stlink`), подключить SN65HVD230 + реле X3, проверить на машине.

## Фокус (2026-08-31, Cursor Agent — Артём)

**Сделано:** проект `Проекты/artem-cursor-agent/` — LAN **10.0.20.56** (pi3), NetBird не нужен. Bundle на Pi 3 обновлён.

## Фокус (2026-08-31, Учёба Артём → Drive)

**Постоянно:** учёба **Шпак Артём** (Арем) — папка Drive **«Учёба Артём»** `1kJfRYBl7QKTVLEWlw32nK_J_sG-dVb5V`. По вопросам про учёбу — **сначала Drive**; сводка `Сводка_родительское_собрание_2026.md`. Правило: `.cursor/rules/artem-study-drive.mdc`, справочник: `.cursor/GOOGLE_SERVICES.md`.

**Ожидается (2026-09-01):** новый договор + документы по **налоговому вычету** → анализ и обновление сводки на Drive.

**Авто (с 2026-08-31):** проверка папки **каждый понедельник 09:00** (`artem-study-drive-check.timer`) + **по твоему запросу**. Проект: `Проекты/artem-study-drive/`.

## Фокус (2026-08-28, A11096 EmKit→Pylon)

**Must:** `firmware_EmKit_to_Pylon_Must/` — мост EmKit→CAN для MUST, `firmware_EmKit_to_Pylon_Must_standalone.bin` 14112 B.

**Сделано:** Pylon LV v1.2 — кадры `351/355/356/359/35C/35E`, `pylon_lv_config.h` (16S LFP), маппинг alarm по Battery-Emulator. Сборка + прошивка ST-Link verify OK.
**Памятка:** `firmware_EmKit_to_Pylon_Deye/README.md`, `…/notes/СОВМЕСТИМОСТЬ_A11034R6.md`.
**Дальше:** RS485 A11034↔A11096 → живые U/I на Deye; при другом пакете — править `pylon_lv_config.h`.

## Фокус (2026-08-27, .cursorignore Arduino)

**Сделано:** из `.cursorignore` убраны `Проекты/Arduino/` и `Arduino/` — значки «запрет» в explorer.
**Нужно:** Reload Window в Cursor, если иконки остались.

## Фокус (2026-08-24, HA Pi5)

**Причина:** после reboot контейнер `homeassistant` не стартовал — device `/dev/gpiochip0` отсутствует на Pi 5.
**Сделано:** убран из `home_assistant/docker-compose.yml`; оставлены gpiochip15 + gpiomem0.
**Проверено:** `:8123` → 200.

## Фокус (2026-08-24, RS485 ANT BMS J75H)

**Связь:** OK. Порт `/dev/ttyAMA0`, baud **9600**, modern `7E A1`.
**BMS:** `ANT@BLE16ZNUB-J75H` · hw `16ZNJARB170A` · sw `16ZNUB00-241008A`.
**Памятка:** `Платы и модули/RS485_CAN_HAT/ANT_BMS_J75H_RS485.md`, `bms-tools/README_ant_j75h_rs485.md`.
**Проверка:** `python3 bms-tools/ant_bms_probe.py --port /dev/ttyAMA0 --baud 9600`.

## Фокус (2026-08-24, RS485 ANT BMS J75H)

**BMS:** `ANT@BLE16ZNUB-J75H` (`65:E4:71:8F:2B:A3`).
**Связь RS485:** ЕСТЬ на **/dev/ttyAMA0 @ 9600** (не 19200). Протокол modern `7E A1`.
**Info:** hw `16ZNJARB170A`, sw `16ZNUB00-241008A` (CRC OK, совпадает с BLE).
**Проверка:** `python3 -c` опрос status/info на 9600 через `bms-tools` / ttyAMA0.

## Фокус (2026-08-20, MUST PV18-4024 — ещё один инвертор)

**Сделано:** рабочий профиль залит в ещё один `Must_PV18-4024_PRO_II` по USB `/dev/ttyUSB0`, Modbus `19200`, slave `4`.
**Проверено:** после `must-verify-profile.py --fix` — **20/20 OK**; проблемный `20117` (выход 230 В / raw 225) доведён автоматической фиксацией.
**Команды:** `bash Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/scripts/must-apply-working.sh` → `python3 .../must-verify-profile.py --fix`.

## Фокус (2026-08-18, .cursorignore)

**Сделано:** из `.cursorignore` убраны `Платы и модули/` и `**/.cursor/`. Read/Grep по модулям и `chat.md` снова работают. Откат: `20260818T161600`.

## Фокус (2026-08-18, LP16-48100 в инверторе)

**АКБ:** MUST LP16-48100, 51.2 В / 100 А·ч. Штатная пара — PV18-8048 PRO II (не 4024).
**Уставки:** 14=LI, 37=SOC, 40=UNI, 41=Must New; ток ≤100 А; Bulk 57.6 В (OVP BMS 58.4 В).
**Источники:** `Платы и модули/Солнечные_инверторы/Must_LP16-48100/` + `notes/СОВМЕСТИМОСТЬ_PV18-8048.md`.

## Фокус (2026-08-18, Vega MT X LTE — 3 CAN)

**Авто:** Touareg GP 2009 3.0 TDI CASA. Блок умеет 3 CAN — подключаем все.
**Схема:** CAN1 Drive Train 500 (оранж/чёрный), CAN2 Komfort 100 (оранж/зелёный), CAN3 Infotainment 100 (оранж/фиолетовый). Gateway в J285.
**Файлы:** `Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.pdf` (5 стр.), `.md`, `PINOUT.md`. Справка шин: `downloads/SSP_298_Touareg_electrical.pdf`.

## Фокус (2026-08-18, Vega MT X LTE PDF)

**Модуль:** в `Платы и модули/Vega_MT_X_LTE/` добавлен читабельный PDF `INSTALL_Touareg_GP_2009_CASA.pdf` и исходник `INSTALL_Touareg_GP_2009_CASA.html`.
**Проверено:** `libreoffice --headless` успешно собрал PDF, файл на месте рядом с `.md`.

## Фокус (2026-08-18, Vega MT X LTE / Touareg GP)

**Модуль:** `Платы и модули/Vega_MT_X_LTE/` создан по стандарту: `source_url.txt`, `source_page.html`, `download_report.json`, `downloads/`, `extracted/`, `pic/`, `PINOUT.md`, `TECH_SUMMARY.md`.
**Добавлено:** практическая инструкция `INSTALL_Touareg_GP_2009_CASA.md` для `Volkswagen Touareg GP 2009 3.0 TDI CASA`: питание `30`, отдельный `15`, старт с одной пары `CAN`, без постоянного монтажа на `OBD`.
**Проверено:** скачаны мануал/протоколы/прошивка/сертификаты, сохранены 3 фото устройства, архив драйвера распакован в `extracted/stsw-stm32102/`.

## Фокус (2026-08-17, n8n удалён)

**Проект:** `Проекты/n8n` снят целиком. Docker, MCP, WAN `:5679`, вкладка PWA — нет.
**Дашборд Малинка 5** живёт в `Проекты/Cursor Agent/` (`scripts/build-pi5-dash.py`, `data/pi5.html`, timer `pi5-dash-refresh`).
**Проверено:** порты 5678/5679 закрыты; `/malinka-dash` 200; MCP только `google`.

## Фокус (2026-08-17, Ungate status bar)

**Пропала** нижняя кнопка Ungate: `show()` ждал async bootstrap после Reload. Исправлено — показывается сразу (приоритет 1000).
**Нужно:** `Ctrl+Shift+P` → **Developer: Reload Window**. Или сразу **Ungate: Open Dashboard**.



**Готово:** туннель живой `https://stated-not-scholarships-allergy.trycloudflare.com` (health 200). Base URL в Cursor: `…/v1`.
**Запас:** WAN `http://91.215.61.76:47821` (Keenetic electro+office + UFW).
**OAuth ChatGPT:** `:1455` слушает с старта API на `0.0.0.0`. Повторный Login; если Chrome снова на Windows localhost — в адресной строке сменить порт `1455` → `47821`, query оставить.
**Процессы:** tmux `job-ungate-api`, `job-ungate-tunnel`.


## Фокус (2026-08-17, EmKit BMS отваливался)

**Проект:** `Проекты/web_config_bms/` — HTTPS `:8443` висел на TLS handshake интернет-сканера (однопоточный `wrap_socket` на listen).
**Сделано:** handshake в рабочем потоке + таймаут 8 с; `Restart=always`; watchdog `web-config-bms-watch.timer` (2 мин).
**Проверено:** `https://127.0.0.1:8443/` 200; `/api/status` → `bms_emkit` up; незавершённый TLS больше не блокирует GET.



**Не Cursor.** PI5_Работа в приложении ChatGPT. Телефон не ходит на :22; релей через десктоп Windows, затем SSH на Pi.
**Сделано:** Codex CLI 0.147.0 на Pi (`~/.local/bin/codex`), в login PATH. `codex login --device-auth` с Pi — 403 (OpenAI).
**Нужно:** на Windows в ChatGPT Connections SSH-хост `91.215.61.76` user `pi` порт `22`; десктоп не закрывать.

## Фокус (2026-08-14, SSH WAN Malinka 5)

**Проект:** Keenetic / Pi 5. На электроцехе `:22` уже шёл на wlan0 Pi 5; на офисе правила не было.
**Сделано:** `ip static tcp ISP 22 192.168.1.2 22` на office. WAN `ssh pi@91.215.61.76`, алиас `pi5-wan`.
**Проверено:** TCP + ssh-keyscan WAN — ключ совпал с sshd Pi 5. Скрипт `Документы/.cursor/scripts/install-pi5-ssh-wan-portforward.sh`.

## Фокус (2026-08-14, Ungate proxy timeout)

**Проект:** `ungate/` — `GET /settings failed: extension proxy timeout`: новый UI ждал api-proxy, хост расширения без хендлера.
**Сделано:** сначала fetch (localhost / tunnel / asExternalUri), proxy — запасной. Сборка в `orchidfiles.ungate-1.7.9`.
**Нужно:** закрыть вкладку Ungate и открыть снова со статус-бара (или Reload Window).

## Фокус (2026-08-14, Ungate HTTP/2)

**Проект:** `ungate/` — Cursor не перезагрузил JS, туннель оставался QUIC. Обёртка `~/.ungate/bin/cloudflared` всегда добавляет `--protocol http2`.
**Сейчас:** процесс с http2, в логе `Initial protocol http2` / `Registered … protocol=http2`. URL в панели Ungate (Settings).
**Проверено:** `ps` — `--protocol http2`; статус running.

## Фокус (2026-08-14, Ungate Failed to fetch)

**Проект:** `ungate/` — туннель `--protocol http2` (QUIC на Pi рвался). Сборка в `orchidfiles.ungate-1.7.9`.
**Проверено:** connector `protocol=http2`, `ha_connections=1`, стабильный. trycloudflare с Pi всё ещё 1033 — нужен Restart tunnel после Reload Window; если URL снова мёртвый — проброс Keenetic `:47821`.
**Дашборд fetch:** починен ранее (api-proxy).

## Фокус (2026-08-14, Ungate Failed to fetch)

**Проект:** `ungate/` — дашборд Analytics на SSH: `Failed to fetch`, webview ходил на `localhost` ПК, API на Pi (`:47821`).
**Сделано:** запросы через extension host (`api-proxy`). Сборка в `~/.cursor-server/extensions/orchidfiles.ungate-1.7.9`.
**Проверено:** API `/health` 200; тесты extension 63. Нужен **Reload Window**.

## Фокус (2026-08-14, БК Pico Audi)

**Проект:** `Проекты/audi_bc_pico/` — 16:38 py залиты, ACM жив. Нажать Reset на Eval (жёлтый, потом WAIT). Без UART.
**Проверено:** UF2+upload 14:49, Pico `2e8a:0005`. MADCTL `0x48` (вверх ногами → `0x88`).
**K-line:** UART0 CP2102; USB-KKL в Eval USB не хост.

## Фокус (2026-08-14, Mint Live USB 10.10.0.85)

**Хост:** `eltavr-mint` · Linux Mint 22.1 Live USB · user `mint` · ключ Pi 5 `id_ed25519`.
**Сеть:** Home `10.10.0.85/24` (провод `enp4s0`, SSID ELEKTRO). Pi 5 в Guest — SSH через Keenetic (`ssh mint`).
**Проверено:** вход OK; `sshd` active; overlay `/cow` ~819 МБ.
**Windows (2026-08-14):** система на NVMe `SYSTEMA`, не на HDD. SAM: `Растислав` и `Admin` — пароль пустой (`chntpw`). Учётки «Расуль» нет. HDD `DATA` 931 ГБ — данные, без SAM.

## Фокус (2026-08-14, БК Pico Audi)

**Проект:** `Проекты/audi_bc_pico/` — БК на Pico-Eval-Board 3.5″ для A4 B5 Y921OE.
**Режим:** DEMO на экране; LIVE — JSON UART0 (CP2102) с Kali.
**Проверено:** MicroPython на Pico (`2e8a:0005`), залиты `lcd.py`/`bc.py`/`main.py`.
**Плата:** `Платы и модули/Pico-Eval-Board/`.

## Фокус (2026-08-14, Pico-Eval-Board)

**Папка:** `Платы и модули/Pico-Eval-Board/` — Waveshare, IPS 3.5″ ILI9488 480×320 + XPT2046, ICM-20948, SDIO, PCM5101A.
**Доки:** `PINOUT.md`, `TECH_SUMMARY.md`. Схема и демо в `downloads/` / `extracted/`.
**Проверено:** схема PDF 771 KB, demo zip 6.9 MB распакован; даташит PCM5101A с wiki не скачался (таймаут).
**БК Audi:** `Проекты/audi_bc_pico/` — DEMO на этом экране.

## Фокус (2026-08-13, дашборд Pi 5)

**Один экран:** https://91.215.61.76:5679/webhook/pi5 и PWA вкладка **Малинка 5** (`/sites/malinka/`).
**Сценарий:** `bS8g9qac1sGRGl0X` (published) — единственный; три ленты: страница, Google, сервисы Pi 5. Остальные 11 в архиве.
**Проверено:** webhook 200 HTML, `/malinka-dash` 200, `/api/sites` содержит malinka.

## Фокус (2026-08-13, n8n Google)

**Проект:** `Проекты/n8n/`. Credentials: Sheets / Drive / Gmail / Calendar.
**Карта:** `ilCWoMl0r96yGVXw`. Просмотр: UPS, расходники, SMS, ОТК АКБ, Коммуналка папки/файлы, Музыка/учёба, Gmail, календарь — все execute success.
**Скрипты хоста не отключал.** PDF с почты `qUxdqEgCEdQ6BOFo` — черновик.

## Фокус (2026-08-13, n8n)

**Проект:** `Проекты/n8n/` — self-hosted n8n **2.34.5**, Docker `n8n`, `restart: unless-stopped`.
**URL:** WAN https://91.215.61.76:5679/ ; LAN https://10.1.30.126:5679/ ; HTTP LAN :5678.
**Проверено:** WAN `/healthz` 200, HTML 200. Проброс Keenetic electro+office **5679**. Голый **5678 на WAN не открыт**.
**MCP:** Cursor подключён (`~/.cursor/mcp.json` → `n8n`, `/mcp-server/http`).
**PWA Сайты:** вкладка **n8n** → `/sites/n8n/` (прокси `:5678`). Проверено: HTML/REST/HTTPS 200, health up. SW **v71**. Ctrl+F5.

## Фокус (2026-08-12, VPN_Server)

**Причина:** техработы Fornex — обновление сети США (Dallas), **полное отключение** услуг USA **09:00–15:00 МСК** 12.08.2026. VPS `89.127.199.6` в US → сеть мертва, reboot fail ожидаем.
**Действие:** ждать до ~15:00; watcher `vpn-wait-fix2` поднимет `x-ui` после SSH.
**Не чинить reboot/Stop-Start** до конца окна.

## Фокус (2026-08-12, Cursor Pi 5)

**Проверено:** `cursor-upgrade-pi5.sh` — IDE **3.15.6**, Agent CLI **2026.08.11-e8db854** (уже latest).

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