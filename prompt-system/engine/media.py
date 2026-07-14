"""Media manifest loader and provenance validator.

New courses reference images and video clips by stable keys from
``assets/media.json``. Keeping path, provenance, license, credit, and
accessibility text together lets the renderer stay declarative and lets gates
fail before an expensive render when an asset is missing or unlicensed.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

PROJECT = Path(os.environ.get("CC_PROJECT") or Path.cwd())
THIRD_PARTY_ORIGINS = {"public-domain", "cc0", "cc-by", "licensed"}
VALID_ORIGINS = THIRD_PARTY_ORIGINS | {"original", "generated-original"}
VALID_KINDS = {"image", "video"}


def manifest_path(project: Path | None = None) -> Path:
    return (project or PROJECT) / "assets" / "media.json"


def load(project: Path | None = None) -> dict:
    path = manifest_path(project)
    if not path.exists():
        return {"schema_version": "2.0", "assets": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def get(ref: str, project: Path | None = None) -> dict | None:
    return (load(project).get("assets") or {}).get(ref)


def resolve(ref: str, project: Path | None = None) -> Path:
    """Resolve a manifest key. Direct paths remain available for legacy v1 specs."""
    project = project or PROJECT
    entry = get(ref, project)
    raw = entry.get("path") if entry else ref
    path = Path(raw)
    if not path.is_absolute():
        path = project / path
    return path


def fingerprint(ref: str | None, project: Path | None = None) -> tuple:
    """Stable cache input that changes whenever the referenced file changes."""
    if not ref:
        return ()
    path = resolve(ref, project)
    if not path.exists():
        return (str(path), "missing")
    stat = path.stat()
    return (str(path.resolve()), stat.st_size, stat.st_mtime_ns)


def validate(project: Path | None = None) -> list[tuple[str, str, str]]:
    project = project or PROJECT
    path = manifest_path(project)
    problems: list[tuple[str, str, str]] = []
    if not path.exists():
        return problems
    try:
        data = load(project)
    except (OSError, json.JSONDecodeError) as exc:
        return [("P1", "MEDIA_JSON", f"cannot parse {path}: {exc}")]

    assets = data.get("assets")
    if not isinstance(assets, dict):
        return [("P1", "MEDIA_SHAPE", "assets/media.json must contain an 'assets' object")]

    for key, item in assets.items():
        where = f"assets.media[{key}]"
        if not isinstance(item, dict):
            problems.append(("P1", "MEDIA_ENTRY", f"{where} must be an object"))
            continue
        kind = item.get("kind")
        origin = item.get("origin")
        if kind not in VALID_KINDS:
            problems.append(("P1", "MEDIA_KIND", f"{where}.kind must be image or video"))
        if origin not in VALID_ORIGINS:
            problems.append(("P1", "MEDIA_ORIGIN", f"{where}.origin is missing or unsupported"))
        if not item.get("path"):
            problems.append(("P1", "MEDIA_PATH", f"{where}.path is required"))
        else:
            resolved = resolve(key, project)
            if not resolved.exists():
                problems.append(("P1", "MEDIA_MISSING", f"{where} file does not exist: {resolved}"))
        if not str(item.get("alt", "")).strip():
            problems.append(("P1", "MEDIA_ALT", f"{where}.alt is required for accessibility"))
        for field in ("license", "creator"):
            if not str(item.get(field, "")).strip():
                problems.append(("P1", "MEDIA_PROVENANCE", f"{where}.{field} is required"))
        if origin in THIRD_PARTY_ORIGINS:
            for field in ("source_url",):
                if not str(item.get(field, "")).strip():
                    problems.append(("P1", "MEDIA_PROVENANCE", f"{where}.{field} is required"))
        if origin == "cc-by" and not str(item.get("credit", "")).strip():
            problems.append(("P1", "MEDIA_CREDIT", f"{where}.credit is required for CC-BY"))
        if origin == "generated-original":
            generation = item.get("generation") or {}
            for field in ("tool", "model", "prompt", "seed"):
                if generation.get(field) in (None, ""):
                    problems.append((
                        "P1", "MEDIA_GENERATION", f"{where}.generation.{field} is required",
                    ))
    return problems
