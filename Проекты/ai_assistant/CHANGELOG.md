# Журнал изменений — ai_assistant

## 2026-08-04 — Бензин: автомониторинг и пуши отключены

- По запросу: без автопоиска, почты и Telegram-пушей по бензину.
- `data/gdebenz-fuel.json` — `monitoring_disabled: true`, чаты `enabled: false`, `alert_email: ""`.
- Таймеры `gdebenz-fuel.timer` / `gdebenz-qr-monitor.timer` — `disabled`.
- `gdebenz_fuel.py` / `gdebenz_notify.py` — глобальный стоп монитора и пушей; `/gdebenz on` не включает авто.
- `scripts/disable-gdebenz-fuel-monitor.sh`; install-таймер по умолчанию не включает (`GDEBENZ_FUEL_ENABLE_TIMER=0`).
- Заглушки: `~/bin/simferopol-fuel-{monitor,news,report}.sh`, `~/bin/post-eltavr-fuel-news.sh`.

## 2026-07-08 — ГдеБЕНЗ: компактная сводка в Telegram

- `fuel_sources/formatters.py` — 2 строки на АЗС (бренд·адрес + марки/%/карта), короткие заголовки секций, без дублей эмодзи и длинных подсказок.
- `fuel_sources/situation.py` — короткие лейблы («🟢 Есть», «🟡 Очередь»).
- `fuel_sources/qr_crimea.py` — блок QR в одну строку (лимит + число АЗС + карта).

## 2026-07-08 — ГдеБЕНЗ: fast-режим и источники из конфига

- `fuel_hub.py` — `fast=True`: обогащение до 10 АЗС (есть/очередь/лимит); мониторинг — только ok/queue (до 15).
- `telegram_relay.py` — `/gdebenz` в чате с `fast=True`; полная сводка — `/gdebenz проверка`.
- `fuel_sources/registry.py` — `sources` из `data/gdebenz-fuel.json` → gdebenz, gdebenz.su, azs-crimea, atan.
- `fuel_sources/fetchers/azs_crimea.py` — fetcher azs-crimea.ru; `gdebenz.su` в CrowdFetcher.
- `fuel_sources/formatters.py` — в чат выводятся только секции: `есть`, `очередь формируется`, `очередь нарастает`; секции `нет/лимит/без отметки` скрыты.
- Добавлен источник `https://toplivo.tbank.ru/` в `fuel_sources/registry.py` и `FUEL_SOURCES.md`.
- `fuel_sources/fetchers/toplivo_tbank.py` — подключен реальный API `toplivo.tbank.ru/api/v1/stations` (bbox), теперь данные Т-Банка участвуют в расчёте `есть/очередь`.
- Т-Банк теперь трактуется как **сигнал факта продажи топлива, оплаченной картой Т-Банка** (а не подтверждение свободной продажи): в выдаче добавлена пометка `топливо продавалось (оплата картой Т-Банка)`, снижена оценка вероятности.
- `gdebenz_fuel.py` — добавлены режимы `/gdebenz регион крым` и `/gdebenz города г1,г2,...` (общий bbox по нескольким городам).
- `fuel_sources/fetchers/crowd.py` — в региональном и multi-city режиме отключён строгий фильтр по одному городу.
- `fuel_sources/formatters.py` — добавлена метка `межгород` для АЗС вне выбранных городов в multi-city режиме.

- Повышена устойчивость к сетевым сбоям: повторный опрос actionable-источников при полном отказе и явный блок `⚠️ Источники со сбоями` в сводке.

- `fuel_sources/fetchers/crowd.py` — добавлен fallback между зеркалами `gdebenz.ru` ↔ `gdebenz.su` при сетевых/DNS сбоях.
- Т-Банк полностью исключён из сигналов `есть/очередь/нет`: используется только как косвенный факт прошлой продажи (исторический индикатор).
## 2026-07-07 — ГдеБЕНЗ: мониторинг бензина в Telegram

- `gdebenz_client.py`, `gdebenz_fuel.py` — API gdebenz.ru, геокодинг города, сравнение статусов АЗС.
- Команды бота: `/gdebenz` (сводка), `/gdebenz on|off`, `/gdebenz город …`, `/gdebenz топливо 95`, `/gdebenz интервал 10`; синонимы `/бенз`, `/топливо`.
- Пуш в чат при появлении отметок «есть» или «очередь» (краудсорсинг, не официальные данные).
- Таймер: `scripts/install-gdebenz-fuel-timer.sh` → `gdebenz-fuel.timer` (каждые 5 мин).
- Конфиг: `data/gdebenz-fuel.json`, состояние: `data/gdebenz-fuel-state.json`.
- **2026-07-07 (вечер):** расширенная сводка — марки 92/95/98/ДТ/газ, уверенность %, комментарии водителей; по умолчанию Симферополь, `/gdebenz сброс`; статус API `yes`→есть.
- **2026-07-07:** фикс 502 DDoS-Guard — retry, сброс cookies, fallback через `curl -sSL`.
- **2026-07-07:** по умолчанию фильтр **АИ-92 + АИ-95** (`fuel: 92,95`).

## 2026-07-07 — Bybit авто: trailing SL + безубыток

- `bybit-auto-trader.py`: режим trailing — после +3% SL в безубыток, далее SL −3% от пика; фикс. TP +4% отключён.
- `bybit-auto-confirm.json`: `trail_enable`, `breakeven_pct`, `trail_start_pct`, `trail_distance_pct`.

## 2026-07-07 — Bybit авто: фикс TP Insufficient balance

- `bybit-auto-trader.py`: `floor_qty` по `basePrecision` с биржи (округление вниз); старые TP/SL с неверным qty перевыставляются.
- Причина: `round_qty` давал 61.73 при балансе 61.728688 ADA → Bybit отклонял лимит.

## 2026-07-01 — Pi3→Pi5 автоматизация полностью выключена

- `disable-pi3-pi5-watch.sh`: отключает `malinki-sync.timer`, `pi5-full-when-up.timer`, tmux/pkill ожидания Pi5.
- `agents-remember.sh` больше **не** запускает sync автоматически (только `--sync` или `malinki-sync-now`).
- На Pi5 применено локально; на Pi3/Kali — при появлении в сети: `ssh pi@100.102.186.61 'bash ~/cursor_bridge_patch/tmux-agent/disable-pi3-pi5-watch.sh'` (или push через `malinki-sync-now`).

## 2026-07-01 — AGENTS.d: только ручная синхронизация

- `malinki-sync.timer` **disabled** на Pi3, Kali, Pi5.
- `install-malinki-sync.sh` больше не включает таймер при установке.
- Ручной запуск: `malinki-sync-now` или `bash ~/cursor_bridge_patch/tmux-agent/sync-malinki-rules.sh`.

## 2026-07-01 — SSH/Wi‑Fi стабильность Pi 5; меньше SSH с Pi 3

- `scripts/fix-wlan0-pi5.sh`: 3 пинга шлюза, fallback 8.8.8.8, cooldown 120 с — не рвёт Wi‑Fi на ложном сбое.
- `config/systemd/wlan0-watchdog.timer`: проверка раз в **5 мин** (было 2).
- `scripts/install-sshd-keepalive-pi5.sh`: `ClientAliveInterval 60`, `ClientAliveCountMax 3`.
- `cursor_bridge_patch/tmux-agent/sync-malinki-rules.sh`: SSH multiplexing, кэш хостов, один SSH на push.
- `install-malinki-sync.sh`: интервал **30 мин** (было 10); на Pi 3 отключён `pi5-full-when-up.timer`.

## 2026-06-29 — ai-tmux run: фоновые задачи для Cursor

- `ai-tmux run|log|wait` — долгие команды в отдельной tmux-сессии `job-ИМЯ`, лог в `Документы/.cursor/data/tmux-jobs/`.
- Правило Cursor: `.cursor/rules/tmux-resilience.mdc`.
- Исправлен `SELF_DIR` при вызове через symlink `~/bin/ai-tmux`.

## 2026-06-24 — Bybit: без авто-push в Telegram

- Отключены таймеры **`bybit-watch.timer`** и **`bybit-auto-trader.timer`** (stop + disable).
- `bybit-auto-trader.service` — без `--telegram` и `BYBIT_AUTO_TRADER_TELEGRAM`.
- `bybit-auto-confirm.json` — **`notify_telegram: false`**; `bybit-auto-trader.py` уважает флаг.
- Установщики `install-bybit-watch-timer.sh` / `install-bybit-auto-trader-timer.sh` — таймеры по умолчанию **выключены**; push только с `*_ENABLE_TELEGRAM=1`.
- По запросу в боте: **`/bybit`**, `/bybit_full`, `/bybit_ideas`.

## 2026-06-23 — Telegram Cursor: без hint «20–90 с»

- `telegram_relay.py`: убраны промежуточные сообщения «Cursor Agent · … обычно 20–90 с»; остаётся только typing + ответ.

## 2026-06-23 — Bybit авто: TP + SL + soft-stop

- `bybit-log-run.sh`: лог Bybit перезаписывается каждый прогон (~1–3 КБ).
- `bybit-spot-order.py`: `place_stop_market_sell`, `cancel_order`.
- `bybit-auto-confirm.json`: `tp_pct`, `sl_pct`, `drawdown_alert_pct`, `soft_stop`.

## 2026-06-23 — Claude Code снят (Pi 5, Pi 3, Kali)

- Pi 5: npm, `~/.claude`, `claude_client.py` (см. выше).
- Pi 3: удалены `cc-bridge.py`, `~/bin/claude-*`, `voice-claude`; OpenCode `oc-bridge` сохранён.
- Kali: npm uninstall, `~/.claude`, cron `update-claude.sh`, `~/bin/claude*`.
- `install-pi3-bridges.sh` — только `oc-bridge`; `cc-bridge-pi3.py` удалён.

## 2026-06-23 — Claude Code снят с Pi 5

- Удалены npm-пакет `@anthropic-ai/claude-code`, `~/.claude`, `claude_client.py`.
- Telegram-бот: режимы claude/pi3cc → cursor/pi3; `/oc` и `/oc_*` — синонимы Cursor.

## 2026-06-23 — лимиты логов (Pi 5)

- Скрипт `Документы/.cursor/scripts/install-log-limits-pi5.sh`: journald 200M/14d, Docker json-file 10m×3, logrotate для `~/logs/`.
- Правило: `Документы/.cursor/rules/log-limits-pi5.mdc`.

## 2026-06-23 — зачистка legacy workspace

- Удалены старый бэкап workspace, планы/загрузки Cursor; упоминания убраны из README/AGENTS/.env.

## 2026-06-21 — Bybit: уведомления только о плюсе

- `bybit-auto-trader.py` — Telegram только при пополнении, TP, успешном BUY; рутина и ошибки — в лог.
- `bybit-auto-confirm.json` — `notify_positive_only: true`.

## 2026-06-21 — Bybit: ETH в оборот + параллельные позиции

- `bybit-auto-trader.py` — продажа ETH→USDT, `allow_parallel`, фикс округления TP (SOL).
- `bybit-auto-confirm.json` — `use_eth`, `deploy_all`, карт-бланш Telegram.

## 2026-06-21 — Bybit: циклический авто-трейдер

- `Документы/.cursor/scripts/bybit-auto-trader.py` — анализ сигналов `bybit-watch`, market buy до лимита из `bybit-auto-confirm.json`, TP +4%, повтор после продажи.
- `install-bybit-auto-trader-timer.sh` — user-timer каждые 30 мин, лог `~/bybit-auto-trader.log`, уведомления Telegram.

## 2026-06-19 — Kali: чистая загрузка без спама BT PAN

- `scripts/fix-kali-boot-network.sh`: отключить autoconnect профиля NM `AiNETi Network` (BT tether iPhone), `bt-pan-autoconnect`, `nfs-blkmap`.
- На Kali применено: `systemctl --failed` пусто, wlan0 GARAGE + NetBird OK.

## 2026-06-18 — Cursor Agent CLI: Kali (agent / agent-vpn)

- `scripts/install-cursor-agent-kali.sh` — установка CLI, ключ, `~/bin/agent` и `~/bin/agent-vpn` (xray + proxychains), Auto + unrestricted, алиасы в `.zshrc`/`.bashrc`.
- Pi 3: те же алиасы `agent` / `agent-vpn` (см. `~/bin/` на pi3).

## 2026-06-09 — ОТК (akb_otk): токен из sms-sheets.json

- `akb_otk.py`: OAuth берётся из `~/.google-mcp/tokens/sms-sheets.json` (или `GOOGLE_TOKEN_FILE`), а не только из захардкоженного refresh token.

## 2026-06-06 — Claude Code на Pi 3

- `scripts/fix-claude-pi3.sh`: npm global update, chmod `~/.npm-global/bin/claude`, cron `claude update` по воскресеньям.

## 2026-07-29

- **OLED + ИК-пульт:** `~/oled_visual/oled_visual.py` — путь ai_assistant на `/home/pi/Documents` (после миграции при boot `_ir_menu` не грузился → MENU не рисовал меню). `argon-ir-stb-ok.service` — ExecStart на Documents; перезапуск `oled-visual` + `argon-ir-stb-ok`.

## 2026-06-19 — Пульт: A11039 ISP — медленный SCK и retry

- `A11039R5_7cel_V10/scripts/isp-prog-args.sh`: для AVR ISP mkII `-B 125kHz` (RDY/nBSY timeout при записи flash).
- `isp-flash-hex.sh`: до 3 попыток при обрыве USB/ISP.

## 2026-06-05 — Пульт: прошивка A11034R6 (sudo / protected_regular)

- `scripts/argon-eltavr-flash-item.sh`: перед A11034 — `pkill openocd`; успех также по `verified 65536 bytes` / OpenOCD.
- `Eltavr_firmware/A11034R6/scripts/flash-stlink.sh`: образ и лог в `.build/` через `mktemp` (sudo с пульта не мог писать в `/tmp` файл пользователя `pi`).

## 2026-06-04 — Bybit: рекомендации без сделок

- `bybit-recommendations.py` — эмодзи в `/bybit_ideas` (🪙🥇📊 как в `/bybit`).
- `Документы/.cursor/scripts/bybit-recommendations.py` — крипто, металлы (XAUT/XAU/PAXG), X-токены; `--telegram` для бота.
- `prompts/bybit-recommendations.md` — промпт для Cursor + блок DATA.
- Telegram: `/bybit_ideas` (синонимы `/идеи`, `/ideas`).

## 2026-06-04 — Промпт Capitol Trades (только анализ)

- `prompts/capitol-trades-analyze.md` — безопасный промпт для Cursor/Telegram, без ордеров.

## 2026-06-04 — Pi 3: мосты Telegram (oc/cc-bridge)

- На Pi 3 установлен `~/.local/bin/cc-bridge.py`; `oc-bridge.py` — проверка устаревшей сессии в SQLite, чтение ответа из всех сообщений ассистента.
- `telegram_relay.py` — повтор без сессии при `Session not found`; сброшен устаревший `pi3_opencode_session` в `data/settings.json`.
- Скрипт деплоя: `scripts/install-pi3-bridges.sh`.

## 2026-06-04 — Cursor Agent по умолчанию в Telegram

- `DEFAULT_AGENT_MODE = "cursor"` в `telegram_relay.py`; тексты `/start`, `/help`, шпаргалка в `bot_ui.py`.

## 2026-06-04 — Bybit в Telegram

- `/bybit` — баланс UNIFIED + идеи `bybit-watch` (скрипты в `Документы/.cursor/scripts/`).
- `/bybit` — краткая сводка + PNG-график; `/bybit_full` — полный текст; авто-push отключён.
- График: `matplotlib` в venv бота (`requirements-bybit-chart.txt`).

## 2026-06-03 — Kali: VLESS Reality (xray-kali), без wg-exit

- `config/xray-kali/config.json` — клиент `kali` из 3x-ui; нативный бинарник `xray` (arm64 с образа teddysun, без Docker — apt на Kali ломается по IPv6).
- `scripts/kali-vpn-toggle.sh`: fix — xray больше не держит flock (из-за этого `von`/`vst` молча не работали после первого `von`).
- `scripts/install-xray-kali.sh`, `scripts/remove-wg-exit-kali.sh`; алиасы `von`/`voff`/`VON`/`VOFF` в `~/.zshrc`.

## 2026-06-03 — Pi 3: удалён wg-exit (WireGuard exit)

- `scripts/remove-wg-exit-pi3.sh`: с Pi 3 сняты `wg-quick@wg-exit`, `/etc/wireguard/wg-exit.conf`, `~/vpn/vps-wg-exit.conf`, `setup-exit-vpn.sh`, `netbird-vpn-preserve.sh`. VPN только `xray-pi3`.
- `scripts/pi3-vpn-toggle.sh`: убран fallback на wg-exit.

## 2026-06-03 — Pi 3: VLESS Reality (xray-pi3)

- `config/xray-pi3/config.json` — клиент `pi3` из 3x-ui (VLESS Reality → `89.127.199.6:443`), SOCKS `127.0.0.1:10808`.
- `scripts/pi3-vpn-toggle.sh` → `/home/pi/bin/pi3-vpn-toggle.sh`: вкл/выкл контейнер `xray-pi3` (`--restart no`); fallback на `wg-exit`. NetBird не затрагивается. Алиасы `von`/`voff`/`VON`/`VOFF` в `~/.bash_aliases`.
- `scripts/install-xray-pi3.sh` — деплой с Pi 5 на Pi 3.

## 2026-06-03 — Pi 3: удаление Amnezia, VPS WireGuard + NetBird

- `scripts/remove-amnezia-pi3.sh`: полное удаление AmneziaWG с Pi 3 (awg, модуль, `/etc/amnezia`, split-скрипты); NetBird и `~/vpn/vps-wg-exit.conf` сохранены.
- `scripts/pi3-setup-exit-vpn.sh` → `/home/pi/vpn/setup-exit-vpn.sh`: только обычный WireGuard к VPS; PostUp сохраняет маршрут NetBird `100.102.0.0/16` через `wt0`.
- `scripts/pi3-netbird-vpn-preserve.sh` → `/home/pi/bin/netbird-vpn-preserve.sh`: nft-mark для UDP NetBird/WG при полном туннеле (без Amnezia).

## 2026-06-03 — CC1101 анализатор спектра (Pi 3)

- `scripts/cc1101-spectrum.py` + `scripts/install-cc1101-spectrum-pi3.sh`: RSSI-сканер (режимы `scan`, `live`, `waterfall`) на базе `cc1101_capture.py`.
- `scripts/cc1101-listen-air.py` → `/home/pi/cc1101_listen_air.py`: аналог AlexGyver `nrf_listen_air`; пресеты ISM/полос CC1101, `--scan-all`, `--span`; чувствительность в пресете (`433+light`) или `--sensitivity`.
- `scripts/cc1101-send.sh` → `/home/pi/bin/cc1101-send`: алиасы `airsend`, `airsend5`, `airgrab`, `airrelay`.
- Документация: `CC1101_SPECTRUM.md`. На Pi 3: `/home/pi/cc1101_spectrum.py`, `/home/pi/cc1101_listen_air.py`.

## 2026-06-02 — VPN toggle переведён на ключ 3x-ui (`xray-pi5`)

- `scripts/argon-vpn-toggle.sh`: переключение с пульта/кнопки теперь в первую очередь управляет контейнером `xray-pi5` (клиент `pi5` из панели 3x-ui), а `wg-quick@wg-exit` оставлен как fallback при отсутствии конфига `~/vpn/xray-pi5/config.json`.
- При включении добавлен быстрый proxy-тест через `127.0.0.1:10808`, чтобы сразу подтвердить трафик в сторону VPS/панели.
- Исправлена «ложная невключаемость»: proxy-проверка теперь с ретраями (до 20 сек), чтобы контейнер успевал стартовать после нажатия `MUTE`.
- При включении `xray-pi5` скрипт теперь принудительно останавливает `wg-quick@wg-exit`, чтобы не было двух VPN одновременно.
- `scripts/argon-ir-stb-remote-listener.py`, `config/argonpowerbutton.py`: обновлены тексты/комментарии для режима `xray-pi5` (с fallback на `wg-exit`).

## 2026-06-02 — ИК-пульт STB: кнопка MUTE переключает VPN

- `scripts/argon-ir-stb-remote-listener.py`: добавлено действие для `MUTE` — запуск `~/bin/argon-vpn-toggle.sh` (вкл/выкл `wg-quick@wg-exit`) с уведомлением.
- `scripts/install-argon-ir-stb-remote.sh`: при установке дополнительно копируется `scripts/argon-vpn-toggle.sh` в `~/bin`.
- `docs/ARGON_IR.md`: обновлена таблица действий кнопок (`MUTE` = VPN on/off).

## 2026-06-02 — Argon кнопка: VPN toggle + OLED-индикация с обычным WireGuard

- `config/argonpowerbutton.py`: возвращено управление VPN с кнопки Argon:
  - `pulsetime 2–3` → `argon-vpn-toggle.sh` (вкл/выкл `wg-quick@wg-exit`);
  - `pulsetime 4–5` → голосовой agent (старт/стоп), чтобы не потерять голосовые сценарии.
- Добавлен `scripts/argon-vpn-toggle.sh`: переключение `wg-quick@wg-exit`, проверка handshake (`wg show wg-exit`), уведомления через `notify-send`.
- `scripts/install-argon-powerbutton.sh`: теперь устанавливает в `~/bin` три скрипта: `argon-agent-voice.sh`, `argon-agent-stop.sh`, `argon-vpn-toggle.sh`.
- `oled_visual/oled_visual.py`: VPN-иконка на OLED теперь проверяет handshake и для `wg`, и для `awg` (раньше только `awg`), поэтому индикация работает с новым VPS VPN.

## 2026-05-29 — Pi 5: стабильный Wi‑Fi wlan0 (watchdog)

- Добавлен `scripts/fix-wlan0-pi5.sh`: проверка `wlan0`, снятие lock BSSID, отключение power save, переподключение `ELEKTRO_` с cooldown.
- Добавлены system-systemd юниты `config/systemd/wlan0-watchdog.{service,timer}` (каждые 2 мин, `Persistent=true`).
- Добавлен установщик `scripts/install-wlan0-watchdog-pi5.sh` (ставит в `/usr/local/bin`, `/etc/systemd/system`, NM drop-in `90-wifi-powersave.conf`).

## 2026-05-27 — Стабилизация Raspberry Pi Connect (watchdog)

- Добавлен `scripts/rpi-connect-watchdog.sh`: проверка DNS/HTTPS/`rpi-connect status` и авто‑перезапуск `rpi-connect.service` при сбоях.
- Добавлены user-systemd юниты `config/systemd/rpi-connect-watchdog.service` и `config/systemd/rpi-connect-watchdog.timer` (запуск каждые 2 минуты, `Persistent=true`).
- Добавлен установщик `scripts/install-rpi-connect-watchdog.sh` (ставит файлы в `~/.config/systemd/user`, включает таймер и делает первый прогон).

## 2026-05-27 — OLED overlay: увеличен межстрочный интервал

- `oled_firmware_draw.py`: больше зазор между строками в экранах `Прошивка...` и результате (`OK/Ошибка`) для лучшей читаемости.

## 2026-05-27 — A11039R5: probe + успех прошивки

- ETR: критерий успеха в `argon-eltavr-flash-item.sh` обновлён на `Прошито[[:space:]]*[(:]` (учитывает `Прошито (atmega328): ...`), чтобы не было ложного fail при verify OK.
- `argon-eltavr-probe-target.sh`: исправлен разбор signature `0x1e940b`; для A11039 используется `A11039R5_7cel_V10/scripts/isp-prog-args.sh`.
- `A11039R5_7cel_V10/scripts/isp-prog-args.sh`: путь через `${BASH_SOURCE[0]}` (probe больше не ломает `$0`).
- `argon-eltavr-flash-item.sh`: успех AVR по `Прошито:` / `Прошито (` (раньше A11039 прошивалась, но OLED показывал fail).

## 2026-05-27 — Переименование платы в OLED: A11039R5

- В OLED-меню обновлены `id/label/short` на `a11039r5_v10` / `A11039R5_V10`.
- Пути прошивки переведены на `A11039R5_7cel_V10/A11039R5_M168.Firmware.hex`.
- Скрипт `argon-eltavr-flash-item.sh` переключён на каталог `A11039R5_7cel_V10`.

## 2026-05-27 — OLED прошивка: проверка «та ли плата»

- Исправлен ложный fail для A11039: заглушён stdout `isp-prog-args.sh`, чтобы в `probe` попадала только сигнатура MCU, а не строка `ISP: ...`.
- `argon-eltavr-probe-target.sh`: перед заливкой — ISP signature (168/328) или ST-Link SWD/SWIM (STM32/STM8).
- `config/eltavr_oled_firmware.json`: поле `target`; при несовпадении OLED «это STM32» / «это 328» и т.п. Обход: `ARGON_SKIP_BOARD_PROBE=1`.

## 2026-05-27 — OLED «завис на прошивке»

- `argon-eltavr-flash-item.sh`: `set +e` на блок прошивки (при ошибке `flash.sh` `set -e` раньше обрывал скрипт до `set_status fail`); EXIT-trap сбрасывает `running` → `fail`.
- `ir_oled_menu.py`: watchdog `running` > 180 с → `fail` «таймаут».

## 2026-05-27 — A20014 из OLED: снова с RDP=1

- `argon-eltavr-flash-item.sh`: `A20014_APPLY_RDP=1` (было `0`); успех только при `64 KiB` + подтверждении RDP; OLED `64K+RDP`.

## 2026-05-27 — IR пульт: не работал после reboot (lircd)

- `argon-ir-stb-ok.service`: убраны `Wants/After oled-visual` (цикл systemd); `lircd` отключён и masked — конфликтовал с `mode2` на `/dev/lirc0`.
- `install-argon-ir-stb-remote.sh`: при установке отключает `lircd.service`/`lircd.socket`.

## 2026-05-27 — OLED меню прошивок: однострочный режим

- `oled_firmware_draw.py`: в меню отображается только текущая прошивка (`>имя`) и позиция `N/total`.
- Навигация `UP/DOWN` осталась пошаговой по одной прошивке.
- Увеличен шрифт однострочного меню (`FONT_MENU=16`, `FONT_TITLE=12`) для маленького OLED.
- Дополнительно: узкий шрифт `DejaVuSansCondensed-Bold`, размер `FONT_MENU=18`, `FONT_TITLE=13`.
- Актуально: **3 строки**, узкий жирный `DejaVuSansCondensed-Bold`; без `N/total`; листание **по кругу**; выбранная строка — **заливка** (инверсия), без `>`.

## 2026-05-27 — BACK: шаг назад в OLED-меню

- `ir_oled_menu.py`: добавлен `step_back()` — сначала скрывает overlay результата прошивки (`ok/fail`), затем возвращает на главный экран.
- `scripts/argon-ir-stb-remote-listener.py`: кнопка `BACK` подключена к `step_back()` (отдельно от `HOME`).

## 2026-05-27 — IR: меню после ребута + POWER как Argon shutdown

- `config/systemd/argon-ir-stb-ok.service`: убран `After=argononed` (цикл systemd → сервис не стартовал после reboot).
- `scripts/argon-poweroff.sh`: `shutdown -h now` (отсечение питания Argon через `argon-shutdown.sh`), не `systemctl poweroff` (давал reboot).
- `argon-ir-stb-remote-listener.py`: POWER → `argon-poweroff.sh`.

## 2026-05-27 — IR POWER как кнопка выключения Pi

- Первая версия POWER (заменена на Argon shutdown выше).

## 2026-05-27 — A11092: ошибка в конце (SWIM 0x04)

- `flash-stlink.sh`: сброс SWIM перед записью, до 3 попыток write/verify.
- `argon-eltavr-flash-item.sh`: NUL в логе stm8flash; успех по `Bytes written/verified`.

## 2026-05-27 — A11092: ошибка прошивки (нет stm8flash)

- Собран `Проекты/Arduino/tools/stm8flash/`; `a11092/scripts/flash-stlink.sh` ищет бинарник там.
- `install-stm8flash.sh` — повторная установка на Pi.
- OLED: при отсутствии утилиты — «нет stm8flash»; при SWIM — «STM8/SWIM?».

## 2026-05-27 — ETR_2206: «Готово» без прошивки (ложный OK)

- `argon-eltavr-flash-item.sh`: успех только при `bytes of flash verified` + `Прошито (`; flock на параллельные запуски; OLED — «5230B OK» + «RESET+откл ISP».
- `oled_firmware_draw.py`: на экране результат verify, не общее «Готово».

## 2026-05-27 — ETR_2206: исправлена прошивка по ISP

- `Buton_to_serial_Rev_4_V2/scripts/isp-detect-mcu.sh`: чтение signature с `-p` и формат `0x1e,0x95,0x14` (ATmega328).
- Прошивка ETR из OLED (`argon-eltavr-flash-item.sh etr_2206_r4v2`) — проверено.

## 2026-05-27 — OLED + пульт: меню прошивок Eltavr a20014

- **MENU** → второй экран OLED со списком прошивок; **HOME** → главный (статус Pi).
- **↑↓** выбор, **OK** прошивка (`argon-eltavr-flash-item.sh`, каталог `config/eltavr_oled_firmware.json`).
- Список меню приведён к 5 пунктам: `A11034R6_V49`, `A11039R5_V10`, `A20014_V7`, `A11092`, `ETR_2206_R4V2`.
- `scripts/argon-ir-stb-remote-listener.py`, правки `~/oled_visual/oled_visual.py`, `ir_oled_menu.py`.

## 2026-05-27 — ИК: кнопки пульта приставки (`stb_remote.json`)

- … VOL_UP/VOL_DOWN, MOUSE в `config/ir/stb_remote.json`; OK `0xf20d4040` (lib/lirc).
- Захват: `scripts/argon-ir-capture-button.py stb_remote <кнопка>`; док: `docs/ARGON_IR.md`.

## 2026-05-27 — Пульт STB: OK 1× → прошивка a20014 (вместо VPN)

- `scripts/argon-a20014-flash-v7.sh` → `~/bin/`: factory v7 9600 + RDP (~20 с); лог `/tmp/argon-a20014-flash.log`.
- `argon-ir-stb-ok-listener.py`: одиночное OK → flash; 2× → голос; 2× при agent → стоп. Док: `docs/ARGON_IR.md`.

## 2026-05-27 — Пульт STB и OLED/Argon: временно отвязаны

- `argon-ir-stb-ok.service` отключён (пульт OK не запускает команды).
- `config/argonpowerbutton.py`: корпусная кнопка теперь делает только toggling голосового agent по двойному нажатию (VPN и OLED-управление убраны).

## 2026-05-26 — VPN: исправлена ложная проверка handshake

- `/home/pi/vpn/setup-exit-vpn.sh`, `/home/pi/bin/argon-vpn-toggle.sh`: grep больше не путает `keepalive: every 25 seconds` с handshake; при FAIL — автоматический `--down`.
- Сейчас оба профиля (`amnezia-de.conf`, `amnezia.conf`) не получают ответ от сервера (0 B received) — нужен живой Amnezia/конфиг.

## 2026-05-26 — Argon V3: ИК-приёмник (GPIO 23) + обучение пульта

- Включено: `dtoverlay=gpio-ir,gpio_pin=23` в `/boot/firmware/config.txt`, пакет `lirc`, `lircd` active, `/dev/lirc0`.
- Скрипты: `scripts/argon-ir-learn-remote.sh`, `scripts/argon-ir-test.sh`; док: `docs/ARGON_IR.md`.
- Пульт **ТВ-приставки (stb)**, кнопка **KEY_OK**: `config/lirc/stb.conf` (`0xf20d4040`); проверка: `scripts/argon-ir-verify-stb-ok.sh`.
- **OK приставки:** `argon-ir-stb-ok.service` — 1× прошивка a20014 (с 2026-05-27); 2× голос; 2× при agent → стоп.

## 2026-05-26 — Pi 3: голос → OpenCode (Ctrl+Space)

- `scripts/pi3-agent-voice.sh` — как Argon на Pi 5, но **OpenCode** (`oc-bridge`) вместо `agent`; каталог `/home/pi/ai_assistant`.
- `scripts/install-pi3-agent-voice.sh`, `pi3-upload-file.sh`, `install-pi3-agent-voice-labwc.sh` — деплой по NetBird; **Ctrl+Space** в labwc.
- `agent-voice-lib.sh` — fallback на системный `python3`, если нет venv (Pi 3, облачный STT).
- Док: `PI3_NETBIRD.md` § «Голос → OpenCode».

## 2026-05-26 — OLED: текст команды и «Готово» (кнопка Argon)

- `voice_oled.py`: режимы `working` / `done` / `idle` в `/run/user/1000/agent-oled-*`.
- `/home/pi/oled_visual/oled_visual.py`: на время agent — текст вместо температуры и полос CPU; затем **«Готово»** ~4 с; снова тулбары.
- `scripts/argon-agent-voice.sh`: после STT — OLED + **ожидание** `agent -p` (не фон); `ARGON_AGENT_OLED_BUSY=1` по умолчанию.
- **Исправление:** `~/bin/argon-agent-voice.sh` брал `ROOT=/home/pi` → `import voice_oled` падал; ROOT → `Проекты/ai_assistant`.
- OLED working: без заголовка **Agent**; текст команды **18 pt** (~2×), до 3 строк.

## 2026-05-25 — Кнопка Argon: откат на голос по короткому нажатию

- `config/argonpowerbutton.py`: откат логики с таймером (двойной клик → VPN): **pulsetime 2–3** сразу → `argon-agent-voice.sh`; **pulsetime 1** → VPN; shutdown 4–5 без изменений.
- `scripts/install-argon-powerbutton.sh` — деплой на Pi 5, `argononed` active.

## 2026-05-25 — Кнопка Argon: двойной клик VPN (отменено)

- Было: одиночное короткое → голос с задержкой; два коротких в 0,42 с → VPN — отменено по запросу пользователя.
- `WORKSPACE_WHERE.md`, `Платы и модули/Raspberry_Pi_5/TECH_SUMMARY.md` — приоритет кнопки + INMP441.

## 2026-05-25 — Карта «где что»

- `WORKSPACE_WHERE.md` — железо (Pi 3 реле / Pi 5 Stack HAT), пути проектов и ai_assistant.
- `claude_client.py` — карта в `--append-system-prompt` (лимит `CLAUDE_WORKSPACE_WHERE_MAX_CHARS`).
- `SESSION_BRIEF.md` — ссылка и топология; `AGENTS.md` — строка в таблице.

## 2026-05-25 — Cursor Agent: прошивка как в IDE

- `cursor_hardware_playbook.py`: при запросах прошивки — playbook A20014/all-in-one, модель `composer-2.5-fast` (`CURSOR_AGENT_HARDWARE_MODEL`), лимит ответа 4500 символов.
- Telegram: hint «Прошивка · 2–5 мин»; `.env` + `.env.example`.

## 2026-05-25 — Cursor Agent Telegram: диагностика и UX

- `agent` на Pi 5 работает; чат в режиме `cursor`. Перед запросом — «20–90 с»; в промпте — без filler и сразу shell/read.

## 2026-05-25

- **Микрофон INMP441:** `AGENT_VOICE_MIC_GAIN` (по умолчанию **2.0**, ffmpeg + лимитер); ALSA на card 2 без Capture volume.
- **OLED голос:** мигающее **«Ai»** (`oled_visual.py`); после STT — вентилятор.
- **Исправление голоса/OLED:** флаг `/run/user/1000/`; кнопка Argon `pulsetime` 2–3; lock `/tmp/`.
- **STT Groq:** в `.env` — `AGENT_VOICE_STT=groq` + `GROQ_API_KEY` (agent-voice, Telegram, кнопка Argon).
- **Кнопка Argon ONE:** короткое одиночное нажатие → `scripts/argon-agent-voice.sh` (`~/bin/`, правка `/etc/argon/argonpowerbutton.py`); двойное — VPN без изменений.
- **STT fallback:** при `AGENT_VOICE_STT=openai|groq` без ключа в `.env` — автоматически local Whisper (без `RuntimeError`); сообщение в stderr; шаблон `OPENAI_*`/`GROQ_*` в `.env`.
- **STT из интернета:** `speech_client.py` — OpenAI Whisper API и Groq; `agent-voice` по умолчанию `AGENT_VOICE_STT=openai`; Telegram через `SPEECH_PROVIDER`.
- **agent-voice: дефолт small** (локально): `AGENT_VOICE_STT=local`.
- **agent-voice: preload** до записи, тише HF Hub; 7 с записи по умолчанию.
- **agent-voice: качество STT:** дефолт `medium`, 7 с, `WHISPER_INITIAL_PROMPT`, `beam_size=7`, правка «прошая→прошей».
- **`scripts/agent-voice.sh`** → `agent-voice`: голос → `agent -p`; `-t`, `-l`.
- **`scripts/agent-input.sh`** → `agent-input`: как чат — печать или `v`+Enter (голос → текст в строке → правка → Enter → agent); общая библиотека `agent-voice-lib.sh`.
- **Исправление `agent-input`:** лишняя `}` в trim добавляла `}}` к каждой строке (`v` → `v}}`), голос не срабатывал — убрана опечатка в четырёх строках trim.
- **`agent-input` — диктовка по Ctrl:** удержание Ctrl → запись → отпускание → текст в строке → Enter; `scripts/agent_input_line.py`, зависимость `evdev` (без фиксированных 5 с).

## 2026-05-22

- **Cursor Agent → Telegram:** усилен промпт (краткий ответ в начале), постобработка `compress_for_telegram` (лимит `CURSOR_TELEGRAM_MAX_CHARS`, сжатие кода, блок «Итог»); не отдаётся сырой NDJSON stream-json в чат.
- **Правила workspace:** активный проект по умолчанию — `ai_assistant` в `.cursor/rules/module-docs-priority.mdc`, `active-project-boundaries.mdc`, `RULES_MASTER_PLAN.md`, `Проекты/README.md`; добавлены `AGENTS.md`, `.cursor/rules/project-workflow.mdc`; стиль ответа — в `core-standards-and-workflow.mdc`.
- **Tmux:** убраны автоподсказки `pane_hint` при `ai-tmux start` (шум в терминале).
- **Tmux ↔ Telegram:** кнопки вкл/выкл в `/tmux`, `/mode`, `/attach`; настройка `tmux_sync` в `data/settings.json` (приоритет над `.env`).
- **Tmux ↔ Telegram:** при `/mode` и каждом сообщении — `tmux_sync.focus_mode()` + подсказка `ai-tmux attach …`; команды `/attach`, `/tmux`; `ai-tmux focus РЕЖИМ`.
- **Tmux для AI:** сессия `ai` с окнами shell/telegram/claude/opencode/agent/pi3; скрипт `scripts/ai-tmux.sh`, конфиг `config/tmux.conf`, док `TMUX.md`; установка `Документы/.cursor/scripts/install-ai-tmux-pi5.sh` → команда `ai-tmux`.

## 2026-05-21

- **OpenCode → Pi 3:** `opencode-sync-pi5-to-pi3.sh` (алиас `pi3`, Kex для NetBird); HTTP-fallback `opencode-sync-pi5-to-pi3-http.sh` (порт 9876 на `wt0`); бандл `~/backups/opencode-pi5-bundle-20260521T183321.tar.gz`. NetBird до Pi 3 нестабилен (rsync/длинный SSH рвутся); на Pi 3 частично обновлён `opencode.json` с Pi 5. Полная установка — при стабильном peer или через Connect + `opencode-apply-bundle-pi3-local.sh`.
- **Геопозиция с телефона:** Telegram принимает `location` / live; сохранение в `data/phone_location.json`; команды `/where`, `/где`; модуль `phone_location.py`; подсказка координат в промпте для режимов claude/cursor/opencode. Док: `PHONE_TRACKING.md`.
- **Cursor Agent без таймаута:** `CURSOR_AGENT_TIMEOUT=0` в `.env` — subprocess без лимита; `parse_agent_timeout()` в `cursor_agent_client.py`.
- **Откат (по запросу):** убраны подсказки Cursor про почту/VPN, статус «жду…» в Telegram и доп. текст при таймауте msmtp — поведение как до инцидента с зависшим письмом.
- **Голос → текст (локальный Whisper):** голосовые и аудио в Telegram распознаются на Pi 5 через `faster-whisper` (`whisper_client.py`, venv проекта); текст уходит в текущий режим (`/mode`). Команда `/whisper`. Платных API нет — только загрузка модели и время CPU. Сервис: `venv/bin/python3`.
- **Whisper fix:** VAD по умолчанию выкл (короткие голосовые); повтор без VAD при пустом тексте; предзагрузка модели при старте бота; подсказка про 1–3 мин при первом скачивании.
- **Cursor Agent + фото:** изображения из Telegram передаются путём к файлу в промпт (Read); таймаут до 420 с при картинках.
- **Cursor vision по умолчанию:** `CURSOR_AGENT_MODEL=gemini-3-flash`; при фото и модели codex/auto — автоподмена на `CURSOR_AGENT_VISION_MODEL`.
- **`/cursor_models`:** шпаргалка «вкладка Agents в Cursor Desktop ↔ Telegram» (модель, сессии, BYOK, workspace).
- **Синхронизация модели GUI→Telegram:** `cursor_gui_sync.py`, чтение `~/.cursor/cli-config.json`; `/cursor_model gui` — снова из IDE.
- **Cursor: модель vs сессия:** при смене модели (GUI/Telegram) сброс `--resume`; в ответе `[Cursor · …]` — фактическая модель запроса; `/cursor_model` показывает сессию.
- **GUI модель из IDE:** `cursor_gui_sync` читает `state.vscdb` (`aiSettings.modelConfig.composer`), не только `cli-config.json` (там мог остаться gemini).
- Убрано предупреждение про расхождение CLI config / IDE в `/cursor_model` (шум для пользователя).
- **Cursor Agent в Telegram:** режим `/mode cursor`, команды `/cursor`, `/cursor_model`, `/cursor_reset`, `/cursor_continue`; клиент `cursor_agent_client.py` (`agent -p`, нужен `agent login`).
- **OpenCode Pi 3:** скрипты `opencode-upgrade-remote-pi3.sh` (с Pi 5) и `opencode-upgrade-pi3-local.sh` (на Pi 3); с Pi 5 SSH пока недоступен — обновление вручную через Connect.
- **OpenAI BYOK:** пользователь добавляет ключ в аккаунте opencode.ai (не локально на Pi). Запасные модели в Telegram: `/oc_model`. См. `PROVIDERS_BACKUP.md`.
- **OpenCode Pi 5:** обновление `1.14.48` → `1.15.6` (`sudo opencode upgrade --method npm`). Автообновление: timer `opencode-auto-upgrade.timer` (ежедневно ~04:15), скрипт `Документы/.cursor/scripts/opencode-auto-upgrade.sh`.
- **Telegram + OpenCode:** `/oc_model` — модель OpenCode на чат; `/oc_models` — шпаргалка бесплатных моделей; режим `/mode opencode` использует выбранную модель.
- **Меню Telegram:** `/cheatsheet`, `/hints`, `/agents`, `/pi3help` + пункты в `setMyCommands`; алиасы `/шпаргалка`, `/подсказки` и др.
- **Pi 3 через NetBird:** `PI3_SSH_HOST=pi@100.102.186.61` (Pi 5 на работе, Pi 3 дома). Док `PI3_NETBIRD.md`; `ai-assistant-telegram.service` — `After=netbird.service`.
- **Режимы агента в Telegram:** по умолчанию Claude Code (Pi 5); `/mode opencode|pi3|pi3cc|shell`; явные `/pi5_oc`, `/pi3_cc`, сброс `/pi3_cc_reset`. Маршрутизация в `telegram_relay.py` (раньше было только в `bot_ui.py`).

## 2026-05-20

- **`bot_ui.py`:** единые подсказки, `/start` и `/help`, меню Telegram (`setMyCommands`), алиасы `/oc_reset`, `/pi3_oc` и т.д.
- **Claude Code — экономия токенов:** по умолчанию **без `--resume`** (новая сессия на сообщение); краткий контекст через `--append-system-prompt` из `SESSION_BRIEF.md`; авто-строки в brief после ответа.
- Telegram: `/oc-continue` — включить длинную сессию; `/oc-reset` — снова новые сессии. Правила в `~/.claude/CLAUDE.md`, память `feedback_session_compact.md`.

## 2026-05-19

- **Фото в Telegram:** сохранение в `data/incoming/<chat_id>/`, анализ через Claude Code **Read** (не `--file`); таймаут до 420 с для картинок.
- Telegram-ассистент на **Pi 5** переведён с **OpenCode** на **Claude Code** (`claude_client.py`, `claude -p --resume`).
- Сессии в `data/settings.json`: ключ **`claude_session`** (старый `opencode_session` читается при миграции).
- `ai-assistant-telegram.service`: переменные Claude в **`ai_assistant/.env`**; бинарь — `claude.exe`. **`CLAUDE_WORKDIR=/home/pi/Документы`**.
- Команды `/pi3-oc` без изменений (OpenCode на Pi 3).
- Правила Claude Code только в `~/.claude/CLAUDE.md` (файл в `Документы/` удалён).

## 2026-05-15

- OpenCode: отключены snapshots (`snapshot: false` в `~/.config/opencode/opencode.json`), чтобы не запускался `git add` по всему `Документы/`.
- `OPENCODE_WORKDIR` → активный проект Switch; `opencode-serve` стартует из каталога Switch.
- Telegram-бот подхватывает `~/.opencode.env`.

## 2026-05-14

- Добавлено правило Cursor **`.cursor/rules/docker-cleanup-after-rebuild.mdc`**: после пересборки Docker запускать **`Документы/.cursor/scripts/docker-post-rebuild-cleanup.sh`** (цикл `docker builder prune -f` до `Total reclaimed space: 0B`, затем `docker image prune -f`); каноника в **`Документы/.cursor/rules/core-standards-and-workflow.mdc`**.

## 2026-05-13

- Проект создан: перенос `telegram_ssh_relay.py` в `Проекты/ai_assistant/telegram_relay.py`.
- Конфигурация Telegram: `TELEGRAM_BOT_TOKEN` и `TELEGRAM_ALLOW_FROM` в `.env` проекта.
- Логика бывшего `opencode_bridge.py` встроена в `opencode_client.py` (отдельный скрипт моста удалён из эксплуатации).
- Состояние: каталог `data/` внутри проекта (миграция offset/settings со старого `~/.local/state/telegram-ssh-relay/` при развёртывании).
- User-systemd: сервис `ai-assistant-telegram.service` вместо `telegram-ssh-relay.service`.
