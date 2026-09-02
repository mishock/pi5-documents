# BMC CAN-эмулятор v4 — подтверждено на машине

**Дата:** 2026-09-02  
**Машина:** неисправная GEM e6, VIN `5ACA6AGA3H0002115` (мёртвый/отсутствующий BMC на шине)  
**Стенд:** Raspberry Pi 5 + **RS485 CAN HAT**, `can0` @ **250 kbit/s**, extended ID  
**Скрипт:** `scripts/can-bmc-emulate.py` (**v4**)  
**Эталон:** `logs/20260902-123304_working_key_off.log` (рабочая e6, АКБ ✓, без DTC)

---

## Результат (подтверждено пользователем)

- Приборка **загорается**, **DTC нет**
- Ушли **P1824 / 524273** (BMC Status Counter) и **P1827 / 524237** (Charger Status Counter)
- CAN-only эмуляция SA=**0xF3** достаточна для **этого этапа** (ключ ON, диагностика на стоянке)

---

## Алгоритм v4 (рабочий)

| CAN ID | Период | Counter / checksum |
|--------|--------|-------------------|
| `0CFF0EF3` | 10 ms | Replay 9 уник. heartbeat из эталона (после 25 с лога) |
| `0CFF0FF3` | 100 ms | byte3 += **0xAF** (1-й шаг) / **0xB0** далее; **10 одинаковых кадров = 1 с**; byte4 −1 каждые 3 шага; byte6=0x7F; **byte7 = XOR(0..6)** |
| `0CFF10F3` | 100 ms | Steady: `C8 2F 8F FF FF 00 C7 AE` |
| `0CFF11F3` | 100 ms | base `42 C0 52 FD FF 46`; **byte6 += 0x10**; **byte7 = XOR(0..6)** |
| `0CFF12F3` | 100 ms | **byte6 от 0x8F**, +=0x10; **byte7 = 0xFF − byte6** |
| `18FECAF3` | 1 s | DM1 чистый: `00 FF 00 00 00 00 FF FF` |

Старт charger counter: byte3=**0xE7**, byte4=**0xF8**.

---

## Запуск

```bash
# CAN TX (не listen-only!)
bash "Платы и модули/Электрокары/Polaris_GEM_e6_2017/scripts/can-setup.sh" --bitrate 250000

# Эмулятор (tmux — при обрыве связи)
ai-tmux run gem-bmc-emu 'python3 "Платы и модули/Электрокары/Polaris_GEM_e6_2017/scripts/can-bmc-emulate.py"'

# Проверка без шины
python3 …/scripts/can-bmc-emulate.py --dry-run

# Стоп
tmux kill-session -t job-gem-bmc-emu
pkill -f can-bmc-emulate.py
```

---

## Ошибки v1–v3 (что ломало VCM)

1. Статичный payload / ручной byte0 → counter fault  
2. Replay всех кадров каждые 100 ms без удержания → P1827  
3. Charger counter **−0xB0** вместо **+0xAF/+0xB0**  
4. `0CFF12F3` старт с **0xBF** вместо **0x8F**

---

## Дальше (не CAN)

- **X3 p12 V-Out +12 V** → полное пробуждение VCM (SA=0xEF) на шине  
- Реле p3/p4/p5, шунт −↔V−, INA226 для живого SOC  
- Долгосрочно: полная state machine X3

## Дискрет X3 v4.2 (реле, SM §8.28)

| Реле | X3 | Старт | Interlock (p11) |
|------|-----|-------|-----------------|
| K5 DC/DC Enable | p4 | **ON** | **ON** |
| K12 DC/DC Relay | p5 | **ON** | **ON** |
| VCM V-Out | p12 | **ON** | **ON** |
| K7 Charger | p3 | OFF | **ON** |

Прошивки: `firmware/gem_bmc_can_emu/` (Nano D3–D7), `firmware/gem_bmc_can_emu_h503/` (H503 PA0–PA4).

## PB MCU01 H503A — STM32H503 + FDCAN (2026-09-02)

Автономная прошивка **v4.2** на **PB MCU01 H503A** (встроенный FDCAN, внешний **SN65HVD230**):

**`firmware/gem_bmc_can_emu_h503/`** — PlatformIO, `src/main.cpp`, `PINOUT.md`, `scripts/build.sh`, `scripts/flash.sh`.

```bash
bash "Платы и модули/Электрокары/Polaris_GEM_e6_2017/firmware/gem_bmc_can_emu_h503/scripts/build.sh"
bash "…/scripts/flash.sh stlink"   # ST-Link SWD
```

Сборка проверена на Pi 5 (2026-09-02): **26976 B Flash**, **1388 B RAM** → `releases/gem_bmc_can_emu_h503_v4.2.bin`.

## Arduino Nano + MCP2515 (legacy)

**`firmware/gem_bmc_can_emu/`** — `gem_bmc_can_emu.ino`, `PINOUT.md`, `scripts/build.sh`, `scripts/flash.sh`.

См. `notes/CAN_BUS_MAP.md`.
