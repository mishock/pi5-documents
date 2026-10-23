#!/usr/bin/env python3
"""PDF: автозапуск TSS TQc 22TS ST ↔ 2× Deye SUN-20K. Дата 2026-10-23."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated" / "АВТОЗАПУСК_TSS_TQc22_2xDeye20K.pdf"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

YELLOW = colors.Color(1, 0.95, 0.6)


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("DejaVu", FONT))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_B))


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Heading1"],
            fontName="DejaVu-Bold",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="DejaVu-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="DejaVu",
            fontSize=8.5,
            leading=11,
            spaceAfter=3,
            alignment=TA_LEFT,
        ),
        "warn": ParagraphStyle(
            "warn",
            parent=base["Normal"],
            fontName="DejaVu-Bold",
            fontSize=8.5,
            leading=11,
            spaceAfter=4,
            textColor=colors.HexColor("#8B0000"),
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["Normal"],
            fontName="DejaVu",
            fontSize=7.5,
            leading=9.5,
            spaceAfter=2,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName="DejaVu",
            fontSize=7.5,
            leading=9.5,
        ),
        "cellb": ParagraphStyle(
            "cellb",
            parent=base["Normal"],
            fontName="DejaVu-Bold",
            fontSize=7.5,
            leading=9.5,
        ),
    }


def P(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text.replace("\n", "<br/>"), style)


def make_table(rows: list[list], col_widths: list[float], yellow_rows: set[int] | None = None) -> Table:
    yellow_rows = yellow_rows or set()
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F4F6F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]
    for r in yellow_rows:
        style_cmds.append(("BACKGROUND", (0, r), (-1, r), YELLOW))
    t.setStyle(TableStyle(style_cmds))
    return t


def build() -> None:
    register_fonts()
    s = styles()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.2 * cm,
        rightMargin=1.2 * cm,
        topMargin=1.0 * cm,
        bottomMargin=1.0 * cm,
    )
    story: list = []

    story.append(P("Deye SUN-20K ×2 ↔ TSS TQc 22TS ST — автозапуск ДГУ", s["title"]))
    story.append(
        P(
            "Версия 2026-10-23. Инвертор: SUN-20K-SG05LP3-EU-SM2. ДГУ: АД-16С-Т400-1РКМ5, "
            "16 кВт / 20 кВА, S/N DG030000022116. Жёлтые строки — ключевые. Колонка «Факт» — на объекте.",
            s["body"],
        )
    )
    story.append(
        P(
            "ДГУ только 16 кВт — Rated Power и ток заряда ограничить. "
            "Gen Signal только на Master. G-start = сухой контакт (без напряжения).",
            s["warn"],
        )
    )

    story.append(P("1. Подключение", s["h1"]))
    c = s["cell"]
    cb = s["cellb"]
    rows = [
        [P("Пункт", cb), P("Выставить", cb), P("Пояснение", cb), P("Факт", cb)],
        [
            P("Сигнал пуска", c),
            P("Master CN2 G-start 1–2 → DIN <b>40</b> и <b>41</b>", c),
            P("Сначала тест замыканием 40–41 в AUTO. Если нет реакции — пара 22–0", c),
            P("", c),
        ],
        [
            P("Slave G-start", c),
            P("Не подключать", c),
            P("Gen Signal на Slave = ВЫКЛ", c),
            P("", c),
        ],
        [
            P("Сила ДГУ", c),
            P("L1 L2 L3 N PE → автомат ~32 А → порт GEN", c),
            P("Не Load / не Grid. Фазировка = Grid", c),
            P("", c),
        ],
        [
            P("L / N1 на DIN", c),
            P("Не трогать для пуска", c),
            P("Не сигнал Remote Start", c),
            P("", c),
        ],
        [
            P("Контроллер ДГУ", c),
            P("Режим AUTO", c),
            P("Типовой SmartGen HGM-6120NC", c),
            P("", c),
        ],
    ]
    story.append(make_table(rows, [3.2 * cm, 5.5 * cm, 6.5 * cm, 2.0 * cm], {1, 2}))
    story.append(Spacer(1, 4 * mm))

    story.append(P("2. GEN PORT USE (оба инвертора)", s["h1"]))
    rows = [
        [P("Пункт", cb), P("Значение", cb), P("Пояснение", cb), P("Факт", cb)],
        [P("Generator Input", c), P("ВКЛ", c), P("Порт = вход генератора", c), P("", c)],
        [P("SmartLoad / Micro Inv", c), P("ВЫКЛ", c), P("Иначе GEN не примет ДГУ", c), P("", c)],
        [
            P("Rated Power", c),
            P("<b>14000 W</b>", c),
            P("Паспорт ДГУ 16 кВт; запас. Не 20000", c),
            P("", c),
        ],
        [P("GEN connect to grid input", c), P("ВЫКЛ", c), P("ДГУ в клеммы GEN", c), P("", c)],
    ]
    story.append(make_table(rows, [4.0 * cm, 3.5 * cm, 7.7 * cm, 2.0 * cm], {1, 3}))
    story.append(Spacer(1, 4 * mm))

    story.append(P("3. Battery Setup — Gen Charge / Gen Signal", s["h1"]))
    rows = [
        [P("Пункт", cb), P("Master", cb), P("Slave", cb), P("Пояснение", cb), P("Факт", cb)],
        [P("Gen Charge", c), P("ВКЛ", c), P("ВКЛ", c), P("Заряд АКБ с GEN", c), P("", c)],
        [
            P("Gen Signal", c),
            P("<b>ВКЛ</b>", c),
            P("<b>ВЫКЛ</b>", c),
            P("Сухой контакт пуска только с Master", c),
            P("", c),
        ],
        [
            P("Start (SOC)", c),
            P("28 %", c),
            P("28 %", c),
            P("Ниже порога → автостарт (25–30 %)", c),
            P("", c),
        ],
        [
            P("Ток заряда A=", c),
            P("80 A", c),
            P("80 A", c),
            P("~4 кВт; запас ДГУ под Load. Подкрутить", c),
            P("", c),
        ],
        [
            P("Gen charge stop %", c),
            P("0", c),
            P("0", c),
            P("≠0 рвёт GEN и гасит Load с ГУ", c),
            P("", c),
        ],
        [P("Gen Max Run Time", c), P("24 h", c), P("24 h", c), P("24 = без суточного стопа", c), P("", c)],
    ]
    story.append(make_table(rows, [3.2 * cm, 2.2 * cm, 2.2 * cm, 7.6 * cm, 2.0 * cm], {2, 3, 4}))
    story.append(Spacer(1, 4 * mm))

    story.append(P("4. Advanced + Parallel", s["h1"]))
    rows = [
        [P("Пункт", cb), P("Значение", cb), P("Пояснение", cb), P("Факт", cb)],
        [
            P("Gen Peak-shaving", c),
            P("ВКЛ", c),
            P("Инвертор добирает из АКБ при перегрузе 16 кВт ДГУ", c),
            P("", c),
        ],
        [P("Parallel role", c), P("INV1 Master / INV2 Slave", c), P("Кабель Parallel_A/B", c), P("", c)],
    ]
    story.append(make_table(rows, [3.5 * cm, 4.5 * cm, 7.2 * cm, 2.0 * cm], {1}))
    story.append(Spacer(1, 4 * mm))

    story.append(P("5. Порядок на объекте", s["h1"]))
    story.append(
        P(
            "☐ AUTO + тест 40–41 (или 22–0) без инвертора &nbsp;&nbsp; "
            "☐ G-start только Master &nbsp;&nbsp; "
            "☐ Сила → GEN, фазы OK<br/>"
            "☐ Меню §2–4 &nbsp;&nbsp; "
            "☐ Пуск по SOC / Gen Force → на LCD Generator V/f/P &nbsp;&nbsp; "
            "☐ Нагрузка без захлёба ДГУ<br/>"
            "☐ Стоп по снятию сигнала / рост SOC &nbsp;&nbsp; "
            "☐ Записать: пара клемм ____ Start% ____ A= ____ Rated ____",
            s["body"],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "Мануал Deye: downloads/Deye_SUN-20K-SG05LP3-EU-SM2_User_Manual_EN.pdf (§3.12 ДГУ, §5.9 GEN PORT). "
            "Папка ДГУ: Платы и модули/Дизельные_генераторы/TSS_TQc_22TS_ST_АД-16С-Т400/. "
            "Подробный md: notes/АВТОЗАПУСК_ГЕНЕРАТОР_TSS_2xDeye20K.md",
            s["small"],
        )
    )

    doc.build(story)
    print(f"OK {OUT}")


if __name__ == "__main__":
    build()
