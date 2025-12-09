"""Tests for HTML meta tags (Open Graph, Twitter Cards, canonical URLs)."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from conftest import is_static_file, parse_html


@pytest.mark.meta
class TestCanonicalURLs:
    """Tests for canonical URL meta tags."""

    def test_all_pages_have_canonical_url(self, html_files, public_dir):
        """Verify that all HTML pages have a canonical URL."""
        missing_canonical = []

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            soup = parse_html(html_file)
            canonical = soup.find("link", {"rel": "canonical"})

            if not canonical or not canonical.get("href"):
                missing_canonical.append(html_file.relative_to(html_file.parent.parent))

        assert not missing_canonical, (
            f"The following pages are missing canonical URLs:\n"
            f"{chr(10).join(str(p) for p in missing_canonical)}"
        )

    def test_canonical_urls_are_absolute(self, html_files):
        """Verify that canonical URLs are absolute (not relative)."""
        invalid_canonical = []

        for html_file in html_files:
            soup = parse_html(html_file)
            canonical = soup.find("link", {"rel": "canonical"})

            if canonical and canonical.get("href"):
                href = canonical["href"]
                if not href.startswith("http://") and not href.startswith("https://"):
                    invalid_canonical.append(
                        (html_file.relative_to(html_file.parent.parent), href)
                    )

        assert not invalid_canonical, (
            f"The following pages have relative canonical URLs:\n"
            f"{chr(10).join(f'{p}: {url}' for p, url in invalid_canonical)}"
        )


@pytest.mark.meta
class TestOpenGraphTags:
    """Tests for Open Graph meta tags."""

    REQUIRED_OG_TAGS = ["og:title", "og:description", "og:type", "og:url"]

    def test_all_pages_have_required_og_tags(self, html_files, public_dir):
        """Verify that all pages have required Open Graph tags."""
        pages_missing_tags = {}

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            soup = parse_html(html_file)
            missing_tags = []

            for tag in self.REQUIRED_OG_TAGS:
                og_tag = soup.find("meta", {"property": tag})
                if not og_tag or not og_tag.get("content"):
                    missing_tags.append(tag)

            if missing_tags:
                pages_missing_tags[
                    html_file.relative_to(html_file.parent.parent)
                ] = missing_tags

        assert not pages_missing_tags, (
            f"The following pages are missing Open Graph tags:\n"
            f"{chr(10).join(f'{p}: {tags}' for p, tags in pages_missing_tags.items())}"
        )

    def test_og_type_is_valid(self, html_files):
        """Verify that og:type values are valid."""
        valid_types = ["website", "article", "profile", "book", "video.movie", "video.episode"]
        invalid_types = []

        for html_file in html_files:
            soup = parse_html(html_file)
            og_type = soup.find("meta", {"property": "og:type"})

            if og_type and og_type.get("content"):
                content = og_type["content"]
                if content not in valid_types:
                    invalid_types.append(
                        (html_file.relative_to(html_file.parent.parent), content)
                    )

        assert not invalid_types, (
            f"The following pages have invalid og:type values:\n"
            f"{chr(10).join(f'{p}: {t}' for p, t in invalid_types)}"
        )


@pytest.mark.meta
class TestTwitterCardTags:
    """Tests for Twitter Card meta tags."""

    REQUIRED_TWITTER_TAGS = ["twitter:card", "twitter:title", "twitter:description"]

    def test_all_pages_have_required_twitter_tags(self, html_files, public_dir):
        """Verify that all pages have required Twitter Card tags."""
        pages_missing_tags = {}

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            soup = parse_html(html_file)
            missing_tags = []

            for tag in self.REQUIRED_TWITTER_TAGS:
                twitter_tag = soup.find("meta", {"name": tag})
                if not twitter_tag or not twitter_tag.get("content"):
                    missing_tags.append(tag)

            if missing_tags:
                pages_missing_tags[
                    html_file.relative_to(html_file.parent.parent)
                ] = missing_tags

        assert not pages_missing_tags, (
            f"The following pages are missing Twitter Card tags:\n"
            f"{chr(10).join(f'{p}: {tags}' for p, tags in pages_missing_tags.items())}"
        )

    def test_twitter_card_type_is_valid(self, html_files):
        """Verify that twitter:card values are valid."""
        valid_cards = ["summary", "summary_large_image", "app", "player"]
        invalid_cards = []

        for html_file in html_files:
            soup = parse_html(html_file)
            twitter_card = soup.find("meta", {"name": "twitter:card"})

            if twitter_card and twitter_card.get("content"):
                content = twitter_card["content"]
                if content not in valid_cards:
                    invalid_cards.append(
                        (html_file.relative_to(html_file.parent.parent), content)
                    )

        assert not invalid_cards, (
            f"The following pages have invalid twitter:card values:\n"
            f"{chr(10).join(f'{p}: {c}' for p, c in invalid_cards)}"
        )


@pytest.mark.meta
class TestDescriptionTags:
    """Tests for page description meta tags."""

    def test_all_pages_have_description(self, html_files, public_dir):
        """Verify that all pages have a meta description tag."""
        missing_description = []

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            soup = parse_html(html_file)
            description = soup.find("meta", {"name": "description"})

            if not description or not description.get("content"):
                missing_description.append(
                    html_file.relative_to(html_file.parent.parent)
                )

        assert not missing_description, (
            f"The following pages are missing meta description:\n"
            f"{chr(10).join(str(p) for p in missing_description)}"
        )

    def test_descriptions_are_not_too_short(self, html_files):
        """Verify that meta descriptions are at least 50 characters."""
        short_descriptions = []
        min_length = 50

        for html_file in html_files:
            soup = parse_html(html_file)
            description = soup.find("meta", {"name": "description"})

            if description and description.get("content"):
                content = description["content"].strip()
                if len(content) < min_length:
                    short_descriptions.append(
                        (html_file.relative_to(html_file.parent.parent), len(content))
                    )

        assert not short_descriptions, (
            f"The following pages have descriptions shorter than {min_length} chars:\n"
            f"{chr(10).join(f'{p}: {length} chars' for p, length in short_descriptions)}"
        )

    def test_descriptions_are_not_too_long(self, html_files):
        """Verify that meta descriptions are not longer than 160 characters."""
        long_descriptions = []
        max_length = 160

        for html_file in html_files:
            soup = parse_html(html_file)
            description = soup.find("meta", {"name": "description"})

            if description and description.get("content"):
                content = description["content"].strip()
                if len(content) > max_length:
                    long_descriptions.append(
                        (html_file.relative_to(html_file.parent.parent), len(content))
                    )

        assert not long_descriptions, (
            f"The following pages have descriptions longer than {max_length} chars:\n"
            f"{chr(10).join(f'{p}: {length} chars' for p, length in long_descriptions)}"
        )
