# Audi A4 B5 (личный автомобиль)

**VIN:** WAUZZZ8DZXA016797 · **госномер:** Y921OE · **регион:** 93  
**Год:** 1999 · **двигатель:** 1.6 AHL (100 л.с.) · **КПП:** МКПП (завод была АКПП 01N)

## Документы

| Файл | Содержание |
|------|------------|
| [FILTERS_AND_WIPERS.md](FILTERS_AND_WIPERS.md) | Фильтры (масло, воздух, салон, топливо) + щётки — OEM и аналоги |
| [../Audi_A4_B5_ECU_AHL_3B0_907_557_B/TECH_SUMMARY.md](../Audi_A4_B5_ECU_AHL_3B0_907_557_B/TECH_SUMMARY.md) | ЭБУ SIMOS 3B0 907 557 B, K-line, CAN |
| [../../Проекты/audi_bc_pico/README.md](../../Проекты/audi_bc_pico/README.md) | Борткомпьютер на Pico |

## Диагностика

- **K-line** (не CAN OBD): ELM327 WiFi часто не тянет KW1281; надёжно — **KKL FTDI** + kw1281test.
- ЭБУ @ **9600** baud; адрес **0x01**.
