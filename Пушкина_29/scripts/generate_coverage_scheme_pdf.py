#!/usr/bin/env python3
"""Схема двора Пушкина 29 — ЗУ3 с зонами покрытия.

Обновлено: 2026-10-26
Источник: notes/zu3_fragment_source_2026-10-26.png
- розовый контур → асфальт
- синий контур → плитка

Пересборка: python3 scripts/generate_coverage_scheme_pdf.py
"""
from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Приложение 1 - Схема зон покрытия (плитка-асфальт) - Пушкина 29.pdf"
SRC = ROOT / "notes" / "zu3_fragment_source_2026-10-26.png"
VERT_OUT = ROOT / "notes" / "zu3_fragment_vertical_2026-10-26.png"
ZONES_OUT = ROOT / "notes" / "zu3_fragment_zones_2026-10-26.png"
UPSCALE = 2

# Палитра оформления (редакция 2026-10-26)
C_INK = (28, 32, 38)
C_MUTED = (90, 98, 110)
C_LINE = (210, 216, 224)
C_PANEL = (246, 248, 251)
C_ACCENT = (26, 86, 140)
C_ASPHALT = (78, 84, 92)
C_ASPHALT_HATCH = (48, 52, 58)
C_TILE = (72, 148, 220)
C_TILE_LIGHT = (186, 218, 248)
C_TILE_INK = (18, 70, 140)
C_PINK = (210, 60, 140)


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
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
    # лёгкое выравнивание наклона (±2°) для более ровной вёрстки
    best = vert
    best_score = score(vert)
    for fine in (-2.0, -1.0, 1.0, 2.0):
        cand = trim_white(
            vert.rotate(fine, expand=True, fillcolor=(255, 255, 255), resample=Image.Resampling.BICUBIC)
        )
        sc = score(cand)
        if sc > best_score:
            best, best_score = cand, sc
    vert = best
    return vert.resize((vert.size[0] * UPSCALE, vert.size[1] * UPSCALE), Image.Resampling.LANCZOS)


def _rounded_label(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fg: tuple[int, int, int, int],
    accent: tuple[int, int, int, int],
) -> None:
    tb = draw.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 16, 10
    bar_w = 8
    x0 = cx - (tw + pad_x * 2 + bar_w) // 2
    y0 = cy - (th + pad_y * 2) // 2
    x1 = x0 + tw + pad_x * 2 + bar_w
    y1 = y0 + th + pad_y * 2
    # тень
    draw.rounded_rectangle(
        [x0 + 3, y0 + 4, x1 + 3, y1 + 4],
        radius=10,
        fill=(0, 0, 0, 45),
    )
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(255, 255, 255, 235))
    draw.rounded_rectangle([x0, y0, x0 + bar_w + 4, y1], radius=10, fill=accent)
    draw.rectangle([x0 + bar_w, y0, x0 + bar_w + 6, y1], fill=(255, 255, 255, 235))
    draw.text((x0 + bar_w + pad_x - 2, y0 + pad_y - 1), text, font=font, fill=fg)


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
    # диагональная штриховка асфальта, «плиточная» сетка для плитки
    asphalt_hatch = asphalt & (((yy + xx) % 12) < 3)
    tile_hatch = tile & ((((yy // 8) + (xx // 8)) % 2) == 0) & (((yy % 8) < 6) & ((xx % 8) < 6))
    out = base.copy()
    # полупрозрачные заливки — чертёж читается под зонами
    out[asphalt] = out[asphalt] * 0.68 + np.array(C_ASPHALT, dtype=np.float32) * 0.32
    out[tile] = out[tile] * 0.62 + np.array(C_TILE_LIGHT, dtype=np.float32) * 0.38
    out[asphalt_hatch] = out[asphalt_hatch] * 0.78 + np.array(C_ASPHALT_HATCH, dtype=np.float32) * 0.22
    out[tile_hatch] = out[tile_hatch] * 0.86 + np.array(C_TILE, dtype=np.float32) * 0.14
    out = np.clip(out, 0, 255).astype(np.uint8)
    # контуры поверх заливки
    for mask, color in ((pink, C_PINK), (blue, C_TILE)):
        thick = dilate(mask, 1)
        out[thick] = color
        out[mask] = color

    img = Image.fromarray(out).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    font = _font("DejaVuSans-Bold", 32)

    def label_at(mask: np.ndarray, text: str, fg, accent) -> None:
        if not mask.any():
            return
        ys, xs = np.where(mask)
        y_lo, y_hi = np.percentile(ys, [30, 70])
        sel = (ys >= y_lo) & (ys <= y_hi)
        cy = int(np.median(ys[sel]))
        cx = int(np.median(xs[sel]))
        _rounded_label(draw, cx, cy, text, font, fg, accent)

    label_at(asphalt, "АСФАЛЬТ", (*C_INK, 255), (*C_PINK, 255))
    label_at(tile, "ПЛИТКА", (*C_TILE_INK, 255), (*C_TILE, 255))
    return img.convert("RGB")


def _legend_swatch(kind: str, size: int = 36) -> Image.Image:
    im = Image.new("RGB", (size, size), (255, 255, 255))
    d = ImageDraw.Draw(im)
    if kind == "asphalt":
        d.rectangle([0, 0, size - 1, size - 1], fill=C_ASPHALT, outline=C_PINK, width=2)
        for i in range(-size, size * 2, 5):
            d.line([i, 0, i + size, size], fill=C_ASPHALT_HATCH, width=1)
        d.rectangle([0, 0, size - 1, size - 1], outline=C_PINK, width=2)
    else:
        d.rectangle([0, 0, size - 1, size - 1], fill=C_TILE_LIGHT, outline=C_TILE, width=2)
        for y in range(4, size, 8):
            for x in range(4, size, 8):
                d.rectangle([x, y, x + 4, y + 4], fill=C_TILE)
    return im


def _compose_header(pw: int) -> Image.Image:
    h = 96
    im = Image.new("RGB", (pw, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, pw, 5], fill=C_ACCENT)
    d.rectangle([20, 14, pw - 20, h - 6], fill=C_PANEL, outline=C_LINE, width=1)
    d.rectangle([20, 14, 26, h - 6], fill=C_ACCENT)

    d.text((40, 20), "СХЕМА ДВОРА", font=_font("DejaVuSans-Bold", 15), fill=C_ACCENT)
    d.text(
        (40, 42),
        "многоквартирного дома № 29 по ул. Пушкина, г. Симферополь",
        font=_font("DejaVuSans", 10),
        fill=C_INK,
    )
    d.text(
        (40, 60),
        "Приложение № 1 к коллективному обращению от 26.10.2026  ·  участок ЗУ3 — зоны покрытия",
        font=_font("DejaVuSans", 8),
        fill=C_MUTED,
    )
    return im


def _compose_legend(pw: int) -> Image.Image:
    h = 52
    im = Image.new("RGB", (pw, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    card_w = (pw - 20 * 2 - 10) // 2
    cards = [
        (20, "asphalt", "Асфальт", "проезд · розовый контур"),
        (20 + card_w + 10, "tile", "Плитка", "пешеходная зона · синий контур"),
    ]
    for x0, kind, title, desc in cards:
        d.rounded_rectangle([x0, 2, x0 + card_w, h - 2], radius=7, fill=C_PANEL, outline=C_LINE, width=1)
        sw = _legend_swatch(kind, 28)
        im.paste(sw, (x0 + 10, 12))
        d.text((x0 + 48, 8), title, font=_font("DejaVuSans-Bold", 11), fill=C_INK)
        d.text((x0 + 48, 28), desc, font=_font("DejaVuSans", 8), fill=C_MUTED)
    return im


def _compose_footer(pw: int) -> Image.Image:
    h = 44
    im = Image.new("RGB", (pw, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.line([20, 1, pw - 20, 1], fill=C_LINE, width=1)
    d.text(
        (20, 8),
        "Основа: чертёж территории, ООО «ГЕОАЛЬЯНС», 2021, кв. 90:22:010301, М 1:500",
        font=_font("DejaVuSans", 7),
        fill=C_MUTED,
    )
    d.text(
        (20, 22),
        "Уполномоченное лицо: Валюкевич Н.Г., кв. 18   ·   лист 1 из 1   ·   редакция 2026-10-26",
        font=_font("DejaVuSans", 7),
        fill=C_INK,
    )
    return im


def _frame_plan(plan: Image.Image, max_w: int, max_h: int) -> Image.Image:
    """Вписать план крупно в рамку с полями."""
    pad = 10
    # обрезать лишнюю белую кайму у плана — больше полезной площади
    plan = trim_white(plan, thr=248)
    iw, ih = plan.size
    scale = min((max_w - pad * 2) / iw, (max_h - pad * 2) / ih)
    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
    resized = plan.resize((nw, nh), Image.Resampling.LANCZOS)

    # рамка плотно по плану, без огромных пустых полей
    box_w = min(max_w, nw + pad * 2)
    box_h = min(max_h, nh + pad * 2)
    canvas_im = Image.new("RGB", (max_w, max_h), (255, 255, 255))
    bx = (max_w - box_w) // 2
    by = (max_h - box_h) // 2
    d = ImageDraw.Draw(canvas_im)
    d.rounded_rectangle(
        [bx, by, bx + box_w - 1, by + box_h - 1],
        radius=8,
        fill=C_PANEL,
        outline=C_LINE,
        width=1,
    )
    ox = bx + (box_w - nw) // 2
    oy = by + (box_h - nh) // 2
    canvas_im.paste(resized, (ox, oy))
    return canvas_im


def build_pdf(plan: Image.Image) -> None:
    pw, ph = A4
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle(OUT.stem)
    c.setAuthor("Пушкина 29")
    c.setSubject("Приложение 1 — зоны покрытия (плитка / асфальт)")

    header = _compose_header(int(pw))
    legend = _compose_legend(int(pw))
    footer = _compose_footer(int(pw))

    header_h = header.size[1]
    legend_h = legend.size[1]
    footer_h = footer.size[1]
    gap = 6

    c.drawImage(ImageReader(header), 0, ph - header_h, width=pw, height=header_h, mask="auto")
    c.drawImage(
        ImageReader(legend),
        0,
        ph - header_h - legend_h - gap,
        width=pw,
        height=legend_h,
        mask="auto",
    )

    max_w = int(pw - 28)
    max_h = int(ph - header_h - legend_h - footer_h - gap * 3)
    framed = _frame_plan(plan, max_w, max_h)
    plan_y = footer_h + gap
    c.drawImage(
        ImageReader(framed),
        (pw - max_w) / 2,
        plan_y,
        width=max_w,
        height=max_h,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )
    c.drawImage(ImageReader(footer), 0, 0, width=pw, height=footer_h, mask="auto")
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
