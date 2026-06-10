"""Generate printable per-family cheat sheets (PNG) + a master overview.

Two-layer learning (council-mandated): videos teach the mental model; these
one-pagers carry fuller coverage - flagship controls, notable enhancements,
connections, and the mnemonic. Facts come from truth.json; glosses are harvested
from the verified in-episode cheat cards.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw
import scene as S
import episode_lib as L

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "course" / "cheatsheets"
OUT.mkdir(parents=True, exist_ok=True)
PW, PH = 1654, 2339  # A4-ish portrait @ ~200dpi

INK, MUTED, GOLD, CYAN, MINT = S.INK, S.MUTED, S.GOLD, S.CYAN, S.MINT


def harvest():
    glosses, mnemonics = {}, {}
    for sp in sorted((ROOT / "course" / "scripts").glob("ep0*.json")):
        spec = json.loads(sp.read_text(encoding="utf-8"))
        for b in spec["beats"]:
            if b.get("scene") == "cheatcard":
                fam = b.get("family", "")
                if b.get("mnemonic"):
                    mnemonics[fam] = b["mnemonic"]
                for bullet in b.get("bullets", []):
                    m = re.match(r"\s*([A-Z]{2}-\d{1,2})\s+.*?\s+\u2014\s+(.*)", bullet)
                    if m:
                        glosses[m.group(1)] = m.group(2)
    return glosses, mnemonics


GLOSS, MNEM = harvest()


def bg():
    img = Image.new("RGB", (PW, PH), S.BG_TOP)
    strip = Image.new("RGB", (1, PH))
    for y in range(PH):
        strip.putpixel((0, y), S.lerp(S.BG_TOP, S.BG_BOT, y / PH))
    img.paste(strip.resize((PW, PH)))
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, PW, 60):
        d.line([(x, 0), (x, PH)], fill=(255, 255, 255, 8))
    for y in range(0, PH, 60):
        d.line([(0, y), (PW, y)], fill=(255, 255, 255, 8))
    return img


def rrect(d, box, r, color, width=3, fill=None):
    if fill:
        d.rounded_rectangle(box, radius=r, fill=fill)
    d.rounded_rectangle(box, radius=r, outline=color, width=width)


def related_families(fam):
    sib = set()
    for cid in L.TRUTH[fam]["flagship"]:
        for rel in L.control(cid).get("related", []):
            rf = rel.split("-")[0]
            if rf != fam and rf in L.TRUTH:
                sib.add(rf)
    return sorted(sib)[:6]


def notable_enhancements(fam, limit=5):
    out = []
    for cid in L.TRUTH[fam]["flagship"]:
        for e in L.control(cid).get("enhancements", []):
            out.append((e["id"], e["title"]))
    # de-dup keep order
    seen, res = set(), []
    for i, t in out:
        if i not in seen:
            seen.add(i); res.append((i, t))
        if len(res) >= limit:
            break
    return res


def sheet(fam):
    persona, guards, reality = L.PERSONAS[fam]
    col = S.LAYER_COLORS[S.FAMILY_LAYER[fam]]
    img = bg()
    d = ImageDraw.Draw(img, "RGBA")
    M = 90
    # top accent
    d.rectangle([0, 0, PW, 14], fill=col)
    S.tracked_text(d, (M, 70), "CYBER CITADEL  \u00b7  CHEAT SHEET", S.FSB(26), col, tracking=6)
    # shield emblem
    S.shield(d, M + 120, 290, 200, 240, (16, 22, 54, 255), col, 6)
    d.text((M + 120, 270), fam, font=S.FB(110), fill=col, anchor="mm")
    rx = M + 280
    d.text((rx, 150), L.fam_name(fam), font=S.FB(60), fill=INK)
    d.text((rx, 232), persona, font=S.FSL(44), fill=GOLD)
    S.tracked_text(d, (rx, 318), "IN REALITY", S.FSB(22), MINT, tracking=5)
    S.draw_wrapped(d, (rx, 352), reality, S.F(32), MUTED, PW - rx - M, 1.3)

    y = 470
    d.line([(M, y), (PW - M, y)], fill=(255, 255, 255, 40), width=2)
    y += 30
    S.tracked_text(d, (M, y), "FLAGSHIP CONTROLS", S.FSB(30), col, tracking=6); y += 64
    for cid in L.TRUTH[fam]["flagship"]:
        rrect(d, [M, y, M + 250, y + 70], 12, col, 2, fill=(col[0] // 6, col[1] // 6, col[2] // 6, 255))
        d.text((M + 20, y + 8), cid, font=S.MONO(40), fill=col)
        d.text((M + 280, y + 2), L.title(cid), font=S.FSB(36), fill=INK)
        gl = GLOSS.get(cid, "")
        if gl:
            ny = S.draw_wrapped(d, (M + 280, y + 44), gl, S.F(28), MUTED, PW - (M + 280) - M, 1.25)
            y = max(y + 84, ny + 12)
        else:
            y += 90

    y += 16
    S.tracked_text(d, (M, y), "NOTABLE ENHANCEMENTS", S.FSB(30), col, tracking=6); y += 60
    for eid, et in notable_enhancements(fam):
        d.text((M + 6, y), "+", font=S.FB(34), fill=GOLD)
        d.text((M + 50, y + 2), eid, font=S.MONO(30), fill=GOLD)
        S.draw_wrapped(d, (M + 230, y + 2), et, S.F(30), INK, PW - (M + 230) - M, 1.2)
        y += 56

    y += 24
    S.tracked_text(d, (M, y), "CONNECTS TO", S.FSB(30), col, tracking=6); y += 58
    cx = M
    for rf in related_families(fam):
        rc = S.LAYER_COLORS[S.FAMILY_LAYER[rf]]
        rrect(d, [cx, y, cx + 110, y + 60], 10, rc, 2, fill=(16, 22, 52, 255))
        d.text((cx + 55, y + 30), rf, font=S.FB(34), fill=rc, anchor="mm")
        cx += 130

    # footer
    fy = PH - 200
    d.line([(M, fy), (PW - M, fy)], fill=(255, 255, 255, 40), width=2)
    if MNEM.get(fam):
        S.tracked_text(d, (M, fy + 24), "REMEMBER", S.FSB(24), GOLD, tracking=5)
        S.draw_wrapped(d, (M, fy + 58), MNEM[fam], S.FSB(40), GOLD, PW - 2 * M, 1.2)
    d.text((M, PH - 70), f"NIST SP 800-53r5  \u00b7  {fam} {L.fam_name(fam)}  \u00b7  {L.TRUTH[fam]['control_count']} controls",
           font=S.MONO(24), fill=MUTED)
    d.text((PW - M, PH - 70), "Educational aid \u2014 consult the standard", font=S.F(24), fill=MUTED, anchor="ra")

    out = OUT / f"{fam}_{L.fam_name(fam).replace(' ', '_').replace(',', '').replace('/', '-')}.png"
    img.convert("RGB").save(out, quality=95)
    return out


SHORTNAME = {
    "IA": "Identification & Authentication", "PE": "Physical & Environmental Protection",
    "AU": "Audit & Accountability", "SI": "System & Information Integrity",
    "PT": "PII Processing & Transparency", "SA": "System & Services Acquisition",
    "SC": "System & Communications Protection", "CA": "Assessment, Authorization & Monitoring",
    "SR": "Supply Chain Risk Management", "CM": "Configuration Management",
}


def master():
    Wd, Hd = 2240, 1740
    img = Image.new("RGB", (Wd, Hd), S.BG_TOP)
    strip = Image.new("RGB", (1, Hd))
    for y in range(Hd):
        strip.putpixel((0, y), S.lerp(S.BG_TOP, S.BG_BOT, y / Hd))
    img.paste(strip.resize((Wd, Hd)))
    d = ImageDraw.Draw(img, "RGBA")
    d.text((Wd / 2, 46), "CYBER CITADEL \u2014 THE TWENTY GUARDIANS", font=S.FB(62), fill=INK, anchor="ma")
    d.text((Wd / 2, 130), "20 control families \u00b7 6 layers of defense \u00b7 NIST SP 800-53r5",
           font=S.FSL(30), fill=MUTED, anchor="ma")
    layers = [(1, "Outer Walls"), (2, "Watchtowers"), (3, "Keepers of the Pact"),
              (4, "High Council"), (5, "The Forge"), (6, "Vaults & Lifelines")]
    x0, colw, ch = 80, 660, 140
    gapx = (Wd - 2 * x0 - 3 * colw) // 2
    for i, (ln, lname) in enumerate(layers):
        x = x0 + (i % 3) * (colw + gapx)
        yrow = 200 + (i // 3) * 770
        fams = L.LAYER_FAMILIES[ln]
        col = S.LAYER_COLORS[S.FAMILY_LAYER[fams[0]]]
        d.rectangle([x, yrow, x + colw, yrow + 8], fill=col)
        S.tracked_text(d, (x, yrow + 24), f"LAYER {ln} \u00b7 {lname.upper()}", S.FSB(26), col, tracking=3)
        yy = yrow + 84
        for fam in fams:
            rrect(d, [x, yy, x + colw, yy + ch], 14, col, 2, fill=(16, 22, 52, 255))
            d.text((x + 30, yy + ch / 2), fam, font=S.FB(54), fill=col, anchor="lm")
            nx = x + 180
            name = SHORTNAME.get(fam, L.fam_name(fam))
            S.draw_wrapped(d, (nx, yy + 22), name, S.FSB(30), INK, colw - 210, 1.12)
            d.text((nx, yy + ch - 44), L.PERSONAS[fam][0], font=S.FSL(26), fill=GOLD)
            yy += ch + 14
    d.text((Wd / 2, Hd - 50), "An educational aid \u2014 always consult NIST SP 800-53r5 and SP 800-53B",
           font=S.MONO(24), fill=MUTED, anchor="ma")
    out = OUT / "00_MASTER_the_twenty_guardians.png"
    img.save(out, quality=95)
    return out


if __name__ == "__main__":
    print("master:", master().name)
    for fam in L.TRUTH:
        print("sheet:", sheet(fam).name)
