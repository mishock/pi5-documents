# Pi 3 ↔ JK AKB-4S-230 BLE — корневая причина

**Обновлено:** 2026-10-31

## Итог

| Вопрос | Ответ |
|--------|--------|
| BMS виден в scan? | Да, `AKB-4S-230` / `C8:47:80:53:0F:B6` |
| Connect бывает? | Да (Bumble HCI USER) |
| Стабильный кадр **0x02** (ячейки/SOC) для HA? | **Пока нет** на встроенном BT Pi3 |
| Эталон 0x02 | Pi5 + bleak, 2026-10-30 (`notes/live_ble_2026-10-30.json`) |

## Причина (железо + эфир)

1. Pi 3: **BCM43438A1**, BT по **UART**, одна антенна с Wi‑Fi.
2. В `dmesg`: `Bluetooth: hci0: Frame reassembly failed (-84)` — порча HCI при нагрузке Wi‑Fi.
3. После CONNECT линк живёт **~1–3 с**, затем HCI **reason 8** (supervision timeout) или **62**.
4. Кадр JK ~300 байт не успевает дойти целиком; иногда приходят обрывки `0x01`/`0x03`.
5. Write на handle **0x12 (FFE1)** даёт мусор `AT\r\n`; полезный write — **FFE2 @0x10**.

## Что нельзя делать

- **`nmcli radio wifi off`** в гараже — Wi‑Fi = основной интернет/NetBird.  
  Правило: `.cursor/rules/garage-wifi-never-off.mdc`.

## Что сделано в скриптах (на будущее)

- `bms-tools/jk4s_bumble_probe.py` — быстрый 0x96, listen-only после JK-заголовка, без discover, write @0x10.
- `bms-tools/jk4s_run_once.sh` — только `txpower↓`, Wi‑Fi radio всегда on, restore bluetooth.
- Таймер `jk4s-ble-logger.timer` на Pi3 — **disabled**, пока линк не стабилен.

## Надёжные варианты дальше

1. **USB BLE-донгл** на Pi3 (обход Cypress UART) — предпочтительно.
2. Реже: опрос с хоста с нормальным BLE (как Pi5), если батарея в зоне досягаемости.
3. Закрыть JK App на телефоне + кнопка на BMS перед опросом.
