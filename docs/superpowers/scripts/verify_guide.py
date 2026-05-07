#!/usr/bin/env python3
"""Verify the T0 Architecture Guide HTML artifact meets acceptance criteria."""
from __future__ import annotations
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
GUIDE_PATH = REPO_ROOT / "docs/superpowers/t0-architecture-guide.html"

REQUIRED_CHAPTERS = 6
REQUIRED_DIAGRAMS = 15
CHAPTER_SUBSECTIONS = ["setup", "diagrams", "code", "deeper-dive", "takeaways", "self-check"]


def check_chapter_count(html: str) -> list[str]:
    found = sorted(int(m) for m in re.findall(r'<section[^>]*id="chapter-(\d+)"', html))
    if found != list(range(1, REQUIRED_CHAPTERS + 1)):
        return [f"Chapters found: {found}, expected 1..{REQUIRED_CHAPTERS}"]
    return []


def check_chapter_sections(html: str) -> list[str]:
    issues: list[str] = []
    for n in range(1, REQUIRED_CHAPTERS + 1):
        m = re.search(
            rf'<section[^>]*id="chapter-{n}"(.*?)(?=<section[^>]*id="chapter-|</main)',
            html, re.DOTALL,
        )
        if not m:
            issues.append(f"Chapter {n}: section not found")
            continue
        body = m.group(1)
        for sub in CHAPTER_SUBSECTIONS:
            if not re.search(rf'id="ch{n}-{re.escape(sub)}"', body):
                issues.append(f"Chapter {n}: missing subsection id ch{n}-{sub}")
        if not re.search(r'<pre class="mermaid">', body):
            issues.append(f"Chapter {n}: contains no mermaid diagram")
    return issues


def check_diagram_count(html: str) -> list[str]:
    n = len(re.findall(r'<pre class="mermaid">', html))
    if n < REQUIRED_DIAGRAMS:
        return [f"Found {n} mermaid blocks; need at least {REQUIRED_DIAGRAMS}"]
    return []


def check_excerpt_refs(html: str) -> list[str]:
    issues: list[str] = []
    pattern = re.compile(r'<!--\s*excerpt:\s*([^:\s]+):(\d+)(?:-(\d+))?\s*-->')
    for m in pattern.finditer(html):
        path_str, start_s, end_s = m.group(1), m.group(2), m.group(3)
        end = int(end_s) if end_s else int(start_s)
        full = REPO_ROOT / path_str
        if not full.exists():
            issues.append(f"Excerpt source missing: {path_str}")
            continue
        line_count = sum(1 for _ in full.open())
        if end > line_count:
            issues.append(
                f"Excerpt {path_str}:{start_s}-{end} exceeds file (only {line_count} lines)"
            )
    return issues


def check_toc_anchors(html: str) -> list[str]:
    nav_match = re.search(
        r'<nav[^>]*class="[^"]*\btoc\b[^"]*"[^>]*>(.*?)</nav>', html, re.DOTALL
    )
    if not nav_match:
        return ["TOC nav not found"]
    referenced = set(re.findall(r'href="#([^"]+)"', nav_match.group(1)))
    defined = set(re.findall(r'id="([^"]+)"', html))
    missing = referenced - defined
    return [f"TOC link target missing: #{a}" for a in sorted(missing)]


CHECKS = (
    check_chapter_count,
    check_chapter_sections,
    check_diagram_count,
    check_excerpt_refs,
    check_toc_anchors,
)


def main() -> int:
    if not GUIDE_PATH.exists():
        print(f"FAIL: guide not found at {GUIDE_PATH}")
        return 1
    html = GUIDE_PATH.read_text()
    issues: list[str] = []
    for check in CHECKS:
        issues.extend(check(html))
    if issues:
        for issue in issues:
            print(f"  FAIL: {issue}")
        return 1
    print("OK: guide passes all checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
