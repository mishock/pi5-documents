# GEM e6 — BMC CAN-эмулятор (Arduino Nano + MCP2515)

Прошивка повторяет **алгоритм v4**, подтверждённый на неисправной GEM e6 с Pi 5 (`../scripts/can-bmc-emulate.py`).

**Папка модуля:** `Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/`

## Назначение

| | |
|---|---|
| **Что это** | Автономный CAN-передатчик, имитирующий **BMC (SA=0xF3)** на шине GEM |
| **Что делает** | CAN SA=0xF3 (v4) + реле **K5/K12/VCM** (ON) + **K7** по interlock (p11) |
| **Железо** | **Arduino Nano** + **MCP2515/TJA1050** + **4× реле** |
| **Связано** | `../notes/BMC_CAN_EMULATOR_v4_OK.md` |

## Подключение

См. **`PINOUT.md`**.

**Кварц MCP2515:** чаще **8 МГц** (`MCP_8MHZ` в `.ino`); если не шлёт — `MCP_16MHZ`.

## Сборка и заливка

```bash
bash "Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/scripts/build.sh"

ARDUINO_PORT=/dev/ttyUSB0 bash "…/firmware/gem_bmc_can_emu/scripts/flash.sh"
```

Абсолютные пути на Pi 5:

```bash
bash /home/pi/Documents/Платы\ и\ модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/scripts/build.sh
ARDUINO_PORT=/dev/ttyUSB0 bash /home/pi/Documents/Платы\ и\ модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu/scripts/flash.sh
```

После заливки: **3 с пауза**, затем TX; LED D13 мигает раз в секунду.

## Дискрет X3 (v4.2, SM §8.28)

| Выход/вход | Пин Nano | Эмуляция BMC | Старт | Interlock |
|------------|----------|--------------|-------|-----------|
| Реле K5 | D3 | X3 **p4** | ON | ON |
| Реле K12 | D4 | X3 **p5** | ON | ON |
| Реле VCM | D5 | X3 **p12** | ON | ON |
| **Реле K7** | **D7** | X3 **p3** | OFF | **ON** |
| Interlock IN | D6 | X3 **p11** | — | +12 V от зарядника |

## CAN-трафик (v4)

| ID | Период |
|----|--------|
| `0CFF0EF3` | 10 ms |
| `0CFF0FF3` | 100 ms (counter +1 с) |
| `0CFF10F3` | 100 ms |
| `0CFF11F3` | 100 ms |
| `0CFF12F3` | 100 ms |
| `18FECAF3` | 1 s |

Логика: `bmc_can_gen.h`.

## Ограничения

- Штатный BMC отключить от CAN и X3 (или заменить жгут на стенд).
- p10 (Key In), шунт −↔V− — следующие этапы (`../notes/BMC_EMULATOR_PLAN.md`).
