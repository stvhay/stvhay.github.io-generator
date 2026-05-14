#!/usr/bin/env python3
"""
Screenshot helper for UX review.

Renders the given URL at a named viewport preset and writes a PNG.

The Hugo dev server should already be running (see CLAUDE.md). Playwright
must be available; an easy way is:

    uv run --with playwright python utilities/screenshot.py --help

Set CHROME_PATH to a chromium binary, e.g.

    nix shell nixpkgs#chromium --command bash -c '
        CHROME_PATH="$(which chromium)" \
        uv run --with playwright python utilities/screenshot.py \
            --url http://localhost:1313/ --out tmp/screenshots/home.png'
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

DEFAULT_CHROME = os.environ.get("CHROME_PATH")

VIEWPORTS = {
    "desktop": {"width": 1280, "height": 800},
    "tablet": {"width": 820, "height": 1180},
    "mobile": {"width": 390, "height": 844},
}


def shoot(url: str, out: Path, viewport: dict, full_page: bool = True) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        kwargs = {"headless": True}
        if DEFAULT_CHROME:
            kwargs["executable_path"] = DEFAULT_CHROME
        browser = p.chromium.launch(**kwargs)
        try:
            ctx = browser.new_context(viewport=viewport, device_scale_factor=1)
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=15000)
            page.screenshot(path=str(out), full_page=full_page)
        finally:
            browser.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument(
        "--viewport",
        choices=list(VIEWPORTS),
        default="desktop",
        help="Named viewport preset.",
    )
    ap.add_argument(
        "--no-full",
        action="store_true",
        help="Disable full-page; capture only the viewport.",
    )
    args = ap.parse_args()
    shoot(
        url=args.url,
        out=args.out,
        viewport=VIEWPORTS[args.viewport],
        full_page=not args.no_full,
    )
    print(f"wrote {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
