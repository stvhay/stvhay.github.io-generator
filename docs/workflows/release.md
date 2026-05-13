# Release: build and publish

How to get content from `main` of this repo to the live site at
<https://stevenhay.com/>.

## Two paths

| Path       | Trigger                             | Use when                                                                     |
| ---------- | ----------------------------------- | ---------------------------------------------------------------------------- |
| **CI**     | `git push origin main` to this repo | Default. Hands-off.                                                          |
| **Manual** | Run `./publish "<msg>"` locally     | CI is broken, or you want to inspect the generated diff before it goes live. |

## CI path (preferred)

1. Commit your changes locally on `main` (or merge a feature branch).
2. Push:
   ```bash
   git push origin main
   ```
3. Watch the workflow at
   <https://github.com/stvhay/website-hugo/actions/workflows/website.yml>.
4. On success, the workflow commits the generated `public/` and pushes
   to `stvhay/stvhay.github.io`. GitHub Pages serves the new content
   within a minute or two.

The workflow:

- Uses Nix with the Cachix binary cache (`stvhay-github-io`) so the
  toolchain doesn't recompile on every run.
- Uses SSH (`WEBSITE_SSH_KEY` secret) to push to the hosting repo.
- Runs `./build && htmltest && pytest`. **Any failure blocks
  publication.**

## Manual path

1. **Build and test locally**:

   ```bash
   nix develop --command bash -c './build && pytest tests/ -m "not external"'
   ```

2. **Review the staged diff in `public/`** (this is what will go live):

   ```bash
   git -C public diff --cached --stat
   git -C public diff --cached         # full diff if needed
   ```

3. **Publish**:

   ```bash
   ./publish "<commit message>"
   ```

   This commits and pushes both the source repo (this one) and the
   hosting repo (`public/`) with the same message. If there are no
   changes in one of them, it skips that one.

   If you want to publish without committing source changes, commit
   them separately first, then run `./publish` — it only pushes what
   already exists.

## Pre-flight checklist

Before either path:

- [ ] `pytest tests/ -m "not external"` is green.
- [ ] You ran `./build` and the output looks correct (PDFs in
      `public/docs/`, all pages present).
- [ ] No accidental commits of `public/` (it's gitignored, but check
      `git status` anyway).
- [ ] No secrets, emails, or API keys in the diff.
- [ ] If you added external links, htmltest passes locally.
- [ ] If you changed CSP, theme JS, or any template that renders
      user-visible content, you previewed in
      `hugo server -D` and checked the browser console for errors.

## Recovery

The hosting repo is just a normal git repo. If a bad commit went out:

```bash
git -C public log --oneline -5         # find the last-good SHA
git -C public reset --hard <good-sha>
git -C public push --force-with-lease  # only after confirming
```

Then fix the source, rebuild, and republish. Don't `--force` push to
the source repo on main without coordinating with anyone working in
parallel (only Steve, but still).
