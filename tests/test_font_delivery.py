"""Tests for efficient local font delivery."""

import re
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


def test_site_owned_styles_reference_shipped_woff2_fonts():
    """Primary and generated-document styles load the shipped web fonts."""
    for css_path in (
        ROOT / "assets" / "css" / "main.css",
        ROOT / "static" / "css" / "latexml" / "site.css",
    ):
        css = css_path.read_text()
        sources = re.findall(
            r'src:\s*url\("(/fonts/SourceSerif4[^"?]+)"\)\s*format\("([^"]+)"\)',
            css,
        )

        assert len(sources) == 2, css_path
        for url, font_format in sources:
            assert font_format == "woff2", css_path
            assert (ROOT / "static" / url.lstrip("/")).is_file(), (css_path, url)
