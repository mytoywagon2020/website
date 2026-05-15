# Handoff: My Toy Wagon Retail Storefront

The retail (DTC) side of My Toy Wagon — a family-run heirloom toy shop in Arcadia, California. This bundle covers the public homepage, product pages, brand pages, blog, and all policy pages.

For the educator portal / B2B side, see the separate `design_handoff_educator_portal` package.

---

## About the Design Files

The files in `designs/` are **design references created in HTML.** They are prototypes showing intended look and behavior — not production code to ship directly. Your task is to **recreate these designs in the My Toy Wagon Shopify store** using the existing **Impulse theme** as the starting point, with custom Liquid sections to match the editorial layout.

Designs are **high-fidelity** — pixel-perfect with final typography, color, spacing, and copy. Treat the spec below as authoritative.

---

## Pages in this bundle

| File | Shopify mapping |
|---|---|
| `MTW Homepage v3.html` | Home (`templates/index.json`) |
| `product-coralwhim-cove.html` | Standard product page (`templates/product.liquid`) — ships from LA warehouse |
| `product-drewart-camper-preorder.html` | Pre-order product variant — "Pre-order, ships [date]" badge |
| `product-garden-of-the-moon.html` | Partner-warehouse variant — "Ships from partner warehouse" badge |
| `catalog.html` | Long-scroll seasonal catalog (`templates/page.catalog.liquid`) |
| `our-story.html` | Founder narrative (`templates/page.our-story.liquid`) |
| `tara-treasures.html` | Maker spotlight page template (`templates/page.maker.liquid`) |
| `rewards.html` | Loyalty / rewards landing |
| `wishlist.html` | Wishlist landing (gated to signed-in customers) |
| `shipping.html`, `returns.html`, `privacy.html`, `terms.html`, `accessibility.html`, `faq.html` | Policy pages (`templates/page.policy.liquid`) |
| `collaboration.html` | Brand partnership inquiry page |
| `school-affiliate.html` | Affiliate program for schools |
| `blog/whats-arrived-gus-and-mabel.html` | Sample blog article — defines the article template |
| `collection-tara-treasures.html` | Collection page template (`templates/collection.liquid`) — use as the pattern for all 9 collections. Hero + sticky filter bar + faceted sidebar (Category, Age, Approach, Price, Availability) + 3-col product grid with hover-swap secondary image, wishlist heart, Add-to-cart reveal, low-stock badge + pagination |

---

## Homepage structure (top to bottom)

1. **Top utility bar** — ink-on-cream announcement strip (currently pre-order announcement for Tiny Fox Hole)
2. **Free shipping progress bar** — cream-beige; only renders for contiguous-US addresses (data-attribute drives visibility)
3. **Main nav** — centered logo lockup (mark + wordmark), Shop / Collections / Ages on left, search + account + cart on right; search bar is enlarged (320px wide) with Cormorant italic placeholder
4. **Split hero** — left: typographic headline + dek + 2 CTAs; right: full-bleed kaleidoscope image with floating product feature tag
5. **Trust strip** — 4 cards (Free U.S. shipping wagon, 30-Day Returns wax seal, Earn Rewards chalkboard sign, Packed with Care gift box), edge-to-edge
6. **Educator program strip** — slim 2-row callout (not a card; intentionally low-prominence)
7. **Section 01 · New items** (4 product cards)
8. **Section 02 · Best sellers** (4 product cards, one has "Only 2 left" amber stock counter)
9. **Section 03 · Gifts under $50** (4 product cards)
10. **Section 04 · Heirloom favorites** (4 product cards)
11. **Maker spotlight** — Bumbu workshop video (9:16 vertical) alongside founder narrative + 4 stats
12. **Shop by age** — 5 circular age cards (First year → Toddler → Preschool → Early school → School age)
13. **Shop by category** — 9 cards in 3×3 grid, 1:1 aspect ratio
14. **Favorite brands** — 8 tiles in 4×2 grid, 1:1 aspect ratio
15. **Reviews** — 3 large review cards with product images, 5-star, verified-purchase badges
16. **Our story** — founder photo + narrative + signature
17. **Gifting** — gift card image + 3 collection tags (under $30 / $50 / $100)
18. **Blog** — 3 article cards
19. **Newsletter** — "Letters from My Toy Wagon" subscribe form
20. **Footer** — 5-column with brand block, social icons, link columns, payment chips, Top Quality Store badge, copyright + legal links

---

## Critical features beyond static styling

### 1. Free shipping progress bar (conditional render)
Renders only for shipping addresses in the contiguous U.S. Outside that, the bar hides. Wire via Shopify Markets logic or a customer-address check on the storefront.

### 2. Pre-order vs in-stock vs partner-warehouse states (product cards + PDPs)
Three product fulfillment states, each with its own badge color and copy:
- **In stock** — forest green pill, "In stock" or "Ships within 2–4 business days from our LA warehouse"
- **Pre-order** — amber pill, "Pre-order · ships [date]" + the CTA becomes "Pre-order now"
- **Partner warehouse** — amber pill, "Ships from partner warehouse" + extended transit copy

Drive via product metafields:
- `product.metafields.fulfillment.type` = `in_stock` | `pre_order` | `partner_warehouse`
- `product.metafields.fulfillment.ship_date` = ISO date (for pre-orders)

### 3. Stock counter "Only X left"
Amber pill on product card when inventory ≤ 3. Reads from `product.variants.first.inventory_quantity`.

### 4. Sticky add-to-cart bar (on product pages)
Slides down from top of screen once user scrolls past the main product section. Shows thumbnail · maker · name · price · Add to cart button. Mobile-responsive.

### 5. Hover state on product cards
Second image swap on hover (when product has 2+ images). Quick view button slides up from bottom on hover.

### 6. Maker spotlight video
9:16 vertical autoplay/muted/looping MP4. Aspect-ratio container with text content alongside.

### 7. Footer "Top Quality Store" badge (Google)
Small badge placeholder; will pull from Google Merchant Center artifact once the badge is officially awarded.

---

## Product page (PDP) structure

Three template variants share the same Liquid template, differentiated by the `fulfillment.type` metafield:

1. **Breadcrumbs**
2. **Gallery + Meta** (2-column, sticky gallery)
   - Main image, thumbs, wishlist heart, badge in top-left
   - Maker name (amber, uppercase) → Title (Cormorant) → Stars + review count → Price + shipping pill → Tax note → Variant chips → Quantity + Add to cart → Buy now with Shop Pay → Trust mini-row (3 icons) → Ship-time note → "Pair with" widget
3. **Long-form description** (single 760px column)
   - Hero italic Cormorant para → "Why you'll love it" → "At a glance" dl in cream card → Pull quote → Accordion (Materials & origin, Ways to play, Skills built, Who it's for, Care & storage, Includes, Shipping, Returns, Ask a question, FAQ) — uses +/− icon, not chevron
4. **Meet the maker** — full-width image left, narrative right, with "Browse all [maker]" CTA
5. **Reviews band** — summary stats left, review list right
6. **Related products** — 4-card grid from same maker
7. **More from the maker** — link to all reviews for this collection
8. **Recently viewed** — 6-tile strip
9. **Footer**

The accordion's content fields map to product metafields:
- `materials_and_construction`, `ways_to_play`, `skills_it_builds`, `who_it_is_for`, `care_and_storage`, `includes_set_contents`, `faq`, `ships_from_partner_warehouse`, `pre_order_ship_estimate`

Shipping / Returns / Ask a question are global blocks pulled from store-level metafields, not per-product.

---

## Design Tokens

### Colors
| Token | Hex | Use |
|---|---|---|
| `--cream` | `#F5F0E5` | Body background |
| `--warm-white` | `#FFFCF7` | Card backgrounds, light surfaces |
| `--ink` | `#2C2C2A` | Primary text, dark backgrounds, primary buttons |
| `--forest` | `#3B6D11` | Accent (in-stock badges, success, primary link hover) |
| `--amber` | `#854F0B` | Secondary accent (pre-order, partner warehouse, low stock, maker names) |
| `--stone` | `#5F5E5A` | Secondary text, captions |
| `--card-bg` | `#EDE3CD` | Section dividers, secondary surfaces |
| `--rule` | `rgba(44,44,42,0.12)` | Subtle borders |
| `--rule-strong` | `rgba(44,44,42,0.22)` | Stronger borders, button outlines |

### Typography
- **Cormorant Garamond** (400/500/600 + italics) — All display, headings, italic accents, brand wordmark
- **Mulish** (400/500/600/700) — Body text, UI labels, navigation, buttons

| Use | Family | Size | Weight | Style |
|---|---|---|---|---|
| Hero h1 | Cormorant Garamond | clamp(48,8vw,96px) | 500 | regular + italic em |
| Section h2 | Cormorant Garamond | 36-60px | 500 | regular + italic em |
| Card title h3 | Cormorant Garamond | 20-24px | 500 | italic |
| Body | Mulish | 14-16px | 400 | regular |
| Italic prose (lede, captions) | Cormorant Garamond | 14-22px | 400 | italic |
| Label (eyebrow) | Mulish | 10.5-12px | 500-600 | uppercase, letter-spacing 0.16-0.18em |
| Button | Mulish | 12-13px | 500-600 | uppercase, letter-spacing 0.10-0.12em |
| Wordmark | Cormorant Garamond | 18-22px | 500 | uppercase, letter-spacing 0.22-0.24em |
| Logo subtitle | Mulish | 9.5-10.5px | 500 | uppercase, letter-spacing 0.22em |

### Spacing
- 4-pt base. Common increments: 4, 8, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 48, 64, 80, 96, 120
- Section vertical padding: 80-120px desktop, 64px mobile
- Card internal padding: 24-32px
- Page max-width: 1440px (full-width sections), 1100px (content), 760-880px (centered text blocks)

### Border radius
- All elements: `2px` (intentionally tight; gives a printed-paper, not web-app feel)
- Round shapes (age circles, avatars): `50%`
- No rounded buttons, no pill shapes besides badges

### Shadows
- Minimal. Use `0.5px solid var(--rule)` borders instead of shadows for separation
- Soft shadow for floating elements (sticky bar, dropdowns): `0 1px 16px rgba(44,44,42,0.06)`

---

## Voice & copy rules (from the brand guide)

- **No em-dashes** in any UI copy. Use periods or commas.
- **No exclamation points.** Ever.
- **Specific transparency.** Name the wood, the country, the maker. Avoid "perfect for any child," "hours of fun," "designed to inspire creativity."
- **Cormorant Garamond italic** is used for emotional pull quotes, brand taglines, and headlines with stylistic emphasis (one or two words inside an `<em>`).
- **Mulish** is for facts, labels, buttons, and body prose.
- **Title case** in product names and section headings (Chicago style: short prepositions and articles lowercase).

---

## Business info

```
My Toy Wagon, LLC
37 W Huntington Drive
Arcadia, California 91007
Phone: 626.841.0421
```

Email inboxes:
- `contact@mytoywagon.com` — general inquiries, retail orders, returns, press
- `educators@mytoywagon.com` — schools, classroom orders, curriculum questions
- `accounting@mytoywagon.com` — W-9, vendor forms, invoices, payment

---

## Open questions for the founders

1. **Pre-order CTA wording** — currently "Pre-order now." Confirm.
2. **"Top Quality Store" badge** — has it been awarded yet, or is it aspirational? Determines whether the footer placeholder ships or is hidden.
3. **Bumbu maker spotlight video** — confirm the actual .mp4 file location and that it's compressed under 2 MB for mobile.
4. **Wishlist app** — Wishlist Plus, Smart Wishlist, or custom? Affects heart icon binding.
5. **Reviews app** — Judge.me is referenced throughout. Confirm version + plan.
6. **Real product prices** — all prices in the designs are placeholders. The Shopify product database is the source of truth; the theme just renders `product.price`.
7. **Mobile breakpoint pass** — designs are tested at 1440px. Need a mobile responsive pass at 390px.

---

## Files in this bundle

In `designs/`:
- All 17 HTML page references
- `blog/` — sample article
- `assets/` — all photography, logos, and media

See the companion `design_handoff_educator_portal/` for the B2B/portal side.

---

*Last updated: May 2026. Designs are pixel-final.*
