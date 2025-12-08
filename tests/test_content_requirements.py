"""Tests for content requirements (frontmatter, descriptions, etc.)."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from conftest import is_static_file


def parse_html(file_path: Path) -> BeautifulSoup:
    """Parse an HTML file and return a BeautifulSoup object."""
    with open(file_path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "lxml")


@pytest.mark.content
class TestPageDescriptions:
    """Tests for page description requirements."""

    def test_all_content_pages_have_descriptions(self, public_dir):
        """Verify that all content pages have descriptions in meta tags."""
        # Get all HTML files except category/tag index pages and static files
        html_files = []
        for html_file in public_dir.rglob("*.html"):
            # Skip Hugo-generated taxonomy pages
            if "categories" in html_file.parts or "tags" in html_file.parts:
                continue
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue
            html_files.append(html_file)

        missing_descriptions = []

        for html_file in html_files:
            soup = parse_html(html_file)
            description = soup.find("meta", {"name": "description"})

            if not description or not description.get("content"):
                missing_descriptions.append(html_file.relative_to(public_dir))

        assert not missing_descriptions, (
            f"The following pages are missing descriptions:\n"
            f"{chr(10).join(str(p) for p in missing_descriptions)}"
        )


@pytest.mark.content
class TestPageTitles:
    """Tests for page title requirements."""

    def test_all_pages_have_unique_titles(self, html_files):
        """Verify that all pages have unique titles."""
        titles_to_pages = {}

        for html_file in html_files:
            soup = parse_html(html_file)
            title_tag = soup.find("title")

            if title_tag and title_tag.string:
                title = title_tag.string.strip()
                if title not in titles_to_pages:
                    titles_to_pages[title] = []
                titles_to_pages[title].append(
                    html_file.relative_to(html_file.parent.parent)
                )

        duplicate_titles = {
            title: pages for title, pages in titles_to_pages.items() if len(pages) > 1
        }

        assert not duplicate_titles, (
            f"The following titles are used on multiple pages:\n"
            + "\n".join(
                f"  '{title}':\n    - " + "\n    - ".join(str(p) for p in pages)
                for title, pages in duplicate_titles.items()
            )
        )

    def test_titles_are_descriptive(self, html_files, public_dir):
        """Verify that page titles are not too short or generic."""
        MIN_TITLE_LENGTH = 10
        GENERIC_TITLES = ["Untitled", "New Page", "Page", "Home"]

        short_or_generic_titles = []

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            soup = parse_html(html_file)
            title_tag = soup.find("title")

            if title_tag and title_tag.string:
                title = title_tag.string.strip()

                if len(title) < MIN_TITLE_LENGTH:
                    short_or_generic_titles.append(
                        (html_file.relative_to(html_file.parent.parent), title, "too short")
                    )
                elif any(generic in title for generic in GENERIC_TITLES):
                    short_or_generic_titles.append(
                        (html_file.relative_to(html_file.parent.parent), title, "generic")
                    )

        assert not short_or_generic_titles, (
            f"The following pages have short or generic titles:\n"
            f"{chr(10).join(f'{p}: \"{t}\" ({reason})' for p, t, reason in short_or_generic_titles)}"
        )


@pytest.mark.content
class TestHeadingHierarchy:
    """Tests for heading hierarchy and structure."""

    def test_all_pages_have_h1(self, html_files):
        """Verify that all pages have exactly one H1 heading."""
        pages_without_h1 = []
        pages_with_multiple_h1 = []

        for html_file in html_files:
            soup = parse_html(html_file)
            h1_tags = soup.find_all("h1")

            if not h1_tags:
                pages_without_h1.append(html_file.relative_to(html_file.parent.parent))
            elif len(h1_tags) > 1:
                pages_with_multiple_h1.append(
                    (html_file.relative_to(html_file.parent.parent), len(h1_tags))
                )

        errors = []
        if pages_without_h1:
            errors.append(
                f"Pages without H1:\n  "
                + "\n  ".join(str(p) for p in pages_without_h1)
            )
        if pages_with_multiple_h1:
            errors.append(
                f"Pages with multiple H1s:\n  "
                + "\n  ".join(f"{p} ({count} H1s)" for p, count in pages_with_multiple_h1)
            )

        assert not errors, "\n\n".join(errors)

    def test_heading_hierarchy_is_logical(self, html_files):
        """Verify that heading levels don't skip (e.g., H1 to H3 without H2)."""
        pages_with_skipped_headings = []

        for html_file in html_files:
            soup = parse_html(html_file)
            headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

            if not headings:
                continue

            heading_levels = [int(h.name[1]) for h in headings]

            # Check for skipped levels
            for i in range(len(heading_levels) - 1):
                current_level = heading_levels[i]
                next_level = heading_levels[i + 1]

                # If next level is more than one level deeper, that's a skip
                if next_level > current_level + 1:
                    pages_with_skipped_headings.append(
                        (
                            html_file.relative_to(html_file.parent.parent),
                            f"H{current_level} to H{next_level}",
                        )
                    )
                    break  # Only report first skip per page

        assert not pages_with_skipped_headings, (
            f"The following pages skip heading levels:\n"
            f"{chr(10).join(f'{p}: {skip}' for p, skip in pages_with_skipped_headings)}"
        )


@pytest.mark.content
class TestContentQuality:
    """Tests for basic content quality."""

    def test_no_lorem_ipsum_in_content(self, html_files):
        """Verify that no pages contain placeholder Lorem Ipsum text."""
        LOREM_INDICATORS = ["lorem ipsum", "dolor sit amet", "consectetur adipiscing"]

        pages_with_lorem = []

        for html_file in html_files:
            soup = parse_html(html_file)
            body_text = soup.get_text().lower()

            if any(indicator in body_text for indicator in LOREM_INDICATORS):
                pages_with_lorem.append(html_file.relative_to(html_file.parent.parent))

        assert not pages_with_lorem, (
            f"The following pages contain Lorem Ipsum placeholder text:\n"
            f"{chr(10).join(str(p) for p in pages_with_lorem)}"
        )

    def test_pages_have_sufficient_content(self, html_files, public_dir):
        """Verify that pages have a reasonable amount of content."""
        MIN_CONTENT_LENGTH = 100  # Minimum characters in body text

        pages_with_little_content = []

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            # Skip Hugo-generated taxonomy pages (minimal by design)
            if "categories" in html_file.parts or "tags" in html_file.parts:
                continue

            soup = parse_html(html_file)

            # Get main content area if possible, otherwise use body
            main_content = soup.find("main") or soup.find("article") or soup.body

            if main_content:
                # Get text content, stripping whitespace
                text = " ".join(main_content.get_text().split())

                if len(text) < MIN_CONTENT_LENGTH:
                    pages_with_little_content.append(
                        (html_file.relative_to(html_file.parent.parent), len(text))
                    )

        assert not pages_with_little_content, (
            f"The following pages have less than {MIN_CONTENT_LENGTH} characters:\n"
            f"{chr(10).join(f'{p}: {length} chars' for p, length in pages_with_little_content)}"
        )
