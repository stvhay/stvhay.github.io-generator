"""Tests for Hugo-generated responsive page images."""

import pytest

from conftest import is_static_file, parse_html


@pytest.mark.performance
def test_content_images_have_responsive_sources(html_files, public_dir):
    """Every authored content image offers build-time generated WebP sizes."""
    images_without_sources = []

    for html_file in html_files:
        if is_static_file(html_file, public_dir):
            continue

        for image in parse_html(html_file).find_all("img"):
            srcset = image.get("srcset", "")
            sizes = image.get("sizes")
            if not srcset or not sizes or ".webp " not in srcset:
                images_without_sources.append(html_file.relative_to(public_dir))

    assert not images_without_sources, (
        "Content images missing responsive WebP sources:\n"
        + "\n".join(str(path) for path in images_without_sources)
    )


@pytest.mark.performance
def test_card_and_article_images_declare_distinct_slot_sizes(public_dir):
    """Responsive hints match the card and article layouts."""
    portfolio = parse_html(public_dir / "portfolio" / "index.html")
    article = parse_html(
        public_dir
        / "writing"
        / "computational-neuroscience-meets-the-17th-century"
        / "index.html"
    )

    assert portfolio.select_one(".post-img img")["sizes"].endswith("150px")
    assert article.select_one(".article-img img")["sizes"].endswith("400px")


@pytest.mark.accessibility
def test_image_alt_text_matches_context(public_dir):
    """Repeated card art is decorative; meaningful article art is described."""
    portfolio = parse_html(public_dir / "portfolio" / "index.html")
    article = parse_html(
        public_dir
        / "writing"
        / "computational-neuroscience-meets-the-17th-century"
        / "index.html"
    )

    assert all(image["alt"] == "" for image in portfolio.select(".post-img img"))
    assert article.select_one(".article-img img")["alt"] == (
        "Portrait of George Berkeley seated in clerical dress."
    )
