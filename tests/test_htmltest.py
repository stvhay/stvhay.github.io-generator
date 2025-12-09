"""Tests that run htmltest as part of pytest suite."""

import subprocess
from pathlib import Path

import pytest


@pytest.mark.html5
def test_htmltest_passes(public_dir):
    """
    Run htmltest to validate all HTML links, images, and structure.

    This ensures:
    - All internal links work correctly
    - All internal hash anchors resolve
    - External links are valid (when CheckExternal is enabled)
    - All images have alt attributes
    - Scripts reference valid files
    - Favicon is present
    - Meta refresh tags have valid URLs
    """
    if not public_dir.exists():
        pytest.fail(
            f"Public directory not found at {public_dir}. "
            "Run './build' before running tests."
        )

    # Run htmltest from the project root
    project_root = public_dir.parent

    try:
        result = subprocess.run(
            ["htmltest"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # htmltest exits with 1 if there are errors
        if result.returncode != 0:
            # Include both stdout and stderr in failure message
            output = result.stdout + result.stderr
            pytest.fail(
                f"htmltest found errors:\n\n{output}\n\n"
                "Fix the HTML validation errors above."
            )

    except subprocess.TimeoutExpired:
        pytest.fail("htmltest timed out after 30 seconds")
    except FileNotFoundError:
        pytest.fail(
            "htmltest command not found. "
            "Make sure you're running tests inside 'nix develop'."
        )
