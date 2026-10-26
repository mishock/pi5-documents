# Электрокары (LSV / golf / people-mover)

Общая папка документации по **лёгким электромобилям**: Polaris GEM, E-Z-GO, Club Car и т.п.

Новую модель — **сразу отдельная подпапка** здесь, не в корень `Платы и модули/`.

## Содержимое

| Папка | Что |
|-------|-----|
| [`Polaris_GEM_e6_2017/`](Polaris_GEM_e6_2017/) | Polaris GEM e6, VIN `5ACA6AGA3H0002115`, MFD 2017. SM Waev **9940314 R02**. Ошибки: [`FAULT_CODES.md`](Polaris_GEM_e6_2017/FAULT_CODES.md). |
| [`EZGO_Club_Car/`](EZGO_Club_Car/) | E-Z-GO ST Shuttle: SM **612342**, Parts **620365**, ST400 **614281**; схемы [`WIRING_REFERENCE.md`](EZGO_Club_Car/WIRING_REFERENCE.md), ошибки [`FAULT_CODES.md`](EZGO_Club_Car/FAULT_CODES.md). |
| [`Curtis_Controller/`](Curtis_Controller/) | Curtis AC 12xx: как читать красный+жёлтый LED, код **47** HPD и др. [`FAULT_CODES.md`](Curtis_Controller/FAULT_CODES.md). Обновлено 2026-10-26. |
| *(позже)* `Club_Car_<модель>_<год>/` | Отдельная подпапка, когда появится документация Club Car. |

## Как добавлять следующую машину

1. Создать `Платы и модули/Электрокары/<Бренд>_<Модель>_<год>/`.
2. Стандарт модуля: `downloads/`, `pic/`, `PINOUT.md`, `TECH_SUMMARY.md`, `source_url.txt`, …
3. Дописать строку в эту таблицу.

## Источники (шпаргалка)

- **GEM / Waev:** https://brandfolder.com/waev/service-support  
- **GEM owners:** https://www.gemcar.com/owners-manuals/  
- **E-Z-GO:** https://www.ezgo.com/  
- **Club Car:** https://www.clubcar.com/  
