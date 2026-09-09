# Keenetic — два роутера (управление с Pi 5)

Доступ с Pi 5 проверен **2026-06-05**. Управление: **RCI** (JSON), **SSH** (CLI), telnet (`:23`).

## Электроцех (домашняя сеть / ELEKTRO_)

| Параметр | Значение |
|----------|----------|
| URL | http://10.10.0.1/ |
| Логин | `admin` |
| Пароль | `admin` |
| Модель | Keenetic Start (KN-1111) |
| Hostname | `Keenetic-6726` |
| Прошивка | KeeneticOS 4.3.7 |
| Wi‑Fi SSID | `ELEKTRO_` (LAN `10.1.30.0/24`) |

## Офис

| Параметр | Значение |
|----------|----------|
| URL | http://192.168.1.1/ |
| Логин | `admin` |
| Пароль | `Mishock24` |
| Модель | Keenetic Giga (KN-1012) |
| Hostname | `Keenetic-5824` |
| LAN | `192.168.1.0/24` |

## API (с Pi 5)

Авторизация KeeneticOS: `GET /auth` → challenge → `POST /auth` с хешем пароля (MD5 внутренний + SHA-256).

```bash
# Пример: версия прошивки (электроцех)
python3 Документы/.cursor/scripts/keenetic-rci.py electro '{"show":{"version":{}}}'
python3 Документы/.cursor/scripts/keenetic-rci.py office '{"show":{"ip":{"hotspot":{}}}}'
```

Скрипт: `Документы/.cursor/scripts/keenetic-rci.py` (`electro` | `office`).

## SSH (CLI) — для агента и ручных правок

| Задача | Инструмент |
|--------|------------|
| Читать статус, JSON | `keenetic-rci.py` |
| Команды CLI, маршруты, `ip static`, save | `keenetic-ssh.sh` |

```bash
# Маршруты, NAT, save конфига
bash Документы/.cursor/scripts/keenetic-ssh.sh electro 'show ip route'
bash Документы/.cursor/scripts/keenetic-ssh.sh office 'show ip hotspot'
bash Документы/.cursor/scripts/keenetic-ssh.sh electro save 'ip static tcp ISP 80 10.1.30.126 80'

# Интерактивная сессия (config)>
bash Документы/.cursor/scripts/keenetic-ssh.sh electro shell
```

SSH-алиасы в `~/.ssh/config`: `keenetic-electro`, `keenetic-electro-vpn`, `keenetic-office` (пароль — в скрипте или вручную через `sshpass`).

## SSH (вход)

Включено **2026-06-05** (`service ssh` + `system configuration save` на обоих). Уровень доступа: **private** (только из локальных сетей, не с интернета).

| Роутер | Адрес | Логин / пароль |
|--------|-------|----------------|
| Электроцех | `10.10.0.1`, `10.1.30.1` | `admin` / `admin` |
| Офис | `192.168.1.1` | `admin` / `Mishock24` |

```bash
ssh admin@10.10.0.1      # электроцех (с Pi 5 / ELEKTRO / ELEKTRO_)
ssh admin@192.168.1.1      # офис (с ELTAVR или через 192.168.1.2 как шлюз)
```

Telnet (`:23`) — запасной вариант. SSH включён `service ssh`, уровень **private** (не с интернета).

## Офис (ELTAVR) → сайт ЭЛЬТАВР на Pi 5

Сайт (Next.js, Docker `eltavr_nginx`) на Pi 5: **порт 80**, IP в электроцехе `10.1.30.126`.

С офисного Wi‑Fi **ELTAVR** (`192.168.1.0/24`) открывать:

| URL | Как работает |
|-----|----------------|
| **http://192.168.1.2/** | Проброс на электро-роутере: `ip static tcp ISP 80 → 10.1.30.126:80` (основной, без конфликта подсетей) |
| **http://10.1.30.126/** | Статический маршрут на офисном роутере: `10.1.30.126/32 via 192.168.1.2` |

Настроено **2026-06-05** (LAN/офис), дополнено **2026-06-10** (интернет):

- **Электроцех:** WAN (`192.168.1.2`): `80`, `443`, `8080`, `8000`, **`22` (SSH, MAC wlan0)**, **`8766`**, **`8767`** → Pi `10.1.30.126`; **`9443` → Pi `8443`** (BMS HTTPS; на Pi только TLS).
- **Офис (белый IP `91.215.61.76`):** `80`, `443`, `8080`, `8000`, **`22` (SSH)**, **`8766`**, **`8767`** → `192.168.1.2`; **`9443` → `192.168.1.2:9443`** (далее на Pi `:8443`).
- **Офис `:8443`** — админка Keenetic (`ip http ssl port 8443`), **не** пробрасывать на Pi.
- **Офис:** маршруты `10.1.30.126/32` и `10.10.0.0/24` через `192.168.1.2`.
- **Pi 5 UFW + DOCKER-USER:** `22/80/443/8080/8000/8443/8766/8767` публично. Восстановление UFW: `Документы/.cursor/scripts/restore-pi5-ufw.sh` (авто: `install-pi5-restore-ufw.sh`). Docker: `fix-pi5-ports-ufw-docker.sh`.

## SSH Malinka 5 (интернет)

Проброс **22** на Pi `10.1.30.126` (wlan0 MAC `2c:cf:67:78:b4:55` на электроцехе).

| Откуда | Команда |
|--------|---------|
| LAN | `ssh pi@10.1.30.126` |
| WAN | `ssh pi@91.215.61.76` |
| Алиас | `ssh pi5-wan` |

Установка/проверка: `bash Документы/.cursor/scripts/install-pi5-ssh-wan-portforward.sh`

**Безопасность:** на WAN открыт стандартный `:22`; вход по ключу `~/.ssh/id_ed25519`. Парольный вход на sshd сейчас включён.

## Nexus Control (интернет)

Проброс **8766** (Nexus AI / PWA / Siri API) на Pi `10.1.30.126`:

| Откуда | URL |
|--------|-----|
| LAN | `http://10.1.30.126:8766/app/` |
| WAN | `http://91.215.61.76:8766/app/` |
| Siri CPU | `http://91.215.61.76:8766/api/pi/cpu` |
| Voice | `http://91.215.61.76:8766/api/voice?text=uptime` |

Проброс **8767** (Cursor Agent HTTPS / голос PWA):

| Откуда | URL |
|--------|-----|
| LAN | `https://10.1.30.126:8767/app/` |
| WAN | `https://91.215.61.76:8767/app/` |
| CA | `https://91.215.61.76:8767/Eltavr-Cursor-Agent-CA.crt` |

Установка/проверка: `bash Документы/.cursor/scripts/install-nexus-wan-portforward.sh`

**Безопасность:** API без пароля — не публикуйте URL широко; для удалённого доступа предпочтительнее **NetBird** (`100.102.159.200:8766`).

Проверка с интернета (`91.215.61.76`): `:80`, `:443`, `:8080`, `:8000` → **200**; BMS — **`https://91.215.61.76:9443/`** (не `http` и не `:8443` с WAN — занят админкой офисного роутера).

**DNS:** `eltavr.ru` пока на старом хостинге (`31.31.196.221`) — для переключения на Pi: A-запись → `91.215.61.76`.

## Офис: VLESS (XKeen) только для ELTAVR_VPN

Настроено **2026-06-05** на офисном Giga (KN-1012), Entware на встроенном `storage:/` (~100 МБ).

| Параметр | Значение |
|----------|----------|
| Wi‑Fi VPN | `ELTAVR_VPN` (сегмент `Guest` / `Bridge1`, `10.1.30.0/24`) |
| Основной Wi‑Fi | `ELTAVR` (`Home` / `Bridge0`, `192.168.1.0/24`) — **без** VPN |
| Политика | `Policy0` → описание **XKeen**; `ip hotspot policy Guest Policy0` |
| Маршрут политики | `permit global ISP` (не WireGuard) |
| Entware SSH | `root@192.168.1.1:222`, пароль по умолчанию `keenetic` |
| Xray | v26.3.27, конфиги `/opt/etc/xray/configs/` |
| VPS / клиент | `keenetic` на `89.127.199.6:443` (VLESS Reality, 3x-ui) |
| Автозапуск | `S99xkeen`, задержка `xkeen -d 30` |

Админка роутера перенесена с `:443` на **`:8443`** (HTTP — **`:8080`**), иначе XKeen не стартует.

Проверка с телефона/ПК на **ELTAVR_** (VPN): внешний IP **`89.127.199.6`**. На **ELTAVR** (Home) — IP провайдера.

**Важно (фикс 2026-06-05):** без исключения локальных подсетей DNS на `10.1.30.1` уходил в туннель — интернет не работал. Файлы: `/opt/etc/xkeen/ip_exclude.lst` (`10.1.30.0/24`, `192.168.0.0/16`, …), `/opt/etc/xray/configs/05_routing.json` (private → `direct`).

```bash
# Entware: статус XKeen
sshpass -p 'keenetic' ssh -p 222 root@192.168.1.1 'xkeen -cp; pidof xray'

# Перезапуск после правки конфигов
sshpass -p 'keenetic' ssh -p 222 root@192.168.1.1 'xkeen -restart'
```

Установка XKeen (неинтерактивно, Stable + Xray latest):

```bash
printf '1\n1\n1\n0\n0\n0\n1\n' | xkeen -i
```

## Джарвис (Pi 5) — доступ без блокировок

Белый список IP агента на обоих Keenetic (2026-09-09):

| IP | Назначение |
|----|------------|
| `10.1.30.126` | Pi 5 (ELEKTRO_, wlan0) |
| `100.102.159.200` | NetBird Pi 5 |

**Офис (`192.168.1.1`):**

- ACL `jarvis-agent` — полный permit для IP агента (все протоколы, все сегменты).
- `no isolate-private` — ACL Keenetic **не** обходит `isolate-private`; без этого Pi не достучится до Guest (инвертор «Зарядка» `10.1.30.81`).
- ACL `guest-isolation` на `Bridge1 out` — Guest **не** ходит в Home (`192.168.1.0/24`, `10.10.0.0/24`); интернет для гостей сохраняется.
- `ip hotspot host 2c:cf:67:78:b4:55 permit` — Pi в белом списке hotspot.

**Электроцех (`10.10.0.1`):**

- ACL `jarvis-agent` на Bridge0/1/2 и ISP.
- `ip route 10.1.30.81 192.168.1.1 ISP` — офисный Guest (перекрытие подсети `10.1.30.0/24`).

**Pi 5:** systemd `jarvis-agent-routes.service` — host-маршруты к устройствам только на офисном Guest (список: `/etc/jarvis-agent-routes/office-guest.conf`).

**Инвертор «Зарядка»** (`b4:89:70:09:2f:20` → `10.1.30.81`):

| WAN | → | Назначение |
|-----|---|------------|
| `:8081` | `:80` | веб logger (ручная калибровка; WAN `:80` занят сайтом) |
| `:8899` | `:8899` | Solarman TCP |

Hotspot: `permit` + `conform` (2026-09-09). Снять `permit` из CLI не выходит — только Web UI Keenetic.

Установка / проверка:

```bash
bash Документы/.cursor/scripts/install-jarvis-agent-router-access.sh
ping -c1 10.1.30.81   # инвертор «Зарядка» (офис Guest)
ping -c1 192.168.1.1  # офисный роутер
```

## Связанные файлы

- RCI: `Документы/.cursor/scripts/keenetic-rci.py`
- SSH CLI: `Документы/.cursor/scripts/keenetic-ssh.sh`
- Джарвис ACL: `Документы/.cursor/scripts/install-jarvis-agent-router-access.sh`
- WireGuard (электроцех → VPS): `Документы/keenetic-wg.conf`
- VPN-методичка: `Документы/vpn-guide.md`
