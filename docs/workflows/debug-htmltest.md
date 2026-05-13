# Debug htmltest failures

`htmltest` validates the rendered site under `public/` for broken
internal links, missing image alt text, broken anchors, scripts that
don't resolve, etc. It runs as part of the pytest suite
(`tests/test_htmltest.py`) and in CI.

## Quick triage

```bash
nix develop --command ./build         # produces public/
nix develop --command htmltest        # direct run, full output
```

The pytest wrapper at `tests/test_htmltest.py` invokes the same binary
but captures output and applies a timeout.

## Common failure modes

### External URL returns 403 / 429 / timeout

Some sites (DOI, WorldCat, LinkedIn, doi.org for some publishers)
block bot user agents. The link works fine in a browser.

**Fix**: add the URL to `IgnoreURLs` in `.htmltest.yml`, _not_ to
the test or markdown. Keep one URL per line, with a brief comment
explaining why if it's not obvious.

### Internal link broken (404 in public/)

The target file doesn't exist in `public/`. Causes:

- Typo in the markdown link.
- Source page is `draft = true` or has a future `publishDate`.
- The link uses a section path that doesn't match Hugo's slug.

**Fix**: open the rendered page in the dev server
(`hugo server -D`), follow the link, see where it lands. Update either
the link or the target page.

### Image missing `alt`

WCAG / accessibility requirement; htmltest catches it.

**Fix**: add an `alt` attribute. In markdown, use
`![descriptive text](image.png)`. In templates, never emit
`<img>` without `alt` — pass an empty string `alt=""` only for purely
decorative images.

### Script `src` not found

Usually a stale reference to a JS file that was renamed or moved
under `static/js/`.

**Fix**: grep templates and markdown for the old path and update.

### htmltest times out

`tests/test_htmltest.py` has a `subprocess.run(..., timeout=...)`. If
the full external-link check takes longer than the timeout, the test
fails even though htmltest itself is fine.

**Diagnosis**: run `htmltest` directly without the test wrapper. If it
finishes cleanly given more time, raise the timeout in
`test_htmltest.py`. Don't disable the external check globally — CI
relies on it.

## `.htmltest.yml` reference

Key options used here:

| Option               | Value                       | Why                                                    |
| -------------------- | --------------------------- | ------------------------------------------------------ |
| `DirectoryPath`      | `public`                    | Where to scan                                          |
| `CheckInternalLinks` | `true`                      | Catches broken `<a>` targets                           |
| `CheckInternalHash`  | `true`                      | Catches broken `#anchor` targets                       |
| `CheckExternal`      | `true`                      | Validates outbound URLs                                |
| `EnforceHTTPS`       | `true`                      | Reject `http://` external links                        |
| `CheckImages`        | `true`                      | Enforce `alt`                                          |
| `CheckScripts`       | `true`                      | Validate `<script src>`                                |
| `CheckFavicon`       | `true`                      | Every page must reference a favicon                    |
| `IgnoreDirs`         | `categories`, `tags`, `cns` | Auto-generated taxonomy pages and class material       |
| `CacheExpires`       | `336h`                      | 2-week cache of external-link checks; speeds up reruns |

## When in doubt

- The fix for a flaky bot-blocked external URL is `IgnoreURLs`, not
  removing the link from content.
- The fix for an internal failure is _always_ in the content or
  template, not in the htmltest config.
