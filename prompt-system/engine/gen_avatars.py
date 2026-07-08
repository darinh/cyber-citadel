"""Cast avatar generator — QUALITY-FIRST, high-quality by default on GPU or CPU.

Produces one portrait per cast member at assets/avatars/<NAME>.png (the assembler overlays
it beside that speaker's subtitle). Avatars are OPTIONAL — if a PNG is missing the renderer
simply omits the corner portrait.

Quality (DEFAULT = sdxl; downgrades are OPT-IN only via CC_AVATARS — never auto-picked by hardware):
  - sdxl       : Stable Diffusion XL fixed-seed ORIGINAL portraits (GPU or CPU). Highest quality. DEFAULT.
  - turbo      : SD-Turbo few-step portraits (a speed/quality downgrade). CC_AVATARS=turbo.
  - illustrated: deterministic Pillow emblem portraits — instant, no model. CC_AVATARS=illustrated.
If SDXL deps are missing the tool FAILS LOUD with guidance (install them — SDXL runs on CPU too —
or explicitly approve CC_AVATARS=illustrated); it never silently ships lower-quality art.

ORIGINAL-IP RULE: character art is built from ORIGINAL primitives (silhouette/palette/motifs) +
a strong negative prompt; never a named franchise/character/likeness. The lint_prompts gate scans
your theme cast descriptions. Define each character in theme.json:
  "cast": [{ "name":"CHEF", "caption_color":"gold",
             "art": { "seed": 4012, "description": "a warm middle-aged head chef, apron, kind eyes" } }]
plus an optional theme-level "art_style": "storybook gouache, soft rim light, plain backdrop".
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme as _theme

PROJECT = Path(os.environ.get("CC_PROJECT") or Path.cwd())
OUT = PROJECT / "assets" / "avatars"
S = 480

NEG = ("trademark, logo, copyrighted character, mascot, franchise, recognizable celebrity, brand, "
       "watermark, signature, text, words, letters, multiple people, extra limbs, deformed, blurry, lowres")


def _tier():
    """Avatar quality. QUALITY-FIRST: default = SDXL (high quality) on GPU OR CPU. 'illustrated'
    (instant geometric portraits) and 'turbo' are DOWNGRADES applied ONLY when the user explicitly
    sets CC_AVATARS — we never auto-pick a lower-quality avatar path based on hardware."""
    env = os.environ.get("CC_AVATARS", "").lower()
    if env in ("sdxl", "sdxl_ipa", "turbo", "sd_turbo", "illustrated"):
        return {"sdxl_ipa": "sdxl", "sd_turbo": "turbo"}.get(env, env)
    return "sdxl"


# ---- illustrated fallback (always works) ---------------------------------
def illustrated(name, color, seed=0, role=""):
    t = _theme.load()
    bg0 = _theme.color("panel", t)
    bg1 = _theme.color("panel_hi", t)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # rounded card with a vertical gradient
    card = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cg = ImageDraw.Draw(card)
    for y in range(S):
        f = y / S
        col = tuple(int(bg0[i] * (1 - f) + bg1[i] * f) for i in range(3)) + (255,)
        cg.line([(0, y), (S, y)], fill=col)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([6, 6, S - 6, S - 6], radius=46, fill=255)
    img.paste(card, (0, 0), mask)
    # seeded geometric motif (unique per character, original)
    import random
    rng = random.Random(seed or sum(ord(c) for c in name))
    for _ in range(7):
        cx, cy = rng.randint(40, S - 40), rng.randint(40, S - 40)
        r = rng.randint(20, 90)
        a = rng.randint(10, 26)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color + (a,), width=3)
    # glowing ring + monogram
    cx, cy, rr = S // 2, S // 2 - 8, 132
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=color + (255,), width=12)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14)))
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=tuple(int(x * 0.5) for x in bg0) + (255,),
              outline=color + (255,), width=6)
    initials = "".join(w[0] for w in name.split()[:2]).upper() or name[:2].upper()
    f = _theme.font_path("bold", t)
    from PIL import ImageFont
    fnt = ImageFont.truetype(f, 150 if len(initials) == 1 else 120)
    tw = d.textlength(initials, font=fnt)
    bb = d.textbbox((0, 0), initials, font=fnt)
    d.text((cx - tw / 2, cy - (bb[3] - bb[1]) / 2 - bb[1]), initials, font=fnt, fill=color)
    # name plate
    nf = ImageFont.truetype(_theme.font_path("semibold", t), 34)
    nm = name.upper()
    nw = d.textlength(nm, font=nf)
    d.text((cx - nw / 2, S - 92), nm, font=nf, fill=_theme.color("ink", t))
    if role:
        rf = ImageFont.truetype(_theme.font_path("regular", t), 22)
        rw = d.textlength(role.upper(), font=rf)
        d.text((cx - rw / 2, S - 52), role.upper(), font=rf, fill=_theme.color("muted", t))
    OUT.mkdir(parents=True, exist_ok=True)
    img.convert("RGBA").save(OUT / f"{name.upper()}.png")
    return OUT / f"{name.upper()}.png"


# ---- SDXL / Turbo path (GPU) ---------------------------------------------
def _diffusion(cast, t, turbo=False):
    import torch
    from diffusers import AutoPipelineForText2Image
    model = "stabilityai/sd-turbo" if turbo else "stabilityai/stable-diffusion-xl-base-1.0"
    pipe = AutoPipelineForText2Image.from_pretrained(model, torch_dtype=torch.float16,
                                                     variant="fp16", use_safetensors=True).to("cuda")
    pipe.set_progress_bar_config(disable=True)
    style = t.get("art_style", "clean character portrait, head and shoulders bust, soft rim light, plain backdrop")
    steps = 4 if turbo else 32
    guidance = 0.0 if turbo else 6.5
    OUT.mkdir(parents=True, exist_ok=True)
    for c in cast:
        art = c.get("art", {}) or {}
        desc = art.get("description") or f"an original {c.get('role','guide')} character"
        seed = int(art.get("seed", sum(ord(x) for x in c.get("name", "X"))))
        g = torch.Generator("cuda").manual_seed(seed)
        prompt = f"{desc}, {style}, single original character, looking at viewer"
        img = pipe(prompt, negative_prompt=NEG, num_inference_steps=steps, guidance_scale=guidance,
                   width=768, height=768, generator=g).images[0]
        img.save(OUT / f"{c['name'].upper()}.png")
        print("avatar (sdxl):", c["name"], "seed", seed)


def main():
    t = _theme.load()
    cast = [c for c in (t.get("cast", []) or []) if c.get("name")]
    if not cast:
        print("no cast in theme.json; nothing to do")
        return
    tier = _tier()
    explicit_illustrated = os.environ.get("CC_AVATARS", "").lower() == "illustrated"
    print(f"avatar quality: {tier}  ({len(cast)} character(s))")
    if tier in ("sdxl", "turbo"):
        try:
            _diffusion(cast, t, turbo=(tier == "turbo"))
            return
        except Exception as e:                              # noqa: BLE001
            # QUALITY-FIRST: do NOT silently drop to low-quality portraits. Fail loud with guidance
            # so the user can install the deps (SDXL runs on CPU too) OR explicitly approve the
            # illustrated downgrade with CC_AVATARS=illustrated.
            raise SystemExit(
                f"\nHigh-quality SDXL avatars are unavailable ({e}).\n"
                "SDXL runs on CPU too (slow, one-time). Install: pip install diffusers transformers "
                "accelerate safetensors torch\n"
                "OR, to explicitly accept instant lower-quality geometric portraits, re-run with "
                "CC_AVATARS=illustrated.\n"
                "(Avatars are optional — you can also skip them entirely.)")
    # explicit, user-approved illustrated downgrade
    for i, c in enumerate(cast):
        col = _theme.color(c.get("caption_color", ["accent", "gold", "mint", "accent2", "violet"][i % 5]), t)
        p = illustrated(c["name"], col, seed=(c.get("art", {}) or {}).get("seed", 0), role=c.get("role", ""))
        print("avatar (illustrated, user-approved):", c["name"], "->", p.name)


if __name__ == "__main__":
    main()
