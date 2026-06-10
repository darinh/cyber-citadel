"""Cyber Citadel scene renderer (Pillow).

Renders 1920x1080 stills for declarative scene types. A consistent "frame"
(gradient + grid + vignette + top bar + caption strip) wraps every scene so the
series feels cohesive. ffmpeg later adds motion (Ken Burns), transitions, music
and burned captions.

Library: render(beat: dict, out_path). CLI: `python scene.py demo` renders one
of each type to course/art/_demo for visual QA.
"""
from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "course" / "art"
W, H = 1920, 1080

# ---- palette -------------------------------------------------------------
BG_TOP = (8, 11, 30)
BG_BOT = (16, 22, 54)
PANEL = (18, 25, 60)
PANEL_HI = (28, 38, 86)
INK = (232, 236, 255)
MUTED = (138, 147, 194)
CYAN = (56, 225, 255)
MAGENTA = (255, 60, 172)
GOLD = (255, 200, 87)
MINT = (94, 234, 212)
RED = (255, 92, 122)
VIOLET = (167, 139, 250)

# Layer color coding (used on the map + accents)
LAYER_COLORS = {
    "walls": CYAN, "watch": MINT, "people": GOLD,
    "council": VIOLET, "forge": (255, 146, 76), "vaults": MAGENTA,
}
FAMILY_LAYER = {
    "AC": "walls", "IA": "walls", "PE": "walls",
    "AU": "watch", "SI": "watch", "IR": "watch",
    "AT": "people", "PS": "people", "PT": "people",
    "RA": "council", "PL": "council", "PM": "council", "CA": "council",
    "SA": "forge", "CM": "forge", "MA": "forge", "SR": "forge",
    "SC": "vaults", "MP": "vaults", "CP": "vaults",
}
FONTS = "C:/Windows/Fonts/"
_cache: dict = {}


def font(name: str, size: int):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS + name, size)
    return _cache[key]


def F(size):       return font("segoeui.ttf", size)
def FB(size):      return font("segoeuib.ttf", size)
def FSB(size):     return font("seguisb.ttf", size)
def FSL(size):     return font("segoeuisl.ttf", size)
def MONO(size):    return font("consolab.ttf", size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---- low-level helpers ---------------------------------------------------

def gradient_bg():
    img = Image.new("RGB", (W, H), BG_TOP)
    top = Image.new("RGB", (1, H))
    for y in range(H):
        top.putpixel((0, y), lerp(BG_TOP, BG_BOT, y / H))
    img.paste(top.resize((W, H)))
    return img


def add_grid(img, step=64, color=(255, 255, 255), alpha=10):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=color + (alpha,))
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=color + (alpha,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"))
    return img


def add_vignette(img, strength=120):
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-W * 0.3, -H * 0.3, W * 1.3, H * 1.3], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    img.paste(Image.composite(img, dark, mask))
    # extra corner darkening
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return img


def tracked_text(d, xy, text, fnt, fill, tracking=0, anchor_center=False):
    x, y = xy
    widths = [d.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1 if text else 0)
    if anchor_center:
        x -= total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, xy, text, fnt, fill, max_w, leading=1.3, center=False):
    x, y = xy
    lh = int(fnt.size * leading)
    for ln in wrap(d, text, fnt, max_w):
        if center:
            tw = d.textlength(ln, font=fnt)
            d.text((x - tw / 2, y), ln, font=fnt, fill=fill)
        else:
            d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def glow_layer(draw_fn, color, blur=18, passes=1):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(layer)
    draw_fn(dd)
    g = layer
    for _ in range(passes):
        g = g.filter(ImageFilter.GaussianBlur(blur))
    return g


def neon_rrect(img, box, radius, color, width=3, glow=True, fill=None):
    if glow:
        g = glow_layer(lambda dd: dd.rounded_rectangle(box, radius=radius,
                       outline=color + (255,), width=width + 2), color, blur=14)
        img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    if fill:
        d.rounded_rectangle(box, radius=radius, fill=fill)
    d.rounded_rectangle(box, radius=radius, outline=color + (255,), width=width)


def shield(d, cx, cy, w, h, fill, outline, width=4):
    x0, y0 = cx - w / 2, cy - h / 2
    pts = [
        (x0, y0), (x0 + w, y0), (x0 + w, y0 + h * 0.55),
        (cx, y0 + h), (x0, y0 + h * 0.55),
    ]
    d.polygon(pts, fill=fill, outline=outline, width=width)


# ---- frame (applied to every scene) -------------------------------------

_BG_IMG = None


def set_background(path):
    """Set an atmospheric backdrop (darkened+blurred) composited behind the UI."""
    global _BG_IMG
    if not path:
        _BG_IMG = None
        return
    im = Image.open(path).convert("RGB").resize((W, H))
    im = im.filter(ImageFilter.GaussianBlur(6))
    im = Image.eval(im, lambda p: int(p * 0.42))
    _BG_IMG = im.convert("RGBA")


def frame(tag_left="AEGIS CITADEL", tag_right=""):
    base = gradient_bg()
    base = add_grid(base)
    base = add_vignette(base)
    img = base.convert("RGBA")
    if _BG_IMG is not None:
        tint = img.copy()
        tint.putalpha(165)
        img = Image.alpha_composite(_BG_IMG.copy(), tint)
    d = ImageDraw.Draw(img)
    # faint circuit arcs
    arc = glow_layer(lambda dd: [dd.arc([200 + i * 360, -260, 760 + i * 360, 300],
                     200, 340, fill=CYAN + (40,), width=2) for i in range(4)],
                     CYAN, blur=2)
    img.alpha_composite(arc)
    # top bar
    d.line([(70, 70), (W - 70, 70)], fill=(255, 255, 255, 26), width=1)
    tracked_text(d, (70, 30), tag_left, FSB(24), CYAN, tracking=6)
    if tag_right:
        tw = sum(d.textlength(c, font=FSB(22)) for c in tag_right) + 4 * (len(tag_right) - 1)
        tracked_text(d, (W - 70 - tw, 32), tag_right, FSB(22), MUTED, tracking=4)
    # corner ticks
    for (cx, cy, dx, dy) in [(70, 70, 1, 1), (W - 70, 70, -1, 1),
                             (70, H - 60, 1, -1), (W - 70, H - 60, -1, -1)]:
        d.line([(cx, cy), (cx + 26 * dx, cy)], fill=CYAN + (180,), width=3)
        d.line([(cx, cy), (cx, cy + 26 * dy)], fill=CYAN + (180,), width=3)
    return img


def caption_strip(img):
    d = ImageDraw.Draw(img)
    band = Image.new("RGBA", (W, 170), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle([0, 0, W, 170], fill=(6, 8, 22, 150))
    img.alpha_composite(band, (0, H - 170))
    d.line([(70, H - 170), (W - 70, H - 170)], fill=(255, 255, 255, 24), width=1)
    return img


def emblem(img, cx, cy, r, color, glyph, sub=""):
    """Character sigil: glowing ring + initial."""
    g = glow_layer(lambda dd: dd.ellipse([cx - r, cy - r, cx + r, cy + r],
                   outline=color + (255,), width=8), color, blur=16)
    img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 14, 34, 230),
              outline=color + (255,), width=5)
    d.ellipse([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14],
              outline=color + (90,), width=2)
    gf = FB(int(r * 1.1))
    tw = d.textlength(glyph, font=gf)
    bb = d.textbbox((0, 0), glyph, font=gf)
    d.text((cx - tw / 2, cy - (bb[3] - bb[1]) / 2 - bb[1]), glyph, font=gf, fill=color)
    if sub:
        sf = FSB(26)
        tw = d.textlength(sub, font=sf)
        d.text((cx - tw / 2, cy + r + 16), sub, font=sf, fill=INK)


# ---- scene renderers -----------------------------------------------------

def s_title(img, b):
    d = ImageDraw.Draw(img)
    badge = b.get("badge", "")
    if badge:
        bw = 220
        neon_rrect(img, [W / 2 - bw / 2, 250, W / 2 + bw / 2, 320], 14, GOLD,
                   width=2, fill=(20, 18, 40, 200))
        d = ImageDraw.Draw(img)
        tracked_text(d, (W / 2, 264), badge, FSB(30), GOLD, tracking=6, anchor_center=True)
    title = b.get("title", "")
    d = ImageDraw.Draw(img)
    # glow title
    g = glow_layer(lambda dd: dd.text((W / 2, 380), title, font=FB(120), fill=CYAN + (255,),
                   anchor="ma"), CYAN, blur=22)
    img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 380), title, font=FB(120), fill=INK, anchor="ma")
    if b.get("subtitle"):
        d.text((W / 2, 560), b["subtitle"], font=FSL(46), fill=MUTED, anchor="ma")
    if b.get("kicker"):
        tracked_text(d, (W / 2, 200), b["kicker"], FSB(28), MAGENTA, tracking=8, anchor_center=True)
    return img


def s_section(img, b):
    d = ImageDraw.Draw(img)
    num = b.get("num", "")
    if num:
        g = glow_layer(lambda dd: dd.text((W / 2, 250), num, font=FB(260),
                       fill=(40, 52, 110, 255), anchor="ma"), VIOLET, blur=30)
        img.alpha_composite(g)
        d = ImageDraw.Draw(img)
        d.text((W / 2, 250), num, font=FB(260), fill=(46, 60, 130), anchor="ma")
    d.text((W / 2, 600), b.get("title", ""), font=FB(96), fill=INK, anchor="ma")
    if b.get("subtitle"):
        d.text((W / 2, 730), b["subtitle"], font=FSL(40), fill=CYAN, anchor="ma")
    return img


CITADEL_ORDER = ["AC", "IA", "PE", "AU", "SI", "IR", "AT", "PS", "PT",
                 "RA", "PL", "PM", "CA", "SA", "CM", "MA", "SR", "SC", "MP", "CP"]


def s_map(img, b):
    d = ImageDraw.Draw(img)
    if b.get("title"):
        d.text((W / 2, 84), b["title"], font=FB(54), fill=INK, anchor="ma")
    cx, cy, R = W / 2, 565, 300
    highlight = set(b.get("highlight", []))
    deps = b.get("deps", [])  # list of [A,B] pairs to connect
    pos = {}
    n = len(CITADEL_ORDER)
    for i, fam in enumerate(CITADEL_ORDER):
        a = -math.pi / 2 + i * 2 * math.pi / n
        pos[fam] = (cx + R * math.cos(a), cy + R * math.sin(a))
    # spokes first (behind keep + nodes)
    for fam, (x, y) in pos.items():
        d.line([(cx, cy), (x, y)], fill=(255, 255, 255, 16), width=1)
    hl = b.get("highlight", [])
    tt = b.get("_t", 1.0)

    def is_active(fam):
        if fam not in set(hl):
            return not hl
        return tt >= hl.index(fam) / max(1, len(hl)) - 1e-6

    # dependency arcs (drawn once both endpoints are active)
    for a, bb in deps:
        if a in pos and bb in pos and is_active(a) and is_active(bb):
            d.line([pos[a], pos[bb]], fill=CYAN + (140,), width=2)
    # central keep (on top of spokes)
    g = glow_layer(lambda dd: dd.ellipse([cx - 92, cy - 92, cx + 92, cy + 92],
                   outline=GOLD + (255,), width=8), GOLD, blur=20)
    img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - 92, cy - 92, cx + 92, cy + 92], fill=(26, 22, 46, 255), outline=GOLD, width=5)
    d.text((cx, cy - 30), "CROWN", font=FSB(30), fill=GOLD, anchor="ma")
    d.text((cx, cy + 6), "DATA", font=FSB(30), fill=GOLD, anchor="ma")
    # nodes
    for fam, (x, y) in pos.items():
        col = LAYER_COLORS[FAMILY_LAYER[fam]]
        ishl = fam in set(hl)
        on = is_active(fam)
        rr = 44 if ishl else 40
        if ishl and on:
            gg = glow_layer(lambda dd, x=x, y=y, col=col, rr=rr: dd.ellipse(
                [x - rr, y - rr, x + rr, y + rr], outline=col + (255,), width=8), col, blur=14)
            img.alpha_composite(gg)
            d = ImageDraw.Draw(img)
        fillc = (18, 25, 60, 255) if on else (14, 18, 40, 255)
        outc = col if on else (70, 80, 120)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=fillc, outline=outc, width=4 if on else 2)
        tcol = INK if on else MUTED
        d.text((x, y), fam, font=FB(32), fill=tcol, anchor="mm")
    return img


def s_guardian(img, b):
    fam = b.get("family", "")
    col = LAYER_COLORS.get(FAMILY_LAYER.get(fam, "walls"), CYAN)
    # left: shield emblem with family code
    sx = 470
    g = glow_layer(lambda dd: shield(dd, sx, 470, 300, 360, (16, 22, 54, 255), col + (255,), 8),
                   col, blur=20)
    img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    shield(d, sx, 470, 300, 360, (16, 22, 54, 255), col, 6)
    d.text((sx, 420), fam, font=FB(150), fill=col, anchor="mm")
    # right: name + persona
    rx = 760
    tracked_text(d, (rx, 250), "DISTRICT GUARDIAN", FSB(26), col, tracking=8)
    d.text((rx, 290), b.get("family_name", ""), font=FB(64), fill=INK)
    if b.get("persona"):
        d.text((rx, 380), b["persona"], font=FSL(44), fill=GOLD)
    y = 470
    if b.get("protects"):
        tracked_text(d, (rx, y), "GUARDS", FSB(22), MUTED, tracking=6); y += 36
        y = draw_wrapped(d, (rx, y), b["protects"], FSB(36), INK, 1020, 1.3); y += 18
    if b.get("reality"):
        tracked_text(d, (rx, y), "IN REALITY", FSB(22), MINT, tracking=6); y += 36
        y = draw_wrapped(d, (rx, y), b["reality"], F(32), MUTED, 1020, 1.3)
    return img


def s_control(img, b):
    cid = b.get("id", "")
    col = LAYER_COLORS.get(FAMILY_LAYER.get(cid.split("-")[0], "walls"), CYAN)
    neon_rrect(img, [150, 250, W - 150, 860], 26, col, width=2, fill=(14, 19, 46, 235))
    d = ImageDraw.Draw(img)
    # ID chip
    neon_rrect(img, [200, 300, 200 + 360, 300 + 110], 16, col, width=2, fill=(col[0]//6, col[1]//6, col[2]//6, 255))
    d = ImageDraw.Draw(img)
    d.text((380, 312), cid, font=MONO(78), fill=col, anchor="ma")
    tracked_text(d, (620, 312), "NIST SP 800-53r5", FSB(22), MUTED, tracking=4)
    d.text((620, 350), b.get("title", ""), font=FB(56), fill=INK)
    y = 470
    if b.get("plain"):
        tracked_text(d, (200, y), "WHAT IT MEANS", FSB(24), GOLD, tracking=6); y += 44
        y = draw_wrapped(d, (200, y), b["plain"], FSL(40), INK, W - 420, 1.32); y += 24
    if b.get("why"):
        tracked_text(d, (200, y), "WHY IT MATTERS", FSB(24), MINT, tracking=6); y += 44
        y = draw_wrapped(d, (200, y), b["why"], F(34), MUTED, W - 420, 1.3)
    return img


def s_quote(img, b):
    # Archivist verbatim — parchment/teletype authoritative styling
    neon_rrect(img, [170, 250, W - 170, 880], 22, GOLD, width=2, fill=(22, 20, 34, 240))
    d = ImageDraw.Draw(img)
    d.text((230, 250), "\u201C", font=FB(220), fill=(GOLD[0], GOLD[1], GOLD[2]))
    tracked_text(d, (250, 300), "VERBATIM \u00B7 THE ARCHIVIST READS", FSB(24), GOLD, tracking=6)
    y = 370
    quote = b.get("quote", "")
    y = draw_wrapped(d, (250, y), quote, FSL(46), INK, W - 560, 1.4)
    y = max(y, 760)
    d.line([(250, 800), (W - 250, 800)], fill=(255, 255, 255, 40), width=1)
    cite = b.get("cite", "")
    d.text((250, 818), cite, font=MONO(32), fill=GOLD)
    return img


def s_diagram(img, b):
    """Boxes + arrows. spec: nodes=[{label,x,y,w?,color?}], arrows=[[i,j,label?]]"""
    d = ImageDraw.Draw(img)
    if b.get("title"):
        d.text((W / 2, 150), b["title"], font=FB(58), fill=INK, anchor="ma")
    nodes = b.get("nodes", [])
    arrows = b.get("arrows", [])
    tt = b.get("_t", 1.0)
    n = max(1, len(nodes))
    boxes = []
    for k, nd in enumerate(nodes):
        w = nd.get("w", 320); h = nd.get("h", 130)
        x = nd["x"]; y = nd["y"]
        col = nd.get("color", CYAN)
        if isinstance(col, str):
            col = {"cyan": CYAN, "gold": GOLD, "mint": MINT, "red": RED,
                   "magenta": MAGENTA, "violet": VIOLET}.get(col, CYAN)
        boxes.append((x, y, w, h, col))
        if tt < (k / n) * 0.45:
            continue
        neon_rrect(img, [x, y, x + w, y + h], 16, col, width=2, fill=(16, 22, 52, 240))
        dd = ImageDraw.Draw(img)
        draw_wrapped(dd, (x + w / 2, y + h / 2 - 22), nd["label"], FSB(34), INK, w - 30, 1.15, center=True)
    d = ImageDraw.Draw(img)
    na = max(1, len(arrows))
    for k, ar in enumerate(arrows):
        i, j = ar[0], ar[1]
        if tt < (max(i, j) / n) * 0.45:
            continue
        f = max(0.0, min(1.0, (tt - (0.5 + k * (0.5 / na))) / (0.5 / na)))
        if f <= 0:
            continue
        x1, y1, w1, h1, _ = boxes[i]
        x2, y2, w2, h2, _ = boxes[j]
        p1 = (x1 + w1 / 2, y1 + h1 / 2)
        p2 = (x2 + w2 / 2, y2 + h2 / 2)
        ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        s = (p1[0] + math.cos(ang) * (w1 / 2 + 6), p1[1] + math.sin(ang) * (h1 / 2 + 6))
        ef = (p2[0] - math.cos(ang) * (w2 / 2 + 16), p2[1] - math.sin(ang) * (h2 / 2 + 16))
        e = (s[0] + (ef[0] - s[0]) * f, s[1] + (ef[1] - s[1]) * f)
        d.line([s, e], fill=CYAN + (220,), width=4)
        if f >= 0.98:
            d.polygon([ef, (ef[0] - 18 * math.cos(ang - 0.4), ef[1] - 18 * math.sin(ang - 0.4)),
                       (ef[0] - 18 * math.cos(ang + 0.4), ef[1] - 18 * math.sin(ang + 0.4))], fill=CYAN)
            if len(ar) > 2 and ar[2]:
                mx, my = (s[0] + ef[0]) / 2, (s[1] + ef[1]) / 2
                d.text((mx, my - 34), ar[2], font=FSB(26), fill=MINT, anchor="ma")
    return img


def s_quiz(img, b):
    d = ImageDraw.Draw(img)
    tracked_text(d, (W / 2, 175), b.get("kicker", "GUARDIAN CHECK \u00B7 PAUSE AND ANSWER"),
                 FSB(28), GOLD, tracking=8, anchor_center=True)
    y = draw_wrapped(d, (W / 2, 250), b.get("q", ""), FB(58), INK, 1500, 1.2, center=True)
    y += 30
    ans = b.get("answer", -1)
    for i, opt in enumerate(b.get("options", [])):
        letter = chr(65 + i)
        correct = (i == ans) and b.get("reveal")
        col = MINT if correct else CYAN
        box = [W / 2 - 620, y, W / 2 + 620, y + 96]
        neon_rrect(img, box, 16, col, width=2 if not correct else 4,
                   fill=(18, 40, 36, 240) if correct else (16, 22, 52, 235))
        dd = ImageDraw.Draw(img)
        dd.text((W / 2 - 560, y + 24), letter, font=FB(48), fill=col)
        dd.text((W / 2 - 470, y + 30), opt, font=FSB(40), fill=INK)
        if correct:
            cxp, cyp = W / 2 + 545, y + 48
            dd.line([(cxp, cyp), (cxp + 16, cyp + 20), (cxp + 48, cyp - 24)],
                    fill=MINT, width=9, joint="curve")
        y += 120
    return img


def s_points(img, b):
    col = CYAN
    neon_rrect(img, [150, 200, W - 150, 900], 26, col, width=2, fill=(14, 19, 46, 235))
    d = ImageDraw.Draw(img)
    tracked_text(d, (210, 234), b.get("kicker", "KEY POINTS"), FSB(26), col, tracking=8)
    d.text((210, 282), b.get("title", ""), font=FB(62), fill=INK)
    y = 404
    bullets = b.get("bullets", [])
    for item in bullets:
        d.ellipse([214, y + 14, 236, y + 36], outline=col, width=4)
        y = draw_wrapped(d, (270, y), item, FSB(38), INK, W - 540, 1.3) + 18
    if b.get("note"):
        d.line([(210, 818), (W - 210, 818)], fill=(255, 255, 255, 40), width=1)
        draw_wrapped(d, (210, 832), b["note"], F(30), MUTED, W - 440, 1.25)
    return img


def s_cheatcard(img, b):
    fam = b.get("family", "")
    col = LAYER_COLORS.get(FAMILY_LAYER.get(fam, "walls"), CYAN)
    neon_rrect(img, [150, 200, W - 150, 900], 26, col, width=3, fill=(14, 19, 46, 240))
    d = ImageDraw.Draw(img)
    tracked_text(d, (210, 230), "CHEAT CARD", FSB(26), col, tracking=8)
    if fam:
        d.text((W - 230, 224), fam, font=FB(90), fill=col, anchor="ra")
    d.text((210, 280), b.get("title", ""), font=FB(60), fill=INK)
    y = 400
    for item in b.get("bullets", []):
        d.ellipse([214, y + 14, 234, y + 34], fill=col)
        y = draw_wrapped(d, (260, y), item, FSB(38), INK, W - 520, 1.3) + 14
    if b.get("mnemonic"):
        d.line([(210, 820), (W - 210, 820)], fill=(255, 255, 255, 40), width=1)
        tracked_text(d, (210, 832), "REMEMBER", FSB(24), GOLD, tracking=6)
        d.text((420, 826), b["mnemonic"], font=FSB(40), fill=GOLD)
    return img


def s_define(img, b):
    """Plain-language definition card for a single term (beginner onboarding)."""
    col = MINT
    neon_rrect(img, [150, 224, W - 150, 884], 26, col, width=2, fill=(12, 24, 30, 235))
    d = ImageDraw.Draw(img)
    tracked_text(d, (210, 256), b.get("kicker", "PLAIN ENGLISH"), FSB(26), col, tracking=8)
    d.text((210, 300), b.get("term", ""), font=FB(74), fill=INK)
    y = 408
    if b.get("expand"):
        tracked_text(d, (210, y), "STANDS FOR", FSB(22), GOLD, tracking=6); y += 38
        y = draw_wrapped(d, (210, y), b["expand"], FSB(38), GOLD, W - 440, 1.22) + 20
    if b.get("plain"):
        tracked_text(d, (210, y), "IN PLAIN ENGLISH", FSB(22), col, tracking=6); y += 38
        y = draw_wrapped(d, (210, y), b["plain"], FSL(40), INK, W - 440, 1.3) + 20
    if b.get("example"):
        tracked_text(d, (210, y), "EVERYDAY EXAMPLE", FSB(22), CYAN, tracking=6); y += 38
        y = draw_wrapped(d, (210, y), b["example"], F(34), MUTED, W - 440, 1.3)
    if b.get("cite"):
        d.text((W - 210, 838), b["cite"], font=MONO(26), fill=(120, 128, 170), anchor="ra")
    return img


def s_coldopen(img, b):
    """'Breach of the week' — a real-world incident hook with a MITRE ATT&CK tag."""
    col = RED
    d = ImageDraw.Draw(img)
    d.polygon([(150, 250), (172, 250), (161, 230)], fill=col)
    tracked_text(d, (192, 226), "BREACH OF THE WEEK", FSB(30), col, tracking=8)
    if b.get("year"):
        g = glow_layer(lambda dd: dd.text((W - 150, 196), b["year"], font=FB(120),
                       fill=col + (255,), anchor="ra"), col, blur=18)
        img.alpha_composite(g)
        d = ImageDraw.Draw(img)
        d.text((W - 150, 196), b["year"], font=FB(120), fill=(255, 150, 168), anchor="ra")
    y = 330
    y = draw_wrapped(d, (150, y), b.get("headline", ""), FB(60), INK, W - 320, 1.14) + 28
    if b.get("body"):
        y = draw_wrapped(d, (150, y), b["body"], FSL(38), MUTED, W - 300, 1.34)
    if b.get("mitre"):
        cy = 792
        neon_rrect(img, [150, cy, 150 + 820, cy + 92], 14, GOLD, width=2, fill=(30, 26, 12, 240))
        dd = ImageDraw.Draw(img)
        tracked_text(dd, (178, cy + 16), "MITRE ATT&CK", FSB(20), GOLD, tracking=4)
        dd.text((178, cy + 44), b["mitre"], font=MONO(34), fill=INK)
    if b.get("teaches"):
        dd = ImageDraw.Draw(img)
        dd.text((W - 150, 800), "GUARDIAN", font=FSB(20), fill=MINT, anchor="ra")
        dd.text((W - 150, 836), b["teaches"], font=FSB(34), fill=MINT, anchor="ra")
    return img


def s_oath(img, b):
    """A guardian's spoken oath (mnemonic), with its sigil and the controls it encodes."""
    fam = b.get("family", "")
    col = LAYER_COLORS.get(FAMILY_LAYER.get(fam, "walls"), CYAN)
    g = glow_layer(lambda dd: shield(dd, W / 2, 372, 230, 270, (16, 22, 54, 255), col + (255,), 8),
                   col, blur=20)
    img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    shield(d, W / 2, 372, 230, 270, (16, 22, 54, 255), col, 6)
    d.text((W / 2, 344), fam, font=FB(112), fill=col, anchor="mm")
    tracked_text(d, (W / 2, 236), "GUARDIAN OATH", FSB(26), col, tracking=10, anchor_center=True)
    oath = "\u201C" + b.get("oath", "") + "\u201D"
    y = 568
    for ln in wrap(d, oath, FSL(52), W - 480):
        tw = d.textlength(ln, font=FSL(52))
        d.text((W / 2 - tw / 2, y), ln, font=FSL(52), fill=INK)
        y += 70
    if b.get("controls"):
        tracked_text(d, (W / 2, y + 22), b["controls"], MONO(34), GOLD, tracking=4, anchor_center=True)
    return img


def s_notebook(img, b):
    """'Nova's notebook' recap page — a friendly handwritten-feeling takeaway card."""
    col = GOLD
    neon_rrect(img, [210, 198, W - 210, 902], 18, col, width=2, fill=(26, 24, 16, 236))
    d = ImageDraw.Draw(img)
    for yy in range(392, 858, 60):
        d.line([(300, yy), (W - 260, yy)], fill=(255, 255, 255, 16), width=1)
    d.line([(338, 250), (338, 858)], fill=col + (110,), width=2)
    tracked_text(d, (280, 232), "NOVA'S NOTEBOOK", FSB(26), col, tracking=8)
    d.text((280, 278), b.get("title", ""), font=FB(52), fill=INK)
    y = 384
    for ln in b.get("lines", []):
        d.text((300, y - 2), "\u2022", font=FB(34), fill=col)
        y = draw_wrapped(d, (366, y), ln, FSL(38), INK, W - 700, 1.3) + 14
    if b.get("mnemonic"):
        tracked_text(d, (366, 832), "REMEMBER", FSB(22), col, tracking=6)
        d.text((600, 824), b["mnemonic"], font=FSB(36), fill=col)
    return img


RENDERERS = {
    "title": s_title, "section": s_section, "map": s_map, "guardian": s_guardian,
    "control": s_control, "quote": s_quote, "diagram": s_diagram, "quiz": s_quiz,
    "points": s_points, "cheatcard": s_cheatcard,
    "define": s_define, "coldopen": s_coldopen, "oath": s_oath, "notebook": s_notebook,
}


def render(beat: dict, out_path: str, t: float = 1.0):
    tag_r = beat.get("tag", "")
    img = frame(tag_right=tag_r)
    RENDERERS[beat["scene"]](img, dict(beat, _t=t))
    img = caption_strip(img)
    img = img.convert("RGB")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, quality=95)
    return out_path


def _demo():
    demo = ART / "_demo"
    demo.mkdir(parents=True, exist_ok=True)
    samples = [
        {"scene": "title", "kicker": "A NIST SP 800-53r5 TRAINING SERIES",
         "badge": "EPISODE 00", "title": "CYBER CITADEL", "subtitle": "The Twenty Guardians",
         "tag": "EP00"},
        {"scene": "section", "num": "01", "title": "THE OUTER WALLS",
         "subtitle": "Access \u00B7 Identity \u00B7 Physical", "tag": "EP01"},
        {"scene": "map", "title": "THE TWENTY DISTRICTS", "highlight": ["AC", "IA", "PE"],
         "deps": [["AC", "IA"], ["AC", "AU"]], "subtitle": "Highlighted: the Outer Walls",
         "tag": "EP01"},
        {"scene": "guardian", "family": "AC", "family_name": "Access Control",
         "persona": "The Gatekeeper", "protects": "Who may enter the city, and what they may touch.",
         "reality": "Policies and mechanisms that decide which users and processes get access to which resources.",
         "tag": "EP01"},
        {"scene": "control", "id": "AC-6", "title": "Least Privilege",
         "plain": "Give every user and process only the access they truly need \u2014 nothing more.",
         "why": "Limits the blast radius when an account is compromised or misused.", "tag": "EP01"},
        {"scene": "quote", "quote": "Employ the principle of least privilege, allowing only authorized "
         "accesses for users (or processes acting on behalf of users) that are necessary to accomplish "
         "assigned organizational tasks.", "cite": "NIST SP 800-53r5  \u00B7  AC-6 Least Privilege", "tag": "EP01"},
        {"scene": "diagram", "title": "How an access request is decided", "tag": "EP01",
         "nodes": [{"label": "User / Process", "x": 180, "y": 430, "color": "cyan"},
                   {"label": "Policy Decision", "x": 800, "y": 430, "color": "gold"},
                   {"label": "Enforcement Gate", "x": 1420, "y": 430, "color": "mint"}],
         "arrows": [[0, 1, "request"], [1, 2, "allow / deny"]]},
        {"scene": "quiz", "q": "Which guardian enforces 'only the access you truly need'?",
         "options": ["AU \u2014 Audit", "AC \u2014 Access Control", "PE \u2014 Physical"],
         "answer": 1, "reveal": True, "tag": "EP01"},
        {"scene": "cheatcard", "family": "AC", "title": "Access Control",
         "bullets": ["AC-2 Account Management \u2014 manage the lifecycle of accounts",
                     "AC-3 Access Enforcement \u2014 enforce approved authorizations",
                     "AC-6 Least Privilege \u2014 minimum necessary access"],
         "mnemonic": "\u201CRight person, right door, right reason.\u201D", "tag": "EP01"},
    ]
    for i, s in enumerate(samples):
        render(s, str(demo / f"demo_{i:02d}_{s['scene']}.jpg"))
        print("rendered", s["scene"])


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        _demo()
