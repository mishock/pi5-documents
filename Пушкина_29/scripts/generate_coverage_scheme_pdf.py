#!/usr/bin/env python3
"""Схема зон покрытия двора Пушкина 29 (плитка / асфальт).

Обновлено: 2026-10-26
Стиль как у «Приложение 1 — Схема двора» от 08.10.2026:
- лист 1: простой заголовок + крупный план;
- лист 2: условные обозначения.

Источник: notes/zu3_fragment_source_2026-10-26.png
- розовый контур → асфальт
- синий контур → плитка

Пересборка: python3 scripts/generate_coverage_scheme_pdf.py
"""
from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Приложение 1 - Схема зон покрытия (плитка-асфальт) - Пушкина 29.pdf"
SRC = ROOT / "notes" / "zu3_fragment_source_2026-10-26.png"
VERT_OUT = ROOT / "notes" / "zu3_fragment_vertical_2026-10-26.png"
ZONES_OUT = ROOT / "notes" / "zu3_fragment_zones_2026-10-26.png"
UPSCALE = 2

# заливки зон (технический стиль, как на схеме двора 08.10)
C_ASPHALT = (110, 110, 115)
C_ASPHALT_HATCH = (55, 55, 60)
C_TILE = (176, 120, 72)
C_TILE_LIGHT = (220, 180, 130)
C_PINK = (210, 60, 140)
C_BLUE = (40, 90, 200)

FONT_REG = "DejaVu"
FONT_BOLD = "DejaVu-Bold"
pdfmetrics.registerFont(TTFont(FONT_REG, "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont(FONT_BOLD, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


def _pil_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)


def dilate(m: np.ndarray, n: int = 1) -> np.ndarray:
    out = m.copy()
    for _ in range(n):
        nxt = out.copy()
        nxt[1:] |= out[:-1]
        nxt[:-1] |= out[1:]
        nxt[:, 1:] |= out[:, :-1]
        nxt[:, :-1] |= out[:, 1:]
        nxt[1:, 1:] |= out[:-1, :-1]
        nxt[:-1, :-1] |= out[1:, 1:]
        out = nxt
    return out


def trim_white(im: Image.Image, thr: int = 250) -> Image.Image:
    a = np.array(im.convert("RGB"))
    m = a.mean(2) < thr
    if not m.any():
        return im
    ys, xs = np.where(m)
    return im.crop(
        (
            max(0, int(xs.min()) - 4),
            max(0, int(ys.min()) - 4),
            min(a.shape[1], int(xs.max()) + 5),
            min(a.shape[0], int(ys.max()) + 5),
        )
    )


def flood_exterior(wall: np.ndarray) -> np.ndarray:
    h, w = wall.shape
    ext = np.zeros_like(wall)
    q: deque[tuple[int, int]] = deque()
    for p in (
        (0, 0),
        (0, w - 1),
        (h - 1, 0),
        (h - 1, w - 1),
        (h // 2, 0),
        (h // 2, w - 1),
        (0, w // 2),
        (h - 1, w // 2),
    ):
        if not wall[p]:
            ext[p] = True
            q.append(p)
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not wall[ny, nx] and not ext[ny, nx]:
                ext[ny, nx] = True
                q.append((ny, nx))
    return ext


def components(inside: np.ndarray, min_n: int = 800) -> list[tuple[int, np.ndarray]]:
    h, w = inside.shape
    vis = np.zeros_like(inside)
    comps: list[tuple[int, np.ndarray]] = []
    for y in range(h):
        for x in np.where(inside[y])[0]:
            if vis[y, x]:
                continue
            q: deque[tuple[int, int]] = deque([(y, x)])
            vis[y, x] = True
            cells: list[tuple[int, int]] = []
            while q:
                cy, cx = q.popleft()
                cells.append((cy, cx))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and inside[ny, nx] and not vis[ny, nx]:
                        vis[ny, nx] = True
                        q.append((ny, nx))
            if len(cells) >= min_n:
                fill = np.zeros_like(inside)
                for cy, cx in cells:
                    fill[cy, cx] = True
                comps.append((len(cells), fill))
    comps.sort(key=lambda t: -t[0])
    return comps


def interiors_from_wall(wall0: np.ndarray, dil: int = 3, min_n: int = 800):
    closed = dilate(wall0, dil)
    ext = flood_exterior(closed)
    inside = ~ext & ~closed
    out = []
    for n, fill in components(inside, min_n=min_n):
        ring = dilate(fill, 3) & closed
        out.append((n, fill | ring))
    return out


def extract_vertical_fragment(src: Path) -> Image.Image:
    arr = np.array(Image.open(src).convert("RGB"))
    h, w = arr.shape[:2]
    r, g, b = (arr[:, :, i].astype(int) for i in range(3))
    wall = dilate((r < 55) & (g < 55) & (b < 55), 2)
    ext = flood_exterior(wall)
    inside = ~ext & ~wall
    mask = inside | (dilate(inside, 3) & wall)
    out = arr.copy()
    out[~mask] = (255, 255, 255)
    ys, xs = np.where(mask)
    pad = 4
    bb = (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(w, int(xs.max()) + pad + 1),
        min(h, int(ys.max()) + pad + 1),
    )
    cropped = Image.fromarray(out).crop(bb)

    def score(im: Image.Image) -> float:
        a = np.array(im.convert("RGB"))
        hh, ww = a.shape[:2]
        rr, gg, bb_ = (a[:, :, i].astype(int) for i in range(3))
        mag = (rr > 140) & (gg < 100) & (bb_ > 100) & (rr > gg + 40)
        blue = (bb_ > 130) & (bb_ > rr + 25) & (bb_ > gg + 15) & (rr < 200)
        dark = (rr < 90) & (gg < 90) & (bb_ < 90)
        aspect = hh / max(ww, 1)
        mag_lo = float(mag[hh // 2 :].mean()) if mag.any() else 0.0
        mag_hi = float(mag[: hh // 2].mean()) if mag.any() else 0.0
        blue_hi = float(blue[: hh // 2].mean()) if blue.any() else 0.0
        blue_lo = float(blue[hh // 2 :].mean()) if blue.any() else 0.0
        dark_lo = float(dark[int(hh * 0.65) :].mean()) if dark.any() else 0.0
        return aspect * 2 + (mag_lo - mag_hi) * 50 + (blue_hi - blue_lo) * 80 + dark_lo * 30

    cands: list[tuple[float, Image.Image]] = []
    for ang in (-50, -45, -40, 40, 45, 50):
        rimg = trim_white(
            cropped.rotate(ang, expand=True, fillcolor=(255, 255, 255), resample=Image.Resampling.BICUBIC)
        )
        variants = [rimg]
        if rimg.size[0] > rimg.size[1]:
            for extra in (90, -90):
                variants.append(
                    trim_white(
                        rimg.rotate(
                            extra,
                            expand=True,
                            fillcolor=(255, 255, 255),
                            resample=Image.Resampling.BICUBIC,
                        )
                    )
                )
        for v in variants:
            if v.size[1] >= v.size[0]:
                cands.append((score(v), v))
    if not cands:
        raise RuntimeError("Не удалось получить вертикальный фрагмент")
    vert = max(cands, key=lambda t: t[0])[1]
    best, best_score = vert, score(vert)
    for fine in (-2.0, -1.0, 1.0, 2.0):
        cand = trim_white(
            vert.rotate(fine, expand=True, fillcolor=(255, 255, 255), resample=Image.Resampling.BICUBIC)
        )
        sc = score(cand)
        if sc > best_score:
            best, best_score = cand, sc
    vert = best
    return vert.resize((vert.size[0] * UPSCALE, vert.size[1] * UPSCALE), Image.Resampling.LANCZOS)


def _plain_label(draw: ImageDraw.ImageDraw, cx: int, cy: int, text: str, fill) -> None:
    """Простая подпись как на схеме двора 08.10 — белый прямоугольник, чёрный текст."""
    font = _pil_font("DejaVuSans-Bold", 30)
    tb = draw.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad = 6
    x0, y0 = cx - tw // 2 - pad, cy - th // 2 - pad
    x1, y1 = cx + tw // 2 + pad, cy + th // 2 + pad
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.text((x0 + pad, y0 + pad - 1), text, font=font, fill=fill)


def paint_zones(vert: Image.Image) -> Image.Image:
    """Розовый контур → асфальт; синий → плитка."""
    arr = np.array(vert.convert("RGB"))
    h, w = arr.shape[:2]
    r, g, b = (arr[:, :, i].astype(int) for i in range(3))

    pink = (r > 140) & (g < 130) & (b > 100) & (r > g + 35) & (b > g + 15)
    pink |= (r > 180) & (b > 140) & (g < 150) & (r > g + 40)
    blue = (b > 125) & (b > r + 25) & (b > g + 20) & (r < 190) & (g < 200)
    blue &= ~((g > b) & (g > 100))

    pink_comps = interiors_from_wall(pink, dil=3, min_n=1500)
    blue_comps = interiors_from_wall(blue, dil=3, min_n=800)
    if not pink_comps:
        raise RuntimeError("Не найден розовый контур (асфальт)")

    asphalt = pink_comps[0][1].copy()
    tile = np.zeros((h, w), dtype=bool)
    for n, f in blue_comps:
        outside = f & ~asphalt
        if outside.sum() >= max(500, int(0.35 * n)):
            tile |= outside
        else:
            ys, _ = np.where(f)
            ays, _ = np.where(asphalt)
            if ys.mean() < ays.mean() - 20:
                tile |= f
    asphalt = asphalt & ~tile

    base = arr.astype(np.float32)
    yy, xx = np.indices((h, w))
    # асфальт — серая диагональная штриховка; плитка — «кирпичная» как зона П на схеме 08.10
    asphalt_hatch = asphalt & (((yy + xx) % 10) < 3)
    tile_brick = tile & ((yy % 10) < 5)
    out = base.copy()
    out[asphalt] = out[asphalt] * 0.70 + np.array(C_ASPHALT, dtype=np.float32) * 0.30
    out[tile] = out[tile] * 0.55 + np.array(C_TILE_LIGHT, dtype=np.float32) * 0.45
    out[asphalt_hatch] = out[asphalt_hatch] * 0.72 + np.array(C_ASPHALT_HATCH, dtype=np.float32) * 0.28
    out[tile_brick] = out[tile_brick] * 0.65 + np.array(C_TILE, dtype=np.float32) * 0.35
    out = np.clip(out, 0, 255).astype(np.uint8)
    for mask, color in ((pink, C_PINK), (blue, C_BLUE)):
        out[dilate(mask, 1)] = color
        out[mask] = color

    img = Image.fromarray(out)
    draw = ImageDraw.Draw(img)

    def label_at(mask: np.ndarray, text: str, fill) -> None:
        if not mask.any():
            return
        ys, xs = np.where(mask)
        y_lo, y_hi = np.percentile(ys, [30, 70])
        sel = (ys >= y_lo) & (ys <= y_hi)
        _plain_label(draw, int(np.median(xs[sel])), int(np.median(ys[sel])), text, fill)

    label_at(asphalt, "А", (0, 0, 0))
    label_at(tile, "Пл", (0, 0, 0))
    return img


def _draw_title(c: canvas.Canvas, pw: float, ph: float, sheet: str) -> float:
    """Заголовок как на схеме двора 08.10. Возвращает Y низа заголовка."""
    y = ph - 28
    c.setFillColorRGB(0, 0, 0)
    c.setFont(FONT_BOLD, 13)
    c.drawCentredString(pw / 2, y, "СХЕМА ДВОРА многоквартирного дома № 29 по ул. Пушкина, г. Симферополь")
    y -= 16
    c.setFont(FONT_REG, 10)
    c.drawCentredString(
        pw / 2,
        y,
        f"(приложение № 1 к коллективному обращению от 26.10.2026) — {sheet}",
    )
    return y - 10


def _draw_footer_page1(c: canvas.Canvas, pw: float) -> None:
    c.setFillColorRGB(0, 0, 0)
    c.setFont(FONT_REG, 9)
    c.drawString(36, 48, "Участок ЗУ3 — зоны покрытия двора (плитка / асфальт).")
    c.drawString(36, 34, "Лист 1 из 2. Условные обозначения — на листе 2.")
    c.drawString(36, 18, "Уполномоченное лицо: Валюкевич Н.Г., кв. 18  _____________  (подпись)")


def _legend_swatch(kind: str, size: int = 28) -> Image.Image:
    im = Image.new("RGB", (size, size), (255, 255, 255))
    d = ImageDraw.Draw(im)
    if kind == "asphalt":
        d.rectangle([0, 0, size - 1, size - 1], fill=C_ASPHALT, outline=C_PINK, width=2)
        for i in range(-size, size * 2, 4):
            d.line([i, 0, i + size, size], fill=C_ASPHALT_HATCH, width=1)
        d.rectangle([0, 0, size - 1, size - 1], outline=C_PINK, width=2)
    else:
        d.rectangle([0, 0, size - 1, size - 1], fill=C_TILE_LIGHT, outline=C_BLUE, width=2)
        for y in range(0, size, 5):
            d.rectangle([1, y, size - 2, y + 2], fill=C_TILE)
        d.rectangle([0, 0, size - 1, size - 1], outline=C_BLUE, width=2)
    return im


def _draw_legend_page(c: canvas.Canvas, pw: float, ph: float) -> None:
    y = _draw_title(c, pw, ph, "лист 2 из 2")
    y -= 18
    c.setFont(FONT_BOLD, 12)
    c.drawString(48, y, "Условные обозначения:")
    y -= 28

    items = [
        ("asphalt", "А — асфальтовое покрытие (проезд / внутри розового контура)"),
        ("tile", "Пл — плиточное покрытие (пешеходная зона / внутри синего контура)"),
    ]
    for kind, text in items:
        sw = _legend_swatch(kind, 26)
        c.drawImage(ImageReader(sw), 52, y - 4, width=26, height=26, mask="auto")
        c.setFont(FONT_REG, 11)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(88, y + 4, text)
        y -= 36

    y -= 8
    c.setFont(FONT_BOLD, 11)
    c.drawString(48, y, "Примечание:")
    y -= 18
    c.setFont(FONT_REG, 10)
    for line in (
        "На листе 1 показан участок ЗУ3 по чертежу территории (фрагмент).",
        "Розовый контур — предлагаемая зона асфальта; синий контур — зона плитки.",
        "Комбинированное покрытие двора вместо сплошного асфальта.",
    ):
        c.drawString(48, y, line)
        y -= 15

    c.setFont(FONT_REG, 8)
    c.drawString(
        36,
        52,
        "Основа: чертёж территории, ООО «ГЕОАЛЬЯНС», 2021, кадастровый квартал 90:22:010301, М 1:500.",
    )
    c.drawString(
        36,
        38,
        "На листе 1 — северная/центральная часть участка ЗУ3 (редакция 2026-10-26).",
    )
    c.drawString(36, 18, "Уполномоченное лицо: Валюкевич Н.Г., кв. 18  _____________  (подпись)")


def build_pdf(plan: Image.Image) -> None:
    pw, ph = A4
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle(OUT.stem)
    c.setAuthor("Пушкина 29")
    c.setSubject("Приложение 1 — зоны покрытия (плитка / асфальт)")

    # —— лист 1 ——
    y_top = _draw_title(c, pw, ph, "лист 1 из 2")
    footer_top = 68
    max_w = pw - 48
    max_h = y_top - footer_top - 8
    plan = trim_white(plan, thr=248)
    iw, ih = plan.size
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    x = (pw - dw) / 2
    y = footer_top + (max_h - dh) / 2
    c.drawImage(ImageReader(plan), x, y, width=dw, height=dh, mask="auto")
    _draw_footer_page1(c, pw)
    c.showPage()

    # —— лист 2 ——
    _draw_legend_page(c, pw, ph)
    c.save()


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Нет фрагмента: {SRC}")
    vert = extract_vertical_fragment(SRC)
    vert.save(VERT_OUT)
    plan = paint_zones(vert)
    plan.save(ZONES_OUT)
    build_pdf(plan)
    print(f"OK {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
