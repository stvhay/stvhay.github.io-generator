---
target: rendered homepage
total_score: 21
max_score: 24
na_heuristics: 5,7,9,10
p0_count: 0
p1_count: 0
timestamp: 2026-07-24T02-39-10Z
slug: layouts-default-home-html
---
Method: dual-agent (A: openrouter-localish/google/gemma-4-31b-it · B: openai-codex/gpt-5.6-sol)

# Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Active navigation and focus are clear; card-level hover feedback overstates the actual clickable area. |
| 2 | Match System / Real World | 4 | Plain language and the notebook metaphor fit a personal research portfolio. |
| 3 | User Control and Freedom | 3 | The visible “CV” label does not disclose its PDF/new-tab behavior. |
| 4 | Consistency and Standards | 4 | Type, color, focus, card, image, and theme behavior are cohesive. |
| 5 | Error Prevention | n/a | The homepage has no data-entry or destructive workflow. |
| 6 | Recognition Rather Than Recall | 4 | Navigation, featured work, project titles, summaries, and thumbnails stay visible. |
| 7 | Flexibility and Efficiency | n/a | Not material to this Experience/portfolio surface. |
| 8 | Aesthetic and Minimalist Design | 3 | A shifted desktop axis, orphaned mobile nav row, and long undifferentiated project stack remain. |
| 9 | Error Recovery | n/a | The homepage has no error-producing workflow. |
| 10 | Help and Documentation | n/a | Not material to this Experience/portfolio surface. |
| **Total** | | **21/24** | **Good (87.5%)** |

# Design Specificity Verdict

**Clearly authored, with a few generic index behaviors left.** The rendered page strongly realizes “The Warm Research Notebook”: Source Serif 4, paper surfaces, flat structural borders, and one signal color feel coherent in both themes. The featured project creates a real point of view. The remaining generic behavior is interaction and flow rather than styling: most cards still carry equal weight, card chrome implies a larger hit target than exists, and the mobile navigation falls into an accidental 4+1 wrap.

**Deterministic/browser scan:** Desktop and mobile URL scans each returned one `single-font` warning at the document body. It is a false positive: Chromium measured a deliberate hierarchy spanning 40px/600 display, 24–20px/600 headings, 19.2px/300 body, 16px/600 navigation, and 13.6px/600 labels. The injected overlay also reported `cream-palette` as advisory; that is likewise intentional and pinned by the design authority.

**Visual overlay:** Browser rendering works. Chromium rendered desktop, mobile, light, and dark views with no console errors, page errors, or horizontal overflow. The site CSP correctly blocked the first localhost script injection; an isolated Puppeteer page with CSP bypass enabled loaded the detector successfully and captured `/tmp/website-hugo-detector-overlay-bypass.png`. The overlay was headless and is not a persistent Human tab.

# Overall Impression

The homepage now feels calm, personal, and credible. The featured project fixes the previous flat opening and gives the portfolio a peak. The biggest remaining opportunity is to align the interaction model with the visual model: make navigation and card affordances feel intentional at mobile sizes instead of merely responsive.

# What’s Working

1. **The visual world is specific.** Light and dark themes preserve the same paper-and-ink character rather than becoming two unrelated skins.
2. **The featured project creates hierarchy without decoration.** A larger image, larger title, and restrained label establish one entry point while keeping the flat notebook rule.
3. **Browser fundamentals are strong.** Chromium found zero horizontal overflow at 1440px and 390px; all nine images completed after scrolling; the first 12 keyboard targets matched `:focus-visible`; outlines measured 2px with 2px offsets in both themes.

# Cognitive Load

**Moderate: 2 of 8 checks fail.** Single focus, grouping, visual hierarchy, one-thing-at-a-time flow, working-memory support, and progressive disclosure pass. **Chunking** and **minimal choices** fail: the navigation exposes five options, and the portfolio remains one group of nine projects. The featured project reduces uncertainty but does not shorten the 5,297px mobile portfolio stack.

# Emotional Journey

The page opens with calm authority, reaches a clear peak at the featured prosopagnosia project, then settles into a long, even browsing plateau. The footer closes quietly and appropriately. On mobile, the emotional valley is duration: eight more full-width cards follow the featured project without a new chapter or stopping point.

# Priority Issues

## [P2] Mobile navigation wraps into an orphaned Contact row

- **Why it matters:** At 390px, Home, Portfolio, Writing, and CV occupy the first row while Contact sits alone 44px lower. The result looks accidental and consumes prime first-viewport space.
- **Fix:** Define an intentional narrow-screen navigation layout—either reduce only inter-item spacing enough to retain one row or use a balanced multi-column arrangement while preserving 44px targets.
- **Suggested command:** `/impeccable adapt`

## [P2] Desktop introduction and portfolio do not share an axis

- **Why it matters:** Chromium measured the introductory heading at x=380 and the portfolio heading/cards at x≈330. The 50px jump makes the transition feel assembled from two centered modules rather than one notebook page.
- **Fix:** Keep the 45rem prose measure but align its inner reading column to the 100ch index axis instead of centering the whole introductory section independently.
- **Suggested command:** `/impeccable layout`

## [P2] Card chrome implies a larger click target than exists

- **Why it matters:** The whole bordered card changes on hover, but only the title link is actionable. On the featured desktop card, the card spans 780×296px while its title link occupies roughly 425×64px. Users can tap the image or empty card surface and get no result.
- **Fix:** Either make the primary card surface genuinely actionable without breaking secondary links, or restrict hover emphasis to the actual linked title/image so the affordance stays honest.
- **Suggested command:** `/impeccable harden`

## [P2] The mobile portfolio remains a very long single chapter

- **Why it matters:** Nine full-width cards produce a 5,297px portfolio section at 390px. The featured entry helps orientation, but Casey still has no compact route through older projects.
- **Fix:** Keep the featured card, then introduce a factual second grouping, a compact standard-card mobile variant, or progressive disclosure for the remaining archive.
- **Suggested command:** `/impeccable shape`

## [P3] Visible CV copy still hides its behavior

- **Why it matters:** Assistive text announces “PDF, opens in a new tab,” but sighted users see only “CV.” The browser behavior can still surprise Jordan or Casey.
- **Fix:** Add a compact visible PDF cue without increasing the navigation’s mobile width enough to worsen wrapping.
- **Suggested command:** `/impeccable clarify`

# Persona Red Flags

**Jordan (First-Timer):** The featured project communicates purpose well. The main remaining ambiguity is interaction: bordered cards look broadly clickable, and “CV” does not visibly disclose the PDF/new-tab transition.

**Sam (Accessibility-Dependent):** Heading structure, focus visibility, contrast, touch targets, and decorative alternatives are strong. All tested keyboard targets displayed focus in both themes. The detector’s single-font warning does not represent an accessibility failure because size, weight, spacing, and hierarchy are distinct.

**Casey (Distracted Mobile User):** No overflow and 44px targets are strong. Contact falling onto its own navigation row and the 5,297px project stack make the first visit longer and less deliberate than the desktop experience.

# Minor Observations

- Explicit light and dark renders had matching structural hierarchy and no console errors.
- Lazy loading behaved correctly: only nearby images loaded initially, and all nine completed after browser scrolling.
- The featured label remains quiet at 13.6px/600 and does not compete with the title.
- The Impeccable overlay works in Chromium when CSP is bypassed for the isolated test page; the production CSP should remain unchanged.

# Questions to Consider

- Should the mobile homepage present the complete archive, or selected work followed by a compact route to everything else?
- Should cards behave like linked notebook entries, or like containers that merely hold several independent links?
- Is the 50px desktop axis shift intended to distinguish prose from index, or should the page read as one continuous notebook column?
