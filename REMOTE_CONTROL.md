# Cursor Remote Control — Pi 5

**Канон:** `/home/pi/Documents`.

## Аккаунты (важно)

| Где | Аккаунт Cursor |
|-----|----------------|
| Телефон + Pi 5 | **mishock24@gmail.com** (домашний) |
| Рабочий ПК | **mishock24@icloud.com** (рабочий) — отдельно |

Worker Pi5 виден **только** на gmail. «Документы на ПК» / CursorDocs — на icloud (или offline); с телефона-gmail его не выбирать.

## Проверено 2026-10-21 15:31

| Проверка | Результат |
|----------|-----------|
| IDE / CLI email | **mishock24@gmail.com** |
| Облако `remoteControlEnabled` | **true** |
| Облако `allowPrivateWorkers` | **true** |
| Private worker | **Документы на Pi5** online (`f6f3e0d8-…`) |
| Сервис | `cursor-self-hosted-worker.service` **active** |
| Auth worker | `CURSOR_API_KEY` в `~/.config/cursor-worker.env` + `~/.config/cursor/auth.json` |
| Enroll | `google-oauth2\|user_01KN47E048DYNJ51WGHYS9F14W` |
| `cursor.desktopBridge.enabled` | **true** |
| Прокси | xray + `cursor-proxy-http` :10809 + `cursor-redsocks` |

## Почему на телефоне было Cloud / No Computers

1. Worker на Pi5 **падал** (`Authentication required`) — слетел CLI `auth.json`, ключ в env был отключён.
2. В Runtime выбран **Cloud**, а не Self-Hosted **Документы на Pi5**.
3. **CursorDocs (ПК)** Disconnected — другой аккаунт (icloud) или ПК выключен; к малинке не относится.

## Как на телефоне (gmail)

1. Аккаунт: **mishock24@gmail.com** (не icloud).
2. Agents → **новый** агент (не переключать старый Cloud).
3. Репозиторий: **mishock/pi5-documents**.
4. Runtime → Self-Hosted → **Документы на Pi5** (зелёный Connected).

Ссылка worker: https://cursor.com/agents#workerId=f6f3e0d8-f362-4376-b9b2-57e967ae4e48

## Фикс на Pi5

```bash
bash ~/bin/cursor-rc-force-on.sh          # облако+enroll+Agents
systemctl --user restart cursor-self-hosted-worker
bash ~/bin/cursor-pi5-worker-health.sh
```

Сервисы: `cursor-self-hosted-worker`, `cursor-redsocks`, `cursor-proxy-http`, `cursor-keep-awake`.


---

## Почему «не включается»

Node utility Cursor ходил на `api2` **в обход** xray → `not available in your region` → UI ставит OFF.  
Облако при этом уже было ON.

## Фикс (постоянно)

```bash
# transparent HTTPS uid=pi → redsocks :12346 → xray SOCKS 10808
bash ~/bin/cursor-redsocks-on.sh start   # или user-service cursor-redsocks
bash ~/bin/cursor-rc-force-on.sh         # облако+enroll+открыть Agents
```

Сервис: `systemctl --user enable --now cursor-redsocks.service`  
(нужен passwordless `sudo iptables` для `cursor-redsocks-iptables.sh`).

Запуск IDE: `~/bin/cursor-with-proxy.sh` / ярлык Agents — **окно не закрывать**.

## Быстрая самопроверка

```bash
curl -sS https://api.ipify.org; echo   # не должен быть 91.215.61.76
systemctl --user is-active cursor-self-hosted-worker cursor-redsocks
grep -E 'region|acquired wakelock' ~/.config/Cursor/logs/*/window*/renderer.log | tail -5
```

## Телефон: Target Unavailable (2026-10-16)

Причина: worker виден (Connected), но агент в приложении привязан к **другому** репо/Cloud.
Worker обслуживает только `mishock/pi5-documents` (папка `/home/pi/Documents`).

**Как правильно:**
1. В приложении — **новый** агент (не переключать runtime у старого Cloud).
2. Репозиторий: **mishock/pi5-documents**.
3. Runtime / My Machines: **Документы на Pi5**.

Репо: https://github.com/mishock/pi5-documents (public; private у GitHub аккаунта недоступны из‑за trade controls).

## Другие машины (обновлено 2026-11-10)

| Worker | Репо | Ссылка |
|--------|------|--------|
| **Документы на Pi5** | mishock/pi5-documents | как выше |
| **Документы на Pi3** | mishock/pi3-documents | https://cursor.com/agents#workerId=a7a15d6f-8f13-4fd6-b5b3-af44fb45fbf8 |
| **Документы на cloud** | mishock/cloud-documents | https://cursor.com/agents#workerId=97046086-e6c3-4eba-adb4-27bbdb20cca2 |
| **Документы на Kali** | mishock/kali-documents | https://cursor.com/agents#workerId=c47e6c35-8494-441d-9d8e-d5b15aeacaf0 |

На iPhone (gmail): новый агент → выбрать репо → Runtime Self-Hosted → нужный worker.

### Kali (2026-11-10)

- Канон: `/home/kali/Documents`, репо `mishock/kali-documents`
- Сервисы user-systemd: `xray-kali`, `cursor-proxy-http` (`127.0.0.1:10809` → SOCKS `10808`), `cursor-self-hosted-worker`
- Env worker как на Pi3: `HTTPS_PROXY/HTTP_PROXY/ALL_PROXY=http://127.0.0.1:10809`, `NODE_OPTIONS=--use-env-proxy` (redsocks для Kali не используем)
- LAN офис: `10.1.30.97`, NetBird: `100.102.121.127`
- Проверка: Runtime → Self-Hosted → **Документы на Kali** (Connected)

## Фикс worker short-lived (2026-11-08)

Причина: `HTTPS_PROXY=http://127.0.0.1:10809` в `cursor-worker.env` ломал WebSocket моста (session ~100ms).
Решение: убрать HTTP_PROXY у worker; egress только через **cursor-redsocks** (transparent → xray 10808).
Скрипт `cursor-pi5-worker-fix.sh` обновлён. Unit зависит от `cursor-redsocks.service`.
