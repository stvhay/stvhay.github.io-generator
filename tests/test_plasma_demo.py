"""Checks for the standalone Plasma demo."""

import re
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).parent.parent
HTML = ROOT / "static" / "plasma" / "plasma.html"
CSS = ROOT / "static" / "plasma" / "plasma.css"
SCRIPT = ROOT / "static" / "plasma" / "plasma.js"


def parse_demo():
    return BeautifulSoup(HTML.read_text(), "lxml")


def test_plasma_declares_mobile_viewport():
    """Mobile browsers render the demo at the device width."""
    viewport = parse_demo().find("meta", attrs={"name": "viewport"})

    assert viewport
    assert "width=device-width" in viewport["content"]


def test_plasma_canvas_has_text_alternative():
    """The animated canvas communicates its content without sight."""
    canvas = parse_demo().find("canvas", id="plasma")

    assert canvas
    assert canvas.get("role") == "img"
    assert canvas.get("aria-label", "").strip()
    assert canvas.get_text(strip=True)


def test_plasma_canvas_remains_fluid_after_load():
    """CSS, rather than fixed inline pixels, controls the canvas size."""
    css = CSS.read_text()
    script = SCRIPT.read_text()
    container = re.search(r"\.canvas-container\s*\{([^}]+)\}", css)
    canvas = re.search(r"\.canvas-container canvas\s*\{([^}]+)\}", css)

    assert container and canvas
    assert "max-width: 80ch" in container.group(1)
    assert "width: calc(100% - 2rem)" in container.group(1)
    assert "width: 100%" in canvas.group(1)
    assert "aspect-ratio: 2 / 1" in canvas.group(1)
    assert "canvas.style.width" not in script
    assert "canvas.style.height" not in script
