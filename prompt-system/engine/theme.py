"""Theme loader — the ONLY place creative tokens (palette, fonts, world vocabulary,
group colors, brand, cast) enter the renderer.

Hard rule (council consensus): theming changes COLORS / TEXTURES / WORDS only. It must
NEVER change geometry, timing, the A/V mux, caption placement, or the quiz option-box
layout (`scene.quiz_layout()` stays the single source of truth and is exported to the
player as `opt_rects`). Quality constants live in `engine/quality.py`, not here, so a
user theme can change how a course LOOKS but can never degrade how it PLAYS.

A theme is a JSON file (normally `course/theme.json`, or `$CC_THEME`). Every field has a
NEUTRAL, non-cyberpunk default so a missing/partial theme still renders cleanly and does
NOT look like any particular existing course.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
FONT_DIR = ENGINE / "assets" / "fonts"

# ---- neutral defaults (deliberately NOT cyan/magenta) --------------------
# A calm slate-and-amber scheme: distinct from any shipped course, readable, high-contrast.
_DEFAULT = {
    "brand": "TRAINING SERIES",
    "series_kicker": "AN INTERACTIVE TRAINING SERIES",
    "fonts": {
        "regular":  "NotoSans-Regular.ttf",
        "semibold": "NotoSans-SemiBold.ttf",
        "bold":     "NotoSans-Bold.ttf",
        "light":    "NotoSans-Regular.ttf",
        "mono":     "NotoSans-Bold.ttf",
    },
    "palette": {
        "bg_top":   [14, 16, 22],
        "bg_bot":   [26, 30, 40],
        "panel":    [30, 35, 47],
        "panel_hi": [44, 51, 68],
        "ink":      [236, 238, 244],
        "muted":    [150, 158, 176],
        "accent":   [120, 170, 255],   # soft blue
        "accent2":  [255, 138, 96],    # warm coral
        "gold":     [240, 196, 110],
        "mint":     [128, 222, 178],
        "danger":   [240, 110, 120],
        "violet":   [176, 150, 240],
    },
    "world": {
        # generic, theme-overridable vocabulary used as on-screen labels/defaults
        "stakes_label":     "PROGRESS",                 # the optional top meter
        "center_label":     "CORE",                     # the protected center on a map
        "group_role_label": "GUIDE",                    # what a group's persona is called
        "covers_label":     "COVERS",                   # persona card: what this group covers
        "meaning_label":    "IN PRACTICE",              # persona card: real-world meaning
        "quiz_kicker":      "KNOWLEDGE CHECK \u00B7 PICK YOUR ANSWER",
        "oath_label":       "THE PLEDGE",
        "source_label":     "",                         # default citation prefix (usually per-beat)
    },
    # Optional method-of-loci grouping for multi-topic COURSES (single videos omit it).
    # cluster -> {color: <palette token>, members: [group keys]}.
    "groups": {"order": [], "clusters": {}},
    # Cast is consumed by the avatar + voice prompts; the renderer only needs names.
    "cast": [],
}


def _deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def theme_path() -> Path | None:
    env = os.environ.get("CC_THEME")
    if env and Path(env).exists():
        return Path(env)
    # search upward from CWD for a course/theme.json or theme.json
    here = Path.cwd()
    for d in [here, *here.parents]:
        for cand in (d / "course" / "theme.json", d / "theme.json"):
            if cand.exists():
                return cand
    return None


_CACHE: dict | None = None


def load(path: str | os.PathLike | None = None) -> dict:
    """Return the merged theme dict (defaults <- file). Cached per process."""
    global _CACHE
    if _CACHE is not None and path is None:
        return _CACHE
    p = Path(path) if path else theme_path()
    data = {}
    if p and Path(p).exists():
        try:
            data = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception as e:                              # noqa: BLE001
            print(f"[theme] WARNING: could not parse {p}: {e}; using defaults")
    merged = _deep_merge(_DEFAULT, data)
    if path is None:
        _CACHE = merged
    return merged


# ---- accessors -----------------------------------------------------------
def color(token: str, t: dict | None = None) -> tuple:
    """RGB tuple for a palette token name, or a literal [r,g,b]/#rrggbb."""
    t = t or load()
    pal = t["palette"]
    if isinstance(token, (list, tuple)):
        return tuple(int(x) for x in token[:3])
    if isinstance(token, str) and token.startswith("#") and len(token) == 7:
        return tuple(int(token[i:i + 2], 16) for i in (1, 3, 5))
    return tuple(pal.get(token, pal["accent"]))


def font_path(role: str, t: dict | None = None) -> str:
    """Absolute path to a vendored/themed font for a role (regular/semibold/bold/light/mono)."""
    t = t or load()
    fname = t["fonts"].get(role, _DEFAULT["fonts"].get(role, "NotoSans-Regular.ttf"))
    # a theme may point at an absolute font file; otherwise resolve in the vendored dir
    p = Path(fname)
    if p.is_absolute() and p.exists():
        return str(p)
    cand = FONT_DIR / fname
    if cand.exists():
        return str(cand)
    return str(FONT_DIR / _DEFAULT["fonts"][role])


def group_color(key: str, t: dict | None = None) -> tuple:
    """Color for a method-of-loci group key (via its cluster), defaulting to accent."""
    t = t or load()
    for _name, c in (t.get("groups", {}).get("clusters", {}) or {}).items():
        if key in (c.get("members") or []):
            return color(c.get("color", "accent"), t)
    return color("accent", t)


def group_order(t: dict | None = None) -> list:
    t = t or load()
    g = t.get("groups", {})
    if g.get("order"):
        return list(g["order"])
    order = []
    for c in (g.get("clusters", {}) or {}).values():
        order.extend(c.get("members") or [])
    return order


def world(key: str, t: dict | None = None) -> str:
    t = t or load()
    return t.get("world", {}).get(key, _DEFAULT["world"].get(key, ""))


def brand(t: dict | None = None) -> str:
    return (t or load()).get("brand", _DEFAULT["brand"])


# ---- validation (used by gates) ------------------------------------------
def _luminance(rgb) -> float:
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b) -> float:
    la, lb = _luminance(a), _luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def validate(t: dict | None = None) -> list:
    """Return a list of (level, msg) problems. Used by the theme-validation gate so a
    creative theme can never silently degrade legibility/quality."""
    t = t or load()
    pal = t["palette"]
    probs = []
    pairs = [("ink", "panel", 4.5), ("ink", "bg_bot", 4.5), ("accent", "panel", 3.0),
             ("gold", "panel", 3.0), ("mint", "panel", 3.0), ("muted", "panel", 2.2)]
    for fg, bg, want in pairs:
        cr = contrast_ratio(color(fg, t), color(bg, t))
        if cr < want:
            probs.append(("P1", f"low contrast {fg} on {bg}: {cr:.2f} < {want} (unreadable)"))
    for role in ("regular", "semibold", "bold"):
        if not Path(font_path(role, t)).exists():
            probs.append(("P1", f"font for role '{role}' not found"))
    return probs


if __name__ == "__main__":
    import sys
    th = load(sys.argv[1] if len(sys.argv) > 1 else None)
    print("brand:", brand(th))
    print("accent:", color("accent", th), "ink:", color("ink", th))
    print("font(bold):", font_path("bold", th))
    pr = validate(th)
    print("validation:", "OK" if not pr else pr)
