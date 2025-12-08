"""Shared pytest fixtures for Hugo static site tests."""

import json
from pathlib import Path
from typing import Iterator

import pytest


@pytest.fixture(scope="session")
def public_dir() -> Path:
    """Return the path to the Hugo public directory."""
    return Path(__file__).parent.parent / "public"


@pytest.fixture(scope="session")
def html_files(public_dir: Path) -> list[Path]:
    """Return all HTML files in the public directory."""
    if not public_dir.exists():
        pytest.fail(
            f"Public directory not found at {public_dir}. "
            "Run './build' before running tests."
        )
    return list(public_dir.rglob("*.html"))


@pytest.fixture
def html_file(request) -> Iterator[Path]:
    """Parametrized fixture that yields each HTML file."""
    return request.param


def parse_html_file(file_path: Path) -> str:
    """Read and return HTML file contents."""
    return file_path.read_text(encoding="utf-8")
