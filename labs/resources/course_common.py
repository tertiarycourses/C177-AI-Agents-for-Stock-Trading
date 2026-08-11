"""Shared utilities for the C177 connected labs."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, payload: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, default=str)
        handle.write("\n")


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


CHECKPOINT_SKIP_NAMES = {"fingerprints.json", ".DS_Store"}


def checkpoint_inventory(root: str | Path) -> dict[str, str]:
    """Return the exact fingerprintable files below one checkpoint folder."""
    base = Path(root).resolve()
    return {
        path.relative_to(base).as_posix(): sha256_file(path)
        for path in sorted(base.rglob("*"))
        if path.is_file()
        and path.name not in CHECKPOINT_SKIP_NAMES
        and not path.name.startswith("~$")
    }


def checkpoint_errors(root: str | Path, manifest_path: str | Path | None = None) -> list[str]:
    """Compare a checkpoint with its saved manifest and return exact defects."""
    base = Path(root).resolve()
    manifest = Path(manifest_path).resolve() if manifest_path else base / "fingerprints.json"
    if not base.is_dir():
        return [f"missing checkpoint folder: {base}"]
    if not manifest.is_file():
        return [f"missing fingerprint manifest: {manifest}"]
    payload = read_json(manifest)
    expected = payload.get("files")
    if not isinstance(expected, dict):
        return [f"invalid fingerprint manifest: {manifest}"]
    actual = checkpoint_inventory(base)
    errors = [f"missing file: {name}" for name in sorted(set(expected) - set(actual))]
    errors.extend(f"unexpected file: {name}" for name in sorted(set(actual) - set(expected)))
    errors.extend(
        f"changed file: {name}"
        for name in sorted(set(expected) & set(actual))
        if expected[name] != actual[name]
    )
    return errors


def require_checkpoint(root: str | Path, label: str) -> Path:
    """Stop a consequential workflow when a checkpoint does not verify."""
    base = Path(root).resolve()
    errors = checkpoint_errors(base)
    if errors:
        joined = "; ".join(errors)
        raise SystemExit(f"HOLD_FINGERPRINT_MISMATCH: {label}: {joined}")
    return base / "fingerprints.json"


def is_placeholder(value: str | None) -> bool:
    if not value:
        return True
    stripped = value.strip()
    return stripped.startswith("<") or stripped in {"CHANGE_ME", "REPLACE_ME"}


def find_unresolved(value: Any, prefix: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            hits.extend(find_unresolved(item, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(find_unresolved(item, f"{prefix}[{index}]"))
    elif isinstance(value, str) and any(
        marker in value for marker in ("OWNER_TO_VERIFY", "SOURCE_NEEDED", "MODEL_GUESS")
    ):
        hits.append(prefix)
    return hits


SECRET_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(OPENAI_API_KEY|ALPACA_API_KEY|ALPACA_SECRET_KEY)\s*[=:]\s*(?!<)[A-Za-z0-9_\-]{12,}"),
]


def scan_secret_hits(root: str | Path) -> list[dict[str, Any]]:
    base = Path(root)
    hits: list[dict[str, Any]] = []
    text_suffixes = {".md", ".txt", ".json", ".csv", ".py", ".env", ".yaml", ".yml"}
    for path in sorted(base.rglob("*")):
        relative_parts = path.relative_to(base).parts
        if any(part in {".git", ".venv", "__pycache__"} for part in relative_parts):
            continue
        if not path.is_file() or path.suffix.lower() not in text_suffixes:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line_number, line in enumerate(content.splitlines(), start=1):
            if "<OPENAI_API_KEY>" in line or "<ALPACA_PAPER_" in line:
                continue
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                hits.append({"file": path.relative_to(base).as_posix(), "line": line_number})
    return hits


def safe_within(base: Path, relative: str) -> Path:
    candidate = (base / relative).resolve()
    resolved_base = base.resolve()
    if candidate != resolved_base and resolved_base not in candidate.parents:
        raise ValueError("Requested path is outside the allowed course pack")
    return candidate


def pydantic_dump(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "dict"):
        return value.dict()
    raise TypeError(f"Unsupported model type: {type(value)!r}")
