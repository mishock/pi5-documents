## Фокус (17:54, 2026-11-23) — Bybit BTC вход весь депозит

Рынок SOL/SUI/альты overheated. Вход BTC spot ~49.53 USDT @~62784, SL −5% (59645). Trailing автотрейдером. Позиции linear нет.
---
## Фокус (17:48, 2026-11-23) — Bybit картбланш весь депозит

Автотрейдер: `use_all_usdt=true`, `max_usdt_per_trade=all` (~49.6 USDT). Было 10$/сделку. Проверено: «лимит весь USDT/сделку». Сигналов нет.
---
## Фокус (11:17, 2026-11-20) — jk_ble_pylon_deye v0.1.10

Убран TX 0x35F (версия АКБ). ESP прошит. H503 код → v0.1.12 (не прошит).
---
## Фокус (11:06, 2026-11-20) — BAT Ver=0 на Deye+Pylon

Вывод: LCD «BAT Ver» при Pylon LV не заполняется кадром 0x35F (упаковка 0x131F тоже). Эталон EmKit→Pylon для Deye шлёт только 351…35E. Поле косметическое; связь ОК по SOC/U/I.
---
## Фокус (10:14, 2026-11-20) — jk_ble_pylon_deye v0.1.8

Паритет с H503: failsafe mute, OCP→351, 0x35F, fresh 10с. Сборка SUCCESS → `releases/jk_ble_pylon_deye_v0.1.8.bin`. Прошить на ESP и проверить Deye BAT Ver / лимиты.
---
## Фокус (18:42, 2026-11-19) — Аккредитация 09.02.07 месяц + email

Таймер `artem-study-accreditation.timer` (1-е число 10:00 MSK). Письмо на mishock24@gmail.com при изменении выписки/статуса. Скрипт `Проекты/artem-study-drive/scripts/accreditation-monitor.mjs`.
---
## Фокус (18:35, 2026-11-19) — Учёба Артём / аккредитация 09.02.07

По выписке госаккредитации на сайте КИПУ (состояние 14.04.2025) специальность **09.02.07** не числится. Лицензия на 09.02.07 есть. На Drive отдельного подтверждения аккредитации нет.
---
## Фокус (15:45, 2026-11-18) — Kali на VLESS SPACE

Pi5+Pi3+Kali+офис = space. Kali exit DE.
---
## Фокус (15:38, 2026-11-18) — Pi3/Pi5 на VLESS SPACE

Оба узла `mode=space`, exit DE. Pi3: config.space.pi3 (NetBird 10809).
---
## Фокус (15:32, 2026-11-18) — Fornex снят

Fornex Etizer retired. Запасной = VLESS SPACE. Офис Keenetic mode=space (exit DE). Pi5/Pi3 primary. Канон: `Проекты/vless-space-vpn/`.
---
## Фокус (15:22, 2026-11-18) — VLESS SPACE

Подписка usr81158 до 2026-12-19. ПК Happ OK. Pi5: `vpn-switch space` (DE exit проверен ~89.19.222.7). Канон: `Проекты/vless-space-vpn/`. Primary восстановлен.
---
## Фокус (17:03, 2026-11-17) — H503 v0.1.10

Добавлен CAN `0x35F` (BAT Ver). JK SW 19.31 → на Deye ожидается **1931**.
`releases/jk_uart_pylon_deye_v0.1.10.bin` прошит.
