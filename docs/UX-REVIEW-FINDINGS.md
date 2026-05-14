# UX/UI Review Findings

Tracking file for issues identified in the Hugo generation code on 2026-05-14.
Each item is checked off when fixed and verified visually.

Severity legend:

- **C** — Critical (functional bug or invalid markup)
- **A** — Accessibility issue
- **V** — Visual / hierarchy issue
- **Q** — Code quality / dead code

| #   | Sev | Status | Issue                                                                   | Primary file(s)                                                   |
| --- | --- | ------ | ----------------------------------------------------------------------- | ----------------------------------------------------------------- |
| 1   | C   | [x]    | Nested `.post-img` wrappers in every post card                          | `layouts/partials/post-card.html`, `layouts/partials/thumb.html`  |
| 2   | C   | [x]    | Card summary renders full markdown including headings/lists             | `layouts/partials/post-card.html`, `content/portfolio/*/index.md` |
| 3   | C   | [x]    | Invalid block elements inside `<p>` on contact page                     | `layouts/shortcodes/scrambled-email.html`, `content/contact.md`   |
| 4   | A   | [x]    | List pages have no visible heading (`sr-only` h1)                       | `layouts/_default/list.html`                                      |
| 5   | A   | [x]    | Section `id` derived from raw `.Title` (spaces invalid)                 | `layouts/_default/list.html`                                      |
| 6   | A   | [x]    | Site title is not a link to home                                        | `layouts/partials/header.html`                                    |
| 7   | A   | [x]    | No skip-to-content link                                                 | `layouts/_default/baseof.html`, CSS                               |
| 8   | A   | [ ]    | `prefers-reduced-motion` ignored by email scrambler                     | `static/js/email-scrambler.js`, `assets/css/main.css`             |
| 9   | A   | [ ]    | Theme-toggle initial label is wrong for half of users                   | `layouts/partials/footer.html`, `static/js/theme-init.js`         |
| 10  | A   | [x]    | CV menu link `target="_blank"` lacks `rel="noopener"`                   | `layouts/partials/menu.html`                                      |
| 11  | V   | [ ]    | `h3` (1.25rem) barely larger than `p` (1.2rem)                          | `assets/css/main.css`                                             |
| 12  | V   | [ ]    | `.section-mark` overlay overlaps long content                           | `assets/css/main.css`, `layouts/partials/post-card.html`          |
| 13  | V   | [ ]    | Mobile nav has no responsive layout                                     | `assets/css/main.css`                                             |
| 14  | V   | [ ]    | Light-mode theme-toggle hover hardcodes dark-mode yellow                | `assets/css/main.css`                                             |
| 15  | V   | [ ]    | `.reveal-email-button:hover` has low contrast (color collision)         | `assets/css/main.css`                                             |
| 16  | V   | [ ]    | `.article-img` fixed at 25rem dominates mid-width screens               | `assets/css/main.css`                                             |
| 17  | Q   | [ ]    | Person structured data never fires (about page title is "Welcome")      | `layouts/partials/structured-data.html`                           |
| 18  | Q   | [ ]    | CSP allows `https://stvhay.github.io` for scripts but no script uses it | `layouts/partials/head.html`                                      |
| 19  | Q   | [ ]    | Theme variables duplicated across `:root`, `@media`, and `[data-theme]` | `assets/css/main.css`                                             |
| 20  | Q   | [ ]    | `terms.html` uses non-semantic `<div>Tags:</div>` label                 | `layouts/partials/terms.html`                                     |
| 21  | Q   | [ ]    | `<br>` used for spacing after date                                      | `layouts/_default/single.html`, `layouts/partials/post-card.html` |
| 22  | Q   | [ ]    | Pre-reveal email is real `<a href="mailto:noscript@example.com">`       | `layouts/shortcodes/scrambled-email.html`                         |
| 23  | Q   | [ ]    | Render-link `_` prefix convention undocumented                          | `layouts/_default/_markup/render-link.html`                       |
| 24  | Q   | [ ]    | `<i>` used purely for italic date                                       | `layouts/partials/post-card.html`, CSS                            |

## Verification protocol

For each fix:

1. Read related HTML output, template(s), and CSS together — check for paired structural/style bugs.
2. Apply fix (smallest scope, simplifying where structure does not pay rent).
3. Rebuild site (`hugo` or `./build`).
4. Open page in the Playwright MCP at desktop (1280×800) and mobile (390×844) widths; take screenshots before/after.
5. Verify the fix renders as intended; check golden path and obvious regressions.
6. Commit atomically with a `fix:` or `refactor:` prefix.

## Investigation log

### 2026-05-14 — Sandbox font-system artifact (resolved, not a real bug)

While setting up the Playwright MCP, observed: every page renders with empty
text, `@font-face` faces report `status: "error"`, and `.container` collapses to
40px because `100ch` evaluates to 0. **Initially logged this as Issue 0, but
the root cause was that this Apple Container has no system fonts at all
(`fc-list` missing, `/usr/share/fonts/` absent).** Even canvas `measureText`
for plain `sans-serif` returns 0. No production code change needed — the site
is fine for users with installed fonts.

Mitigation: MCP launch wrapped in `nix shell nixpkgs#fontconfig
nixpkgs#dejavu_fonts` plus a user-level `~/.config/fontconfig/fonts.conf` that
points at the nix DejaVu directory and the project's `static/fonts/`. After
this, the MCP browser renders text normally.
