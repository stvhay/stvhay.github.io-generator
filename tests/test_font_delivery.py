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


def test_woff2_payload_uses_latin_subsets():
    """The two variable web fonts stay within the Latin-subset budget."""
    fonts = list((ROOT / "static" / "fonts").glob("*.woff2"))
    total_bytes = sum(font.stat().st_size for font in fonts)

    assert len(fonts) == 2
    assert all("Latin" in font.name for font in fonts)
    assert 0 < total_bytes < 400_000
