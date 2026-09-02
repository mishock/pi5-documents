# PB MCU01 H503A — распиновка для GEM BMC эмулятора

Плата: **PB MCU01 H503A**, MCU **STM32H503CBT6**, USB Type-C.

## Разъём GEM X3 (на плате эмулятора)

Штатный жгут e6 втыкается в **male header** на месте BMC X3:

| | P/N |
|---|-----|
| Header на плате эмулятора | **TE AMPSEAL 776262-1** (14POS, vertical, COD 1) |
| Plug на жгуте (уже на машине) | **776273-1** |

Footprint — по TE drawing **ENG_CD_776262_B** (THT, sealed flange). Нумерация пинов 1–14 как в `../../WIRING_REFERENCE.md` § BMC X3.

> Проверьте распиновку по [документации PB-Embedded](https://pb-embedded.ru/products/tproduct/466974915232-pbmcu01h503a) и silkscreen вашей ревизии.

## CAN (FDCAN1 + SN65HVD230)

Контроллер — **встроенный FDCAN1** (PB7/PB8). На шину GEM — **модуль-трансивер**, не MCP2515.

### Модуль: SN65HVD230 (VP230), 3.3 V

| Модуль SN65 | PB MCU01 | GEM BMC X3 |
|-------------|----------|------------|
| 3V3 | **3.3** | — |
| GND | **GND** | GND (кузов) |
| CTX | **B7** | — |
| CRX | **B8** | — |
| CANH | — | **p14** (Yw) |
| CANL | — | **p13** (Gn) |

- Скорость: **250 kbit/s** (в прошивке).
- **120 Ω** на модуле (121): на машине терминатор обычно уже есть — **не дублировать**, если модуль в жгуте, а не на конце короткого кабеля.
- Справочник того же чипа: `Платы и модули/RS485_CAN_HAT/`.
- Плата PB: `Платы и модули/PB_MCU01_H503A/PINOUT.md`.

## Реле (→ BMC X3)

| Функция | BMC X3 | GPIO | По умолчанию | При interlock (зарядка) |
|---------|--------|------|--------------|-------------------------|
| K5 DC/DC Relay #1 | p4 | **PA0** | ON | **ON** (SM) |
| K12 DC/DC Relay #2 | p5 | **PA1** | ON | **ON** (SM) |
| VCM +12 V | p12 | **PA2** | ON | **ON** (SM) |
| **K7 Charger Relay** | **p3** | **PA4** | OFF | **ON** (SM) |

`RELAY_ACTIVE_LOW = 0` в `include/hw_pins.h` — модули с опто, active-high.

## Interlock

| Сигнал | BMC X3 | GPIO |
|--------|--------|------|
| Aux NO (зарядник) | p11 | **PA3** INPUT |

+12 V от зарядника → оптопара → PA3. HIGH = зарядник воткнут → **K7 включается**, K5/K12/VCM **остаются ON**.

## Индикация / UART

| | Pin |
|---|-----|
| LED | **PC13** |
| UART TX | PA9 |
| UART RX | PA10 |

## Питание

3.3 V логика STM32; реле/оптопары — по схеме GEM (12 V BMC, не подавать на GPIO напрямую).

## Прошивка

- ST-Link: SWDIO/SWCLK/GND/3V3
- DFU: USB-C + BOOT0
