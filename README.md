# stvhay.github.io-generator

[![website](https://github.com/stvhay/stvhay.github.io-generator/actions/workflows/website.yml/badge.svg)](https://github.com/stvhay/stvhay.github.io-generator/actions/workflows/website.yml)

I wanted to be able to write documents in LaTeX and Markdown and published easily into a website. This is the result.

- I've ported my web content to Markdown and used [Hugo](https://gohugo.io/) to generate a static website.
- LaTeX files are converted to .pdf with [pdfTeX](https://tug.org/applications/pdftex/).
- Hugo outputs to a git submodule *public*.
- I run [prettier](https://prettier.io) on the Hugo output for consistent formatting.
- Continuous integration is used to push static content to a [GitHub](https://github.com/stvhay/stvhay.github.io/) repository configured for static hosting [here](https://stevenhay.com).

## Build environment

```bash
repo="git_pages_repo"
apt install hugo texlive-latex-base texlive-latex-extra \
    texlive-bibtex-extra latexmk biber \
    libimage-exiftool-perl
npm install --save-dev --save-exact prettier
./build
./publish
```

## Utilities

Sourcing **utilities.sh** will create functions in the shell that will create
or edit a blog post and launch the configured `$EDITOR`, as well as functions
to build and publish.