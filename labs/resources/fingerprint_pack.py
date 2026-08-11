"""Create or verify SHA-256 manifests for one C177 lab checkpoint."""

from __future__ import annotations

import argparse
from pathlib import Path

from course_common import checkpoint_inventory, read_json, utc_now, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output")
    group.add_argument("--verify")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Checkpoint folder not found: {root}")
    actual = checkpoint_inventory(root)

    if args.output:
        output = Path(args.output).resolve()
        write_json(
            output,
            {
                "algorithm": "sha256",
                "created_at_utc": utc_now(),
                "root": root.name,
                "file_count": len(actual),
                "files": actual,
            },
        )
        print(f"FINGERPRINTS_WRITTEN: {len(actual)} files -> {output}")
        return 0

    manifest = read_json(args.verify)
    expected = manifest.get("files", {})
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(name for name in set(expected) & set(actual) if expected[name] != actual[name])
    if missing or extra or changed:
        print("HOLD_FINGERPRINT_MISMATCH")
        print(f"missing={missing}")
        print(f"extra={extra}")
        print(f"changed={changed}")
        return 1
    print(f"FINGERPRINTS_VERIFIED: {len(actual)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
