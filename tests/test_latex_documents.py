"""Tests for LaTeX-generated documents (PDF and LaTeXML HTML output).

The build reads latex/latex.manifest ("<doc.tex> [formats]", formats pdf
and/or html, default pdf) and publishes each requested artifact under
public/docs/. HTML documents carry the SHA-384 hash of their .tex source
in a <meta name="texhash"> tag, link the shared LaTeXML stylesheets, and
are listed in the sitemap so crawlers can find them even though site
links intentionally point at the PDF versions.
"""

import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from conftest import parse_html

REPO_DIR = Path(__file__).parent.parent
MANIFEST = REPO_DIR / "latex" / "latex.manifest"
KNOWN_FORMATS = {"pdf", "html"}


def manifest_entries() -> list[tuple[str, set[str]]]:
    """Parse latex.manifest into (document path sans .tex, formats) pairs."""
    entries = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        formats = set(fields[1:]) or {"pdf"}
        entries.append((fields[0].removesuffix(".tex"), formats))
    return entries


def sha384_of(path: Path) -> str:
    return hashlib.sha384(path.read_bytes()).hexdigest()


def html_documents() -> list[str]:
    return [doc for doc, formats in manifest_entries() if "html" in formats]


@pytest.mark.content
class TestManifest:
    """Tests for the manifest itself."""

    def test_manifest_formats_are_known(self):
        """Every format token in the manifest is one the build understands."""
        for doc, formats in manifest_entries():
            unknown = formats - KNOWN_FORMATS
            assert not unknown, f"{doc}: unknown formats {unknown}"

    def test_manifest_sources_exist(self):
        """Every manifest entry points at an existing .tex source."""
        for doc, _ in manifest_entries():
            assert (REPO_DIR / "latex" / f"{doc}.tex").is_file(), (
                f"latex/{doc}.tex not found"
            )


@pytest.mark.content
class TestPublishedArtifacts:
    """Tests that the built site contains exactly the requested artifacts."""

    def test_requested_artifacts_published(self, public_dir):
        """Each document exists in public/docs in every requested format."""
        missing = []
        for doc, formats in manifest_entries():
            for fmt in formats:
                artifact = public_dir / "docs" / f"{doc}.{fmt}"
                if not artifact.is_file():
                    missing.append(str(artifact.relative_to(public_dir)))
        assert not missing, f"Missing artifacts: {missing}"

    def test_unrequested_artifacts_absent(self, public_dir):
        """Formats dropped from the manifest disappear from the site."""
        stale = []
        for doc, formats in manifest_entries():
            for fmt in KNOWN_FORMATS - formats:
                artifact = public_dir / "docs" / f"{doc}.{fmt}"
                if artifact.exists():
                    stale.append(str(artifact.relative_to(public_dir)))
        assert not stale, f"Stale artifacts for unrequested formats: {stale}"


@pytest.mark.content
class TestHtmlDocuments:
    """Tests for LaTeXML-generated HTML documents."""

    def test_texhash_matches_source(self, public_dir):
        """The embedded texhash matches the current .tex source, so the
        published HTML was generated from the committed source."""
        for doc in html_documents():
            soup = parse_html(public_dir / "docs" / f"{doc}.html")
            meta = soup.find("meta", {"name": "texhash"})
            assert meta, f"{doc}.html: missing texhash meta tag"
            assert meta["content"] == sha384_of(REPO_DIR / "latex" / f"{doc}.tex"), (
                f"{doc}.html: texhash does not match latex/{doc}.tex; "
                "rebuild with ./build"
            )

    def test_head_links_shared_resources(self, public_dir):
        """HTML documents link the favicon and the shared site-served
        stylesheets, and every linked resource exists in the built site."""
        for doc in html_documents():
            soup = parse_html(public_dir / "docs" / f"{doc}.html")
            icons = soup.find_all("link", rel="icon")
            assert icons, f"{doc}.html: missing favicon links"
            stylesheets = soup.find_all("link", rel="stylesheet")
            hrefs = [link["href"] for link in stylesheets]
            assert "/css/latexml/LaTeXML.css" in hrefs, (
                f"{doc}.html: missing shared LaTeXML stylesheet"
            )
            for href in hrefs + [icon["href"] for icon in icons]:
                assert (public_dir / href.lstrip("/")).is_file(), (
                    f"{doc}.html: linked resource {href} not in built site"
                )

    def test_documents_have_title_and_language(self, public_dir):
        """Basic accessibility: a non-empty <title> and an html lang."""
        for doc in html_documents():
            soup = parse_html(public_dir / "docs" / f"{doc}.html")
            assert soup.title and soup.title.get_text(strip=True), (
                f"{doc}.html: missing or empty <title>"
            )
            assert soup.html.get("lang"), f"{doc}.html: missing lang attribute"


@pytest.mark.content
class TestSitemap:
    """Tests for crawler discovery of generated HTML documents."""

    def test_sitemap_lists_html_documents(self, public_dir):
        """Every html-format document appears in sitemap.xml, since site
        links point at the PDFs and crawlers find the HTML via the sitemap."""
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        tree = ET.parse(public_dir / "sitemap.xml")
        locs = {el.text for el in tree.findall(".//sm:loc", ns)}
        for doc in html_documents():
            url = f"https://stevenhay.com/docs/{doc}.html"
            assert url in locs, f"sitemap.xml missing {url}"
