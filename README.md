# stvhay.github.io-generator

I wanted to be able to write documents in LaTeX and Markdown and published easily into a website. This is the result.

- I've ported my web content to Markdown and used [Hugo](https://gohugo.io/) to generate a static website.
- LaTeX files are converted to .pdf with [pdfTeX](https://tug.org/applications/pdftex/).
- Hugo outputs to a git submodule *public*.
- I run [prettier](https://prettier.io) on the Hugo output for consistent formatting.
- The *public* submodule is linked to a [GitHub](https://github.com/stvhay/stvhay.github.io/) repository configured for static hosting [here](https://stevenhay.com).

## TODO

- Document how to setup the build environment.
- Make a **publish.sh** script that will automatically commit the changes in the submodule.