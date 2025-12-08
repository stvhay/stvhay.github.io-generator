"""Tests for HTML5 validation using the Nu Html Checker."""

import subprocess
from pathlib import Path

import pytest


@pytest.mark.html5
class TestHTML5Validation:
    """Tests for HTML5 validation."""

    def test_all_html_files_are_valid_html5(self, public_dir):
        """Verify that all HTML files pass HTML5 validation."""
        # Run html5validator on the public directory
        # --root specifies the directory to validate
        # --show-warnings shows warnings in addition to errors
        # --match specifies the file pattern to validate
        result = subprocess.run(
            [
                "html5validator",
                "--root",
                str(public_dir),
                "--match",
                "*.html",
                "--blacklist",
                "categories",
                "tags",
            ],
            capture_output=True,
            text=True,
        )

        # html5validator returns:
        # 0 if no errors
        # 1 if errors found
        assert result.returncode == 0, (
            f"HTML5 validation errors found:\n{result.stdout}\n{result.stderr}"
        )

    def test_homepage_is_valid_html5(self, public_dir):
        """Verify that the homepage passes HTML5 validation."""
        index_file = public_dir / "index.html"
        if not index_file.exists():
            pytest.fail("Homepage (index.html) not found")

        result = subprocess.run(
            ["html5validator", "--root", str(public_dir), "--match", "index.html"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"Homepage HTML5 validation errors:\n{result.stdout}\n{result.stderr}"
        )


@pytest.mark.html5
class TestHTMLStructure:
    """Tests for basic HTML structure requirements."""

    def test_all_pages_have_doctype(self, html_files):
        """Verify that all HTML pages have a DOCTYPE declaration."""
        from bs4 import BeautifulSoup

        missing_doctype = []

        for html_file in html_files:
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
                soup = BeautifulSoup(content, "lxml")

                # Check if the file starts with DOCTYPE
                if not content.strip().upper().startswith("<!DOCTYPE"):
                    missing_doctype.append(html_file.relative_to(html_file.parent.parent))

        assert not missing_doctype, (
            f"The following pages are missing DOCTYPE:\n"
            f"{chr(10).join(str(p) for p in missing_doctype)}"
        )

    def test_all_pages_have_html_tag(self, html_files):
        """Verify that all HTML pages have an <html> tag."""
        from bs4 import BeautifulSoup

        missing_html_tag = []

        for html_file in html_files:
            soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "lxml")
            if not soup.html:
                missing_html_tag.append(html_file.relative_to(html_file.parent.parent))

        assert not missing_html_tag, (
            f"The following pages are missing <html> tag:\n"
            f"{chr(10).join(str(p) for p in missing_html_tag)}"
        )

    def test_all_pages_have_head_tag(self, html_files):
        """Verify that all HTML pages have a <head> tag."""
        from bs4 import BeautifulSoup

        missing_head_tag = []

        for html_file in html_files:
            soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "lxml")
            if not soup.head:
                missing_head_tag.append(html_file.relative_to(html_file.parent.parent))

        assert not missing_head_tag, (
            f"The following pages are missing <head> tag:\n"
            f"{chr(10).join(str(p) for p in missing_head_tag)}"
        )

    def test_all_pages_have_body_tag(self, html_files):
        """Verify that all HTML pages have a <body> tag."""
        from bs4 import BeautifulSoup

        missing_body_tag = []

        for html_file in html_files:
            soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "lxml")
            if not soup.body:
                missing_body_tag.append(html_file.relative_to(html_file.parent.parent))

        assert not missing_body_tag, (
            f"The following pages are missing <body> tag:\n"
            f"{chr(10).join(str(p) for p in missing_body_tag)}"
        )

    def test_all_pages_have_title_tag(self, html_files):
        """Verify that all HTML pages have a <title> tag."""
        from bs4 import BeautifulSoup

        missing_title_tag = []

        for html_file in html_files:
            soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "lxml")
            if not soup.title or not soup.title.string:
                missing_title_tag.append(html_file.relative_to(html_file.parent.parent))

        assert not missing_title_tag, (
            f"The following pages are missing <title> tag or have empty title:\n"
            f"{chr(10).join(str(p) for p in missing_title_tag)}"
        )

    def test_all_pages_have_lang_attribute(self, html_files):
        """Verify that all HTML pages have a lang attribute on the <html> tag."""
        from bs4 import BeautifulSoup

        missing_lang_attr = []

        for html_file in html_files:
            soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "lxml")
            if soup.html and not soup.html.get("lang"):
                missing_lang_attr.append(html_file.relative_to(html_file.parent.parent))

        assert not missing_lang_attr, (
            f"The following pages are missing lang attribute on <html> tag:\n"
            f"{chr(10).join(str(p) for p in missing_lang_attr)}"
        )

    def test_all_pages_have_charset_declaration(self, html_files):
        """Verify that all HTML pages have a charset declaration."""
        from bs4 import BeautifulSoup

        missing_charset = []

        for html_file in html_files:
            soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "lxml")
            charset_meta = soup.find("meta", {"charset": True}) or soup.find(
                "meta", {"http-equiv": "Content-Type"}
            )

            if not charset_meta:
                missing_charset.append(html_file.relative_to(html_file.parent.parent))

        assert not missing_charset, (
            f"The following pages are missing charset declaration:\n"
            f"{chr(10).join(str(p) for p in missing_charset)}"
        )
