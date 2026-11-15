# Draws the project thumbnail: a laser bouncing off two mirrors into a target.
# Needs Pillow (python -m pip install --user pillow).
# Run from the project root:
#   python docs/thumbnail/make_thumb.py docs/thumbnail/LaserLab_1024.png LaserLab.png
# The first path gets the 1024x1024 image, the second the 192x192 project thumbnail.
import sys, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

K = 2                      # supersample factor
S = 1024 * K
def p(v): return int(round(v * K))
def pts(*xy): return [p(v) for v in xy]

random.seed(7)

def brushed(w, h, base, spread=18, horizontal=True):
    n = Image.effect_noise((w, 6) if horizontal else (6, h), 40).resize((w, h), Image.BILINEAR)
    n = n.filter(ImageFilter.GaussianBlur(K))
    r, g, b = base
    lut = lambda c: [max(0, min(255, int(c + (i - 128) * spread / 128))) for i in range(256)]
    return Image.merge("RGB", (n.point(lut(r)), n.point(lut(g)), n.point(lut(b))))

def rr_mask(size, box, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle(box, radius=radius, fill=255)
    return m

# ---------- background ----------
img = Image.new("RGB", (S, S), (6, 10, 18))
bg = Image.radial_gradient("L").resize((S, S)).point(lambda v: 255 - v)
img = Image.composite(Image.new("RGB", (S, S), (22, 34, 54)), img, bg.point(lambda v: int(v * 0.8)))

# ---------- frame (bluish brushed metal) ----------
F0, F1 = 40, 984
frame = brushed(S, S, (78, 100, 130), 26)
fm = rr_mask((S, S), pts(F0, F0, F1, F1), p(56))
# frame shadow
sh = Image.new("L", (S, S), 0)
ImageDraw.Draw(sh).rounded_rectangle(pts(F0 + 10, F0 + 18, F1 + 10, F1 + 18), radius=p(56), fill=200)
sh = sh.filter(ImageFilter.GaussianBlur(p(18)))
img = Image.composite(Image.new("RGB", (S, S), (0, 0, 0)), img, sh)
img.paste(frame, (0, 0), fm)
d = ImageDraw.Draw(img)
d.rounded_rectangle(pts(F0, F0, F1, F1), radius=p(56), outline=(150, 175, 205), width=p(4))
d.rounded_rectangle(pts(F0 + 6, F0 + 6, F1 - 6, F1 - 6), radius=p(50), outline=(40, 52, 70), width=p(3))
# screws
for sx, sy in [(76, 76), (948, 76), (76, 948), (948, 948)]:
    d.ellipse(pts(sx - 11, sy - 11, sx + 11, sy + 11), fill=(48, 60, 78), outline=(160, 182, 210), width=p(2))
    d.line(pts(sx - 7, sy - 7, sx + 7, sy + 7), fill=(28, 36, 48), width=p(3))

# ---------- inner well + tiles ----------
B0, CELL, N = 112, 200, 4
d.rounded_rectangle(pts(B0 - 10, B0 - 10, B0 + CELL * N + 10, B0 + CELL * N + 10), radius=p(22), fill=(14, 20, 30))
tile_tex = brushed(p(CELL), p(CELL), (74, 90, 112), 16)
for cy in range(N):
    for cx in range(N):
        x0, y0 = B0 + cx * CELL + 6, B0 + cy * CELL + 6
        x1, y1 = x0 + CELL - 12, y0 + CELL - 12
        m = rr_mask((p(CELL - 12), p(CELL - 12)), (0, 0, p(CELL - 12) - 1, p(CELL - 12) - 1), p(16))
        img.paste(tile_tex.crop((0, 0, p(CELL - 12), p(CELL - 12))), (p(x0), p(y0)), m)
        d.rounded_rectangle(pts(x0, y0, x1, y1), radius=p(16), outline=(30, 40, 54), width=p(3))
        d.line(pts(x0 + 16, y0 + 3, x1 - 16, y0 + 3), fill=(140, 162, 190), width=p(3))
        d.line(pts(x0 + 3, y0 + 16, x0 + 3, y1 - 16), fill=(118, 140, 168), width=p(2))
        d.line(pts(x0 + 16, y1 - 3, x1 - 16, y1 - 3), fill=(40, 50, 66), width=p(3))
        # small center marks
        cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
        for ox, oy in [(-70, -70), (70, -70), (-70, 70), (70, 70)]:
            d.ellipse(pts(cxm + ox - 4, cym + oy - 4, cxm + ox + 4, cym + oy + 4), fill=(52, 64, 82))

def ctr(i): return B0 + i * CELL + CELL / 2

# ---------- object shadows ----------
shadow = Image.new("L", (S, S), 0)
sd = ImageDraw.Draw(shadow)
def obj_shadow(box, r=24):
    x0, y0, x1, y1 = box
    sd.rounded_rectangle(pts(x0 + 16, y0 + 22, x1 + 16, y1 + 22), radius=p(r), fill=170)

EX, EY = ctr(0), ctr(0)          # emitter
M1 = (ctr(3), ctr(0))            # "\" mirror
M2 = (ctr(3), ctr(3))            # "/" mirror
TX, TY = ctr(0), ctr(3)          # target
CR = (ctr(2), ctr(1))            # hazard crate
GL = (ctr(1), ctr(2))            # glass prism block (decor)

obj_shadow((EX - 66, EY - 56, EX + 62, EY + 56))
obj_shadow((TX - 60, TY - 60, TX + 60, TY + 60), 60)
obj_shadow((CR[0] - 70, CR[1] - 70, CR[0] + 70, CR[1] + 70), 14)
for mx, my in (M1, M2):
    sd.ellipse(pts(mx - 66 + 14, my - 66 + 20, mx + 66 + 14, my + 66 + 20), fill=150)
shadow = shadow.filter(ImageFilter.GaussianBlur(p(14)))
img = Image.composite(Image.new("RGB", (S, S), (4, 6, 10)), img, shadow)
d = ImageDraw.Draw(img)

# ---------- hazard crate ----------
def hazard_box(cx, cy, h):
    x0, y0, x1, y1 = cx - h, cy - h, cx + h, cy + h
    stripes = Image.new("RGB", (p(2 * h), p(2 * h)), (245, 196, 30))
    sdr = ImageDraw.Draw(stripes)
    for k in range(-6, 8):
        o = k * 40
        sdr.polygon(pts(o, 0, o + 20, 0, o + 20 - 2 * h, 2 * h, o - 2 * h, 2 * h), fill=(22, 22, 24))
    m = rr_mask(stripes.size, (0, 0, stripes.size[0] - 1, stripes.size[1] - 1), p(14))
    img.paste(stripes, (p(x0), p(y0)), m)
    d.rounded_rectangle(pts(x0 + 26, y0 + 26, x1 - 26, y1 - 26), radius=p(8), fill=(46, 54, 66), outline=(120, 136, 158), width=p(3))
    d.line(pts(x0 + 30, y0 + 30, x1 - 30, y0 + 30), fill=(150, 168, 190), width=p(2))
    d.rounded_rectangle(pts(x0, y0, x1, y1), radius=p(14), outline=(20, 20, 22), width=p(4))
hazard_box(*CR, 70)

# ---------- glass block (decor) ----------
gx, gy = GL
glass = Image.new("RGBA", (S, S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glass)
gd.rounded_rectangle(pts(gx - 58, gy - 58, gx + 58, gy + 58), radius=p(12), fill=(120, 200, 255, 70), outline=(190, 235, 255, 200), width=p(3))
gd.polygon(pts(gx - 50, gy - 50, gx + 10, gy - 50, gx - 50, gy + 10), fill=(220, 245, 255, 70))
img = Image.alpha_composite(img.convert("RGBA"), glass).convert("RGB")
d = ImageDraw.Draw(img)

# ---------- emitter ----------
d.rounded_rectangle(pts(EX - 66, EY - 56, EX + 62, EY + 56), radius=p(18), fill=(36, 42, 52), outline=(130, 146, 168), width=p(3))
d.rounded_rectangle(pts(EX - 54, EY - 44, EX + 30, EY + 44), radius=p(10), fill=(52, 60, 74))
for k in range(4):                                     # vents
    yy = EY - 30 + k * 20
    d.rounded_rectangle(pts(EX - 44, yy - 4, EX + 6, yy + 4), radius=p(4), fill=(20, 24, 30))
d.rectangle(pts(EX + 30, EY - 56, EX + 44, EY + 56), fill=(245, 196, 30))   # hazard band
for k in range(5):
    yy = EY - 56 + k * 24
    d.polygon(pts(EX + 30, yy, EX + 44, yy + 10, EX + 44, yy + 20, EX + 30, yy + 10), fill=(22, 22, 24))
d.rounded_rectangle(pts(EX + 44, EY - 22, EX + 86, EY + 22), radius=p(8), fill=(70, 80, 96), outline=(160, 176, 198), width=p(2))
d.ellipse(pts(EX + 66, EY - 16, EX + 98, EY + 16), fill=(255, 90, 40), outline=(90, 30, 20), width=p(3))

# ---------- target / receiver ----------
d.ellipse(pts(TX - 62, TY - 62, TX + 62, TY + 62), fill=(34, 40, 50), outline=(140, 158, 182), width=p(4))
d.ellipse(pts(TX - 44, TY - 44, TX + 44, TY + 44), fill=(18, 40, 32), outline=(70, 230, 140), width=p(6))
d.ellipse(pts(TX - 22, TY - 22, TX + 22, TY + 22), fill=(150, 255, 190))

# ---------- mirrors ----------
def mirror(cx, cy, kind):
    d.ellipse(pts(cx - 66, cy - 66, cx + 66, cy + 66), fill=(40, 48, 60), outline=(140, 158, 182), width=p(4))
    d.ellipse(pts(cx - 50, cy - 50, cx + 50, cy + 50), outline=(64, 76, 94), width=p(3))
    L = 64
    if kind == "\\":
        a, b = (cx - L * .72, cy - L * .72), (cx + L * .72, cy + L * .72)
        n = (-1, 1)     # face toward lower-left
    else:
        a, b = (cx - L * .72, cy + L * .72), (cx + L * .72, cy - L * .72)
        n = (-1, -1)    # face toward upper-left
    off = 7
    back = [(a[0] - n[0] * off, a[1] - n[1] * off), (b[0] - n[0] * off, b[1] - n[1] * off)]
    d.line(pts(*back[0], *back[1]), fill=(52, 86, 132), width=p(18))          # steel blue back
    d.line(pts(*a, *b), fill=(200, 222, 240), width=p(10))                    # silver face
    d.line(pts(a[0] + n[0] * 4, a[1] + n[1] * 4, b[0] + n[0] * 4, b[1] + n[1] * 4), fill=(255, 255, 255), width=p(3))
    for q in (a, b):
        d.ellipse(pts(q[0] - 9, q[1] - 9, q[0] + 9, q[1] + 9), fill=(90, 104, 124), outline=(30, 36, 46), width=p(2))
mirror(*M1, "\\")
mirror(*M2, "/")

# ---------- laser beam ----------
path = [(EX + 98, EY), M1, M2, (TX + 44, TY)]
glow = Image.new("RGB", (S, S), (0, 0, 0))
gdr = ImageDraw.Draw(glow)
for w, col, blur in [(70, (120, 18, 4), 40), (30, (255, 60, 15), 14), (12, (255, 120, 40), 4)]:
    layer = Image.new("RGB", (S, S), (0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.line([q for pt in path for q in pts(*pt)], fill=col, width=p(w), joint="curve")
    glow = ImageChops.add(glow, layer.filter(ImageFilter.GaussianBlur(p(blur))))
# hit flares
for (fx, fy), r, col in [(M1, 70, (255, 90, 30)), (M2, 70, (255, 90, 30)), ((EX + 82, EY), 50, (255, 80, 30)), ((TX, TY), 90, (60, 255, 140))]:
    layer = Image.new("RGB", (S, S), (0, 0, 0))
    ImageDraw.Draw(layer).ellipse(pts(fx - r / 2, fy - r / 2, fx + r / 2, fy + r / 2), fill=col)
    glow = ImageChops.add(glow, layer.filter(ImageFilter.GaussianBlur(p(r / 2.2))))
img = ImageChops.screen(img, glow)
d = ImageDraw.Draw(img)
d.line([q for pt in path for q in pts(*pt)], fill=(255, 236, 200), width=p(5), joint="curve")
for (fx, fy) in (M1, M2):
    d.ellipse(pts(fx - 9, fy - 9, fx + 9, fy + 9), fill=(255, 250, 235))
    d.line(pts(fx - 30, fy, fx + 30, fy), fill=(255, 220, 180), width=p(2))
    d.line(pts(fx, fy - 30, fx, fy + 30), fill=(255, 220, 180), width=p(2))

# ---------- vignette ----------
vig = Image.radial_gradient("L").resize((S, S)).point(lambda v: int(max(0, v - 150) * 1.1))
img = Image.composite(Image.new("RGB", (S, S), (0, 0, 0)), img, vig)

out_big, out_thumb = sys.argv[1], sys.argv[2]
big = img.resize((1024, 1024), Image.LANCZOS)
big.save(out_big)
thumb = big.resize((192, 192), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1, percent=60, threshold=1))
thumb.save(out_thumb)
print("ok")
