# Журнал изменений агентов (общий для всех)

**Назначение:** Cursor, Claude Code, OpenCode и Telegram-бот видят, что уже меняли предшественники, и могут откатить файлы.

## Перед задачей (обязательно)

1. `.cursor/chat.md` и `.cursor/CHAT_HANDOFF.md`
2. **Этот файл** — последние записи сверху
3. `CHANGELOG.md` активного проекта под `Проекты/`

## После правок файлов (обязательно)

```bash
bash Документы/.cursor/scripts/agent-change-backup.sh --agent cursor --project ai_assistant --note "кратко что сделано" путь/к/файлу ...
```

Скрипт создаёт снимок в `.cursor/backups/<id>/` и дописывает запись ниже.

## Откат

| Ситуация | Команда |
|----------|---------|
| Последний снимок | `bash Документы/.cursor/scripts/agent-change-revert.sh --last` |
| По ID снимка | `bash Документы/.cursor/scripts/agent-change-revert.sh 20260525T120000` |
| Проект с git | `git -C Проекты/komunalka status` / `git checkout -- <файл>` |
| Старый контекст без снимка | `.cursor/chat.md`, `CHANGELOG.md` проекта, бэкапы `*.bak` рядом с файлом |

Список снимков: `ls -1t Документы/.cursor/backups/`

---

## Записи (новые сверху)

### 2026-10-13 18:11 — manual PDF + TECH_SUMMARY

- **Агент:** cursor
- **Проект:** aqara-e1
- **Файлы:** \`Платы и модули/Aqara_Camera_E1_CH-C01E/README.md\`, \`Платы и модули/Aqara_Camera_E1_CH-C01E/TECH_SUMMARY.md\`, \`Платы и модули/Aqara_Camera_E1_CH-C01E/source_url.txt\`, \`Платы и модули/Aqara_Camera_E1_CH-C01E/downloads/Camera-E1_User-Manual_V7_2023-11.pdf\`
- **Снимок:** `.cursor/backups/20261013T181140/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261013T181140`


### 2026-10-12 12:25 — Русский мануал Adion восстановлен и переименован

- **Агент:** cursor
- **Проект:** Adion_Expert_6kW_Twin
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/downloads/ADION_AXPERT_KING_II_6.0kW_TWIN-B_manual_RU.pdf\`, \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/source_url.txt\`, \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/PINOUT.md\`, \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/НАСТРОЙКА_ЭКСПЛУАТАЦИЯ.md\`, \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/download_report.json\`, \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20261012T122507/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261012T122507`


### 2026-10-12 08:56 — UART bootloop CH-C01E, заметка и контекст

- **Агент:** cursor
- **Проект:** aqara-e1
- **Файлы:** \`Платы и модули/Aqara_Camera_E1_CH-C01E/README.md\`, \`Платы и модули/Aqara_Camera_E1_CH-C01E/notes/UART_BOOTLOOP_2026-10-12.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20261012T085622/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261012T085622`


### 2026-10-08 20:49 — Удалено слово межевание; приложение 2 переименовано в чертёж территории

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`, \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`, \`Пушкина_29/Приложение 2 - Чертёж территории - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T204907/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T204907`


### 2026-10-08 20:45 — Перед удалением слова межевание

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`, \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`, \`Пушкина_29/Приложение 2 - Чертёж межевания - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T204528/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T204528`


### 2026-10-08 20:39 — Добавлена Меджитова А.Н., кв. 10; таблица пересортирована

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`
- **Снимок:** `.cursor/backups/20261008T203927/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T203927`


### 2026-10-08 20:37 — Перед добавлением Меджитовой А.Н., кв. 10

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`
- **Снимок:** `.cursor/backups/20261008T203735/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T203735`


### 2026-10-08 20:21 — Исправлены инициалы: Аверина Е.И.

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`
- **Снимок:** `.cursor/backups/20261008T202128/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T202128`


### 2026-10-08 20:21 — Перед исправлением инициалов Авериной Е.Н. → Е.И.

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`
- **Снимок:** `.cursor/backups/20261008T202109/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T202109`


### 2026-10-08 20:13 — Добавлена 8-я стойка бельевой сушилки под снос; схема и обращение

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`, \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T201340/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T201340`


### 2026-10-08 20:11 — Перед добавлением 8-й стойки бельевой сушилки под снос

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`, \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T201155/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T201155`


### 2026-10-08 19:52 — Кирпичная клумба П укорочена точно до уровня Д1

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T195214/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T195214`


### 2026-10-08 19:51 — Перед укорачиванием клумбы до уровня Д1

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T195108/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T195108`


### 2026-10-08 19:33 — Кирпичная клумба П продлена выше дерева Д1

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T193337/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T193337`


### 2026-10-08 19:31 — Перед продлением кирпичной клумбы П за Д1

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T193133/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T193133`


### 2026-10-08 18:51 — Явные чёрные рамки таблицы подписей для мобильного просмотра

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`
- **Снимок:** `.cursor/backups/20261008T185100/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T185100`


### 2026-10-08 18:50 — Перед явными рамками таблицы подписей

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`
- **Снимок:** `.cursor/backups/20261008T185022/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T185022`


### 2026-10-08 18:23 — Финал: аккуратная схема без С2, обращение на 2 страницы

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`, \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20261008T182353/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T182353`


### 2026-10-08 18:20 — Аккуратная пересборка схемы без С2 и исправление формулировок

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`, \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T182058/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T182058`


### 2026-10-08 18:11 — С2 не трогать, кирpичная клумба

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`, \`Пушкина_29/Приложение 1 - Схема двора - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T181142/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T181142`


### 2026-10-08 15:20 — Опоры ЛЭП под замену: схема + п.3 обращения

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`
- **Снимок:** `.cursor/backups/20261008T152031/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T152031`


### 2026-10-08 14:50 — Новый проект зеркала Пушкина_29 → Drive + правило

- **Агент:** cursor
- **Проект:** drive-folder-sync
- **Файлы:** \`Проекты/drive-folder-sync\`, \`.cursor/rules/pushkina29-drive-sync.mdc\`, \`Проекты/README.md\`
- **Снимок:** `.cursor/backups/20261008T145049/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T145049`


### 2026-10-08 14:39 — Деревья на схеме + текст обращения

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`, \`Пушкина_29/Схема двора (межевание) - Пушкина 29.pdf\`
- **Снимок:** `.cursor/backups/20261008T143917/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T143917`


### 2026-10-08 14:17 — Правки обращения + схема двора

- **Агент:** cursor
- **Проект:** Пушкина_29
- **Файлы:** \`Пушкина_29/Обращение - Пушкина 29.docx\`
- **Снимок:** `.cursor/backups/20261008T141717/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T141717`


### 2026-10-08 07:48 — resolve() для запуска через симлинки ~/.local/bin

- **Агент:** cursor
- **Проект:** bybit
- **Файлы:** \`.cursor/scripts/bybit-balance.py\`, \`.cursor/scripts/bybit-dashboard.py\`, \`.cursor/scripts/bybit-recommendations.py\`, \`.cursor/scripts/bybit-spot-order.py\`, \`.cursor/scripts/bybit-watch.py\`
- **Снимок:** `.cursor/backups/20261008T074804/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261008T074804`


### 2026-10-07 18:02 — xray nightly update timer

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/xray-nightly-update.sh\`, \`Проекты/ai_assistant/scripts/install-xray-nightly-update-timer.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20261007T180259/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T180259`


### 2026-10-07 15:10 — 3x-ui client Владимир + vpn-guide

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`vpn-guide.md\`
- **Снимок:** `.cursor/backups/20261007T151029/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T151029`


### 2026-10-07 14:30 — HA: удаление ESP Camera (карточка, кэш HK, YAML-комментарий)

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/lovelace.lovelace\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/homekit_controller-entity-map\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/configuration.yaml\`
- **Снимок:** `.cursor/backups/20261007T143018/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T143018`


### 2026-10-07 14:29 — README: аудио

- **Агент:** cursor
- **Проект:** Hikvision
- **Файлы:** \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md\`
- **Снимок:** `.cursor/backups/20261007T142934/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T142934`


### 2026-10-07 14:27 — Hikvision: движение+push+HomeKit, доки

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`, \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/packages/hikvision_elektrotsekh.yaml\`
- **Снимок:** `.cursor/backups/20261007T142745/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T142745`


### 2026-10-07 14:26 — HA: до снятия exclude_accessory_mode у HASS Bridge

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/core.config_entries\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/configuration.yaml\`
- **Снимок:** `.cursor/backups/20261007T142645/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T142645`


### 2026-10-07 14:19 — HA: до датчика движения Hikvision и HomeKit

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/configuration.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/core.entity_registry\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/core.config_entries\`
- **Снимок:** `.cursor/backups/20261007T141919/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T141919`


### 2026-10-07 14:16 — HA Pi5: камера Hikvision camera.elektrotsekh + stream

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/configuration.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`, \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md\`
- **Снимок:** `.cursor/backups/20261007T141613/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T141613`


### 2026-10-07 14:14 — HA: до добавления камеры Hikvision

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/lovelace.lovelace\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/core.entity_registry\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/core.config_entries\`
- **Снимок:** `.cursor/backups/20261007T141453/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T141453`


### 2026-10-07 14:12 — README: пароль, NTP/MSK

- **Агент:** cursor
- **Проект:** Hikvision_DS-2CD2122FWD-IS
- **Файлы:** \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md\`
- **Снимок:** `.cursor/backups/20261007T141229/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T141229`


### 2026-10-07 14:11 — Перепрошивка 5.5.82_190909 через TFTP, README, скрипты

- **Агент:** cursor
- **Проект:** Hikvision_DS-2CD2122FWD-IS
- **Файлы:** \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md\`, \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/scripts/hikvision_tftpd.py\`, \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/scripts/uboot_catch.py\`
- **Снимок:** `.cursor/backups/20261007T141120/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T141120`


### 2026-10-07 13:34 — README: раздел Доступ

- **Агент:** cursor
- **Проект:** Hikvision_DS-2CD2122FWD-IS
- **Файлы:** \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md\`
- **Снимок:** `.cursor/backups/20261007T133435/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T133435`


### 2026-10-07 13:33 — IP камеры 10.1.30.64

- **Агент:** cursor
- **Проект:** Hikvision_DS-2CD2122FWD-IS
- **Файлы:** \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md\`
- **Снимок:** `.cursor/backups/20261007T133339/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T133339`


### 2026-10-07 13:31 — UART-проверка камеры, README

- **Агент:** cursor
- **Проект:** Hikvision_DS-2CD2122FWD-IS
- **Файлы:** \`Платы и модули/Hikvision_DS-2CD2122FWD-IS/README.md\`
- **Снимок:** `.cursor/backups/20261007T133143/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T133143`


### 2026-10-07 08:15 — JK PDF: QR на jkcfg в Google Drive

- **Агент:** cursor
- **Проект:** Платы и модули
- **Файлы:** \`Платы и модули/BMS/JK_B2A20S20P/scripts\`, \`Платы и модули/BMS/JK_B2A20S20P/generated\`, \`Платы и модули/BMS/JK_B2A20S20P/notes/configs/ELTAVR_48V230Ah_16S_template\`, \`Платы и модули/BMS/JK_B2A20S20P/README.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20261007T081548/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T081548`


### 2026-10-07 08:06 — JK B2A20S20P: PDF шаблона настроек

- **Агент:** cursor
- **Проект:** Платы и модули
- **Файлы:** \`Платы и модули/BMS/JK_B2A20S20P/scripts\`, \`Платы и модули/BMS/JK_B2A20S20P/generated\`, \`Платы и модули/BMS/JK_B2A20S20P/README.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20261007T080625/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261007T080625`


### 2026-10-06 16:57 — PWA без стилей при обрыве: sw v75 network-first для страницы/style.css, шрифты Google неблокирующие

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/pwa/app.js\`
- **Снимок:** `.cursor/backups/20261006T165728/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261006T165728`


### 2026-10-06 14:10 — Тарифы: текущий тариф + мини-график истории на карточках, data/tariffs.json, /api/tariffs

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/tariffs.js\`, \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/styles.css\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20261006T141043/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261006T141043`


### 2026-10-06 13:59 — Тарифы: текущий + история + график (до правок)

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/styles.css\`, \`Проекты/komunalka/index.html\`
- **Снимок:** `.cursor/backups/20261006T135925/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261006T135925`


### 2026-10-06 10:29 — K8-K16 освобождены

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`
- **Снимок:** `.cursor/backups/20261006T102919/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261006T102919`


### 2026-10-06 10:24 — M3K LED: карта #1951-1956 = индикаторы M350; K14 сканер

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/generated/m3k_led_scan\`
- **Снимок:** `.cursor/backups/20261006T102408/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261006T102408`


### 2026-10-06 10:18 — M3K = K8-K16, заметка о синхронизации LED с выходом

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`
- **Снимок:** `.cursor/backups/20261006T101846/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261006T101846`


### 2026-10-06 10:16 — K8-K16: только LED #1951-#1959

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/generated/k8k16_led\`
- **Снимок:** `.cursor/backups/20261006T101619/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261006T101619`


### 2026-10-06 10:11 — K3-K7: только LED #1946-#1950, пар. 212-216=0

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/generated/k3k7_led\`
- **Снимок:** `.cursor/backups/20261006T101149/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261006T101149`


### 2026-10-05 16:33 — DM856: раздел ProTuner/RS232

- **Агент:** cursor
- **Проект:** Leadshine_DM856
- **Файлы:** \`Платы и модули/Leadshine_DM856/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20261005T163316/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T163316`


### 2026-10-05 16:27 — K1 = вкл/выкл OUT20 (СОЖ) + LED #1944

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/generated/k1_toggle/SYSDISK/key-1.nc\`
- **Снимок:** `.cursor/backups/20261005T162718/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T162718`


### 2026-10-05 16:26 — K2 = вкл/выкл OUT19 (обдув датчика длины) + LED #1945

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/generated/k2_toggle/SYSDISK/key-2.nc\`
- **Снимок:** `.cursor/backups/20261005T162632/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T162632`


### 2026-10-05 16:25 — K2 = вкл/выкл OUT20 (СОЖ+обдув) + светодиод #1945

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/generated/k2_toggle/SYSDISK/key-2.nc\`
- **Снимок:** `.cursor/backups/20261005T162537/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T162537`


### 2026-10-05 16:22 — M350 выходы: #789=19 (обдув замера), #730=20 (СОЖ M8)

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/generated/outputs_fix/SYSDISK/setting\`
- **Снимок:** `.cursor/backups/20261005T162221/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T162221`


### 2026-10-05 16:19 — SPINDLE: ACM/VS0/COM/FOR; OUT20 — реле вместе с M3

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`
- **Снимок:** `.cursor/backups/20261005T161910/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T161910`


### 2026-10-05 16:15 — Карта выходов M350 по фото: подключены только OUT19/OUT20, OUT18 пуст

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`
- **Снимок:** `.cursor/backups/20261005T161555/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T161555`


### 2026-10-05 16:04 — MACHINE.md: клапаны OUT18/OUT19, M50-M91, M7 не работает

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`
- **Снимок:** `.cursor/backups/20261005T160417/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T160417`


### 2026-10-05 15:28 — MACHINE.md: полная карта IO, кнопки HOME/START/PAUSE

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`
- **Снимок:** `.cursor/backups/20261005T152801/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T152801`


### 2026-10-05 12:44 — MACHINE.md: часы контроллера

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`
- **Снимок:** `.cursor/backups/20261005T124423/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T124423`


### 2026-10-05 12:29 — ускорение G00 300, Z 1500/800

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/generated/accel_fix/SYSDISK/setting\`, \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`, \`Платы и модули/M350_CNC_Controller/notes/O502_SLOW_TRAVEL_FIX_20261005.md\`
- **Снимок:** `.cursor/backups/20261005T122903/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T122903`


### 2026-10-05 12:22 — двигатели X/Y ШДГ-57 4.4A, рекомендация SW3 ON

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/Leadshine_DM856/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20261005T122229/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T122229`


### 2026-10-05 12:17 — двигатели X/Y/Z в MACHINE.md

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`, \`Платы и модули/Leadshine_DM856/TECH_SUMMARY.md\`, \`Платы и модули/M350_CNC_Controller/pic/motor_xy_label.png\`, \`Платы и модули/M350_CNC_Controller/pic/motor_z_pl57h110.png\`
- **Снимок:** `.cursor/backups/20261005T121754/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T121754`


### 2026-10-05 12:12 — Leadshine DM856: папка модуля, DIP расшифровка, MACHINE.md

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/Leadshine_DM856\`, \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`.cursor/rules/module-docs-priority.mdc\`
- **Снимок:** `.cursor/backups/20261005T121242/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T121242`


### 2026-10-05 12:08 — O9053 G00 без F/ABC, G00+XY 3000

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/generated/rapid_fix/SYSDISK/slib-g.nc\`, \`Платы и модули/M350_CNC_Controller/generated/rapid_fix/SYSDISK/setting\`, \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`, \`Платы и модули/M350_CNC_Controller/notes/O502_SLOW_TRAVEL_FIX_20261005.md\`
- **Снимок:** `.cursor/backups/20261005T120816/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T120816`


### 2026-10-05 11:55 — slib-g O502 та же длина (фикс хоуминга Y)

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/generated/o502_fix/SYSDISK/slib-g.nc\`, \`Платы и модули/M350_CNC_Controller/notes/O502_SLOW_TRAVEL_FIX_20261005.md\`
- **Снимок:** `.cursor/backups/20261005T115510/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T115510`


### 2026-10-05 11:48 — O502: переезд к датчику без A/B/C (медленно из дальнего угла)

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/notes/O502_SLOW_TRAVEL_FIX_20261005.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`, \`Платы и модули/M350_CNC_Controller/generated/o502_fix/SYSDISK/slib-g.nc\`
- **Снимок:** `.cursor/backups/20261005T114834/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T114834`


### 2026-10-05 11:20 — CAM: защита шаг Z=0, наклонное врезание cam31-33, новые картинки cam10-39

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/scripts/m350-cam-pics.py\`, \`Платы и модули/M350_CNC_Controller/scripts/m350-cam-fix.py\`, \`Платы и модули/M350_CNC_Controller/scripts/m350-cam-sim.py\`, \`Платы и модули/M350_CNC_Controller/generated/cam_fix\`, \`Платы и модули/M350_CNC_Controller/generated/cam_pics\`, \`Платы и модули/M350_CNC_Controller/notes/CAM_REVIEW_20261005.md\`, \`Платы и модули/M350_CNC_Controller/notes/CAM10-19_NEW_20261005.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`, \`Платы и модули/M350_CNC_Controller/pic/cam_menu_pictures.png\`
- **Снимок:** `.cursor/backups/20261005T112007/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T112007`


### 2026-10-05 11:03 — Ревизия CAM: исправлены cam20-27,32,33, симулятор --fix

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/scripts/m350-cam-fix.py\`, \`Платы и модули/M350_CNC_Controller/scripts/m350-cam-sim.py\`, \`Платы и модули/M350_CNC_Controller/generated/cam_fix\`, \`Платы и модули/M350_CNC_Controller/notes/CAM_REVIEW_20261005.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`
- **Снимок:** `.cursor/backups/20261005T110318/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T110318`


### 2026-10-05 10:48 — cam10-19 заменены улучшенными макросами щупа; генератор, симулятор, заметка

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/scripts/m350-cam10-19.py\`, \`Платы и модули/M350_CNC_Controller/scripts/m350-cam-sim.py\`, \`Платы и модули/M350_CNC_Controller/notes/CAM10-19_NEW_20261005.md\`, \`Платы и модули/M350_CNC_Controller/notes/CAM_ADDONS_20261005.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`
- **Снимок:** `.cursor/backups/20261005T104813/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T104813`


### 2026-10-05 10:19 — m350-proc.sh, ОЗУ/CPU в TECH_SUMMARY

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/scripts/m350-proc.sh\`, \`Платы и модули/M350_CNC_Controller/TECH_SUMMARY.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`
- **Снимок:** `.cursor/backups/20261005T101904/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T101904`


### 2026-10-05 10:01 — паспорт станка MACHINE.md, фото, cam38 обдув=1

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/MACHINE.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`, \`Платы и модули/M350_CNC_Controller/pic\`, \`Платы и модули/M350_CNC_Controller/notes/CAM_ADDONS_20261005.md\`, \`Платы и модули/M350_CNC_Controller/scripts/m350-cam-addons.py\`, \`Платы и модули/M350_CNC_Controller/generated/cam_addons\`
- **Снимок:** `.cursor/backups/20261005T100148/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T100148`


### 2026-10-05 09:58 — #141=3000 восстановлен; cam38/39 щуп+датчик длины

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/scripts\`, \`Платы и модули/M350_CNC_Controller/notes/CAM_ADDONS_20261005.md\`, \`Платы и модули/M350_CNC_Controller/notes/FIRMWARE_UPDATE_20261005.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`, \`Платы и модули/M350_CNC_Controller/generated\`
- **Снимок:** `.cursor/backups/20261005T095844/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T095844`


### 2026-10-05 09:47 — cam36 резьбофрезерование, cam37 выравнивание стола

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/scripts/m350-cam-addons.py\`, \`Платы и модули/M350_CNC_Controller/notes/CAM_ADDONS_20261005.md\`, \`Платы и модули/M350_CNC_Controller/README.md\`, \`Платы и модули/M350_CNC_Controller/generated/cam_addons\`
- **Снимок:** `.cursor/backups/20261005T094700/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T094700`


### 2026-10-05 09:31 — Доп. CAM-макросы cam20-35 из FB-группы (Savelev/Al Tie), старые cam10-19 сохранены

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller/README.md\`, \`Платы и модули/M350_CNC_Controller/notes/CAM_ADDONS_20261005.md\`, \`Платы и модули/M350_CNC_Controller/notes/FACEBOOK_GROUP_USEFUL.md\`, \`Платы и модули/M350_CNC_Controller/scripts/m350-cam-addons.py\`
- **Снимок:** `.cursor/backups/20261005T093110/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261005T093110`


### 2026-10-01 11:32 — ANT «Ячейки»: max красный, min синий

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/ant-bms-24c.yaml\`
- **Снимок:** `.cursor/backups/20261001T113234/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261001T113234`


### 2026-10-01 11:29 — card-mod + строка разброса ячеек в «Сейчас»

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/configuration.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/ant-bms-24c.yaml\`
- **Снимок:** `.cursor/backups/20261001T112911/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261001T112911`


### 2026-10-01 11:26 — ANT24C: display_precision напряжений (1 знак пакет, 3 ячейки)

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/core.entity_registry\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/ant-bms-24c.yaml\`
- **Снимок:** `.cursor/backups/20261001T112655/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261001T112655`


### 2026-10-01 10:53 — JK B2A20S20P: готовый jkcfg ЭЛЬТАВР 230Ah + make_jkcfg.py

- **Агент:** cursor
- **Проект:** Платы и модули
- **Файлы:** \`Платы и модули/BMS/JK_B2A20S20P/scripts/make_jkcfg.py\`, \`Платы и модули/BMS/JK_B2A20S20P/notes/configs/ELTAVR_48V230Ah_16S_template\`, \`Платы и модули/BMS/JK_B2A20S20P/README.md\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/scripts/generate_battery_template_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/generated\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20261001T105338/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261001T105338`


### 2026-10-01 10:31 — Deye 6.6K: шаблон настроек АКБ ЭЛЬТАВР 230Ah (PDF+генератор)

- **Агент:** cursor
- **Проект:** Платы и модули
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/scripts/generate_battery_template_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/generated\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/diag_2026-10-01_АКБ_SOC/README.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20261001T103132/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261001T103132`


### 2026-10-01 09:53 — Deye 6.6K + JK B2A20S20P: диагностика SOC, decode_jkcfg.py

- **Агент:** cursor
- **Проект:** Платы и модули
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/diag_2026-10-01_АКБ_SOC\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/README.md\`, \`Платы и модули/BMS/JK_B2A20S20P/scripts/decode_jkcfg.py\`, \`Платы и модули/BMS/JK_B2A20S20P/notes/configs\`, \`Платы и модули/BMS/JK_B2A20S20P/README.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20261001T095359/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20261001T095359`


### 2026-09-30 14:16 — Жилсервис: обороты/последняя оплата — CHANGELOG

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260930T141617/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T141617`


### 2026-09-30 14:12 — Жилсервис: cookie jar, обороты, последняя оплата, retry

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/app.js\`
- **Снимок:** `.cursor/backups/20260930T141232/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T141232`


### 2026-09-30 14:08 — Крымэнерго: история оплат через меню + ожидания, CHANGELOG

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/CHANGELOG.md\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260930T140853/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T140853`


### 2026-09-30 13:30 — Крымэнерго: таймаут прокси Сайты 60с→300с; дата ISO→ДД.ММ.ГГГГ

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/Cursor Agent/api/sites_proxy.py\`
- **Снимок:** `.cursor/backups/20260930T133002/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T133002`


### 2026-09-30 12:36 — README-карты «что где лежит» для ANT и обеих JK; правило §5.1

- **Агент:** cursor
- **Проект:** bms
- **Файлы:** \`Платы и модули/BMS/ANT_BMS_16ZNJ6-16S-130A/README.md\`, \`Платы и модули/BMS/JK_PB1A16S10P/README.md\`, \`Платы и модули/BMS/JK_B2A20S20P/README.md\`, \`.cursor/rules/module-docs-priority.mdc\`
- **Снимок:** `.cursor/backups/20260930T123640/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T123640`


### 2026-09-30 12:32 — ANT BMS 16ZNJ6 + общая папка Платы и модули/BMS, перенос JK, пути обновлены

- **Агент:** cursor
- **Проект:** bms
- **Файлы:** \`Платы и модули/BMS/README.md\`, \`Платы и модули/BMS/ANT_BMS_16ZNJ6-16S-130A/PINOUT.md\`, \`Платы и модули/BMS/ANT_BMS_16ZNJ6-16S-130A/TECH_SUMMARY.md\`, \`Платы и модули/BMS/ANT_BMS_16ZNJ6-16S-130A/notes/INSTANCE.md\`, \`Платы и модули/BMS/ANT_BMS_16ZNJ6-16S-130A/download_report.json\`, \`.cursor/rules/module-docs-priority.mdc\`, \`.cursor/rules/separate-folder-per-topic.mdc\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260930T123226/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T123226`


### 2026-09-30 12:31 — перед переносом BMS в Платы и модули/BMS

- **Агент:** cursor
- **Проект:** bms
- **Файлы:** \`.cursor/rules/module-docs-priority.mdc\`, \`.cursor/rules/separate-folder-per-topic.mdc\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260930T123100/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T123100`


### 2026-09-30 12:21 — ESPHome подогрев АКБ: firmware/esphome_heater (yaml, build.sh, README), ссылки в HEATING/INSTANCE/PINOUT

- **Агент:** cursor
- **Проект:** JK_B2A20S20P
- **Файлы:** \`Платы и модули/JK_B2A20S20P/firmware/esphome_heater\`, \`Платы и модули/JK_B2A20S20P/notes/HEATING.md\`, \`Платы и модули/JK_B2A20S20P/notes/INSTANCE.md\`, \`Платы и модули/JK_B2A20S20P/PINOUT.md\`
- **Снимок:** `.cursor/backups/20260930T122101/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T122101`


### 2026-09-30 12:02 — Подогрев АКБ: notes/HEATING.md + схема, ссылки в PINOUT B2A и PB

- **Агент:** cursor
- **Проект:** JK_B2A20S20P
- **Файлы:** \`Платы и модули/JK_B2A20S20P/notes/HEATING.md\`, \`Платы и модули/JK_B2A20S20P/pic/heating_wiring_B-series_JK_guide_p3.png\`, \`Платы и модули/JK_B2A20S20P/PINOUT.md\`, \`Платы и модули/JK_PB1A16S10P/PINOUT.md\`
- **Снимок:** `.cursor/backups/20260930T120223/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T120223`


### 2026-09-30 12:00 — PINOUT под ревизию V19 по фото торца (P8 报警 для реле), мануал V19.1.1; PB: номинал DRY 30В/1А

- **Агент:** cursor
- **Проект:** JK_B2A20S20P
- **Файлы:** \`Платы и модули/JK_B2A20S20P/PINOUT.md\`, \`Платы и модули/JK_B2A20S20P/TECH_SUMMARY.md\`, \`Платы и модули/JK_B2A20S20P/notes/INSTANCE.md\`, \`Платы и модули/JK_B2A20S20P/download_report.json\`, \`Платы и модули/JK_PB1A16S10P/PINOUT.md\`
- **Снимок:** `.cursor/backups/20260930T120033/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T120033`


### 2026-09-30 11:49 — esphome-jk-bms @6a59290 в extracted/, памятка notes/ESPHOME_JK_BMS.md, ссылка из JK_PB1A16S10P

- **Агент:** cursor
- **Проект:** JK_B2A20S20P
- **Файлы:** \`Платы и модули/JK_B2A20S20P/notes/ESPHOME_JK_BMS.md\`, \`Платы и модули/JK_B2A20S20P/download_report.json\`, \`Платы и модули/JK_PB1A16S10P/notes/FIRMWARE_AND_PROTOCOLS.md\`
- **Снимок:** `.cursor/backups/20260930T114913/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T114913`


### 2026-09-30 11:48 — Перед удалением дублей downloads/protocols и zip esphome-jk-bms (оставлен extracted/)

- **Агент:** cursor
- **Проект:** JK_B2A20S20P
- **Файлы:** \`Платы и модули/JK_B2A20S20P/downloads/protocols\`, \`Платы и модули/JK_B2A20S20P/PINOUT.md\`, \`Платы и модули/JK_B2A20S20P/TECH_SUMMARY.md\`, \`Платы и модули/JK_B2A20S20P/download_report.json\`
- **Снимок:** `.cursor/backups/20260930T114842/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T114842`


### 2026-09-30 11:42 — Новая папка модуля JK-B2A20S20P + строка в module-docs-priority.mdc

- **Агент:** cursor
- **Проект:** Платы и модули/JK_B2A20S20P
- **Файлы:** \`Платы и модули/JK_B2A20S20P\`, \`.cursor/rules/module-docs-priority.mdc\`
- **Снимок:** `.cursor/backups/20260930T114246/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T114246`


### 2026-09-30 11:18 — GEM S3: команда cores

- **Агент:** cursor
- **Проект:** gem-bmc-esp32s3
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/README.md\`
- **Снимок:** `.cursor/backups/20260930T111832/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T111832`


### 2026-09-30 11:03 — GEM S3 v0.2.1 captive portal + wifi log

- **Агент:** cursor
- **Проект:** gem-bmc-esp32s3
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/src/web_ui.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/README.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260930T110337/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T110337`


### 2026-09-30 10:55 — GEM S3 v0.2.0 BLE+SoftAP, MIN 0.1.1, README/PINOUT

- **Агент:** cursor
- **Проект:** gem-bmc-esp32s3
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/PINOUT.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/src\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/include\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/scripts\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/README.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260930T105548/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T105548`


### 2026-09-30 10:21 — GEM BMC эмулятор для ESP32-S3-RS485-CAN v0.1.0

- **Агент:** cursor
- **Проект:** GEM_e6
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/src/twai_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/src/bmc_can_gen.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/include/hw_pins.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/include/twai_gem.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/include/bmc_can_gen.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/scripts/flash.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32s3_rs485can/PINOUT.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/README.md\`, \`Платы и модули/ESP32-S3-RS485-CAN/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260930T102119/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T102119`


### 2026-09-30 10:14 — Перенос в Платы и модули/ESP32-S3-RS485-CAN, правка путей и .dockerignore

- **Агент:** cursor
- **Проект:** ESP32-S3-RS485-CAN
- **Файлы:** \`Платы и модули/ESP32-S3-RS485-CAN/README.md\`, \`Платы и модули/ESP32-S3-RS485-CAN/CHANGELOG.md\`, \`Платы и модули/ESP32-S3-RS485-CAN/TECH_SUMMARY.md\`, \`Платы и модули/ESP32-S3-RS485-CAN/.dockerignore\`, \`Проекты/README.md\`
- **Снимок:** `.cursor/backups/20260930T101400/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T101400`


### 2026-09-30 10:13 — Перед переносом Проекты/ESP32-S3-RS485-CAN → Платы и модули/ESP32-S3-RS485-CAN

- **Агент:** cursor
- **Проект:** ESP32-S3-RS485-CAN
- **Файлы:** \`Проекты/ESP32-S3-RS485-CAN/Dockerfile\`, \`Проекты/ESP32-S3-RS485-CAN/docker-compose.yml\`, \`Проекты/ESP32-S3-RS485-CAN/.dockerignore\`, \`Проекты/ESP32-S3-RS485-CAN/README.md\`, \`Проекты/ESP32-S3-RS485-CAN/CHANGELOG.md\`, \`Проекты/ESP32-S3-RS485-CAN/scripts/pio.sh\`, \`Проекты/ESP32-S3-RS485-CAN/scripts/flash.sh\`, \`Проекты/ESP32-S3-RS485-CAN/scripts/monitor.sh\`, \`Проекты/ESP32-S3-RS485-CAN/scripts/detect.sh\`, \`Проекты/ESP32-S3-RS485-CAN/firmware/board_test/platformio.ini\`, \`Проекты/ESP32-S3-RS485-CAN/firmware/board_test/src/main.cpp\`, \`Проекты/ESP32-S3-RS485-CAN/.cursor/rules/docker-cleanup-after-rebuild.mdc\`, \`Проекты/README.md\`, \`Платы и модули/ESP32-S3-RS485-CAN/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260930T101323/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T101323`


### 2026-09-30 10:01 — releases: 2 бинаря TJA1050/MCP2515; build.sh; README

- **Агент:** cursor
- **Проект:** gem-bmc-esp32c3
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_esp32c3_v0.4.0_TJA1050.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_esp32c3_v0.4.0_MCP2515.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/flash-can-min.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260930T100152/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T100152`


### 2026-09-30 10:01 — снимок releases/ перед чисткой (оставить 2 бинаря)

- **Агент:** cursor
- **Проект:** gem-bmc-esp32c3
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.1.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.2.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.3.1.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.3.2.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.3.3.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.3.4.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.3.5.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.3.6.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.3.7.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.3.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.4.0.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.4.1-bench.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.4.2-bench-swap.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.4.3-bench.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.5.0.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.5.1-echo.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.5.2.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.5.3.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.0.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.10.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.11.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.12.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.13.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.14.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.1.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.4.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.6.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.7.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.8.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.9.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.7.0.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_min_esp32c3_v0.1.0.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_min_esp32c3_v0.2.0.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_min_esp32c3_v0.3.0.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_min_esp32c3_v0.3.1.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_min_esp32c3_v0.3.2.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_min_esp32c3_v0.4.0.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_can_simple_esp32c3_v0.1.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_vp230_diag_esp32c3_v0.1.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/flash-can-min.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260930T100114/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T100114`


### 2026-09-30 10:00 — MIN v0.4.0 / v0.7.0: TWAI+TJA1050, can_gem.h

- **Агент:** cursor
- **Проект:** gem-bmc-esp32c3
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/can_gem.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/twai_gem.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/twai_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main_can_min.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/PINOUT.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/flash-can-min.sh\`
- **Снимок:** `.cursor/backups/20260930T100002/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T100002`


### 2026-09-30 09:57 — до перевода на TWAI+TJA1050 (снимок)

- **Агент:** cursor
- **Проект:** gem-bmc-esp32c3
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main_can_min.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/PINOUT.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/flash.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/flash-can-min.sh\`
- **Снимок:** `.cursor/backups/20260930T095715/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T095715`


### 2026-09-30 09:46 — PINOUT: диагностика перепутанных TX/RX

- **Агент:** cursor
- **Проект:** gem-bmc-h503
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/PINOUT.md\`
- **Снимок:** `.cursor/backups/20260930T094640/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T094640`


### 2026-09-30 09:41 — v4.3.0 TJA1050 + fix TX stall

- **Агент:** cursor
- **Проект:** gem-bmc-h503
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/src/fdcan_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/include/fdcan_gem.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/PINOUT.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/scripts/flash.sh\`
- **Снимок:** `.cursor/backups/20260930T094117/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260930T094117`


### 2026-09-29 17:45 — Deye Cloud: исправлены параметры станции 62712642

- **Агент:** cursor
- **Проект:** Мирное_Никольская_10
- **Файлы:** \`Проекты/Мирное_Никольская_10/notes/БЛОКНОТ.md\`
- **Снимок:** `.cursor/backups/20260929T174523/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T174523`


### 2026-09-29 17:24 — Deye Cloud: станция у заказчика в EMEA 62712642, онлайн

- **Агент:** cursor
- **Проект:** Мирное_Никольская_10
- **Файлы:** \`Проекты/Мирное_Никольская_10/notes/БЛОКНОТ.md\`
- **Снимок:** `.cursor/backups/20260929T172436/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T172436`


### 2026-09-29 17:08 — Deye Cloud: перенос на заказчика, логгер офлайн (AMER vs EMEA)

- **Агент:** cursor
- **Проект:** Мирное_Никольская_10
- **Файлы:** \`Проекты/Мирное_Никольская_10/notes/БЛОКНОТ.md\`
- **Снимок:** `.cursor/backups/20260929T170845/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T170845`


### 2026-09-29 16:38 — Deye Cloud онлайн, настройки прочитаны

- **Агент:** cursor
- **Проект:** Мирное_Никольская_10
- **Файлы:** \`Проекты/Мирное_Никольская_10/notes/БЛОКНОТ.md\`
- **Снимок:** `.cursor/backups/20260929T163835/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T163835`


### 2026-09-29 16:19 — блокнот: Solarman отклонён, статус Deye Cloud

- **Агент:** cursor
- **Проект:** Мирное_Никольская_10
- **Файлы:** \`Проекты/Мирное_Никольская_10/notes/БЛОКНОТ.md\`
- **Снимок:** `.cursor/backups/20260929T161904/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T161904`


### 2026-09-29 16:17 — DL1000B = Deye Cloud, не Solarman

- **Агент:** cursor
- **Проект:** Мирное_Никольская_10
- **Файлы:** \`Проекты/Мирное_Никольская_10/notes/БЛОКНОТ.md\`, \`Проекты/Мирное_Никольская_10/notes/SOLARMAN_PRO.md\`
- **Снимок:** `.cursor/backups/20260929T161720/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T161720`


### 2026-09-29 15:40 — PDF 3× RW-F16 + общий генератор 2x/3x

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_rwf16_system_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/generated/Deye_SUN-20K_3xRW-F16_Installation_Setup_RU.pdf\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/PINOUT.md\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/README.md\`
- **Снимок:** `.cursor/backups/20260929T154053/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T154053`


### 2026-09-29 15:38 — до генератора 2x/3x в одном скрипте

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_2x_rwf16_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260929T153806/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T153806`


### 2026-09-29 08:08 — удалён мануал 3x RW-F16 (2 PDF + 2 генератора), хелперы перенесены в generate_2x, доки обновлены

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16\`, \`Платы и модули/Солнечные_инверторы/README.md\`
- **Снимок:** `.cursor/backups/20260929T080813/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T080813`


### 2026-09-29 08:07 — до удаления мануала 3x RW-F16

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_2x_rwf16_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_3x_rwf16_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_menu_settings_3x_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/generated\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/PINOUT.md\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/README.md\`
- **Снимок:** `.cursor/backups/20260929T080748/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T080748`


### 2026-09-29 08:07 — 2x RW-F16: один PDF (установка+схема+меню); удалены Menu_Settings 2x, общий RW-F16 PDF, Full_System_Guide 2x и их генераторы

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/generated\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16\`, \`Платы и модули/Солнечные_инверторы/README.md\`
- **Снимок:** `.cursor/backups/20260929T080726/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T080726`


### 2026-09-29 08:06 — до объединения 2x в один PDF

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_menu_settings_2x_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_pdfs.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_2x_rwf16_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16\`
- **Снимок:** `.cursor/backups/20260929T080609/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T080609`


### 2026-09-29 08:04 — блок ОБЯЗАТЕЛЬНО связь BMS (PCS→инвертор, OUT→IN) в 2x PDF, TECH_SUMMARY, PINOUT

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16\`
- **Снимок:** `.cursor/backups/20260929T080444/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T080444`


### 2026-09-29 08:03 — до блока ОБЯЗАТЕЛЬНО связь PCS/IN/OUT

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_2x_rwf16_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_menu_settings_2x_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16\`
- **Снимок:** `.cursor/backups/20260929T080358/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260929T080358`


### 2026-09-28 16:12 — pi3-ha-proxy Pi5:8124

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/scripts/pi3_ha_proxy.py\`
- **Снимок:** `.cursor/backups/20260928T161228/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T161228`


### 2026-09-28 15:54 — Графики Pi5: оси CPU

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/pi5.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/lovelace.lovelace\`
- **Снимок:** `.cursor/backups/20260928T155427/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T155427`


### 2026-09-28 15:46 — ANT24C графики: мёртвая зона + фикс. оси

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/packages/ant24c.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/ant-bms-24c.yaml\`
- **Снимок:** `.cursor/backups/20260928T154644/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T154644`


### 2026-09-28 14:32 — убраны дубли 2x PDF из SUN-20K/generated; генераторы пишут в одно место; правило 'без копий' в separate-folder-per-topic.mdc

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts\`, \`.cursor/rules/separate-folder-per-topic.mdc\`
- **Снимок:** `.cursor/backups/20260928T143241/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T143241`


### 2026-09-28 14:27 — Batt Mode = радиокнопка: только Lithium; убраны ошибочные 'Use Batt % включить' в 2x/3x/общих PDF; 3x больше не копируется в RW-F16/generated

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/generated\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/generated\`
- **Снимок:** `.cursor/backups/20260928T142740/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T142740`


### 2026-09-28 14:26 — до исправления Batt Mode (радиокнопка)

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_2x_rwf16_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_menu_settings_2x_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_3x_rwf16_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_menu_settings_3x_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/generated\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/generated\`
- **Снимок:** `.cursor/backups/20260928T142619/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T142619`


### 2026-09-28 13:53 — generated переделан под 2x RW-F16: Installation_Setup + Menu_Settings (Max A 240/250), 3x-копия удалена (оригинал в SUN-20K/generated)

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/generated\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/PINOUT.md\`, \`Платы и модули/Солнечные_инверторы/README.md\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_2x_rwf16_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_menu_settings_2x_pdf.py\`
- **Снимок:** `.cursor/backups/20260928T135311/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T135311`


### 2026-09-28 13:51 — generated: переделка под 2x RW-F16 (до)

- **Агент:** cursor
- **Проект:** Deye_RW-F16
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/generated\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/PINOUT.md\`
- **Снимок:** `.cursor/backups/20260928T135125/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T135125`


### 2026-09-28 08:45 — PlatformIO Docker для ESP32-S3-RS485-CAN

- **Агент:** cursor
- **Проект:** ESP32-S3-RS485-CAN
- **Файлы:** \`Проекты/ESP32-S3-RS485-CAN/Dockerfile\`, \`Проекты/ESP32-S3-RS485-CAN/docker-compose.yml\`, \`Проекты/ESP32-S3-RS485-CAN/README.md\`, \`Проекты/ESP32-S3-RS485-CAN/CHANGELOG.md\`, \`Проекты/ESP32-S3-RS485-CAN/scripts/pio.sh\`, \`Проекты/ESP32-S3-RS485-CAN/scripts/flash.sh\`, \`Проекты/ESP32-S3-RS485-CAN/scripts/monitor.sh\`, \`Проекты/ESP32-S3-RS485-CAN/scripts/detect.sh\`, \`Проекты/ESP32-S3-RS485-CAN/firmware/board_test/platformio.ini\`, \`Проекты/ESP32-S3-RS485-CAN/firmware/board_test/src/main.cpp\`, \`Проекты/README.md\`
- **Снимок:** `.cursor/backups/20260928T084505/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T084505`


### 2026-09-28 08:28 — Новый модуль ESP32-S3-RS485-CAN (Waveshare)

- **Агент:** cursor
- **Проект:** Платы и модули
- **Файлы:** \`Платы и модули/ESP32-S3-RS485-CAN/PINOUT.md\`, \`Платы и модули/ESP32-S3-RS485-CAN/TECH_SUMMARY.md\`, \`.cursor/rules/module-docs-priority.mdc\`
- **Снимок:** `.cursor/backups/20260928T082827/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260928T082827`


### 2026-09-25 18:03 — silent deny чужих в Telegram

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/telegram_relay.py\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260925T180305/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260925T180305`


### 2026-09-25 17:52 — VIN search: restart hung polling + pool timeouts + auto VIN

- **Агент:** cursor
- **Проект:** telegram_bot
- **Файлы:** \`Проекты/telegram_bot/bot.py\`, \`Проекты/telegram_bot/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260925T175200/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260925T175200`


### 2026-09-23 14:53 — проверка прошивки EOS 0606i

- **Агент:** cursor
- **Проект:** Hyperion_EOS_0606i
- **Файлы:** \`Платы и модули/Hyperion_EOS_0606i\`
- **Снимок:** `.cursor/backups/20260923T145346/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260923T145346`


### 2026-09-22 15:15 — док M350 + smb скрипт

- **Агент:** cursor
- **Проект:** M350_CNC_Controller
- **Файлы:** \`Платы и модули/M350_CNC_Controller\`
- **Снимок:** `.cursor/backups/20260922T151549/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260922T151549`


### 2026-09-22 10:45 — Солнечные_панели: Trina TSM-NED9R.28 + Jinko JKM605-630N

- **Агент:** cursor
- **Проект:** Солнечные_инверторы
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Солнечные_панели\`, \`Платы и модули/Солнечные_инверторы/README.md\`
- **Снимок:** `.cursor/backups/20260922T104553/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260922T104553`


### 2026-09-18 15:53 — MIN v0.3.2 no relay OFF pulse

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/hw_pins.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main_can_min.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/flash-can-min.sh\`
- **Снимок:** `.cursor/backups/20260918T155307/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T155307`


### 2026-09-18 15:48 — MIN v0.3.1 CAN+relay no radio

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main_can_min.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/flash-can-min.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260918T154852/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T154852`


### 2026-09-18 15:45 — MIN v0.3.0 pure CAN emu

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main_can_min.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/flash-can-min.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260918T154554/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T154554`


### 2026-09-18 15:40 — ESP v0.6.14 CAN watchdog USB

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/mcp_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/mcp_gem.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.14.bin\`
- **Снимок:** `.cursor/backups/20260918T154037/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T154037`


### 2026-09-18 15:20 — ESP v0.6.13b single-frame pump

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/mcp_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.13.bin\`
- **Снимок:** `.cursor/backups/20260918T152034/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T152034`


### 2026-09-18 15:18 — ESP v0.6.13 P1824/P1827 slot-skip fix

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/bmc_can_gen.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/web_ui.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.13.bin\`
- **Снимок:** `.cursor/backups/20260918T151850/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T151850`


### 2026-09-18 15:07 — ESP BMC v0.6.12 ANT_BLE off

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/ant_ble.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.12.bin\`
- **Снимок:** `.cursor/backups/20260918T150741/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T150741`


### 2026-09-18 14:57 — ESP BMC v0.6.11: async BLE + CAN task + phased TX

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/ant_ble.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/mcp_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/releases/gem_bmc_can_emu_esp32c3_v0.6.11.bin\`
- **Снимок:** `.cursor/backups/20260918T145716/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T145716`


### 2026-09-18 11:06 — v0.6.10 emul U+SOC

- **Агент:** cursor
- **Проект:** gem-bmc-esp
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/bmc_can_gen.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/bmc_can_gen.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260918T110612/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T110612`


### 2026-09-18 10:54 — README пометки dual proto

- **Агент:** cursor
- **Проект:** gem-bmc-esp
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260918T105449/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T105449`


### 2026-09-18 10:50 — v0.6.9 dual ANT proto web

- **Агент:** cursor
- **Проект:** gem-bmc-esp
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/ant_ble.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/web_ui.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/settings.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/settings.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/ant_ble.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260918T105028/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T105028`


### 2026-09-18 10:44 — v0.6.8 harden verify PASS

- **Агент:** cursor
- **Проект:** gem-bmc-esp
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/mcp_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/bmc_can_gen.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/ant_ble.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260918T104457/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T104457`


### 2026-09-18 10:35 — EF3 live U/I/SOC overlay v0.6.7

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/bmc_can_gen.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/bmc_can_gen.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/CAN_BUS_MAP.md\`
- **Снимок:** `.cursor/backups/20260918T103547/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T103547`


### 2026-09-18 10:23 — ANT BLE legacy DBDB v0.6.6

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/ant_ble.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260918T102307/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260918T102307`


### 2026-09-17 13:18 — PDF полный LCD снова + Master×3

- **Агент:** cursor
- **Проект:** Deye_SUN-6.6K-OG03LP1-EU-AM2
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/LCD_НАСТРОЙКА_3Ф_3шт.pdf\`
- **Снимок:** `.cursor/backups/20260917T131819/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260917T131819`


### 2026-09-17 12:38 — F41 fix: Master на всех 3 фазах

- **Агент:** cursor
- **Проект:** Deye_SUN-6.6K-OG03LP1-EU-AM2
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/РУКОВОДСТВО_RU.md\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/LCD_НАСТРОЙКА_3Ф_3шт.pdf\`
- **Снимок:** `.cursor/backups/20260917T123844/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260917T123844`


### 2026-09-17 10:36 — TWAI→MCP2515 v0.6.0

- **Агент:** cursor
- **Проект:** gem_bmc_esp32c3
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/mcp_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main_can_min.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/mcp_gem.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/PINOUT.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260917T103640/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260917T103640`


### 2026-09-17 10:33 — PDF LCD чеклист 3ф×3

- **Агент:** cursor
- **Проект:** Deye_SUN-6.6K-OG03LP1-EU-AM2
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/LCD_НАСТРОЙКА_3Ф_3шт.pdf\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/README.md\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/РУКОВОДСТВО_RU.md\`
- **Снимок:** `.cursor/backups/20260917T103308/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260917T103308`


### 2026-09-17 09:58 — Uno+Shield V1.2 CS=D9 16MHz

- **Агент:** cursor
- **Проект:** gem_bmc_can_emu
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/gem_bmc_can_emu.ino\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/PINOUT.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/hw_pins.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/scripts/flash.sh\`
- **Снимок:** `.cursor/backups/20260917T095852/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260917T095852`


### 2026-09-17 09:50 — flash.sh: OpenOCD none+halt

- **Агент:** cursor
- **Проект:** gem_bmc_h503
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/scripts/flash.sh\`
- **Снимок:** `.cursor/backups/20260917T095022/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260917T095022`


### 2026-09-17 09:43 — v4.2.2 FDCAN PLL1Q 250k fix

- **Агент:** cursor
- **Проект:** gem_bmc_h503
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/src/fdcan_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/include/fdcan_gem.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/PINOUT.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/README.md\`
- **Снимок:** `.cursor/backups/20260917T094337/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260917T094337`


### 2026-09-16 16:44 — RX diag + sniffer MCP_8MHZ

- **Агент:** cursor
- **Проект:** gem_can_simple
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main_can_simple.cpp\`, \`Проекты/Arduino/firmware/CAN_Sniffer_Shield_LCD/CAN_Sniffer_Shield_LCD.ino\`, \`Проекты/Arduino/firmware/CAN_Sniffer_Shield_LCD/README.md\`
- **Снимок:** `.cursor/backups/20260916T164453/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260916T164453`


### 2026-09-16 16:11 — CAN sniffer setMode NORMAL after begin

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/CAN_Sniffer_Shield_LCD/CAN_Sniffer_Shield_LCD.ino\`, \`Проекты/Arduino/firmware/CAN_Sniffer_Shield_LCD/CAN_Sniffer_Shield_LCD.hex\`, \`Проекты/Arduino/firmware/CAN_Sniffer_Shield_LCD/README.md\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260916T161117/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260916T161117`


### 2026-09-16 16:06 — CAN_Sniffer default 250 kbps

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/CAN_Sniffer_Shield_LCD/CAN_Sniffer_Shield_LCD.ino\`, \`Проекты/Arduino/firmware/CAN_Sniffer_Shield_LCD/CAN_Sniffer_Shield_LCD.hex\`, \`Проекты/Arduino/firmware/CAN_Sniffer_Shield_LCD/README.md\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260916T160625/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260916T160625`


### 2026-09-16 14:20 — ESP TWAI NO_ACK bench v0.4.1

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/twai_gem.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/platformio.ini\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/PINOUT.md\`
- **Снимок:** `.cursor/backups/20260916T142046/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260916T142046`


### 2026-09-16 14:09 — ESP BMC v0.4.0 = Pi CAN v4 + relays X3

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/include/bmc_can_gen.h\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_esp32c3/README.md\`
- **Снимок:** `.cursor/backups/20260916T140900/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260916T140900`


### 2026-09-16 08:26 — apply 13S via i.Solar + script

- **Агент:** cursor
- **Проект:** SILA_VM_II_Premium_Plus_6.2K
- **Файлы:** \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/scripts/isolar-apply-13s.sh\`, \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/notes/USER_13S_LION_SETTINGS.md\`, \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/settings/apply_13s_latest.json\`, \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/settings/НАСТРОЙКИ_latest.md\`
- **Снимок:** `.cursor/backups/20260916T082637/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260916T082637`


### 2026-09-16 08:18 — профиль User 13S Li-ion + правка руководства

- **Агент:** cursor
- **Проект:** SILA_VM_II_Premium_Plus_6.2K
- **Файлы:** \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/notes/USER_13S_LION_SETTINGS.md\`, \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/РУКОВОДСТВО_RU.md\`, \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/notes/check_Li_ANT_BMS_2026-08-06.md\`
- **Снимок:** `.cursor/backups/20260916T081808/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260916T081808`


### 2026-09-15 14:50 — OSD timestamp mirrorH

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_HIDDEN_FEATURES.md\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/dumps/osd_fonts/720.xx.mirrorH\`
- **Снимок:** `.cursor/backups/20260915T145017/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260915T145017`


### 2026-09-15 14:40 — CH-H01 upside-down mount: flip=3 + osd_flip180

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_HIDDEN_FEATURES.md\`
- **Снимок:** `.cursor/backups/20260915T144046/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260915T144046`


### 2026-09-14 21:24 — eltavr-bot proxy+slim после ребута

- **Агент:** cursor
- **Проект:** telegram_bot
- **Файлы:** \`Проекты/telegram_bot/bot.py\`, \`Проекты/telegram_bot/docker-compose.yml\`, \`Проекты/telegram_bot/dockerfile\`, \`Проекты/telegram_bot/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260914T212426/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T212426`


### 2026-09-14 21:05 — fix false-positive SHELL_ALIVE check

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/uart_wait_fix_motion.py\`
- **Снимок:** `.cursor/backups/20260914T210526/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T210526`


### 2026-09-14 21:04 — uart_wait_fix_motion: ждёт power-cycle для motion

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/uart_wait_fix_motion.py\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260914T210452/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T210452`


### 2026-09-14 13:52 — motion no-response analysis

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`
- **Снимок:** `.cursor/backups/20260914T135200/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T135200`


### 2026-09-14 13:40 — mDNS 3D65 via set_lumi_info

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/acc.dat.3d65.15170.bin\`
- **Снимок:** `.cursor/backups/20260914T134031/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T134031`


### 2026-09-14 13:11 — mDNS still 1B6C; uart down

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`
- **Снимок:** `.cursor/backups/20260914T131115/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T131115`


### 2026-09-14 12:53 — root cause 1B6C=did.json

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`
- **Снимок:** `.cursor/backups/20260914T125352/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T125352`


### 2026-09-14 12:42 — unpair for 3D65 re-add; 1B6C is Home ghost

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`
- **Снимок:** `.cursor/backups/20260914T124230/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T124230`


### 2026-09-14 12:25 — wipe EE74 hap.dat; 1B6C not correct

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`
- **Снимок:** `.cursor/backups/20260914T122529/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T122529`


### 2026-09-14 12:17 — motion no-response: fix acc.dat 3D65 identity_watch

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`
- **Снимок:** `.cursor/backups/20260914T121759/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T121759`


### 2026-09-14 12:05 — WiFi priority GARAGE>AiNET v3 dual

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/wifi_start_hardened.sh\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/wifi.conf.good\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260914T120527/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T120527`


### 2026-09-14 12:00 — WiFi GARAGE switch

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/wifi.conf.good\`
- **Снимок:** `.cursor/backups/20260914T120054/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T120054`


### 2026-09-14 11:37 — Unable to add HAP diagnosis

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`
- **Снимок:** `.cursor/backups/20260914T113702/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T113702`


### 2026-09-14 11:02 — HK EE74 conflict note

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`
- **Снимок:** `.cursor/backups/20260914T110203/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T110203`


### 2026-09-14 10:49 — CH-H01 MAC 3D65 identity + boot hooks

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/CHH01_MAC_3D65.md\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260914T104953/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260914T104953`


### 2026-09-12 14:11 — Bybit via Tor on VPS: http helper, tunnel service, recv_window 60s

- **Агент:** cursor
- **Проект:** bybit
- **Файлы:** \`.cursor/scripts/bybit-http.py\`, \`.cursor/scripts/bybit-balance.py\`, \`.cursor/scripts/bybit-spot-order.py\`, \`.cursor/scripts/bybit-watch.py\`, \`.cursor/scripts/bybit-auto-trader.py\`, \`.cursor/scripts/bybit-tor-tunnel.service\`, \`.cursor/scripts/install-bybit-tor-tunnel.sh\`
- **Снимок:** `.cursor/backups/20260912T141157/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260912T141157`


### 2026-09-10 15:25 — скрипты полного MTD-дампа + заметка

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/uart_dump_mtd_to_sd.py\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/copy_dump_from_sd.sh\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/FULL_MTD_DUMP.md\`
- **Снимок:** `.cursor/backups/20260910T152515/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260910T152515`


### 2026-09-10 15:08 — UART root login/пароль в TECH_SUMMARY

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260910T150833/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260910T150833`


### 2026-09-10 14:50 — FLASHKA formatted for OTA 2.2.6 SD

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/OTA_SD_2.2.6.0003.0616.md\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/downloads/2.2.6.0003.0616_ota/README_FLASH.txt\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/downloads/2.2.6.0003.0616_ota/source_url.txt\`
- **Снимок:** `.cursor/backups/20260910T145006/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260910T145006`


### 2026-09-10 14:26 — hardened wifi_start against optical QR bad psk

- **Агент:** cursor
- **Проект:** Aqara_Camera_G2_ZNSXJ12LM
- **Файлы:** \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/wifi_start_hardened.sh\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/scripts/wifi.conf.good\`, \`Платы и модули/Aqara_Camera_G2_ZNSXJ12LM/notes/WIFI_QR_PSK_CORRUPTION.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260910T142608/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260910T142608`


### 2026-09-10 09:25 — WAN configure + LOGGER_PORT

- **Агент:** cursor
- **Проект:** Deye_SUN-6.6K
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/scripts/configure-logger-zaryadka.sh\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/WIFI_LOGGER_ЗАРЯДКА.md\`
- **Снимок:** `.cursor/backups/20260910T092504/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260910T092504`


### 2026-09-08 15:11 — Заливка рабочего профиля S/N 96342510600141

- **Агент:** cursor
- **Проект:** Adion_Expert_6kW_Twin
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/applied-settings/units/README.md\`, \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/applied-settings/units/96342510600141.txt\`, \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/applied-settings/inverter_working.txt\`, \`Платы и модули/Солнечные_инверторы/Adion_Expert_6kW_Twin/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260908T151106/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260908T151106`


### 2026-09-08 09:13 — папка модуля JK-PB1A16S10P по этикетке

- **Агент:** cursor
- **Проект:** JK_PB1A16S10P
- **Файлы:** \`Платы и модули/JK_PB1A16S10P\`, \`.cursor/rules/module-docs-priority.mdc\`
- **Снимок:** `.cursor/backups/20260908T091306/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260908T091306`


### 2026-09-07 16:49 — ANT BMS графики: убрать иголки (hold last + filter)

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/packages/ant24c.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/ant-bms-24c.yaml\`, \`bms-tools/ant24c_logger.py\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260907T164920/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T164920`


### 2026-09-07 16:26 — Filters and wipers reference Y921OE

- **Агент:** cursor
- **Проект:** audi-a4
- **Файлы:** \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260907T162615/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T162615`


### 2026-09-07 16:19 — список доп. QR-декодеров

- **Агент:** cursor
- **Проект:** LiFePO4_Cell_QR_Decoder
- **Файлы:** \`Платы и модули/LiFePO4_Cell_QR_Decoder/TECH_SUMMARY.md\`, \`Платы и модули/LiFePO4_Cell_QR_Decoder/source_url.txt\`, \`Платы и модули/LiFePO4_Cell_QR_Decoder/README.md\`
- **Снимок:** `.cursor/backups/20260907T161946/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T161946`


### 2026-09-07 16:10 — PWA UUID resume fix agent- prefix

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/llm/cursor_cli_client.py\`, \`Проекты/Cursor Agent/api/chat_recovery.py\`, \`Проекты/Cursor Agent/api/ws_chat.py\`, \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260907T161053/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T161053`


### 2026-09-07 15:40 — ANT BMS V2 account registration

- **Агент:** cursor
- **Проект:** ANT_BMS
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/notes/ANT_BMS_V2_ACCOUNT.md\`
- **Снимок:** `.cursor/backups/20260907T154041/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T154041`


### 2026-09-07 12:33 — RC region: proxy launch + keep-awake fix

- **Агент:** cursor
- **Проект:** cursor-remote-control
- **Файлы:** \`REMOTE_CONTROL.md\`
- **Снимок:** `.cursor/backups/20260907T123326/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T123326`


### 2026-09-07 11:47 — Telegram CURSOR_API_KEY auth fix

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/cursor_agent_client.py\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260907T114704/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T114704`


### 2026-09-07 10:00 — PWA chat CLI backend

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/llm/cursor_cli_client.py\`, \`Проекты/Cursor Agent/llm/factory.py\`, \`Проекты/Cursor Agent/api/mvp_app.py\`, \`Проекты/Cursor Agent/api/cursor_bridge.py\`, \`Проекты/Cursor Agent/config/settings.py\`, \`Проекты/Cursor Agent/scripts/cursor_http_socks_proxy.py\`
- **Снимок:** `.cursor/backups/20260907T100036/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T100036`


### 2026-09-07 09:58 — Telegram Cursor HTTPS_PROXY fix

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/cursor_agent_client.py\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`Проекты/ai_assistant/.env\`
- **Снимок:** `.cursor/backups/20260907T095858/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T095858`


### 2026-09-07 09:31 — force bridge refresh despite active_chats

- **Агент:** cursor
- **Проект:** cursor-agent
- **Файлы:** \`Проекты/Cursor Agent/api/bridge_internal.py\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260907T093159/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T093159`


### 2026-09-07 09:23 — MVP Wants proxy; MUTE no kill PWA

- **Агент:** cursor
- **Проект:** cursor-agent
- **Файлы:** \`Проекты/Cursor Agent/CHANGELOG.md\`, \`Проекты/ai_assistant/scripts/argon-vpn-toggle.sh\`
- **Снимок:** `.cursor/backups/20260907T092359/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T092359`


### 2026-09-07 09:20 — OLED V xray.service

- **Агент:** cursor
- **Проект:** oled_visual
- **Файлы:** \`Проекты/oled_visual/oled_visual.py\`
- **Снимок:** `.cursor/backups/20260907T092016/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T092016`


### 2026-09-07 09:14 — VPN /run flag reboot + mute

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-vpn-toggle.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260907T091459/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T091459`


### 2026-09-07 09:07 — argon VPN toggle xray.service

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-vpn-toggle.sh\`, \`Проекты/ai_assistant/scripts/argon-ir-stb-remote-listener.py\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260907T090709/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T090709`


### 2026-09-07 09:01 — chat handoff cursor worker proxy

- **Агент:** cursor
- **Проект:** cursor-agent
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260907T090113/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T090113`


### 2026-09-07 09:01 — worker proxy 10809 for region block

- **Агент:** cursor
- **Проект:** cursor-agent
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260907T090104/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260907T090104`


### 2026-09-03 13:04 — Ещё один MUST PV18-4024: dump 130250, verify 20/20

- **Агент:** cursor
- **Проект:** Must_PV18-4024_PRO_II
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/CHANGELOG.md\`, \`Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/factory-settings/inverter_factory_20260903_130250.txt\`, \`Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/factory-settings/inverter_factory_20260903_130250.json\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260903T130449/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260903T130449`


### 2026-09-03 11:19 — Заливка рабочего профиля MUST PV18-4024, dump 20260903, verify 20/20

- **Агент:** cursor
- **Проект:** Must_PV18-4024_PRO_II
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/CHANGELOG.md\`, \`Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/factory-settings/README.md\`, \`Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/factory-settings/inverter_factory_20260903_111458.txt\`, \`Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/factory-settings/inverter_factory_20260903_111458.json\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260903T111957/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260903T111957`


### 2026-09-03 10:00 — PDF 3x RW-F16 + SUN-20K схема и инструкция

- **Агент:** cursor
- **Проект:** deye-sun20k
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_3x_rwf16_pdf.py\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/generated/Deye_SUN-20K_3xRW-F16_Installation_Setup_RU.pdf\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/generated/Deye_SUN-20K_3xRW-F16_Installation_Setup_RU.pdf\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Deye_RW-F16/PINOUT.md\`, \`Платы и модули/Солнечные_инверторы/README.md\`
- **Снимок:** `.cursor/backups/20260903T100009/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260903T100009`


### 2026-09-02 18:19 — H503 v4.2 build OK, releases bin, relay docs sync

- **Агент:** cursor
- **Проект:** gem-e6
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/scripts/build.sh\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/src/main.cpp\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/releases/gem_bmc_can_emu_h503_v4.2.bin\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/README.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/BMC_CAN_EMULATOR_v4_OK.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/BMC_EMULATOR_PLAN.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260902T181918/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260902T181918`


### 2026-09-02 14:50 — Arduino Nano MCP2515 BMC CAN emu v4

- **Агент:** cursor
- **Проект:** gem_bmc_can_emu
- **Файлы:** \`Проекты/Arduino/firmware/gem_bmc_can_emu/gem_bmc_can_emu.ino\`, \`Проекты/Arduino/firmware/gem_bmc_can_emu/bmc_can_gen.h\`, \`Проекты/Arduino/firmware/gem_bmc_can_emu/README.md\`, \`Проекты/Arduino/firmware/gem_bmc_can_emu/PINOUT.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/README.md\`
- **Снимок:** `.cursor/backups/20260902T145023/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260902T145023`


### 2026-09-02 13:37 — BMC CAN emulator v4 подтверждён на неисправной e6, DTC нет

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/scripts/can-bmc-emulate.py\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/BMC_CAN_EMULATOR_v4_OK.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/CAN_BUS_MAP.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/BMC_EMULATOR_PLAN.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260902T133711/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260902T133711`


### 2026-09-02 12:37 — CAN bus map BMC/VCM fixed 2026-09-02

- **Агент:** cursor
- **Проект:** gem-e6
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/CAN_BUS_MAP.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/BMC_EMULATOR_PLAN.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/CAN_BUS.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/TECH_SUMMARY.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260902T123707/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260902T123707`


### 2026-08-28 13:49 — firmware_EmKit_to_Pylon_Must

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/Eltavr_firmware/A11096_can-rs485-adapter-master_vcs/firmware_EmKit_to_Pylon_Must/README.md\`, \`Проекты/Arduino/firmware/Eltavr_firmware/A11096_can-rs485-adapter-master_vcs/firmware_EmKit_to_Pylon_Must/CHANGELOG.md\`, \`Проекты/Arduino/firmware/Eltavr_firmware/A11096_can-rs485-adapter-master_vcs/firmware_EmKit_to_Pylon_Must/scripts/build-standalone.sh\`, \`Проекты/Arduino/firmware/Eltavr_firmware/A11096_can-rs485-adapter-master_vcs/firmware_EmKit_to_Pylon_Must/firmware/src/a11096vcs.c\`, \`Проекты/Arduino/firmware/Eltavr_firmware/A11096_can-rs485-adapter-master_vcs/firmware_EmKit_to_Pylon_Must/firmware/releases/firmware_EmKit_to_Pylon_Must_standalone.bin\`
- **Снимок:** `.cursor/backups/20260828T134937/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260828T134937`


### 2026-08-28 08:01 — firmware_EmKit_to_Pylon EmKit→Pylon bridge

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/Eltavr_firmware/A11096_can-rs485-adapter-master_vcs/firmware_EmKit_to_Pylon\`, \`Проекты/Arduino/firmware/Eltavr_firmware/A11096_can-rs485-adapter-master_vcs/README.md\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/notes/СОВМЕСТИМОСТЬ_A11034R6.md\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260828T080129/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260828T080129`


### 2026-08-27 16:56 — cursorignore: open Проекты/Arduino again

- **Агент:** cursor
- **Проект:** Documents
- **Файлы:** \`.cursorignore\`
- **Снимок:** `.cursor/backups/20260827T165622/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260827T165622`


### 2026-08-25 18:38 — DHCP брони AiNET WiFi MAC→IP + apply script

- **Агент:** cursor
- **Проект:** Raspberry_Pi_3_HomePortable
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/config/timecapsule/ainet-wifi-reservations.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/config/timecapsule/dhcpd.ainet-wifi.fragment\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/apply-ainet-wifi-dhcp-reservations.sh\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260825T183828/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260825T183828`


### 2026-08-24 14:48 — HA fix: remove missing gpiochip0 after reboot

- **Агент:** cursor
- **Проект:** Apple_HomeKit_accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/docker-compose.yml\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260824T144835/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260824T144835`


### 2026-08-24 14:43 — J75H write via RS485 documented

- **Агент:** cursor
- **Проект:** RS485_CAN_HAT
- **Файлы:** \`Платы и модули/RS485_CAN_HAT/ANT_BMS_J75H_RS485.md\`, \`bms-tools/README_ant_j75h_rs485.md\`
- **Снимок:** `.cursor/backups/20260824T144333/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260824T144333`


### 2026-08-24 14:34 — ANT J75H RS485 9600 зафиксировано

- **Агент:** cursor
- **Проект:** RS485_CAN_HAT
- **Файлы:** \`Платы и модули/RS485_CAN_HAT/ANT_BMS_J75H_RS485.md\`, \`Платы и модули/RS485_CAN_HAT/PINOUT.md\`, \`Платы и модули/RS485_CAN_HAT/RS485_CAN_HAT-1.md\`, \`bms-tools/README_ant_j75h_rs485.md\`, \`bms-tools/ant_bms_probe.py\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260824T143422/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260824T143422`


### 2026-08-20 09:46 — MUST PV18-4024: ещё один инвертор прошит рабочим профилем; chat/handoff обновлены

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260820T094624/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260820T094624`


### 2026-08-18 16:16 — changelog/chat: открыт доступ к Платы и модули

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260818T161622/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T161622`


### 2026-08-18 16:16 — открыть Платы и модули и .cursor (rules/skills/chat) в агенте; убрать из .cursorignore

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursorignore\`
- **Снимок:** `.cursor/backups/20260818T161600/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T161600`


### 2026-08-18 13:06 — Vega MT X LTE: монтаж на Touareg GP переписан на все 3 CAN

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.md\`, \`Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.html\`, \`Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.pdf\`, \`Платы и модули/Vega_MT_X_LTE/PINOUT.md\`, \`Платы и модули/Vega_MT_X_LTE/TECH_SUMMARY.md\`, \`Платы и модули/Vega_MT_X_LTE/download_report.json\`
- **Снимок:** `.cursor/backups/20260818T130623/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T130623`


### 2026-08-18 12:58 — Vega MT X LTE: монтажная инструкция оформлена в PDF

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** `Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.html`, `Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.pdf`
- **Снимок:** `.cursor/backups/20260818T125803/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T125803`


### 2026-08-18 12:58 — добавлен PDF монтажной инструкции Vega MT X LTE для Touareg GP 2009 CASA

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.html\`, \`Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.pdf\`
- **Снимок:** `.cursor/backups/20260818T125818/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T125818`


### 2026-08-18 12:57 — Vega MT X LTE: собран модуль и инструкция для Touareg GP 2009 CASA

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** `Платы и модули/Vega_MT_X_LTE/source_url.txt`, `Платы и модули/Vega_MT_X_LTE/source_page.html`, `Платы и модули/Vega_MT_X_LTE/download_report.json`, `Платы и модули/Vega_MT_X_LTE/TECH_SUMMARY.md`, `Платы и модули/Vega_MT_X_LTE/PINOUT.md`, `Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.md`
- **Снимок:** `.cursor/backups/20260818T125717/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T125717`


### 2026-08-18 12:57 — добавлен модуль Vega_MT_X_LTE и инструкция установки для Touareg GP 2009 CASA

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`Платы и модули/Vega_MT_X_LTE/source_url.txt\`, \`Платы и модули/Vega_MT_X_LTE/source_page.html\`, \`Платы и модули/Vega_MT_X_LTE/download_report.json\`, \`Платы и модули/Vega_MT_X_LTE/TECH_SUMMARY.md\`, \`Платы и модули/Vega_MT_X_LTE/PINOUT.md\`, \`Платы и модули/Vega_MT_X_LTE/INSTALL_Touareg_GP_2009_CASA.md\`
- **Снимок:** `.cursor/backups/20260818T125717/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T125717`


### 2026-08-18 11:45 — удалён ungate: extension, ~/.ungate, UFW restore

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/scripts/restore-pi5-ufw.sh\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260818T114556/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T114556`


### 2026-08-18 11:36 — ANT24C: одна компактная карточка для всех 13 ячеек

- **Агент:** cursor
- **Проект:** apple_homekit_accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/ant-bms-24c.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260818T113621/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T113621`


### 2026-08-18 11:34 — ANT24C: точный вывод ячеек и честная верификация balancer/last_cmd

- **Агент:** cursor
- **Проект:** apple_homekit_accessory
- **Файлы:** \`bms-tools/ant24c_logger.py\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/ant-bms-24c.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260818T113421/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T113421`


### 2026-08-18 11:23 — ANT24C: точность 0.001 В и визуальная сетка gauge по 13 ячейкам

- **Агент:** cursor
- **Проект:** apple_homekit_accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/packages/ant24c.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/ant-bms-24c.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260818T112346/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T112346`


### 2026-08-18 11:20 — ANT24C: добавлены напряжения 13 ячеек в JSON/HA/dashboard

- **Агент:** cursor
- **Проект:** apple_homekit_accessory
- **Файлы:** \`bms-tools/ant24c_logger.py\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/packages/ant24c.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/dashboards/ant-bms-24c.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260818T112050/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260818T112050`


### 2026-08-17 16:40 — n8n удалён; дашборд Малинка 5 в Cursor Agent

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/scripts/build-pi5-dash.py\`, \`Проекты/Cursor Agent/scripts/pi5-dash-refresh.service\`, \`Проекты/Cursor Agent/scripts/pi5-dash-refresh.timer\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/CHANGELOG.md\`, \`Проекты/README.md\`
- **Снимок:** `.cursor/backups/20260817T164055/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260817T164055`


### 2026-08-17 15:24 — status bar Ungate show immediately

- **Агент:** cursor
- **Проект:** ungate
- **Файлы:** \`ungate/apps/extension/src/extension-controller.ts\`, \`ungate/apps/extension/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260817T152417/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260817T152417`


### 2026-08-17 15:16 — OAuth :1455 always-on + Keenetic :47821 + tunnel retry

- **Агент:** cursor
- **Проект:** ungate
- **Файлы:** \`ungate/apps/api/src/auth/openai/callback-server.ts\`, \`ungate/apps/api/src/server.ts\`, \`ungate/apps/api/src/routes/auth.ts\`, \`ungate/apps/extension/CHANGELOG.md\`, \`.cursor/scripts/restore-pi5-ufw.sh\`, \`.cursor/scripts/install-ungate-wan-portforward.sh\`
- **Снимок:** `.cursor/backups/20260817T151611/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260817T151611`


### 2026-08-17 14:45 — EmKit BMS HTTPS: TLS handshake в потоке + watchdog, чтобы сканеры не вешали :8443

- **Агент:** cursor
- **Проект:** web_config_bms
- **Файлы:** \`Проекты/web_config_bms/serve-https.py\`, \`Проекты/web_config_bms/scripts/watchdog.sh\`, \`Проекты/web_config_bms/install-pi.sh\`, \`Проекты/web_config_bms/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260817T144540/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260817T144540`


### 2026-08-17 10:51 — MUST LP16-48100 module folder + RU manual

- **Агент:** cursor
- **Проект:** solar-inverters
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Must_LP16-48100\`, \`Платы и модули/Солнечные_инверторы/README.md\`, \`Платы и модули/Солнечные_инверторы/Must_PV18-4024_PRO_II/README.md\`
- **Снимок:** `.cursor/backups/20260817T105124/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260817T105124`


### 2026-08-14 16:38 — залиты lcd/bc/main без reset

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/main.py\`, \`Проекты/audi_bc_pico/scripts/upload.sh\`
- **Снимок:** `.cursor/backups/20260814T163820/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T163820`


### 2026-08-14 16:08 — без 5-baud, жёлтый старт, только JSON

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/main.py\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T160848/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T160848`


### 2026-08-14 16:06 — без машины, отладка JSON/KW1281

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/scripts/send-json.sh\`, \`Проекты/audi_bc_pico/README.md\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T160607/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T160607`


### 2026-08-14 16:02 — без перерисовки машины каждый кадр

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T160232/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T160232`


### 2026-08-14 15:54 — проброс SSH WAN :22 на Malinka 5

- **Агент:** cursor
- **Проект:** keenetic
- **Файлы:** \`.cursor/scripts/install-pi5-ssh-wan-portforward.sh\`, \`keenetic-routers.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260814T155442/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T155442`


### 2026-08-14 15:53 — только цифры RPM и ОЖ

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T155301/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T155301`


### 2026-08-14 15:49 — жёлтый RPM, красная ОЖ

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T154931/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T154931`


### 2026-08-14 15:49 — дашборд: fetch fallback вместо только proxy timeout

- **Агент:** cursor
- **Проект:** ungate
- **Файлы:** \`ungate/apps/web/src/shared/api.ts\`, \`ungate/apps/extension/src/dashboard.ts\`
- **Снимок:** `.cursor/backups/20260814T154905/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T154905`


### 2026-08-14 15:47 — крупные RPM сверху и ОЖ снизу

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/main.py\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T154754/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T154754`


### 2026-08-14 15:45 — крупные RPM и ОЖ

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T154523/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T154523`


### 2026-08-14 15:43 — обёртка cloudflared HTTP/2 — Ungate в памяти ещё без флага

- **Агент:** cursor
- **Проект:** ungate
- **Файлы:** \`ungate/scripts/cloudflared-force-http2.sh\`, \`ungate/apps/extension/src/tunnel-manager.ts\`
- **Снимок:** `.cursor/backups/20260814T154359/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T154359`


### 2026-08-14 15:43 — машина x0.5 по центру

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/scripts/gen_car_rle.py\`, \`Проекты/audi_bc_pico/firmware/car0.bin\`, \`Проекты/audi_bc_pico/firmware/car1.bin\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T154304/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T154304`


### 2026-08-14 15:41 — машина x0.25 по центру

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/scripts/gen_car_rle.py\`, \`Проекты/audi_bc_pico/firmware/car0.bin\`, \`Проекты/audi_bc_pico/firmware/car1.bin\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T154138/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T154138`


### 2026-08-14 15:38 — пусто: не грузить car.bin в RAM

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/main.py\`, \`Проекты/audi_bc_pico/firmware/car0.bin\`, \`Проекты/audi_bc_pico/firmware/car1.bin\`
- **Снимок:** `.cursor/backups/20260814T153822/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T153822`


### 2026-08-14 15:36 — Ungate tunnel HTTP/2 вместо QUIC

- **Агент:** cursor
- **Проект:** ungate
- **Файлы:** \`ungate/apps/extension/src/tunnel-manager.ts\`, \`ungate/scripts/tunnel/main.ts\`, \`ungate/apps/extension/tests/unit/tunnel-manager-binary-path.test.ts\`, \`ungate/apps/extension/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T153624/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T153624`


### 2026-08-14 15:33 — вид сверху A4 как 3dMFD

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/car0.bin\`, \`Проекты/audi_bc_pico/firmware/car1.bin\`, \`Проекты/audi_bc_pico/scripts/upload.sh\`, \`Проекты/audi_bc_pico/scripts/gen_car_rle.py\`, \`Проекты/audi_bc_pico/README.md\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T153351/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T153351`


### 2026-08-14 15:28 — UI как 3D Color MFD тахометр+ОЖ

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`
- **Снимок:** `.cursor/backups/20260814T152802/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T152802`


### 2026-08-14 15:27 — Ungate dashboard API proxy для Remote SSH Failed to fetch

- **Агент:** cursor
- **Проект:** ungate
- **Файлы:** \`ungate/apps/web/src/shared/api.ts\`, \`ungate/apps/web/src/shared/vscode.ts\`, \`ungate/apps/extension/src/dashboard.ts\`, \`ungate/packages/shared/src/frontend.ts\`, \`ungate/apps/extension/CHANGELOG.md\`, \`ungate/apps/extension/tests/unit/dashboard-set-port.test.ts\`
- **Снимок:** `.cursor/backups/20260814T152730/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T152730`


### 2026-08-14 15:23 — без полосок, поворот влево 90 в буфере

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/lcd.py\`, \`Проекты/audi_bc_pico/firmware/main.py\`
- **Снимок:** `.cursor/backups/20260814T152314/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T152314`


### 2026-08-14 15:19 — явный reset после заливки, полоски затем БК

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/main.py\`, \`Проекты/audi_bc_pico/firmware/lcd.py\`, \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/scripts/upload.sh\`
- **Снимок:** `.cursor/backups/20260814T151912/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T151912`


### 2026-08-14 15:16 — БК на рабочем LCD RPM+ОЖ

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/main.py\`
- **Снимок:** `.cursor/backups/20260814T151616/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T151616`


### 2026-08-14 15:14 — тач отключён, только полоски

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/lcd.py\`
- **Снимок:** `.cursor/backups/20260814T151449/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T151449`


### 2026-08-14 15:11 — тест экрана цветные полоски Waveshare

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/main.py\`
- **Снимок:** `.cursor/backups/20260814T151134/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T151134`


### 2026-08-14 15:08 — возврат первого рабочего LCD show_up/show_down

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/lcd.py\`, \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/main.py\`
- **Снимок:** `.cursor/backups/20260814T150858/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T150858`


### 2026-08-14 15:06 — LCD 16-bit Waveshare C 0x28

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/lcd.py\`, \`Проекты/audi_bc_pico/firmware/bc.py\`
- **Снимок:** `.cursor/backups/20260814T150648/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T150648`


### 2026-08-14 15:01 — LCD Waveshare init + UF2 из BOOTSEL, красный тест

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/lcd.py\`, \`Проекты/audi_bc_pico/firmware/main.py\`, \`Проекты/audi_bc_pico/firmware/bc.py\`
- **Снимок:** `.cursor/backups/20260814T150118/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T150118`


### 2026-08-14 14:57 — починен сброс USB после первого кадра

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/lcd.py\`, \`Проекты/audi_bc_pico/firmware/kline.py\`
- **Снимок:** `.cursor/backups/20260814T145712/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T145712`


### 2026-08-14 14:51 — убрано демо, только живые RPM/ОЖ

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/README.md\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T145112/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T145112`


### 2026-08-14 14:49 — портрет 320x480 обороты и ОЖ группа 1

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/lcd.py\`, \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/kline.py\`, \`Проекты/audi_bc_pico/README.md\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T144950/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T144950`


### 2026-08-14 14:43 — демо кириллица K-line UART0 без большого framebuf

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware/lcd.py\`, \`Проекты/audi_bc_pico/firmware/bc.py\`, \`Проекты/audi_bc_pico/firmware/kline.py\`, \`Проекты/audi_bc_pico/firmware/main.py\`, \`Проекты/audi_bc_pico/firmware/font8.py\`, \`Проекты/audi_bc_pico/scripts/upload.sh\`, \`Проекты/audi_bc_pico/README.md\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T144328/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T144328`


### 2026-08-14 14:30 — БК Audi A4 B5 на Pico-Eval-Board DEMO+JSON UART

- **Агент:** cursor
- **Проект:** audi_bc_pico
- **Файлы:** \`Проекты/audi_bc_pico/firmware\`, \`Проекты/audi_bc_pico/scripts\`, \`Проекты/audi_bc_pico/README.md\`, \`Проекты/audi_bc_pico/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260814T143016/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T143016`


### 2026-08-14 14:16 — Модуль Waveshare Pico-Eval-Board: схема, демо, PINOUT, TECH_SUMMARY

- **Агент:** cursor
- **Проект:** Pico-Eval-Board
- **Файлы:** \`Платы и модули/Pico-Eval-Board\`, \`.cursor/rules/module-docs-priority.mdc\`
- **Снимок:** `.cursor/backups/20260814T141621/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260814T141621`


### 2026-08-13 16:55 — холст: сервисы Pi 5

- **Агент:** cursor
- **Проект:** n8n
- **Файлы:** \`Проекты/n8n/dashboard/build-pi5-dash.py\`
- **Снимок:** `.cursor/backups/20260813T165548/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T165548`


### 2026-08-13 16:52 — холст дашборда: все Google-связи

- **Агент:** cursor
- **Проект:** n8n
- **Файлы:** \`Проекты/n8n/CHANGELOG.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260813T165211/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T165211`


### 2026-08-13 16:48 — архив 11 сценариев, один дашборд

- **Агент:** cursor
- **Проект:** n8n
- **Файлы:** \`Проекты/n8n/dashboard/build-pi5-dash.py\`, \`Проекты/n8n/README.md\`, \`Проекты/n8n/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260813T164855/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T164855`


### 2026-08-13 16:46 — дашборд Pi 5: webhook + PWA вкладка + таймер снимка

- **Агент:** cursor
- **Проект:** n8n
- **Файлы:** \`Проекты/n8n/dashboard/build-pi5-dash.py\`, \`Проекты/n8n/workflows/pi5-dashboard.js\`, \`Проекты/n8n/README.md\`, \`Проекты/n8n/CHANGELOG.md\`, \`Проекты/Cursor Agent/api/sites_proxy.py\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260813T164638/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T164638`


### 2026-08-13 16:26 — n8n: карта всех Google-связей, просмотр таблиц и папок

- **Агент:** cursor
- **Проект:** n8n
- **Файлы:** \`Проекты/n8n/README.md\`, \`Проекты/n8n/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260813T162648/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T162648`


### 2026-08-13 16:22 — n8n Google: Sheets/Drive/Gmail сценарии коммуналка и UPS

- **Агент:** cursor
- **Проект:** n8n
- **Файлы:** \`Проекты/n8n/README.md\`, \`Проекты/n8n/CHANGELOG.md\`, \`Проекты/n8n/workflows/ups-production-overview.js\`, \`Проекты/n8n/workflows/komunalka-drive-folders.js\`, \`Проекты/n8n/workflows/komunalka-gmail-pdf.js\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260813T162254/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T162254`


### 2026-08-13 16:13 — WAN HTTPS n8n :5679 + Keenetic

- **Агент:** cursor
- **Проект:** n8n
- **Файлы:** \`Проекты/n8n/docker-compose.yml\`, \`Проекты/n8n/nginx/n8n.conf\`, \`Проекты/n8n/README.md\`, \`Проекты/n8n/CHANGELOG.md\`, \`Проекты/n8n/.env.example\`, \`.cursor/scripts/install-n8n-wan-portforward.sh\`, \`.cursor/scripts/restore-pi5-ufw.sh\`, \`Проекты/Cursor Agent/api/sites_proxy.py\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260813T161355/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T161355`


### 2026-08-13 16:08 — n8n во вкладке PWA Сайты

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/sites_proxy.py\`, \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/CHANGELOG.md\`, \`Проекты/n8n/README.md\`, \`Проекты/n8n/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260813T160836/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T160836`


### 2026-08-13 16:04 — Cursor MCP подключён к n8n

- **Агент:** cursor
- **Проект:** n8n
- **Файлы:** \`Проекты/n8n/README.md\`, \`Проекты/n8n/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`.cursor/GOOGLE_SERVICES.md\`
- **Снимок:** `.cursor/backups/20260813T160425/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T160425`


### 2026-08-13 15:57 — Установлен self-hosted n8n Docker на Pi 5, порт 5678

- **Агент:** cursor
- **Проект:** n8n
- **Файлы:** \`Проекты/n8n/docker-compose.yml\`, \`Проекты/n8n/README.md\`, \`Проекты/n8n/CHANGELOG.md\`, \`Проекты/n8n/.env.example\`, \`Проекты/README.md\`, \`.cursor/scripts/restore-pi5-ufw.sh\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260813T155712/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260813T155712`


### 2026-08-09 17:45 — BC ECU minimal docs

- **Агент:** cursor
- **Проект:** Audi_A4_B5_ECU
- **Файлы:** \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260809T174510/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T174510`


### 2026-08-09 17:26 — SIMOS real groups map

- **Агент:** cursor
- **Проект:** Audi_A4_B5_ECU
- **Файлы:** \`Платы и модули/Audi_A4_B5_ECU_AHL_3B0_907_557_B/SIMOS_GROUPS_REAL.md\`, \`Платы и модули/Audi_A4_B5_ECU_AHL_3B0_907_557_B/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260809T172619/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T172619`


### 2026-08-09 17:15 — БК freeze: chat/handoff + docs pointer

- **Агент:** cursor
- **Проект:** cluster_pi
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260809T171513/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T171513`


### 2026-08-09 16:40 — БК engine_cl docs

- **Агент:** cursor
- **Проект:** Audi_A4_B5_ECU
- **Файлы:** \`Платы и модули/Audi_A4_B5_ECU_AHL_3B0_907_557_B/TECH_SUMMARY.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260809T164000/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T164000`


### 2026-08-09 16:10 — ЭБУ 9600 SIMOS статус

- **Агент:** cursor
- **Проект:** Audi_A4_B5_ECU
- **Файлы:** \`Платы и модули/Audi_A4_B5_ECU_AHL_3B0_907_557_B/TECH_SUMMARY.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260809T161055/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T161055`


### 2026-08-09 13:22 — FIS MFA 14.1 handoff notes

- **Агент:** cursor
- **Проект:** cluster_pi
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260809T132259/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T132259`


### 2026-08-09 12:40 — завод АКПП подтверждено владельцем

- **Агент:** cursor
- **Проект:** audi-ecu-ahl
- **Файлы:** \`Платы и модули/Audi_A4_B5_ECU_AHL_3B0_907_557_B/TECH_SUMMARY.md\`, \`.cursor/data/audi_a4_vehicle_profile.yaml\`
- **Снимок:** `.cursor/backups/20260809T124059/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T124059`


### 2026-08-09 01:31 — вода полный обход ЛК

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/scripts/voda-full-export.mjs\`, \`Проекты/komunalka/scripts/monthly-drive-sync.sh\`, \`Проекты/komunalka/DRIVE_SYNC.md\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260809T013151/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T013151`


### 2026-08-09 01:11 — ежемесячные чеки и показания

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/DRIVE_SYNC.md\`, \`Проекты/komunalka/scripts/monthly-drive-sync.sh\`, \`Проекты/komunalka/scripts/install-monthly-drive-sync-timer.sh\`, \`Проекты/komunalka/CHANGELOG.md\`, \`.cursor/rules/komunalka-drive-monthly.mdc\`
- **Снимок:** `.cursor/backups/20260809T011141/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T011141`


### 2026-08-09 01:07 — корень Drive без файлов

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/scripts/drive-lib.mjs\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260809T010738/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T010738`


### 2026-08-09 01:06 — без счётчика без CSV-сводки

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/scripts/drive-lib.mjs\`, \`Проекты/komunalka/scripts/export-all-services-to-drive.mjs\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260809T010643/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T010643`


### 2026-08-09 01:04 — вода и счётчики: единицы расхода

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/scripts/drive-lib.mjs\`, \`Проекты/komunalka/scripts/export-all-services-to-drive.mjs\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260809T010459/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T010459`


### 2026-08-09 01:02 — газ CSV м³ расход

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/scripts/drive-lib.mjs\`, \`Проекты/komunalka/scripts/export-all-services-to-drive.mjs\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260809T010248/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T010248`


### 2026-08-09 00:23 — export all services to Drive

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/scripts/export-all-services-to-drive.mjs\`, \`Проекты/komunalka/scripts/drive-lib.mjs\`, \`Проекты/komunalka/CHANGELOG.md\`, \`Проекты/komunalka/.gitignore\`
- **Снимок:** `.cursor/backups/20260809T002330/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260809T002330`


### 2026-08-07 19:44 — БК 5″ полный функционал UI

- **Агент:** cursor
- **Проект:** cluster_pi
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/data/bc_full_5inch.png\`
- **Снимок:** `.cursor/backups/20260807T194450/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260807T194450`


### 2026-08-07 19:31 — БК: ускорен опрос K-line

- **Агент:** cursor
- **Проект:** cluster_pi
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260807T193106/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260807T193106`


### 2026-08-07 18:22 — режим QR decode script

- **Агент:** cursor
- **Проект:** LiFePO4_Cell_QR_Decoder
- **Файлы:** \`Платы и модули/LiFePO4_Cell_QR_Decoder/scripts/decode_cell_qr.py\`, \`Платы и модули/LiFePO4_Cell_QR_Decoder/README.md\`, \`Платы и модули/LiFePO4_Cell_QR_Decoder/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260807T182208/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260807T182208`


### 2026-08-07 18:17 — QR decoders + decode 04QCB72 LF230

- **Агент:** cursor
- **Проект:** LiFePO4_Cell_QR_Decoder
- **Файлы:** \`Платы и модули/LiFePO4_Cell_QR_Decoder\`
- **Снимок:** `.cursor/backups/20260807T181719/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260807T181719`


### 2026-08-06 16:47 — расшифровка ошибок EZGO на русском

- **Агент:** cursor
- **Проект:** EZGO_Club_Car
- **Файлы:** \`Платы и модули/Электрокары/EZGO_Club_Car/notes/FAULT_CODES_EXTRACT.md\`, \`Платы и модули/Электрокары/EZGO_Club_Car/FAULT_CODES.md\`
- **Снимок:** `.cursor/backups/20260806T164721/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T164721`


### 2026-08-06 16:45 — доп мануалы и схемы wiring

- **Агент:** cursor
- **Проект:** EZGO_Club_Car
- **Файлы:** \`Платы и модули/Электрокары/EZGO_Club_Car/WIRING_REFERENCE.md\`, \`Платы и модули/Электрокары/EZGO_Club_Car/TECH_SUMMARY.md\`, \`Платы и модули/Электрокары/EZGO_Club_Car/downloads\`, \`Платы и модули/Электрокары/EZGO_Club_Car/pic/wiring\`, \`Платы и модули/Электрокары/EZGO_Club_Car/pic/parts\`
- **Снимок:** `.cursor/backups/20260806T164530/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T164530`


### 2026-08-06 16:17 — Снимки настроек i.Solar + скрипт fetch

- **Агент:** cursor
- **Проект:** SILA_VM_II_Premium_Plus_6.2K
- **Файлы:** \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/settings\`, \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K/РУКОВОДСТВО_RU.md\`
- **Снимок:** `.cursor/backups/20260806T161728/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T161728`


### 2026-08-06 13:49 — Новая папка SILA VM II Premium+ 6.2K, EN мануалы, РУКОВОДСТВО_RU

- **Агент:** cursor
- **Проект:** SILA_VM_II_Premium_Plus_6.2K
- **Файлы:** \`Платы и модули/Солнечные_инверторы/SILA_VM_II_Premium_Plus_6.2K\`, \`Платы и модули/Солнечные_инверторы/README.md\`, \`Платы и модули/Солнечные_инверторы/Инверторы_сводка_токи_заряда/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260806T134929/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T134929`


### 2026-08-06 12:27 — Переименование папки Deye_Inverter → Deye_SUN-6.6K-OG03LP1-EU-AM2

- **Агент:** cursor
- **Проект:** Deye_SUN-6.6K-OG03LP1-EU-AM2
- **Файлы:** \`Платы и модули/Солнечные_инверторы/README.md\`, \`Платы и модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260806T122710/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T122710`


### 2026-08-06 12:26 — Только 6.6K; РУКОВОДСТВО_RU; чужие PDF удалены

- **Агент:** cursor
- **Проект:** Deye_Inverter
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_Inverter/РУКОВОДСТВО_RU.md\`, \`Платы и модули/Солнечные_инверторы/Deye_Inverter/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Deye_Inverter/PINOUT.md\`, \`Платы и модули/Солнечные_инверторы/Deye_Inverter/download_report.json\`, \`Платы и модули/Солнечные_инверторы/README.md\`
- **Снимок:** `.cursor/backups/20260806T122610/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T122610`


### 2026-08-06 12:23 — Модель пользователя SUN-6.6K-OG03LP1-EU-AM2; TECH/PINOUT/сводка токов

- **Агент:** cursor
- **Проект:** Deye_Inverter
- **Файлы:** \`Платы и модули/Солнечные_инверторы/Deye_Inverter/TECH_SUMMARY.md\`, \`Платы и модули/Солнечные_инверторы/Deye_Inverter/PINOUT.md\`, \`Платы и модули/Солнечные_инверторы/Инверторы_сводка_токи_заряда/TECH_SUMMARY.md\`
- **Снимок:** `.cursor/backups/20260806T122355/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T122355`


### 2026-08-06 12:21 — FAULT_CODES шпаргалка миганий ST Shuttle

- **Агент:** cursor
- **Проект:** EZGO_Club_Car
- **Файлы:** \`Платы и модули/Электрокары/EZGO_Club_Car/FAULT_CODES.md\`
- **Снимок:** `.cursor/backups/20260806T122120/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T122120`


### 2026-08-06 12:11 — шпаргалка ошибок GEM e6

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/FAULT_CODES.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/DTC_FULL_TABLE.md\`, \`Платы и модули/Электрокары/Polaris_GEM_e6_2017/notes/CHARGING_STATION_LED.md\`
- **Снимок:** `.cursor/backups/20260806T121131/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T121131`


### 2026-08-06 11:58 — объединение инверторов в Солнечные_инверторы

- **Агент:** cursor
- **Проект:** Солнечные_инверторы
- **Файлы:** \`Платы и модули/Deye_Inverter\`, \`Платы и модули/Must_PH1100_12kW\`, \`Платы и модули/Must_PV18-4024_PRO_II\`, \`Платы и модули/Must_PV18-8048_PRO_II\`, \`Платы и модули/Adion_Expert_6kW_Twin\`, \`Платы и модули/Инверторы_сводка_токи_заряда\`
- **Снимок:** `.cursor/backups/20260806T115804/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T115804`


### 2026-08-06 11:57 — README индекс электрокаров

- **Агент:** cursor
- **Проект:** Электрокары
- **Файлы:** \`Платы и модули/Электрокары/README.md\`
- **Снимок:** `.cursor/backups/20260806T115710/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T115710`


### 2026-08-06 11:55 — объединение GEM+EZGO в Платы и модули/Электрокары

- **Агент:** cursor
- **Проект:** Электрокары
- **Файлы:** \`Платы и модули/Polaris_GEM_e6_2017\`, \`Платы и модули/EZGO_Club_Car\`, \`Платы и модули\`
- **Снимок:** `.cursor/backups/20260806T115540/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T115540`


### 2026-08-06 11:53 — новая папка EZGO/Club Car + мануал ST Shuttle из бэкапа GEM

- **Агент:** cursor
- **Проект:** EZGO_Club_Car
- **Файлы:** \`Платы и модули/EZGO_Club_Car\`
- **Снимок:** `.cursor/backups/20260806T115305/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T115305`


### 2026-08-06 10:43 — удалить VCM 3стр (есть в SM 9940314)

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Polaris_GEM_e6_2017/downloads/GEM_VCM_Diagram_2016-2022.pdf\`, \`Платы и модули/Polaris_GEM_e6_2017/pic/vcm_diagram_p1.png\`, \`Платы и модули/Polaris_GEM_e6_2017/TECH_SUMMARY.md\`, \`Платы и модули/Polaris_GEM_e6_2017/PINOUT.md\`, \`Платы и модули/Polaris_GEM_e6_2017/download_report.json\`
- **Снимок:** `.cursor/backups/20260806T104341/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T104341`


### 2026-08-06 10:40 — Brandfolder: SM 2016-2023 + схемы

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Polaris_GEM_e6_2017/TECH_SUMMARY.md\`, \`Платы и модули/Polaris_GEM_e6_2017/download_report.json\`, \`Платы и модули/Polaris_GEM_e6_2017/notes/brandfolder_findings.md\`
- **Снимок:** `.cursor/backups/20260806T104029/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T104029`


### 2026-08-06 10:25 — порядок: убрать дубли PDF и чужой E-Z-GO

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Polaris_GEM_e6_2017/downloads\`, \`Платы и модули/Polaris_GEM_e6_2017/TECH_SUMMARY.md\`, \`Платы и модули/Polaris_GEM_e6_2017/source_url.txt\`, \`Платы и модули/Polaris_GEM_e6_2017/notes\`
- **Снимок:** `.cursor/backups/20260806T102501/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T102501`


### 2026-08-06 09:44 — VCM wiring Scribd extract

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Polaris_GEM_e6_2017/VCM_WIRING_2016-2022.md\`
- **Снимок:** `.cursor/backups/20260806T094423/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T094423`


### 2026-08-06 09:44 — VCM wiring 2016-2022 from Scribd

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Polaris_GEM_e6_2017/ЭЛЕКТРОСХЕМА.md\`, \`Платы и модули/Polaris_GEM_e6_2017/source_url.txt\`
- **Снимок:** `.cursor/backups/20260806T094407/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T094407`


### 2026-08-06 09:13 — Deye OG03: структура папки, EN manual, RU SolarCrown, TECH_SUMMARY

- **Агент:** cursor
- **Проект:** Deye_Inverter
- **Файлы:** \`Платы и модули/Deye_Inverter\`
- **Снимок:** `.cursor/backups/20260806T091302/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260806T091302`


### 2026-08-04 16:09 — HA Обзор: убраны битые ESP Camera, график CPU на overview

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/configuration.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/lovelace.lovelace\`
- **Снимок:** `.cursor/backups/20260804T160908/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260804T160908`


### 2026-08-04 15:58 — Pi5 HA CPU temp: timer вместо сломанного cron с пробелами

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/scripts/publish_cpu_temp.sh\`, \`Проекты/Apple HomeKit accessory/home_assistant/scripts/publish_pi5_host_status.sh\`, \`Проекты/Apple HomeKit accessory/home_assistant/scripts/install-pi5-ha-host-status.sh\`, \`Проекты/Apple HomeKit accessory/home_assistant/scripts/pi5-ha-cpu-temp.service\`, \`Проекты/Apple HomeKit accessory/home_assistant/scripts/pi5-ha-cpu-temp.timer\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/configuration.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260804T155804/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260804T155804`


### 2026-08-04 15:52 — HA Sites: /auth escape + Location rewrite + shim

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/sites_proxy.py\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260804T155236/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260804T155236`


### 2026-08-04 15:49 — edm-web после reboot: убран Documents.mount, Restart=always

- **Агент:** cursor
- **Проект:** EDM
- **Файлы:** \`Проекты/EDM/scripts/edm-web.service\`, \`Проекты/EDM/CHANGELOG.md\`, \`.cursor/scripts/fix-documents-paths.sh\`
- **Снимок:** `.cursor/backups/20260804T154901/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260804T154901`


### 2026-08-04 15:14 — схемы wiring JPG + WIRING_PINOUT

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Polaris_GEM_e6_2017/ЭЛЕКТРОСХЕМА.md\`, \`Платы и модули/Polaris_GEM_e6_2017/WIRING_PINOUT.md\`, \`Платы и модули/Polaris_GEM_e6_2017/downloads/wiring\`
- **Снимок:** `.cursor/backups/20260804T151406/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260804T151406`


### 2026-08-04 15:02 — папка GEM + ЭЛЕКТРОСХЕМА + скрипты скачивания

- **Агент:** cursor
- **Проект:** Polaris_GEM_e6_2017
- **Файлы:** \`Платы и модули/Polaris_GEM_e6_2017/ЭЛЕКТРОСХЕМА.md\`, \`Платы и модули/Polaris_GEM_e6_2017/TECH_SUMMARY.md\`, \`Платы и модули/Polaris_GEM_e6_2017/scripts/download-key-pages.py\`, \`Платы и модули/Polaris_GEM_e6_2017/scripts/download-electrical.sh\`, \`Платы и модули/Polaris_GEM_e6_2017/scripts/download-pages.py\`, \`Платы и модули/Polaris_GEM_e6_2017/source_url.txt\`
- **Снимок:** `.cursor/backups/20260804T150258/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260804T150258`


### 2026-08-03 18:29 — google-oauth phone page

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/google_oauth_phone.py\`, \`Проекты/Cursor Agent/api/mvp_app.py\`
- **Снимок:** `.cursor/backups/20260803T182914/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260803T182914`


### 2026-08-03 18:05 — Переименование Инструкции PTV → Инструкции Эльтавр

- **Агент:** cursor
- **Проект:** instructions-eltavr
- **Файлы:** \`Инструкции Эльтавр/README.md\`, \`Инструкции для сервиса Эльтавр/README.md\`
- **Снимок:** `.cursor/backups/20260803T180559/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260803T180559`


### 2026-08-03 18:05 — Папка Инструкции PTV

- **Агент:** cursor
- **Проект:** instructions-ptv
- **Файлы:** \`Инструкции PTV/README.md\`, \`Инструкции PTV/Диагностика_нет_данных_на_мониторе_Як_Дилижанс.html\`, \`Инструкции PTV/downloads/Диагностика_нет_данных_на_мониторе_Як_Дилижанс.pdf\`, \`Инструкции для сервиса Эльтавр/README.md\`
- **Снимок:** `.cursor/backups/20260803T180532/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260803T180532`


### 2026-08-01 17:35 — клиент appletv в 3x-ui + vpn-guide

- **Агент:** cursor
- **Проект:** vpn
- **Файлы:** \`vpn-guide.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260801T173540/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260801T173540`


### 2026-07-31 10:52 — JIKONG_BMS project scaffold

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/JIKONG_BMS\`, \`Проекты/Arduino/firmware/ANT_BMS/PROTOCOL_JK_BMS.md\`, \`Проекты/Arduino/firmware/ANT_BMS/README.md\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260731T105204/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260731T105204`


### 2026-07-29 16:08 — заряд с сети Vbatt

- **Агент:** cursor
- **Проект:** Must_PH1100_12kW
- **Файлы:** \`Платы и модули/Must_PH1100_12kW/notes/GRID_MODE_КРЫМ.md\`
- **Снимок:** `.cursor/backups/20260729T160805/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260729T160805`


### 2026-07-27 20:39 — Kali 5inch HDMI XPT2046 docs

- **Агент:** cursor
- **Проект:** modules
- **Файлы:** \`Платы и модули/HDMI_5inch_800x480_XPT2046/TECH_SUMMARY.md\`, \`Платы и модули/HDMI_5inch_800x480_XPT2046/PINOUT.md\`
- **Снимок:** `.cursor/backups/20260727T203937/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260727T203937`


### 2026-07-25 13:36 — новый модуль MUST PV18-4024 PRO II

- **Агент:** cursor
- **Проект:** Must_PV18-4024
- **Файлы:** \`Платы и модули/Must_PV18-4024_PRO_II\`
- **Снимок:** `.cursor/backups/20260725T133636/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260725T133636`


### 2026-07-23 16:01 — обновлён рабочий дамп после LCD

- **Агент:** cursor
- **Проект:** Adion_Expert_6kW_Twin
- **Файлы:** \`Платы и модули/Adion_Expert_6kW_Twin/applied-settings/inverter_working.txt\`
- **Снимок:** `.cursor/backups/20260723T160151/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260723T160151`


### 2026-07-23 13:34 — Adion_Expert_6kW_Twin module

- **Агент:** cursor
- **Проект:** modules
- **Файлы:** \`Платы и модули/Adion_Expert_6kW_Twin\`
- **Снимок:** `.cursor/backups/20260723T133444/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260723T133444`


### 2026-07-16 16:02 — ANT_LCD hide T1/T2 pages

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`
- **Снимок:** `.cursor/backups/20260716T160234/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T160234`


### 2026-07-16 15:40 — ANT_LCD degree C on temp pages

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.h\`
- **Снимок:** `.cursor/backups/20260716T154029/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T154029`


### 2026-07-16 15:38 — ANT_LCD page2 vertical center

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`
- **Снимок:** `.cursor/backups/20260716T153846/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T153846`


### 2026-07-16 15:35 — ANT_LCD runtime load current only

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/AntBmsCore/AntBmsProtocol.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`
- **Снимок:** `.cursor/backups/20260716T153517/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T153517`


### 2026-07-16 15:33 — ANT_LCD runtime Physics_AH/I

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/AntBmsCore/AntBmsProtocol.cpp\`
- **Снимок:** `.cursor/backups/20260716T153324/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T153324`


### 2026-07-16 15:25 — ANT_LCD vertical bat on page2

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.h\`
- **Снимок:** `.cursor/backups/20260716T152530/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T152530`


### 2026-07-16 14:44 — ANT_LCD remove SOC page

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.h\`
- **Снимок:** `.cursor/backups/20260716T144456/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T144456`


### 2026-07-16 14:35 — ANT_LCD SOC on V+I page text

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`
- **Снимок:** `.cursor/backups/20260716T143551/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T143551`


### 2026-07-16 14:32 — ANT_LCD vertical batteries

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`
- **Снимок:** `.cursor/backups/20260716T143231/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T143231`


### 2026-07-16 14:29 — ANT_LCD nicer battery icon

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.h\`
- **Снимок:** `.cursor/backups/20260716T142941/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T142941`


### 2026-07-16 14:27 — ANT_LCD battery icon on V+I

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`
- **Снимок:** `.cursor/backups/20260716T142700/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T142700`


### 2026-07-16 14:19 — ANT_LCD cell numbers under bars

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`
- **Снимок:** `.cursor/backups/20260716T141918/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T141918`


### 2026-07-16 14:14 — ANT_LCD U+I one page

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.h\`, \`Проекты/Arduino/firmware/ANT_LCD/README.md\`
- **Снимок:** `.cursor/backups/20260716T141402/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T141402`


### 2026-07-16 14:10 — ANT_LCD bars main page 8s

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/README.md\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260716T141045/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T141045`


### 2026-07-16 14:07 — ANT_LCD H/L из BMS + bars UI

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/AntBmsCore/AntBmsProtocol.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260716T140758/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T140758`


### 2026-07-16 12:46 — ANT_LCD: fixed GPIO4/5, link badge OK/RX/TMO

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/AntBmsCore/AntBmsUartClient.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/AntBmsCore/AntBmsUartClient.h\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/DisplayApi/BmsViewModel.h\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/README.md\`, \`Проекты/Arduino/firmware/ANT_LCD/PINOUT.md\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260716T124603/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T124603`


### 2026-07-16 12:35 — ANT_LCD: latin OLED, fix UART0, BMS connect

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD/lib/OledSsd1306/OledSsd1306Display.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/AntBmsCore/AntBmsUartClient.cpp\`, \`Проекты/Arduino/firmware/ANT_LCD/lib/AntBmsCore/AntBmsUartClient.h\`, \`Проекты/Arduino/firmware/ANT_LCD/ANT_LCD.ino\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260716T123553/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T123553`


### 2026-07-16 11:09 — Каркас firmware/ANT_LCD

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_LCD\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260716T110911/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260716T110911`


### 2026-07-13 16:30 — Must PV18: фото с mustups, убраны рендеры PDF

- **Агент:** cursor
- **Проект:** modules
- **Файлы:** \`Платы и модули/Must_PV18-8048_PRO_II/pic/pv18-pro-ii2-1.jpg\`, \`Платы и модули/Must_PV18-8048_PRO_II/pic/pv18-pro-ii2-2.jpg\`, \`Платы и модули/Must_PV18-8048_PRO_II/pic/pv18-pro-ii2-3.jpg\`, \`Платы и модули/Must_PV18-8048_PRO_II/download_report.json\`, \`Платы и модули/Must_PV18-8048_PRO_II/PINOUT.md\`, \`Платы и модули/Must_PV18-8048_PRO_II/TECH_SUMMARY.md\`, \`Платы и модули/Must_PV18-8048_PRO_II/source_url.txt\`
- **Снимок:** `.cursor/backups/20260713T163014/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260713T163014`


### 2026-07-13 14:49 — Must PV18-8048 PRO II карточка модуля

- **Агент:** cursor
- **Проект:** modules
- **Файлы:** \`Платы и модули/Must_PV18-8048_PRO_II/source_url.txt\`, \`Платы и модули/Must_PV18-8048_PRO_II/source_page.html\`, \`Платы и модули/Must_PV18-8048_PRO_II/download_report.json\`, \`Платы и модули/Must_PV18-8048_PRO_II/PINOUT.md\`, \`Платы и модули/Must_PV18-8048_PRO_II/TECH_SUMMARY.md\`, \`Платы и модули/Must_PV18-8048_PRO_II/downloads/4200-010063-0000_PV18_8-12K_PRO_II_T1.0.pdf\`, \`Платы и модули/Must_PV18-8048_PRO_II/pic/manual-01.png\`, \`Платы и модули/Must_PV18-8048_PRO_II/pic/manual-03.png\`
- **Снимок:** `.cursor/backups/20260713T144958/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260713T144958`


### 2026-07-09 15:57 — ANT BMS web v2.8.0 APK parity

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`
- **Снимок:** `.cursor/backups/20260709T155716/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T155716`


### 2026-07-09 15:39 — ANT BMS web v2.7.13 USB hard reconnect + APK default pwd

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T153924/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T153924`


### 2026-07-09 15:35 — ANT BMS web v2.7.12 backend reconnect on save

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T153513/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T153513`


### 2026-07-09 15:33 — ANT BMS web v2.7.11 usb save auto reconnect

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T153305/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T153305`


### 2026-07-09 15:30 — ANT BMS web v2.7.10 save reconnect desktop parity

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T153024/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T153024`


### 2026-07-09 15:26 — ANT BMS web v2.7.9 reconnect after save

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T152629/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T152629`


### 2026-07-09 13:06 — ANT BMS v2.5.4: runtime --297D parser

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`.cursor/AGENT_CHANGES.md\`
- **Снимок:** `.cursor/backups/20260709T130650/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T130650`


### 2026-07-09 13:06 — ANT BMS v2.5.4: runtime parser for --297D...

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** `Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md`, `.cursor/chat.md`, `.cursor/CHAT_HANDOFF.md`, `.cursor/AGENT_CHANGES.md`
- **Снимок:** (см. запись после backup)
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh --last`


### 2026-07-09 12:52 — ANT BMS v2.5.1: оси графиков, время и min/max

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.css\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`.cursor/AGENT_CHANGES.md\`
- **Снимок:** `.cursor/backups/20260709T125221/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T125221`


### 2026-07-09 12:52 — ANT BMS v2.5.1: chart axes/time labels + min/max

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.css`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md`, `.cursor/chat.md`, `.cursor/CHAT_HANDOFF.md`
- **Снимок:** (см. запись после backup)
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh --last`


### 2026-07-09 12:48 — ANT BMS v2.5.0: загрузка SystemLog и графики в веб-конфигураторе

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.css\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/i18n-ru.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`.cursor/AGENT_CHANGES.md\`
- **Снимок:** `.cursor/backups/20260709T124826/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T124826`


### 2026-07-09 12:49 — ANT BMS v2.5.0: SystemLog upload + charts in web UI

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** `Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.css`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/i18n-ru.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md`, `.cursor/chat.md`, `.cursor/CHAT_HANDOFF.md`
- **Снимок:** (см. запись после backup)
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh --last`


### 2026-07-09 12:44 — визуализация SystemLog ANT BMS

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/scripts/visualize_system_log.py\`, \`Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/events.csv\`, \`Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/current_over_time.png\`, \`Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/cells_min_max_over_time.png\`, \`Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/cell_diff_over_time.png\`, \`Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/temperature_over_time.png\`, \`Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/event_type_histogram.png\`, \`Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/cell_positions_uv_histogram.png\`, \`Проекты/Arduino/firmware/ANT_BMS/analysis/SystemLog_20260709_122623/README.md\`, \`Проекты/Arduino/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T124404/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T124404`


### 2026-07-09 12:40 — ANT BMS v2.4.9: имена BLE как в телефоне через bluetoothctl fallback

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`.cursor/AGENT_CHANGES.md\`
- **Снимок:** `.cursor/backups/20260709T124036/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T124036`


### 2026-07-09 12:40 — ANT BMS v2.4.9: BLE names fallback via bluetoothctl

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** `Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md`, `.cursor/chat.md`, `.cursor/CHAT_HANDOFF.md`
- **Снимок:** (см. запись после backup)
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh --last`


### 2026-07-09 12:32 — ANT BMS v2.4.8: имена BLE в scan, без MAC как имени

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`.cursor/AGENT_CHANGES.md\`
- **Снимок:** `.cursor/backups/20260709T123255/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T123255`


### 2026-07-09 12:33 — ANT BMS v2.4.8: fix BLE names (no MAC as title)

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** `Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md`, `.cursor/chat.md`, `.cursor/CHAT_HANDOFF.md`
- **Снимок:** (см. запись после backup)
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh --last`


### 2026-07-09 12:31 — анализ лога ANT BMS и обновление контекста

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T123125/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T123125`


### 2026-07-09 12:30 — ANT BMS v2.4.7: scan без фильтра, видны все BLE устройства

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`.cursor/AGENT_CHANGES.md\`
- **Снимок:** `.cursor/backups/20260709T123001/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T123001`


### 2026-07-09 12:30 — ANT BMS v2.4.7: scan all BLE devices (no filters)

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** `Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md`, `.cursor/chat.md`, `.cursor/CHAT_HANDOFF.md`
- **Снимок:** (см. запись после backup)
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh --last`


### 2026-07-09 12:24 — ANT BMS v2.4.6: состояние UI, русские ошибки, быстрый вход в параметры

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.css\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`.cursor/AGENT_CHANGES.md\`
- **Снимок:** `.cursor/backups/20260709T122403/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T122403`


### 2026-07-09 12:24 — ANT BMS v2.4.6 state UI + ru alarms + faster params entry

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.css`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py`, `Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md`, `.cursor/chat.md`, `.cursor/CHAT_HANDOFF.md`
- **Снимок:** (см. запись после backup)
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh --last`


### 2026-07-09 12:17 — ANT BMS v2.4.5: maximum BLE connect speed mode

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T121709/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T121709`


### 2026-07-09 12:14 — ANT BMS control: chemistry buttons in English, others in Russian

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/commands_catalog.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T121432/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T121432`


### 2026-07-09 12:13 — ANT BMS v2.4.3: fix connect hang with subprocess timeouts + fail-fast 45s

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T121303/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T121303`


### 2026-07-09 12:04 — ANT BMS v2.4.2: SOC labels, CSS busy-overlay, BLE auto-reconnect

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/i18n-ru.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.css\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T120432/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T120432`


### 2026-07-09 11:56 — fix param translations and duplicates v2.4.1

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/i18n-ru.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/param_labels_ru.json\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260709T115615/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T115615`


### 2026-07-09 11:13 — ANT BMS v2.3.5 fail-fast BLE connect

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T111314/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T111314`


### 2026-07-09 11:03 — Safari ws reconnect v66 fix

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/api/ws_chat.py\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T110316/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T110316`


### 2026-07-09 10:56 — PWA v65 iOS Safari WS HTTP 8766

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/api/ws_chat.py\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T105637/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T105637`


### 2026-07-09 10:48 — ANT BMS web v2.3.2 BLE connect fix

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/ble_manager.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/sw.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T104808/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T104808`


### 2026-07-09 10:47 — PWA v64 force cache purge WS fix

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/api/mvp_app.py\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T104712/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T104712`


### 2026-07-09 10:42 — PWA WS LAN fix v63 - no LAN to WAN switch

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T104229/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T104229`


### 2026-07-09 09:39 — APK-like UI v2.1

- **Агент:** cursor
- **Проект:** ANT_BMS
- **Файлы:** \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/index.html\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.css\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/static/app.js\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/ant_protocol.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/ant_dict.py\`, \`Проекты/Arduino/firmware/ANT_BMS/web_configurator/app.py\`, \`Проекты/Arduino/firmware/ANT_BMS/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T093914/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T093914`


### 2026-07-09 09:27 — BMS tab → ANT configurator 8788

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/sites_proxy.py\`, \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T092746/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T092746`


### 2026-07-09 09:22 — PWA WS WAN port fix v61

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260709T092230/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260709T092230`


### 2026-07-08 23:05 — fix sites load failed WAN fallback + sw v60

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260708T230517/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260708T230517`


### 2026-07-07 16:43 — ГдеБЕНЗ мониторинг: gdebenz_client/fuel, команды /gdebenz, таймер

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/gdebenz_client.py\`, \`Проекты/ai_assistant/gdebenz_fuel.py\`, \`Проекты/ai_assistant/telegram_relay.py\`, \`Проекты/ai_assistant/bot_ui.py\`, \`Проекты/ai_assistant/scripts/install-gdebenz-fuel-timer.sh\`, \`Проекты/ai_assistant/data/gdebenz-fuel.json\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260707T164332/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260707T164332`


### 2026-07-07 15:26 — a20014_v26_ant fork from v7

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/Eltavr_firmware/a20014_v26_ant\`, \`Проекты/Arduino/firmware/Eltavr_firmware/a20014_plata_monitora/README.md\`, \`Проекты/Arduino/firmware/Eltavr_firmware/README.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260707T152606/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260707T152606`


### 2026-07-07 09:51 — Bybit trailing SL profile B

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`.cursor/scripts/bybit-auto-trader.py\`, \`.cursor/data/bybit-auto-confirm.json\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260707T095128/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260707T095128`


### 2026-07-02 09:02 — подбор домена/хостинга

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260702T090203/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260702T090203`


### 2026-07-02 08:17 — 3x-ui vpn_panel proxy: Location rewrite + panel paths

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/sites_proxy.py\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260702T081737/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260702T081737`


### 2026-07-01 12:31 — disable pi5-full-when-up and malinki auto on Pi3

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260701T123143/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260701T123143`


### 2026-07-01 10:15 — disable malinki-sync auto timer

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260701T101524/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260701T101524`


### 2026-07-01 10:10 — SSH/Wi-Fi stability + malinki-sync less SSH from Pi3

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/fix-wlan0-pi5.sh\`, \`Проекты/ai_assistant/scripts/install-sshd-keepalive-pi5.sh\`, \`Проекты/ai_assistant/config/systemd/wlan0-watchdog.timer\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260701T101006/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260701T101006`


### 2026-06-29 12:53 — fix bridge offline badge

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260629T125305/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260629T125305`


### 2026-06-29 12:37 — VPN_Server SSH + API + agent prompt

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/vpn_server.py\`, \`Проекты/Cursor Agent/api/voice_fast.py\`, \`Проекты/Cursor Agent/api/cursor_chat.py\`, \`Проекты/Cursor Agent/api/status_api.py\`, \`Проекты/Cursor Agent/api/mvp_app.py\`, \`Проекты/Cursor Agent/config/nodes.json\`, \`.cursor/VPN_SERVER.md\`, \`vpn-guide.md\`
- **Снимок:** `.cursor/backups/20260629T123748/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260629T123748`


### 2026-06-29 12:22 — STT: base, beam3, VAD, ffmpeg, prompt

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/stt_api.py\`, \`Проекты/Cursor Agent/api/stt_preprocess.py\`, \`Проекты/Cursor Agent/scripts/cursor-agent-mvp.service\`, \`Проекты/Cursor Agent/pwa/voice-mode.js\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260629T122208/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260629T122208`


### 2026-06-29 11:57 — убрать clear chat, VAD 480, TTS +20%

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/style.css\`, \`Проекты/Cursor Agent/pwa/voice-mode.js\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/scripts/edge_tts_worker.py\`, \`Проекты/Cursor Agent/scripts/edge_tts_speak.py\`, \`Проекты/Cursor Agent/api/tts_api.py\`, \`Проекты/Cursor Agent/scripts/cursor-agent-mvp.service\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260629T115703/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260629T115703`


### 2026-06-29 11:46 — voice fast-path pi/greeting, TTS warm

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/voice_fast.py\`, \`Проекты/Cursor Agent/api/ws_chat.py\`, \`Проекты/Cursor Agent/api/siri_api.py\`, \`Проекты/Cursor Agent/api/tts_api.py\`, \`Проекты/Cursor Agent/api/mvp_app.py\`, \`Проекты/Cursor Agent/api/voice_api.py\`, \`Проекты/Cursor Agent/pwa/voice-mode.js\`, \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260629T114616/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260629T114616`


### 2026-06-29 11:38 — голос: voice_mode, ранний TTS, edge_tts worker

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/cursor_chat.py\`, \`Проекты/Cursor Agent/api/chat_recovery.py\`, \`Проекты/Cursor Agent/api/ws_chat.py\`, \`Проекты/Cursor Agent/api/tts_api.py\`, \`Проекты/Cursor Agent/scripts/edge_tts_worker.py\`, \`Проекты/Cursor Agent/pwa/voice-mode.js\`, \`Проекты/Cursor Agent/pwa/app.js\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260629T113832/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260629T113832`


### 2026-06-29 10:30 — rename NexusControl to CursorAgent

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/ios/CursorAgent\`, \`Проекты/Cursor Agent/api/cursor_chat.py\`, \`Проекты/Cursor Agent/api/siri_api.py\`, \`Проекты/Cursor Agent/config/settings.py\`, \`Проекты/Cursor Agent/README.md\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260629T103044/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260629T103044`


### 2026-06-29 08:39 — HA sites: /config shim

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/sites_proxy.py\`, \`Проекты/Cursor Agent/pwa/sw.js\`, \`Проекты/Cursor Agent/pwa/index.html\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260629T083950/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260629T083950`


### 2026-06-26 15:55 — TLS local CA + Windows trust

- **Агент:** cursor
- **Проект:** web_config_bms
- **Файлы:** \`Проекты/web_config_bms/serve-https.py\`, \`Проекты/web_config_bms/install-pi.sh\`, \`Проекты/web_config_bms/README.md\`, \`Проекты/web_config_bms/CHANGELOG.md\`, \`Проекты/web_config_bms/scripts/generate-tls-certs.sh\`, \`Проекты/web_config_bms/scripts/install-trust-ca-windows.ps1\`
- **Снимок:** `.cursor/backups/20260626T155556/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T155556`


### 2026-06-26 15:34 — voice plain b64 underscore for shortcuts spaces

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/voice_api.py\`, \`Проекты/Cursor Agent/api/health.py\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260626T153438/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T153438`


### 2026-06-26 14:11 — voice pi_fast fallback bridge relaunch resume fix

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/voice_api.py\`, \`Проекты/Cursor Agent/llm/cursor_client.py\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260626T141114/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T141114`


### 2026-06-26 12:19 — siri/voice logs via settings; remove Nexus AI artifact

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/api/siri_log.py\`, \`Проекты/Cursor Agent/api/voice_log.py\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260626T121913/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T121913`


### 2026-06-26 12:05 — venv после переименования + start-mvp venv_ok

- **Агент:** cursor
- **Проект:** Cursor Agent
- **Файлы:** \`Проекты/Cursor Agent/scripts/start-mvp.sh\`, \`Проекты/Cursor Agent/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260626T120548/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T120548`


### 2026-06-26 11:42 — Cursor Agent: ws/chat, voice, chat MVP

- **Агент:** cursor
- **Проект:** Nexus AI
- **Файлы:** \`Проекты/Nexus AI/api/cursor_chat.py\`, \`Проекты/Nexus AI/api/ws_chat.py\`, \`Проекты/Nexus AI/api/voice_api.py\`, \`Проекты/Nexus AI/api/chat.py\`, \`Проекты/Nexus AI/api/health.py\`, \`Проекты/Nexus AI/pwa/app.js\`, \`Проекты/Nexus AI/pwa/sw.js\`, \`Проекты/Nexus AI/MVP.md\`, \`Проекты/Nexus AI/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260626T114202/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T114202`


### 2026-06-26 10:18 — Pi5 full-stack architecture

- **Агент:** cursor
- **Проект:** Nexus AI
- **Файлы:** \`Проекты/Nexus AI/tools/registry.py\`, \`Проекты/Nexus AI/tools/filesystem_tool.py\`, \`Проекты/Nexus AI/tools/run_tool.py\`, \`Проекты/Nexus AI/agent\`, \`Проекты/Nexus AI/api/mvp_app.py\`, \`Проекты/Nexus AI/api/voice_api.py\`, \`Проекты/Nexus AI/api/agent_api.py\`, \`Проекты/Nexus AI/api/health.py\`, \`Проекты/Nexus AI/config/nodes.json\`, \`Проекты/Nexus AI/MVP.md\`
- **Снимок:** `.cursor/backups/20260626T101815/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T101815`


### 2026-06-26 09:57 — Agent Loop: planner, executor, state machine, ws_chat

- **Агент:** cursor
- **Проект:** Nexus AI
- **Файлы:** \`Проекты/Nexus AI/agent\`, \`Проекты/Nexus AI/api/ws_chat.py\`, \`Проекты/Nexus AI/api/mvp_app.py\`, \`Проекты/Nexus AI/api/health.py\`, \`Проекты/Nexus AI/scripts/smoke-agent-loop.sh\`, \`Проекты/Nexus AI/CHANGELOG.md\`, \`Проекты/Nexus AI/MVP.md\`
- **Снимок:** `.cursor/backups/20260626T095727/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T095727`


### 2026-06-26 08:44 — Safe Execution Layer task 5

- **Агент:** cursor
- **Проект:** Nexus AI
- **Файлы:** \`Проекты/Nexus AI/execution\`, \`Проекты/Nexus AI/tools/safe_shell_tool.py\`, \`Проекты/Nexus AI/tools/docker_tool.py\`, \`Проекты/Nexus AI/tools/process_tool.py\`, \`Проекты/Nexus AI/tools/registry.py\`, \`Проекты/Nexus AI/tools/schemas.py\`, \`Проекты/Nexus AI/README.md\`, \`Проекты/Nexus AI/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260626T084432/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T084432`


### 2026-06-26 08:42 — ProjectContextEngine task 4

- **Агент:** cursor
- **Проект:** Nexus AI
- **Файлы:** \`Проекты/Nexus AI/context\`, \`Проекты/Nexus AI/llm/tool_orchestrator.py\`, \`Проекты/Nexus AI/api/chat.py\`, \`Проекты/Nexus AI/api/app.py\`, \`Проекты/Nexus AI/api/health.py\`, \`Проекты/Nexus AI/README.md\`, \`Проекты/Nexus AI/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260626T084229/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T084229`


### 2026-06-26 08:40 — Tool System task 3

- **Агент:** cursor
- **Проект:** Nexus AI
- **Файлы:** \`Проекты/Nexus AI/tools\`, \`Проекты/Nexus AI/llm/tool_orchestrator.py\`, \`Проекты/Nexus AI/api/chat.py\`, \`Проекты/Nexus AI/api/app.py\`, \`Проекты/Nexus AI/config/settings.py\`, \`Проекты/Nexus AI/README.md\`, \`Проекты/Nexus AI/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260626T084013/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T084013`


### 2026-06-26 08:37 — Cursor Agent LLM /chat

- **Агент:** cursor
- **Проект:** Nexus AI
- **Файлы:** \`Проекты/Nexus AI/llm\`, \`Проекты/Nexus AI/api/chat.py\`, \`Проекты/Nexus AI/api/app.py\`, \`Проекты/Nexus AI/config/settings.py\`, \`Проекты/Nexus AI/models/messages.py\`, \`Проекты/Nexus AI/README.md\`, \`Проекты/Nexus AI/CHANGELOG.md\`, \`Проекты/Nexus AI/requirements.txt\`, \`Проекты/Nexus AI/.env.example\`
- **Снимок:** `.cursor/backups/20260626T083721/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T083721`


### 2026-06-26 08:26 — MVP ядро FastAPI WebSocket

- **Агент:** cursor
- **Проект:** Nexus AI
- **Файлы:** \`Проекты/Nexus AI\`
- **Снимок:** `.cursor/backups/20260626T082652/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260626T082652`


### 2026-06-24 16:31 — Bybit: отключить авто Telegram push

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`.cursor/scripts/bybit-auto-trader.py\`, \`.cursor/scripts/install-bybit-auto-trader-timer.sh\`, \`.cursor/scripts/install-bybit-watch-timer.sh\`, \`.cursor/data/bybit-auto-confirm.json\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260624T163148/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260624T163148`


### 2026-06-24 16:13 — Крымгазсеть: Долг/Переплата

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260624T161351/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260624T161351`


### 2026-06-24 16:07 — Крымэнерго: sequential refresh, SPA wait, UI merge

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260624T160708/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260624T160708`


### 2026-06-24 15:40 — Крымгазсеть: парсинг Задолженность, merge метрик

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260624T154032/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260624T154032`


### 2026-06-23 18:30 — Bybit hourly Telegram push

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/scripts/bybit-watch.py\`, \`.cursor/scripts/install-bybit-watch-timer.sh\`
- **Снимок:** `.cursor/backups/20260623T183048/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260623T183048`


### 2026-06-23 12:55 — Claude Code удалён

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/telegram_relay.py\`, \`Проекты/ai_assistant/bot_ui.py\`, \`Проекты/ai_assistant/attachment_utils.py\`, \`Проекты/ai_assistant/cursor_agent_client.py\`, \`Проекты/ai_assistant/tmux_sync.py\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`Проекты/ai_assistant/AGENTS.md\`, \`Проекты/ai_assistant/.env.example\`
- **Снимок:** `.cursor/backups/20260623T125542/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260623T125542`


### 2026-06-23 12:21 — tailscaled+openclaw removal

- **Агент:** cursor
- **Проект:** cleanup
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/README.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`, \`Проекты/ai_assistant/README.md\`, \`Проекты/ai_assistant/AGENTS.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260623T122133/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260623T122133`


### 2026-06-23 11:52 — st-flash: удалены логи 38G, без .build логов, timeout

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/Eltavr_firmware/A11034R6/scripts/flash-stlink.sh\`, \`Проекты/Arduino/firmware/Eltavr_firmware/A11034R6/scripts/flash-openocd.sh\`, \`Проекты/Arduino/firmware/Eltavr_firmware/a20014_plata_monitora/scripts/flash-stlink-common.sh\`, \`Проекты/Arduino/firmware/Ruchnik_na_STM32F103C6/scripts/flash-stlink.sh\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260623T115220/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260623T115220`


### 2026-06-22 14:01 — File Browser Time Capsule :8092 + пароли на дашборде

- **Агент:** cursor
- **Проект:** Raspberry_Pi_3_HomePortable
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/docker-compose.yml\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/install-timecapsule-filebrowser.sh\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/patch_timecapsule_filebrowser_dashboard.py\`, \`Проекты/Raspberry_Pi_3_HomePortable/ha_config/dashboards/timecapsule.yaml\`, \`Проекты/Raspberry_Pi_3_HomePortable/ha_config/dashboards/timecapsule.template.yaml\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260622T140127/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260622T140127`


### 2026-06-22 13:31 — tc tc-hdd ssh mesh aliases

- **Агент:** cursor
- **Проект:** Raspberry_Pi_3_HomePortable
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/scripts/timecapsule-ssh-keys-sync.sh\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/install-timecapsule-ssh-access.sh\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/tc-hdd\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/README.md\`
- **Снимок:** `.cursor/backups/20260622T133135/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260622T133135`


### 2026-06-22 12:59 — TimeCapsuleSMB deploy + smb.conf.example

- **Агент:** cursor
- **Проект:** Raspberry_Pi_3_HomePortable
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/README.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/config/timecapsule/smb.conf.example\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260622T125905/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260622T125905`


### 2026-06-21 19:43 — Bybit notify positive only

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`.cursor/scripts/bybit-auto-trader.py\`, \`.cursor/data/bybit-auto-confirm.json\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260621T194323/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260621T194323`


### 2026-06-21 19:40 — ETH в оборот, parallel trades, SOL TP fix

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`.cursor/scripts/bybit-auto-trader.py\`, \`.cursor/data/bybit-auto-confirm.json\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260621T194052/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260621T194052`


### 2026-06-21 19:36 — Bybit: все USDT на авто-сделки

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`.cursor/data/bybit-auto-confirm.json\`, \`.cursor/scripts/bybit-auto-trader.py\`
- **Снимок:** `.cursor/backups/20260621T193614/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260621T193614`


### 2026-06-21 19:23 — bybit spot auto 10 USDT ADA

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`.cursor/scripts/bybit-spot-order.py\`
- **Снимок:** `.cursor/backups/20260621T192322/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260621T192322`


### 2026-06-19 16:54 — Kali boot fix BT autoconnect

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/fix-kali-boot-network.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260619T165429/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260619T165429`


### 2026-06-19 16:50 — Pi3 boot fix wlan1-watchdog amneziawg

- **Агент:** cursor
- **Проект:** Raspberry_Pi_3_HomePortable
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/scripts/fix-wlan1.sh\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/wlan1-watchdog.service\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260619T165035/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260619T165035`


### 2026-06-19 16:28 — Remove ZeroTier everywhere

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/scripts/purge-zerotier.sh\`, \`.cursor/scripts/purge-legacy-mesh-remote-pi3.sh\`, \`.cursor/scripts/restore-pi5-ufw.sh\`
- **Снимок:** `.cursor/backups/20260619T162819/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260619T162819`


### 2026-06-19 16:24 — UFW restore script + systemd pi5-restore-ufw

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/scripts/restore-pi5-ufw.sh\`, \`.cursor/scripts/install-pi5-restore-ufw.sh\`, \`.cursor/scripts/pi5-restore-ufw.service\`, \`.cursor/scripts/fix-pi5-ports-ufw-docker.sh\`
- **Снимок:** `.cursor/backups/20260619T162425/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260619T162425`


### 2026-06-18 15:04 — Экор: 5 счетов с датами на кнопках

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260618T150423/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T150423`


### 2026-06-18 14:23 — Экор: выписка и скачивание счёта

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260618T142329/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T142329`


### 2026-06-18 14:14 — Жилсервис: fetch-логин вместо Playwright

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260618T141427/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T141427`


### 2026-06-18 14:07 — Дата последнего платежа + resolveServiceUrl + energy pays nav

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260618T140734/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T140734`


### 2026-06-18 13:47 — voda meter reading from vodomer tab

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260618T134751/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T134751`


### 2026-06-18 09:26 — always 5 receipt slots all cards

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/styles.css\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260618T092650/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T092650`


### 2026-06-18 09:12 — energy only receipt buttons v4 storage

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260618T091249/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T091249`


### 2026-06-18 09:04 — fix energy Cheki template key

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260618T090404/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T090404`


### 2026-06-18 09:01 — energy receipts check.ofd.ru

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/server.js\`, \`Проекты/komunalka/app.js\`, \`Проекты/komunalka/index.html\`, \`Проекты/komunalka/CHANGELOG.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260618T090125/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T090125`


### 2026-06-18 08:49 — fix playwright chromium for api refresh

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`Проекты/komunalka/package.json\`, \`Проекты/komunalka/CHANGELOG.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260618T084941/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T084941`


### 2026-06-18 08:45 — switch active project to komunalka

- **Агент:** cursor
- **Проект:** komunalka
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260618T084528/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260618T084528`


### 2026-06-17 13:08 — Создан базовый каркас проекта EDM

- **Агент:** cursor
- **Проект:** EDM
- **Файлы:** \`Проекты/EDM\`, \`Проекты/README.md\`
- **Снимок:** `.cursor/backups/20260617T130829/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260617T130829`


### 2026-06-11 13:16 — Time Capsule rw+dashboard+secrets

- **Агент:** cursor
- **Проект:** Raspberry_Pi_3_HomePortable
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/docker-compose.yml\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/README.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/ha_config/dashboards/timecapsule.yaml\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/sync-timecapsule-auth.sh\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/migrate-timecapsule-secrets.sh\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/patch_timecapsule_ha_dashboard.py\`, \`Проекты/Raspberry_Pi_3_HomePortable/config/timecapsule/secrets.env.example\`
- **Снимок:** `.cursor/backups/20260611T131607/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260611T131607`


### 2026-06-10 08:35 — zakupki source URLs for clients

- **Агент:** cursor
- **Проект:** www
- **Файлы:** \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260610T083544/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260610T083544`


### 2026-06-08 14:44 — удалён ESPHAPCamera_MY

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/README.md\`, \`Проекты/Arduino/firmware/scripts/cleanup-vendor-libs.sh\`, \`Проекты/Arduino/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260608T144457/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260608T144457`


### 2026-06-08 14:39 — HA update 2024.3.3→2026.6.1 + docker-compose

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/docker-compose.yml\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260608T143903/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260608T143903`


### 2026-06-08 14:27 — удалён EspHapAdvancedDimmableLed_MY

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/README.md\`, \`Проекты/Arduino/firmware/scripts/cleanup-vendor-libs.sh\`, \`Проекты/Arduino/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260608T142708/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260608T142708`


### 2026-06-08 10:14 — ESP HomeKit: каркас dimmable+camera, удалён EspHapAdvancedLed_MY_LED

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/EspHapAdvancedDimmableLed_MY\`, \`Проекты/Arduino/firmware/ESPHAPCamera_MY\`, \`Проекты/Arduino/firmware/scripts/fetch-esphap-libs.sh\`, \`Проекты/Arduino/firmware/scripts/cleanup-vendor-libs.sh\`, \`Проекты/Arduino/firmware/README.md\`, \`Проекты/Arduino/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260608T101444/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260608T101444`


### 2026-06-06 13:39 — fix-claude-pi3 script + README 3 RO

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/fix-claude-pi3.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/scripts/deploy-switch-to-pi3.sh\`, \`Проекты/Raspberry_Pi_3_HomePortable/README.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260606T133905/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260606T133905`


### 2026-06-06 04:02 — Pi3 garage: 3 relay outputs (RO) connected

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`, \`Проекты/Raspberry_Pi_3_HomePortable/README.md\`
- **Снимок:** `.cursor/backups/20260606T040228/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260606T040228`


### 2026-06-05 17:51 — HomeKit: состояние только по концевикам

- **Агент:** cursor
- **Проект:** Raspberry_Pi_3_HomePortable
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/switch/app/main.py\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260605T175122/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T175122`


### 2026-06-05 17:43 — HomeKit между концевиками stopped

- **Агент:** cursor
- **Проект:** Raspberry_Pi_3_HomePortable
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/switch/app/main.py\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260605T174354/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T174354`


### 2026-06-05 17:40 — логика концевиков ворот OPEN/CLOSED

- **Агент:** cursor
- **Проект:** Raspberry_Pi_3_HomePortable
- **Файлы:** \`Проекты/Raspberry_Pi_3_HomePortable/switch/app/main.py\`, \`Проекты/Raspberry_Pi_3_HomePortable/switch/app/config.py\`, \`Проекты/Raspberry_Pi_3_HomePortable/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260605T174031/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T174031`


### 2026-06-05 17:03 — ELTAVR_ VLESS working, DNS exclude fix documented

- **Агент:** cursor
- **Проект:** keenetic
- **Файлы:** \`keenetic-routers.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260605T170353/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T170353`


### 2026-06-05 16:37 — XKeen VLESS ELTAVR_VPN office router

- **Агент:** cursor
- **Проект:** keenetic
- **Файлы:** \`keenetic-routers.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260605T163719/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T163719`


### 2026-06-05 16:02 — keenetic-ssh.sh + SSH config aliases

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/scripts/keenetic-ssh.sh\`, \`keenetic-routers.md\`
- **Снимок:** `.cursor/backups/20260605T160212/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T160212`


### 2026-06-05 15:59 — SSH включён на обоих Keenetic

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`keenetic-routers.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260605T155949/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T155949`


### 2026-06-05 15:53 — Офис ELTAVR → сайт ЭЛЬТАВР: маршруты, DNAT, UFW

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`keenetic-routers.md\`, \`.cursor/scripts/docker-ufw-docker-user-apply.sh\`, \`.cursor/scripts/fix-pi5-ports-ufw-docker.sh\`
- **Снимок:** `.cursor/backups/20260605T155311/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T155311`


### 2026-06-05 14:43 — Keenetic routers reference + RCI script

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`keenetic-routers.md\`, \`.cursor/scripts/keenetic-rci.py\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260605T144350/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T144350`


### 2026-06-05 11:07 — MAR3501 resistive touch driver + demo

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/EmKit_A2001_R2/include/touch_config.h\`, \`Проекты/Arduino/firmware/EmKit_A2001_R2/include/resistive_touch.h\`, \`Проекты/Arduino/firmware/EmKit_A2001_R2/src/resistive_touch.cpp\`, \`Проекты/Arduino/firmware/EmKit_A2001_R2/src/main.cpp\`, \`Проекты/Arduino/firmware/EmKit_A2001_R2/src/ili9486_8080.cpp\`, \`Проекты/Arduino/firmware/EmKit_A2001_R2/include/ili9486_8080.h\`, \`Проекты/Arduino/firmware/EmKit_A2001_R2/PINOUT.md\`, \`Проекты/Arduino/firmware/EmKit_A2001_R2/README.md\`
- **Снимок:** `.cursor/backups/20260605T110729/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T110729`


### 2026-06-05 08:49 — EmKit_A2001_R2 TFT firmware scaffold

- **Агент:** cursor
- **Проект:** Arduino
- **Файлы:** \`Проекты/Arduino/firmware/EmKit_A2001_R2\`, \`Проекты/Arduino/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260605T084918/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260605T084918`


### 2026-06-03 12:25 — Kali xray VLESS native von voff

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/xray-kali/config.json\`, \`Проекты/ai_assistant/config/kali-zshrc.vpn.snippet\`, \`Проекты/ai_assistant/scripts/kali-vpn-toggle.sh\`, \`Проекты/ai_assistant/scripts/install-xray-kali.sh\`, \`Проекты/ai_assistant/scripts/remove-wg-exit-kali.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260603T122558/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260603T122558`


### 2026-06-03 12:14 — Pi3 remove wg-exit, xray-only VPN

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/remove-wg-exit-pi3.sh\`, \`Проекты/ai_assistant/scripts/pi3-vpn-toggle.sh\`, \`Проекты/ai_assistant/config/pi3-bash_aliases.vpn.snippet\`, \`Проекты/ai_assistant/scripts/remove-amnezia-pi3.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260603T121424/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260603T121424`


### 2026-06-03 12:05 — Pi3 xray VLESS Reality pi3 client

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/xray-pi3/config.json\`, \`Проекты/ai_assistant/scripts/pi3-vpn-toggle.sh\`, \`Проекты/ai_assistant/scripts/install-xray-pi3.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260603T120518/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260603T120518`


### 2026-06-03 12:02 — Pi3 remove Amnezia, VPS wg scripts

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/remove-amnezia-pi3.sh\`, \`Проекты/ai_assistant/scripts/pi3-setup-exit-vpn.sh\`, \`Проекты/ai_assistant/scripts/pi3-netbird-vpn-preserve.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260603T120241/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260603T120241`


### 2026-06-02 17:15 — disabled vpn autostart on reboot and enforced single-vpn toggle

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-vpn-toggle.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T171530/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T171530`


### 2026-06-02 17:12 — oled blank recovery noted in context files

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T171232/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T171232`


### 2026-06-02 17:11 — oled vpn icon switched to xray-pi5 detection with wg fallback

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T171114/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T171114`


### 2026-06-02 17:06 — fixed remote VPN toggle false fail by adding proxy readiness retries

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-vpn-toggle.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T170620/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T170620`


### 2026-06-02 17:03 — vpn toggle switched from wg-exit to xray-pi5 for panel visibility

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-vpn-toggle.sh\`, \`Проекты/ai_assistant/scripts/argon-ir-stb-remote-listener.py\`, \`Проекты/ai_assistant/config/argonpowerbutton.py\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T170337/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T170337`


### 2026-06-02 16:52 — pi5 switched to panel key via docker xray socks proxy

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T165204/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T165204`


### 2026-06-02 16:39 — обновил vpn-guide под клиентов по устройствам и текущую безопасность

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`vpn-guide.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T163930/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T163930`


### 2026-06-02 15:42 — stb remote mute toggles vpn

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-ir-stb-remote-listener.py\`, \`Проекты/ai_assistant/scripts/install-argon-ir-stb-remote.sh\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T154253/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T154253`


### 2026-06-02 15:23 — argon button vpn toggle and oled wg indicator

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/argonpowerbutton.py\`, \`Проекты/ai_assistant/scripts/argon-vpn-toggle.sh\`, \`Проекты/ai_assistant/scripts/install-argon-powerbutton.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T152332/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T152332`


### 2026-06-02 15:17 — pi5 switched from amnezia to vps wireguard wg-exit

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T151731/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T151731`


### 2026-06-02 14:36 — wireguard subnet changed to 10.90.90.0/24 on vps and keenetic docs

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`keenetic-wg.conf\`, \`vpn-guide.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T143623/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T143623`


### 2026-06-02 10:03 — настроил ssh ключ на новом vps 89.127.199.6

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T100348/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T100348`


### 2026-06-02 09:33 — удалил claude code на vps и обновил контекст

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260602T093307/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260602T093307`


### 2026-05-29 13:00 — pi5 ha cpu temperature sensors

- **Агент:** cursor
- **Проект:** Apple HomeKit accessory
- **Файлы:** \`Проекты/Apple HomeKit accessory/home_assistant/config/configuration.yaml\`, \`Проекты/Apple HomeKit accessory/home_assistant/scripts/publish_pi5_host_status.sh\`, \`Проекты/Apple HomeKit accessory/home_assistant/scripts/install-pi5-ha-host-status.sh\`, \`Проекты/Apple HomeKit accessory/home_assistant/CHANGELOG.md\`, \`Проекты/Apple HomeKit accessory/home_assistant/config/.storage/lovelace\`
- **Снимок:** `.cursor/backups/20260529T130057/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260529T130057`


### 2026-05-29 08:50 — pi5 wlan0 watchdog for stable wifi

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/fix-wlan0-pi5.sh\`, \`Проекты/ai_assistant/scripts/install-wlan0-watchdog-pi5.sh\`, \`Проекты/ai_assistant/config/systemd/wlan0-watchdog.service\`, \`Проекты/ai_assistant/config/systemd/wlan0-watchdog.timer\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260529T085052/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260529T085052`


### 2026-05-29 08:48 — pi5 wifi bssid fix context

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260529T084819/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260529T084819`


### 2026-05-28 16:11 — disable kali auto root login

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T161117/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T161117`


### 2026-05-28 16:01 — fix kali root claude wrapper path

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T160131/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T160131`


### 2026-05-28 15:49 — kali ssh keys check and auto root zsh

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T154910/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T154910`


### 2026-05-28 14:28 — sync opencode credentials pi5 to kali

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T142817/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T142817`


### 2026-05-28 12:49 — bt pan watchdog self-heal enabled

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T124917/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T124917`


### 2026-05-28 12:47 — bt pan switched to static bnep0 ip

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T124747/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T124747`


### 2026-05-28 12:45 — bluetooth pan autoconnect configured on kali

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T124551/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T124551`


### 2026-05-28 12:12 — offline kali card fix wifi autoconnect and usb0 static

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T121211/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T121211`


### 2026-05-28 11:29 — kali zero2w gadget mode success context update

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T112953/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T112953`


### 2026-05-28 11:24 — kali otg gadget test and rollback context

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260528T112418/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260528T112418`


### 2026-05-27 18:15 — update pi5 opencode server to 1.15.11 and verify 4096

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T181553/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T181553`


### 2026-05-27 18:11 — install opencode on kali pi2 via nvm and symlink to /usr/local/bin

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T181110/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T181110`


### 2026-05-27 17:43 — подтвержден LAN/SSH IP kali pi2 10.1.30.97

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T174326/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T174326`


### 2026-05-27 17:03 — kali netbird setup-key connected and ssh keepalive tools

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T170319/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T170319`


### 2026-05-27 16:56 — install netbird on kali pi2 needslogin

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T165632/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T165632`


### 2026-05-27 16:49 — diagnose kali pi2 rpi-connect absence

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T164928/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T164928`


### 2026-05-27 16:48 — sync ssh keys among pi5 pi3 pi2 and note network blockers

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T164808/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T164808`


### 2026-05-27 16:44 — add kali rpi2 ssh keys context update

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T164458/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T164458`


### 2026-05-27 16:23 — add rpi-connect watchdog timer and installer

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/rpi-connect-watchdog.sh\`, \`Проекты/ai_assistant/scripts/install-rpi-connect-watchdog.sh\`, \`Проекты/ai_assistant/config/systemd/rpi-connect-watchdog.service\`, \`Проекты/ai_assistant/config/systemd/rpi-connect-watchdog.timer\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T162308/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T162308`


### 2026-05-27 16:19 — rpi-connect dns diagnostic context update

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T161944/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T161944`


### 2026-05-27 16:02 — increase OLED flash/result line spacing

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/oled_firmware_draw.py\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T160221/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T160221`


### 2026-05-27 15:26 — fix A11039R5 probe signature and flash OK grep

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-eltavr-probe-target.sh\`, \`Проекты/ai_assistant/scripts/argon-eltavr-flash-item.sh\`, \`Проекты/Arduino/firmware/Eltavr_firmware/A11039R5_7cel_V10/scripts/isp-prog-args.sh\`, \`Проекты/Arduino/firmware/Eltavr_firmware/A11039R5_7cel_V10/scripts/config.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T152657/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T152657`


### 2026-05-27 15:22 — rename A11039 to A11039R5 in menu paths and firmware dir

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/eltavr_oled_firmware.json\`, \`Проекты/ai_assistant/scripts/argon-eltavr-flash-item.sh\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`Проекты/Arduino/firmware/Eltavr_firmware/A11039R5_7cel_V10\`, \`Проекты/Arduino/firmware/Eltavr_firmware/README.md\`, \`Проекты/Arduino/firmware/Eltavr_firmware/CONNECTIVITY.md\`, \`Проекты/Arduino/firmware/Eltavr_firmware/HARDWARE_IMAGES.md\`, \`Проекты/Arduino/firmware/Eltavr_firmware/GERBER_INDEX.md\`, \`Проекты/Arduino/firmware/Eltavr_firmware/scripts/organize-gerber-outputs.sh\`, \`Проекты/Arduino/firmware/Eltavr_firmware/scripts/render-gerber-png.py\`, \`Проекты/Arduino/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T152215/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T152215`


### 2026-05-27 15:09 — a11039 probe false error fixed and context updated

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-eltavr-probe-target.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`, \`.cursor/chat.md\`, \`.cursor/CHAT_HANDOFF.md\`
- **Снимок:** `.cursor/backups/20260527T150958/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T150958`


### 2026-05-27 15:09 — fix A11039 false probe fail

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-eltavr-probe-target.sh\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T150905/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T150905`


### 2026-05-27 14:01 — increase OLED firmware menu font

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/oled_firmware_draw.py\`
- **Снимок:** `.cursor/backups/20260527T140140/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T140140`


### 2026-05-27 14:00 — OLED firmware menu one-line

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/oled_firmware_draw.py\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T140050/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T140050`


### 2026-05-27 13:53 — BACK one-step in OLED menu

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/ir_oled_menu.py\`, \`Проекты/ai_assistant/scripts/argon-ir-stb-remote-listener.py\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T135308/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T135308`


### 2026-05-27 13:50 — fix IR service cycle + Argon poweroff

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/systemd/argon-ir-stb-ok.service\`, \`Проекты/ai_assistant/scripts/argon-poweroff.sh\`, \`Проекты/ai_assistant/scripts/argon-ir-stb-remote-listener.py\`, \`Проекты/ai_assistant/scripts/install-argon-ir-stb-remote.sh\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T135018/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T135018`


### 2026-05-27 13:43 — IR POWER -> systemctl poweroff

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/scripts/argon-ir-stb-remote-listener.py\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T134313/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T134313`


### 2026-05-27 13:02 — Fix OLED firmware menu and flash launcher for 5 Eltavr items

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/eltavr_oled_firmware.json\`, \`Проекты/ai_assistant/ir_oled_menu.py\`, \`Проекты/ai_assistant/oled_firmware_draw.py\`, \`Проекты/ai_assistant/scripts/argon-ir-stb-remote-listener.py\`, \`Проекты/ai_assistant/scripts/argon-eltavr-flash-item.sh\`, \`Проекты/ai_assistant/scripts/install-argon-ir-stb-remote.sh\`, \`Проекты/ai_assistant/scripts/argon-a20014-flash-v7.sh\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T130245/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T130245`


### 2026-05-27 12:33 — OLED Eltavr menu IR MENU HOME OK

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/ir_oled_menu.py\`, \`Проекты/ai_assistant/ir_remote_codes.py\`, \`Проекты/ai_assistant/oled_firmware_draw.py\`, \`Проекты/ai_assistant/config/eltavr_oled_firmware.json\`, \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/scripts/argon-ir-stb-remote-listener.py\`, \`Проекты/ai_assistant/scripts/argon-a20014-flash-image.sh\`, \`Проекты/ai_assistant/scripts/install-argon-ir-stb-remote.sh\`, \`Проекты/ai_assistant/config/systemd/argon-ir-stb-ok.service\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T123340/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T123340`


### 2026-05-27 12:25 — IR MOUSE 0xb8474040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T122543/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T122543`


### 2026-05-27 12:24 — IR VOL_DOWN 0xe8174040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T122436/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T122436`


### 2026-05-27 12:23 — IR VOL_UP 0xe7184040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T122345/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T122345`


### 2026-05-27 12:22 — IR BACK 0xbd424040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T122228/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T122228`


### 2026-05-27 12:21 — IR MENU 0xba454040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T122115/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T122115`


### 2026-05-27 12:20 — IR HOME 0xe51a4040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T122019/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T122019`


### 2026-05-27 12:19 — IR RIGHT 0xee114040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T121922/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T121922`


### 2026-05-27 12:18 — IR LEFT 0xef104040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T121829/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T121829`


### 2026-05-27 12:17 — IR DOWN 0xf10e4040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T121730/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T121730`


### 2026-05-27 12:16 — IR UP stb_remote 0xf40b4040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T121635/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T121635`


### 2026-05-27 12:14 — IR MUTE stb_remote 0xbc434040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T121432/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T121432`


### 2026-05-27 12:12 — IR POWER stb_remote 0xb24d4040

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/ir/stb_remote.json\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T121253/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T121253`


### 2026-05-27 12:08 — pult detached; argon body only double voice toggle

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`Проекты/ai_assistant/config/argonpowerbutton.py\`, \`Проекты/ai_assistant/scripts/argon-ir-stb-ok-listener.py\`, \`Проекты/ai_assistant/docs/ARGON_IR.md\`, \`Проекты/ai_assistant/CHANGELOG.md\`
- **Снимок:** `.cursor/backups/20260527T120801/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T120801`


### 2026-05-27 11:49 — add strict self-check preference before ready replies

- **Агент:** cursor
- **Проект:** ai_assistant
- **Файлы:** \`.cursor/chat.md\`
- **Снимок:** `.cursor/backups/20260527T114940/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260527T114940`


### 2026-05-25 18:30 — журнал AGENT_CHANGES и скрипты отката

- **Агент:** cursor
- **Проект:** workspace
- **Файлы:** \`.cursor/rules/chat-context-continuity.mdc\`, \`.cursor/rules/core-standards-and-workflow.mdc\`
- **Снимок:** `.cursor/backups/20260525T183031/`
- **Откат:** `bash Документы/.cursor/scripts/agent-change-revert.sh 20260525T183031`


### 2026-05-25 — журнал и откат для всех агентов

- **Агент:** cursor (по запросу пользователя в Telegram)
- **Проект:** workspace `.cursor/`
- **Файлы:** `AGENT_CHANGES.md`, `rules/chat-context-continuity.mdc`, `rules/core-standards-and-workflow.mdc`, `scripts/agent-change-backup.sh`, `scripts/agent-change-revert.sh`, `CHANGELOG.md`, `skills/workspace-pi5/SKILL.md`, `RULES_MASTER_PLAN.md`, `AGENTS.md`
- **Снимок:** —
- **Откат:** удалить перечисленные файлы правил/скриптов вручную или из git в подпроектах

### До журнала (источники)

- Сводка сессий: `.cursor/chat.md` (раздел «Что сделано в этой сессии»)
- Техдетали по проекту: `Проекты/<проект>/CHANGELOG.md`
- Handoff: `.cursor/CHAT_HANDOFF.md`
