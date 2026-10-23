# TECH_SUMMARY — Deye SUN-20K-SG05LP3-EU-SM2

Трёхфазный гибридный инвертор 48 В, 20 кВт. Штатная пара Deye — **2× RW-F16** (№1 → BAT1, №2 → BAT2, Parallel Mode 2).

## Ключевые параметры

| Параметр | Значение |
|----------|----------|
| Модель | SUN-20K-SG05LP3-EU-SM2 |
| Мощность | 20 кВт |
| Батарея | 40–60 В, Li-ion / свинец |
| Макс. I заряд/разряд (инвертор) | 350 А |
| Входов батареи | 2 (BAT1, BAT2) |
| BMS | Self-adaption to BMS |
| AC автомат Grid/Load | 100 А |
| DC кабель батареи | 3/0 AWG (70 мм²), 24,5 Н·м |

## Совместимость с RW-F16

- **Approved Battery List DY-LV48-0127:** RW-F16, CAN, **Lithium Mode 00**.
- При PCS >8 кВт — **Parallel Mode 2** на стороне батарей.
- Лимит тока инвертора **350 А**, но с 2× RW-F16 потолок **250 А** (встроенные автоматы 2×125 А); в меню **240 А**.
- С 3× RW-F16 (№1+№2 → BAT1, №3 → BAT2) потолок **350 А** (инвертор), в меню **300 А**, 942 Ah.
- PDF: `../Deye_RW-F16/generated/Deye_SUN-20K_2xRW-F16_Installation_Setup_RU.pdf`, `../Deye_RW-F16/generated/Deye_SUN-20K_3xRW-F16_Installation_Setup_RU.pdf`.

## Deye Cloud (DL1000B-WIFI logger)

- Мониторинг и удалённые настройки — **Deye Cloud** (https://www.deyecloud.com), **не Solarman Pro** (DL1000B в Solarman не добавляется).
- Logger шлёт данные в дата-центр **EMEA** (eu1.deyecloud.com).
- **Приложение Deye Cloud у клиента — только через VPN** (exit **не США** / не AMER). Без VPN телефон попадает в **AMER (Соединённые Штаты)** — станция офлайн или не видна. VPN → регион **EMEA/APAC** в приложении.
- **Подключение DL1000B к Wi‑Fi дома:** (1) телефон → Wi‑Fi **stick** (SSID = **SN** на наклейке), пароль — **PWD** с наклейки logger (**не** пароль домашней сети); (2) браузер **`http://10.10.100.254`** → **Wireless Settings** → SSID и пароль **домашнего роутера** (2,4 GHz). Либо Wi‑Fi Configuration в приложении Deye Cloud.
- Эталон объекта: `Проекты/Мирное_Никольская_10/notes/БЛОКНОТ.md` (раздел Deye Cloud).

## Автозапуск ДГУ (TSS)

**2026-10-23:** 2× SUN-20K + TSS TQc 22TS ST (16 кВт). Чеклист и PDF:

- `notes/АВТОЗАПУСК_ГЕНЕРАТОР_TSS_2xDeye20K.md`
- `generated/АВТОЗАПУСК_TSS_TQc22_2xDeye20K.pdf`
- ДГУ: `Платы и модули/Дизельные_генераторы/TSS_TQc_22TS_ST_АД-16С-Т400/`

## Документация (локально)

`downloads/` — User Manual EN, Datasheet, Energy Storage Solution.  
`generated/` — PDF-инструкции для монтажника (RU) — раздел **5.6 Удалённый доступ (Deye Cloud)**.

## Проверка

```bash
ls "Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/downloads/"
python3 "Платы и модули/Солнечные_инверторы/Deye_SUN-20K-SG05LP3-EU-SM2/scripts/generate_rwf16_system_pdf.py"
```
