# Design

Visual and UX choices that shape the site.

## Theme system

Three states, controlled by a `data-theme` attribute on `<html>`:

| `data-theme` value | Effect                                     |
| ------------------ | ------------------------------------------ |
| _absent_           | Follow OS `prefers-color-scheme` (default) |
| `"light"`          | Force light, regardless of OS              |
| `"dark"`           | Force dark, regardless of OS               |

The override is persisted in `localStorage` under `theme-preference`.

### Three files cooperate

- **`static/js/theme-init.js`** — runs **blocking** in `<head>` (see
  `layouts/partials/head.html` near the top). Reads `theme-preference` and
  sets `data-theme` before paint, preventing a flash of unstyled content
  (FOUC). Keep this minimal and synchronous.
- **`static/js/theme-toggle.js`** — wires up the footer toggle button.
  Three-state logic: when the user clicks toward their OS preference, the
  override is _cleared_ rather than set, so the site goes back to following
  the OS. When clicking _away_ from the OS preference, the override is
  saved. Listens for `prefers-color-scheme` changes and updates button
  text in real time.
- **`assets/css/main.css`** — defines CSS variables for both themes. The
  light variables live on `:root` and `[data-theme="light"]`. The dark
  variables live on both `[data-theme="dark"]` _and_ inside a
  `@media (prefers-color-scheme: dark)` block guarded by
  `:root:not([data-theme="light"])`, so an explicit light override beats
  the OS dark preference. This duplication is intentional — see comments
  near the dark theme block.

### Adding a themed color

1. Add the variable to **all four** places in `main.css`:
   - `:root` (default/light)
   - `[data-theme="light"]`
   - `[data-theme="dark"]`
   - The `@media (prefers-color-scheme: dark)` rule inside `:root:not(...)`
2. Reference via `var(--color-...)` in component rules. Avoid hard-coded
   colors anywhere else.

## Typography

- **Source Serif 4** variable font, served locally from
  `static/fonts/` to avoid third-party CDN dependencies and keep CSP
  strict. Regular + Italic VF files cover all weights via
  `font-weight: 100 900` in the `@font-face` rule.
- Body weight is `300` (light) per `body { font-weight: 300; }` for an
  airy reading experience; bold uses `font-weight: 600` (not 700) to
  match the design language.
- Base `font-size` is `12pt` on `html`, with `rem`-based scaling everywhere
  else. Mobile breakpoint at `768px`.
- `font-display: swap` so fallback serif renders immediately while the
  font loads.

## Color palette intent

- **Light** — warm off-white background (`#faf7f2`), darker
  near-black text (`#1a1a1a`), blue accent (`#0069d9`). Designed to feel
  paper-like rather than sterile.
- **Dark** — true-dark background (`#121212`), warm yellow accent
  (`#e0d890` resting → `#f9ff99` on hover) chosen to be readable and
  warm without the typical blue-on-black harshness.

## Layout primitives

- `.container` — max-width `100ch`, centered. Standard reading-width
  pattern for prose pages.
- `.card` — `1px` border that animates to the accent color on hover or
  focus-within. Used for portfolio/post listings.
- `.post` — CSS grid `150px 1fr` with `image text` areas; collapses to
  single-column at `≤768px` via `grid-template-areas`. Used by
  `layouts/partials/post-card.html`.
- `.article` / `.article-img` — float-based layout for inline images
  with prose. Collapses to block layout on mobile.

## Accessibility notes

- `.sr-only` utility for screen-reader-only headings (structural
  H1/H2/etc. that shouldn't render visually). See `main.css`.
- Every interactive element has an explicit `:focus-visible` rule with
  a `2px` outline at `--color-accent` and `2px` offset. Don't remove
  `:focus-visible` outlines without replacing them.
- Theme toggle button has dynamic `aria-label` ("Switch to dark mode" /
  "Switch to light mode") that updates with the effective theme.
- The site target is **WCAG 2.1 Level AA**. New visual changes must
  preserve adequate contrast in both themes — verify with browser
  devtools or a contrast checker.

## CSP and inline content

- Strict CSP forbids `unsafe-inline`. All JavaScript lives in
  `static/js/` and is loaded via `<script src="...">`.
- Single exception: `theme-init.js` is loaded with a `<script>` tag at
  the very top of `<head>` to prevent FOUC; it is still external (not
  inline), so CSP is satisfied.
- Avoid `style=""` attributes in templates. Add a class and rule in
  `main.css` instead.

## Open Graph / structured data

- Open Graph + Twitter Card meta tags emitted by
  `layouts/partials/head.html`. Twitter card type upgrades to
  `summary_large_image` when a page declares `.Params.image`.
- JSON-LD structured data in `layouts/partials/structured-data.html`:
  `WebSite` schema on home, `Article` schema on writing posts, `Person`
  schema on the About page. Validated by
  `tests/test_structured_data.py`.

## Markdown rendering

- Hugo's default markdown renderer.
- Custom render hook at `layouts/_default/_markup/render-link.html`:
  - Links starting with `_` open in a new tab (strip the underscore
    prefix and add `target="_blank" rel="noopener noreferrer"`).
  - External links (anything not under `site.BaseURL`) also open in a
    new tab.
  - Link text is rendered with `safeHTML` so inline emphasis/code is
    preserved. Safe here because all content is trusted (single-author).
