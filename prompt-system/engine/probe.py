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
    # ---- tier choices (strict thresholds to avoid runtime OOM) ----
    if cuda and vram >= 6:
        tts = "chatterbox"
    else:
        tts = "piper"
    if cuda and vram >= 10:
        avatars = "sdxl_ipa"          # SDXL base portraits + IP-Adapter expressions
    elif cuda and vram >= 4:
        avatars = "sd_turbo"          # few-step turbo portraits (no IP-Adapter)
    else:
        avatars = "illustrated"       # deterministic Pillow portraits OR bring-your-own images
    if cuda and vram >= 8:
        stt = "large-v3"
    elif cuda or ram >= 12:
        stt = "small"
    else:
        stt = "base"
    caps["tiers"] = {"tts": tts, "avatars": avatars, "stt": stt,
                     "stt_compute": "float16" if cuda else "int8"}
    caps["overall"] = ("gpu" if (cuda and vram >= 10) else
                       "low_gpu" if cuda else "cpu")
    return caps


_PLAN = {
    "tts": {
        "chatterbox": "pip install chatterbox-tts torch --index-url https://download.pytorch.org/whl/cu124  (~3GB weights on first run)",
        "piper": "pip install piper-tts ; download 2-3 voice .onnx models into assets/voices/ (~60MB each)",
    },
    "stt": {
        "large-v3": "faster-whisper downloads large-v3 (~3GB) on first verify",
        "small": "faster-whisper downloads small int8 (~0.5GB) on first verify",
        "base": "faster-whisper downloads base int8 (~0.15GB) on first verify",
    },
    "avatars": {
        "sdxl_ipa": "pip install diffusers ; SDXL base (~6GB) + IP-Adapter (~1GB) on first run",
        "sd_turbo": "pip install diffusers ; SD-Turbo (~2GB), few-step portraits, no IP-Adapter",
        "illustrated": "no model download — deterministic Pillow portraits, or bring your own images",
    },
}


def preflight(caps):
    print("Preflight plan for the detected tiers (download BEFORE a live run):")
    for sub in ("tts", "stt", "avatars"):
        tier = caps["tiers"][sub]
        print(f"  - {sub:8s} [{tier}]: {_PLAN.get(sub, {}).get(tier, '(no extra setup)')}")
    if not caps["ffmpeg"]:
        print("  ! ffmpeg/ffprobe NOT found — install ffmpeg 6+ and put it on PATH (required).")
    if caps["overall"] == "cpu":
        print("  note: CPU-only — renders work but are slower; expect piper voices + illustrated avatars.")


def main():
    caps = detect()
    if "--json" in sys.argv:
        print(json.dumps(caps, indent=1))
    elif len(sys.argv) > 1 and sys.argv[1] == "preflight":
        preflight(caps)
    else:
        print(f"OS {caps['os']} · Python {caps['python']} · RAM {caps['ram_gb']}GB · ffmpeg {caps['ffmpeg']}")
        print(f"GPU: {caps['gpu'] or 'none'} · CUDA {caps['cuda']} · VRAM {caps['vram_gb']}GB")
        print(f"overall tier: {caps['overall'].upper()}")
        for k, v in caps["tiers"].items():
            print(f"  {k:12s}: {v}")
    (PROJECT / "capabilities.json").write_text(json.dumps(caps, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
