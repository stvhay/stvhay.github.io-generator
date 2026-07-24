"""Regression tests for the generated homepage design."""

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
