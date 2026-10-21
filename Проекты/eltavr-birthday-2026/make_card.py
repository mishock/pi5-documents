#!/usr/bin/env python3
"""Открытка «Эльтавр — 12 лет» (21.10.2014 → 21.10.2026). Результат: generated/."""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "generated"
OUT.mkdir(exist_ok=True)

W, H = 1440, 1980
NOTO = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(NOTO + name, size)


F_BLACK = "NotoSansDisplay-Black.ttf"
F_XBOLD = "NotoSansDisplay-ExtraBold.ttf"
F_BOLD = "NotoSansDisplay-Bold.ttf"
F_SEMI = "NotoSansDisplay-SemiBold.ttf"
F_REG = "NotoSansDisplay-Regular.ttf"
F_ITAL = "NotoSansDisplay-Italic.ttf"

GOLD = (255, 205, 80)
GOLD2 = (255, 160, 40)
WHITE = (255, 255, 255)
SOFT = (215, 230, 255)

random.seed(2014)


def background():
    bg = Image.new("RGB", (W, H))
    px = bg.load()
    top, bottom = (8, 22, 70), (14, 80, 170)
    for y in range(H):
        t = y / H
        for x in range(W):
            r = math.hypot(x - W / 2, y - H * 0.32) / (W * 0.9)
            glow = max(0.0, 1 - r) ** 2 * 0.55
            c = [int(top[i] + (bottom[i] - top[i]) * t + 90 * glow) for i in range(3)]
            px[x, y] = tuple(min(255, v) for v in c)
    return bg.convert("RGBA")


def lightning_rays(img):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = W / 2, 560
    for i in range(36):
        a = i * math.pi * 2 / 36
        a2 = a + math.pi / 72
        d.polygon(
            [(cx, cy), (cx + 1600 * math.cos(a), cy + 1600 * math.sin(a)),
             (cx + 1600 * math.cos(a2), cy + 1600 * math.sin(a2))],
            fill=(255, 255, 255, 14),
        )
    return Image.alpha_composite(img, layer)


def confetti(img, n=260):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    colors = [GOLD, (255, 90, 120), (90, 220, 255), (140, 255, 150), (200, 140, 255), WHITE, GOLD2]
    for _ in range(n):
        x, y = random.randint(0, W), random.randint(0, int(H * 0.6))
        c = random.choice(colors) + (random.randint(150, 240),)
        kind = random.random()
        s = random.randint(6, 16)
        if kind < 0.4:
            d.ellipse([x, y, x + s, y + s], fill=c)
        elif kind < 0.8:
            a = random.uniform(0, math.pi)
            dx, dy = math.cos(a) * s, math.sin(a) * s
            d.line([x, y, x + dx * 1.6, y + dy * 1.6], fill=c, width=max(3, s // 3))
        else:
            d.regular_polygon((x, y, s), 4, rotation=random.randint(0, 90), fill=c)
    for _ in range(70):
        x, y = random.randint(0, W), random.randint(0, H)
        r = random.choice([1, 1, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, random.randint(120, 255)))
    return Image.alpha_composite(img, layer)


def balloons(img):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    specs = [(110, 330, (255, 80, 110)), (215, 250, GOLD), (60, 520, (90, 200, 255)),
             (W - 120, 320, (90, 200, 255)), (W - 225, 240, (255, 80, 110)), (W - 70, 530, GOLD)]
    for x, y, c in specs:
        rw, rh = 62, 78
        d.line([(x, y + rh), (x + 18, y + rh + 120), (x - 6, y + rh + 260)], fill=(255, 255, 255, 120), width=3)
        d.ellipse([x - rw, y - rh, x + rw, y + rh], fill=c + (235,))
        d.ellipse([x - rw * 0.55, y - rh * 0.7, x - rw * 0.15, y - rh * 0.25], fill=(255, 255, 255, 110))
        d.polygon([(x - 10, y + rh + 12), (x + 10, y + rh + 12), (x, y + rh - 2)], fill=c + (235,))
    return Image.alpha_composite(img, layer)


def text_center(img, y, text, fnt, fill, shadow=True, glow=None):
    d = ImageDraw.Draw(img)
    w = d.textlength(text, font=fnt)
    x = (W - w) / 2
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).text((x, y), text, font=fnt, fill=glow)
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(18)))
    if shadow:
        s = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(s).text((x + 4, y + 6), text, font=fnt, fill=(0, 0, 30, 150))
        img.alpha_composite(s.filter(ImageFilter.GaussianBlur(4)))
    ImageDraw.Draw(img).text((x, y), text, font=fnt, fill=fill)
    return img


def gold_number(img, text, y, size):
    fnt = font(F_BLACK, size)
    d = ImageDraw.Draw(img)
    bbox = d.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (W - tw) / 2 - bbox[0]
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).text((x, y), text, font=fnt, fill=255)

    glow = Image.new("RGBA", img.size, GOLD2 + (0,))
    glow.putalpha(mask.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.9)))
    img.alpha_composite(glow)

    shadow = Image.new("RGBA", img.size, (40, 10, 0, 0))
    shadow.putalpha(mask.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.6)))
    img.alpha_composite(shadow, (8, 14))

    grad = Image.new("RGBA", img.size)
    gd = ImageDraw.Draw(grad)
    y0, y1 = y + bbox[1], y + bbox[3]
    for yy in range(H):
        t = min(1, max(0, (yy - y0) / max(1, (y1 - y0))))
        if t < 0.5:
            c = [int(255 + (GOLD[i] - 255) * t * 2) for i in range(3)]
        else:
            c = [int(GOLD[i] + (GOLD2[i] - GOLD[i]) * (t - 0.5) * 2) for i in range(3)]
        gd.line([(0, yy), (W, yy)], fill=tuple(c) + (255,))
    grad.putalpha(mask)
    img.alpha_composite(grad)

    edge = mask.filter(ImageFilter.FIND_EDGES)
    stroke = Image.new("RGBA", img.size, (255, 250, 220, 0))
    stroke.putalpha(edge.point(lambda v: min(255, v * 2)))
    img.alpha_composite(stroke)
    return y + bbox[3]


def paste_vehicle(img, path, box_w, cx, bottom_y, flip=False):
    v = Image.open(path).convert("RGBA")
    if flip:
        v = v.transpose(Image.FLIP_LEFT_RIGHT)
    # срезаем полупрозрачную белую кайму после removebg
    a = v.getchannel("A").point(lambda p: 0 if p < 40 else p)
    v.putalpha(a)
    bb = v.getbbox()
    v = v.crop(bb)
    k = box_w / v.width
    v = v.resize((int(v.width * k), int(v.height * k)), Image.LANCZOS)
    x, y = int(cx - v.width / 2), int(bottom_y - v.height)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([x + v.width * 0.08, bottom_y - 22, x + v.width * 0.92, bottom_y + 22], fill=(0, 0, 20, 150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    img.alpha_composite(v, (x, y))


def ribbon(img, y, text):
    fnt = font(F_XBOLD, 64)
    d = ImageDraw.Draw(img)
    tw = d.textlength(text, font=fnt)
    pad = 70
    x0, x1 = (W - tw) / 2 - pad, (W + tw) / 2 + pad
    h = 110
    d.polygon([(x0 - 60, y + 20), (x0 + 10, y + 20), (x0 + 10, y + h + 20), (x0 - 60, y + h + 20), (x0 - 30, y + 20 + h / 2)], fill=(150, 20, 50))
    d.polygon([(x1 + 60, y + 20), (x1 - 10, y + 20), (x1 - 10, y + h + 20), (x1 + 60, y + h + 20), (x1 + 30, y + 20 + h / 2)], fill=(150, 20, 50))
    d.rounded_rectangle([x0, y, x1, y + h], radius=14, fill=(220, 40, 80))
    d.rounded_rectangle([x0 + 6, y + 6, x1 - 6, y + h - 6], radius=10, outline=(255, 200, 210), width=2)
    d.text(((W - tw) / 2, y + 12), text, font=fnt, fill=WHITE)


def logo_white(img, y, height):
    lg = Image.open(SRC / "cropped-Logo_wyte_2019_1.png").convert("RGBA")
    k = height / lg.height
    lg = lg.resize((int(lg.width * k), height), Image.LANCZOS)
    img.alpha_composite(lg, ((W - lg.width) // 2, y))


def build():
    img = background()
    img = lightning_rays(img)
    img = balloons(img)
    img = confetti(img)

    logo_white(img, 70, 92)
    text_center(img, 205, "С ДНЁМ РОЖДЕНИЯ!", font(F_BLACK, 104), WHITE, glow=(120, 200, 255, 200))

    bottom_12 = gold_number(img, "12", 300, 470)
    text_center(img, bottom_12 + 10, "ЛЕТ  ВМЕСТЕ", font(F_XBOLD, 78), GOLD)
    ribbon(img, bottom_12 + 120, "21.10.2014  —  21.10.2026")

    y = bottom_12 + 290
    lines = [
        ("Двенадцать лет мы строим то, что ездит, плавает", F_SEMI, 46, WHITE),
        ("и даёт свет, когда вокруг темно.", F_SEMI, 46, WHITE),
        ("Электромобили, катамараны, аккумуляторы, инверторы —", F_REG, 40, SOFT),
        ("за каждым стоят ваши руки, голова и характер.", F_REG, 40, SOFT),
        ("Спасибо, команда! Заряда на 100%, без перегрузок,", F_BOLD, 44, GOLD),
        ("и пусть наш свет не гаснет никогда!", F_BOLD, 44, GOLD),
    ]
    for i, (t, f, s, c) in enumerate(lines):
        if i in (2, 4):
            y += 18
        text_center(img, y, t, font(f, s), c)
        y += int(s * 1.32)

    floor_y = H - 80
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([-200, floor_y - 120, W + 200, floor_y + 260], fill=(120, 190, 255, 70))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(40)))

    paste_vehicle(img, SRC / "Elektrokatamaran_1-1024x753-removebg-preview.png", 380, W / 2, floor_y - 60)
    paste_vehicle(img, SRC / "IMG_6021-removebg-preview.png", 560, 300, floor_y)
    paste_vehicle(img, SRC / "IMG_20191004_152733-removebg-preview.png", 520, W - 290, floor_y)

    text_center(img, H - 52, "ООО «Эльтавр»  •  eltavr.ru  •  Крым", font(F_SEMI, 30), (200, 220, 255), shadow=False)

    out = OUT / "eltavr_12_let_otkrytka.png"
    img.convert("RGB").save(out, optimize=True)
    img.convert("RGB").save(out.with_suffix(".jpg"), quality=92)
    print(out)


if __name__ == "__main__":
    build()
