"""Tests for theme toggle JavaScript functionality."""

import pytest
from pathlib import Path


@pytest.fixture(scope="module")
def js_theme_init():
    """Path to the theme init JavaScript file."""
    return Path(__file__).parent.parent / "static" / "js" / "theme-init.js"


@pytest.fixture(scope="module")
def js_theme_toggle():
    """Path to the theme toggle JavaScript file."""
    return Path(__file__).parent.parent / "static" / "js" / "theme-toggle.js"


@pytest.fixture(scope="module")
def main_css():
    """Path to the main CSS file."""
    return Path(__file__).parent.parent / "assets" / "css" / "main.css"


# =============================================================================
# Theme Init Script Tests
# =============================================================================


@pytest.mark.javascript
def test_theme_init_exists(js_theme_init):
    """Verify theme-init.js exists."""
    assert js_theme_init.exists(), "theme-init.js should exist"


@pytest.mark.javascript
def test_theme_init_reads_localstorage(js_theme_init):
    """Verify theme init reads from localStorage."""
    content = js_theme_init.read_text()
    assert "localStorage.getItem" in content


@pytest.mark.javascript
def test_theme_init_sets_data_attribute(js_theme_init):
    """Verify theme init sets data-theme attribute."""
    content = js_theme_init.read_text()
    assert 'setAttribute("data-theme"' in content or "setAttribute('data-theme'" in content


@pytest.mark.javascript
def test_theme_init_handles_exceptions(js_theme_init):
    """Verify theme init handles localStorage exceptions."""
    content = js_theme_init.read_text()
    assert "catch" in content or "try" in content


@pytest.mark.javascript
def test_theme_init_no_eval(js_theme_init):
    """Verify no eval() is used (security requirement)."""
    content = js_theme_init.read_text()
    assert "eval(" not in content, "eval() usage violates security standards"


# =============================================================================
# Theme Toggle Script Tests
# =============================================================================


@pytest.mark.javascript
def test_theme_toggle_exists(js_theme_toggle):
    """Verify theme-toggle.js exists."""
    assert js_theme_toggle.exists(), "theme-toggle.js should exist"


@pytest.mark.javascript
def test_theme_toggle_no_eval(js_theme_toggle):
    """Verify no eval() is used (security requirement)."""
    content = js_theme_toggle.read_text()
    assert "eval(" not in content, "eval() usage violates security standards"


@pytest.mark.javascript
def test_theme_toggle_no_innerhtml(js_theme_toggle):
    """Verify no innerHTML is used (security requirement)."""
    content = js_theme_toggle.read_text()
    assert "innerHTML" not in content, "innerHTML usage violates security standards"


@pytest.mark.javascript
def test_theme_toggle_uses_textcontent(js_theme_toggle):
    """Verify textContent is used for button text."""
    content = js_theme_toggle.read_text()
    assert "textContent" in content, "Should use textContent for safe DOM manipulation"


@pytest.mark.javascript
def test_theme_toggle_uses_localstorage(js_theme_toggle):
    """Verify localStorage is used for persistence."""
    content = js_theme_toggle.read_text()
    assert "localStorage" in content


@pytest.mark.javascript
def test_theme_toggle_checks_system_preference(js_theme_toggle):
    """Verify system preference is checked."""
    content = js_theme_toggle.read_text()
    assert "prefers-color-scheme" in content


@pytest.mark.javascript
def test_theme_toggle_handles_media_query_change(js_theme_toggle):
    """Verify media query change listener exists."""
    content = js_theme_toggle.read_text()
    assert 'addEventListener("change"' in content or "addEventListener('change'" in content


@pytest.mark.javascript
def test_theme_toggle_has_aria_label(js_theme_toggle):
    """Verify accessibility attributes are set."""
    content = js_theme_toggle.read_text()
    assert "aria-label" in content


@pytest.mark.javascript
def test_theme_toggle_clears_storage(js_theme_toggle):
    """Verify storage can be cleared when returning to system preference."""
    content = js_theme_toggle.read_text()
    assert "removeItem" in content


@pytest.mark.javascript
def test_theme_toggle_storage_key(js_theme_toggle):
    """Verify consistent storage key is used."""
    content = js_theme_toggle.read_text()
    assert "theme-preference" in content


# =============================================================================
# CSS Theme Support Tests
# =============================================================================


@pytest.mark.javascript
def test_css_has_light_theme_override(main_css):
    """Verify CSS has light theme data attribute selector."""
    content = main_css.read_text()
    assert '[data-theme="light"]' in content


@pytest.mark.javascript
def test_css_has_dark_theme_override(main_css):
    """Verify CSS has dark theme data attribute selector."""
    content = main_css.read_text()
    assert '[data-theme="dark"]' in content


@pytest.mark.javascript
def test_css_has_theme_toggle_button_styles(main_css):
    """Verify CSS has theme toggle button styles."""
    content = main_css.read_text()
    assert ".theme-toggle-btn" in content


@pytest.mark.javascript
def test_css_theme_button_has_focus_styles(main_css):
    """Verify theme button has focus-visible styles for accessibility."""
    content = main_css.read_text()
    assert ".theme-toggle-btn:focus-visible" in content


@pytest.mark.javascript
def test_css_preserves_system_preference(main_css):
    """Verify CSS still supports system preference when no override."""
    content = main_css.read_text()
    assert "@media (prefers-color-scheme: dark)" in content
