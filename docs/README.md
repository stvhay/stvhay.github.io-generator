# docs/

Repository documentation, primarily for agents working on the site but readable
by humans too. Living information about how this project is structured,
designed, and operated on lives here.

## Map

- **[ARCHITECTURE.md](ARCHITECTURE.md)** — repository layout, build pipeline,
  dual-repo deployment model, Hugo mounts, the three-category `static/`
  convention, and CI.
- **[DESIGN.md](DESIGN.md)** — visual and UX choices: theme system
  (light/dark/system), typography, CSS variable conventions, layout
  partials.
- **[workflows/](workflows/)** — task-oriented runbooks for recurring work:
  - [add-portfolio-item.md](workflows/add-portfolio-item.md)
  - [add-writing-post.md](workflows/add-writing-post.md)
  - [add-latex-doc.md](workflows/add-latex-doc.md)
  - [debug-htmltest.md](workflows/debug-htmltest.md)
  - [release.md](workflows/release.md)

## What's _not_ here

- Agent-specific prompting, coding standards, and process notes. Those live
  in a local-only `.claude/` (gitignored) and are not part of the
  committed project documentation.
- Subsystem deep-dives (e.g. email-scrambler internals, theme system
  invariants). These can be added under `docs/specs/` when a subsystem
  warrants it; otherwise the code is the source of truth.

## Note on the name

`docs/` (this directory) is project documentation for humans and agents.
`/docs/` on the live site (sourced from `latex/output/` via a Hugo mount —
see [ARCHITECTURE.md](ARCHITECTURE.md)) serves the compiled LaTeX PDFs
(CV, papers). The two are unrelated. The collision is documented but
not engineered around.
