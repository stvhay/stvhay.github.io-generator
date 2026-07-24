"""Tests for efficient local font delivery."""

from pathlib import Path


ROOT = Path(__file__).parent.parent


def test_source_serif_uses_woff2_only():
    """Browser font assets use the compressed web-font format."""
    css = (ROOT / "assets" / "css" / "main.css").read_text()
    fonts = list((ROOT / "static" / "fonts").iterdir())

    assert css.count('format("woff2")') == 2
    assert ".ttf" not in css
    assert fonts
    assert all(font.suffix == ".woff2" for font in fonts)


def test_woff2_payload_is_smaller_than_previous_ttf_total():
    """The two web fonts remain below the former 2 MiB TTF payload."""
    total_bytes = sum(
        font.stat().st_size for font in (ROOT / "static" / "fonts").glob("*.woff2")
    )
    assert 0 < total_bytes < 2_000_000
