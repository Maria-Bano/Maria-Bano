# -*- coding: utf-8 -*-
"""Generate github-banner.png for Maria-Bano GitHub profile."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parent.parent / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

BG = (13, 17, 23)       # #0D1117
BG2 = (22, 27, 34)      # #161B22
ACCENT = (88, 166, 255)  # #58A6FF
TEXT = (201, 209, 217)   # #C9D1D9
MUTED = (139, 148, 158)  # #8B949E
PANEL = (48, 54, 61)     # #30363D


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def gradient_bg(w: int, h: int) -> Image.Image:
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(BG[0] + (BG2[0] - BG[0]) * t)
        g = int(BG[1] + (BG2[1] - BG[1]) * t)
        b = int(BG[2] + (BG2[2] - BG[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img


def centered_text(draw, y, text, fnt, fill=TEXT):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    x = (draw.im.size[0] - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), text, font=fnt, fill=fill)


def make_banner():
    w, h = 1280, 320
    img = gradient_bg(w, h)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((32, 32, w - 32, h - 32), radius=18, outline=PANEL, width=2)

    # Accent line
    draw.line([(120, 88), (1160, 88)], fill=ACCENT, width=2)

    centered_text(draw, 108, "Maria Bano", font(52, True), TEXT)
    centered_text(
        draw,
        178,
        "AI Automation Engineer  \u2022  Voice AI  \u2022  Production Systems",
        font(24),
        MUTED,
    )
    centered_text(
        draw,
        228,
        "Building AI systems that automate communication, lead generation, and operations at scale",
        font(18),
        ACCENT,
    )

    # Subtle corner accents
    draw.arc((980, 40, 1240, 300), start=200, end=320, fill=ACCENT, width=2)
    draw.arc((40, 40, 300, 300), start=140, end=260, fill=PANEL, width=2)

    out = ASSETS / "github-banner.png"
    img.save(out, "PNG", optimize=True)
    print(f"Saved {out}")


if __name__ == "__main__":
    make_banner()
