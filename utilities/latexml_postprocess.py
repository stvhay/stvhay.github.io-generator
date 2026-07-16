#!/usr/bin/env python3
"""Finish the <head> of a LaTeXML-generated HTML document.

Usage: latexml_postprocess.py <file.html> <texhash> <pipeline-version>

LaTeXML output is post-processed so each document is self-contained,
site-styled, and carries a strict per-page Content-Security-Policy:

- The legacy http-equiv encoding declaration becomes the HTML5 charset
  meta the site standard expects.
- Every inline style attribute (LaTeXML's representation of computed
  values like font scaling and rule dimensions) is converted to a
  deterministic class in one document <style> block, allowed by CSP
  hash. This is what lets the policy avoid 'unsafe-inline' entirely.
- The policy blocks everything else: these pages have no scripts, no
  forms, and only same-origin images, styles, and fonts.
- The favicon (required in every static HTML file), the shared
  stylesheets under /css/latexml/, and the texhash stamp the build
  uses for skip-unchanged caching are linked in.

NOTE: the CSP hash covers the exact bytes of the <style> element, so
generated documents must not be reformatted afterwards (public/docs/
is excluded in .prettierignore).
"""

import base64
import hashlib
import re
import sys

from bs4 import BeautifulSoup

CHARSET_LEGACY = {"http-equiv": "content-type"}
STYLESHEETS = [
    "/css/latexml/LaTeXML.css",
    "/css/latexml/ltx-article.css",
    "/css/latexml/site.css",
]
FAVICONS = [
    {"href": "/favicon.ico", "sizes": "32x32"},
    {"href": "/favicon.svg", "type": "image/svg+xml"},
]


def class_name(value: str, taken: dict[str, str]) -> str:
    """Deterministic, readable class for a style value, e.g.
    "font-size: 173%" -> "ltxs-font-size-173"."""
    slug = "ltxs-" + re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    name = slug
    counter = 2
    while name in taken and taken[name] != value:
        name = f"{slug}-{counter}"
        counter += 1
    taken[name] = value
    return name


def main() -> None:
    path, texhash, pipeline = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    head = soup.head
    if head is None:
        sys.exit(f"no <head> in {path}")

    legacy = head.find("meta", attrs=CHARSET_LEGACY)
    if legacy is not None:
        legacy.decompose()
    head.insert(0, soup.new_tag("meta", charset="utf-8"))

    # The generated footer carries a meaningless SOURCE_DATE_EPOCH
    # timestamp and a data:-URI logo the CSP would refuse; LaTeXML is
    # credited in README.md instead.
    for footer in soup.select(".ltx_page_footer"):
        footer.decompose()

    # Inline styles -> one hashed <style> block of deterministic classes.
    taken: dict[str, str] = {}
    rules: dict[str, str] = {}
    for el in soup.select("[style]"):
        value = re.sub(r"\s+", " ", el["style"]).strip().rstrip(";")
        del el["style"]
        if not value:
            continue
        name = class_name(value, taken)
        rules[name] = value
        el["class"] = el.get("class", []) + [name]

    style_src = "'self'"
    if rules:
        css_text = "\n" + "".join(
            f".{name} {{ {value}; }}\n" for name, value in sorted(rules.items())
        )
        digest = hashlib.sha256(css_text.encode("utf-8")).digest()
        style_src += f" 'sha256-{base64.b64encode(digest).decode()}'"

    # Per-page CSP, stricter than the site's: no scripts at all. Meta
    # CSP must precede the resources it governs, so it goes second in
    # the head (after the charset declaration).
    csp = soup.new_tag("meta")
    csp["http-equiv"] = "Content-Security-Policy"
    csp["content"] = (
        "default-src 'none'; "
        "img-src 'self'; "
        f"style-src {style_src}; "
        "font-src 'self'; "
        "base-uri 'none'; "
        "form-action 'none'"
    )
    head.insert(1, csp)

    for attrs in FAVICONS:
        head.append(soup.new_tag("link", rel="icon", **attrs))
    for href in STYLESHEETS:
        head.append(soup.new_tag("link", rel="stylesheet", href=href, type="text/css"))
    if rules:
        style = soup.new_tag("style")
        style.string = css_text
        head.append(style)
    head.append(soup.new_tag("meta", attrs={"name": "texhash", "content": texhash}))
    head.append(
        soup.new_tag("meta", attrs={"name": "latexml-pipeline", "content": pipeline})
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(str(soup))


if __name__ == "__main__":
    main()
