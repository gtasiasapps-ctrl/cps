#!/usr/bin/env python3
"""Demo εικόνες έργων (abstract architectural line-art) για το CPS site."""
from PIL import Image, ImageDraw, ImageFilter
import os, math

W, H = 1300, 1300          # 1:1 (γεμίζει το hero)
S = 2                      # supersample
OUT = "projects"          # ένας φάκελος ανά έργο: projects/<slug>/{cover,01,02}.jpg

# ποιο «μοτίβο» αντιστοιχεί σε ποιο slug
SLUGS = {
    "work-1":  "house-pool",
    "work-2":  "retail-store",
    "work-3":  "apartments",
    "work-4":  "apartment-110",
    "work-5":  "offices-industrial",
    "work-6":  "hotel-trikala",
    "work-7":  "cafe-central",
    "work-8":  "restaurant-larissa",
    "work-9":  "corporate-offices",
    "work-10": "showroom",
    "work-11": "hillside",
    "work-12": "hotel-rooms",
}

# «κάδρα» για τις λεπτομέρειες (x0,y0,x1,y1 σε αναλογία 0-1)
DETAILS = [(0.04, 0.16, 0.66, 0.82), (0.34, 0.02, 0.98, 0.62)]
os.makedirs(OUT, exist_ok=True)

INK   = (11, 18, 32)
ACC   = (70, 70, 70)

PALETTES = [   # μόνο λευκό / μαύρο (grayscale)
    ((236, 236, 236), (200, 200, 200), (220, 220, 220)),
    ((233, 233, 233), (193, 193, 193), (214, 214, 214)),
    ((238, 238, 238), (204, 204, 204), (222, 222, 222)),
    ((231, 231, 231), (190, 190, 190), (212, 212, 212)),
    ((235, 235, 235), (198, 198, 198), (218, 218, 218)),
    ((239, 239, 239), (206, 206, 206), (224, 224, 224)),
]


def vgrad(size, top, bot):
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        row = tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = row
    return img


def radial_tint(img, center, radius, color, strength):
    w, h = img.size
    ov = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(ov)
    cx, cy = center
    steps = 40
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(strength * 255 * (1 - i / steps) ** 1.6)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
    ov = ov.filter(ImageFilter.GaussianBlur(radius * 0.12))
    img.paste(Image.new("RGB", (w, h), color), (0, 0), ov)
    return img


def grain(img, amount=6):
    w, h = img.size
    px = img.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            n = ((x * 7919 + y * 104729) % 255) / 255.0
            k = (n - 0.5) * amount
            p = px[x, y]
            px[x, y] = tuple(max(0, min(255, int(p[i] + k))) for i in range(3))
    return img


def grid(d, w, h, step, color, alpha=26, width=1):
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for x in range(0, w + step, step):
        od.line([(x, 0), (x, h)], fill=color + (alpha,), width=width)
    for y in range(0, h + step, step):
        od.line([(0, y), (w, y)], fill=color + (alpha,), width=width)
    return ov


def windows(d, x0, y0, x1, y1, cols, rows, col, gap=0.16, w=3, fill=None):
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / rows
    for c in range(cols):
        for r in range(rows):
            ax = x0 + c * cw + cw * gap / 2
            bx = x0 + (c + 1) * cw - cw * gap / 2
            ay = y0 + r * ch + ch * gap / 2
            by = y0 + (r + 1) * ch - ch * gap / 2
            if fill:
                d.rectangle([ax, ay, bx, by], fill=fill)
            d.rectangle([ax, ay, bx, by], outline=col, width=w)


def base(pal):
    a, b, c = pal
    img = vgrad((W * S, H * S), a, b)
    img = radial_tint(img, (W * S * 0.72, H * S * 0.18), W * S * 0.85, c, 0.85)
    return img


def finish(img, name):
    img = img.resize((W, H), Image.LANCZOS)
    img = grain(img, 5)
    slug = SLUGS[name]
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    img.save(os.path.join(d, "cover.jpg"), quality=88, optimize=True)
    # 2 «λεπτομέρειες» = διαφορετικά κάδρα της ίδιας λήψης
    w, h = img.size
    for i, (x0, y0, x1, y1) in enumerate(DETAILS, start=1):
        c = img.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
        c = c.resize((1100, 1100), Image.LANCZOS)
        c.save(os.path.join(d, f"0{i}.jpg"), quality=88, optimize=True)
    print("wrote", d + "/  (cover, 01, 02)")


def d_of(img):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    return layer, ImageDraw.Draw(layer), layer


SHIFT = int(H * S * 0.065)   # ανεβάζει λίγο το «θέμα» μέσα στο κάδρο


def merge(img, layer):
    img.paste(layer, (0, -SHIFT), layer)
    return img


# ── 1. Μονοκατοικία ───────────────────────────────────────────
def work1():
    pal = PALETTES[0]
    img = base(pal)
    img = merge(img, grid(img, W * S, H * S, int(76 * S), INK, 20))
    layer, d, _ = d_of(img)
    w, h = img.size
    L = int(2.6 * S)
    d.line([(0.06 * w, 0.70 * h), (0.94 * w, 0.70 * h)], fill=INK + (205,), width=L)
    d.polygon([(0.20 * w, 0.70 * h), (0.20 * w, 0.46 * h), (0.50 * w, 0.30 * h), (0.80 * w, 0.46 * h), (0.80 * w, 0.70 * h)],
              outline=INK + (205,), width=L)
    windows(d, 0.26 * w, 0.50 * h, 0.44 * w, 0.64 * h, 2, 1, INK + (190,), 0.18, L)
    windows(d, 0.56 * w, 0.50 * h, 0.74 * w, 0.64 * h, 2, 1, INK + (190,), 0.18, L)
    d.rectangle([0.47 * w, 0.58 * h, 0.53 * w, 0.70 * h], outline=ACC + (220,), width=L)
    d.ellipse([0.83 * w, 0.16 * h, 0.93 * w, 0.26 * h], outline=INK + (205,), width=L)
    d.line([(0.13 * w, 0.70 * h), (0.13 * w, 0.63 * h)], fill=INK + (205,), width=L)
    d.ellipse([0.06 * w, 0.52 * h, 0.20 * w, 0.66 * h], outline=INK + (205,), width=L)
    d.line([(0.62 * w, 0.74 * h), (0.72 * w, 0.74 * h)], fill=ACC + (200,), width=L)
    finish(merge(img, layer), "work-1")


# ── 2. Κατάστημα ──────────────────────────────────────────────
def work2():
    pal = PALETTES[1]
    img = base(pal)
    img = merge(img, grid(img, W * S, H * S, int(76 * S), INK, 18))
    layer, d, _ = d_of(img)
    w, h = img.size
    L = int(2.6 * S)
    d.line([(0.05 * w, 0.72 * h), (0.95 * w, 0.72 * h)], fill=INK + (205,), width=L)
    d.rectangle([0.10 * w, 0.30 * h, 0.90 * w, 0.72 * h], outline=INK + (205,), width=L)
    for i in range(9):
        x = 0.10 * w + i * (0.80 * w / 9)
        d.line([(x, 0.30 * h), (x + 0.05 * w, 0.37 * h)], fill=INK + (185,), width=L)
    d.polygon([(0.10 * w, 0.30 * h), (0.90 * w, 0.30 * h), (0.96 * w, 0.37 * h), (0.04 * w, 0.37 * h)],
              outline=INK + (200,), width=L)
    windows(d, 0.15 * w, 0.44 * h, 0.85 * w, 0.66 * h, 3, 1, INK + (215,), 0.14, L)
    d.rectangle([0.44 * w, 0.50 * h, 0.56 * w, 0.72 * h], outline=ACC + (215,), width=L)
    finish(merge(img, layer), "work-2")


# ── 3. Πολυκατοικία ───────────────────────────────────────────
def work3():
    pal = PALETTES[2]
    img = base(pal)
    img = merge(img, grid(img, W * S, H * S, int(76 * S), INK, 18))
    layer, d, _ = d_of(img)
    w, h = img.size
    L = int(2.6 * S)
    d.line([(0.05 * w, 0.74 * h), (0.95 * w, 0.74 * h)], fill=INK + (205,), width=L)
    d.rectangle([0.16 * w, 0.20 * h, 0.84 * w, 0.74 * h], outline=INK + (205,), width=L)
    for r in range(4):
        y0 = 0.26 * h + r * 0.115 * h
        windows(d, 0.22 * w, y0, 0.78 * w, y0 + 0.075 * h, 4, 1, INK + (180,), 0.16, L)
        d.line([(0.19 * w, y0 + 0.095 * h), (0.81 * w, y0 + 0.095 * h)], fill=ACC + (150,), width=L)
    d.rectangle([0.46 * w, 0.66 * h, 0.54 * w, 0.74 * h], outline=INK + (200,), width=L)
    finish(merge(img, layer), "work-3")


# ── 4. Εσωτερικός χώρος (one-point) ───────────────────────────
def work4():
    pal = PALETTES[3]
    img = base(pal)
    img = merge(img, grid(img, W * S, H * S, int(76 * S), INK, 18))
    layer, d, _ = d_of(img)
    w, h = img.size
    L = int(2.6 * S)
    vx, vy = 0.56 * w, 0.48 * h
    d.rectangle([0.07 * w, 0.16 * h, 0.93 * w, 0.86 * h], outline=INK + (200,), width=L)
    for cx, cy in [(0.07, 0.16), (0.93, 0.16), (0.07, 0.86), (0.93, 0.86)]:
        d.line([(cx * w, cy * h), (vx, vy)], fill=INK + (150,), width=L)
    d.rectangle([0.36 * w, 0.38 * h, 0.74 * w, 0.58 * h], outline=INK + (200,), width=L)
    d.line([(0.36 * w, 0.48 * h), (0.74 * w, 0.48 * h)], fill=INK + (140,), width=L)
    d.line([(0.44 * w, 0.58 * h), (0.44 * w, 0.70 * h)], fill=INK + (180,), width=L)
    d.line([(0.66 * w, 0.58 * h), (0.66 * w, 0.70 * h)], fill=INK + (180,), width=L)
    d.ellipse([0.78 * w, 0.30 * h, 0.86 * w, 0.42 * h], outline=ACC + (210,), width=L)
    d.line([(0.82 * w, 0.42 * h), (0.82 * w, 0.62 * h)], fill=ACC + (200,), width=L)
    d.polygon([(0.22 * w, 0.80 * h), (0.50 * w, 0.74 * h), (0.66 * w, 0.80 * h), (0.38 * w, 0.87 * h)],
              outline=INK + (185,), width=L)
    finish(merge(img, layer), "work-4")


# ── 5. Γραφεία / skyline ──────────────────────────────────────
def work5():
    pal = PALETTES[4]
    img = base(pal)
    img = merge(img, grid(img, W * S, H * S, int(76 * S), INK, 18))
    layer, d, _ = d_of(img)
    w, h = img.size
    L = int(2.6 * S)
    d.line([(0.05 * w, 0.76 * h), (0.95 * w, 0.76 * h)], fill=INK + (205,), width=L)
    towers = [(0.12, 0.40), (0.33, 0.26), (0.55, 0.34), (0.76, 0.48)]
    for i, (x, top) in enumerate(towers):
        x0, x1 = x * w, (x + 0.15) * w
        d.rectangle([x0, top * h, x1, 0.76 * h], outline=INK + (200,), width=L)
        cols = 3
        rows = max(2, int((0.76 - top) / 0.075))
        windows(d, x0, top * h, x1, 0.76 * h, cols, rows, INK + (185,), 0.22, max(1, L - 1))
        if i == 1:
            d.line([(x0 + 0.005 * w, top * h - 0.03 * h), (x1 - 0.005 * w, top * h - 0.03 * h)], fill=ACC + (210,), width=L)
    finish(merge(img, layer), "work-5")


# ── 6. Ξενοδοχειακός χώρος (lobby) ────────────────────────────
def work6():
    pal = PALETTES[5]
    img = base(pal)
    img = merge(img, grid(img, W * S, H * S, int(76 * S), INK, 18))
    layer, d, _ = d_of(img)
    w, h = img.size
    L = int(2.6 * S)
    d.line([(0.06 * w, 0.78 * h), (0.94 * w, 0.78 * h)], fill=INK + (205,), width=L)
    for x in (0.18, 0.42, 0.66, 0.88):
        d.line([(x * w, 0.28 * h), (x * w, 0.78 * h)], fill=INK + (215,), width=L)
    d.arc([0.10 * w, 0.10 * h, 0.94 * w, 0.52 * h], 180, 360, fill=INK + (160,), width=L)
    for i in range(4):
        y = 0.78 * h + i * 0.035 * h
        d.line([(0.30 * w + i * 0.012 * w, y), (0.72 * w - i * 0.012 * w, y)], fill=INK + (185,), width=L)
    d.line([(0.50 * w, 0.22 * h), (0.50 * w, 0.32 * h)], fill=ACC + (220,), width=L)
    d.ellipse([0.46 * w, 0.32 * h, 0.54 * w, 0.38 * h], outline=ACC + (220,), width=L)
    finish(merge(img, layer), "work-6")


for fn in (work1, work2, work3, work4, work5, work6):
    fn()


# ── 7. Café ───────────────────────────────────────────────────
def work7():
    img = base(PALETTES[1]); img = merge(img, grid(img, W*S, H*S, int(76*S), INK, 18))
    layer, d, _ = d_of(img); w, h = img.size; L = int(4.0*S)
    d.line([(0.05*w,0.78*h),(0.95*w,0.78*h)], fill=INK+(205,), width=L)
    d.rectangle([0.12*w,0.56*h,0.88*w,0.78*h], outline=INK+(210,), width=L)
    d.line([(0.12*w,0.62*h),(0.88*w,0.62*h)], fill=INK+(170,), width=L)
    for x in (0.26,0.5,0.74):
        d.ellipse([(x-0.045)*w,0.44*h,(x+0.045)*w,0.50*h], outline=INK+(200,), width=L)
        d.line([(x*w,0.50*h),(x*w,0.78*h)], fill=INK+(170,), width=L)
    for x in (0.3,0.7):
        d.line([(x*w,0.10*h),(x*w,0.24*h)], fill=INK+(180,), width=L)
        d.ellipse([(x-0.035)*w,0.24*h,(x+0.035)*w,0.31*h], outline=ACC+(215,), width=L)
    d.rectangle([0.68*w,0.64*h,0.86*w,0.74*h], outline=INK+(170,), width=L)
    finish(merge(img, layer), "work-7")

# ── 8. Εστιατόριο ─────────────────────────────────────────────
def work8():
    img = base(PALETTES[2]); img = merge(img, grid(img, W*S, H*S, int(76*S), INK, 18))
    layer, d, _ = d_of(img); w, h = img.size; L = int(4.0*S)
    d.line([(0.05*w,0.80*h),(0.95*w,0.80*h)], fill=INK+(205,), width=L)
    d.rectangle([0.10*w,0.14*h,0.58*w,0.52*h], outline=INK+(200,), width=L)
    windows(d, 0.10*w, 0.14*h, 0.58*w, 0.52*h, 3, 2, INK+(150,), 0.14, max(1,L-1))
    d.ellipse([0.30*w,0.60*h,0.74*w,0.70*h], outline=INK+(205,), width=L)
    d.line([(0.52*w,0.70*h),(0.52*w,0.80*h)], fill=INK+(180,), width=L)
    for x in (0.32,0.62):
        d.rectangle([x*w,0.64*h,(x+0.09)*w,0.78*h], outline=INK+(175,), width=L)
    d.line([(0.66*w,0.12*h),(0.66*w,0.26*h)], fill=INK+(180,), width=L)
    d.ellipse([0.61*w,0.26*h,0.71*w,0.34*h], outline=ACC+(215,), width=L)
    finish(merge(img, layer), "work-8")

# ── 9. Γραφεία ────────────────────────────────────────────────
def work9():
    img = base(PALETTES[4]); img = merge(img, grid(img, W*S, H*S, int(76*S), INK, 18))
    layer, d, _ = d_of(img); w, h = img.size; L = int(4.0*S)
    d.line([(0.05*w,0.80*h),(0.95*w,0.80*h)], fill=INK+(205,), width=L)
    d.line([(0.50*w,0.30*h),(0.50*w,0.80*h)], fill=INK+(150,), width=L)
    for x in (0.14,0.60):
        d.rectangle([x*w,0.55*h,(x+0.26)*w,0.60*h], outline=INK+(205,), width=L)
        for lx in (x+0.02, x+0.22):
            d.line([(lx*w,0.60*h),(lx*w,0.80*h)], fill=INK+(170,), width=L)
        d.rectangle([(x+0.07)*w,0.42*h,(x+0.17)*w,0.55*h], outline=INK+(175,), width=L)
        d.rectangle([(x+0.05)*w,0.30*h,(x+0.21)*w,0.38*h], outline=ACC+(200,), width=L)
    finish(merge(img, layer), "work-9")

# ── 10. Showroom / Retail ─────────────────────────────────────
def work10():
    img = base(PALETTES[3]); img = merge(img, grid(img, W*S, H*S, int(76*S), INK, 18))
    layer, d, _ = d_of(img); w, h = img.size; L = int(4.0*S)
    d.line([(0.05*w,0.82*h),(0.95*w,0.82*h)], fill=INK+(205,), width=L)
    for i,y in enumerate((0.28,0.46,0.64)):
        d.line([(0.12*w,y*h),(0.88*w,y*h)], fill=INK+(200,), width=L)
        for k in range(1,5):
            d.line([(0.12*w+k*0.19*w,y*h),(0.12*w+k*0.19*w,y*h+0.035*h)], fill=INK+(160,), width=L)
        d.rectangle([(0.20+i*0.14)*w,(y-0.10)*h,(0.28+i*0.14)*w,y*h], outline=INK+(180,), width=L)
    d.rectangle([0.62*w,0.70*h,0.88*w,0.82*h], outline=ACC+(205,), width=L)
    finish(merge(img, layer), "work-10")

# ── 11. Villa / εξωτερικός χώρος ──────────────────────────────
def work11():
    img = base(PALETTES[0]); img = merge(img, grid(img, W*S, H*S, int(76*S), INK, 18))
    layer, d, _ = d_of(img); w, h = img.size; L = int(4.0*S)
    d.line([(0.05*w,0.66*h),(0.95*w,0.66*h)], fill=INK+(205,), width=L)
    d.rectangle([0.14*w,0.40*h,0.86*w,0.58*h], outline=INK+(210,), width=L)
    d.rectangle([0.20*w,0.24*h,0.56*w,0.40*h], outline=INK+(205,), width=L)
    d.line([(0.14*w,0.58*h),(0.86*w,0.58*h)], fill=INK+(160,), width=L)
    windows(d, 0.60*w, 0.44*h, 0.82*w, 0.56*h, 3, 1, INK+(180,), 0.16, max(1,L-1))
    d.rectangle([0.22*w,0.70*h,0.78*w,0.82*h], outline=INK+(185,), width=L)
    for i in range(4):
        d.line([(0.24*w+i*0.13*w,0.72*h),(0.30*w+i*0.13*w,0.80*h)], fill=ACC+(150,), width=max(1,L-2))
    d.ellipse([0.88*w,0.16*h,0.96*w,0.24*h], outline=INK+(170,), width=L)
    finish(merge(img, layer), "work-11")

# ── 12. Δωμάτιο ξενοδοχείου ───────────────────────────────────
def work12():
    img = base(PALETTES[5]); img = merge(img, grid(img, W*S, H*S, int(76*S), INK, 18))
    layer, d, _ = d_of(img); w, h = img.size; L = int(4.0*S)
    d.line([(0.05*w,0.82*h),(0.95*w,0.82*h)], fill=INK+(205,), width=L)
    d.rectangle([0.16*w,0.72*h,0.80*w,0.82*h], outline=INK+(205,), width=L)
    d.rectangle([0.14*w,0.44*h,0.82*w,0.72*h], outline=INK+(210,), width=L)
    d.rectangle([0.20*w,0.40*h,0.40*w,0.46*h], outline=INK+(175,), width=L)
    d.rectangle([0.46*w,0.40*h,0.66*w,0.46*h], outline=INK+(175,), width=L)
    d.rectangle([0.84*w,0.58*h,0.94*w,0.72*h], outline=INK+(180,), width=L)
    d.ellipse([0.86*w,0.50*h,0.92*w,0.58*h], outline=ACC+(210,), width=L)
    d.rectangle([0.24*w,0.14*h,0.52*w,0.32*h], outline=INK+(190,), width=L)
    d.line([(0.28*w,0.23*h),(0.48*w,0.23*h)], fill=INK+(150,), width=max(1,L-1))
    finish(merge(img, layer), "work-12")

for fn in (work7, work8, work9, work10, work11, work12):
    fn()
