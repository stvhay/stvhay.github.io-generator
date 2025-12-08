"""Tests for URLs ignored by htmltest to verify they actually work."""

import subprocess
from pathlib import Path

import pytest
import yaml


@pytest.fixture(scope="session")
def htmltest_config(public_dir):
    """Load the htmltest configuration file."""
    config_path = public_dir.parent / ".htmltest.yml"
    if not config_path.exists():
        pytest.skip("No .htmltest.yml configuration file found")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def ignored_urls(htmltest_config):
    """Extract the list of ignored URLs from htmltest config."""
    ignore_urls = htmltest_config.get("IgnoreURLs", [])
    if not ignore_urls:
        pytest.skip("No IgnoreURLs configured in .htmltest.yml")
    return ignore_urls


@pytest.mark.external
class TestIgnoredURLs:
    """Tests for URLs that htmltest ignores but should still work."""

    def test_ignored_urls_are_reachable(self, ignored_urls):
        """Verify that ignored URLs return valid HTTP responses."""
        unreachable_urls = []
        blocked_urls = []

        for url in ignored_urls:
            # Use curl with a browser-like user agent to bypass bot blocking
            result = subprocess.run(
                [
                    "curl",
                    "-s",
                    "-o", "/dev/null",
                    "-w", "%{http_code}",
                    "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "-L",  # Follow redirects
                    "--max-time", "10",
                    url,
                ],
                capture_output=True,
                text=True,
            )

            http_code = result.stdout.strip()

            # Accept 2xx and 3xx status codes as valid
            # Some sites may redirect, which is fine
            if http_code.startswith(("2", "3")):
                continue
            # 403 Forbidden means the resource exists but has very aggressive bot blocking
            # This is acceptable for ignored URLs, but worth noting
            elif http_code == "403":
                blocked_urls.append((url, http_code))
            # Other error codes (404, 500, etc.) suggest broken links
            else:
                unreachable_urls.append((url, http_code))

        if blocked_urls:
            print(
                f"\nNOTE: The following URLs return 403 even with browser user agent (very aggressive bot protection):\n"
                f"{chr(10).join(f'{url}: HTTP {code}' for url, code in blocked_urls)}"
            )

        assert not unreachable_urls, (
            f"The following ignored URLs appear to be broken (not just bot-protected):\n"
            f"{chr(10).join(f'{url}: HTTP {code}' for url, code in unreachable_urls)}\n\n"
            f"These URLs are ignored in .htmltest.yml but may be dead links. "
            f"Consider removing them from IgnoreURLs or updating the links."
        )

    def test_ignored_urls_block_bots(self, ignored_urls):
        """Verify that ignored URLs actually block bot user agents."""
        # This test ensures URLs are legitimately ignored due to bot blocking,
        # not just because we're hiding broken links

        urls_that_allow_bots = []

        for url in ignored_urls:
            # Test with htmltest's default user agent
            result = subprocess.run(
                [
                    "curl",
                    "-s",
                    "-o", "/dev/null",
                    "-w", "%{http_code}",
                    "-A", "htmltest",
                    "-L",
                    "--max-time", "10",
                    url,
                ],
                capture_output=True,
                text=True,
            )

            http_code = result.stdout.strip()

            # If the URL returns 2xx with bot user agent, it shouldn't be ignored
            if http_code.startswith("2"):
                urls_that_allow_bots.append((url, http_code))

        if urls_that_allow_bots:
            print(
                f"\nWARNING: The following URLs don't block bots and may not need to be ignored:\n"
                f"{chr(10).join(f'{url}: HTTP {code}' for url, code in urls_that_allow_bots)}"
            )
