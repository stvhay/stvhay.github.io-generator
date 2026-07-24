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


def test_cns_figures_are_external_and_dimensioned():
    """Generated plots are cacheable files that reserve their layout space."""
    images = parse_writeup().find_all("img")

    for image in images:
        source = image["src"]
        assert not source.startswith("data:")
        assert (WRITEUP.parent / source).is_file()
        assert int(image["width"]) > 0
        assert int(image["height"]) > 0
        assert image["loading"] == "lazy"
        assert image["decoding"] == "async"
