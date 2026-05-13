# Add a LaTeX document

LaTeX documents (CV, papers) are compiled to PDFs and served at
`/docs/<doc>/<doc>.pdf` on the live site. They use a content-hash cache
so unchanged sources are not recompiled.

## How it works

1. Source `.tex` files live under `latex/<doc>/`.
2. `latex/latex.manifest` enumerates which `.tex` files to build.
3. `./build` (`utilities/build.sh`) computes SHA-384 of each source and
   compares it against the `XMP-pdfx:texhash` metadata embedded in the
   existing PDF (recovered from the hosting repo's `main` branch).
4. If hashes differ: `latexmk` rebuilds the PDF, `exiftool` embeds the
   new hash in the metadata.
5. Built PDFs land in `latex/output/<doc>/<doc>.pdf` (gitignored). A
   Hugo `module.mounts` rule (see `hugo.toml`) maps that directory to
   `static/docs/`, so the PDF is served at URL
   `/docs/<doc>/<doc>.pdf`.
6. After Hugo runs, the build script removes the PDFs from
   `latex/output/` so the source tree stays clean. The PDFs in the
   hosting repo's `public/docs/` are what get committed and served.

## Steps to add a new document

1. **Create the source directory**:

   ```bash
   mkdir -p latex/my-paper
   ```

2. **Add the `.tex` file** (and any `.bib` files, `structure.tex`, etc.).
   Look at `latex/cv/` or `latex/experience-prosopagnosia/` for working
   examples.

3. **Register it in the manifest**:

   ```bash
   echo "my-paper/my-paper.tex" >> latex/latex.manifest
   ```

   Path is relative to `latex/`.

4. **Verify the local TeX Live coverage**. The Nix flake includes a
   curated set of packages (see `flake.nix`,
   `texlive.combine { ... }`). If your document uses a package not
   listed there, add it.

5. **Build**:

   ```bash
   nix develop --command ./build
   ```

   Expect to see `Building: my-paper/my-paper.tex` on first run,
   `Skipping: ... (unchanged)` on subsequent runs.

6. **Verify the PDF URL**:

   ```bash
   ls public/docs/my-paper/my-paper.pdf
   ```

   If present and non-empty, it will be served at
   `https://stevenhay.com/docs/my-paper/my-paper.pdf`.

7. **(Optional) Link from a menu**. To add to the top nav, edit
   `hugo.toml`:
   ```toml
   [[menus.main]]
   name = 'My Paper'
   url = '/docs/my-paper/my-paper.pdf'
   params = { target = "_blank" }
   weight = 220     # position relative to other menu items
   ```

## Cache invalidation

The hash cache lives in PDF metadata. To force a rebuild:

- Modify the source content (any byte change → new hash → rebuild).
- Or delete the PDF from `public/docs/` _and_ from the hosting repo's
  `main` branch before `./build`. The build's first step does
  `git -C public checkout main docs/...pdf`, which would otherwise
  restore the cached PDF.

## Common pitfalls

- **`latexmk` failure** stops the whole build. The full log is dumped
  to stderr. Check for missing packages first; add them to `flake.nix`.
- **PDF not appearing at `/docs/`**: confirm the entry in
  `latex.manifest` matches the `.tex` path exactly (no leading `./`,
  no extra whitespace). The build silently skips malformed entries.
- **Hash never matches → rebuilds every time**: usually means
  `exiftool` failed to write metadata. Check the build output for
  `markpdf` errors.
- **Changing the URL path** (renaming `latex/my-paper/`): updates the
  served URL too, which can break external links. Prefer keeping
  directory names stable once a paper is published.
