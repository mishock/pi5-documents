# Учёба Артём — мониторинг Google Drive

> **Обновлено:** 2026-11-19

Папка на Drive: **Учёба Артём** · id `1kJfRYBl7QKTVLEWlw32nK_J_sG-dVb5V`  
https://drive.google.com/drive/folders/1kJfRYBl7QKTVLEWlw32nK_J_sG-dVb5V

## Задача

Пользователь закидывает в папку документы, чеки, аудио с собраний. Агент (Cursor):

1. **Раз в неделю** (таймер) или **по запросу** — проверяет новые файлы.
2. **Анализирует** PDF/фото/договоры, **транскрибирует** аудио.
3. **Обновляет сводку** `.md` на Drive (аккуратно, по разделам).
4. Временные фото — удалять после переноса в сводку (если пользователь просил).
5. **Раз в месяц** — госаккредитация **09.02.07** на сайте КИПУ; при изменении — письмо на **mishock24@gmail.com**.

Правило Cursor: `Документы/.cursor/rules/artem-study-drive.mdc`

## Автопроверка (Pi 5)

```bash
bash Проекты/artem-study-drive/scripts/install-weekly-timer.sh
bash Проекты/artem-study-drive/scripts/install-monthly-accreditation-timer.sh
```

- Таймер: **понедельник 09:00** — полная проверка **раз в неделю**
- Таймер: **1-е число, 10:00 MSK** — **аккредитация 09.02.07** (`artem-study-accreditation.timer`)
- Фильтр актуальности: `scripts/temporal-filter.mjs` (текущий учебный год + будущее)
- Лог (неделя): `~/logs/artem-study-drive.log`
- Лог (аккредитация): `~/logs/artem-accreditation.log`
- Очередь для агента: `~/logs/cursor-work/pending-artem-study.md`
- Манифест файлов: `data/manifest.json`
- Транскрипты аудио: `data/transcripts/`

Вручную:

```bash
bash Проекты/artem-study-drive/scripts/weekly-drive-check.sh
node Проекты/artem-study-drive/scripts/academic-monitor.mjs   # только успеваемость
node Проекты/artem-study-drive/scripts/accreditation-monitor.mjs   # аккредитация 09.02.07
```

## Единый справочник (ответы на любые вопросы)

- **`00_Справочник_КИПУ_Артём.md`** — собирается автоматически из Drive + мониторинга
- Скрипт: `scripts/knowledge-sync.mjs`
- База фактов: `config/knowledge-base.json`
- Темы: учёба, успеваемость, реквизиты, цены, аккредитация, контакты, вычет

## Успеваемость (списки допуска / неуспевающих)

- Скрипт: `scripts/academic-monitor.mjs`
- Конфиг: `config/academic-track.json` (ФИО, группа, email)
- Сводка на Drive: **`00_Успеваемость_Артём.md`**
- Email при попадании в негативный список → **mishock24@gmail.com**
- Когда узнаете **номер группы** — добавить в `group` и `groupPatterns` в конфиге

## Госаккредитация 09.02.07 (месяц)

- Скрипт: `scripts/accreditation-monitor.mjs`
- Конфиг: `config/accreditation-watch.json`
- Источники: [sveden/common](https://kipu-rc.ru/sveden/common/), PDF выписки аккредитации и лицензии
- Снимок: `data/accreditation-snapshot.json`
- Сводка: `data/00_Аккредитация_09.02.07.md`
- Email **только при изменении** (или `--notify-baseline` / `--force-email`) → **mishock24@gmail.com**

## Именование файлов на Drive

Префиксы для сортировки:

| Префикс | Тема |
|---------|------|
| `00_` | **Профиль** `00_Профиль_Артём.md` + **Справочник** `00_Справочник_КИПУ_Артём.md` + сводки (`00_Сводка_…`, `00_Мониторинг_…`, `00_Успеваемость_…`) |
| `01_` | Договор |
| `02_` | Чеки оплаты |
| `03_`–`06_` | Приказы, постановления, компенсация |
| `07_` | Аудио собраний |
| `08_` | Налоговый вычет *(новые)* |
| `09_` | Прочие документы |

При загрузке новых файлов — переименовывать по этой схеме.
