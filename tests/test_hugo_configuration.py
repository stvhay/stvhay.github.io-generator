"""Tests for current Hugo configuration and template APIs."""

from pathlib import Path


ROOT = Path(__file__).parent.parent


def test_language_configuration_uses_current_hugo_api():
    """Locale and direction avoid APIs scheduled for removal."""
    config = (ROOT / "hugo.toml").read_text()
    base = (ROOT / "layouts" / "_default" / "baseof.html").read_text()

    assert "locale = 'en-US'" in config
    assert "languageCode" not in config
    assert ".Language.Locale" in base
    assert ".Language.Direction" in base
    assert ".Language.LanguageCode" not in base
    assert ".Language.LanguageDirection" not in base
