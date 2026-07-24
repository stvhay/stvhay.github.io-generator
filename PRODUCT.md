# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The primary users are research collaborators, advisors, and technically curious peers who want to understand Steven Hay's transition into computational neuroscience. They need to assess his research direction, connect it to his engineering record, inspect the work behind the claims, and decide whether to read further, collaborate, or make contact.

## Product Purpose

Stevenhay.com establishes a credible line from two decades of complex-systems engineering to current work in computational neuroscience. It publishes projects, essays, technical documents, and learning in public.

Success means that a visitor can quickly understand this career arc, examine supporting work, find the writing, portfolio, or CV they need, and contact Steven without navigating a promotional funnel.

## Positioning

The site is an evidence-backed personal research notebook. It combines mature engineering practice, an active transition into computational neuroscience, original essays, runnable technical work, project narratives, and a detailed CV. This specific career history and body of work distinguish it from a generic portfolio or research profile.

## Operating Context

Visitors typically arrive at the homepage, read the concise positioning statement, inspect the featured project, and then browse portfolio work, essays, or the CV. Project pages link to source repositories, demonstrations, galleries, papers, and generated documents where those materials exist. The contact page supports research discussion, collaboration, and professional conversation.

The site also preserves work outside the central neuroscience direction, including open-source systems work, photography, digital music, and small software projects. This breadth supplies evidence of a long technical and creative practice rather than a separate product line.

## Capabilities and Constraints

- Hugo generates a static website from trusted Markdown, templates, page resources, and LaTeX sources.
- LaTeX documents may ship as PDFs and accessible HTML. Standalone demonstrations and archives remain part of the site when they provide real evidence of past work.
- Core reading and navigation work without JavaScript. JavaScript is limited to progressive enhancements such as theme selection and protected email reveal.
- The site has no account system, application backend, advertising, analytics, or behavioral tracking.
- A strict Content Security Policy, local assets, and privacy-light delivery are durable constraints.
- Steven is the sole author and source of product claims. Future work must preserve factual accuracy and must not invent testimonials, clients, publications, research results, or credentials.
- Static generation, responsive delivery, and straightforward deployment must remain more important than adding application infrastructure.

## Brand Commitments

The product name is **Steven Hay**, presented in Steven's direct first-person voice. The voice is thoughtful, technically precise, candid about learning, and willing to connect engineering, neuroscience, philosophy, and creative work.

Future work must preserve the site's breadth across neuroscience, systems engineering, machine learning, open source, photography, and music while keeping the present research direction clear. It must not recast active learning as settled expertise or turn the site into impersonal marketing copy.

## Evidence on Hand

- `content/about.md` states the current transition, research interests, and public-learning purpose.
- `latex/cv/cv-steve-hay.tex` documents education, engineering and research experience, presentations, technical skills, and specific professional results.
- `content/portfolio/using-augmented-reality-to-experience-prosopagnosia/` and `latex/experience-prosopagnosia/` provide a project narrative and technical papers on face-perception work.
- `content/portfolio/` contains project records spanning Linux and embedded systems, machine learning, data acquisition, photography, music, and software tools.
- `content/writing/` contains original long-form writing on computational neuroscience, perception, and philosophy.
- `static/plasma/` and `static/s3m/` contain runnable browser demonstrations; selected static archives preserve additional technical and research work.
- The repository contains no customer testimonials, sales case studies, pricing, or third-party endorsements. Future work must not fabricate them.

## Product Principles

1. **Show the work.** Support important claims with projects, documents, source links, demonstrations, or specific experience.
2. **Connect the disciplines.** Make the continuity between systems engineering and computational neuroscience easier to understand without erasing either field.
3. **Publish learning honestly.** Distinguish current study, exploratory work, and established expertise.
4. **Preserve useful breadth.** Keep technical and creative history available, but give the current research direction a clear path.
5. **Own the reading experience.** Prefer a fast, static, private, durable website over tracking, feeds, or application complexity.

## Accessibility & Inclusion

The site must support keyboard navigation, visible focus, semantic landmarks and headings, readable contrast, meaningful image alternatives, responsive layouts, and reduced-motion preferences. Core content must remain available without JavaScript. When a LaTeX document is published in both PDF and HTML, the HTML version provides a searchable and assistive-technology-friendly alternative.
