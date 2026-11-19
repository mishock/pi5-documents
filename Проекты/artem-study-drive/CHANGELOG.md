# CHANGELOG — artem-study-drive

## 2026-11-19

- Месячный монитор **госаккредитации 09.02.07**: `scripts/accreditation-monitor.mjs`, конфиг `config/accreditation-watch.json`.
- Таймер `artem-study-accreditation.timer` — **1-е число, 10:00 MSK**; при изменении PDF/статуса/страницы — письмо на **mishock24@gmail.com**.
- Сводка `data/00_Аккредитация_09.02.07.md`, снимок `data/accreditation-snapshot.json`, лог `~/logs/artem-accreditation.log`.
- Установка: `scripts/install-monthly-accreditation-timer.sh`.

## 2026-10-28

- Добавлен **`00_Профиль_Артём.md`** (ДР 20.06.2009, семья, учёба, решение по курсу «Скултех»/Квантастика — не регистрироваться).
- Обновлены `00_Сводка_учёба_Артём.md` и `config/knowledge-base.json` (чек 64 350 ₽, профиль, parentOffers).
- Дубликат профиля и сводки залит на Drive «Учёба Артём».

## 2026-08-31 (4)

- **Единый справочник** `00_Справочник_КИПУ_Артём.md` — ответы на любые вопросы об учёбе.
- `knowledge-sync.mjs` + `config/knowledge-base.json` (реквизиты, договор, контакты, темы).
- Расширен мониторинг сайта: ЦСПО, аккредитация, лицензия, новости, образование.
- Таймер **четверг 09:00** — быстрая проверка сайта (`quick-site-check.sh`).

## 2026-08-31 (3)

- Мониторинг **успеваемости**: `academic-monitor.mjs`, конфиг `config/academic-track.json`.
- Живая сводка на Drive: **`00_Успеваемость_Артём.md`**.
- Email-алерты на mishock24@gmail.com при негативных списках / новых списках по 09.02.07.
- Еженедельная проверка: Drive + сайт + успеваемость.

## 2026-08-31 (2)

- Мониторинг сайта **kipu-rc.ru**: `site-monitor.mjs`, конфиг `config/site-watch.json`.
- Живая сводка на Drive: **`00_Мониторинг_сайта_КИПУ.md`** (id `1IDIKXiBbQcLhAQXlFPUzm04BH6qeqPAD`).
- Еженедельная проверка: Drive + сайт (понедельник 09:00).

## 2026-08-31

- Создан проект мониторинга папки «Учёба Артём» на Google Drive.
- Скрипт `drive-check.mjs`: diff файлов, автотранскрипция аудио (Whisper).
- Таймер `artem-study-drive-check.timer` — понедельник 09:00.
- Правило Cursor `artem-study-drive.mdc` дополнено еженедельной проверкой.
