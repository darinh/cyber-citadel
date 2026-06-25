"""Original-IP guardrail (deterministic): block named franchises / trademarked characters,
places, studios, and "in the style of <artist>" from theme + scripts + image prompts.

A requested AESTHETIC (e.g. wizarding-school, cartoon-pony, high-fantasy fellowship, bullet-time
hacker-noir) must become an ORIGINAL world + ORIGINAL characters in that vibe — never a named IP.
This gate is a safety net over the creative surface (theme.json cast/world/art-style, every episode
spec's on-screen + spoken text, and any avatar/background prompt files). It is intentionally
conservative; extend assets/banned_terms.txt for your needs. Exit 1 on any hit.

  python lint_prompts.py            # scan theme.json + course/scripts/*.json (+ prompt files)
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

PROJECT = Path(os.environ.get("CC_PROJECT") or Path.cwd())
ENGINE = Path(__file__).resolve().parents[1]

# Starter denylist — well-known franchises, characters, places, studios. NOT exhaustive;
# the real guardrail is the "design ORIGINAL characters" step in the avatar/world prompts.
_BANNED = [
    # franchises / worlds
    "harry potter", "hogwarts", "wizarding world", "lord of the rings", "middle earth",
    "middle-earth", "the hobbit", "star wars", "jedi", "sith", "star trek", "the matrix",
    "game of thrones", "westeros", "my little pony", "equestria", "friendship is magic",
    "ninja turtles", "teenage mutant", "pokemon", "pokémon", "naruto", "dragon ball",
    "one piece", "minecraft", "fortnite", "super mario", "the legend of zelda", "hyrule",
    "avengers", "x-men", "justice league", "harry's", "narnia", "frozen", "moana",
    "spongebob", "rick and morty", "the simpsons", "south park", "looney tunes",
    # characters
    "gandalf", "frodo", "aragorn", "legolas", "gollum", "dumbledore", "hermione",
    "voldemort", "darth vader", "luke skywalker", "yoda", "spider-man", "spiderman",
    "iron man", "captain america", "batman", "superman", "wonder woman", "pikachu",
    "mario", "luigi", "sonic the hedgehog", "master chief", "lara croft", "kratos",
    "mickey mouse", "donald duck", "elsa", "shrek", "twilight sparkle", "rainbow dash",
    "neo", "morpheus", "trinity", "leonardo", "michelangelo", "donatello", "raphael",
    # studios / brands
    "disney", "pixar", "dreamworks", "nintendo", "warner bros", "marvel", "dc comics",
    "lucasfilm", "hasbro", "studio ghibli", "ghibli", "blizzard", "riot games", "sega",
]
_STYLE = re.compile(r"\bin the style of\s+[A-Z][a-z]+", re.I)       # "in the style of <Artist>"
_TM = re.compile(r"[\u00ae\u2122]")                                  # ® or ™


def _load_extra():
    f = ENGINE / "gates" / "assets" / "banned_terms.txt"
    if f.exists():
        return [ln.strip().lower() for ln in f.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.startswith("#")]
    return []


def _texts_from_theme():
    out = []
    tf = PROJECT / "theme.json"
    if not tf.exists():
        for c in [PROJECT, *PROJECT.parents]:
            if (c / "theme.json").exists():
                tf = c / "theme.json"
                break
    if tf.exists():
        t = json.loads(tf.read_text(encoding="utf-8"))
        out.append(("theme.brand", t.get("brand", "")))
        for c in (t.get("cast", []) or []):
            for k in ("name", "role", "persona", "description", "art_style", "appearance"):
                if c.get(k):
                    out.append((f"theme.cast[{c.get('name','?')}].{k}", str(c[k])))
        for k, v in (t.get("world", {}) or {}).items():
            out.append((f"theme.world.{k}", str(v)))
    return out


def _texts_from_specs():
    out = []
    for sp in sorted((PROJECT / "course" / "scripts").glob("*.json")):
        try:
            s = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            continue
        for i, b in enumerate(s.get("beats", [])):
            for k in ("title", "subtitle", "term", "plain", "why", "quote", "headline",
                      "body", "example", "expand", "mnemonic", "q", "persona", "summary", "meaning"):
                if b.get(k):
                    out.append((f"{sp.name}#{i}.{k}", str(b[k])))
            for opt in b.get("options", []) or []:
                out.append((f"{sp.name}#{i}.option", str(opt)))
            for sp2, tx in b.get("say", []):
                out.append((f"{sp.name}#{i}.say", str(tx)))
    return out


def _texts_from_prompts():
    out = []
    for d in (PROJECT / "world", PROJECT / "assets"):
        if d.exists():
            for f in d.rglob("*prompt*.txt"):
                out.append((str(f.relative_to(PROJECT)), f.read_text(encoding="utf-8")))
            for f in d.rglob("*.prompt.json"):
                out.append((str(f.relative_to(PROJECT)), f.read_text(encoding="utf-8")))
    return out


def lint():
    banned = _BANNED + _load_extra()
    items = _texts_from_theme() + _texts_from_specs() + _texts_from_prompts()
    hits = []
    for where, text in items:
        low = (text or "").lower()
        for term in banned:
            if re.search(r"(?<![a-z])" + re.escape(term) + r"(?![a-z])", low):
                hits.append((where, f'named IP "{term}"'))
        if _STYLE.search(text or ""):
            hits.append((where, '"in the style of <artist>" — use original art direction'))
        if _TM.search(text or ""):
            hits.append((where, "trademark/registered symbol present"))
    print(f"=== lint_prompts: scanned {len(items)} text field(s) ===")
    for where, why in hits:
        print(f"  FAIL {where}: {why}")
    if not hits:
        print("  PASSED \u2713  no named franchises/characters/trademarks detected")
    return not hits


if __name__ == "__main__":
    sys.exit(0 if lint() else 1)
