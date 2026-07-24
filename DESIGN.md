---
name: Steven Hay
description: A warm, paper-like research notebook for projects and public learning.
colors:
  warm-paper: "#faf7f2"
  quiet-paper: "#f2efe9"
  ink: "#1a1a1a"
  graphite: "#4a4a4a"
  signal-blue: "#0069d9"
  deep-signal-blue: "#0056b3"
  soft-white: "#e0e0e0"
  pure-white: "#ffffff"
  carbon: "#121212"
  night-chrome: "#1f1f1f"
  night-paper: "#222222"
  soft-ash: "#cccccc"
  reading-gold: "#e0d890"
  bright-reading-gold: "#f9ff99"
  night-structure: "#444444"
  night-structure-hover: "#888888"
  night-control-hover: "#666666"
typography:
  display:
    fontFamily: '"Source Serif 4", serif'
    fontSize: "clamp(2rem, 1.75rem + 1.25vw, 2.5rem)"
    fontWeight: 600
    lineHeight: 1.15
  headline:
    fontFamily: '"Source Serif 4", serif'
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.25
  title:
    fontFamily: '"Source Serif 4", serif'
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.3
  minor:
    fontFamily: '"Source Serif 4", serif'
    fontSize: "1.2rem"
    fontWeight: 600
    lineHeight: 1.35
  body:
    fontFamily: '"Source Serif 4", serif'
    fontSize: "1.2rem"
    fontWeight: 300
    lineHeight: 1.5
  nav:
    fontFamily: '"Source Serif 4", serif'
    fontSize: "1rem"
    fontWeight: 600
    lineHeight: 1.5
  metadata:
    fontFamily: '"Source Serif 4", serif'
    fontSize: "0.9rem"
    fontWeight: 300
    lineHeight: 1.5
  label:
    fontFamily: '"Source Serif 4", serif'
    fontSize: "0.85rem"
    fontWeight: 300
    lineHeight: 1.5
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  none: "0"
  sm: "4px"
  md: "8px"
spacing:
  xs: "0.5rem"
  sm: "0.625rem"
  md: "1rem"
  lg: "1.25rem"
  xl: "1.5rem"
  2xl: "1.875rem"
  3xl: "2rem"
components:
  button-primary:
    backgroundColor: "{colors.signal-blue}"
    textColor: "{colors.pure-white}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "{spacing.xs} 0.75rem"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.deep-signal-blue}"
    textColor: "{colors.pure-white}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "{spacing.xs} 0.75rem"
    height: "44px"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.75rem {spacing.md}"
    height: "44px"
  nav-link:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    typography: "{typography.nav}"
    rounded: "{rounded.none}"
    padding: "{spacing.xs} 0.75rem"
    height: "44px"
  card:
    backgroundColor: "{colors.quiet-paper}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
---

# Design System: Steven Hay

## Overview

**Creative North Star: "The Warm Research Notebook"**

The site should feel like opening a careful research notebook: warm, legible, personal, and quietly technical. Source Serif 4 gives ideas the authority of print without making the portfolio feel ceremonial. Paper-toned surfaces, light rules, and generous reading space let projects and writing carry the page.

The system is deliberately restrained. A single signal color handles navigation, links, focus, and action in the light theme; a warm reading glow takes that role at night. Components are structurally explicit and quietly tactile rather than glossy, ornamental, or application-like.

**Key Characteristics:**

- Warm paper surfaces with ink-like serif typography.
- One scarce signal color per theme.
- Flat, border-defined depth with no shadows.
- Comfortable prose measures and compact, scannable indexes.
- Motion limited to state communication and disabled for reduced-motion users.
- Light, dark, and system-following themes with equal visual authority.

## Colors

The palette is **Paper, Ink & Signal**: warm neutrals carry the reading surface, while one high-contrast accent marks interaction and orientation.

### Primary

- **Signal Blue** (`#0069d9`): light-theme links, focus rings, card emphasis, and primary actions.
- **Deep Signal Blue** (`#0056b3`): light-theme hover and active emphasis.

### Secondary

- **Reading Gold** (`#e0d890`): dark-theme links and focus treatment; warm enough to preserve the notebook character against Carbon.
- **Bright Reading Gold** (`#f9ff99`): dark-theme hover emphasis.

### Neutral

- **Warm Paper** (`#faf7f2`): the light-theme page and inset code surface.
- **Quiet Paper** (`#f2efe9`): light-theme cards, masthead, navigation, footer, and raised accessibility affordances.
- **Ink** (`#1a1a1a`): primary light-theme text.
- **Graphite** (`#4a4a4a`): light-theme metadata, quotations, and secondary copy.
- **Soft White** (`#e0e0e0`): dark-theme primary text and the light-theme hairline.
- **Pure White** (`#ffffff`): primary button text in the light theme.
- **Carbon** (`#121212`): dark-theme page surface.
- **Night Chrome** (`#1f1f1f`): dark masthead, navigation, and footer.
- **Night Paper** (`#222222`): dark cards.
- **Soft Ash** (`#cccccc`): dark secondary text.
- **Night Structure** (`#444444`): dark borders and primary control fill.
- **Night Structure Hover** (`#888888`): dark card-border emphasis.
- **Night Control Hover** (`#666666`): dark control hover fill.

**The One Signal Rule.** Use Signal Blue in light mode and Reading Gold in dark mode for links, focus, and action. Do not introduce a competing accent.

**The Paired Theme Rule.** Every semantic color change must be defined for the light default, system-dark mode, and explicit dark override. An explicit light choice continues to inherit the light default.

## Typography

**Display Font:** Source Serif 4, with the generic serif fallback.

**Body Font:** Source Serif 4, with the generic serif fallback.

**Label/Mono Font:** Source Serif 4 for controls; the platform monospace stack for code and the revealed-email treatment.

**Character:** One variable serif family keeps the site cohesive across personal writing, research notes, and project indexes. Light body weight gives the page air; semibold headings and navigation add structure without shifting into a separate display voice.

### Hierarchy

- **Display** (600, `clamp(2rem, 1.75rem + 1.25vw, 2.5rem)`, 1.15): balanced site and page titles that tighten on narrow screens.
- **Headline** (600, `1.5rem`, 1.25): major section headings.
- **Title** (600, `1.25rem`, 1.3): card titles and compact content headings.
- **Minor Heading** (600, `1.2rem`, 1.35): lower-level headings that must not render smaller than the body copy they introduce.
- **Body** (300, `1.2rem`, 1.5): prose, summaries, and article copy; long-form articles stop at `45rem`, approximately 70–75 characters.
- **Navigation** (600, `1rem`, 1.5): sticky index links and current-location states.
- **Metadata** (300, `0.9rem`, 1.5): dates, section marks, and footer copy.
- **Label** (300, `0.85rem`, 1.5): compact controls and footer actions.
- **Code** (platform monospace, `0.9em` inline / `0.95rem` block, 1.5): technical notation and examples.

Source Serif 4 is served locally as Latin-subset regular and italic variable WOFF2 files covering weights 100–900. The primary site and generated LaTeXML documents share these files. Use weight 600, not 700, for bold text. Keep `font-display: swap` so fallback text appears immediately.

**The Single Voice Rule.** Use weight, size, spacing, and italics to create hierarchy before introducing another typeface.

## Layout

The global `.container` is centered and capped at `100ch`; it creates a generous index canvas rather than a full-bleed application shell. Sections use `1.875rem 1.25rem` padding, and containers add `1.25rem` internal padding. Long-form `.article` content narrows to `45rem` and permits long technical strings to wrap rather than widen the viewport.

Portfolio and writing cards use a `150px 1fr` grid with a `1.25rem` gutter. At `768px` and below, cards become a single column, floated article media becomes full width, and text remains left aligned. Navigation wraps, stays sticky, and preserves 44px minimum targets. Responsive images retain intrinsic dimensions and use Hugo-generated WebP sources with JPEG fallbacks.

**The Reading Measure Rule.** Indexes may use the full `100ch` container; prose must use the narrower `45rem` article measure.

**The Content-First Collapse Rule.** At narrow widths, remove floats and side-by-side card geometry before reducing readable type or touch targets.

## Elevation & Depth

The notebook is flat by design. It uses no box shadows. Quiet Paper against Warm Paper, Night Paper against Carbon, one-pixel borders, and accent-colored interaction states provide enough separation without making content look like floating application chrome.

**The Flat Notebook Rule.** Depth comes from tonal surfaces and structural borders. Do not add ambient shadows to cards, navigation, controls, or article media.

## Shapes

Corners are gently curved, never pill-like. Cards and media use the medium radius (`8px`); compact action controls and code use the small radius (`4px`). Navigation links and the theme toggle remain square so the masthead reads as an index rather than a toolbar.

Borders are thin and functional. A one-pixel rule defines cards, code, tables, and controls; a three-pixel accent rule identifies quotations. Focus uses a two-pixel accent outline with a two-pixel offset and must remain visually independent from borders.

**The Quiet Corner Rule.** Use `8px` for content containers, `4px` for compact controls, and no radius for text navigation. Never use pills as decoration.

## Components

Components are restrained and quietly tactile: their default state recedes, while hover, focus, and active states make structure unmistakable.

### Buttons

- **Primary:** Signal Blue fill, Pure White text, one-pixel matching border, small corners (`4px`), and at least a 44px target. In dark mode, use Night Structure with Soft White text.
- **Hover:** deepen Signal Blue in the light theme; use Night Control Hover in the dark theme; underline text when the control behaves like a disclosure or reveal.
- **Focus:** preserve the two-pixel accent outline and two-pixel offset.
- **Ghost:** the theme toggle has no fill or border. It reveals its underline on hover and retains the same minimum target.
- **Disabled:** reduce opacity and use a not-allowed cursor without removing the label.

### Cards / Containers

- **Corner Style:** gently curved (`8px`).
- **Background:** Quiet Paper in light mode; Night Paper in dark mode.
- **Shadow Strategy:** none; see the Flat Notebook Rule.
- **Border:** one-pixel semantic border that changes to the active theme emphasis on hover or focus-within.
- **Internal Padding:** `1.25rem` for standard post cards and `2rem` for article cards.
- **Focus:** focus-within adds both the emphasized border and an external focus outline.

Post-card thumbnails are decorative because the adjacent heading names the destination. Detail-page content images carry meaningful alternatives from Hugo page-resource metadata.

### Navigation

The masthead title is a semibold display link. The primary navigation is centered, sticky, wrapping, and built from minimum-44px text links. Hover underlines and shifts to the theme's stronger accent. The current page or ancestor uses a two-pixel underline offset by `0.4em`; do not replace this with a filled tab.

### Code, Tables, and Quotations

Inline code and code blocks use Warm Paper inside light cards, with a thin border and small or medium corners. Wide code and tables scroll within their own box rather than widening the page. Blockquotes use Graphite italic text and a three-pixel Signal Blue rule; this is semantic annotation, not card decoration.

### Generated Documents

LaTeXML documents use the same Source Serif 4, body weight, heading scale, paper surfaces, and print-minded restraint through `static/css/latexml/site.css`. Keep `LaTeXML.css` and `ltx-article.css` unmodified so upstream replacements remain possible. Generated documents carry no JavaScript, follow system color preference only, and use an ink-friendly print layer.

### Theme Behavior

The absent `data-theme` state follows `prefers-color-scheme`; `data-theme="light"` and `data-theme="dark"` force an override. `static/js/theme-init.js` applies a saved preference before paint. `static/js/theme-toggle.js` persists only an override and returns to system-following behavior when the selected theme matches the operating system.

## Do's and Don'ts

### Do:

- **Do** use semantic CSS variables for every themed color and update the light default, system-dark declaration, and explicit dark declaration together.
- **Do** keep Source Serif 4 local, variable, Latin-subset, and loaded with `font-display: swap`.
- **Do** preserve 44px interaction targets and visible `:focus-visible` outlines.
- **Do** keep article prose near 70–75 characters and let indexes use the wider grid.
- **Do** use responsive Hugo page resources with intrinsic dimensions, WebP sources, and JPEG fallbacks.
- **Do** honor `prefers-reduced-motion` and preserve core reading access without JavaScript.

### Don't:

- **Don't** hard-code themed colors in component rules; use the established semantic variables.
- **Don't** add shadows, glossy gradients, decorative pills, or extra accent colors.
- **Don't** remove focus indicators, shrink touch targets, or communicate state through color alone.
- **Don't** use inline scripts or inline styles in Hugo templates; the strict CSP requires external scripts and class-based styling.
- **Don't** edit vendored LaTeXML stylesheets for site-specific changes; use `static/css/latexml/site.css`.
- **Don't** repeat nearby link text in thumbnail alternatives; decorative card thumbnails use empty alt text, while meaningful article images use page-resource metadata.
