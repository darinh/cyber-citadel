"""Render every episode spec in order. Prints per-episode + total runtime."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_episode2 import assemble

ROOT = Path(__file__).resolve().parent.parent
specs = sorted((ROOT / "course" / "scripts").glob("ep*.json"))
only = sys.argv[1:]
if only:
    specs = [s for s in specs if s.stem in only]

t0 = time.time()
total_min = 0.0
for s in specs:
    print(f"\n===== RENDER {s.stem} =====")
    st = time.time()
    final = assemble(str(s))
    print(f"   rendered in {(time.time()-st)/60:.1f} min")
import subprocess
print(f"\nALL DONE in {(time.time()-t0)/60:.1f} min")
for f in sorted((ROOT / "course" / "episodes").glob("*.mp4")):
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout.strip()
    print(f"  {f.name:42s} {float(dur)/60:5.1f} min  {f.stat().st_size/1e6:5.1f} MB")
