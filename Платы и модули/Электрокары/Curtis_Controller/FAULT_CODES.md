# Curtis — мигающие коды ошибок (красный + жёлтый LED)

**Обновлено:** 2026-11-23

Семейство AC-контроллеров **1232 / 1234 / 1236 / 1238** (E / SE и аналоги с двумя LED).  
Русскоязычной официальной таблицы Curtis **нет** — ниже перевод по официальному списку для модели **1238** (тот же ряд, что 1236).

В боте ЭЛЬТАВР: **Сервис → Ошибки Curtis** (`Проекты/telegram_bot/knowledge/service/curtis_fault_codes.json` + PDF для выдачи).

| Источник | Ссылка |
|----------|--------|
| Официальный переводчик (EN) | https://faultcodes.curtisinstruments.com/ |
| Полный список 1238 | https://faultcodes.curtisinstruments.com/list.php?action=Submit&mc=1238 |
| Полный список 1236SE | https://faultcodes.curtisinstruments.com/list.php?action=Submit&mc=1236SE |
| HPEVS troubleshooting (EN текст) | `notes/hpevs_troubleshooting_acos26_extract.txt` |
| Краткая таблица Roxie (EN PDF) | `downloads/fault_codes/Curtis_Fault_Code_Roxie.pdf` |
| RICO 1236E quick guide (EN PDF) | `downloads/fault_codes/Curtis_RICO_1236E_Troubleshooting.pdf` |
| Сводка Varelec (PT/EN) | https://www.varelec.pt/alarmes/curtis/1236-1238/ |
| **PDF полной таблицы RU** | [`downloads/fault_codes/Curtis_FAULT_CODES_RU.pdf`](downloads/fault_codes/Curtis_FAULT_CODES_RU.pdf) (**74 строки**, 3 стр., ред. 2026-10-30) |

Точная формулировка зависит от модели и ОС — при споре сверять шильду с faultcodes.curtisinstruments.com.

Пересборка PDF: `python3 scripts/generate_fault_codes_pdf.py` → `downloads/fault_codes/`

---

## Как читать мигание (важно)

Это **один** двузначный код, не два отдельных:

| Шаг | Красный | Жёлтый | Смысл |
|-----|---------|--------|--------|
| 1 | **1** вспышка | затем **N** вспышек | первая цифра = **N** |
| 2 | **2** вспышки | затем **M** вспышек | вторая цифра = **M** |

**Код = NM.**

Пример: `1× красный → 4× жёлтый → 2× красный → 7× жёлтый` = **47**, а не «14 и 27».  
Пример кода **23**: 1× красный → 2× жёлтый → 2× красный → 3× жёлтый.

| LED | Состояние |
|-----|-----------|
| Только жёлтый мигает | Нормальная работа |
| Оба горят постоянно | Flash program mode |
| Красный постоянно | Watchdog / нет ПО — цикл KSI, при необходимости прошить ПО |
| Оба погашены | Нет питания / АКБ / тяжёлое повреждение |

Сброс многих ошибок: выключить/включить ключ (**цикл KSI**). Если не уходит — выключить KSI, снять 35-pin, проверить коррозию/обжимки.

---

## Полная таблица (RU)

Полный список семейства OS26/OS30: **все используемые коды**, варианты одного номера (17/18/31/32/47) и OEM **51–67** по отдельности.  
PDF: [`downloads/fault_codes/Curtis_FAULT_CODES_RU.pdf`](downloads/fault_codes/Curtis_FAULT_CODES_RU.pdf) (**74 строки**, 3 стр., ред. 2026-10-30).

| Код | Имя (EN / RU) | Суть / что смотреть |
|-----|---------------|---------------------|
| **12** | Controller Overcurrent / Перегруз по току | КЗ фаз U/V/W; параметры мотора; дефект; шум энкодера |
| **13** | Current Sensor Fault / Датчик тока | Утечка фазы на раму; дефект контроллера |
| **14** | Precharge Failed / Предзаряд | B+ не зарядился до KSI; нагрузка на B+ |
| **15** | Severe Undertemp / Сильный недогрев | Радиатор < −40 °C |
| **16** | Severe Overtemp / Сильный перегрев | Радиатор > ~95 °C |
| **17** | Severe B+ Undervoltage / Понижение B+ | Конденсаторы ниже Severe UV; АКБ / предохранитель / контактор |
| **17** | Severe KSI Undervoltage / Понижение KSI | KSI < ~8,4 В; предохранитель / обрыв ключа |
| **18** | Severe B+ Overvoltage / Повышение B+ | Severe OV при рекуперации / отключении АКБ |
| **18** | Severe KSI Overvoltage / Повышение KSI | Слишком высокое на pin 1; блок контактора |
| **22** | Overtemp Cutback / Снижение по температуре | Радиатор > ~85 °C — снижен момент |
| **23** | B+ Undervoltage Cutback / Понижение АКБ | Часто норма: АКБ разряжены |
| **24** | B+ Overvoltage Cutback / Повышение при regen | Только в рекуперации |
| **25** | +5V Supply Failure / Питание +5 В | Нагрузка pin 26; вне ±10 % |
| **26** | DigOut 6 Open/Short / Выход 6 | Перегруз (часто pin 19), > ~1 А |
| **27** | DigOut 7 Open/Short / Выход 7 | Перегруз (часто pin 20), > ~1 А |
| **28** | Motor Temp Hot Cutback / Мотор горячий | ≥ Temperature Hot; ток режется |
| **29** | Motor Temp Sensor Fault / Датчик t° мотора | Термистор / pin 8 |
| **31** | Main Open/Short / Главный контактор | Драйвер pin 6 при Main Enable = On |
| **31** | Coil1 Driver Open/Short / Катушка 1 | Драйвер pin 6 при Main Enable = Off |
| **32** | EMBrake Open/Short / EM-тормоз | Драйвер pin 5 при EM Brake Type > 0 |
| **32** | Coil2 Driver Open/Short / Катушка 2 | Драйвер pin 5 при EM Brake Type = 0 |
| **33** | Coil3 Open/Short / Катушка 3 | Драйвер pin 4 |
| **34** | Coil4 Open/Short / Катушка 4 | Драйвер pin 3 |
| **35** | Proportional Driver Open/Short | Драйвер pin 2 |
| **36** | Encoder Fault / Энкодер | Отказ энкодера / проводка |
| **37** | Motor Open / Обрыв фазы | Обрыв U/V/W |
| **38** | Main Contactor Welded / Контактор сварился | Залипание / обрыв U/V / лишний ток на B+ |
| **39** | Main Contactor Did Not Close | Не закрылся / окисление / B+ fuse |
| **41** | Throttle Wiper High / Педаль высокая | Pin 16 выше порога |
| **42** | Throttle Wiper Low / Педаль низкая | Pin 16 ниже порога |
| **43** | Pot2 Wiper High | Pin 17 высокий |
| **44** | Pot2 Wiper Low | Pin 17 низкий |
| **45** | Pot Low Overcurrent | Pot Low > ~10 мА (pin 18) |
| **46** | EEPROM Failure | Ошибка записи EEPROM |
| **47** | HPD / Sequencing / Неверная последовательность | Порядок KSI→interlock→направление→газ; см. ниже |
| **47** | Emer Rev HPD / После Emergency Reverse | После EMR не нейтраль газ/F-R/interlock |
| **49** | Parameter Change Fault / Смена параметра | Нужен цикл KSI |
| **51** … **67** | OEM Fault 1…17 / Ошибки OEM | По одной на номер; смотреть документацию OEM / VCL |
| **68** | VCL Run Time Error | Runtime VCL |
| **69** | Ext Supply Out of Range | Ток +5/+12 В вне порогов |
| **71** | OS General | Внутренняя ошибка ОС |
| **72** | PDO Timeout | Таймаут CAN PDO |
| **73** | Stall Detected / Стол | Нет движения по энкодеру → LOS |
| **74** | Fault On Other Traction | Dual Drive |
| **75** | Dual Severe Fault | Dual Drive |
| **77** | Supervisor Fault | Расхождение измерений / шум входов |
| **78** | Supervisor Incompatible | Несовместимость Supervisor |
| **82** | Bad Calibrations | Плохая калибровка |
| **83** | Driver Supply | Сбой питания драйверов |
| **87** | Motor Characterization Fault | Сбой характеризации (код 0–9) |
| **88** | Encoder Pulse Count Fault | Encoder Steps ≠ реальному |
| **89** | Motor Type Fault | Motor_Type вне диапазона |
| **91** | VCL/OS Mismatch | Несовпадение VCL и ОС |
| **92** | EM Brake Failed to Set | Тормоз не удержал |
| **93** | Encoder LOS | LOS после 36 или 73 |
| **94** | EMR Rev Timeout | Таймаут / залип EMR |
| **98** | Illegal Model Number | ПО ≠ железо |
| **99** | Parameter Mismatch | Dual Drive / feedback |

**Незанятые номера** (на LED не используются): 19, 20, 21, 30, 40, 48, 50, 70, 76, 79–81, 84–86, 90, 95–97.

---

## Запрос 2026-10-26: паттерн «14 и 27»

Наблюдение: 1 красный + 4 жёлтых, потом 2 красных + 7 жёлтых.

| Неверно | Верно |
|---------|--------|
| коды **14** и **27** | один код **47** |

### Код **47** — HPD / Sequencing Fault

**На LCD программера:** High Pedal Disable / Sequencing Fault

**Суть:** неправильная последовательность входов ключ (KSI) → interlock → направление → газ; или педаль уже вжата при включении.

**Эффект:** газ отключён (Shutdown Throttle).

**Что проверить:**
1. Отпустить педаль газа, нейтраль направления, выключить/включить ключ (цикл KSI).
2. Порядок: ключ ON → interlock/сиденье → направление F/R → только потом газ.
3. Проводка/концевики: KSI, interlock, F/R, throttle.
4. После Emergency Reverse — вернуть газ, направление и interlock в нейтраль.

---

## Частые коды рядом

| Код | Кратко |
|-----|--------|
| 23 | Undervoltage cutback — АКБ сели / высокое сопротивление |
| 38 | Main Contactor Welded |
| 39 | Main Contactor Did Not Close |
| 41 / 42 | Throttle wiper high / low |
| 47 | HPD / Sequencing (см. выше) |
| 36 / 73 / 93 | Энкодер / столл / LOS |
