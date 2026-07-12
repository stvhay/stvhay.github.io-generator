"""Run htmltest as part of the pytest suite.

htmltest is configured for internal links and HTML structure only
(CheckExternal: false in .htmltest.yml), so it is fast, offline, and
runs in the default suite. External links are checked separately by
lychee on a schedule (.github/workflows/external-links.yml).
"""

import subprocess

import pytest


@pytest.mark.html5
def test_htmltest_passes(public_dir):
    """Validate the generated site's internal links and structure."""
    if not public_dir.exists():
        pytest.fail(
            f"Public directory not found at {public_dir}. "
            "Run './build' before running tests."
        )

    project_root = public_dir.parent

    try:
        result = subprocess.run(
            ["htmltest"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        pytest.fail("htmltest timed out after 180 seconds")
    except FileNotFoundError:
        pytest.fail(
            "htmltest command not found. "
            "Make sure you're running tests inside 'nix develop'."
        )

    if result.returncode != 0:
        output = result.stdout + result.stderr
        pytest.fail(
            f"htmltest found errors:\n\n{output}\n\n"
            "Fix the HTML validation errors above."
        )
