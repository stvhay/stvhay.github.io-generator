"""Regression tests for the generated homepage design."""

from conftest import parse_html


def test_homepage_uses_factual_positioning_heading(public_dir):
    homepage = parse_html(public_dir / "index.html")

    assert homepage.h1.get_text(" ", strip=True) == "Engineer learning neuroscience"
