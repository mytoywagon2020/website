# Educator Portal — Claude Code Handover

> **Status:** 6 of 8 catalog pages live as hi-fi HTML prototypes.
> Cross-section editorial chassis is shared.
> Section pages drive off the same token system; per-section accents and personality CSS layer on top.

---

## What's built

### Live HTML files

| File | Target Shopify route | Type |
|---|---|---|
| `educators.html` | `/pages/educators` | Page (Liquid template) |
| `educator.html` | `/pages/educator-apply` | Page (Liquid template) |
| `Sensory Play v1.html` | `/pages/educator-sensory-play` | Page (Liquid template) |
| `Woodland v3.html` | `/pages/educator-woodland` | Page (Liquid template) |
| `Small World v2.html` | `/pages/educator-small-world` | Page (Liquid template) |
| `Fairy Villages v3.html` | `/pages/educator-fairy-villages` | Page (Liquid template) |
| `ordering-for-schools.html` | `/pages/schools` | Page (Liquid template) |
| `procurement-guide.html` | `/pages/procurement-guide` | Page (Liquid template) |
| `vendor-profile.html` | `/pages/vendor-profile` | Page (Liquid template) |
| `educator-dashboard.html` | `/account/educator` | Customer Account UI Extension |
| `new-quote.html` | `/account/quotes/new` | Customer Account UI Extension |

### Coming sections (placeholder cards in landing)

- Section 02 — Nature Play
- Section 06 — STEAM, Wonder & Investigation
- Section 07 — Dramatic Play
- Section 08 — Creative Arts

---

## Liquid token pattern

All `assets/X` paths have been rewritten to use the Shopify Liquid `asset_url` filter:

```html
<img src="{{ 'mtw-logo-full.png' | asset_url }}" alt="..."/>
```

This means the images need to be uploaded as **theme assets** (admin > themes > edit code > assets), not as **Shopify Files**. If you prefer Files, swap to:

```html
<img src="{{ 'mtw-logo-full.png' | file_url }}" alt="..."/>
```

---

## Editorial chassis

### Type system

- **Headings:** Cormorant Garamond (weights 300, 400, 500, 600)
- **Body:** Mulish (weights 300, 400, 500, 600, 700)
- **Hierarchy:** h1 `clamp(56px, 8vw, 112px)` italic, h2 `clamp(40px, 5vw, 60px)`, h3 `clamp(32px, 4vw, 52px)`
- **Body size:** 17px / 1.55 line-height
- **Letter-spacing:** -0.014em on h1, -0.008em on h2/h3

### Color tokens

```css
--cream: #F5F0E5;
--warm-white: #FFFCF7;
--ink: #2C2C2A;
--ink-soft: #44423E;
--stone: #5F5E5A;
--forest: #3B6D11;
--amber: #854F0B;
```

### Per-section accent (set in `:root` block)

| Section | Accent | Token suffix |
|---|---|---|
| 01 Sensory Play | `#3D7A6A` teal-green | --accent / --accent-soft / --accent-pale / --accent-deep |
| 02 Nature Play | `#6B8C3A` sage | (not built) |
| 03 Woodland Habitats | `#2D5C3A` forest | (live) |
| 04 Small World | `#7A5C8A` plum | (live) |
| 05 Fairy Villages | `#B86A7E` rose | (live) |
| 06 STEAM | `#9B7A3F` amber | (not built) |
| 07 Dramatic Play | `#8B6840` tan | (not built) |
| 08 Creative Arts | `#436F6F` teal-slate | (not built) |

### Custom CSS classes added

Beyond the brand chassis, these classes are reused across section pages:

- `.split` — featured-product layout (image-left + content-right default)
- `.split.image-right` — mirror split
- `.split.stage` — full-bleed image, content centered below
- `.gallery` — collection grid (default: hero+4 cell layout)
- `.gallery.even` — 5 equal columns
- `.gallery.strip` — 3 hero + 2 wide detail cells
- `.home` — product card inside a gallery
- `.cap` — caption block (name + desc + SKU + price + add-to-cart)
- `.cap.expanded` — caption with small accent rule + serif italic body for hero card emphasis
- `.cap.stripped` — caption with desc removed (currently unused, available for editorial picks)
- `.pull-quote` — large serif italic quote between sections (catalog-sourced)
- `.section-divider` — magazine-style numbered editorial divider
- `.standards-row` — CCSS/NGSS chips below the .craft block
- `.ships-separately-pill` — auto-injected by JS on cards tagged `data-long-lead="true"`
- `.kit` / `.kit.featured` — Outfit section cards
- `.qf-chip` — quote form filter chip

### Per-section type personalities (in addition to accent)

Each section page has a small CSS block that gives that page a distinct voice without breaking the chassis:

- **Sensory Play:** tighter headline tracking
- **Woodland:** wider vertical padding, regular weight headlines
- **Small World:** italic-forward descriptions, italic gallery names
- **Fairy Villages:** lighter weight headlines

---

## Cross-cutting components shared across all 6 live pages

| Block | Where it lives | Notes |
|---|---|---|
| Utility bar | top of every page | Phone + track order + apply/sign-in links |
| Nav (search + logo + dashboard/cart actions) | top of every page | Sticky, scrolls solid |
| Promo strip | below nav | "Fall booking" seasonal banner |
| Footer | bottom of every page | Identical across pages |
| Educator Hub Bridge | bottom of section pages, above footer | Single CTA back to `/pages/educators` |

The Reviews carousel, "How educator orders work" 3-step, and "Stay close to the seasons" Klaviyo signup were **moved off** the per-section pages to `/pages/educators` to avoid repetition.

---

## Klaviyo integration points

The Klaviyo signup on `/pages/educators` is the canonical educator letter signup. Replace `LIST_ID` with the actual Klaviyo list ID:

```html
<form action="https://manage.kmail-lists.com/subscriptions/subscribe" 
      method="POST" 
      data-form-id="LIST_ID">
  <input type="hidden" name="g" value="LIST_ID"/>
  ...
```

Reviews on `/pages/educators` are seed cards. When the Klaviyo Reviews program goes live, swap the static `.review` cards in `.rc-track` for the `<klaviyo-reviews>` web component, filtered to reviews tagged `audience=educator`.

---

## SKU conventions

All product SKUs follow:

```
MTW-[SECTION]-[PRODUCT]
```

Section codes:

- SP — Sensory Play
- NP — Nature Play (Tender Leaf, etc.)
- WD — Woodland (Bumbu)
- SW — Small World (Tara Treasures, Papoose, Himalayan Felt Co.)
- FV — Fairy Villages (Tara Treasures fairy homes, Wonderheart, Bumbu)
- ST — STEAM
- DP — Dramatic Play
- CA — Creative Arts (also Análu therapy dough)

Note: Análu Therapy Dough (MTW-CA-*) is **brand-cross-listed** in §01 Sensory Play per the catalog source. Tender Leaf My Forest Floor (MTW-NP-TLF) is **brand-cross-listed** in §01 Sensory Play. Both are flagged in HTML comments on the relevant cards.

---

## Catalog sets (bundles)

Each section page has an "Outfit your classroom" block at the bottom listing the catalog-sourced bundles, like:

| Section | Catalog set SKU | Title |
|---|---|---|
| 01 Sensory | MTW-SP-BTR | The Tray Range |
| 01 Sensory | MTW-SP-CRS | The Self-Regulation Set |
| 01 Sensory | MTW-CA-ANS | The Seven Scents Set |
| 03 Woodland | MTW-WD-WFS | The Woodland Family Set |
| 03 Woodland | MTW-WD-FFS | The Woodland Tree Set |
| 04 Small World | MTW-SW-FB5 | The Complete Felt Habitats |
| 04 Small World | MTW-SW-NWS | The Natural World Set |
| 04 Small World | MTW-SW-SSS | The Songs & Stories Set |
| 05 Fairy Villages | MTW-FV-VLG | Build the Village |

Below the catalog sets, each section also has an "Educator Combo" strip describing a custom bundle that's NOT a SKU — it's a quote-only PO combo with a small package discount.

---

## JS components

Each live page includes inline JS for:

1. **Nav scroll detection** — adds `.scrolled` class after 60px scroll
2. **Cart count badge** — increments on .add-btn click (replace with real Shopify cart on port)
3. **Utility-bar rotating announcement** — 3 messages, 5s cycle
4. **Section stepper auto-population** — reads `const CATALOG` for current section
5. **`data-long-lead` pill injection** — auto-tags cards with "Ships separately"
6. **Reviews carousel** (educators.html only) — snap-scroll, dots, prev/next

---

## Known bugs / TODOs

1. OG image files referenced but don't exist yet: `og-educators.jpg`, `og-sensory-play.jpg`, `og-woodland.jpg`, `og-small-world.jpg`, `og-fairy-villages.jpg`. Either create them or remove the OG references.
2. Long-lead item list (Magic Wood, Drewart, select Bumbu sets) is in the footnote but no specific products are tagged with `data-long-lead="true"` yet.
3. `.cap.stripped` class exists but is unused. Available for editorial picks.
4. The `direction: rtl` workaround for `.split.image-right` was replaced with `order:` grid rules. The leftover `.split.image-right > * { direction: ltr }` may still exist in some files (remove if found).
5. CSS file is sprawling (~25 custom classes on top of chassis). Future edits should consolidate.

---

## Per-section pre-mortem notes (carried forward)

- **Layout alternation** uses 3 split variants (default/image-right/stage) and 3 gallery variants (default/even/strip), applied by content type (equal-weight collection → `.even`; content with editorial anchor → default).
- **Pull-quotes** are 100% catalog-sourced (pages 6, 12, 18, 23, 31).
- **Section dividers** are numbered editorial moments before each major block. Have a mobile fallback.
- **Per-section type personalities** are subtle. Test live, may need to amplify.
- **No visual verification** has been done. Builder should screenshot at desktop + mobile, validate the rotation rhythm.

---

## Next sections to build

In the same pattern as the 4 live sections:

1. **Section 02 Nature Play** — Tender Leaf, Gus + Mabel Busy Bee Tray, Papoose, Wild Mountain Child. Catalog pp. 13–17.
2. **Section 06 STEAM** — Amber Kaleidoscopes, Connetix, Bauspiel, Q Toys Microscope, June & December. Catalog pp. 34–37.
3. **Section 07 Dramatic Play** — Drewart Cow Shed, Tara Treasures harvest/market/food. Catalog pp. 38–47 (10 pages, largest section).
4. **Section 08 Creative Arts** — Q Toys Weaving, June & December Heirloom Press, Eco-Cutters, Felt Florals. Catalog pp. 48–50.

Each new section needs:

1. Clone the closest existing live section page
2. Swap the `:root` ECOSYSTEM PALETTE block (5 token colors + 5 mood gradient)
3. Rewrite cover, intro, hero, galleries, outfit per catalog content
4. Update the `CATALOG` JS constant at the bottom
5. Add per-section type personality CSS overrides at the end of `<style>`
6. Apply `.cap.expanded` to 1-2 editorial hero cards per gallery
7. Add a section-themed pull-quote (catalog-sourced)
8. Wire the section's Vol card on `/pages/educators` to its new page

---

## Catalog source of truth

`uploads/MTW_Catalog_SOURCE_v22r23.html` is the canonical content source. All product names, prices, descriptions, scenarios, SKUs, set names, testimonials, and pull-quotes should be drawn from there. Do not invent products.

The catalog page numbers and section start/end points are in the comments at the top of each `<section class="page eco-X">` block.
