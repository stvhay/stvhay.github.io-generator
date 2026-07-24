"""Tests for the site's documented typographic roles."""

import re
from pathlib import Path


CSS = (Path(__file__).parent.parent / "assets" / "css" / "main.css").read_text()
CSS_WITHOUT_COMMENTS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.DOTALL)


def declarations(selector: str) -> str:
    """Return declarations for one exact selector block."""
    normalized = " ".join(selector.split())
    for candidate, body in re.findall(r"([^{}]+)\{([^{}]*)\}", CSS_WITHOUT_COMMENTS):
        if " ".join(candidate.split()) == normalized:
            return body
    raise AssertionError(f"Missing selector: {selector}")


def test_display_type_is_fluid_compact_and_balanced():
    display = declarations(".site-title,\nh1")
    headings = declarations("h1,\nh2")

    assert "font-size: clamp(2rem, 1.75rem + 1.25vw, 2.5rem)" in display
    assert "line-height: 1.15" in display
    assert "text-wrap: balance" in headings


def test_heading_roles_use_the_documented_scale():
    section = declarations("h2")
    minor = declarations("h3,\nh4,\nh5,\nh6")
    card = declarations(".post-text h2")

    assert "font-size: 1.5rem" in section
    assert "line-height: 1.25" in section
    assert "font-size: 1.2rem" in minor
    assert "line-height: 1.35" in minor
    assert "font-size: 1.25rem" in card
    assert "line-height: 1.3" in card
