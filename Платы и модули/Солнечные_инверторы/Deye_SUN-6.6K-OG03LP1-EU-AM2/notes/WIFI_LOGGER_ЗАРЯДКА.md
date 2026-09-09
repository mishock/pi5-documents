# Wi‑Fi logger «Зарядка» — сеть и доступ

**Инвертор:** Deye SUN-6.6K-OG03LP1-EU-AM2 · SN `2607250740`  
**Wi‑Fi stick:** SN `1538281644` · hostname `1538281644` · MAC `b4:89:70:09:2f:20`

## Сеть (2026-09-09)

| Параметр | Значение |
|----------|----------|
| SSID | `ELTAVR_` (офис Guest / Bridge1) |
| IP | `10.1.30.81` (DHCP reservation на роутере) |
| Прошивка logger | `V1.4.05_R01D.0B2_M5434_00000008` |
| Режим Wi‑Fi | `APSTA` · STA RSSI ~68–74% |
| Веб logger | `http://10.1.30.81:80` |
| Modbus/Solarman TCP | `:8899` — **closed** (после POST-настройки тоже) |
| Remote server A/B | **Not connected** (поля `status_a` / `status_b` пустые) |
| AP (резерв) | `AP_1538281644` · `10.10.100.254` |

## Вход в веб `:80`

| Поле | Значение |
|------|----------|
| Логin | `admin` |
| Пароль | на наклейке **PWD** на Wi‑Fi-модуле (не `admin` / не `12345678`) |

Проверено с Pi 5: Basic auth `admin` + PWD с наклейки → **HTTP 200**.

## Скрытая настройка (Solarman)

`http://10.1.30.81/config_hide.html` → iframe `hide_set_edit.html`:

- Working mode → **Data collection** (`yz_tmode=cmd`)
- Internal server → **TCP-Server**, port **8899**
- UART → **9600 8N1**

Автоскрипт (нужен `LOGGER_PASS`):

```bash
LOGGER_PASS='…' bash Платы\ и\ модули/Солнечные_инверторы/Deye_SUN-6.6K-OG03LP1-EU-AM2/scripts/configure-logger-zaryadka.sh
```

После каждого `do_cmd.html` — подтверждение `success.html` + `HF_PROCESS_CMD=RESTART`.

## WAN

Проброс офисного роутера: `91.215.61.76:8899` → `10.1.30.81:8899` (`ip static tcp ISP 8899 …`) — DNAT есть; **8899 на logger не слушает**, с WAN тоже **connection refused**.

## Роутер (XKeen / Guest)

Инвертор в Guest с политикой **Policy0 (XKeen)**. На роутере:

- `host b4:89:70:09:2f:20 permit` — снять через CLI **не удалось** (`no … permit` / `no host` — ошибка Keenetic)
- **2026-09-09:** добавлен `host b4:89:70:09:2f:20 conform` (сохранено)

Если облако не поднимется — убрать `permit` через веб-админку Keenetic или временно отключить Policy0 для Guest.

## Solarman / pysolarman

- Serial для V5: **`1538281644`** (SN Wi‑Fi-модуля, не SN инвертора)
- `pysolarmanv5` на Pi 5 не установлен (PEP 668); ставить в venv/Docker при необходимости

## Диагностика

```bash
curl -u admin:$LOGGER_PASS http://10.1.30.81:80/status.html | grep -E 'webdata_sn|status_a|cover_ver'
timeout 3 bash -c 'echo >/dev/tcp/10.1.30.81/8899' && echo OPEN || echo CLOSED
ping -c1 10.1.30.81
```

## Фото наклеек

Сохранены пользователем 2026-09-09 (WIFI SN / PWD / SN инвертора).

## Что ещё проверить

1. **Бренд инвертора** в `config_hide.html` (поле `inv_tp`) — в HTML vars пустые; выбрать Deye вручную в браузере.
2. **Инвертор включён** и отдаёт мощность (сейчас `webdata_now_p` пусто; SN `2607250740` читается).
3. **Guest + XKeen** — маршрут облака Solarman/Deye через VPN может блокировать Server A.
