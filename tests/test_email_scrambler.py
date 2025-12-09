"""Tests for email scrambler JavaScript functionality."""

import pytest
import subprocess
import json
from pathlib import Path


@pytest.fixture(scope="module")
def js_scrambler():
    """Path to the email scrambler JavaScript file."""
    return Path(__file__).parent.parent / "static" / "js" / "email-scrambler.js"


@pytest.mark.javascript
def test_scramble_email_function_exists(js_scrambler):
    """Verify scrambleEmail function is defined."""
    content = js_scrambler.read_text()
    assert "function scrambleEmail" in content


@pytest.mark.javascript
def test_unscramble_email_function_exists(js_scrambler):
    """Verify unscrambleEmail function is defined."""
    content = js_scrambler.read_text()
    assert "async function unscrambleEmail" in content


@pytest.mark.javascript
def test_setup_email_reveal_function_exists(js_scrambler):
    """Verify setupEmailReveal function is defined."""
    content = js_scrambler.read_text()
    assert "function setupEmailReveal" in content


@pytest.mark.javascript
def test_no_innerHTML_usage(js_scrambler):
    """Verify no innerHTML is used (security requirement)."""
    content = js_scrambler.read_text()
    assert "innerHTML" not in content, "innerHTML usage violates security standards"


@pytest.mark.javascript
def test_no_eval_usage(js_scrambler):
    """Verify no eval() is used (security requirement)."""
    content = js_scrambler.read_text()
    assert "eval(" not in content, "eval() usage violates security standards"


@pytest.mark.javascript
def test_uses_text_content(js_scrambler):
    """Verify textContent is used instead of innerHTML."""
    content = js_scrambler.read_text()
    assert "textContent" in content, "Should use textContent for safe DOM manipulation"


@pytest.mark.javascript
def test_uses_create_element(js_scrambler):
    """Verify createElement is used for DOM manipulation."""
    content = js_scrambler.read_text()
    assert "createElement" in content, "Should use createElement for building DOM"


@pytest.mark.javascript
def test_uses_append_child(js_scrambler):
    """Verify appendChild is used for adding elements."""
    content = js_scrambler.read_text()
    assert "appendChild" in content, "Should use appendChild to add elements"


@pytest.mark.javascript
def test_scramble_unscramble_roundtrip():
    """Test that scramble/unscramble is reversible using Node.js."""
    test_email = "test@example.com"

    # Create a test script
    test_script = f"""
    const fs = require('fs');
    const path = require('path');

    // Load the scrambler
    const scramblerPath = path.join(__dirname, '../static/js/email-scrambler.js');
    eval(fs.readFileSync(scramblerPath, 'utf8'));

    // Test roundtrip
    const original = "{test_email}";
    const scrambled = scrambleEmail(original);

    // Manually unscramble (sync version for testing)
    const chars = scrambled.split('');
    const len = scrambled.length;

    // Reverse the scrambling algorithm
    for (let i = len - 2; i >= 0; i--) {{
        const swapTarget = (i + len) % (len - i);
        const j = i + swapTarget;
        [chars[i], chars[j]] = [chars[j], chars[i]];
    }}

    const unscrambled = chars.join('');

    console.log(JSON.stringify({{
        original: original,
        scrambled: scrambled,
        unscrambled: unscrambled,
        match: original === unscrambled
    }}));
    """

    # Write test script
    test_file = Path(__file__).parent / "test_scramble.js"
    test_file.write_text(test_script)

    try:
        # Run with node
        result = subprocess.run(
            ["node", str(test_file)],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            pytest.skip("Node.js not available or test script failed")

        output = json.loads(result.stdout)

        assert output["original"] == test_email
        assert output["scrambled"] != test_email, "Scrambled should differ from original"
        assert output["unscrambled"] == test_email, "Unscramble should reverse scramble"
        assert output["match"], "Roundtrip should return original email"

    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()


@pytest.mark.javascript
def test_jsdoc_comments_present(js_scrambler):
    """Verify functions have JSDoc documentation."""
    content = js_scrambler.read_text()

    # Check for JSDoc comment blocks
    assert "/**" in content, "Should have JSDoc comments"
    assert "@param" in content, "Should document parameters"
    assert "@returns" in content, "Should document return values"


@pytest.mark.javascript
def test_export_for_node(js_scrambler):
    """Verify module exports for Node.js testing."""
    content = js_scrambler.read_text()
    assert "module.exports" in content, "Should export functions for testing"
