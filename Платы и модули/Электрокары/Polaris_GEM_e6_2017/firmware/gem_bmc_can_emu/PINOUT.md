# Подключение: Arduino Nano — эмулятор BMC (A2)

**CAN:** 250 kbit/s · **29-bit extended** · **Дискрет:** X3 p3 / p4 / p5 / p11 / p12

**Разъём X3 на плате:** TE AMPSEAL **776262-1** (14POS header, COD 1) — жгут **776273-1**. См. `../../WIRING_REFERENCE.md` § BMC.

## Nano ↔ MCP2515 (SPI)

| MCP2515 | Nano | |
|---------|------|--|
| VCC | 5V | |
| GND | GND | общая масса с GEM |
| CS | **D10** | |
| SO | D12 | |
| SI | D11 | |
| SCK | D13 | |

| CANH / CANL | GEM BMC X3 |
|-------------|------------|
| CANH | **p14** |
| CANL | **p13** |

## Реле (вкл. при старте Arduino, см. `hw_pins.h`)

Эмуляция выходов **BMC X3** на жгут A2. Тип реле на стенде — на ваш выбор; ниже логика прошивки.

| Nano | Реле стенда | GEM / Breakout | BMC X3 | Цепь |
|------|-------------|----------------|--------|------|
| **D3** | **#1 K5** | DC/DC Converter Relay #1 | **p4** Bl | **DC/DC Enable GND** — масса катушки K5 в fuse box |
| **D4** | **#2 K12** | Fuse Box DC/DC Relay #2 | **p5** Bn/Wh | **DC/DC Converter Relay GND** — масса K12 |
| **D5** | **#3 VCM** | A1 Vehicle Control Module | **p12** Rd/Gn | **V-Out +12 V** на VCM X1:p16 (Ignition/Charger ON) |
| **D7** | **#4 K7** | Delta-Q Charger Relay | **p3** Bn/Wh | **Charger Relay GND** — +48 V на зарядник |

**Логика (SM §8.28):** K5/K12/VCM **ON** всегда; **K7 ON** только при interlock (зарядник воткнут).

### Как вешать на машину

**p4 / p5 (K5, K12):** штатный BMC тянет линию на **массу**. Реле/ключ — **low-side**: COM → провод X3, NO → **GND** кузова (или транзистор open-collector).

**p12 (VCM):** штатный BMC подаёт **+12 V**. Реле — **high-side** или отдельное автомобильное реле: COM → **+12 V Constant** (F1/splice), NO → провод **X3:p12** → VCM.

**Питание катушек реле D3/D4:** только от 5 V Nano (модули 1-канальные с оптопарой). Силовые контакты — автомotive 12 V / GND.

По умолчанию `RELAY_ACTIVE_LOW = 1` (типовой синий модуль: **LOW = реле ON**).

## Вход interlock (BMC X3 p11)

| Nano | Сигнал | BMC X3 |
|------|--------|--------|
| **D6** | Charger interlock IN | **p11** Pk — Aux NO (+12 V от зарядника, когда EVSE воткнут) |

**Обязательно:** не подавать +12 V на D6 напрямую. Схема: оптопара или делитель (например 10 kΩ / 4.7 kΩ) + защитный диод.  
На входе **HIGH** = interlock активен → **K7 (D7) включается**, K5/K12/VCM **остаются ON**.

Прошивка опрашивает D6 каждые 100 ms, смену состояния пишет в Serial.

## Настройки в коде

| Файл | Что менять |
|------|------------|
| `hw_pins.h` | пины D3–D7, `RELAY_ACTIVE_LOW`, кварц MCP2515 |
| `gem_bmc_can_emu.ino` | только при смене CAN-расписания |

```cpp
#define MCP2515_CLOCK   MCP_8MHZ   // или MCP_16MHZ
#define CAN_BITRATE     CAN_250KBPS
```

## Питание

- Nano: 5 V стабильный БП или USB (на машине — DC/DC 12→5 V).
- Общий **GND** Nano и кузова GEM.
- **Не** подключать 48 V пакета к Nano.

## Проверка

1. Подача 5 V на Nano → **щёлк** три реле (K5, K12, VCM), через 3 с — CAN TX, LED D13 1 Гц.
2. KEY ON — приборка без P1824/P1827 (при исправном CAN).
3. Interlock: +12 V на оптопару D6 → Serial `Interlock p11: ON → K7 ON`, щёлк **K7**.

См. `../../WIRING_REFERENCE.md` § BMC X3, `../../notes/BMC_EMULATOR_PLAN.md`.
