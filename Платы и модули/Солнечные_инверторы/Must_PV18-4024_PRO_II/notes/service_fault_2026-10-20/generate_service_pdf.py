#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Пересборка PDF описания неисправности для СЦ (MUST PV18-4024 PRO II)."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

OUT = Path(__file__).resolve().parent
PDF = OUT / "Описание_неисправности_Must_PV18-4024_PRO_II_для_СЦ.pdf"
LABEL = OUT / "label_for_pdf.jpg"

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
BLUE, DARK, GRAY = HexColor("#0069b4"), HexColor("#1a1a1a"), HexColor("#444444")
LIGHT, WARN = HexColor("#f3f7fb"), HexColor("#8a1f1f")

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVu", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(18 * mm, 10 * mm, "НПП «Эльтавр» · Симферополь · support@eltavr.ru")
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"стр. {doc.page}")
    canvas.restoreState()

def main() -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="HMain", fontName="DejaVuBold", fontSize=13.5, leading=17, textColor=BLUE, alignment=TA_CENTER, spaceAfter=3 * mm))
    styles.add(ParagraphStyle(name="Sub", fontName="DejaVu", fontSize=9.5, leading=12, textColor=GRAY, alignment=TA_CENTER, spaceAfter=2.5 * mm))
    styles.add(ParagraphStyle(name="Sec", fontName="DejaVuBold", fontSize=10.5, leading=13, textColor=BLUE, spaceBefore=3 * mm, spaceAfter=1.5 * mm))
    styles.add(ParagraphStyle(name="BodyRU", fontName="DejaVu", fontSize=9.5, leading=12.5, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=1.5 * mm))
    styles.add(ParagraphStyle(name="BulletRU", fontName="DejaVu", fontSize=9.5, leading=12.5, textColor=DARK, leftIndent=3 * mm, spaceAfter=0.7 * mm))
    styles.add(ParagraphStyle(name="Cell", fontName="DejaVu", fontSize=9, leading=11.5, textColor=DARK))
    styles.add(ParagraphStyle(name="CellB", fontName="DejaVuBold", fontSize=9, leading=11.5, textColor=DARK))
    styles.add(ParagraphStyle(name="Warn", fontName="DejaVuBold", fontSize=9.5, leading=12.5, textColor=WARN, spaceBefore=1.5 * mm, spaceAfter=1.5 * mm))
    styles.add(ParagraphStyle(name="Cap", fontName="DejaVu", fontSize=8, leading=10, textColor=GRAY, alignment=TA_CENTER, spaceBefore=1 * mm))

    def meta_table(rows):
        data = [[Paragraph(a, styles["CellB"]), Paragraph(b, styles["Cell"])] for a, b in rows]
        t = Table(data, colWidths=[48 * mm, 124 * mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.5, BLUE),
            ("INNERGRID", (0, 0), (-1, -1), 0.3, HexColor("#c5d6e8")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
            ("TOPPADDING", (0, 0), (-1, -1), 2.2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ]))
        return t

    story = [
        Paragraph("ОПИСАНИЕ НЕИСПРАВНОСТИ ДЛЯ СЕРВИСНОГО ЦЕНТРА", styles["HMain"]),
        Paragraph("Инвертор MUST PV18-4024 PRO II — отправка в ремонт / диагностику", styles["Sub"]),
        HRFlowable(width="100%", thickness=1.1, color=BLUE, spaceAfter=2.5 * mm),
        meta_table([
            ("Дата обращения", "20.10.2026"),
            ("Отправитель", "НПП «Эльтавр», г. Симферополь"),
            ("Контакт (сервис)", "support@eltavr.ru · +7 978 878-59-76 · eltavr.ru"),
            ("Видео неисправности", "IMG_3651.MOV (в той же папке Google Drive)"),
        ]),
        Paragraph("1. Идентификация устройства", styles["Sec"]),
        meta_table([
            ("Бренд / серия", "MUST · PV1800 PRO II"),
            ("Модель (MD)", "PV18-4024 PRO II"),
            ("Серийный номер (S/N)", "009000001400028"),
            ("Номинал", "4000 VA / 4000 W · АКБ 24 VDC · AC 230 V"),
            ("PV (паспорт)", "до 5000 W · MPPT 90–430 V · Voc 500 V"),
            ("Заряд от сети", "до 80 A (24 VDC)"),
            ("Производитель", "Must Energy (Guangdong) Technology Co., Ltd., China"),
            ("Импортёр (РФ, шильдик)", "ООО «ЭНВЕК», г. Москва"),
        ]),
        Paragraph("2. Схема подключения на момент отказа", styles["Sec"]),
        Paragraph(
            "К инвертору были подключены <b>только</b>: сеть 230&nbsp;V (AC input), нагрузка (AC output) и аккумуляторная батарея 24&nbsp;V. "
            "<b>Солнечные панели (PV) не подключались. Генератор не подключался.</b>",
            styles["BodyRU"],
        ),
        Paragraph("3. Симптомы неисправности", styles["Sec"]),
    ]
    for b in [
        "Устройство <b>перестало работать</b> / не выходит в нормальный режим работы.",
        "При попытке включения <b>мигает дисплей (LCD)</b>, полноценный старт отсутствует.",
        "Из корпуса ощущается <b>явный запах гари</b> (признак внутреннего повреждения электроники).",
        "Инвертор <b>не стартует и не включается</b> в рабочий режим.",
        "Связь с ПК / мониторинг по USB <b>не устанавливается</b> (USB Serial на хосте есть, ответа MCU по Modbus нет).",
    ]:
        story.append(Paragraph("• " + b, styles["BulletRU"]))
    story.append(Paragraph(
        "Предварительная оценка: вероятна внутренняя неисправность платы управления и/или силовой части "
        "(мигание LCD без старта + запах гари + отсутствие ответа по USB/Modbus).",
        styles["Warn"],
    ))
    story.append(Paragraph("4. Что проверено на месте (до отправки)", styles["Sec"]))
    for b in [
        "USB-адаптер CH340 (1a86:7523) на хосте определяется штатно, порт свободен.",
        "Опрос Modbus RTU по USB (разные baud / slave) — <b>ответа нет</b>; спонтанного трафика нет.",
        "USB — только мониторинг; старт инвертора должен идти от АКБ 24&nbsp;V и клавиши ON/OFF.",
        "Внешние повреждения корпуса как основная причина отказа не выявлены.",
    ]:
        story.append(Paragraph("• " + b, styles["BulletRU"]))
    story += [
        Paragraph("5. Просьба к сервисному центру", styles["Sec"]),
        Paragraph(
            "Просим провести диагностику и ремонт: установить и устранить причину отсутствия старта, мигания LCD, "
            "запаха гари и отсутствия связи по USB/Modbus. По результатам — заключение о характере дефекта "
            "(гарантийный / негарантийный), перечень заменённых узлов и возможность возврата в работоспособное состояние.",
            styles["BodyRU"],
        ),
        Paragraph("6. Комплектность отправки", styles["Sec"]),
    ]
    for b in [
        "Инвертор MUST PV18-4024 PRO II (S/N 009000001400028) в упаковке.",
        "Документация / инструкция (вложена в коробку).",
        "Видеофиксация: IMG_3651.MOV (озвученное описание симптомов).",
        "Настоящее описание неисправности (этот PDF).",
    ]:
        story.append(Paragraph("• " + b, styles["BulletRU"]))
    story.append(Paragraph("7. Фото шильдика с упаковки", styles["Sec"]))
    if LABEL.exists():
        pil = PILImage.open(LABEL)
        w_mm, h_mm = 95.0, 95.0 * pil.height / pil.width
        if h_mm > 70:
            h_mm = 70.0
            w_mm = h_mm * pil.width / pil.height
        img = RLImage(str(LABEL), width=w_mm * mm, height=h_mm * mm)
        img.hAlign = "CENTER"
        story.append(img)
    story += [
        Paragraph("Шильдик на упаковке: модель PV18-4024 PRO II, S/N 009000001400028.", styles["Cap"]),
        Spacer(1, 2.5 * mm),
        HRFlowable(width="100%", thickness=0.6, color=BLUE, spaceAfter=1.5 * mm),
        Paragraph(
            "Краткое резюме для приёмки: MUST PV18-4024 PRO II, S/N 009000001400028 — не стартует, мигает LCD, "
            "запах гари внутри, USB/Modbus молчит. Подключались только сеть, нагрузка и АКБ 24&nbsp;V (без PV и генератора).",
            styles["BodyRU"],
        ),
    ]
    doc = SimpleDocTemplate(
        str(PDF), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=14 * mm, bottomMargin=16 * mm,
        title="Описание неисправности MUST PV18-4024 PRO II",
        author="НПП «Эльтавр», г. Симферополь",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(PDF)

if __name__ == "__main__":
    main()
