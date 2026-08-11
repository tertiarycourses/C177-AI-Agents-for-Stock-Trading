"""Small cross-platform file helper used by the C177 lab command blocks."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from course_common import sha256_file


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    mkdir = sub.add_parser("mkdir")
    mkdir.add_argument("paths", nargs="+")
    copy = sub.add_parser("copy")
    copy.add_argument("source")
    copy.add_argument("destination")
    show = sub.add_parser("show")
    show.add_argument("path")
    unresolved = sub.add_parser("unresolved")
    unresolved.add_argument("path")
    locate = sub.add_parser("locate")
    locate.add_argument("paths", nargs="+")
    copytree = sub.add_parser("copytree")
    copytree.add_argument("source")
    copytree.add_argument("destination")
    args = parser.parse_args()

    if args.action == "mkdir":
        for value in args.paths:
            path = Path(value)
            path.mkdir(parents=True, exist_ok=True)
            print(f"DIRECTORY_READY: {path.resolve()}")
    elif args.action == "copy":
        destination = Path(args.destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.source, destination)
        print(f"COPIED: {Path(args.source).resolve()} -> {destination.resolve()}")
    elif args.action == "show":
        print(Path(args.path).read_text(encoding="utf-8"))
    elif args.action == "unresolved":
        text = Path(args.path).read_text(encoding="utf-8")
        hits = [
            (number, marker)
            for number, line in enumerate(text.splitlines(), start=1)
            for marker in ("OWNER_TO_VERIFY", "SOURCE_NEEDED", "MODEL_GUESS")
            if marker in line
        ]
        for number, marker in hits:
            print(f"line={number}; marker={marker}")
        print(f"unresolved_markers={len(hits)}")
        return 1 if hits else 0
    elif args.action == "locate":
        for value in args.paths:
            path = Path(value)
            if not path.is_file():
                print(f"MISSING: {path.resolve()}")
                return 1
            print(f"FILE: {path.resolve()}; bytes={path.stat().st_size}; sha256={sha256_file(path)}")
    else:
        source = Path(args.source)
        destination = Path(args.destination)
        if destination.exists():
            raise SystemExit(f"HOLD_COPY: destination already exists: {destination}")
        shutil.copytree(source, destination)
        print(f"CHECKPOINT_COPIED: {source.resolve()} -> {destination.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
