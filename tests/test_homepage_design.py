"""Regression tests for the generated homepage design."""

from pathlib import Path

from conftest import parse_html


def test_homepage_uses_factual_positioning_heading(public_dir):
    homepage = parse_html(public_dir / "index.html")

    assert homepage.h1.get_text(" ", strip=True) == "Engineer learning neuroscience"


def test_homepage_labels_portfolio_and_uses_logical_card_headings(public_dir):
    homepage = parse_html(public_dir / "index.html")
    portfolio = homepage.find("section", id="portfolio")

    assert portfolio["aria-labelledby"] == "portfolio-heading"
    assert portfolio.find("h2", id="portfolio-heading").get_text(strip=True) == "Portfolio"
    assert len(portfolio.find_all("h3")) == 9
    assert not portfolio.find_all("h2")[1:]


def test_cv_link_discloses_pdf_and_new_tab_behavior(public_dir):
    homepage = parse_html(public_dir / "index.html")
    cv_link = homepage.find("nav").find("a", href="/docs/cv/cv-steve-hay.pdf")

    assert cv_link.get_text(" ", strip=True) == "CV (PDF, opens in a new tab)"
    assert cv_link.find("span", class_="sr-only") is not None


def test_homepage_features_only_the_first_editorially_weighted_project(public_dir):
    homepage = parse_html(public_dir / "index.html")
    portfolio = homepage.find("section", id="portfolio")
    cards = portfolio.select("article.post.card")
    featured = portfolio.select("article.featured-project")

    assert len(cards) == 9
    assert len(featured) == 1
    assert featured[0] == cards[0]
    assert featured[0].find(class_="featured-label").get_text(strip=True) == "Featured project"
    assert "Using Augmented Reality" in featured[0].find(class_="post-title").get_text()
    assert featured[0].find("source")["sizes"].endswith(", 240px")
    assert cards[1].find("source")["sizes"].endswith(", 150px")


def test_featured_project_has_larger_desktop_scale():
    css = Path("assets/css/main.css").read_text()

    assert ".featured-project" in css
    assert "grid-template-columns: 240px 1fr" in css
    assert ".featured-project .post-title" in css


def test_home_intro_uses_documented_prose_measure(public_dir):
    homepage = parse_html(public_dir / "index.html")
    css = Path("assets/css/main.css").read_text()

    assert "home-intro" in homepage.find("section", id="home").get("class", [])
    assert ".home-intro" in css
    assert "max-width: 45rem" in css.split(".home-intro", 1)[1].split("}", 1)[0]


def test_card_lists_omit_redundant_section_marks(public_dir):
    pages = [
        public_dir / "index.html",
        public_dir / "portfolio" / "index.html",
        public_dir / "writing" / "index.html",
    ]

    assert all(not parse_html(page).select(".section-mark") for page in pages)
