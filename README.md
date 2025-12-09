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
- **Public repository** (`public/`): Git submodule pointing to [stvhay.github.io](https://github.com/stvhay/stvhay.github.io/) for GitHub Pages hosting

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
public/               # Generated site (git submodule)
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
- [prettier](https://prettier.io) - HTML formatting
- [exiftool](https://exiftool.org/) - PDF metadata for build caching
- [GitHub Pages](https://pages.github.com/) - Hosting

## AI-Assisted Development

This project is developed with [Claude Code](https://claude.ai/code) as an AI coding assistant. Commits co-authored by Claude are marked with `Co-Authored-By: Claude <noreply@anthropic.com>`.
