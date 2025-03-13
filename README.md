# stvhay.github.io-generator

I wanted to be able to write documents in LaTeX and Markdown and published easily into a website. This is the result.

- I've ported my web content to Markdown and used [Hugo](https://gohugo.io/) to generate a static website.
- LaTeX files are converted to .pdf with [pdfTeX](https://tug.org/applications/pdftex/).
- Hugo outputs to a git submodule *public*.
- I run [prettier](https://prettier.io) on the Hugo output for consistent formatting.
- The *public* submodule is linked to a [GitHub](https://github.com/stvhay/stvhay.github.io/) repository configured for static hosting [here](https://stevenhay.com).

## Build environment

```bash
repo="git_pages_repo"
apt install hugo texlive-latex-base
npm install --save-dev --save-exact prettier
if [[ -d .git ]] 
then
    git submodule add "$repo" public
else
    git clone "$repo" public
fi
./build.sh
./publish.sh
```