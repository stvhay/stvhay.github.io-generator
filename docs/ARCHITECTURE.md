# Architecture

How the site is organized, built, and deployed.

## Two repositories

This project lives in **two independent git repositories**, not a submodule
arrangement:

| Repo                       | Role                                                       | Remote                    |
| -------------------------- | ---------------------------------------------------------- | ------------------------- |
| `website-hugo` (this repo) | Source: Hugo content, layouts, LaTeX, build scripts, tests | `stvhay/website-hugo`     |
| `stvhay.github.io`         | Hosting: generated HTML and PDFs served by GitHub Pages    | `stvhay/stvhay.github.io` |

The source repo expects the hosting repo to be cloned as a working tree at
`./public/`. The build script (`utilities/build.sh`) manages that clone:
resets it, restores cached LaTeX PDFs, runs Hugo into it, then stages the
result. CI does the same in `.github/workflows/website.yml` and pushes the
generated commit to the hosting repo.

`public/` is in `.gitignore` so the source repo never tracks it. There is
**no `.gitmodules`** — the README's "git submodule" wording is historical
and inaccurate.

### Portability seam

The build's contract with the outside world is **a directory of static
files at `public/`**. The "push to a separate hosting repo" pattern is
just one consumer of that directory. Any other consumer of a static-file
tree can replace it without touching anything upstream of `public/`:

| Target                | Replacement                                  |
| --------------------- | -------------------------------------------- |
| S3 / CloudFront       | `aws s3 sync public/ s3://bucket/`           |
| Generic SSH host      | `rsync -avz --delete public/ host:/var/www/` |
| Netlify               | `netlify deploy --dir=public --prod`         |
| Cloudflare Pages / R2 | `wrangler pages publish public/`             |

This is the durable virtue of the dual-repo pattern over alternatives
like `actions/deploy-pages` (which couples the project to GitHub Pages
specifically). The filesystem boundary is host-agnostic; the dual-repo
choreography on top of it is a swappable thin layer.

## Toolchain

Everything runs inside `nix develop`. The flake (`flake.nix`) pins:

- Hugo extended
- A trimmed TeX Live distribution (latexmk, biber, fonts, hyperref, etc.)
- `exiftool` for PDF metadata
- `htmltest` for HTML link/image validation
- Python 3 + pytest + BeautifulSoup + lxml + PyYAML
- Node + prettier (for HTML formatting)

Quick commands:

```bash
nix develop                                           # enter shell
nix develop --command ./build                         # full build
nix develop --command hugo server -D                  # dev server (live reload)
nix develop --command pytest tests/ -m "not external" # tests (no network)
```

## Build pipeline

`./build` runs `utilities/build.sh`, which performs:

1. **Reset `public/`**: clone the hosting repo if needed, otherwise reset
   and pull. `git rm --cached` everything except `.gitignore` and previously
   built PDFs (recovered from `main` via `git checkout main docs/...pdf`).
2. **LaTeX compile, hash-cached**: for each entry in `latex/latex.manifest`,
   compute SHA-384 of the `.tex` source and compare against `XMP-pdfx:texhash`
   embedded in the existing PDF. If they match, skip. Otherwise: `latexmk`,
   then `exiftool` to embed the new hash into the rebuilt PDF.
3. **Place outputs**: built PDFs are moved to `latex/output/<doc>/<doc>.pdf`.
   Hugo's `[module.mounts]` config (see `hugo.toml`) maps `latex/output` to
   `static/docs`, so PDFs appear at site URL `/docs/<doc>/<doc>.pdf` (e.g.
   `/docs/cv/cv-steve-hay.pdf`).
4. **Run Hugo**: produces the static site in `public/`.
5. **Prettier**: format all generated HTML.
6. **Clean**: remove built PDFs from `latex/output/` (they live in the
   hosting repo, not the source repo).
7. **Report status** for both repos.

`./publish "<message>"` commits and pushes both repos with the same message.

## Repository layout

```
.
├── archetypes/        # Hugo content templates
├── assets/css/        # Hugo Pipes assets (currently just main.css)
├── content/           # Site content (Markdown)
│   ├── portfolio/     # Portfolio items (bundle dirs with index.md + assets)
│   ├── writing/       # Blog posts (bundle dirs)
│   ├── about.md
│   └── contact.md
├── docs/              # This directory — repo documentation
├── latex/             # LaTeX sources + build outputs
│   ├── cv/
│   ├── experience-prosopagnosia/
│   ├── latex.manifest # List of .tex files to build
│   └── output/        # Build artifacts (gitignored, served at /docs/)
├── layouts/           # Hugo templates
│   ├── _default/      # baseof, home, list, single + _markup/render-link
│   ├── partials/      # head, header, footer, menu, post-card, etc.
│   └── shortcodes/    # scrambled-email
├── public/            # Hosting repo working tree (gitignored)
├── static/            # Served as-is at site root — see "Static content" below
├── tests/             # pytest suite (markers: meta, structured_data, html5,
│                      #   content, accessibility, javascript, external)
├── utilities/         # build.sh, publish.sh, post.sh sourced by utilities.sh
├── build, publish, post  # Bash wrappers that source utilities.sh
├── flake.nix          # Pinned dev environment
├── hugo.toml          # Hugo config, including module.mounts for LaTeX
└── .htmltest.yml      # htmltest configuration
```

## Static content: three categories

Files under `static/` are served verbatim at the site root by Hugo. Three
categories live there:

| Category          | Examples                                                                                                         | Conventions                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Generated**     | `static/cns/` (Jupyter HTML), `latex/output/` mounted at `static/docs`                                           | Source lives elsewhere or in an automated pipeline. Not authored by hand.      |
| **Vendored**      | `static/s3m/js-dos.js`                                                                                           | Third-party. Pinned version, license + purpose documented in `README.md`.      |
| **Hand-authored** | `static/js/`, `static/plasma/`, `static/s3m/it.html`, `static/fonts/`, `static/favicon.ico`, `static/robots.txt` | Authored in-repo, conceptually "generated" by the trivial copy transformation. |

Top-level dirs that aren't `vendored/` or explicitly noted as generated
should be treated as hand-authored. `static/cns/` is an exception: the
HTML was generated from Jupyter notebooks for a class, but the notebooks
are intentionally not committed here (they are coursework solutions kept
private out of courtesy to the professor).

## URL paths worth remembering

| URL                                    | Source                                                               |
| -------------------------------------- | -------------------------------------------------------------------- |
| `/`                                    | `layouts/_default/home.html` + `content/_index` (none → empty)       |
| `/portfolio/`, `/writing/`             | `layouts/_default/list.html` + each `content/<section>/_index.md`    |
| `/portfolio/<slug>/` etc.              | `layouts/_default/single.html` + `content/<section>/<slug>/index.md` |
| `/docs/cv/cv-steve-hay.pdf`            | `latex/output/cv/cv-steve-hay.pdf` (via Hugo mount)                  |
| `/docs/experience-prosopagnosia/*.pdf` | same mechanism                                                       |
| `/cns/`, `/plasma/`, `/s3m/`           | `static/` (served as-is)                                             |
| `/js/`, `/favicon.ico`, `/robots.txt`  | `static/` (served as-is)                                             |

## Security model

The site is static, served over HTTPS by GitHub Pages. Threat model is
client-side only: XSS, CSP compliance, third-party supply chain. Details
and the pre-commit checklist live in the gitignored agent instructions
(`.claude/CLAUDE.md`); summary in `README.md`.

Notable in-template choices:

- Strict CSP: `default-src 'self'; script-src 'self';` declared in
  `layouts/partials/head.html`. No `unsafe-inline`, no `unsafe-eval`.
- All scripts external; no inline `<script>` or `on*=""` handlers.
- `layouts/_default/_markup/render-link.html` uses `safeHTML` on link text
  to preserve markdown formatting inside links; this is safe because all
  content in this repo is trusted (single-author).

## CI

`.github/workflows/website.yml` runs on push to `main`:

1. Install Nix via `cachix/install-nix-action`
2. Attach Cachix binary cache `stvhay-github-io` (via `CACHIX_AUTH_TOKEN`)
3. SSH key (`WEBSITE_SSH_KEY`) lets the runner push to the hosting repo
4. `nix develop --command bash -c './build && htmltest && pytest'`
5. Commit and push generated `public/` to the hosting repo

Note: the workflow runs `htmltest` and `pytest` separately rather than via
`./build`, which keeps the build script generation-focused.
