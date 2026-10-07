# Методичка VPN-сервера — vpn1

Дата создания: 2026-06-02

## 1. Подключение к серверу

| Параметр | Значение |
|----------|----------|
| IP | `89.127.199.6` |
| Имя в Fornex | **VPN_Server** |
| Пользователь | `vpnuser` |
| Пароль sudo | `vJUkjnVPSzJGiy6Rgqch` |
| SSH-ключ | `~/.ssh/vpn1_key` |
| Быстрое подключение | `ssh VPN_Server` или `ssh vpn1` |

## 2. Панель 3x-ui

| Параметр | Значение |
|----------|----------|
| URL | `https://127.0.0.1:37702/q6omE9HRd1U9d6t4XH` |
| Логин | `q1EQTDSBUr` |
| Пароль | `OZSkBn5yVz` |
| API Token | `41ObxsuHYJvQQjwuEbYv5MoemS6gSulebARUrH3gq4ca7Wif` |

Доступ через SSH-туннель:
```
ssh -L 37702:127.0.0.1:37702 vpn1
```
Затем открой: `https://127.0.0.1:37702/q6omE9HRd1U9d6t4XH`

## 3. VPN-подключение

| Параметр | Значение |
|----------|----------|
| Протокол | VLESS Reality |
| Порт | 443 |
| SNI | `www.yahoo.com` |
| Клиент | Hiddify / v2rayN / v2rayNG |

Клиенты в 3x-ui разделены по устройствам (каждое устройство должно использовать свой профиль):

| Устройство | Имя клиента в панели |
|------------|----------------------|
| Raspberry Pi 5 | `pi5` |
| Raspberry Pi 3 | `pi3` |
| Kali (Pi2) | `kali` |
| Телефон | `phone` |
| ПК | `pc` |
| Keenetic | `keenetic` |
| Ноутбук | `laptop` |
| Аня | `Аня` |
| Кемал | `Кемал` |
| Владимир Шуликов | `Владимир` |
| Apple TV | `appletv` |

Старый общий клиент `user1` оставлен временно для миграции. После переноса всех устройств на новые профили его нужно отключить/удалить.

Подписка (Hiddify / v2rayN → Add Profile → URL). **Только HTTPS, порт 2096** — `http://89.127.199.6/sub` устарел (статический файл `user1` от 2026-06-02):

| Устройство | URL подписки |
|------------|----------------|
| ПК (`Рабочий_комп`) | `https://89.127.199.6:2096/sub/da882d0a-9b2e-41fb-9dc9-1b8e3b4af99a` |
| Pi 5 (`pi5`) | `https://89.127.199.6:2096/sub/f6330ce2-9029-49be-9c81-e0b7dacd89d8` |
| Pi 3 (`pi3`) | `https://89.127.199.6:2096/sub/431ad87a-00d9-4a5a-bd9c-347764239516` |
| Kali (`kali`) | `https://89.127.199.6:2096/sub/1395d99e-7121-450f-8e65-816bc6645183` |
| Телефон (`phone`) | `https://89.127.199.6:2096/sub/c57ca873-642f-440f-954a-d9ae3ad87718` |
| Keenetic (`keenetic`) | `https://89.127.199.6:2096/sub/81171323-908e-4618-ae8b-7e76091155cc` |
| Аня (`Аня`) | `https://89.127.199.6:2096/sub/16e97685-4d04-4b13-b29c-e10f893468ed` |
| Кемал (`Кемал`) | `https://89.127.199.6:2096/sub/b8d19300-d118-41fd-a8b7-f0a9b0341085` |
| Владимир (`Владимир`) | `https://89.127.199.6:2096/sub/9a690f7c-0051-4544-8be4-d83a7578a471` |
| Apple TV (`appletv`) | `https://89.127.199.6:2096/sub/5101960c-1fb4-4c31-b125-fff1e6e29a6b` |

Клиент для Apple TV: приложение **Happ — Proxy Utility for TV** (VLESS Reality). Импорт подписки по URL выше.

При первом импорте подписки на ПК подтверди самоподписанный сертификат (или импортируй ссылку `vless://` из панели 3x-ui).

## 4. WireGuard (Keenetic роутер)

| Параметр | Значение |
|----------|----------|
| Endpoint | `89.127.199.6:51820` |
| Server Public Key | `xGoa2gU8PBE2C5umnuYCjPOz156nCv+xmFzpmVvk2QM=` |
| Client Private Key | `iOYkV6SmM/JLGaAScXDAzfOnqDNS23vK76PIAKbQBUM=` |
| Client Address | `10.90.90.2/32` |
| DNS | `8.8.8.8` |
| AllowedIPs | `0.0.0.0/0` |
| Keepalive | `25` |

Конфиг для импорта в Keenetic:
```ini
[Interface]
PrivateKey = iOYkV6SmM/JLGaAScXDAzfOnqDNS23vK76PIAKbQBUM=
Address = 10.90.90.2/32
DNS = 8.8.8.8

[Peer]
PublicKey = xGoa2gU8PBE2C5umnuYCjPOz156nCv+xmFzpmVvk2QM=
Endpoint = 89.127.199.6:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

Настройка: Веб-интерфейс Keenetic → Интернет → Другие подключения → WireGuard → Добавить туннель → Импорт из QR-кода.

Управление WireGuard на сервере:
```bash
ssh vpn1 "sudo wg show"            # статус туннеля
ssh vpn1 "sudo systemctl restart wg-quick@wg0"  # перезапуск
```

## 5. Настройка SSH-ключа

Если у тебя ещё нет SSH-ключа, следуй инструкциям для своей ОС:

### macOS / Linux

```bash
# Создать ключ
ssh-keygen -t ed25519 -C "vpnuser@vpn1" -f ~/.ssh/vpn1_key -N ""

# Отправить публичный ключ на сервер
scp ~/.ssh/vpn1_key.pub vpnuser@89.127.199.6:~/

# Установить права
chmod 600 ~/.ssh/vpn1_key

# Добавить в SSH-конфиг
cat >> ~/.ssh/config << 'SSHEOF'

Host vpn1
    HostName 89.127.199.6
    User vpnuser
    IdentityFile ~/.ssh/vpn1_key
    IdentitiesOnly yes
SSHEOF

# Проверить подключение
ssh vpn1
```

### Windows (PowerShell)

```powershell
# Создать ключ
ssh-keygen -t ed25519 -C "vpnuser@vpn1" -f $HOME\.ssh\vpn1_key -N '""'

# Отправить публичный ключ на сервер
scp $HOME\.ssh\vpn1_key.pub vpnuser@89.127.199.6:~/

# Добавить в SSH-конфиг
Add-Content $HOME\.ssh\config @"

Host vpn1
    HostName 89.127.199.6
    User vpnuser
    IdentityFile ~/.ssh/vpn1_key
    IdentitiesOnly yes
"@

# Проверить подключение
ssh vpn1
```

## 6. Частые команды

```bash
ssh vpn1                           # подключиться к серверу
ssh vpn1 "sudo x-ui status"        # статус панели
ssh vpn1 "sudo x-ui restart"       # перезапустить панель
ssh vpn1 "sudo x-ui log"           # логи
ssh vpn1 "sudo x-ui setting -reset" # сбросить пароль панели
```

Добавить нового VPN-клиента:
Открой панель (напрямую или через SSH-туннель) → Inbounds → ... → Add Client → отправь ссылку/QR.

Проверить список клиентов через API:
```bash
curl -k -H "Authorization: Bearer <API_TOKEN>" \
  "https://89.127.199.6:37702/q6omE9HRd1U9d6t4XH/panel/api/clients/list"
```

## 7. Статус безопасности

| Параметр | Статус |
|----------|--------|
| Вход под root | Отключён |
| Вход по паролю (root) | Отключён |
| Файрвол UFW | Включён (SSH, 80, 443, 2096, 51820/udp, 37702/tcp) |
| fail2ban | Удалён (по запросу) |
| Усиление ядра | Частично включено (sysctl) |
| BBR | Включён |
| ICMP (ping) | Требует отдельной проверки |

## 8. Решение проблем

| Проблема | Решение |
|----------|---------|
| Hiddify «ошибка подключения» при добавлении подписки | Просрочен SSL на `:2096` / `:37702` — на VPS: `sudo openssl req -x509 -nodes -days 825 -newkey rsa:2048 -keyout /root/cert/ip/privkey.pem -out /root/cert/ip/fullchain.pem -subj '/CN=89.127.199.6'` && `sudo systemctl restart x-ui` |
| Connection refused | `ssh vpn1 "sudo x-ui status"` — перезапусти если остановлен |
| Permission denied (publickey) | Проверь путь и права ключа: `ls -la ~/.ssh/vpn1_key` |
| Host key verification failed | `ssh-keygen -R 89.127.199.6` и переподключись |
| Панель недоступна | Используй SSH-туннель (см. раздел 2) |
| VPN не подключается | Неверный SNI или сервер лежит — проверь `sudo x-ui log` |
| Забыл пароль панели | `ssh vpn1 "sudo x-ui setting -reset"` |

## 9. Инструкции для Claude Code

Этот раздел для автоматической настройки через Claude Code на твоём ноутбуке.
Скопируй всё ниже и вставь в Claude Code на ноутбуке.

---

**ЗАДАЧА: Настроить SSH-ключ и завершить настройку безопасности VPN-сервера**

Данные сервера:
- SERVER_IP: 89.127.199.6
- USERNAME: vpnuser
- PASSWORD: vJUkjnVPSzJGiy6Rgqch
- NICKNAME: vpn1

Шаги:

**Часть А: Установка sshpass (нужен для автоматической передачи пароля)**
1. Определи ОС и установи sshpass:
   - macOS: `brew install hudochenkov/sshpass/sshpass`
   - Linux (Debian/Ubuntu): `sudo apt install -y sshpass`

**Часть Б: Создание и установка SSH-ключа**
2. Создай SSH-ключ: `ssh-keygen -t ed25519 -C "vpnuser@vpn1" -f ~/.ssh/vpn1_key -N ""`
3. Установи ключ на сервере одной командой:
   ```
   sshpass -p 'vJUkjnVPSzJGiy6Rgqch' ssh-copy-id -i ~/.ssh/vpn1_key.pub -o StrictHostKeyChecking=accept-new vpnuser@89.127.199.6
   ```
4. Проверь вход по ключу (должен работать БЕЗ пароля):
   ```
   ssh -i ~/.ssh/vpn1_key vpnuser@89.127.199.6 "echo 'SSH key OK'"
   ```
5. Добавь SSH-конфиг:
   ```
   cat >> ~/.ssh/config << 'EOF'

   Host vpn1
       HostName 89.127.199.6
       User vpnuser
       IdentityFile ~/.ssh/vpn1_key
       IdentitiesOnly yes
   EOF
   ```
6. Проверь подключение через конфиг: `ssh vpn1 "echo 'Config OK'"`

**Часть В: Финальная защита сервера (fail2ban + блокировка пароля)**
7. Установи fail2ban:
   ```
   ssh vpn1 'sudo apt install -y fail2ban && sudo tee /etc/fail2ban/jail.local << JAILEOF
   [DEFAULT]
   bantime = 1h
   findtime = 10m
   maxretry = 5

   [sshd]
   enabled = true
   port = ssh
   filter = sshd
   logpath = /var/log/auth.log
   maxretry = 3
   bantime = 24h
   JAILEOF
   sudo systemctl enable fail2ban && sudo systemctl restart fail2ban'
   ```
8. Заблокируй парольный вход и root:
   ```
   ssh vpn1 'sudo sed -i "s/^#\?PermitRootLogin.*/PermitRootLogin no/" /etc/ssh/sshd_config && sudo sed -i "s/^#\?PasswordAuthentication.*/PasswordAuthentication no/" /etc/ssh/sshd_config && sudo systemctl restart sshd'
   ```
9. Проверь что SSH-ключ всё ещё работает после блокировки:
   ```
   ssh vpn1 "grep -E 'PermitRootLogin|PasswordAuthentication' /etc/ssh/sshd_config && sudo systemctl status fail2ban --no-pager && echo 'Сервер полностью защищён!'"
   ```
10. Скажи пользователю: "Готово! SSH-ключ настроен, fail2ban установлен, парольный вход отключён. Подключайся: ssh vpn1"
