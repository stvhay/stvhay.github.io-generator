"""Shared pytest fixtures for Hugo static site tests."""

import json
from pathlib import Path
from typing import Iterator

import pytest
from bs4 import BeautifulSoup


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


def parse_html(file_path: Path) -> BeautifulSoup:
    """Parse an HTML file and return a BeautifulSoup object."""
    with open(file_path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "lxml")


def is_static_file(file_path: Path, public_dir: Path) -> bool:
    """
    Check if a file originated from static/ directory.

    These files are copied as-is by Hugo and are typically interactive
    demos or tools that don't need full SEO/content requirements.
    """
    try:
        rel_path = file_path.relative_to(public_dir)
        static_paths = ['s3m/', 'plasma/', 'cns/']
        return any(str(rel_path).startswith(p) for p in static_paths)
    except ValueError:
        return False
