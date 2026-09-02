# Прошивки — Polaris GEM e6 2017

| Папка | Платформа | Описание |
|-------|-----------|----------|
| **`gem_bmc_can_emu_h503/`** | **PB MCU01 H503A** (STM32H503, FDCAN) | BMC CAN-эмулятор v4.2 — **рекомендуется** |
| **`gem_bmc_can_emu/`** | Arduino Nano + MCP2515 | BMC CAN-эмулятор v4.2 (legacy) |

## PB MCU01 H503A (STM32H503)

```bash
bash firmware/gem_bmc_can_emu_h503/scripts/build.sh
bash firmware/gem_bmc_can_emu_h503/scripts/flash.sh stlink   # или dfu
```

См. `firmware/gem_bmc_can_emu_h503/README.md`, `PINOUT.md`.

**CAN:** модуль **SN65HVD230 (VP230) 3.3 V** → B7/B8; MCP2515 не нужен.

Как работает: `firmware/gem_bmc_can_emu_h503/README.md` § «Как работает прошивка».

## Arduino Nano + MCP2515

```bash
bash firmware/gem_bmc_can_emu/scripts/build.sh
ARDUINO_PORT=/dev/ttyUSB0 bash firmware/gem_bmc_can_emu/scripts/flash.sh
```

См. `firmware/gem_bmc_can_emu/README.md`, `notes/BMC_CAN_EMULATOR_v4_OK.md`.
