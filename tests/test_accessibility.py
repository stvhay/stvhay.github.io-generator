"""Tests for accessibility beyond alt text (which htmltest already checks)."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from conftest import is_static_file


def parse_html(file_path: Path) -> BeautifulSoup:
    """Parse an HTML file and return a BeautifulSoup object."""
    with open(file_path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "lxml")


@pytest.mark.accessibility
class TestARIALandmarks:
    """Tests for ARIA landmarks and semantic HTML."""

    def test_pages_have_main_landmark(self, html_files, public_dir):
        """Verify that pages have a main landmark."""
        pages_without_main = []

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            soup = parse_html(html_file)

            # Check for <main> tag or role="main"
            main_element = soup.find("main") or soup.find(attrs={"role": "main"})

            if not main_element:
                pages_without_main.append(html_file.relative_to(html_file.parent.parent))

        assert not pages_without_main, (
            f"The following pages are missing main landmark:\n"
            f"{chr(10).join(str(p) for p in pages_without_main)}"
        )

    def test_pages_have_navigation_landmark(self, html_files, public_dir):
        """Verify that pages have a navigation landmark."""
        pages_without_nav = []

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            soup = parse_html(html_file)

            # Check for <nav> tag or role="navigation"
            nav_element = soup.find("nav") or soup.find(attrs={"role": "navigation"})

            if not nav_element:
                pages_without_nav.append(html_file.relative_to(html_file.parent.parent))

        assert not pages_without_nav, (
            f"The following pages are missing navigation landmark:\n"
            f"{chr(10).join(str(p) for p in pages_without_nav)}"
        )


@pytest.mark.accessibility
class TestFormAccessibility:
    """Tests for form accessibility."""

    def test_all_form_inputs_have_labels(self, html_files, public_dir):
        """Verify that all form inputs have associated labels."""
        inputs_without_labels = []

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            soup = parse_html(html_file)
            inputs = soup.find_all(["input", "select", "textarea"])

            for input_elem in inputs:
                # Skip hidden inputs and buttons
                input_type = input_elem.get("type", "text")
                if input_type in ["hidden", "submit", "button", "reset"]:
                    continue

                input_id = input_elem.get("id")
                input_name = input_elem.get("name")

                # Check for label by 'for' attribute
                has_label = False
                if input_id:
                    label = soup.find("label", {"for": input_id})
                    if label:
                        has_label = True

                # Check for aria-label or aria-labelledby
                if not has_label:
                    if input_elem.get("aria-label") or input_elem.get("aria-labelledby"):
                        has_label = True

                # Check if input is wrapped in a label
                if not has_label:
                    parent = input_elem.find_parent("label")
                    if parent:
                        has_label = True

                if not has_label:
                    inputs_without_labels.append(
                        (
                            html_file.relative_to(html_file.parent.parent),
                            input_type,
                            input_id or input_name or "unnamed",
                        )
                    )

        assert not inputs_without_labels, (
            f"The following form inputs are missing labels:\n"
            f"{chr(10).join(f'{p}: {t} ({n})' for p, t, n in inputs_without_labels)}"
        )

    def test_form_buttons_have_accessible_names(self, html_files, public_dir):
        """Verify that all buttons have accessible names."""
        buttons_without_names = []

        for html_file in html_files:
            # Skip static files (interactive demos/tools)
            if is_static_file(html_file, public_dir):
                continue

            soup = parse_html(html_file)
            buttons = soup.find_all(["button", "input"])

            for button in buttons:
                # Only check button-type inputs
                if button.name == "input":
                    input_type = button.get("type", "text")
                    if input_type not in ["submit", "button", "reset"]:
                        continue

                # Check for text content, value, aria-label, or aria-labelledby
                has_name = False

                if button.get_text(strip=True):
                    has_name = True
                elif button.get("value"):
                    has_name = True
                elif button.get("aria-label") or button.get("aria-labelledby"):
                    has_name = True

                if not has_name:
                    buttons_without_names.append(
                        html_file.relative_to(html_file.parent.parent)
                    )
                    break  # Only report once per page

        assert not buttons_without_names, (
            f"The following pages have buttons without accessible names:\n"
            f"{chr(10).join(str(p) for p in buttons_without_names)}"
        )


@pytest.mark.accessibility
class TestLinkAccessibility:
    """Tests for link accessibility."""

    def test_links_have_descriptive_text(self, html_files):
        """Verify that links have descriptive text (not just 'click here')."""
        NON_DESCRIPTIVE_PHRASES = [
            "click here",
            "read more",
            "more",
            "link",
            "here",
        ]

        links_with_poor_text = []

        for html_file in html_files:
            soup = parse_html(html_file)
            links = soup.find_all("a")

            for link in links:
                link_text = link.get_text(strip=True).lower()
                aria_label = (link.get("aria-label") or "").lower()

                # Use aria-label if present, otherwise link text
                text_to_check = aria_label if aria_label else link_text

                if text_to_check in NON_DESCRIPTIVE_PHRASES:
                    links_with_poor_text.append(
                        (html_file.relative_to(html_file.parent.parent), text_to_check)
                    )

        assert not links_with_poor_text, (
            f"The following pages have non-descriptive link text:\n"
            f"{chr(10).join(f'{p}: \"{text}\"' for p, text in links_with_poor_text)}"
        )

    def test_links_to_external_sites_are_marked(self, html_files):
        """Verify that external links are marked (warning only)."""
        import urllib.parse

        unmarked_external_links = []

        for html_file in html_files:
            soup = parse_html(html_file)
            links = soup.find_all("a", href=True)

            for link in links:
                href = link["href"]

                # Skip internal links and anchors
                if href.startswith("/") or href.startswith("#") or href.startswith("mailto:"):
                    continue

                # Parse the URL
                try:
                    parsed = urllib.parse.urlparse(href)
                    if parsed.scheme in ["http", "https"]:
                        # This is an external link
                        # Check if it has target="_blank" or rel="external"
                        has_target_blank = link.get("target") == "_blank"
                        rel = link.get("rel", [])
                        if isinstance(rel, str):
                            rel = [rel]
                        has_external_rel = "external" in rel or "noopener" in rel

                        if not (has_target_blank or has_external_rel):
                            unmarked_external_links.append(
                                (html_file.relative_to(html_file.parent.parent), href)
                            )
                except Exception:
                    pass  # Skip malformed URLs

        # This is a warning, not a hard failure
        if unmarked_external_links:
            print(
                "\nWARNING: Some external links are not marked:\n"
                + "\n".join(
                    f"  {p}: {url}"
                    for p, url in unmarked_external_links[:10]  # Limit output
                )
            )


@pytest.mark.accessibility
class TestImageAccessibility:
    """Tests for image accessibility (beyond alt text)."""

    def test_decorative_images_have_empty_alt(self, html_files):
        """Verify that decorative images have empty alt attributes."""
        # This is more of a warning - we can't automatically determine
        # if an image is decorative, but we can check for patterns
        images_with_alt_decorative = []

        for html_file in html_files:
            soup = parse_html(html_file)
            images = soup.find_all("img")

            for img in images:
                alt = img.get("alt", "").lower()

                # If alt text is "decorative", "decoration", etc., it should be empty
                if alt in ["decorative", "decoration", "spacer", "divider"]:
                    images_with_alt_decorative.append(
                        (html_file.relative_to(html_file.parent.parent), alt)
                    )

        # This is a warning
        if images_with_alt_decorative:
            print(
                "\nWARNING: Some images have 'decorative' text in alt (should be empty):\n"
                + "\n".join(f"  {p}: alt=\"{alt}\"" for p, alt in images_with_alt_decorative)
            )


@pytest.mark.accessibility
class TestKeyboardNavigation:
    """Tests for keyboard navigation support."""

    def test_no_positive_tabindex(self, html_files):
        """Verify that no elements use positive tabindex values."""
        elements_with_positive_tabindex = []

        for html_file in html_files:
            soup = parse_html(html_file)
            elements = soup.find_all(attrs={"tabindex": True})

            for elem in elements:
                try:
                    tabindex = int(elem["tabindex"])
                    if tabindex > 0:
                        elements_with_positive_tabindex.append(
                            (
                                html_file.relative_to(html_file.parent.parent),
                                elem.name,
                                tabindex,
                            )
                        )
                except ValueError:
                    pass  # Skip non-numeric tabindex

        assert not elements_with_positive_tabindex, (
            f"The following elements have positive tabindex (anti-pattern):\n"
            f"{chr(10).join(f'{p}: <{tag}> tabindex={idx}' for p, tag, idx in elements_with_positive_tabindex)}"
        )

    def test_interactive_elements_are_keyboard_accessible(self, html_files):
        """Verify that interactive elements are keyboard accessible."""
        # Check for onclick handlers on non-interactive elements
        non_interactive_with_onclick = []

        INTERACTIVE_TAGS = ["a", "button", "input", "select", "textarea"]

        for html_file in html_files:
            soup = parse_html(html_file)
            elements = soup.find_all(attrs={"onclick": True})

            for elem in elements:
                if elem.name not in INTERACTIVE_TAGS:
                    # Check if it has tabindex or role to make it keyboard accessible
                    has_tabindex = elem.get("tabindex") is not None
                    role = elem.get("role", "")
                    is_interactive_role = role in ["button", "link", "tab"]

                    if not (has_tabindex or is_interactive_role):
                        non_interactive_with_onclick.append(
                            (html_file.relative_to(html_file.parent.parent), elem.name)
                        )

        assert not non_interactive_with_onclick, (
            f"The following pages have non-interactive elements with onclick:\n"
            f"{chr(10).join(f'{p}: <{tag}>' for p, tag in non_interactive_with_onclick)}"
        )
