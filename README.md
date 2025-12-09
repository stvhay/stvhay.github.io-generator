# stvhay.github.io-generator

[![website](https://github.com/stvhay/stvhay.github.io-generator/actions/workflows/website.yml/badge.svg)](https://github.com/stvhay/stvhay.github.io-generator/actions/workflows/website.yml)

A Hugo-based static site generator that integrates LaTeX document compilation with automated deployment to GitHub Pages.

## Overview

This repository generates a static website from Markdown and LaTeX sources. The build process:
- Compiles LaTeX documents to PDFs (with smart caching to avoid unnecessary rebuilds)
- Builds a Hugo static site from Markdown content
- Formats HTML output with prettier
- Deploys to GitHub Pages via a dual-repository structure

## Architecture

### Dual-Repository Design

- **Source repository** (this repo): Contains Hugo source, LaTeX files, and build scripts
- **Public repository** (`public/`): Git submodule pointing to [stvhay.github.io](https://github.com/stvhay/stvhay.github.io/) for GitHub Pages hosting

The `public/` directory is a clone of the GitHub Pages repository. When you build, Hugo generates the site into `public/`, and you can push those changes separately to deploy.

### LaTeX Build System

LaTeX documents are managed via `latex/latex.manifest`, which lists all `.tex` files to compile:

```
cv/cv-steve-hay.tex
experience-prosopagnosia/experience-prosopagnosia.tex
experience-prosopagnosia/experience-prosopagnosia-design.tex
```

**Smart caching**: The build system embeds a SHA-384 hash of each `.tex` file into its generated PDF metadata. On subsequent builds, it only recompiles PDFs when the source `.tex` file has changed, significantly speeding up the build process.

## Setup

### Prerequisites

Install required packages:

```bash
# Debian/Ubuntu
apt install hugo texlive-latex-base texlive-latex-extra \
    texlive-bibtex-extra latexmk biber \
    libimage-exiftool-perl

# Node.js packages
npm install --save-dev --save-exact prettier
```

### Initialize public/ repository

Clone the GitHub Pages repository into `public/`:

```bash
git clone git@github.com:stvhay/stvhay.github.io.git public
```

## Build Scripts

### `./build`

Main build script that:
1. Clones/updates the `public/` repository
2. Reads `latex/latex.manifest` and compiles changed LaTeX documents
3. Runs Hugo to generate the static site
4. Formats HTML with prettier
5. Stages changes in both repos

Options:
- `./build --no-pretty` - Skip prettier formatting

### `./publish [message]`

Commits and pushes changes to both repositories:
- Commits to `public/` (GitHub Pages repo)
- Commits to source repo
- Pushes both

Usage:
```bash
./publish "add new blog post"
```

## Utility Functions

Source `utilities.sh` to access helper functions in your shell:

```bash
source utilities.sh
```

Available functions:

### `post <title>`

Create a new blog post or portfolio item:

```bash
post "My New Article"              # Creates content/writing/my-new-article/index.md
post --page portfolio "My Project" # Creates content/portfolio/my-project/index.md
post --single "Quick Note"         # Creates single .md file instead of bundle
```

Opens your `$EDITOR` to edit the new post.

### `build [--no-pretty]`

Same as `./build` script (see above).

### `publish [message]`

Same as `./publish` script (see above).

## Project Structure

```
.
├── content/              # Hugo content (Markdown)
│   ├── portfolio/       # Portfolio items
│   ├── writing/         # Blog posts
│   ├── about.md         # About page
│   └── contact.md       # Contact page
├── layouts/             # Hugo templates
├── static/              # Static assets
├── latex/               # LaTeX source files
│   ├── latex.manifest   # List of .tex files to compile
│   └── cv/             # Example: CV documents
├── public/              # Generated site (git submodule)
├── utilities/           # Build script modules
│   ├── build.sh        # Build logic
│   ├── publish.sh      # Publish logic
│   └── post.sh         # Post creation logic
└── utilities.sh         # Loads all utilities

```

## Development Workflow

1. **Create content**: Use `post` function or manually create Markdown files
2. **Add LaTeX docs**: Place `.tex` files in `latex/` and add to `latex/latex.manifest`
3. **Build locally**: Run `./build` to test
4. **Publish**: Run `./publish "commit message"` to deploy

## CI/CD

GitHub Actions automatically builds and deploys on push to `main`:
- Installs dependencies (TeX Live, Hugo, prettier)
- Runs `./build`
- Pushes to GitHub Pages repository

See `.github/workflows/website.yml` for details.

## Technologies

- [Hugo](https://gohugo.io/) - Static site generator
- [pdfTeX](https://tug.org/applications/pdftex/) via latexmk - LaTeX compilation
- [prettier](https://prettier.io) - HTML formatting
- [exiftool](https://exiftool.org/) - PDF metadata management for build caching
- [GitHub Pages](https://pages.github.com/) - Hosting

## AI-Assisted Development

This project is developed with [Claude](https://claude.ai/) as an AI coding assistant, using [Claude Code](https://claude.ai/code) for collaborative development. Claude assists with code generation, refactoring, testing, and documentation.

Commits co-authored by Claude are marked with:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```
