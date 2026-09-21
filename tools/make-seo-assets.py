#!/usr/bin/env python3
"""C.P.S — SEO assets: favicon set + og-image (ασπρόμαυρο, από το πραγματικό λογότυπο)."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, pathlib

A = pathlib.Path("assets")
SRC = A / "cps-wordmark.png"          # C.P.S wordmark (μαύρο σε transparent)
LOCKUP = A / "cps-lockup.png"          # C.P.S + Complete Project Solutions

def tight(img):
    a = np.array(img.convert("RGBA"))
    m = a[..., 3] > 20
    cols, rows = m.any(axis=0), m.any(axis=1)
    x0, x1 = int(np.argmax(cols)), len(cols) - 1 - int(np.argmax(cols[::-1]))
    y0, y1 = int(np.argmax(rows)), len(rows) - 1 - int(np.argmax(rows[::-1]))
    return img.crop((x0, y0, x1 + 1, y1 + 1))

def square_icon(mark, size, pad=0.09, bg="white"):
    """Βάζει το mark (πλατύ) κεντραρισμένο σε τετράγωνο καμβά."""
    canvas = Image.new("RGBA", (size, size), bg)
    inner = int(size * (1 - 2 * pad))
    w, h = mark.size
    scale = min(inner / w, inner / h)
    m2 = mark.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    canvas.alpha_composite(m2, ((size - m2.width) // 2, (size - m2.height) // 2))
    return canvas

wordmark = tight(Image.open(SRC).convert("RGBA"))
lockup   = tight(Image.open(LOCKUP).convert("RGBA"))
print("wordmark tight:", wordmark.size, "| lockup tight:", lockup.size)

# ── favicons (από το πραγματικό C.P.S mark) ──
for s in (16, 32, 48, 96, 192, 512):
    square_icon(wordmark, s).save(A / f"favicon-{s}x{s}.png")
square_icon(wordmark, 180, pad=0.10).convert("RGB").save(A / "apple-touch-icon.png")

ico = square_icon(wordmark, 256, pad=0.09)
ico.save(A / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("favicon set ✅")

# ── og-image 1200x630 ──
W, H = 1200, 630
og = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(og)

try:
    f_sub = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 30)
    f_url = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 24)
except Exception:
    f_sub = f_url = ImageFont.load_default()

lw = 760
lk = lockup.resize((lw, round(lockup.height * lw / lockup.width)), Image.LANCZOS)
og.paste(lk, ((W - lk.width) // 2, 190), lk)

d.line([(W // 2 - 60, 340), (W // 2 + 60, 340)], fill=(10, 10, 10), width=1)
sub = "Πολιτικός Μηχανικός · Διακόσμηση · Λάρισα"
tw = d.textlength(sub, font=f_sub)
d.text(((W - tw) / 2, 386), sub, fill=(74, 74, 74), font=f_sub)

url = "cps-solutions.gr"
uw = d.textlength(url, font=f_url)
d.text(((W - uw) / 2, 520), url, fill=(10, 10, 10), font=f_url)

og.save(A / "og-image.jpg", quality=88, optimize=True)
print("og-image ✅", (A / "og-image.jpg").stat().st_size // 1024, "KB")
