"""Frame the raw SDXL portraits into circular avatar cards for overlay next to
the speaker's subtitle. Output: course/art/avatars/<SPEAKER>.png (RGBA)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scene as S

RAW = Path(__file__).resolve().parent.parent / "course" / "art" / "avatars" / "raw"
OUT = Path(__file__).resolve().parent.parent / "course" / "art" / "avatars"

COLOR = {"VEGA": S.CYAN, "NOVA": S.MINT, "ARCHIVIST": S.GOLD,
         "NULL": S.MAGENTA, "NARRATOR": (200, 210, 255), "HERALD": S.VIOLET}

D = 150          # portrait diameter
PAD = 14         # ring + glow padding
SZ = D + PAD * 2


def make(name, col):
    raw = Image.open(RAW / f"{name}.png").convert("RGB")
    w, h = raw.size
    s = min(w, h)
    raw = raw.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2)).resize((D, D))
    card = Image.new("RGBA", (SZ, SZ), (0, 0, 0, 0))
    # soft outer glow ring
    glow = Image.new("RGBA", (SZ, SZ), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([PAD - 6, PAD - 6, SZ - PAD + 6, SZ - PAD + 6], outline=col + (255,), width=10)
    card.alpha_composite(glow.filter(ImageFilter.GaussianBlur(7)))
    # circular portrait
    mask = Image.new("L", (D, D), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, D, D], fill=255)
    # dark backing disc
    ImageDraw.Draw(card).ellipse([PAD - 4, PAD - 4, SZ - PAD + 4, SZ - PAD + 4],
                                 fill=(10, 14, 34, 255))
    card.paste(raw, (PAD, PAD), mask)
    # crisp ring
    ImageDraw.Draw(card).ellipse([PAD - 4, PAD - 4, SZ - PAD + 4, SZ - PAD + 4],
                                 outline=col + (255,), width=5)
    card.save(OUT / f"{name}.png")
    return OUT / f"{name}.png"


if __name__ == "__main__":
    for name, col in COLOR.items():
        if (RAW / f"{name}.png").exists():
            print("card:", make(name, col).name)
