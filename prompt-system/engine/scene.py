"""Instructional scene renderer (Pillow) — theme-driven and topic-agnostic.

Renders 1920x1080 stills for declarative scene types. The engine offers several
visual grammars—full-bleed media, annotated screenshots, comparison, timeline,
process, data chart, worked example, practice, and legacy cards—so a course does
not collapse into one slide template. ffmpeg later adds motion and captions.

Colors, fonts, and optional vocabulary come from the active theme. Layouts are
engine-owned rather than generated from raw pixel instructions. The quiz option
geometry alone is globally frozen so interactive click-hotspots always align.

Library: render(beat: dict, out_path). CLI: `python scene.py demo` renders one
of each type to engine/_demo_out for visual QA.
"""
from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent          # engine/
import sys as _sys
_sys.path.insert(0, str(ROOT))
import theme as _theme
import media as _media
ART = ROOT / "_demo_out"
W, H = 1920, 1080
_T = _theme.load()

# ---- palette -------------------------------------------------------------
# EVERY color comes from the theme (neutral, non-cyberpunk defaults if no theme.json).
# This is the ONLY creative-token surface in the renderer; geometry/timing never change.
def _c(tok):
    return _theme.color(tok, _T)
BG_TOP, BG_BOT = _c("bg_top"), _c("bg_bot")
PANEL, PANEL_HI = _c("panel"), _c("panel_hi")
INK, MUTED = _c("ink"), _c("muted")
CYAN, MAGENTA = _c("accent"), _c("accent2")
GOLD, MINT = _c("gold"), _c("mint")
RED, VIOLET = _c("danger"), _c("violet")


def group_color(key):
    """Color for a method-of-loci GROUP key (via the theme's clusters); accent by default."""
    return _theme.group_color(key, _T)


def group_order():
    """Ordered group keys for the map (from the theme); empty for single-video courses."""
    return _theme.group_order(_T)


_cache: dict = {}


def font(role: str, size: int):
    """Font for a ROLE (regular/semibold/bold/light/mono) from the vendored/themed fonts."""
    key = (role, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(_theme.font_path(role, _T), size)
    return _cache[key]


def F(size):       return font("regular", size)
def FB(size):      return font("bold", size)
def FSB(size):     return font("semibold", size)
def FSL(size):     return font("light", size)
def MONO(size):    return font("mono", size)


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


def fit_tracked_font(d, text, fontfn, start_size, max_w, tracking=0, min_size=18):
    size = start_size
    while size > min_size:
        fnt = fontfn(size)
        width = sum(d.textlength(ch, font=fnt) for ch in text)
        width += tracking * max(0, len(text) - 1)
        if width <= max_w:
            return fnt
        size -= 2
    return fontfn(min_size)


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


def fit_font(d, text, fontfn, size, max_w, min_size=22):
    """Largest font (down to min_size) at which `text` fits in max_w on one line.
    Prevents long official control/family titles from overflowing the slide container."""
    s = size
    while s > min_size and d.textlength(text or "", font=fontfn(s)) > max_w:
        s -= 2
    return fontfn(s)


def draw_fit(d, xy, text, fontfn, size, fill, max_w, anchor=None, min_size=18):
    """Draw a single line of VARIABLE-length text auto-shrunk to fit max_w. Use for any
    content-driven text (titles, names, options, mnemonics, cites) so nothing overflows."""
    d.text(xy, text or "", font=fit_font(d, text or "", fontfn, size, max_w, min_size),
           fill=fill, anchor=anchor)


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


def frame(tag_left=None, tag_right="", integrity=None):
    if tag_left is None:
        tag_left = _theme.brand(_T)
    base = gradient_bg()
    surface = _theme.visual("background_style", _T)
    chrome = _theme.visual("chrome", _T)
    if surface == "grid":
        base = add_grid(base)
    if surface in ("gradient", "grid") or chrome == "framed":
        base = add_vignette(base)
    img = base.convert("RGBA")
    if _BG_IMG is not None:
        tint = img.copy()
        tint.putalpha(165)
        img = Image.alpha_composite(_BG_IMG.copy(), tint)
    d = ImageDraw.Draw(img)
    # top bar
    d.line([(70, 70), (W - 70, 70)], fill=(255, 255, 255, 26), width=1)
    tracked_text(d, (70, 30), tag_left, FSB(24), CYAN, tracking=6)
    if tag_right:
        tw = sum(d.textlength(c, font=FSB(22)) for c in tag_right) + 4 * (len(tag_right) - 1)
        tracked_text(d, (W - 70 - tw, 32), tag_right, FSB(22), MUTED, tracking=4)
    if chrome == "framed":
        for (cx, cy, dx, dy) in [(70, 70, 1, 1), (W - 70, 70, -1, 1),
                                 (70, H - 60, 1, -1), (W - 70, H - 60, -1, -1)]:
            d.line([(cx, cy), (cx + 26 * dx, cy)], fill=CYAN + (180,), width=3)
            d.line([(cx, cy), (cx, cy + 26 * dy)], fill=CYAN + (180,), width=3)
    if integrity is not None:
        integrity_bar(img, integrity)
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


def integrity_bar(img, value):
    """Centered top-chrome stakes HUD: '<STAKES LABEL> ▮▮▮▮▮▯▯ NN%'. Optional; driven
    by the assembler's running meter (dips on antagonist/threat beats, rises as taught)."""
    d = ImageDraw.Draw(img)
    val = max(0, min(100, int(round(value))))
    col = MINT if val >= 67 else (GOLD if val >= 34 else RED)
    segs, sw, gap = 10, 14, 5
    bw = segs * (sw + gap) - gap
    lab, pct = _theme.world("stakes_label", _T), f"{val}%"
    lf, pf = FSB(18), FB(18)
    lw = d.textlength(lab, font=lf)
    pw = d.textlength(pct, font=pf)
    x = int((W - (lw + 16 + bw + 14 + pw)) // 2)
    y = 33
    d.text((x, y), lab, font=lf, fill=MUTED)
    bx = int(x + lw + 16)
    filled = round(val * segs / 100)
    for i in range(segs):
        sx = bx + i * (sw + gap)
        d.rectangle([sx, y + 2, sx + sw, y + 16],
                    fill=col + (255,) if i < filled else (70, 80, 120, 150))
    d.text((bx + bw + 14, y), pct, font=pf, fill=col)




# ---- scene renderers -----------------------------------------------------

def s_title(img, b):
    d = ImageDraw.Draw(img)
    badge = b.get("badge", "")
    if badge:
        badge_tracking = 6
        badge_font = fit_tracked_font(d, badge, FSB, 30, W - 400, badge_tracking)
        badge_text_w = sum(d.textlength(ch, font=badge_font) for ch in badge)
        badge_text_w += badge_tracking * max(0, len(badge) - 1)
        bw = min(W - 320, max(220, badge_text_w + 80))
        neon_rrect(img, [W / 2 - bw / 2, 250, W / 2 + bw / 2, 320], 14, GOLD,
                   width=2, fill=(20, 18, 40, 200))
        d = ImageDraw.Draw(img)
        tracked_text(d, (W / 2, 264), badge, badge_font, GOLD,
                     tracking=badge_tracking, anchor_center=True)
    title = b.get("title", "")
    d = ImageDraw.Draw(img)
    tf = fit_font(d, title, FB, 120, W - 320)
    # glow title
    g = glow_layer(lambda dd: dd.text((W / 2, 380), title, font=tf, fill=CYAN + (255,),
                   anchor="ma"), CYAN, blur=22)
    img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 380), title, font=tf, fill=INK, anchor="ma")
    if b.get("subtitle"):
        d.text((W / 2, 560), b["subtitle"], font=fit_font(d, b["subtitle"], FSL, 46, W - 280), fill=MUTED, anchor="ma")
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
    d.text((W / 2, 600), b.get("title", ""), font=fit_font(d, b.get("title", ""), FB, 96, W - 320), fill=INK, anchor="ma")
    if b.get("subtitle"):
        d.text((W / 2, 730), b["subtitle"], font=fit_font(d, b["subtitle"], FSL, 40, W - 260), fill=CYAN, anchor="ma")
    return img


# (Group order for the map comes from the theme's clusters via group_order(); a map beat
# may also carry its own "order": [...] list. No course-specific order is hardcoded here.)


def s_map(img, b):
    d = ImageDraw.Draw(img)
    if b.get("title"):
        d.text((W / 2, 84), b["title"], font=fit_font(d, b["title"], FB, 54, W - 200), fill=INK, anchor="ma")
    cx, cy, R = W / 2, 565, 300
    deps = b.get("deps", [])  # list of [A,B] pairs to connect
    pos = {}
    # group keys come from the theme (method-of-loci clusters); a beat may override.
    order = b.get("order") or group_order()
    n = len(order)
    if n == 0:
        return img
    for i, fam in enumerate(order):
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
    d.text((cx, cy - 16), _theme.world("center_label", _T), font=FSB(30), fill=GOLD, anchor="ma")
    # nodes
    for fam, (x, y) in pos.items():
        col = group_color(fam)
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
    fam = b.get("group", b.get("family", ""))
    col = group_color(fam)
    # left: shield emblem with group code
    sx = 470
    g = glow_layer(lambda dd: shield(dd, sx, 470, 300, 360, (16, 22, 54, 255), col + (255,), 8),
                   col, blur=20)
    img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    shield(d, sx, 470, 300, 360, (16, 22, 54, 255), col, 6)
    d.text((sx, 420), fam, font=FB(150), fill=col, anchor="mm")
    # right: name + persona
    rx = 760
    tracked_text(d, (rx, 250), _theme.world("group_role_label", _T), FSB(26), col, tracking=8)
    draw_fit(d, (rx, 290), b.get("group_name", b.get("family_name", "")), FB, 64, INK, 1020)
    if b.get("persona"):
        draw_fit(d, (rx, 380), b["persona"], FSL, 44, GOLD, 1020)
    y = 470
    _summary = b.get("summary", b.get("protects"))
    _meaning = b.get("meaning", b.get("reality"))
    if _summary:
        tracked_text(d, (rx, y), _theme.world("covers_label", _T) or "COVERS", FSB(22), MUTED, tracking=6); y += 36
        y = draw_wrapped(d, (rx, y), _summary, FSB(36), INK, 1020, 1.3); y += 18
    if _meaning:
        tracked_text(d, (rx, y), _theme.world("meaning_label", _T) or "IN PRACTICE", FSB(22), MINT, tracking=6); y += 36
        y = draw_wrapped(d, (rx, y), _meaning, F(32), MUTED, 1020, 1.3)
    return img


def s_control(img, b):
    cid = b.get("id", "")
    col = group_color(cid.split("-")[0])
    neon_rrect(img, [150, 250, W - 150, 860], 26, col, width=2, fill=(14, 19, 46, 235))
    d = ImageDraw.Draw(img)
    # ID chip
    neon_rrect(img, [200, 300, 200 + 360, 300 + 110], 16, col, width=2, fill=(col[0]//6, col[1]//6, col[2]//6, 255))
    d = ImageDraw.Draw(img)
    d.text((380, 312), cid, font=MONO(78), fill=col, anchor="ma")
    # source/citation comes from the beat (a control card may name its source + section);
    # falls back to the theme's source_label. No standard-specific mapping is hardcoded.
    _section = b.get("section", "")
    _src = b.get("source", _theme.world("source_label", _T))
    _line = (_src + (f"   \u00b7   \u00a7{_section}" if _section else "")) if (_src or _section) else ""
    if _line:
        tracked_text(d, (620, 312), _line, FSB(22), MUTED, tracking=4)
    d.text((620, 350), b.get("title", ""), font=fit_font(d, b.get("title", ""), FB, 56, W - 644 - 150), fill=INK)
    y = 470
    if b.get("plain"):
        tracked_text(d, (200, y), "WHAT IT MEANS", FSB(24), GOLD, tracking=6); y += 44
        y = draw_wrapped(d, (200, y), b["plain"], FSL(40), INK, W - 420, 1.32); y += 24
    if b.get("why"):
        tracked_text(d, (200, y), "WHY IT MATTERS", FSB(24), MINT, tracking=6); y += 44
        y = draw_wrapped(d, (200, y), b["why"], F(34), MUTED, W - 420, 1.3)
    return img


def s_quote(img, b):
    # Verbatim source — parchment/teletype authoritative styling
    neon_rrect(img, [170, 250, W - 170, 880], 22, GOLD, width=2, fill=(22, 20, 34, 240))
    d = ImageDraw.Draw(img)
    d.text((230, 250), "\u201C", font=FB(220), fill=(GOLD[0], GOLD[1], GOLD[2]))
    tracked_text(d, (250, 300), _theme.world("quote_label", _T) or "VERBATIM \u00B7 FROM THE SOURCE", FSB(24), GOLD, tracking=6)
    y = 370
    quote = b.get("quote", "")
    y = draw_wrapped(d, (250, y), quote, FSL(46), INK, W - 560, 1.4)
    y = max(y, 760)
    d.line([(250, 800), (W - 250, 800)], fill=(255, 255, 255, 40), width=1)
    cite = b.get("cite", "")
    draw_fit(d, (250, 818), cite, MONO, 32, GOLD, W - 560)
    return img


def s_diagram(img, b):
    """Boxes + arrows. spec: nodes=[{label,x,y,w?,color?}], arrows=[[i,j,label?]]"""
    d = ImageDraw.Draw(img)
    if b.get("title"):
        d.text((W / 2, 150), b["title"], font=fit_font(d, b["title"], FB, 58, W - 300), fill=INK, anchor="ma")
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


QUIZ_BOX_H = 84
QUIZ_BOX_STEP = 100
QUIZ_SAFE_BOTTOM = 890


def quiz_layout(b):
    """SINGLE source of truth for quiz option-box geometry, in 1920x1080 px.
    Shared by s_quiz (drawing) and build_episode2/cues.json (interactive
    click-hotspots) so the web buttons sit EXACTLY on the rendered boxes.
    Returns a list of (x0, y0, x1, y1), one per option. Mirrors the layout in
    s_quiz: kicker @175, question wrapped from y=250 (FB58, 1.2 leading, max_w
    1500), +30, then caption-safe boxes stacked above y=890, 1240px wide, centered."""
    d = ImageDraw.Draw(Image.new("RGB", (W, H)))
    lh = int(FB(58).size * 1.2)
    nlines = len(wrap(d, b.get("q", ""), FB(58), 1500))
    y = 250 + nlines * lh + 30
    boxes = []
    for _ in b.get("options", []):
        boxes.append((W / 2 - 620, y, W / 2 + 620, y + QUIZ_BOX_H))
        y += QUIZ_BOX_STEP
    return boxes


def s_quiz(img, b):
    d = ImageDraw.Draw(img)
    tracked_text(d, (W / 2, 175), b.get("kicker", _theme.world("quiz_kicker", _T)),
                 FSB(28), GOLD, tracking=8, anchor_center=True)
    draw_wrapped(d, (W / 2, 250), b.get("q", ""), FB(58), INK, 1500, 1.2, center=True)
    ans = b.get("answer", -1)
    boxes = quiz_layout(b)
    for i, opt in enumerate(b.get("options", [])):
        x0, y0, x1, y1 = boxes[i]
        letter = chr(65 + i)
        correct = (i == ans) and b.get("reveal")
        col = MINT if correct else CYAN
        neon_rrect(img, [x0, y0, x1, y1], 16, col, width=2 if not correct else 4,
                   fill=(18, 40, 36, 240) if correct else (16, 22, 52, 235))
        dd = ImageDraw.Draw(img)
        dd.text((x0 + 60, y0 + 18), letter, font=FB(48), fill=col)
        draw_fit(dd, (x0 + 150, y0 + 24), opt, FSB, 40, INK, 980)
        if correct:
            cxp, cyp = x1 - 75, y0 + QUIZ_BOX_H / 2
            dd.line([(cxp, cyp), (cxp + 16, cyp + 20), (cxp + 48, cyp - 24)],
                    fill=MINT, width=9, joint="curve")
    return img


def s_points(img, b):
    col = CYAN
    neon_rrect(img, [150, 200, W - 150, 900], 26, col, width=2, fill=(14, 19, 46, 235))
    d = ImageDraw.Draw(img)
    tracked_text(d, (210, 234), b.get("kicker", "KEY POINTS"), FSB(26), col, tracking=8)
    d.text((210, 282), b.get("title", ""), font=fit_font(d, b.get("title", ""), FB, 62, W - 210 - 180), fill=INK)
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
    fam = b.get("group", b.get("family", ""))
    col = group_color(fam)
    neon_rrect(img, [150, 200, W - 150, 900], 26, col, width=3, fill=(14, 19, 46, 240))
    d = ImageDraw.Draw(img)
    tracked_text(d, (210, 230), "CHEAT CARD", FSB(26), col, tracking=8)
    if fam:
        d.text((W - 230, 224), fam, font=FB(90), fill=col, anchor="ra")
    d.text((210, 280), b.get("title", ""), font=fit_font(d, b.get("title", ""), FB, 60, W - 210 - 320), fill=INK)
    y = 400
    for item in b.get("bullets", []):
        d.ellipse([214, y + 14, 234, y + 34], fill=col)
        y = draw_wrapped(d, (260, y), item, FSB(38), INK, W - 520, 1.3) + 14
    if b.get("mnemonic"):
        d.line([(210, 820), (W - 210, 820)], fill=(255, 255, 255, 40), width=1)
        tracked_text(d, (210, 832), "REMEMBER", FSB(24), GOLD, tracking=6)
        draw_fit(d, (420, 826), b["mnemonic"], FSB, 40, GOLD, W - 180 - 420)
    return img


def s_define(img, b):
    """Plain-language definition card for a single term (beginner onboarding)."""
    col = MINT
    neon_rrect(img, [150, 224, W - 150, 884], 26, col, width=2, fill=(12, 24, 30, 235))
    d = ImageDraw.Draw(img)
    tracked_text(d, (210, 256), b.get("kicker", "PLAIN ENGLISH"), FSB(26), col, tracking=8)
    draw_fit(d, (210, 300), b.get("term", ""), FB, 74, INK, W - 440)
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
        draw_fit(d, (W - 210, 838), b["cite"], MONO, 26, (120, 128, 170), W - 420, anchor="ra")
    return img


def s_coldopen(img, b):
    """An incident/scenario hook card (optional real-world example) with an optional tag."""
    col = RED
    d = ImageDraw.Draw(img)
    d.polygon([(150, 250), (172, 250), (161, 230)], fill=col)
    tracked_text(d, (192, 226), b.get("label", "BREACH OF THE WEEK"), FSB(30), col, tracking=8)
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
        tracked_text(dd, (178, cy + 16), b.get("mitre_label", "MITRE ATT&CK"), FSB(20), GOLD, tracking=4)
        draw_fit(dd, (178, cy + 44), b["mitre"], MONO, 34, INK, 560)
    if b.get("teaches"):
        dd = ImageDraw.Draw(img)
        dd.text((W - 150, 800), _theme.world("group_role_label", _T), font=FSB(20), fill=MINT, anchor="ra")
        draw_fit(dd, (W - 150, 836), b["teaches"], FSB, 34, MINT, 760, anchor="ra")
    return img


def s_oath(img, b):
    """A group's spoken pledge (mnemonic), with its sigil and the items it encodes."""
    fam = b.get("group", b.get("family", ""))
    col = group_color(fam)
    g = glow_layer(lambda dd: shield(dd, W / 2, 372, 230, 270, (16, 22, 54, 255), col + (255,), 8),
                   col, blur=20)
    img.alpha_composite(g)
    d = ImageDraw.Draw(img)
    shield(d, W / 2, 372, 230, 270, (16, 22, 54, 255), col, 6)
    d.text((W / 2, 344), fam, font=FB(112), fill=col, anchor="mm")
    tracked_text(d, (W / 2, 236), _theme.world("oath_label", _T), FSB(26), col, tracking=10, anchor_center=True)
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
    """A learner's recap / notebook page. Ruled lines sit UNDER each written line
    (never crossing the text) and use a solid dim ink so they never distract."""
    col = GOLD
    neon_rrect(img, [210, 198, W - 210, 902], 18, col, width=2, fill=(24, 22, 15, 238))
    d = ImageDraw.Draw(img)
    RULE = (58, 54, 42)      # solid, very dim warm ink (alpha-on-RGB isn't blended, so use a real color)
    MARGIN = (120, 104, 64)
    tracked_text(d, (282, 236), _theme.world("notebook_label", _T) or "FIELD NOTES", FSB(26), col, tracking=8)
    d.text((282, 282), b.get("title", ""), font=fit_font(d, b.get("title", ""), FB, 50, W - 282 - 280), fill=INK)
    d.line([(304, 372), (304, 862)], fill=MARGIN, width=2)   # margin rule
    fnt = FSL(38); lh = int(fnt.size * 1.44); x0 = 344; maxw = W - 720
    y = 384
    for ln in b.get("lines", []):
        first = True
        for seg in wrap(d, ln, fnt, maxw):
            ry = y + lh - 9
            d.line([(x0, ry), (W - 280, ry)], fill=RULE, width=1)   # rule beneath the writing
            if first:
                d.text((308, y + 2), "\u2022", font=FB(30), fill=col); first = False
            d.text((x0, y), seg, font=fnt, fill=INK)
            y += lh
        y += 12
    if b.get("mnemonic"):
        tracked_text(d, (344, 838), "REMEMBER", FSB(22), col, tracking=6)
        draw_fit(d, (566, 830), b["mnemonic"], FSB, 34, col, W - 280 - 566)
    return img


def _asset_meta(ref):
    return _media.get(str(ref)) or {}


def _place_asset(img, ref, box, fit="cover", focus=(0.5, 0.5), panel=True):
    """Place a manifest image and return its actual displayed rectangle."""
    path = _media.resolve(str(ref))
    if not path.exists():
        raise FileNotFoundError(f"media asset not found: {path}")
    source = Image.open(path).convert("RGB")
    x0, y0, x1, y1 = [int(v) for v in box]
    tw, th = x1 - x0, y1 - y0
    if panel:
        ImageDraw.Draw(img).rectangle([x0, y0, x1, y1], fill=PANEL + (255,))
    if fit == "contain":
        placed = ImageOps.contain(source, (tw, th), Image.Resampling.LANCZOS)
        px = x0 + (tw - placed.width) // 2
        py = y0 + (th - placed.height) // 2
    else:
        centering = tuple(max(0.0, min(1.0, float(v))) for v in focus[:2])
        placed = ImageOps.fit(source, (tw, th), Image.Resampling.LANCZOS, centering=centering)
        px, py = x0, y0
    img.paste(placed.convert("RGBA"), (px, py))
    return px, py, px + placed.width, py + placed.height


def _media_credit(ref, beat):
    meta = _asset_meta(ref)
    return (beat.get("credit") or meta.get("credit") or
            " · ".join(x for x in (meta.get("creator"), meta.get("license")) if x))


def _arrow(d, start, end, color=CYAN, width=4):
    d.line([start, end], fill=color, width=width)
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 18
    d.polygon([
        end,
        (end[0] - size * math.cos(ang - 0.45), end[1] - size * math.sin(ang - 0.45)),
        (end[0] - size * math.cos(ang + 0.45), end[1] - size * math.sin(ang + 0.45)),
    ], fill=color)


def s_image(img, b):
    """Full-bleed relevant image with restrained labels and provenance."""
    ref = b.get("asset")
    _place_asset(img, ref, [0, 72, W, H - 170], b.get("fit", "cover"),
                 tuple(b.get("focus", [0.5, 0.5])), panel=False)
    shade = Image.new("RGBA", (W, H - 242), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(shade.height):
        edge = min(y / 260, (shade.height - y) / 300)
        alpha = int(190 * max(0.0, 1.0 - edge))
        sd.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    img.alpha_composite(shade, (0, 72))
    d = ImageDraw.Draw(img)
    if b.get("title"):
        draw_fit(d, (110, 126), b["title"], FB, 68, INK, W - 220)
    if b.get("caption"):
        draw_wrapped(d, (110, 750), b["caption"], FSB(36), INK, W - 220, 1.25)
    credit = _media_credit(ref, b)
    if credit:
        draw_fit(d, (W - 110, H - 208), credit, F, 22, MUTED, W - 220, anchor="ra")
    return img


def s_screenshot(img, b):
    """Large screenshot with normalized callouts that reveal in sequence."""
    d = ImageDraw.Draw(img)
    if b.get("title"):
        draw_fit(d, (110, 105), b["title"], FB, 54, INK, W - 220)
    image_box = [110, 190, W - 110, 836]
    actual = _place_asset(img, b.get("asset"), image_box, b.get("fit", "contain"),
                          tuple(b.get("focus", [0.5, 0.5])))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(image_box, radius=18, outline=MUTED + (180,), width=2)
    callouts = b.get("callouts") or []
    visible = math.ceil(max(0.0, min(1.0, b.get("_t", 1.0))) * len(callouts))
    ax0, ay0, ax1, ay1 = actual
    aw, ah = ax1 - ax0, ay1 - ay0
    for index, callout in enumerate(callouts[:visible]):
        x, y, w, h = callout["rect"]
        box = [ax0 + x * aw, ay0 + y * ah, ax0 + (x + w) * aw, ay0 + (y + h) * ah]
        color = _c(callout.get("color", "danger"))
        d.rounded_rectangle(box, radius=10, outline=color, width=5)
        bx, by = box[0] + 18, max(96, box[1] - 18)
        d.ellipse([bx - 22, by - 22, bx + 22, by + 22], fill=color)
        d.text((bx, by), str(index + 1), font=FB(24), fill=BG_TOP, anchor="mm")
        label = str(callout.get("label", ""))
        lw = min(620, max(180, int(d.textlength(label, font=FSB(26)) + 36)))
        ly = min(H - 230, max(100, by - 20))
        d.rounded_rectangle([bx + 32, ly - 8, bx + 32 + lw, ly + 42],
                            radius=10, fill=(8, 10, 18, 225))
        draw_fit(d, (bx + 50, ly), label, FSB, 26, INK, lw - 30)
    credit = _media_credit(b.get("asset"), b)
    if credit:
        draw_fit(d, (W - 110, 852), credit, F, 20, MUTED, W - 220, anchor="ra")
    return img


def _comparison_side(img, item, box, color):
    x0, y0, x1, y1 = box
    neon_rrect(img, box, 22, color, width=2, glow=False, fill=PANEL + (245,))
    d = ImageDraw.Draw(img)
    image_bottom = y0
    if item.get("asset"):
        image_bottom = y0 + 330
        _place_asset(img, item["asset"], [x0 + 18, y0 + 18, x1 - 18, image_bottom],
                     item.get("fit", "cover"), tuple(item.get("focus", [0.5, 0.5])))
    title_y = image_bottom + 28 if image_bottom > y0 else y0 + 58
    draw_fit(d, (x0 + 42, title_y), item.get("title", ""), FB, 46, color, x1 - x0 - 84)
    body_y = title_y + 72
    draw_wrapped(d, (x0 + 42, body_y), item.get("body", ""), F(31), INK,
                 x1 - x0 - 84, 1.35)
    if item.get("label"):
        tracked_text(d, (x0 + 42, y1 - 62), item["label"], FSB(21), MUTED, tracking=4)


def s_comparison(img, b):
    """Two materially different cases shown at the same time for discrimination."""
    d = ImageDraw.Draw(img)
    draw_fit(d, (W / 2, 120), b.get("title", ""), FB, 58, INK, W - 240, anchor="ma")
    tt = b.get("_t", 1.0)
    if tt >= 0.05:
        _comparison_side(img, b.get("left") or {}, [90, 220, 930, 858], CYAN)
    if tt >= 0.5:
        _comparison_side(img, b.get("right") or {}, [990, 220, W - 90, 858], GOLD)
    return img


def s_timeline(img, b):
    """Auto-laid-out sequence; authors supply events, never pixel coordinates."""
    d = ImageDraw.Draw(img)
    draw_fit(d, (W / 2, 118), b.get("title", ""), FB, 58, INK, W - 240, anchor="ma")
    events = (b.get("events") or [])[:6]
    if not events:
        return img
    x0, x1, y = 170, W - 170, 520
    d.line([(x0, y), (x1, y)], fill=MUTED, width=4)
    visible = math.ceil(max(0.0, min(1.0, b.get("_t", 1.0))) * len(events))
    gap = (x1 - x0) / max(1, len(events) - 1)
    for index, event in enumerate(events[:visible]):
        x = x0 + index * gap
        color = _c(event.get("color", "accent" if index % 2 == 0 else "gold"))
        d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=color)
        above = index % 2 == 0
        cy = 270 if above else 590
        box = [x - 140, cy, x + 140, cy + 190]
        d.rounded_rectangle(box, radius=18, fill=PANEL + (245,), outline=color, width=2)
        draw_fit(d, (x, cy + 20), event.get("when", ""), FSB, 24, color, 240, anchor="ma")
        draw_fit(d, (x, cy + 58), event.get("label", ""), FB, 30, INK, 240, anchor="ma")
        draw_wrapped(d, (x, cy + 105), event.get("note", ""), F(23), MUTED, 230, 1.25, center=True)
        d.line([(x, y - 16 if above else y + 16), (x, cy + 190 if above else cy)],
               fill=color, width=2)
    return img


def s_process(img, b):
    """Auto-laid-out linear or cycle process with progressive reveal."""
    d = ImageDraw.Draw(img)
    draw_fit(d, (W / 2, 116), b.get("title", ""), FB, 58, INK, W - 240, anchor="ma")
    steps = (b.get("steps") or [])[:6]
    if not steps:
        return img
    visible = math.ceil(max(0.0, min(1.0, b.get("_t", 1.0))) * len(steps))
    layout = b.get("layout", "linear")
    boxes = []
    if layout == "cycle":
        radius = 285
        for index in range(len(steps)):
            angle = -math.pi / 2 + index * 2 * math.pi / len(steps)
            cx = W / 2 + radius * math.cos(angle)
            cy = 540 + radius * math.sin(angle)
            boxes.append([cx - 145, cy - 70, cx + 145, cy + 70])
    else:
        gap = 34
        card_w = min(310, (W - 220 - gap * (len(steps) - 1)) / len(steps))
        total = card_w * len(steps) + gap * (len(steps) - 1)
        left = (W - total) / 2
        boxes = [[left + i * (card_w + gap), 360,
                  left + i * (card_w + gap) + card_w, 690] for i in range(len(steps))]

    for index in range(min(visible, len(steps))):
        if index:
            prev, cur = boxes[index - 1], boxes[index]
            if layout == "cycle":
                _arrow(d, ((prev[0] + prev[2]) / 2, (prev[1] + prev[3]) / 2),
                       ((cur[0] + cur[2]) / 2, (cur[1] + cur[3]) / 2), MUTED, 3)
            else:
                _arrow(d, (prev[2] + 5, (prev[1] + prev[3]) / 2),
                       (cur[0] - 10, (cur[1] + cur[3]) / 2), MUTED, 3)
        step = steps[index]
        color = _c(step.get("color", "accent" if index % 2 == 0 else "gold"))
        box = boxes[index]
        d.rounded_rectangle(box, radius=20, fill=PANEL + (245,), outline=color, width=3)
        d.ellipse([box[0] + 20, box[1] + 20, box[0] + 70, box[1] + 70], fill=color)
        d.text((box[0] + 45, box[1] + 45), str(index + 1), font=FB(26),
               fill=BG_TOP, anchor="mm")
        draw_fit(d, (box[0] + 24, box[1] + 92), step.get("title", ""), FB, 31,
                 INK, box[2] - box[0] - 48)
        draw_wrapped(d, (box[0] + 24, box[1] + 145), step.get("detail", ""),
                     F(24), MUTED, box[2] - box[0] - 48, 1.3)
    if layout == "cycle" and visible == len(steps):
        first, last = boxes[0], boxes[-1]
        _arrow(d, ((last[0] + last[2]) / 2, (last[1] + last[3]) / 2),
               ((first[0] + first[2]) / 2, (first[1] + first[3]) / 2), MUTED, 3)
    return img


def s_chart(img, b):
    """Simple engine-laid-out bar or line chart for sourced quantitative claims."""
    d = ImageDraw.Draw(img)
    draw_fit(d, (W / 2, 112), b.get("title", ""), FB, 58, INK, W - 240, anchor="ma")
    data = (b.get("data") or [])[:10]
    if not data:
        return img
    values = [float(item.get("value", 0)) for item in data]
    high = max(max(values), 1.0)
    left, top, right, bottom = 220, 245, W - 180, 790
    d.line([(left, top), (left, bottom), (right, bottom)], fill=MUTED, width=3)
    unit = b.get("unit", "")
    if unit:
        d.text((left, top - 40), unit, font=FSB(23), fill=MUTED)
    tt = max(0.0, min(1.0, b.get("_t", 1.0)))
    chart_type = b.get("chart_type", "bar")
    gap = (right - left) / len(data)
    if chart_type == "line":
        points = []
        visible = max(1, math.ceil(tt * len(data)))
        for index, item in enumerate(data[:visible]):
            x = left + gap * (index + 0.5)
            y = bottom - (float(item.get("value", 0)) / high) * (bottom - top)
            points.append((x, y))
            color = _c(item.get("color", "accent"))
            d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=color)
            draw_fit(d, (x, bottom + 22), str(item.get("label", "")), FSB, 22,
                     MUTED, max(70, gap - 12), anchor="ma")
            d.text((x, y - 34), f"{item.get('value')}{unit}", font=FSB(21),
                   fill=INK, anchor="ma")
        if len(points) > 1:
            d.line(points, fill=CYAN, width=5, joint="curve")
    else:
        for index, item in enumerate(data):
            x0 = left + gap * index + gap * 0.18
            x1 = left + gap * (index + 1) - gap * 0.18
            height = (float(item.get("value", 0)) / high) * (bottom - top) * tt
            y0 = bottom - height
            color = _c(item.get("color", "accent" if index % 2 == 0 else "gold"))
            d.rounded_rectangle([x0, y0, x1, bottom], radius=10, fill=color)
            draw_fit(d, ((x0 + x1) / 2, bottom + 22), str(item.get("label", "")),
                     FSB, 22, MUTED, max(70, gap - 10), anchor="ma")
            if tt > 0.65:
                d.text(((x0 + x1) / 2, y0 - 34), f"{item.get('value')}{unit}",
                       font=FSB(22), fill=INK, anchor="ma")
    if b.get("insight"):
        draw_fit(d, (W / 2, 846), b["insight"], FSB, 30, GOLD, W - 320, anchor="ma")
    return img


def s_worked_example(img, b):
    """Problem at left, expert reasoning steps at right, optionally faded."""
    d = ImageDraw.Draw(img)
    draw_fit(d, (W / 2, 108), b.get("title", "WORKED EXAMPLE"), FB, 58,
             INK, W - 240, anchor="ma")
    left = [110, 220, 750, 858]
    right = [800, 220, W - 110, 858]
    d.rounded_rectangle(left, radius=22, fill=PANEL + (245,), outline=GOLD, width=2)
    d.rounded_rectangle(right, radius=22, fill=PANEL + (245,), outline=CYAN, width=2)
    tracked_text(d, (155, 258), "PROBLEM", FSB(23), GOLD, tracking=5)
    draw_wrapped(d, (155, 310), b.get("problem", ""), FSB(34), INK, 550, 1.35)
    tracked_text(d, (845, 258), "REASONING", FSB(23), CYAN, tracking=5)
    steps = b.get("steps") or []
    visible = math.ceil(max(0.0, min(1.0, b.get("_t", 1.0))) * len(steps))
    faded_from = b.get("faded_from")
    reveal = b.get("reveal", True)
    y = 315
    for index, raw in enumerate(steps[:visible]):
        step = raw if isinstance(raw, dict) else {"title": f"Step {index + 1}", "detail": str(raw)}
        d.ellipse([845, y + 4, 889, y + 48], fill=CYAN)
        d.text((867, y + 26), str(index + 1), font=FB(23), fill=BG_TOP, anchor="mm")
        if faded_from is not None and index >= int(faded_from) and not reveal:
            d.text((915, y + 4), "YOUR TURN", font=FSB(28), fill=GOLD)
            d.line([(915, y + 50), (W - 165, y + 50)], fill=GOLD, width=2)
            y += 100
            continue
        draw_fit(d, (915, y), step.get("title", ""), FB, 29, INK, 760)
        y = draw_wrapped(d, (915, y + 42), step.get("detail", ""), F(25), MUTED,
                         760, 1.28) + 22
    if b.get("model_answer") and (faded_from is None or reveal):
        tracked_text(d, (155, 760), "RESULT", FSB(22), MINT, tracking=5)
        draw_fit(d, (155, 800), b["model_answer"], FB, 32, MINT, 550)
    return img


def s_practice(img, b):
    """Pause-and-do activity with a distinct prompt and explanatory reveal."""
    d = ImageDraw.Draw(img)
    reveal = bool(b.get("reveal"))
    color = MINT if reveal else GOLD
    tracked_text(d, (W / 2, 150), "FEEDBACK" if reveal else
                 b.get("kicker", "PAUSE · TRY IT"), FSB(28), color,
                 tracking=8, anchor_center=True)
    if not reveal:
        draw_wrapped(d, (W / 2, 270), b.get("prompt", ""), FB(54), INK,
                     1460, 1.23, center=True)
        if b.get("instructions"):
            draw_wrapped(d, (W / 2, 620), b["instructions"], FSL(34), MUTED,
                         1320, 1.3, center=True)
    else:
        draw_wrapped(d, (W / 2, 260), b.get("model_answer", ""), FB(48), MINT,
                     1460, 1.25, center=True)
        if b.get("feedback"):
            draw_wrapped(d, (W / 2, 590), b["feedback"], F(34), INK,
                         1400, 1.35, center=True)
    return img


def s_video(img, b):
    """Poster used only by scene demos; the assembler inserts the actual source clip."""
    d = ImageDraw.Draw(img)
    tracked_text(d, (W / 2, 210), "SOURCE CLIP", FSB(28), CYAN, tracking=8,
                 anchor_center=True)
    draw_fit(d, (W / 2, 330), b.get("title", "VIDEO DEMONSTRATION"), FB, 66,
             INK, W - 300, anchor="ma")
    d.rounded_rectangle([390, 500, W - 390, 720], radius=24,
                        fill=PANEL + (245,), outline=CYAN, width=3)
    d.polygon([(875, 550), (875, 670), (1015, 610)], fill=CYAN)
    return img


RENDERERS = {
    "title": s_title, "section": s_section, "map": s_map,
    "quote": s_quote, "diagram": s_diagram, "quiz": s_quiz,
    "points": s_points, "cheatcard": s_cheatcard,
    "define": s_define, "coldopen": s_coldopen, "notebook": s_notebook,
    "image": s_image, "screenshot": s_screenshot, "video": s_video,
    "comparison": s_comparison, "timeline": s_timeline, "process": s_process,
    "chart": s_chart, "worked_example": s_worked_example, "practice": s_practice,
    # neutral scene-type names + legacy aliases (same renderer) so authoring stays theme-free
    "persona": s_guardian, "guardian": s_guardian,
    "concept": s_control, "control": s_control,
    "pledge": s_oath, "oath": s_oath,
}


def render(beat: dict, out_path: str, t: float = 1.0):
    tag_r = beat.get("tag", "")
    img = frame(tag_right=tag_r, integrity=beat.get("_integrity"))
    RENDERERS[beat["scene"]](img, dict(beat, _t=t))
    img = caption_strip(img)
    img = img.convert("RGB")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, quality=95)
    return out_path


def _demo():
    demo = ART / "_demo"
    demo.mkdir(parents=True, exist_ok=True)
    sample_asset = demo / "_sample_dashboard.png"
    sample = Image.new("RGB", (1400, 760), (238, 241, 246))
    sd = ImageDraw.Draw(sample)
    sd.rounded_rectangle([70, 70, 1330, 690], radius=30, fill=(255, 255, 255),
                         outline=(90, 105, 130), width=4)
    sd.line([(170, 590), (170, 170), (1210, 170)], fill=(70, 80, 100), width=4)
    pts = [(190, 540), (370, 500), (550, 430), (730, 455), (910, 330), (1090, 260)]
    sd.line(pts, fill=(62, 124, 210), width=12, joint="curve")
    for x, y in pts:
        sd.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(62, 124, 210))
    sample.save(sample_asset)

    # A neutral data-literacy demo exercises both legacy cards and the new visual grammar.
    samples = [
        {"scene": "title", "kicker": "AN INTERACTIVE TRAINING SERIES",
         "badge": "LESSON 01", "title": "KNIFE SKILLS", "subtitle": "Cut with confidence",
         "tag": "L01"},
        {"scene": "section", "num": "01", "title": "THE WORKBENCH",
         "subtitle": "Grip \u00B7 Board \u00B7 Edge", "tag": "L01"},
        {"scene": "define", "kicker": "PLAIN LANGUAGE", "term": "The Claw",
         "plain": "Curl your guiding fingertips under so the flat of the blade rides your knuckles \u2014 never your tips.",
         "example": "Like holding a tennis ball while the knife glides against your knuckles.", "tag": "L01"},
        {"scene": "control", "id": "KN-1", "title": "Pinch Grip",
         "plain": "Pinch the blade just ahead of the handle between thumb and forefinger for control.",
         "why": "A pinch grip steadies the tip and turns the wrist into a precise hinge.",
         "source": "Kitchen Academy Handbook", "section": "2.1", "tag": "L01"},
        {"scene": "quote", "quote": "Let the weight of the blade do the work; guide, do not force.",
         "cite": "Kitchen Academy Handbook  \u00B7  Ch. 2 Knife Skills", "tag": "L01"},
        {"scene": "points", "kicker": "REMEMBER", "title": "Three checks before you cut",
         "bullets": ["Board on a damp towel so it cannot slip",
                     "Blade sharp \u2014 a dull edge slips and bites",
                     "Guiding hand in the claw, tips tucked"],
         "note": "Set up once, cut safely all session.", "tag": "L01"},
        {"scene": "quiz", "q": "Where should your guiding fingertips be while slicing?",
         "options": ["Flat against the food", "Curled under in a claw", "Wrapped over the blade"],
         "answer": 1, "reveal": True, "tag": "L01"},
        {"scene": "cheatcard", "family": "KN", "title": "Knife Skills",
         "bullets": ["Pinch grip \u2014 control from the wrist",
                     "The claw \u2014 protect your fingertips",
                     "Rock, don't saw \u2014 tip stays on the board"],
         "mnemonic": "\u201CSharp blade, safe claw, steady board.\u201D", "tag": "L01"},
        {"scene": "image", "asset": str(sample_asset), "title": "Start with the whole pattern",
         "caption": "Relevant imagery establishes context; narration explains what to notice.",
         "credit": "Original engine demo asset", "tag": "L01"},
        {"scene": "screenshot", "asset": str(sample_asset), "title": "Read the axes before the line",
         "callouts": [{"rect": [0.06, 0.12, 0.12, 0.70], "label": "Vertical scale"},
                      {"rect": [0.18, 0.68, 0.70, 0.12], "label": "Time axis"}],
         "tag": "L01"},
        {"scene": "comparison", "title": "Trend or one-off anomaly?",
         "left": {"title": "Trend", "body": "A sustained direction across several observations.",
                  "label": "PATTERN"},
         "right": {"title": "Anomaly", "body": "A short departure from the surrounding pattern.",
                   "label": "EXCEPTION"}, "tag": "L01"},
        {"scene": "timeline", "title": "A compact review schedule",
         "events": [{"when": "NOW", "label": "Learn", "note": "Build the first model."},
                    {"when": "NEXT", "label": "Retrieve", "note": "Recall without looking."},
                    {"when": "LATER", "label": "Transfer", "note": "Apply in a new case."}],
         "tag": "L01"},
        {"scene": "process", "title": "Read a chart in four moves", "layout": "linear",
         "steps": [{"title": "Axes", "detail": "Name each measure."},
                   {"title": "Scale", "detail": "Check the visible range."},
                   {"title": "Pattern", "detail": "Look across observations."},
                   {"title": "Claim", "detail": "State evidence, not impression."}], "tag": "L01"},
        {"scene": "chart", "title": "One spike is not a sustained trend", "chart_type": "line",
         "unit": "%", "data": [{"label": "Jan", "value": 40}, {"label": "Feb", "value": 42},
                               {"label": "Mar", "value": 71, "color": "danger"},
                               {"label": "Apr", "value": 43}, {"label": "May", "value": 44}],
         "insight": "Compare the spike with the observations on both sides.", "tag": "L01"},
        {"scene": "worked_example", "title": "Model the reasoning",
         "problem": "Does the March spike prove a rising trend?",
         "steps": [{"title": "Inspect neighbors", "detail": "February and April remain near the baseline."},
                   {"title": "Classify the pattern", "detail": "Only one observation departs sharply."},
                   {"title": "Justify", "detail": "The evidence supports an anomaly, not a sustained rise."}],
         "model_answer": "March is an anomaly.", "tag": "L01"},
        {"scene": "practice", "prompt": "Classify the pattern and name the evidence you used.",
         "instructions": "Pause before the reveal. Explain your reasoning in one sentence.",
         "reveal": False, "tag": "L01"},
        {"scene": "practice", "model_answer": "Anomaly: the adjacent observations return to baseline.",
         "feedback": "The category matters less than the evidence. Compare multiple observations.",
         "reveal": True, "tag": "L01"},
    ]
    for i, s in enumerate(samples):
        render(s, str(demo / f"demo_{i:02d}_{s['scene']}.jpg"))
        print("rendered", s["scene"])


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        _demo()
