# CHANGELOG

## 2026-10-31 — JK АКБ 4S 230Ah: кнопка короткого опроса

- Дашборд **JK АКБ 4S 230Ah** (`/jk-akb-4s-230/home`): кнопка **«Опросить батарею»**.
- `input_button.jk4s_poll` + `shell_command.jk4s_poll_request` → `jk4s_poll.request`.
- Хост: `jk4s-ha-poll.path` / `jk4s_ha_poll.sh` → SSH Pi3 `sudo run_once.sh` → scp `jk4s.json`; после опроса BLE отключается.
- Сенсоры статуса: `sensor.jk4s_poll_state`, `sensor.jk4s_poll_status`.
- Периодический `jk4s-ble-logger.timer` на Pi3 — **disabled**.

## 2026-10-31 — JK АКБ 4S 230Ah (гараж) в HA

- Дашборд **JK АКБ 4S 230Ah** (`/jk-akb-4s-230/home`) — стиль как ANT BMS24C.
- Пакет `config/packages/jk4s.yaml`, reader `host_status/jk4s_read.py`.
- Данные: BLE с Pi 3 (`AKB-4S-230`, MAC `C8:47:80:53:0F:B6`) → `jk4s.json` (логгер `bms-tools/jk4s_ble_logger.py`).

## 2026-10-07 — ESP Camera (офис) убрана из HA

- Главная панель: удалена markdown-карточка «ESP Camera (офис)» (камера offline с 2026-08).
- `.storage/homekit_controller-entity-map`: удалены сиротские сопряжения ESP Camera `5D:11:A4:87:61:46`, `33:FF:B7:13:B1:F6` (интеграций под ними не было); остался только Switch.
- `configuration.yaml`: удалён закомментированный блок `ESP Camera HK` (порт 21065).
- Скрипты сопряжения `scripts/*esp-camera*` оставлены — на случай возврата камеры. Бэкап: agent-change от 14:3x 2026-10-07.

## 2026-10-07 — Камера электроцеха: движение, push, Apple «Дом»

- Generic Camera удалена; `camera.elektrotsekh` теперь от интеграции **Hikvision** (та же камера 10.1.30.64), датчик движения `binary_sensor.elektrotsekh_dvizhenie`.
- Новый пакет `config/packages/hikvision_elektrotsekh.yaml`: `input_boolean.elektrotsekh_motion_notify` + автоматизация «Электроцех: движение → push на iPhone» (`notify.mobile_app_aineti`, снимок камеры, time-sensitive, пауза 2 мин).
- Мост HomeKit «HASS Bridge» (UI-запись `02271e20…`): в опциях добавлена камера с `linked_motion_sensor` и `video_codec: copy`; в `.storage/core.config_entries` снят `exclude_accessory_mode` (иначе мост отбрасывает камеры). Проверено диагностикой: аксессуар «Камера электроцех» со службами Camera RTP ×3 + Motion.
- `configuration.yaml`: в YAML-блоке `homekit:` пояснение, что UI-мост этим YAML не настраивается.
- На камере исключено LED-табло из зоны детекции (ложные срабатывания). Бэкапы: agent-change `20261007T141919`, `20261007T142645`.

## 2026-10-07 — Камера Hikvision электроцеха

- Интеграция **Generic Camera** (config entry «Камера электроцех»): RTSP `rtsp://10.1.30.64:554/Streaming/Channels/101` (TCP), снимок `http://10.1.30.64/ISAPI/Streaming/channels/101/picture`, digest, `admin`; сущность `camera.elektrotsekh`.
- `configuration.yaml`: добавлен `stream:` (без него только снимки, без живого видео HLS).
- Главная панель «Обзор» → вид Home: первой карточкой `picture-entity` камеры (`camera_view: auto`).
- Проверено: снимок 1920×1080 через `camera_proxy`, HLS-плейлист H.264. Справка по камере: `Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md`.

## 2026-10-01 — ANT BMS24C: подсветка крайних ячеек

- `dashboards/ant-bms-24c.yaml`, карточка «Ячейки»: шаблон-цикл по 13 ячейкам; самая высокая — **красная** (`#e53935`), самая низкая — **синяя** (`#1e88e5`); при равных значениях без подсветки. «Мин»/«Макс» в шапке тем же цветом.

## 2026-10-01 — ANT BMS24C: разброс ячеек в «Сейчас»

- Установлен **card-mod v4.2.1**: `config/www/card-mod.js`, подключён через `frontend: extra_module_url` в `configuration.yaml`.
- `dashboards/ant-bms-24c.yaml`, карточка «Сейчас»: строка «Разброс ячеек» (`sensor.ant24c_cell_delta`, мВ) — зелёная иконка до 20 мВ, **красная + жирный** при > 20 мВ.

## 2026-10-01 — ANT BMS24C: точность напряжений

- Реестр сущностей (`.storage/core.entity_registry`, `options.sensor.display_precision`): напряжение пакета, пик/пол, мин/макс лога, `*_graph`/`*_smooth` — **1 знак**; ячейки 1–13 и `cell_min`/`cell_max` — **3 знака** (раньше HA округлял `voltage` до целого).
- `dashboards/ant-bms-24c.yaml`: в карточке «Ячейки» формат `'%.3f'` (4.180 не превращается в 4.18).

## 2026-09-10 — Deye «Зарядка»: убрано из HA

- Stick без UART к инвертору не даёт телеметрии — пакет `deye_zaryadka.yaml`, дашборд и скрипты `deye_zaryadka_*` **удалены**.
- Мониторинг «Зарядки» только через Solarman Business / облако (если подключите stick к инвертору позже).

## 2026-09-07 — ANT BMS24C: графики без «иголок»

- **Причина:** при offline логгер писал `pack_V/soc/… = null`, а HA `command_line` делал `or 0` → на history-graph выбросы 0↔реал (~3900 нулей в истории).
- **Логгер** (`bms-tools/ant24c_logger.py`): при offline держит последние валидные pack/ток/SOC/ячейки.
- **HA:** `host_status/ant24c_read.py` — нет значения → exit 1 (unavailable); template `*_graph` с отсечением выбросов; дашборд → graph-сенсоры; из recorder удалены нулевые точки.
- **Файлы:** `config/packages/ant24c.yaml`, `config/dashboards/ant-bms-24c.yaml`.

## 2026-08-24 — HA не стартовал после reboot (gpiochip0)

- **Причина:** после reboot 13:54 контейнер `homeassistant` Exit 255 — в `docker-compose.yml` был device `/dev/gpiochip0`, которого на Pi 5 (ядро 6.12) нет (`gpiochip11–15`).
- **Исправлено:** убран `gpiochip0`; оставлены `gpiochip15` + `gpiomem0`.
- **Проверено:** `docker compose up -d` → Up; `http://127.0.0.1:8123/` → **200**.

## 2026-08-18 — ANT BMS24C: напряжения всех ячеек на дашборде

- `config/packages/ant24c.yaml`: добавлены сенсоры `cell_min/cell_max/cell_delta` и 13 сенсоров `Cell N Voltage`.
- `config/dashboards/ant-bms-24c.yaml`: ячейки собраны в **одну** markdown-карточку: `min / max / delta` и все 13 значений с точностью до `0.001 В`.
- `bms-tools/ant24c_logger.py`: в `host_status/ant24c.json` публикуется массив `cells_V` и `cell_count` для Home Assistant; переключатель балансира теперь считается успешным только после проверки свежего снимка BMS.

## 2026-08-04 — Обзор: «Объект не найден» + график CPU

- **Причина жёлтых карточек:** `camera.esp_camera` / вспышка / identify отсутствуют (камера `10.1.30.129` offline, pairing сброшен); lovelace всё ещё ссылался на них. HomeKit `ESP Camera HK` падал при старте.
- **Сделано:** на Обзоре — `history-graph` Pi5 CPU 24ч; битые карточки камеры → markdown с инструкцией pairing; из `configuration.yaml` и config entry убран ESP Camera HK / `light.esp_camera_flash`.
- **Когда камера вернётся:** `finish-esp-camera-ha.sh` или HomeKit Device код `111-11-111`, затем раскомментировать блок ESP Camera HK.

## 2026-08-04 — график CPU temp Pi5 «залипал»

- **Причина:** cron `publish_cpu_temp.sh` с путём `Apple HomeKit accessory` **без кавычек** — команда рвалась на `…/Apple`, файл `cpu_temp.txt` не обновлялся с 31.07 (залип на 38.4 °C при живых ~47 °C).
- **Исправлено:** systemd timer `pi5-ha-cpu-temp.timer` + обёртка `~/bin/pi5-ha-publish-cpu-temp.sh`; сломанный cron убран; пути на `/home/pi/Documents/…`.
- **Проверка:** `sensor.pi5_cpu_temperature` → 48.3; файл обновляется; timer active.

## 2026-06-23 — legacy VPN mesh

- С хоста и Docker окончательно сняты остатки mesh VPN (пакет, контейнер, образы).

## 2026-06-15 — камера 2 (elektro): прошивка как ainet + HA pairing

- `sdkconfig.defaults.elektro` — профиль как `ainet` (face recognition, GPIO0 reset), Wi‑Fi `ELEKTRO_`.
- Полная прошивка @ 115200: MAC `24:62:ab:dc:81:30`, IP `10.1.30.129`.
- HA pairing: HomeKit ID `45:2D:4B:29:00:2A`, entry `014F9AD2E0DCE1498EBDC6066B`.
- Сущности: `camera.esp_camera`, `light.esp_camera_flash`, `button.esp_camera_identify`.
- `scripts/flash-elektro-wait.sh` — 5 попыток USB вместо 180 (`FLASH_MAX_TRY`).

## 2026-06-11 — ESP Camera: автопairing + fix прошивки (OOM face)

- Прошивка `elektro`: отключены face recognition и сброс pairing на GPIO0 (как garage).
- Скрипт `scripts/flash-and-pair-esp-camera.sh` — прошивка + pairing по IP без UI.
- Причина нестабильности: `matrix3du` OOM → отвал Wi‑Fi/HomeKit; нужна новая прошивка на устройстве.

## 2026-06-11 — repair HA Pi 5 перед pairing ESP Camera

- `scripts/repair_ha_pi5.sh` — очистка битых esp_camera в `.storage`, подъём `homeassistant`.
- Дашборд: вместо «Объект не найден» — карточка с инструкцией pairing (HomeKit Device, код 111-11-111).

## 2026-06-11 — вторая ESP32-CAM в HA (скрипты pairing)

- `scripts/pair_esp_camera_ha.py` — сопряжение ESP Camera по IP (код `111-11-111`) → `homekit_controller`.
- `scripts/pair-second-esp-camera.sh` — вторая камера MAC `24:62:ab:dc:81:30`, очистка orphan, рестарт HA.

## 2026-06-08 — обновление Home Assistant 2024.3.3 → 2026.6.1

- `docker-compose.yml`: тег образа `2026.6.1`.
- Бэкап конфига: `backups/pre-update-2026.6.1-20260608-142502/config-full.tar.gz`.
- На хосте: удалён конфликтующий `docker.io` 20.10, активен `docker-ce` 29.5.3 (старый Docker не тянул слои новых образов).
- Проверка: UI `:8123` HTTP 200, `.HA_VERSION` = `2026.6.1`, миграции recorder прошли.

## 2026-05-29 — мониторинг Pi 5 в Home Assistant

- `scripts/publish_pi5_host_status.sh` + cron (раз в минуту) → `config/host_status/*.txt`.
- `config/configuration.yaml`: сенсоры `Pi5 CPU Temperature`, `Pi5 Core Voltage`, `Pi5 Throttling`, `Pi5 Undervoltage`.
- `scripts/install-pi5-ha-host-status.sh` — установка cron и рестарт контейнера.
- Дашборд lovelace: карточка **Pi5** с температурой CPU.

## 2026-05-26 — пищалка HAT (BCM 13)

- **`switch.gpio13`** убран из HASS Bridge, **`configuration.yaml`**, lovelace; в Switch **Gpio13** по умолчанию выключен. См. `Платы и модули/Многофункциональная плата расширения Raspberry Pi 3B+ 3B/TECH_SUMMARY.md`.

## 2026-05-25 — HomeKit + HA стабильно на Pi 5

- **`switch.gpio13`** (было `gpio12`): HomeKit **Gpio13**, BCM **13** (CH3); позже отключён (пищалка на HAT).
- **`switch.gpio12`**: реле на **BCM 13** (CH3), BCM **12** — только микрофон I2S; правки в **`../Switch/app/config.py`**; сущность HA без переименования.
- **Восстановлен `switch.gpio12`**: **`../Switch/app/config.py`**, **`../Switch/app/main.py`** — аксессуар **Gpio12** (BCM 12) снова на **Pi5 Bridge**; **`config/configuration.yaml`**, **HASS Bridge**, дашборд **Pi5 Bridge** — три переключателя; `reload_ha_homekit.sh`.
- *(ранее)* снят Gpio12 под I2S SCK INMP441 — откат по запросу пользователя.
- `Switch/app/main.py`: раздельно `listen_address` (0.0.0.0) и `advertised_address` (LAN IP) — mDNS Pi5 Bridge больше не `0.0.0.0`.
- `configuration.yaml`: HASS Bridge только `include_entities` (переключатели с моста).
- Скрипты: `scripts/sync_network_identity.sh`, `cleanup_ha_orphans.sh`; `pi5_up.sh` — полный цикл подъёма.

## 2026-05-20

- Каталог перенесён в **`Проекты/Apple HomeKit accessory/home_assistant/`** (объединение с Switch).
- **`.storage/core.config_entries`**: в **HASS Bridge** в `include_entities` добавлен **`switch.gpio12`** (раньше были только `switch.switch_2` и `switch.led2_2` — поэтому в приложении «Дом» третий переключатель не появлялся).
- **`.storage`**: третий канал моста — **`switch.gpio12`** (BCM 12); дашборд **Pi5 Bridge**: `switch.switch_2`, `switch.led2_2`, `switch.gpio12`.
- **`config/configuration.yaml`**: убраны сломанный `command_line` Led2 и обёртки `light`/`customize` (конфликт GPIO 16 с контейнером `switch`); второй переключатель — только через **HomeKit Controller** (мост `Pi5 Bridge`, аксессуар **Led2**). В фильтр `homekit` добавлен домен **`switch`**.
- **`.storage/core.entity_registry`**: удалены нерабочие `switch.switch` (привязка к aid моста без On), `switch.led2` (command_line), `light.led`; рабочие сущности — **`switch.switch_2`** (реле BCM 19), **`switch.led2_2`** (GPIO 16).

## 2026-05-14

- Добавлено правило Cursor **`.cursor/rules/docker-cleanup-after-rebuild.mdc`**: после пересборки Docker-образов выполнять очистку кэша BuildKit и висячих образов по глобальному стандарту воркспейса (`Документы/.cursor/rules/core-standards-and-workflow.mdc`).
- Скрипт **`Документы/.cursor/scripts/docker-post-rebuild-cleanup.sh`**: цикл `docker builder prune -f` до `Total reclaimed space: 0B`, затем `docker image prune -f`; глобальные правила обновлены под запуск этого скрипта агентом после пересборки.

## 2026-05-06 (Pi 5: приоритет Wi‑Fi ELEKTRO_ → AiNET)

- В NetworkManager на Pi 5 выставлены приоритеты автоподключения: `ELEKTRO_` = `100` (основная сеть), `netplan-wlan0-AiNET` = `10` (резерв).
- Если `ELEKTRO_` недоступна, система поднимает `AiNET` автоматически.
- `README.md` дополнен разделом проверки приоритетов Wi‑Fi через `nmcli`.


- **`README.md`:** разделы доступа и диагностики переведены на LAN; инструкции по tailnet убраны как неактуальные.

## 2026-05-04 (фикс HomeKit Bridge на Pi 5)
- В `config/configuration.yaml` добавлен YAML-блок `homekit` для стабильного моста: `name: HASS Bridge`, `port: 21064`, `ip_address: 0.0.0.0`, `advertise_ip: 10.1.30.126`, фильтр доменов `cover/switch`.
- Задан фиксированный PIN моста в YAML: `126-30-126` (удобно для повторного сопряжения после сброса).
- Очищены state-файлы HomeKit Bridge (`/config/.storage/homekit.*.{state,aids,iids}`) с бэкапом в `/config/.storage/homekit_bridge_backup_*`, затем перезапущен контейнер `homeassistant`.

## 2026-05-04 (снова включён HA на Pi 5)
- В **`docker-compose.yml`** возвращён **`restart: unless-stopped`**, выполнен **`docker compose pull` / `up -d`** — контейнер **`homeassistant`** запущен; **`README.md`** обновлён.

## 2026-05-04
- На **Pi 5** контейнер **`homeassistant` ранее** был остановлен и удалён; в **`docker-compose.yml`** временно стояло **`restart: "no"`** (служба после ребута сама не стартовала).

## 2026-05-03
- В `README.md` отмечены политика `restart: unless-stopped` и ссылки на Pi 3: **`Проекты/Raspberry_Pi_3_HomePortable/`** и `Проекты/Apple HomeKit accessory/README_Raspberry_Pi_3_Docker.md`.

## 2026-04-23
- Диагностирована ошибка добавления HomeKit Bridge в приложение "Дом" на iPhone: причина в блокировке порта `21065/tcp` фаерволом `ufw`.
- В `ufw` добавлены правила для HomeKit Bridge и обнаружения устройств: `21065/tcp` и `5353/udp` (IPv4/IPv6).
- Подтверждено, что контейнер `homeassistant` продолжает работать после обновления сетевых правил.
- Временная секция `logger` удалена из `config/configuration.yaml` после проверки; контейнер перезапущен.
- По ошибке iOS-приложения `Response status code was unacceptable: 500` собран traceback из контейнера: падение в `homeassistant.components.mobile_app.http_api` на `homeassistant.components.cloud.CloudNotConnected`.
- Создана резервная копия реестра config entries: `config/.storage/core.config_entries.bak_2026-04-23-cloudfix`.
- Для обхода `CloudNotConnected` отключена системная запись `cloud` в `config/.storage/core.config_entries` (`disabled_by: "user"`), контейнер перезапущен.
- Попытка обновить `homeassistant/home-assistant` до `stable` отложена: текущая проблема Docker Hub (`EOF` при обращении к `registry-1.docker.io`), поэтому конфигурация `docker-compose.yml` возвращена на `2024.3.3`.
- Выявлена сетевая причина таймаутов `hass_nabucasa`: из контейнера HA `IPv4` до `remote.nabucasa.com` работает, `IPv6` дает `Network unreachable`.
- Для обхода добавлен `gai.conf` (приоритет IPv4) и подключен в контейнер как `/etc/gai.conf` через `docker-compose.yml`; контейнер пересоздан.
- Для исправления `500` при входе iOS app очищено состояние Home Assistant Cloud в `config/.storage/cloud` (отключены cloudhooks и логин-состояние), создан бэкап `config/.storage/cloud.bak_2026-04-23-mobileapp500`.
- После перезапуска контейнера в контрольном окне логов отсутствуют новые traceback `mobile_app/http_api` / `CloudNotConnected`.
- Выявлено, что `cloud` продолжал подниматься через `default_config`, поэтому `configuration.yaml` переведен на явный минимальный набор интеграций без cloud: `frontend`, `config`, `history`, `logbook`, `map`, `ssdp`, `zeroconf`, `sun`, `system_health`, `mobile_app`.
- После перезапуска в мониторинге логов за 40 секунд не зафиксировано `hass_nabucasa`, `CloudNotConnected` и `Error handling request` для `mobile_app`.

## 2026-04-21
- Создан Docker-проект `home_assistant` с `docker-compose.yml`.
- `Home Assistant` переведен на контейнерный запуск (`homeassistant/home-assistant:2024.3.3`) с `network_mode: host`.
- Для конфигурации контейнера используется каталог `/home/pi/.homeassistant`.
- Удалены старые systemd-сервисы `home-assistant.service` и окружения `Home Assistant Core` в `/srv`.
- Удален `Homebridge`: сервис, глобальные npm-пакеты и его конфигурационные каталоги.
- Конфигурация `Home Assistant` перенесена в папку проекта: `Проекты/home_assistant/config`.
- В `docker-compose.yml` обновлен volume `/config` на путь внутри проекта.
- Старый каталог `~/.homeassistant` перенесен в `Проекты/home_assistant/backup/homeassistant_legacy_home_dir`.
- Удалена backup-папка `Проекты/home_assistant/backup/homeassistant_legacy_home_dir` после проверки успешного запуска контейнера с новой конфигурацией.
- В `config/configuration.yaml` добавлены `default_config:` и `mobile_app:` для корректной регистрации официального iOS-приложения Home Assistant.
- Контейнер `homeassistant` перезапущен после изменения конфигурации.
- Проверена интеграция `Switch` через HomeKit: подтверждено, что `homekit_controller` не поддерживает YAML-настройку в текущей версии HA.
- Временная строка `homekit_controller:` удалена из `config/configuration.yaml`, Home Assistant возвращен в рабочее состояние после перезапуска.
- Выполнена очистка дублей `Switch` в `.storage`: удалены `switch.switch_2`, `button.switch_identify_2`, лишнее устройство и лишняя `homekit_controller` config entry.
- Оставлен один активный `Switch` (`switch.switch` + `button.switch_identify`); ссылки на удаленные дубли в `lovelace` очищены.
- Перед очисткой создана резервная копия реестров в `config/.storage_backup_cleanup/`.
- По запросу удален `Switch` из Home Assistant полностью: очищены сущности, устройство, `homekit_controller` config entry, pairing map и ссылки в `lovelace`.
- `config/configuration.yaml` приведен к минимальному виду: оставлены только `default_config:` и `mobile_app:`.
- Home Assistant перезапущен после упрощения конфигурации.
