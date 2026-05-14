"""Run htmltest as part of the pytest suite.

Marked ``external`` because htmltest validates external links and is
network-dependent. Local fast iteration uses ``htmltest --skip-external``
directly from the shell; pytest is the canonical entry point for the
full check (CI, pre-publish verification).
"""

import subprocess

import pytest


@pytest.mark.html5
@pytest.mark.external
def test_htmltest_passes(public_dir):
    """Validate the generated site with htmltest, including external links."""
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
