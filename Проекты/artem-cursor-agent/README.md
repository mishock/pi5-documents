# Cursor Agent — ПК Артёма (через Pi 3)

Установка **Cursor Agent CLI** на Windows-ПК **Шпак Артём** с доступом к малинкам (Pi 3, Pi 5, Kali) по NetBird + SSH.

## Быстрый старт (Артём)

1. **NetBird** — установить с https://netbird.io/, войти в **семейный аккаунт**, статус Connected.
2. **Скачать пакет с Pi 3** (PowerShell):
   ```powershell
   scp -r pi@100.102.186.61:~/artem-cursor-agent $env:USERPROFILE\Downloads\artem-cursor-agent
   ```
3. **Установить**:
   ```powershell
   cd $env:USERPROFILE\Downloads\artem-cursor-agent
   powershell -ExecutionPolicy Bypass -File install-cursor-agent-windows.ps1
   ```
4. **Проверка**:
   ```powershell
   ssh pi3 hostname
   agent --version
   agent -p "ответь одним словом: OK"
   ```

## Доступ

| Узел | SSH | Назначение |
|------|-----|------------|
| **pi3** | `ssh pi3` | Гараж, 24/7, OpenCode, голос |
| **pi5** | `ssh pi5` | Основной «мозг», Documents |
| **kali** | `ssh kali` | Через pi3, OBD/приборка |
| **pi5-wan** | `ssh pi5-wan` | Pi 5 с работы (без NetBird) |

**PWA Джарвис (чат + голос):** https://91.215.61.76:8767/app/

## Credentials (не коммитить)

Папка `credentials/` — только на Pi 5 и в bundle на Pi 3:

- `artem_ed25519` / `.pub` — SSH-ключ
- `cursor-api-key.txt` — User API Key Cursor

## Деплой с Pi 5

```bash
bash Проекты/artem-cursor-agent/scripts/deploy-via-pi3.sh
```

Обновление ключей на малинках:

```bash
bash Проекты/artem-cursor-agent/scripts/install-ssh-keys-mesh.sh
```

## Безопасность

- Приватный ключ **не** отправлять в Telegram и не публиковать.
- Bundle на Pi 3: `chmod 600` на credentials.
- Отозвать доступ: удалить строку `artem-shpak-cursor-agent` из `~/.ssh/authorized_keys` на каждой малинке.
