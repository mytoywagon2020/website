# My Toy Wagon — Homepage Build Handover

Working theme: **"Current Shop with Updated Impulse (9.0)"** — UNPUBLISHED
(`gid://shopify/OnlineStoreTheme/145720180906`). Live store untouched.

Preview: https://mytoywagon.com?preview_theme_id=145720180906

## What's built (new namespaced sections, can't collide with Impulse)

Homepage order (top → down): `mtw_hero` → `mtw_educator` → `mtw_trust` →
`mtw_rail_new` → `mtw_rail_best` → `mtw_rail_gifts` → `mtw_rail_heirloom`
→ then the original Impulse sections (still in place below, to be
removed once the full homepage is rebuilt).

| Section file | Purpose | Content source |
|---|---|---|
| `sections/mtw-hero.liquid` | Split editorial hero | Section settings + Files image `hero-amber-kaleidoscope.webp` |
| `sections/mtw-educator-strip.liquid` | Slim educator callout | Section settings; CTA → `/pages/educator-register` |
| `sections/mtw-trust-strip.liquid` | 4 trust cards (blocks) | `trust-strip-*-mark.png` in Files |
| `sections/mtw-product-rail.liquid` | Reusable product row (used 4×) | Real Shopify collections |

Rail → collection mapping:
- 01 New → `whats-new` (102)
- 02 Best sellers → `best-sellers` (30)
- 03 Gifts under $50 → `50-and-under` (5977)
- 04 Heirloom favorites → `customer-favorites` (23) — **PLACEHOLDER, see below**

## OPEN ISSUES / FLAGS

### ⚠️ Heirloom collection (action needed)
There is **no dedicated "Heirloom favorites" collection** in the store.
The `mtw_rail_heirloom` section currently points at **`customer-favorites`**
as a stand-in so the rail isn't empty. This is not editorially correct —
"heirloom" should be hand-picked pieces meant to be passed down
(hand-carved, hand-stitched, keepsake-grade).

**To resolve:** create a curated collection (e.g. handle `heirloom-favorites`),
add the intended products, then in the theme editor set the
"04 / Heirloom favorites" section's Collection to it (or update
`mtw_rail_heirloom.settings.collection` in `templates/index.json`).

### Other notes
- **GitHub push blocked:** the Claude↔GitHub connection is read-only for
  this session; commits are local only. Fix: grant the Claude GitHub App
  **write** access to `mytoywagon2020/website`, then start a fresh Claude
  Code session — all commits push at once.
- **Collections are broad:** `50-and-under` (5977) and `whats-new` (102)
  show whatever's first in the collection. For the curated editorial feel
  of the design, consider tighter hand-picked collections per rail.
- **Hero image is low-res** (`hero-amber-kaleidoscope.webp`, 653×653) —
  may look soft on large screens. Swap a higher-res file via the theme
  editor (MTW Hero → Hero image) when available.
- **Address:** the homepage now says "Los Angeles, California"; the legal
  address in the educator/procurement docs is still Arcadia. Confirm
  which is intended where.
- **Product cards** link to the PDP; the design's quick-add / quick-view
  buttons are not yet wired (needs cart JS) — deferred.
- **Old Impulse homepage sections** remain below the new ones for now and
  should be removed/disabled once the homepage rebuild is complete.

## Safety / revert
`theme-snapshot/` holds the pristine pre-edit copies of
`templates/index.json`, `config/settings_data.json`,
`config/settings_schema.json`, `layout/theme.liquid`. Restoring any of
these to the theme reverts that file.
