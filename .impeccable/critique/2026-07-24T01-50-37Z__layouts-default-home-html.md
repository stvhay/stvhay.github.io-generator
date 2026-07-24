---
target: homepage
total_score: 21
max_score: 24
na_heuristics: 5,7,9,10
p0_count: 0
p1_count: 0
timestamp: 2026-07-24T01-50-37Z
slug: layouts-default-home-html
---
Method: dual-agent (A: openrouter-localish/google/gemma-4-31b-it · B: openrouter-localish/deepseek/deepseek-v4-flash)

# Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Current navigation, focus, and theme state are clear; this static surface needs little process feedback. |
| 2 | Match System / Real World | 4 | Plain labels and the notebook metaphor match a personal research portfolio. |
| 3 | User Control and Freedom | 3 | Navigation is predictable, but “CV” does not disclose that it opens a PDF in a new tab. |
| 4 | Consistency and Standards | 4 | Type, color, focus, card, and theme patterns are cohesive. |
| 5 | Error Prevention | n/a | The homepage has no data-entry or destructive workflow. |
| 6 | Recognition Rather Than Recall | 4 | Text navigation, project names, summaries, and thumbnails keep choices visible. |
| 7 | Flexibility and Efficiency | n/a | Not material to this Experience/portfolio surface. |
| 8 | Aesthetic and Minimalist Design | 3 | Repeated “(portfolio)” marks and nine equal-weight cards add avoidable visual sameness. |
| 9 | Error Recovery | n/a | The homepage has no error-producing workflow. |
| 10 | Help and Documentation | n/a | Not material to this Experience/portfolio surface. |
| **Total** | | **21/24** | **Good (87.5%)** |

# Design Specificity Verdict

**Specific visual identity, generic portfolio composition.** Assessment A found a strong authored world: Source Serif 4, warm paper surfaces, one signal color, flat borders, and restrained interaction all belong to “The Warm Research Notebook.” The remaining sameness is structural: nine image-left cards receive identical weight, so the page does not yet reveal which work best represents the current research trajectory.

**Deterministic scan:** zero findings (`[]`, exit 0) across `layouts/` and `public/index.html`. The scan confirms a clean mechanical floor but does not catch the missing portfolio section heading, wide introductory measure, repeated metadata, or flat project hierarchy.

**Visual overlays:** none. This harness exposes no browser automation, Playwright/Puppeteer package, or Chromium/Firefox executable, so no screenshot, injection, console evidence, or user-visible overlay is available.

# Overall Impression

Calm, credible, and unusually coherent for a personal site. The typography and paper palette feel authored; the homepage information architecture does not yet match that level of specificity. The biggest opportunity is to turn the project list from a uniform archive into a clear statement of present direction.

# What’s Working

1. **The visual world is coherent.** `DESIGN.md` and `assets/css/main.css` agree on family, weight, paper tones, border-defined depth, and one accent per theme.
2. **Reading and interaction foundations are strong.** Fluid balanced display type, visible focus, a skip link, reduced-motion support, 44px navigation targets, and responsive intrinsic images support varied users without visual noise.
3. **Cards scan well.** The `150px 1fr` desktop rhythm and one-column mobile collapse make nine different projects easy to browse.

# Cognitive Load

**Moderate: 2 of 8 checks fail.** Single focus, grouping, hierarchy, one-thing-at-a-time flow, working-memory support, and progressive disclosure pass. **Chunking** and **minimal choices** fail: the navigation exposes five options and the portfolio exposes nine equal-weight project choices with no grouping or featured path.

# Emotional Journey

The warm masthead and personal introduction create a calm entry. The emotional peak arrives immediately, then flattens into nine visually equivalent cards. The footer closes quietly and appropriately. A featured current thread or clearer project grouping would give exploration a second peak without adding decoration.

# Priority Issues

## [P2] The homepage headline says only “Welcome”

- **Why it matters:** The strongest heading does not identify the work, discipline, or reason to continue. Jordan must read the paragraph before understanding the site’s value.
- **Fix:** Replace the generic title with a factual positioning line drawn from existing copy or site metadata; keep the personal introduction beneath it.
- **Suggested command:** `/impeccable clarify`

## [P2] The portfolio section has no heading

- **Why it matters:** `layouts/_default/home.html` moves directly from introductory prose into nine card-level `<h2>` elements. Visual and screen-reader users receive no explicit transition into the project collection.
- **Fix:** Add a visible section heading such as the existing “Portfolio” label and connect the section with `aria-labelledby` if needed.
- **Suggested command:** `/impeccable harden`

## [P2] Nine projects have identical visual priority

- **Why it matters:** Equal cards make the archive easy to scan but hide the current research narrative. Visitors cannot distinguish signature work, current direction, and older experiments without opening several pages.
- **Fix:** Feature one or two representative projects or group the list by a factual theme or period. Preserve the notebook restraint; change hierarchy, not decoration.
- **Suggested command:** `/impeccable shape`

## [P2] Introductory prose violates the documented reading measure

- **Why it matters:** `#home.container` uses `max-width: 100ch`, while the design system reserves that width for indexes and caps prose near `45rem`. The short copy remains usable, but the inconsistency weakens reading rhythm on wide displays.
- **Fix:** Constrain only the introductory copy to the article measure; leave the project index wide.
- **Suggested command:** `/impeccable layout`

## [P3] Repeated “(portfolio)” marks add no information

- **Why it matters:** All nine homepage cards repeat the same `.section-mark`, producing visual noise without helping orientation.
- **Fix:** Hide the mark when the surrounding section already supplies the category, or replace it only when meaningful metadata exists.
- **Suggested command:** `/impeccable distill`

# Persona Red Flags

**Jordan (First-Timer):** “Welcome” does not state the site’s purpose; the unheaded transition into nine projects makes the first decision ambiguous; “CV” does not disclose that it opens a PDF in a new tab.

**Sam (Accessibility-Dependent):** Skip navigation, focus states, semantic card articles, and decorative thumbnail alternatives are strong. The missing portfolio heading weakens heading navigation. Outside this homepage target, `.reveal-email-button` lacks its own `:focus-visible` rule.

**Casey (Distracted Mobile User):** Touch targets, lazy responsive images, and the single-column collapse are strong. Nine full-width cards create a long undifferentiated scroll, with no “selected work” path for a quick visit.

# Minor Observations

- The current-page link correctly uses both `.active` and `aria-current="page"`.
- Responsive card thumbnails reserve dimensions, lazy-load, and provide WebP plus JPEG fallback.
- The sticky navigation’s fade is subtle and consistent with the paper world.
- The CV link should expose its PDF/new-tab behavior in visible or assistive copy.

# Questions to Consider

- Which two projects best prove the work Steven wants to do next?
- Should the first heading welcome visitors, or position the research practice?
- What would make the project sequence feel like a research notebook rather than a generic portfolio archive?
