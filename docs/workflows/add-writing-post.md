# Add a writing post

Blog posts live as page bundles under `content/writing/`. They get
Article JSON-LD structured data and appear in the RSS feed.

## Steps

1. **Scaffold**:

   ```bash
   nix develop
   source utilities.sh
   post "My Post Title"          # defaults to --page writing
   ```

   Creates `content/writing/My Post Title/index.md`.

2. **Front matter**:

   ```toml
   +++
   title = 'My Post Title'
   date = 2026-05-13T10:00:00-04:00
   publishDate = 2026-05-13T10:00:00-04:00
   lastmod = 2026-05-13T10:00:00-04:00
   draft = false
   description = 'Required: surfaces in meta description, OG, and twitter card.'
   author = 'Steven Hay'          # optional; falls back to site.Params.author
   image = 'hero.jpg'             # optional; enables large twitter card
   +++
   ```

   `publishDate` and `lastmod` populate `article:published_time` /
   `article:modified_time` in OpenGraph and `datePublished` /
   `dateModified` in the Article JSON-LD. Keep them current.

3. **Write the post** in markdown. Use the project's shortcodes for
   custom HTML — don't enable `unsafe = true` in config.
   - Email obfuscation: `{{< scrambled-email "user@example.com" >}}`
     (see `layouts/shortcodes/scrambled-email.html`).
   - Inline images: place files in the bundle dir,
     `![alt text](filename.png)`.
   - External links: any `http(s)://` link not under `site.BaseURL` is
     automatically given `target="_blank" rel="noopener noreferrer"` by
     the render hook at `layouts/_default/_markup/render-link.html`.
   - Force-open-in-new-tab for internal links: prefix the URL with `_`
     (the render hook strips it and adds `target="_blank"`).

4. **Preview**:

   ```bash
   hugo server -D
   ```

   Open <http://localhost:1313/writing/>.

5. **Validate structured data**:

   ```bash
   ./build
   pytest tests/ -m structured_data
   ```

   The Article schema is generated automatically — no manual JSON-LD
   needed. The test asserts every writing post emits valid Article JSON-LD.

6. **Full test pass** before commit:
   ```bash
   pytest tests/ -m "not external"
   ```

## Conventions

- Use the bundle form (directory with `index.md`), not a single
  `.md` file, even for image-less posts. Keeps the option open to add
  assets later without restructuring.
- Always set `description`. The home page and listing pages use it as
  the summary if present; otherwise Hugo falls back to `.Summary`.
- Don't write inline `<script>` or `style="..."` — CSP forbids it.
  Add CSS rules to `assets/css/main.css` and JS files to `static/js/`.

## Common pitfalls

- **Post not visible on `/writing/`**: check `draft = false` and that
  `date`/`publishDate` is not in the future.
- **htmltest failing on external URL**: some external sites block bots
  (DOI, WorldCat, etc.). If the URL works in a browser, add it to
  `IgnoreURLs` in `.htmltest.yml` rather than removing the link.
- **Structured-data test failing**: missing `description` is the most
  common cause. The Article JSON-LD requires it (falls back to
  `.Summary` only when nothing else is available).
