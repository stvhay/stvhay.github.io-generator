"""Tests for JSON-LD structured data validation."""

import json
from pathlib import Path

import pytest
from bs4 import BeautifulSoup


def parse_html(file_path: Path) -> BeautifulSoup:
    """Parse an HTML file and return a BeautifulSoup object."""
    with open(file_path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "lxml")


def extract_json_ld(soup: BeautifulSoup) -> list[dict]:
    """Extract all JSON-LD structured data from a page."""
    json_ld_scripts = soup.find_all("script", {"type": "application/ld+json"})
    json_ld_data = []

    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            json_ld_data.append(data)
        except json.JSONDecodeError as e:
            # We'll catch invalid JSON in a separate test
            json_ld_data.append({"_error": str(e), "_content": script.string})

    return json_ld_data


@pytest.mark.structured_data
class TestJSONLDPresence:
    """Tests for JSON-LD structured data presence."""

    def test_homepage_has_website_schema(self, public_dir):
        """Verify that the homepage has WebSite schema."""
        index_file = public_dir / "index.html"
        assert index_file.exists(), "Homepage (index.html) not found"

        soup = parse_html(index_file)
        json_ld_data = extract_json_ld(soup)

        website_schemas = [
            data for data in json_ld_data if data.get("@type") == "WebSite"
        ]

        assert website_schemas, "Homepage is missing WebSite schema"
        assert len(website_schemas) == 1, "Homepage should have exactly one WebSite schema"

    def test_blog_posts_have_article_schema(self, public_dir):
        """Verify that blog posts have Article schema."""
        # Look for blog posts in writing/ directory
        writing_dir = public_dir / "writing"
        if not writing_dir.exists():
            pytest.skip("No writing directory found")

        blog_posts = []
        for html_file in writing_dir.rglob("*.html"):
            # Skip index pages
            if html_file.name == "index.html":
                continue
            blog_posts.append(html_file)

        if not blog_posts:
            pytest.skip("No blog posts found")

        missing_article_schema = []

        for post in blog_posts:
            soup = parse_html(post)
            json_ld_data = extract_json_ld(soup)

            article_schemas = [
                data for data in json_ld_data if data.get("@type") == "Article"
            ]

            if not article_schemas:
                missing_article_schema.append(post.relative_to(public_dir))

        assert not missing_article_schema, (
            f"The following blog posts are missing Article schema:\n"
            f"{chr(10).join(str(p) for p in missing_article_schema)}"
        )


@pytest.mark.structured_data
class TestJSONLDValidity:
    """Tests for JSON-LD structured data validity."""

    def test_all_json_ld_is_valid_json(self, html_files):
        """Verify that all JSON-LD blocks contain valid JSON."""
        invalid_json = []

        for html_file in html_files:
            soup = parse_html(html_file)
            json_ld_scripts = soup.find_all("script", {"type": "application/ld+json"})

            for script in json_ld_scripts:
                try:
                    json.loads(script.string)
                except json.JSONDecodeError as e:
                    invalid_json.append(
                        (html_file.relative_to(html_file.parent.parent), str(e))
                    )

        assert not invalid_json, (
            f"The following pages have invalid JSON-LD:\n"
            f"{chr(10).join(f'{p}: {err}' for p, err in invalid_json)}"
        )

    def test_all_json_ld_has_context(self, html_files):
        """Verify that all JSON-LD blocks have @context."""
        missing_context = []

        for html_file in html_files:
            soup = parse_html(html_file)
            json_ld_data = extract_json_ld(soup)

            for data in json_ld_data:
                if "_error" in data:
                    continue  # Skip invalid JSON (caught by other test)

                if "@context" not in data:
                    missing_context.append(html_file.relative_to(html_file.parent.parent))
                    break

        assert not missing_context, (
            f"The following pages have JSON-LD without @context:\n"
            f"{chr(10).join(str(p) for p in missing_context)}"
        )

    def test_all_json_ld_has_type(self, html_files):
        """Verify that all JSON-LD blocks have @type."""
        missing_type = []

        for html_file in html_files:
            soup = parse_html(html_file)
            json_ld_data = extract_json_ld(soup)

            for data in json_ld_data:
                if "_error" in data:
                    continue  # Skip invalid JSON (caught by other test)

                if "@type" not in data:
                    missing_type.append(html_file.relative_to(html_file.parent.parent))
                    break

        assert not missing_type, (
            f"The following pages have JSON-LD without @type:\n"
            f"{chr(10).join(str(p) for p in missing_type)}"
        )


@pytest.mark.structured_data
class TestWebSiteSchema:
    """Tests for WebSite schema validation."""

    REQUIRED_WEBSITE_FIELDS = ["name", "url"]

    def test_website_schema_has_required_fields(self, public_dir):
        """Verify that WebSite schema has required fields."""
        index_file = public_dir / "index.html"
        if not index_file.exists():
            pytest.skip("Homepage not found")

        soup = parse_html(index_file)
        json_ld_data = extract_json_ld(soup)

        website_schemas = [
            data for data in json_ld_data if data.get("@type") == "WebSite"
        ]

        if not website_schemas:
            pytest.skip("No WebSite schema found")

        website_schema = website_schemas[0]
        missing_fields = [
            field for field in self.REQUIRED_WEBSITE_FIELDS if field not in website_schema
        ]

        assert not missing_fields, (
            f"WebSite schema is missing required fields: {missing_fields}"
        )


@pytest.mark.structured_data
class TestArticleSchema:
    """Tests for Article schema validation."""

    REQUIRED_ARTICLE_FIELDS = ["headline", "author"]
    RECOMMENDED_ARTICLE_FIELDS = ["datePublished", "description"]

    def test_article_schema_has_required_fields(self, public_dir):
        """Verify that Article schemas have required fields."""
        writing_dir = public_dir / "writing"
        if not writing_dir.exists():
            pytest.skip("No writing directory found")

        blog_posts = [
            f for f in writing_dir.rglob("*.html") if f.name != "index.html"
        ]

        if not blog_posts:
            pytest.skip("No blog posts found")

        missing_fields_by_post = {}

        for post in blog_posts:
            soup = parse_html(post)
            json_ld_data = extract_json_ld(soup)

            article_schemas = [
                data for data in json_ld_data if data.get("@type") == "Article"
            ]

            if not article_schemas:
                continue  # Caught by presence test

            article_schema = article_schemas[0]
            missing_fields = [
                field for field in self.REQUIRED_ARTICLE_FIELDS
                if field not in article_schema
            ]

            if missing_fields:
                missing_fields_by_post[post.relative_to(public_dir)] = missing_fields

        assert not missing_fields_by_post, (
            f"The following articles are missing required fields:\n"
            f"{chr(10).join(f'{p}: {fields}' for p, fields in missing_fields_by_post.items())}"
        )

    def test_article_schema_has_recommended_fields(self, public_dir):
        """Verify that Article schemas have recommended fields (warning only)."""
        writing_dir = public_dir / "writing"
        if not writing_dir.exists():
            pytest.skip("No writing directory found")

        blog_posts = [
            f for f in writing_dir.rglob("*.html") if f.name != "index.html"
        ]

        if not blog_posts:
            pytest.skip("No blog posts found")

        missing_fields_by_post = {}

        for post in blog_posts:
            soup = parse_html(post)
            json_ld_data = extract_json_ld(soup)

            article_schemas = [
                data for data in json_ld_data if data.get("@type") == "Article"
            ]

            if not article_schemas:
                continue

            article_schema = article_schemas[0]
            missing_fields = [
                field for field in self.RECOMMENDED_ARTICLE_FIELDS
                if field not in article_schema
            ]

            if missing_fields:
                missing_fields_by_post[post.relative_to(public_dir)] = missing_fields

        # This is a warning, not a failure - just report it
        if missing_fields_by_post:
            print(
                "\nWARNING: Some articles are missing recommended fields:\n"
                + "\n".join(
                    f"  {p}: {fields}"
                    for p, fields in missing_fields_by_post.items()
                )
            )
