# Cursor Agent — ПК Артёма (через Pi 3, домашняя LAN)

Установка **Cursor Agent CLI** на Windows-ПК **Шпак Артём**. Pi 3 и ПК Артёма в одной сети **GARAGE** (`10.0.20.0/24`) — **NetBird не нужен**.

## Быстрый старт (Артём)

1. Подключиться к домашней Wi‑Fi **GARAGE**.
2. **Скачать пакет с Pi 3** (PowerShell):
   ```powershell
   scp -r pi@10.0.20.56:~/artem-cursor-agent $env:USERPROFILE\Downloads\artem-cursor-agent
   ```
3. **Установить**:
   ```powershell
   cd $env:USERPROFILE\Downloads\artem-cursor-agent
   powershell -ExecutionPolicy Bypass -File install-cursor-agent-windows.ps1
   ```
4. **Проверка**:
   ```powershell
   ping 10.0.20.56
   ssh pi3 hostname
   agent --version
   agent -p "ответь одним словом: OK"
   ```

## Доступ (LAN)

| Команда | IP | Назначение |
|---------|-----|------------|
| `ssh pi3` | **10.0.20.56** | Малинка в гараже |
| `ssh kali` | **10.0.20.42** | Kali в гараже (если включена) |
| `ssh pi5-wan` | 91.215.61.76 | Pi 5 на работе (опционально, WAN) |

## Credentials (не коммитить)

Папка `credentials/` — на Pi 3 в bundle и локально на Pi 5:

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

- Приватный ключ **не** отправлять в Telegram.
- Bundle на Pi 3: `chmod 600` на credentials.
- Отозвать доступ: удалить `artem-shpak-cursor-agent` из `~/.ssh/authorized_keys`.
