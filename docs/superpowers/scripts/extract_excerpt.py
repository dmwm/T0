#!/usr/bin/env python3
"""Print a `path:start-end` excerpt from the repo, with line numbers.

Usage:
    python docs/superpowers/scripts/extract_excerpt.py src/python/T0/__init__.py:1-9
"""
from __future__ import annotations
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def parse_ref(ref: str) -> tuple[Path, int, int]:
    if ":" not in ref:
        raise SystemExit(f"Bad ref {ref!r}; expected PATH:START-END or PATH:N")
    path_str, lines = ref.split(":", 1)
    if "-" in lines:
        start_s, end_s = lines.split("-", 1)
        start, end = int(start_s), int(end_s)
    else:
        start = end = int(lines)
    return REPO_ROOT / path_str, start, end


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    path, start, end = parse_ref(argv[1])
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    with path.open() as fh:
        lines = fh.readlines()
    if end > len(lines):
        raise SystemExit(f"{path} only has {len(lines)} lines; requested up to {end}")
    width = len(str(end))
    for i, line in enumerate(lines[start - 1 : end], start=start):
        print(f"{i:>{width}}  {line.rstrip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
