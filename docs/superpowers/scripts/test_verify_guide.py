"""Unit tests for verify_guide.py."""
from __future__ import annotations
import sys
import textwrap
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_guide as vg  # noqa: E402


def chapter_block(n: int, *, sections: list[str] | None = None,
                  diagrams: int = 1, excerpts: list[str] | None = None) -> str:
    if sections is None:
        sections = ["setup", "diagrams", "code", "deeper-dive", "takeaways", "self-check"]
    parts = [f'<section id="chapter-{n}"><h2>Chapter {n}</h2>']
    for s in sections:
        parts.append(f'<div id="ch{n}-{s}">x</div>')
    for _ in range(diagrams):
        parts.append('<pre class="mermaid">graph LR; a-->b;</pre>')
    for ref in excerpts or []:
        parts.append(f'<!-- excerpt: {ref} --><pre><code>x</code></pre>')
    parts.append('</section>')
    return "\n".join(parts)


def make_guide(chapters: int = 6, **kwargs) -> str:
    nav_links = "".join(f'<a href="#chapter-{n}">Ch {n}</a>' for n in range(1, chapters + 1))
    body = "".join(chapter_block(n, **kwargs) for n in range(1, chapters + 1))
    return textwrap.dedent(f"""\
        <!doctype html><html><body>
        <nav class="toc">{nav_links}</nav>
        <main>{body}</main>
        </body></html>
    """)


class CheckChapterCount(unittest.TestCase):
    def test_all_six_present(self) -> None:
        self.assertEqual(vg.check_chapter_count(make_guide()), [])

    def test_missing_chapter(self) -> None:
        html = make_guide(chapters=5)
        issues = vg.check_chapter_count(html)
        self.assertTrue(any("expected 1..6" in i for i in issues), issues)


class CheckChapterSections(unittest.TestCase):
    def test_all_sections_present(self) -> None:
        self.assertEqual(vg.check_chapter_sections(make_guide(diagrams=3)), [])

    def test_missing_section(self) -> None:
        html = make_guide(sections=["setup", "diagrams", "code", "takeaways", "self-check"])
        issues = vg.check_chapter_sections(html)
        self.assertTrue(any("deeper-dive" in i for i in issues), issues)


class CheckDiagramCount(unittest.TestCase):
    def test_enough_diagrams(self) -> None:
        # 6 chapters * 3 diagrams = 18 ≥ 15
        self.assertEqual(vg.check_diagram_count(make_guide(diagrams=3)), [])

    def test_too_few_diagrams(self) -> None:
        # 6 chapters * 1 diagram = 6 < 15
        issues = vg.check_diagram_count(make_guide(diagrams=1))
        self.assertEqual(len(issues), 1)
        self.assertIn("at least 15", issues[0])


class CheckExcerptRefs(unittest.TestCase):
    def test_valid_excerpt(self) -> None:
        # src/python/T0/__init__.py exists at the repo root and has 8 lines.
        html = '<!-- excerpt: src/python/T0/__init__.py:1-5 --><pre><code>x</code></pre>'
        self.assertEqual(vg.check_excerpt_refs(html), [])

    def test_missing_file(self) -> None:
        html = '<!-- excerpt: src/python/T0/does_not_exist.py:1-5 --><pre><code>x</code></pre>'
        self.assertTrue(vg.check_excerpt_refs(html))

    def test_line_out_of_range(self) -> None:
        html = '<!-- excerpt: src/python/T0/__init__.py:1-9999 --><pre><code>x</code></pre>'
        issues = vg.check_excerpt_refs(html)
        self.assertTrue(any("exceeds file" in i for i in issues), issues)


class CheckTocAnchors(unittest.TestCase):
    def test_all_resolve(self) -> None:
        self.assertEqual(vg.check_toc_anchors(make_guide()), [])

    def test_dangling_link(self) -> None:
        html = make_guide().replace('href="#chapter-3"', 'href="#chapter-99"')
        issues = vg.check_toc_anchors(html)
        self.assertTrue(any("chapter-99" in i for i in issues), issues)


if __name__ == "__main__":
    unittest.main()
