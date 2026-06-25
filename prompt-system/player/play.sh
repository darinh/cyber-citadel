#!/usr/bin/env bash
# One-click local playback for this course (macOS / Linux). Needs Python 3.
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then python3 serve.py "$@"; else python serve.py "$@"; fi
