# GEM e6 BMC эмулятор — PB MCU01 H503A (STM32H503CB)

Порт алгоритма **v4.2** с Pi/Arduino на плату **PB MCU01 H503A** (STM32H503, USB Type-C).

## Как работает прошивка

Заменяет **мёртвый BMC (A2, SA=0xF3)** на GEM e6: VCM и приборка получают те же CAN-кадры и дискретные сигналы X3, что ждут от штатного блока.

### Что делает после включения

1. **Старт (~0.5 с)** — инициализация GPIO, **FDCAN1** @ 250 kbit/s (extended ID), UART 115200.
2. **Реле** — K5/K12/VCM (**PA0–PA2**) сразу **ON** (эмуляция «ключ / зарядка», SM §8.28).
3. **CAN TX** — непрерывная отправка кадров BMC; **RX не нужен** (только передатчик).
4. **Interlock** — каждые 100 ms опрос **PA3** (X3 p11): если зарядник воткнут (+12 V) → **K7 ON** (PA4, X3 p3); иначе K7 OFF. K5/K12/VCM **не гасятся**.
5. **LED PC13** — мигает раз в секунду (жизнь + успешный DM1); при сбое FDCAN — быстрое мигание.

### CAN — алгоритм v4 (подтверждён на машине)

Источник истины: `scripts/can-bmc-emulate.py`, эталон `notes/BMC_CAN_EMULATOR_v4_OK.md`.

| CAN ID | Период | Содержание |
|--------|--------|------------|
| `0CFF0EF3` | 10 ms | 9 heartbeat-кадров по кругу (из лога рабочей e6) |
| `0CFF0FF3` | 100 ms | Charger counter: byte3 +0xAF/0xB0, 10 кадров = 1 с, byte7 = XOR |
| `0CFF10F3` | 100 ms | Статичный payload |
| `0CFF11F3` | 100 ms | BMC counter byte6 += 0x10, byte7 = XOR |
| `0CFF12F3` | 100 ms | byte6 от 0x8F, byte7 = 0xFF − byte6 |
| `18FECAF3` | 1 s | DM1 без ошибок (`00 FF 00 00 00 00 FF FF`) |

Без правильных **счётчиков и XOR** VCM выставляет **P1824** (BMC) и **P1827** (charger).

### Структура кода

| Файл | Роль |
|------|------|
| `src/main.cpp` | Цикл по таймерам, реле, interlock |
| `src/bmc_can_gen.cpp` | Генератор payload v4 (`BmcGenerator`) |
| `src/fdcan_gem.cpp` | FDCAN1 HAL: PB7 TX, PB8 RX → SN65HVD230 |
| `include/hw_pins.h` | PA0–PA4 реле, PA3 interlock, PC13 LED |

### Чего прошивка пока не делает

- Не читает CAN с шины (VCM/MCU не эмулируются).
- Нет Key In (p10), шунта −↔V−, LED зарядника (p1/p6) — см. `notes/BMC_EMULATOR_PLAN.md`.
- CAN в режиме зарядки тот же v4 (отдельный charging-профиль — позже).

### Ожидаемый результат на машине

При KEY ON, CAN на X3 p13/p14: **приборка OK, DTC P1824/P1827 нет** (проверено с Pi v4 на VIN `5ACA6AGA3H0002115`).

## Отличия от Arduino Nano

| | Nano + MCP2515 | PB MCU01 H503A |
|---|----------------|----------------|
| CAN | MCP2515 SPI | **FDCAN1** + модуль **SN65HVD230 (VP230) 3.3 V** |
| Трансивер | на модуле MCP2515 | **отдельный SN65HVD230**: CTX→**B7**, CRX→**B8** |
| Прошивка | avr-gcc | PlatformIO + Arduino STM32 |
| Заливка | USB-UART | ST-Link SWD или **USB DFU** |

## Сборка

```bash
bash firmware/gem_bmc_can_emu_h503/scripts/build.sh
```

Артефакт: `releases/gem_bmc_can_emu_h503_v4.2.bin` (копируется автоматически после сборки).

Требуется `platformio` (`pip install platformio`).

## Прошивка

**ST-Link (рекомендуется):** SWD на плате →

```bash
bash firmware/gem_bmc_can_emu_h503/scripts/flash.sh stlink
```

**DFU (USB-C):** BOOT0=1, Reset → `flash.sh dfu`

## CAN

- **Железо:** модуль **SN65HVD230** (VP230), 3.3 V — см. **`PINOUT.md`**
- **Не использовать MCP2515** с этой прошивкой (FDCAN уже в MCU)
- 250 kbit/s, extended ID, SA=0xF3
- Кадры: `0CFF0EF3` (10 ms), `0CFF0FF3/10/11/12` (100 ms), `18FECAF3` (1 s)
- Логика = `scripts/can-bmc-emulate.py` v4

## Реле и interlock (SM §8.28–8.30)

| Реле | Старт | Interlock (зарядник) |
|------|-------|----------------------|
| K5, K12, VCM (p4/p5/p12) | **ON** | **ON** |
| K7 (p3, зарядник +48 V) | OFF | **ON** |

См. `PINOUT.md`.

## Отладка

UART **115200** на PA9/PA10 (если выведены на USB-UART мост платы).

## Связанные файлы

- `notes/BMC_CAN_EMULATOR_v4_OK.md` — эталон алгоритма
- `firmware/gem_bmc_can_emu/` — вариант для Arduino Nano
