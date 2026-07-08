"""Hardware capability probe + tier chooser (GPU if available, graceful fallback otherwise).

Detects CUDA + VRAM, RAM, ffmpeg, OS, optional engines, and picks a TIER per subsystem so a
run never hard-fails on a non-CUDA / low-VRAM / CPU-only machine. Writes capabilities.json.

  python probe.py            # print a report + write capabilities.json
  python probe.py --json     # machine-readable only
  python probe.py preflight  # print the download/setup plan for the chosen tiers

Quality/structure/interactivity are IDENTICAL across tiers; only voice timbre + avatar fidelity
(and render speed) vary. Strict VRAM thresholds avoid the classic "download 10GB then OOM" trap.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(os.environ.get("CC_PROJECT") or Path.cwd())


def _has(cmd):
    return shutil.which(cmd) is not None


def _cuda():
    """Return (available, vram_gb, name)."""
    try:
        import torch
        if torch.cuda.is_available():
            p = torch.cuda.get_device_properties(0)
            return True, round(p.total_memory / (1024 ** 3), 1), p.name
    except Exception:                                       # noqa: BLE001
        pass
    # torch missing/CPU-only: try nvidia-smi for awareness (won't be usable without CUDA torch)
    if _has("nvidia-smi"):
        try:
            out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total",
                                  "--format=csv,noheader,nounits"],
                                 capture_output=True, text=True).stdout.strip().splitlines()
            if out:
                name, mem = out[0].split(",")
                return False, round(int(mem.strip()) / 1024, 1), name.strip() + " (no CUDA torch)"
        except Exception:                                   # noqa: BLE001
            pass
    return False, 0.0, ""


def _ram_gb():
    try:
        if hasattr(os, "sysconf") and "SC_PAGE_SIZE" in os.sysconf_names:
            return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024 ** 3), 1)
    except Exception:                                       # noqa: BLE001
        pass
    if platform.system() == "Windows":
        try:
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            ms = MS(); ms.dwLength = ctypes.sizeof(MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
            return round(ms.ullTotalPhys / (1024 ** 3), 1)
        except Exception:                                   # noqa: BLE001
            pass
    return 0.0


def _spec(name):
    try:
        import importlib.util
        return importlib.util.find_spec(name) is not None
    except Exception:                                       # noqa: BLE001
        return False


def detect():
    cuda, vram, gpu = _cuda()
    ram = _ram_gb()
    caps = {
        "os": platform.system(),
        "python": platform.python_version(),
        "ffmpeg": _has("ffmpeg") and _has("ffprobe"),
        "node": _has("node"),
        "cuda": cuda,
        "vram_gb": vram,
        "gpu": gpu,
        "ram_gb": ram,
        "have": {k: _spec(k) for k in ("torch", "chatterbox", "faster_whisper", "piper", "diffusers")},
    }
    # ---- QUALITY-FIRST tiers -------------------------------------------------------------
    # Quality is FIXED at the highest models; hardware only changes SPEED. A missing GPU does NOT
    # lower quality — the same models run on CPU, just slower. Downgrades are NEVER auto-applied;
    # they are opt-in and require the user's explicit approval (env vars below).
    caps["recommended"] = {
        "tts": "chatterbox",            # high-quality neural voice (GPU or CPU)
        "avatars": "sdxl",              # SDXL portraits (GPU or CPU)
        "stt": "large-v3",              # strongest audio-QA gate
        "stt_compute": "float16" if cuda else "int8",
    }
    # expected SPEED of the high-quality path on this machine (quality is identical across these)
    if cuda and vram >= 8:
        caps["speed"] = "fast"
    elif cuda:
        caps["speed"] = "ok"            # low-VRAM GPU
    else:
        caps["speed"] = "slow"          # CPU-only: still full quality, but renders take much longer
    caps["overall"] = "gpu" if cuda else "cpu"
    # optional, USER-APPROVED-ONLY speed downgrades (the engine never applies these automatically)
    caps["downgrades_opt_in"] = {
        "tts": "CC_TTS=piper       (fast, robotic voices — a QUALITY downgrade)",
        "avatars": "CC_AVATARS=illustrated  (instant geometric portraits instead of SDXL)",
        "stt": "CC_STT_MODEL=small (faster but weaker audio-QA gate)",
    }
    if cuda and vram and vram < 6:
        caps["notes"] = ("GPU VRAM is low; high-quality models may spill to CPU/RAM and run slowly. "
                         "Quality stays high — only speed is affected.")
    return caps


_PLAN = {
    "tts": {
        "chatterbox": "pip install chatterbox-tts torch  (~3GB weights on first run; GPU via the cu124 index, else CPU)",
    },
    "stt": {
        "large-v3": "faster-whisper downloads large-v3 (~3GB) on first verify (GPU or CPU)",
    },
    "avatars": {
        "sdxl": "pip install diffusers transformers accelerate ; SDXL (~6GB) on first run (GPU or CPU)",
    },
}


def preflight(caps):
    print("Preflight — download the HIGH-QUALITY models BEFORE a live run (same models on GPU/CPU):")
    for sub in ("tts", "stt", "avatars"):
        tier = caps["recommended"][sub]
        print(f"  - {sub:8s} [{tier}]: {_PLAN.get(sub, {}).get(tier, '(no extra setup)')}")
    if not caps["ffmpeg"]:
        print("  ! ffmpeg/ffprobe NOT found — install ffmpeg 6+ and put it on PATH (required).")
    if caps["overall"] == "cpu":
        print("  note: CPU-only — SAME high quality, but renders are much slower. Warn the user and get")
        print("        explicit approval before applying any speed downgrade (CC_TTS=piper, etc.).")


def main():
    caps = detect()
    if "--json" in sys.argv:
        print(json.dumps(caps, indent=1))
    elif len(sys.argv) > 1 and sys.argv[1] == "preflight":
        preflight(caps)
    else:
        print(f"OS {caps['os']} · Python {caps['python']} · RAM {caps['ram_gb']}GB · ffmpeg {caps['ffmpeg']}")
        print(f"GPU: {caps['gpu'] or 'none'} · CUDA {caps['cuda']} · VRAM {caps['vram_gb']}GB")
        print(f"render speed on this machine: {caps['speed'].upper()} "
              f"({'GPU' if caps['overall'] == 'gpu' else 'CPU — high quality, just slower'})")
        print("recommended models (HIGH QUALITY — used on GPU or CPU):")
        for k, v in caps["recommended"].items():
            print(f"  {k:12s}: {v}")
        if caps.get("notes"):
            print(f"note: {caps['notes']}")
        print("downgrades are OPT-IN only (never automatic) — apply ONLY with user approval:")
        for k, v in caps["downgrades_opt_in"].items():
            print(f"  {k:12s}: {v}")
    (PROJECT / "capabilities.json").write_text(json.dumps(caps, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
