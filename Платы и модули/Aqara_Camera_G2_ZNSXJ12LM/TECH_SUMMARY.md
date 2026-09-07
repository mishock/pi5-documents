# Aqara Camera G2 (Gateway Edition) — ZNSXJ12LM

Модель с фото пользователя: **智能摄像机 G2 (网关版)** · **ZNSXJ12LM** · 5 V ⎓ 1 A.

## Интеграция в Home Assistant (Pi 3)

Рекомендуемый путь — **HomeKit Controller** (локально, без telnet/RTSP-хака).

### Подготовка (один раз)

1. Подключите камеру к Wi‑Fi **AiNET** через приложение **Aqara Home** (QR на дне корпуса).
2. Если камера уже в **Apple Home** — удалите её оттуда (HomeKit = один контроллер).
3. Найдите **HomeKit-код** (формат `XXX-XX-XXX`): наклейка / Aqara Home → устройство → HomeKit.

### Автоматическое добавление на Pi 3

```bash
cd ~/Raspberry_Pi_3_HomePortable
bash scripts/add-aqara-g2-camera-ha.sh XXX-XX-XXX
# при нескольких HomeKit-устройствах:
AQARA_G2_IP=10.0.20.xx bash scripts/add-aqara-g2-camera-ha.sh XXX-XX-XXX
```

Только поиск в сети:

```bash
docker cp scripts/discover_aqara_g2_ha.py homeassistant:/tmp/discover_aqara.py
docker exec homeassistant python3 /tmp/discover_aqara.py --all
```

### Результат в HA

- Сущность: `camera.aqara_g2` (или по `--title`)
- Зона: **Гараж** (`garazh`) — дашборд «Обзор» (original-states)
- Проверка: `http://10.0.20.56:8123` → Настройки → Устройства → Aqara G2

### Если камера не находится

- Камера не в той же подсети, что Pi 3 (`10.0.20.0/24`).
- Камера занята Apple Home — снять pairing в приложении «Дом».
- Режим приложения: для G2 иногда нужен **Aqara Home**, не Mi Home.
- Альтернатива (сложнее): Aqara Gateway + telnet + HACS — см. [AqaraCameraHubfw](https://github.com/niceboygithub/AqaraCameraHubfw).

## Связанное

- HA Pi 3: `Проекты/Raspberry_Pi_3_HomePortable/`
- Hub M1S в той же сети: `10.0.20.30` (DHCP-бронь), отдельная интеграция для Zigbee-датчиков.
