"""Checks for the published computational-neuroscience write-up."""

from pathlib import Path

from bs4 import BeautifulSoup


WRITEUP = Path(__file__).parent.parent / "static" / "cns" / "set1-writeup.html"


def parse_writeup():
    return BeautifulSoup(WRITEUP.read_text(), "lxml")


def test_cns_figures_have_text_alternatives():
    """Every generated plot communicates its purpose without sight."""
    images = parse_writeup().find_all("img")

    assert images
    assert all(image.get("alt", "").strip() for image in images)
