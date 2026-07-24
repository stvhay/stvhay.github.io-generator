"""Semantic baseline for audited standalone pages."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


ROOT = Path(__file__).parent.parent
PAGES = [
    ROOT / "static" / "plasma" / "plasma.html",
    ROOT / "static" / "s3m" / "it.html",
]


@pytest.mark.parametrize("page", PAGES, ids=lambda page: page.parent.name)
def test_standalone_page_declares_direction_and_main_landmark(page):
    """Standalone English pages expose direction and primary content."""
    soup = BeautifulSoup(page.read_text(), "lxml")

    assert soup.html.get("lang") == "en"
    assert soup.html.get("dir") == "ltr"
    assert len(soup.find_all("main")) == 1
