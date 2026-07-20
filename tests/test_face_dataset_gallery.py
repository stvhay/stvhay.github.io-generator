"""Tests for the standalone face dataset gallery."""

import json
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
GALLERY_HTML = REPO_ROOT / "static" / "face-dataset" / "index.html"
GALLERY_MANIFEST = REPO_ROOT / "static" / "face-dataset" / "manifest.json"
EXPECTED_CATEGORY_COUNTS = {
    "canonical": 2,
    "transformations": 8,
    "profiles": 5,
    "male-multiview": 16,
    "female-multiview": 16,
    "reconstructions": 4,
}


def test_manifest_assigns_every_item_to_a_gallery_category():
    """Every published item belongs to one supported, non-empty category."""
    manifest = json.loads(GALLERY_MANIFEST.read_text(encoding="utf-8"))
    counts = Counter(item.get("category") for item in manifest["items"])

    assert counts == EXPECTED_CATEGORY_COUNTS


def test_gallery_builds_native_lazy_collapsible_groups():
    """Category previews use native disclosure controls and render cards on open."""
    source = GALLERY_HTML.read_text(encoding="utf-8")

    assert "document.createElement('details')" in source
    assert "document.createElement('summary')" in source
    assert "details.addEventListener('toggle'" in source
    assert "if (details.open && !rendered)" in source
    assert "category.summary" in source
    assert "category.method" in source
    assert "items.slice(0, 3)" in source
