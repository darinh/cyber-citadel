# Build your own narrated, interactive **video training course**

This folder is a self-contained engine + prompt system for **GitHub Copilot CLI**. Give it a topic
and the look/feel you want, and it produces a **binge-watchable video course** that runs **locally**
in your browser — with original characters, an original world in your chosen aesthetic, neural
narration, sourced music, and a signature **interactive quiz** where you click answers laid right
over the video. No cloud, no accounts, no publishing.

It works **with or without a GPU** — it uses the **same high-quality models either way**; a machine
without a GPU just renders more slowly (it never silently drops to lower quality). It produces a
**single video** or a **whole course**. Quizzes are on by default; study guides, custom avatars, and
music are optional.

## Quick start
1. Open **this folder** in GitHub Copilot CLI (it auto-loads `AGENTS.md`).
2. Say what you want, e.g.:
   > *"Make me a 1-video course on home espresso, warm hand-drawn cafe vibe."*
   > *"Build a 4-episode course on basic personal finance, cozy storybook world, with quizzes."*
3. The agent interviews you briefly, then walks the pipeline (`system-prompts/01…12`): truth layer →
   world + cast → avatars → voices → music → script → gates → render → **play locally**.
4. When it's done, double-click **`play.cmd`** (Windows) or run **`./play.sh`** (macOS/Linux) and watch.

## What you can theme it as
Any **original** world in the vibe you like — a wizard academy, a saturday-morning cartoon, a
high-fantasy guild, a neon hacker city, a cozy kitchen. It builds **original** characters and places
in that style; it will **not** use real franchises, characters, or trademarks (a gate blocks that).

## Requirements
- **Python 3.10+** and **ffmpeg** on your PATH (the setup prompt installs the rest).
- A GPU is optional. You get the **same high quality** on any machine — expressive cloned voices +
  AI-generated portraits — because the same models run on CPU too. A GPU just makes rendering faster;
  a CPU-only laptop takes longer. Quality is only reduced if **you** explicitly ask to trade it for speed.

## What's in here
| Path | What it is |
|------|-----------|
| `AGENTS.md` | The agent's entry point (auto-loaded by Copilot CLI). |
| `system-prompts/` | The numbered phase prompts that drive a build. |
| `engine/` | The tested, theme-agnostic engine (renderer, voices, music, gates) — don't edit for content. |
| `player/` | The local interactive player + a tiny range server + launchers. |
| `reference/` | The contracts + rules the prompts cite (scene fields, accuracy, audio, licensing…). |
| `schemas/` | JSON schemas for `theme.json`, the episode spec, the truth layer, and intake. |
| `examples/kitchen-academy/` | A complete worked example (a knife-skills lesson) you can render and watch. |

## Try the example
```bash
# from this folder (set CC_PROJECT to the example):
python engine/probe.py                       # see your render-speed + the high-quality models
CC_PROJECT=examples/kitchen-academy CC_THEME=examples/kitchen-academy/theme.json \
  python engine/build_episode.py examples/kitchen-academy/course/scripts/ep01.json
python engine/package.py --project examples/kitchen-academy
cd examples/kitchen-academy && python serve.py        # opens the player in your browser
```

## Ground rules it follows
- **Accuracy:** every on-screen fact/quote comes from a truth layer you build from real source
  material — never invented. A deterministic gate enforces it.
- **Original IP only:** your aesthetic becomes original characters/worlds, never a named franchise.
- **Sourced audio:** music is public-domain / Creative-Commons (attributed) — never AI-generated.
- **Quality is fixed; only the content/look is yours to tailor.**

See `AGENTS.md` for the full pipeline and `reference/TROUBLESHOOTING.md` if something doesn't run.
