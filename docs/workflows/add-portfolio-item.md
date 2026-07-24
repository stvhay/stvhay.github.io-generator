# Add a portfolio item

Each portfolio entry is a Hugo page bundle: a directory under
`content/portfolio/` containing `index.md` plus any media (thumbnails,
PDFs, embedded images).

## Steps

1. **Enter the nix shell** (or prefix each command with
   `nix develop --command`):

   ```bash
   nix develop
   ```

2. **Scaffold the bundle** using the project helper, which calls
   `hugo new content` and moves the result into a bundle directory:

   ```bash
   source utilities.sh
   post --page portfolio "My Project Title"
   ```

   This creates `content/portfolio/My Project Title/index.md` (with
   default front matter from `archetypes/`) and opens it in `$EDITOR`.

3. **Edit the front matter**:

   ```toml
   +++
   title = 'My Project Title'
   date = 2026-05-13T10:00:00-04:00
   draft = false
   description = 'One-sentence summary; surfaces in <meta description> and
                  OpenGraph tags.'
   [[resources]]
   src = 'img.jpg'
   [resources.params]
   alt = 'Concise description of the project image.'
   +++
   ```

4. **Add media** alongside `index.md`:

   ```
   content/portfolio/My Project Title/
   ├── index.md
   ├── img.jpg          # card/detail image matched by the resource metadata
   └── screenshot1.png  # referenced inline from markdown
   ```

   Reference inline media with relative paths: `![alt](screenshot1.png)`.

5. **Preview** locally with the dev server (live reload):

   ```bash
   hugo server -D
   ```

   Open <http://localhost:1313/portfolio/>.

6. **Build and test** before committing:

   ```bash
   ./build
   pytest tests/ -m "not external"
   ```

7. **Commit** atomically (content + media in one commit):
   ```bash
   git add "content/portfolio/My Project Title/"
   git commit -m "feat: add portfolio item — my project title"
   ```

## Conventions

- Directory name = `title` slug. Hugo derives the URL from the directory
  name; keep them aligned.
- Always include a `description`. Tests in
  `tests/test_content_requirements.py` enforce that every page has one
  (drives `<meta name="description">`, OpenGraph, Twitter Cards).
- Name the card/detail image `img.webp`, `img.png`, or `img.jpg`, and describe
  it with `resources.params.alt`. Listing cards treat repeated art as
  decorative; the detail page uses this description.
- Optimize source images before committing. Hugo generates responsive WebP
  sources plus a JPEG fallback at build time.

## Common pitfalls

- **Image not appearing in post-card**: check the `image` path is
  relative to the bundle dir, not absolute.
- **Page not building**: verify `draft = false` and that the date is
  in the past.
- **htmltest failing on internal links**: link targets in markdown must
  resolve to actual files. For another portfolio item, use
  `[link](../other-item/)`.
