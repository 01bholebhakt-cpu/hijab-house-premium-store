"""Renders illustrative, locally-stored product images (no external downloads).
These are DEMONSTRATION renders. Replace with the owner's real photographs (see README).
Run:  python3 tools/gen_images.py
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import PRODUCTS, slug

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "products")
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

W0, H0 = 800, 1000
RNG = np.random.RandomState(7)


# ------------------------------------------------------------------ helpers
def hx(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def blur(a, r):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    im = im.filter(ImageFilter.GaussianBlur(r))
    return np.asarray(im, dtype=np.float32) / 255.0


def grid(w, h):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    return x, y


def save(img, path, q=82):
    arr = np.clip(img, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(path, "JPEG", quality=q, optimize=True, progressive=True)


def bg(w, h, c1, c2, light=(0.35, 0.22)):
    x, y = grid(w, h)
    x /= w
    y /= h
    t = np.clip(0.6 * y + 0.2 * x, 0, 1)[..., None]
    base = hx(c1) * (1 - t) + hx(c2) * t
    d = np.sqrt((x - light[0]) ** 2 + ((y - light[1]) * 1.1) ** 2)
    base = base * (1.10 - 0.42 * d)[..., None]
    base += np.random.normal(0, 1.3, (h, w, 1))
    return base.astype(np.float32)


def paste(img, rgb, a, x0, y0):
    H, W = img.shape[:2]
    h, w = a.shape
    xa, ya = max(0, x0), max(0, y0)
    xb, yb = min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya:
        return
    sub = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0))
    al = a[sub][..., None]
    img[ya:yb, xa:xb] = img[ya:yb, xa:xb] * (1 - al) + rgb[sub] * al


def drop_shadow(img, a, x0, y0, off=(16, 24), r=20, k=0.38, tint=(60, 40, 30)):
    H, W = img.shape[:2]
    layer = np.zeros((H, W), np.float32)
    h, w = a.shape
    xa, ya = x0 + off[0], y0 + off[1]
    xs, ys = max(0, xa), max(0, ya)
    xe, ye = min(W, xa + w), min(H, ya + h)
    if xe > xs and ye > ys:
        layer[ys:ye, xs:xe] = a[ys - ya:ye - ya, xs - xa:xe - xa]
    layer = blur(layer, r) * k
    img[:] = img * (1 - layer[..., None]) + np.array(tint, np.float32) * layer[..., None] * 0.6


def place(img, rgb, a, x0, y0, **kw):
    drop_shadow(img, a, x0, y0, **kw)
    paste(img, rgb, a, x0, y0)


def draw_mask(w, h, fn, ss=2):
    im = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    fn(d, ss)
    im = im.resize((w, h), Image.LANCZOS)
    return np.asarray(im, np.float32) / 255.0


# ------------------------------------------------------------------ fabric
def fabric_field(w, h, col, k=3.2, theta=0.35, seed=0, weave=0.02, sheen=0.16, light=(0.3, 0.2)):
    x, y = grid(w, h)
    x /= w
    y /= h
    s = x * math.cos(theta) + y * math.sin(theta)
    phase = s * k * math.pi * 2 + 1.1 * np.sin(y * 3.2 + x * 2.0 + seed) + 0.5 * np.sin(x * 7 + seed * 2)
    fold = np.sin(phase)
    shade = 0.80 + 0.20 * fold + 0.05 * np.sin(phase * 2.3 + 1.0)
    d = np.sqrt((x - light[0]) ** 2 + (y - light[1]) ** 2)
    shade *= 1.12 - 0.4 * d
    rgb = col[None, None, :] * shade[..., None]
    sp = np.clip(fold, 0, 1) ** 8 * sheen
    rgb += sp[..., None] * (255 - col) * 0.9
    wv = np.sin(x * w * 1.9) * np.sin(y * h * 1.9) * weave + np.random.normal(0, 0.012, (h, w))
    return rgb * (1 + wv)[..., None]


def scarf(w, h, col, pcol=None, seed=0):
    """A hijab hanging from a gathered point at the top. Returns rgb, alpha."""
    x, y = grid(w, h)
    x /= w
    y /= h
    cx = 0.5 + 0.025 * np.sin(y * 4.2 + seed)
    hwid = 0.075 + 0.415 * sstep(0.0, 0.62, y) ** 0.8
    u = (x - cx) / hwid
    bottom = 0.965 - 0.022 * np.sin(x * 15 + seed) - 0.012 * np.sin(x * 33)
    alpha = np.clip((1 - np.abs(u)) * hwid * w / 1.2, 0, 1) * np.clip((bottom - y) * h / 1.5, 0, 1)

    base = np.ones((h, w, 3), np.float32) * col
    if pcol is not None:
        pm = draw_mask(w, h, lambda d, ss: _flowers(d, ss, w, h, seed), ss=1)
        base = base * (1 - pm[..., None]) + pcol * pm[..., None]

    phase = u * 3.6 * math.pi + 1.3 * np.sin(y * 5.5 + u * 1.7 + seed)
    fold = np.sin(phase)
    fold2 = np.sin(u * 4.25 * math.pi + y * 3 + seed * 1.3)
    shade = 0.80 + 0.20 * fold + 0.06 * fold2
    shade *= 1 - 0.20 * u ** 2
    shade += 0.10 * np.sin(u * 14 * math.pi) * sstep(0.22, 0.0, y)
    shade *= 1 - 0.18 * sstep(0.12, 0.0, y)
    dist_b = (bottom - y)
    shade *= 1 - 0.10 * (dist_b < 0.014)
    shade += 0.05 * np.exp(-(((dist_b - 0.02) * h / 1.6) ** 2))
    rgb = base * shade[..., None]
    sp = np.clip(fold, 0, 1) ** 8 * (1 - np.abs(u)) * 0.22
    rgb += sp[..., None] * (255 - base) * 0.9
    wv = np.sin(x * w * 1.9) * np.sin(y * h * 1.9) * 0.018 + np.random.normal(0, 0.014, (h, w))
    rgb *= (1 + wv)[..., None]
    return rgb.astype(np.float32), alpha.astype(np.float32)


def _flowers(d, ss, w, h, seed):
    r = np.random.RandomState(seed + 3)
    step = 58
    for gy in range(-1, h // step + 2):
        for gx in range(-1, w // step + 2):
            ox = gx * step + (step // 2 if gy % 2 else 0) + r.randint(-6, 7)
            oy = gy * step + r.randint(-6, 7)
            for k in range(5):
                a = k * 2 * math.pi / 5
                px, py = ox + math.cos(a) * 9, oy + math.sin(a) * 9
                d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=255)
            d.ellipse([ox - 4, oy - 4, ox + 4, oy + 4], fill=0)


def rod(img, y, x0, x1, th=16, col=(205, 168, 82)):
    H, W = img.shape[:2]
    ys = np.arange(max(0, y - th), min(H, y + th))
    t = (ys - y) / th
    sh = np.sqrt(np.clip(1 - t ** 2, 0, 1))
    c = np.array(col, np.float32)
    band = c[None, :] * (0.45 + 0.65 * sh[:, None]) + (255 - c)[None, :] * (np.clip(sh - 0.85, 0, 1) * 3.5)[:, None] * 0.6
    x0, x1 = max(0, x0), min(W, x1)
    sub = img[ys[0]:ys[-1] + 1, x0:x1]
    a = (sh > 0.02).astype(np.float32)[:, None, None]
    img[ys[0]:ys[-1] + 1, x0:x1] = sub * (1 - a) + band[:, None, :] * a
    for xe in (x0 + 4, x1 - 4):
        sphere(img, xe, y, th * 1.25, np.array(col, np.float32))


def sphere(img, cx, cy, r, base, spec=0.9, gloss=28):
    H, W = img.shape[:2]
    x0, x1 = int(max(0, cx - r - 3)), int(min(W, cx + r + 3))
    y0, y1 = int(max(0, cy - r - 3)), int(min(H, cy + r + 3))
    if x1 <= x0 or y1 <= y0:
        return
    xs, ys = np.meshgrid(np.arange(x0, x1, dtype=np.float32), np.arange(y0, y1, dtype=np.float32))
    dx, dy = (xs - cx), (ys - cy)
    d = np.sqrt(dx ** 2 + dy ** 2)
    a = np.clip(r - d + 0.5, 0, 1)
    nx, ny = dx / r, dy / r
    z = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
    lam = np.clip(-0.38 * nx - 0.48 * ny + 0.79 * z, 0, 1)
    shade = 0.32 + 0.68 * lam
    shade *= 1 - 0.25 * (d / r) ** 4
    rgb = base[None, None, :] * shade[..., None]
    sp = np.clip(-0.38 * nx - 0.48 * ny + 0.79 * z - 0.0, 0, 1) ** gloss * spec
    rgb = rgb + sp[..., None] * (255 - rgb)
    al = a[..., None]
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - al) + rgb * al


def metal(img, mask, base, bevel=5, shadow=True):
    """Embossed metal from a 0..1 mask the size of img."""
    H, W = mask.shape
    if shadow:
        drop_shadow(img, mask, 0, 0, off=(5, 8), r=6, k=0.45)
    hgt = blur(mask, bevel)
    gy, gx = np.gradient(hgt)
    light = np.clip(0.78 + (-gx * 0.9 - gy * 1.1) * bevel * 2.4, 0.30, 1.45)
    xx, yy = grid(W, H)
    grad = 0.93 + 0.07 * np.sin((xx + yy) / 38.0)
    col = base[None, None, :] * (light * grad)[..., None]
    spec = np.clip((-gx - gy) * bevel * 3.4 - 0.5, 0, 1) ** 1.4
    col = col + spec[..., None] * (255 - col) * 0.75
    a = mask[..., None]
    img[:] = img * (1 - a) + col * a


# ------------------------------------------------------------------ scenes: hijab
def rod_scene_bg(W, H, bgc):
    return bg(W, H, *bgc)


def scene_scarf(col, pcol=None, seed=0, W=W0, H=H0, bgc=("#f7f0e6", "#ead7cd")):
    img = bg(W, H, *bgc)
    sw, sh = int(W * 0.80), int(H * 0.88)
    sx, sy = (W - sw) // 2, int(H * 0.085)
    rgb, a = scarf(sw, sh, hx(col), hx(pcol) if pcol else None, seed)
    place(img, rgb, a, sx, sy)
    rod(img, sy + 6, int(W * 0.06), int(W * 0.94))
    return img


def detail_scarf(col, pcol=None, seed=0, W=W0, H=H0):
    f = fabric_field(W, H, hx(col), k=1.9, theta=0.9, seed=seed, weave=0.05, sheen=0.2)
    if pcol is not None:
        pm = draw_mask(W, H, lambda d, ss: _flowers_big(d, ss, W, H), ss=1)
        pm = blur(pm, 1.0)
        f = f * (1 - pm[..., None]) + (hx(pcol)[None, None, :] * (f.mean(axis=2, keepdims=True) / max(1, hx(col).mean()))) * pm[..., None]
    # a folded crease
    x, y = grid(W, H)
    crease = np.exp(-(((x * 0.55 + y * 0.83) - 0.62 * W) / 28.0) ** 2)
    f *= (1 - 0.35 * crease)[..., None]
    f *= (1 + 0.18 * np.exp(-(((x * 0.55 + y * 0.83) - 0.62 * W + 40) / 22.0) ** 2))[..., None]
    return f


def _flowers_big(d, ss, w, h):
    step = 130
    for gy in range(-1, h // step + 2):
        for gx in range(-1, w // step + 2):
            ox = gx * step + (step // 2 if gy % 2 else 0)
            oy = gy * step
            for k in range(5):
                a = k * 2 * math.pi / 5
                px, py = ox + math.cos(a) * 20, oy + math.sin(a) * 20
                d.ellipse([px - 16, py - 16, px + 16, py + 16], fill=255)
            d.ellipse([ox - 9, oy - 9, ox + 9, oy + 9], fill=0)


# ------------------------------------------------------------------ scenes: caps
def cap(w, h, col, kind):
    x, y = grid(w, h)
    x /= w
    y /= h
    cxm, cyc, rx, ry = 0.5, 0.50, 0.40, 0.43
    nx = (x - cxm) / rx
    ny = (y - cyc) / ry
    r = np.sqrt(nx ** 2 + ny ** 2)
    a_top = np.clip(0.5 - (r - 1) * rx * w, 0, 1)
    bottom = 0.92 + 0.025 * np.sin(nx * 2.2)
    if kind == "cap_lace":
        bottom = 0.93 + 0.012 * np.abs(np.sin(x * w * 0.2))
    t = np.clip((y - cyc) / 0.42, 0, 1)
    a_body = np.clip((1 - 0.05 * t - np.abs(nx)) * rx * w + 0.5, 0, 1) * np.clip((bottom - y) * h + 0.5, 0, 1)
    alpha = np.where(y < cyc, a_top, a_body)
    nyb = np.where(y < cyc, ny, (y - cyc) * 0.5)
    nxb = np.where(y < cyc, nx, nx / (1 - 0.05 * t))
    z = np.sqrt(np.clip(1 - nxb ** 2 - nyb ** 2, 0, 1))
    lam = np.clip(-0.42 * nxb - 0.52 * nyb + 0.74 * z, 0, 1)
    shade = 0.40 + 0.60 * lam
    c = np.ones((h, w, 3), np.float32) * col
    if kind == "cap_tube":
        ribs = 0.5 + 0.5 * np.sin(x * w * 0.50)
        shade *= 0.88 + 0.12 * ribs
    else:
        shade *= 1 + 0.045 * np.sin(x * w * 1.2) + 0.035 * np.sin(y * h * 1.2)
    if kind == "cap_bonnet":
        band = sstep(0.70, 0.72, y) * (1 - sstep(0.80, 0.82, y))
        shade *= 1 - 0.10 * band
        shade += 0.04 * np.exp(-(((y - 0.70) * h / 2) ** 2))
    if kind == "cap_lace":
        ly = (y > 0.80).astype(np.float32)
        lace = np.ones(3, np.float32) * np.array([245, 238, 226], np.float32)
        holes = (((x * w) % 18 - 9) ** 2 + ((y * h) % 18 - 9) ** 2 < 12).astype(np.float32)
        c = c * (1 - ly[..., None] * 0.85) + lace * ly[..., None] * 0.85
        shade *= 1 - 0.22 * holes * ly
    rgb = c * shade[..., None]
    sp = np.clip(lam - 0.80, 0, 1) ** 1.3 * 0.9
    rgb += sp[..., None] * (255 - rgb) * 0.5
    rgb *= (1 + np.random.normal(0, 0.012, (h, w)))[..., None]
    return rgb.astype(np.float32), alpha.astype(np.float32)


def bow(img, cx, cy, s, col):
    H, W = img.shape[:2]

    def fn(d, ss):
        for sgn in (-1, 1):
            pts = [(cx, cy), (cx + sgn * s * 1.1, cy - s * 0.65), (cx + sgn * s * 1.25, cy + s * 0.6)]
            d.polygon([(px * ss, py * ss) for px, py in pts], fill=255)
        d.ellipse([(cx - s * 0.28) * ss, (cy - s * 0.28) * ss, (cx + s * 0.28) * ss, (cy + s * 0.28) * ss], fill=255)

    m = draw_mask(W, H, fn)
    drop_shadow(img, m, 0, 0, off=(5, 8), r=6, k=0.4)
    hgt = blur(m, 3)
    gy, gx = np.gradient(hgt)
    light = np.clip(0.9 + (-gx * 0.9 - gy * 1.1) * 7, 0.45, 1.35)
    rgbc = col[None, None, :] * light[..., None]
    img[:] = img * (1 - m[..., None]) + rgbc * m[..., None]


def scene_cap(col, kind, W=W0, H=H0, bgc=("#f8f1e8", "#ecd9cf"), scale=0.86, dx=0, dy=0, shadow=True):
    img = bg(W, H, *bgc) if bgc else None
    return img


def draw_cap_on(img, col, kind, cx, cy, cw, ch):
    rgb, a = cap(cw, ch, hx(col), kind)
    x0, y0 = int(cx - cw / 2), int(cy - ch / 2)
    # ground shadow
    H, W = img.shape[:2]
    gl = np.zeros((H, W), np.float32)
    gimg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(gimg).ellipse([cx - cw * 0.46, y0 + ch * 0.90, cx + cw * 0.46, y0 + ch * 1.0], fill=255)
    gl = np.asarray(gimg.filter(ImageFilter.GaussianBlur(14)), np.float32) / 255 * 0.5
    img[:] = img * (1 - gl[..., None]) + np.array([60, 40, 30], np.float32) * gl[..., None] * 0.5
    paste(img, rgb, a, x0, y0)
    if kind == "cap_bonnet":
        bow(img, cx + cw * 0.22, y0 + ch * 0.76, cw * 0.075, hx(col) * 0.85 + 20)


def render_cap(col, kind, W=W0, H=H0, bgc=("#f8f1e8", "#ecd9cf")):
    img = bg(W, H, *bgc)
    # table surface
    x, y = grid(W, H)
    surf = sstep(0.80, 0.84, y / H)
    img *= (1 - 0.06 * surf)[..., None]
    cw, ch = int(W * 0.84), int(H * 0.62)
    draw_cap_on(img, col, kind, W / 2, H * 0.50, cw, ch)
    return img


def detail_cap(col, kind, W=W0, H=H0):
    c = hx(col)
    x, y = grid(W, H)
    nx = (x / W - 0.5)
    shade = 0.78 + 0.28 * np.cos(nx * 2.2)
    if kind == "cap_tube":
        shade *= 0.80 + 0.20 * (0.5 + 0.5 * np.sin(x * 0.42))
    else:
        shade *= 1 + 0.10 * np.sin(x * 0.62) * np.sin(y * 0.18 + 0.4 * np.sin(x * 0.05))
        shade *= 1 + 0.05 * np.sin(y * 0.62)
    shade *= 1.05 - 0.45 * np.sqrt((x / W - 0.3) ** 2 + (y / H - 0.2) ** 2)
    rgb = c[None, None, :] * shade[..., None]
    rgb += (np.clip(shade - 1.0, 0, 1) ** 1.2 * 0.8)[..., None] * (255 - rgb) * 0.4
    if kind == "cap_lace":
        holes = (((x) % 26 - 13) ** 2 + ((y) % 26 - 13) ** 2 < 24).astype(np.float32)
        rgb = rgb * (1 - 0.3 * holes[..., None])
    return rgb + np.random.normal(0, 1.5, (H, W, 1))


# ------------------------------------------------------------------ scenes: accessories
def circle_mask(W, H, cx, cy, r):
    return draw_mask(W, H, lambda d, ss: d.ellipse([(cx - r) * ss, (cy - r) * ss, (cx + r) * ss, (cy + r) * ss], fill=255))


def ell_pts(cx, cy, a, b, ang, n=48):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        px, py = a * math.cos(t), b * math.sin(t)
        pts.append((cx + px * math.cos(ang) - py * math.sin(ang), cy + px * math.sin(ang) + py * math.cos(ang)))
    return pts


PEARL = np.array([245, 236, 232], np.float32)
CRYSTAL = np.array([235, 242, 250], np.float32)
ROSEGEM = np.array([214, 120, 140], np.float32)
EMGEM = np.array([40, 150, 110], np.float32)


def draw_floral(img, cx, cy, s, mcol, gem=ROSEGEM):
    H, W = img.shape[:2]

    def petals(d, ss, n=8, a=0.30, b=0.14, off=0.30, rot=0.0):
        for k in range(n):
            ang = k * 2 * math.pi / n + rot
            ex, ey = cx + math.cos(ang) * off * s, cy + math.sin(ang) * off * s
            d.polygon([(px * ss, py * ss) for px, py in ell_pts(ex, ey, a * s, b * s, ang)], fill=255)

    m1 = draw_mask(W, H, lambda d, ss: petals(d, ss))
    metal(img, m1, mcol, bevel=5)
    m2 = draw_mask(W, H, lambda d, ss: petals(d, ss, 8, 0.20, 0.085, 0.24, math.pi / 8))
    metal(img, m2, np.minimum(mcol * 1.12 + 10, 255), bevel=3, shadow=False)
    m3 = circle_mask(W, H, cx, cy, 0.22 * s)
    metal(img, m3, mcol * 0.95, bevel=4)
    sphere(img, cx, cy, 0.145 * s, gem, gloss=22)
    for k in range(8):
        ang = k * 2 * math.pi / 8
        sphere(img, cx + math.cos(ang) * 0.52 * s, cy + math.sin(ang) * 0.52 * s, 0.032 * s, CRYSTAL, gloss=18)


def draw_star(img, cx, cy, s, mcol, gem=CRYSTAL):
    H, W = img.shape[:2]

    def star(d, ss, ro, ri, n=8, rot=-math.pi / 2):
        pts = []
        for i in range(n * 2):
            r = ro if i % 2 == 0 else ri
            a = rot + i * math.pi / n
            pts.append(((cx + math.cos(a) * r * s) * ss, (cy + math.sin(a) * r * s) * ss))
        d.polygon(pts, fill=255)

    m1 = draw_mask(W, H, lambda d, ss: star(d, ss, 0.55, 0.27))
    metal(img, m1, mcol, bevel=5)
    m2 = draw_mask(W, H, lambda d, ss: star(d, ss, 0.40, 0.19, 8, -math.pi / 2 + math.pi / 8))
    metal(img, m2, np.minimum(mcol * 1.1 + 12, 255), bevel=3, shadow=False)
    sphere(img, cx, cy, 0.17 * s, gem, gloss=20)
    for k in range(8):
        a = -math.pi / 2 + k * math.pi / 4
        sphere(img, cx + math.cos(a) * 0.44 * s, cy + math.sin(a) * 0.44 * s, 0.045 * s, CRYSTAL, gloss=16)


def draw_pin(img, hx_, hy, tx, ty, mcol, head="pearl", hr=20, wid=4):
    H, W = img.shape[:2]

    def fn(d, ss):
        d.line([(hx_ * ss, hy * ss), (tx * ss, ty * ss)], fill=255, width=int(wid * ss))
        d.polygon([(tx * ss, ty * ss)] + [(tx * ss, ty * ss)], fill=255)

    m = draw_mask(W, H, fn)
    metal(img, m, mcol, bevel=2)
    col = {"pearl": PEARL, "crystal": CRYSTAL, "rose": ROSEGEM, "emerald": EMGEM, "gold": mcol}[head]
    drop = np.zeros((H, W), np.float32)
    drop_shadow(img, circle_mask(W, H, hx_, hy, hr), 0, 0, off=(5, 8), r=6, k=0.45)
    sphere(img, hx_, hy, hr, col, gloss=26)


def draw_pearlpins(img, cx, cy, s, mcol):
    for i, ang in enumerate([-0.42, -0.21, 0.0, 0.21, 0.42]):
        L = 0.95 * s
        hx_ = cx + math.sin(ang) * L * 0.5
        hy = cy - math.cos(ang) * L * 0.5
        tx = cx - math.sin(ang) * L * 0.5
        ty = cy + math.cos(ang) * L * 0.5
        draw_pin(img, hx_, hy, tx, ty, mcol, "pearl", hr=0.075 * s, wid=max(3, 0.012 * s))


def draw_magpins(img, cx, cy, s, mcol):
    H, W = img.shape[:2]
    spots = [(cx - 0.30 * s, cy - 0.22 * s, PEARL), (cx + 0.32 * s, cy - 0.10 * s, ROSEGEM), (cx - 0.02 * s, cy + 0.30 * s, CRYSTAL)]
    for (px, py, gem) in spots:
        r = 0.27 * s
        back = circle_mask(W, H, px + r * 0.9, py + r * 0.55, r * 0.62)
        metal(img, back, mcol * 0.85, bevel=4)
        m = circle_mask(W, H, px, py, r)
        metal(img, m, mcol, bevel=7)
        ring = circle_mask(W, H, px, py, r * 0.72)
        metal(img, ring, np.minimum(mcol * 1.1 + 8, 255), bevel=4, shadow=False)
        sphere(img, px, py, r * 0.50, gem, gloss=24)


def draw_clip(img, cx, cy, s, mcol):
    H, W = img.shape[:2]

    def fn(d, ss):
        r = 0.46 * s
        d.ellipse([(cx - r) * ss, (cy - r) * ss, (cx + r) * ss, (cy + r) * ss], fill=255)
        r2 = 0.38 * s
        ox, oy = 0.15 * s, -0.10 * s
        d.ellipse([(cx + ox - r2) * ss, (cy + oy - r2) * ss, (cx + ox + r2) * ss, (cy + oy + r2) * ss], fill=0)

    m = draw_mask(W, H, fn)
    metal(img, m, mcol, bevel=5)
    sphere(img, cx - 0.30 * s, cy - 0.28 * s, 0.065 * s, PEARL, gloss=24)
    sphere(img, cx - 0.12 * s, cy + 0.42 * s, 0.05 * s, PEARL, gloss=24)
    sphere(img, cx - 0.42 * s, cy + 0.10 * s, 0.045 * s, CRYSTAL, gloss=18)


def draw_pinpack(img, cx, cy, s, mcol):
    H, W = img.shape[:2]
    cw, chh = 0.95 * s, 1.15 * s
    card = draw_mask(W, H, lambda d, ss: d.rounded_rectangle([(cx - cw / 2) * ss, (cy - chh / 2) * ss, (cx + cw / 2) * ss, (cy + chh / 2) * ss], radius=14 * ss, fill=255))
    drop_shadow(img, card, 0, 0, off=(10, 16), r=14, k=0.45)
    gx, gy = grid(W, H)
    paper = np.array([243, 236, 224], np.float32)[None, None, :] * (0.96 + 0.04 * np.sin(gx / 30))[..., None]
    img[:] = img * (1 - card[..., None]) + paper * card[..., None]
    heads = ["pearl", "crystal", "rose", "gold", "emerald", "pearl"]
    for i in range(6):
        yy = cy - chh / 2 + 0.14 * s + i * 0.19 * s
        draw_pin(img, cx - cw / 2 + 0.17 * s, yy, cx + cw / 2 - 0.12 * s, yy, mcol, heads[i], hr=0.058 * s, wid=max(3, 0.011 * s))


ACC = dict(magpin=draw_magpins, pearlpin=draw_pearlpins, brooch_floral=draw_floral, brooch_star=draw_star, clip=draw_clip, pinpack=draw_pinpack)
ACC_BG = {"Gold": "#0f4a3a", "Silver": "#2a3552", "Rose Gold": "#5a3d33", "Mixed": "#0f4a3a"}


def render_acc(kind, mcol_hex, bgcol, zoom=1.0, W=W0, H=H0, seed=0, dx=0, dy=0):
    img = fabric_field(W, H, hx(bgcol), k=2.2, theta=0.5, seed=seed, weave=0.03, sheen=0.18)
    s = 0.62 * W * zoom
    ACC[kind](img, W / 2 + dx, H / 2 + dy, s, hx(mcol_hex))
    return img


# ------------------------------------------------------------------ main
def main():
    count = 0
    for p in PRODUCTS:
        kind = p["kind"]
        for i, c in enumerate(p["colours"]):
            name, hexc = c[0], c[1]
            pc = c[2] if len(c) > 2 else None
            fn = os.path.join(OUT, f"{p['id']}-{slug(name)}.jpg")
            if kind.startswith("scarf"):
                img = scene_scarf(hexc, pc, seed=i + sum(map(ord, p["id"])) % 7)
            elif kind.startswith("cap"):
                img = render_cap(hexc, kind)
            else:
                img = render_acc(kind, hexc, ACC_BG.get(name, "#0f4a3a"), seed=i)
            save(img, fn)
            count += 1
        # detail close-up (first colour)
        name, hexc = p["colours"][0][0], p["colours"][0][1]
        pc = p["colours"][0][2] if len(p["colours"][0]) > 2 else None
        if kind.startswith("scarf"):
            img = detail_scarf(hexc, pc, seed=3)
        elif kind.startswith("cap"):
            img = detail_cap(hexc, kind)
        else:
            img = render_acc(kind, hexc, ACC_BG.get(name, "#0f4a3a"), zoom=1.9, seed=5, dx=0, dy=0)
        save(img, os.path.join(OUT, f"{p['id']}-detail.jpg"))
        count += 1
    print("product images:", count)

    # ---------- hero (wide) ----------
    HW, HH = 1800, 1100
    img = bg(HW, HH, "#0b3b2e", "#0f5a46", light=(0.72, 0.25))
    cols = [("#eebfba", 0.40, 1.00), ("#2f8a6c", 0.51, 0.93), ("#e4d0a2", 0.62, 1.02), ("#f1ead8", 0.73, 0.95), ("#c68790", 0.84, 1.00), ("#1d2a44", 0.94, 0.90)]
    for i, (c, fx, sc) in enumerate(cols):
        sw, sh = int(520 * sc), int(1010 * sc)
        rgb, a = scarf(sw, sh, hx(c), None, seed=i * 2 + 1)
        place(img, rgb, a, int(HW * fx - sw / 2), 70, off=(20, 30), r=26, k=0.5)
    rod(img, 76, int(HW * 0.30), HW - 20, th=18)
    save(img, os.path.join(ASSETS, "hero.jpg"), q=84)
    og = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).crop((420, 0, 1620, 630)).resize((1200, 630))
    og.save(os.path.join(ASSETS, "og-image.jpg"), quality=84)

    # ---------- category tiles ----------
    TW, TH = 800, 1000
    img = bg(TW, TH, "#f8f1e8", "#ecd2cc")
    for i, (c, fx, sc) in enumerate([("#0f5a46", 0.28, 0.80), ("#eebfba", 0.72, 0.80), ("#efe6d2", 0.50, 0.92)]):
        sw, sh = int(440 * sc), int(880 * sc)
        rgb, a = scarf(sw, sh, hx(c), None, seed=i * 3 + 2)
        place(img, rgb, a, int(TW * fx - sw / 2), 90 + (0 if i < 2 else 30))
    rod(img, 96, 40, TW - 40)
    save(img, os.path.join(ASSETS, "cat-hijabs.jpg"))

    img = bg(TW, TH, "#f8f1e8", "#ead4cb")
    draw_cap_on(img, "#d9b99f", "cap_classic", TW * 0.30, TH * 0.34, 470, 400)
    draw_cap_on(img, "#0f5a46", "cap_bonnet", TW * 0.72, TH * 0.52, 470, 400)
    draw_cap_on(img, "#1d1d20", "cap_tube", TW * 0.34, TH * 0.74, 470, 400)
    save(img, os.path.join(ASSETS, "cat-caps.jpg"))

    img = fabric_field(TW, TH, hx("#0f4a3a"), k=2.2, theta=0.5, seed=2, weave=0.03, sheen=0.18)
    draw_floral(img, TW * 0.50, TH * 0.28, 380, hx("#d4af55"))
    draw_pearlpins(img, TW * 0.27, TH * 0.72, 380, hx("#d4af55"))
    draw_magpins(img, TW * 0.72, TH * 0.74, 330, hx("#d69a86"))
    save(img, os.path.join(ASSETS, "cat-accessories.jpg"))

    # brand story image
    img = bg(1000, 1200, "#f8f1e8", "#ecd9cf")
    rgb, a = scarf(760, 1040, hx("#0f5a46"), None, seed=11)
    place(img, rgb, a, 120, 100)
    rod(img, 106, 50, 950)
    save(img, os.path.join(ASSETS, "story.jpg"))
    print("done")


if __name__ == "__main__":
    main()
