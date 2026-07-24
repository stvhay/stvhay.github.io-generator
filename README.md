# stvhay.github.io-generator

[![website](https://github.com/stvhay/stvhay.github.io-generator/actions/workflows/website.yml/badge.svg)](https://github.com/stvhay/stvhay.github.io-generator/actions/workflows/website.yml)

A Hugo-based static site generator with LaTeX document compilation and automated deployment to GitHub Pages.

## Overview

This repository generates a static website from Markdown and LaTeX sources:

- Compiles LaTeX documents to PDFs (with smart caching)
- Builds a Hugo static site from Markdown content
- Formats HTML output with prettier
- Deploys to GitHub Pages via a dual-repository structure

## Architecture

- **Source repository** (this repo): Hugo source, LaTeX files, and build scripts
- **Hosting repository** ([stvhay.github.io](https://github.com/stvhay/stvhay.github.io/)): Separate repository that serves GitHub Pages. The build script clones it into `public/` (gitignored) and pushes generated output there. Not a git submodule.

See [`DESIGN.md`](DESIGN.md) for the visual system and [`docs/`](docs/) for
architecture and workflow documentation.

### LaTeX Build System

LaTeX documents are listed in `latex/latex.manifest`. The build system embeds a SHA-384 hash into each PDF's metadata, only recompiling when the source changes.

## Setup

```bash
# Debian/Ubuntu
apt install hugo texlive-latex-base texlive-latex-extra \
    texlive-bibtex-extra latexmk biber libimage-exiftool-perl

# Node.js packages
npm install --save-dev --save-exact prettier

# Initialize public/ repository
git clone git@github.com:stvhay/stvhay.github.io.git public
```

## Usage

### Build Scripts

**`./build`** - Compiles LaTeX, builds Hugo site, formats HTML, stages changes.

**`./render <file.tex>`** - Compiles a single LaTeX document without building the
site. Documents under `latex/` render to `latex/output/`; documents elsewhere
render beside their source. Use `-o DIR` to choose a destination.

**`./publish [message]`** - Commits and pushes to both repositories.

### Utility Functions

Source `utilities.sh` for shell helpers:

```bash
source utilities.sh

post "My New Article"              # Creates content/writing/my-new-article/index.md
post --page portfolio "My Project" # Creates content/portfolio/my-project/index.md
post --single "Quick Note"         # Creates single .md file instead of bundle
```

## Project Structure

```
content/              # Hugo content (Markdown)
├── portfolio/        # Portfolio items
├── writing/          # Blog posts
├── about.md
└── contact.md
layouts/              # Hugo templates
static/               # Static assets
latex/                # LaTeX sources + latex.manifest
public/               # Generated site (clone of hosting repo, gitignored)
DESIGN.md             # Canonical visual design system
docs/                 # Repo documentation (architecture and workflows)
utilities/            # Build script modules
```

## Development Workflow

1. Create content with `post` or manually
2. Add LaTeX docs to `latex/` and update `latex.manifest`
3. Build locally with `./build`
4. Deploy with `./publish "message"`

## CI/CD

GitHub Actions builds and deploys on push to `main`. See `.github/workflows/website.yml`.

## Technologies

- [Hugo](https://gohugo.io/) - Static site generator
- [pdfTeX](https://tug.org/applications/pdftex/) via latexmk - LaTeX compilation
- [LaTeXML](https://math.nist.gov/~BMiller/LaTeXML/) - LaTeX to HTML conversion for accessible document versions
- [prettier](https://prettier.io) - HTML formatting
- [exiftool](https://exiftool.org/) - PDF metadata for build caching
- [htmltest](https://github.com/wjdp/htmltest) - Internal link and HTML structure validation
- [lychee](https://github.com/lycheeverse/lychee) - External link checking (scheduled CI)
- [GitHub Pages](https://pages.github.com/) - Hosting

### Asset Licenses

- Favicon artwork (`static/favicon.ico`, `static/favicon.svg`,
  `static/apple-touch-icon.png`) is the robot emoji (U+1F916) from
  [Twemoji](https://github.com/jdecked/twemoji), © Twitter/X and other
  contributors, licensed [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Document stylesheets (`static/css/latexml/`) are copied from
  [LaTeXML](https://github.com/brucemiller/LaTeXML) 0.8.8 (`LaTeXML.css`,
  `ltx-article.css`), a public-domain work of NIST. They are kept unmodified
  so upgrades can replace them wholesale; site-specific styling for generated
  documents lives in `site.css` alongside them.

## AI-Assisted Development

This project is developed with [Claude Code](https://claude.ai/code) as an AI coding assistant. Commits co-authored by Claude are marked with `Co-Authored-By: Claude <noreply@anthropic.com>`.
