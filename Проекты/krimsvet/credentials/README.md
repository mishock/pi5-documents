# Доступы krimsvet.ru (REG.RU)

Обновлено: 2026-11-10

Секреты: **`regru-hosting.env`** (права `600`).

| Что | Где |
|-----|-----|
| ISPmanager / SSH / SFTP | `ISP_*` |
| FTP (рабочий) | `FTP_PASS` |
| FTP как в карточке REG.RU | `FTP_PASS_PANEL` |
| MySQL | `MYSQL_*` |
| Папка сайта | `FTP_PATH=www/krimsvet.ru/` |

Карточка: REG.RU `12832707`. Панель: `https://server276.hosting.reg.ru:1500/`

```bash
set -a; source Проекты/krimsvet/credentials/regru-hosting.env; set +a
```
