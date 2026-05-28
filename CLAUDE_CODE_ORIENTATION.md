# Claude Code — Session Orientation (Educator Portal Staging)

## Where the live work sits

The 8 educator section pages are deployed as **drafts** on the Shopify theme **"Educator Portal Staging (copy of live 2026-05-18)"** (theme ID 145914462378). **They are NOT in your GitHub repo.** The repo carries an earlier state; the staging theme carries the canonical, current build.

## What's live on staging (all noindex, all drafts)

| Section | URL handle | Page title |
|---|---|---|
| Catalog landing | `/pages/educators` | The Educator Catalog |
| Section 01 | `/pages/educator-sensory-play` | Sensory Play |
| Section 02 | `/pages/educator-nature-play` | Nature Play |
| Section 03 | `/pages/educator-woodland` | Woodland Habitats |
| Section 04 | `/pages/educator-small-world` | Small World & Storytelling |
| Section 05 | `/pages/educator-fairy-villages` | Fairy Villages |
| Section 06 | `/pages/educator-steam` | STEAM · Wonder & Investigation |
| Section 07 | `/pages/educator-dramatic-play` | Dramatic Play |
| Section 08 | `/pages/educator-creative-arts` | Creative Arts |
| Apply page | `/pages/educator-program` | Educator Program (public, indexed) |
| Dashboard | `/account/educator` | Educator Dashboard (Customer Account UI Extension) |

Each section page is deployed as its own Liquid template: `page.educator-{section}.liquid`.

## Chassis conventions (already baked in)

- **Asset paths**: Liquid `{{ 'filename.ext' | asset_url }}` for theme assets; `{{ 'filename.ext' | file_url }}` for Shopify Files
- **Robots**: All 8 section pages + dashboard carry `<meta name="robots" content="noindex,nofollow">`
- **Breadcrumbs**: Visible nav + schema.org `BreadcrumbList` JSON-LD on every section page (Home → Educator Catalog → Section XX · Name)
- **Section navigation**: Subnav with section stepper (Prev / Current / Next), auto-populated via `const CATALOG` JS const at bottom of each file
- **Type**: Cormorant Garamond (display) + Mulish (body)
- **Each section has its own palette token block** in `:root` — see `--accent`, `--accent-soft`, `--accent-pale`, `--accent-deep`, `--alt`, `--alt-deep`, `--hue-3`, `--hue-3-deep`, and `--mood-a` through `--mood-e`
- **Per-section type personality** in a CSS block labeled `/* Section XX, {Name} personality */`
- **Section dividers**: `.section-divider` numbered editorial transitions between major blocks
- **Pull-quotes**: `.pull-quote` blockquote between sections, catalog-sourced
- **Layout variants** for editorial rhythm:
  - `.split` (default), `.split.image-right`, `.split.stage` (full-bleed)
  - `.gallery` (hero+4), `.gallery.even` (5 equal columns), `.gallery.strip` (3 hero + 2 wide)
  - `.cap.expanded` for editorial hero cards (small accent rule + serif italic body)
- **Footer**: `© 2026 My Toy Wagon · Educator Catalog · All rights reserved`

## Current photo workflow

1. User uploads product photos to **Shopify Files** with clean filenames
2. User tells Claude Design the filenames
3. Claude Design wires `<img src="{{ 'filename' | file_url }}" alt="..." loading="lazy">` into the HTML source with descriptive alt text, adds `has-photo` class to the parent `.tile` (chassis hides the gradient + brief tags when `.has-photo` is present)
4. You redeploy the updated HTML to the staging theme
5. Photos render in theme editor preview

## What's done — Sensory Play (Section 01) photo wiring

19 photos wired with Liquid `file_url` references + descriptive alt text. The HTML file Claude Design serves replaces the current `page.educator-sensory-play.liquid`. After redeploy, all 19 render via Liquid → Shopify CDN.

One slot still open: **Editorial Intro lifestyle photo** — waiting for user to pick which lifestyle shot.

## What's done — All 8 sections (no photos yet)

All 8 section pages deployed to staging as drafts with chassis intact (palettes, breadcrumbs, type personalities, pull-quotes, section dividers, quote-only pricing where applicable). Photos still rendering as placeholder gradient tiles with text briefs in `[ ... ]` tags inside `<span class="tag">`.

## What's pending

- Sections 02–08 photo wiring (same workflow as Section 01 once filenames provided)
- Editorial Intro lifestyle photo on Section 01
- Photo replacement for Castle Tray (Sensory Play Gallery 1 — current photo will be swapped later)
- Creative Arts (Section 08) has 10 "SKU pending" cards — need real catalog verification before publish
- Three page-body items: educators@ plural → educator@ on Schools/Procurement/Vendor Profile (13×); Arcadia address → Los Angeles on Schools marketing page only; dead `href="#"` download buttons on procurement-guide
- Launch-gated: remove noindex + wire title/description/OG to Shopify Page metafields + add per-section og:image
- Launch-gated: B2B backend — Companies + Catalogs + Payment terms + Draft Order API for quote builder

## Catalog source of truth

`uploads/MTW_Catalog_SOURCE_v22r23.html` — all SKUs, product names, descriptions, and bundle compositions trace here. Do not invent products.

## Customer Account UI Extensions

- Apply form: `educator.html` → writes customer metafields `educator.application_status = pending`, staff flips to `verified` and sets `educator.terms` (net30/net60/prepaid)
- Dashboard: `educator-dashboard.html` → reads draft orders filtered by `customer.id` + custom metafield `draft_order.is_educator_quote = true`
- Quote builder: `new-quote.html` → posts to Admin GraphQL `draftOrderCreate` with line items, `appliedDiscount`, custom attributes `quote_name`, `for_program`, `needed_by`

## Outstanding repos vs theme

If at any point you reconcile your repo against staging, **staging is the source of truth**. The repo carries pre-photo, pre-palette-fix, pre-typography-personality state. Pulling repo over staging would lose work.
