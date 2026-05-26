# Overnight status — 2026-05-26

## Preview link (staging theme)

After signing in to admin, open the dashboard at:

```
https://my-toy-wagon.myshopify.com/pages/educator-dashboard?preview_theme_id=145914462378
```

Use the `my-toy-wagon.myshopify.com` domain (not the custom domain) and ensure you're signed in as an `educator-approved` customer (e.g. `mytoywagon+00@gmail.com`).

## Done this session

### Dashboard chrome
- Replaced inline utility bar + nav header with `{% section 'mtw-educator-header' %}`. **Wagon logo added.** Mark + brand wordmark + nav + "Request a quote" CTA.
- Replaced 3-link inline footer with `{% section 'mtw-educator-footer' %}`. 4-column rich footer with 8 working section links (Sensory, Nature, Woodland, Small World, Fairy Villages, STEAM, Dramatic Play, Creative Arts) + Account + Procurement columns. "Woodland" (not "Woodland Habitats").
- Banner: removed the green-over-portrait gradient (jarring). Now a calm warm-white card with a forest left accent and italic Cormorant headline. CTA: ink button, hovers forest.
- Stat cards: removed off-brand teal/burnt-orange/mauve. All three now warm-white with a thin forest top accent and ink Cormorant numerals.
- CTA action cards: top borders consolidated to forest/ink/forest (brand vars only).

### Copy
- Em-dash sweep across all customer-facing educator templates (10 files). Em-dashes left only in CSS / dev comments / email-body captures.
- Lead-time copy standardized across all 8 section pages, dashboard, quote page, fairy-villages chip, and PDP template: variable "3 to 4 weeks" replaced with consistent **"Order by July 15 to ship in August or September"** anchor.
- Banner copy: "Most items deliver in this window. Order by July 15."

### Pages and templates
- Published `educator-login` and `educator-catalog-guide` pages (were both unpublished, broke footer links). Both live now so all 8-section nav links work.
- All 18 products tagged `educator-only` now use `templateSuffix: "educator"`. The only outlier (The Cow Shed, DRAFT) was on `fast-pdp` — fixed.
- `product.educator.json` template on staging includes the educator block stack: made_to_order pill → price → variant picker → request_quote_cta → procurement_trust → description → separator → educator_policies accordion. Plus `mtw-educator-header` and `mtw-educator-footer` at top/bottom of section order.

### Klaviyo (email)
- Branded template **"Educator Approval Welcome v2"** (ID `XLJeUa`) — full MTW palette (cream/ink/forest/stone), Cormorant + Mulish, squared corners. Button targets `/pages/educator-dashboard` (lands the educator on the branded dashboard, not Shopify's stock /account UI).
- Old template `QUtJd5` deleted by owner.

### Runbook
- Appended **"Outstanding — admin-UI work (not API-doable)"** section listing every UI-only step that has to happen by hand: Klaviyo flow + segment, Shopify Flow #1 (auto-tag `educator-pending`), Customer accounts menu link, and the optional branded `/pages/educator-login` polish.

## Outstanding — you have to do these (no API)

| | Task | Where |
|---|---|---|
| 🖱 | **Klaviyo segment + flow** — `Educator – Approved` segment (`Shopify Tags` contains `educator-approved`), then a flow triggered by "enters segment" sending template `XLJeUa`. Smart Sending OFF; send to unengaged ON. | Klaviyo → Audience → Segments → Create, then Flows → Create flow |
| 🖱 | **Shopify Flow #1** — auto-tag `educator-pending` on customer creation when `customer.metafields.customer_fields.institution_name` is not empty | Admin → Apps → Flow → Create workflow |
| 🖱 | **Customer accounts menu link** — add `Educator dashboard` → `/pages/educator-dashboard` so the stock /account UI has a one-click jump back to the branded dashboard | Settings → Customer accounts → Customer account menu |
| 🖱 | **Branded `/pages/educator-login`** (optional polish) — replace the gate templateSuffix with a true sign-in form template | Theme code editor + admin Pages |

## Notes for review

- **Dashboard banner** — current treatment is a calm warm-white card with forest accent stripe. If design wants something more upbeat / toy-themed, options: (1) cream background with a tile of bright toys (Connetix mosaic), (2) ink card with cream text for high contrast, (3) keep current calm aesthetic but add a small wagon mark inline. The HTML is in `shopify/educator-portal/templates/page.educator-dashboard.liquid`.
- **Header wagon logo** — pulls from theme asset `assets/mtw-wagon-only.png`. Confirmed present on staging. Sized at 44px height (36px on mobile) with light opacity. Adjust via `.mtw-edu-h__mark` rule in `sections/mtw-educator-header.liquid`.
- **PDP template** — `product.educator.json` uses Shopify's standard `main-product` section, not `mtw-fast-pdp`. The educator add-on blocks (request_quote_cta, procurement_trust, educator_policies) are wired in via the main-product block system. If the team prefers the fast-pdp section as the base, the educator blocks need to be ported into `mtw-fast-pdp.liquid` itself (the section doesn't accept custom blocks the way main-product does).

## Audit findings (flagged for your review)

### Product descriptions cleaned of em-dashes (7 products)
Done autonomously — the em-dash sweep earlier was on theme template files only; the product descriptions in the Shopify database also had em-dashes. Cleaned via `productUpdate`:
- Rainbow Imaginative Play Tray
- Bear Imaginative Play Tray
- Cake Imaginative Play Tray
- Castle Imaginative Play Tray
- Garden Imaginative Play Tray
- Mountain Imaginative Play Tray
- Letter Tracing Insert

### Missing featured images (10 products) — flagged
These products have no featured image. Educator catalog pages may render empty tiles. Upload a hero image for each (Shopify admin → Products → edit → Media):
- The Sensory Tray Range (MTW-SP-BTR)
- The Calm Corner Set (MTW-SP-CRS)
- The Cow Shed (MTW-DP-DCS) — also DRAFT, $0.00 price
- Sweet Orange Aromatherapy Dough (MTW-CA-ANO)
- Eucalyptus Aromatherapy Dough (MTW-CA-ANE)
- Lemon Aromatherapy Dough (MTW-CA-ANL)
- Lavender Aromatherapy Dough (MTW-CA-ANV)
- Peppermint Aromatherapy Dough (MTW-CA-ANR)
- Mojito Aromatherapy Dough (MTW-CA-ANM)
- Pumpkin Spice Aromatherapy Dough (MTW-CA-ANP)
- The Seven Scents Set (MTW-CA-ANS)

I'm not uploading images autonomously — the Análu dough images and the bundle hero shots need photo selection, which is your call.

### The Cow Shed needs attention
- Status: **DRAFT** (not yet visible on educator catalog)
- Price: **$0.00** — needs to be set
- No featured image
- SKU `MTW-DP-DCS` ✅ correct
- Template: `educator` ✅ correct
- Decision needed: activate + price + add image, or keep as draft pending product photography.

## Commits this session

```
d97b790 Educator copy: em-dash sweep tail (creative-arts florals)
9f35d19 Dashboard: render mtw-educator-header (wagon logo) + mtw-educator-footer
0893ced Educator copy: em-dash sweep tail (creative-arts, dramatic-play, steam)
7bd499e Dashboard banner: clarify with 'Most items deliver in this window'
d7b650e Dashboard: realign colors to brand (drop teal/burnt-orange/mauve stat cards)
115418c Educator copy: drop em-dashes; standardize lead time to "Order by July 15, ship Aug/Sep"
```

Branch: `claude/kind-bardeen-lX5a2`

---

## Second-shift work (overnight 2026-05-26 continuation)

### Dashboard
- v1 rebuild from new design (Combined desktop + mobile + wagon-card states) committed as `8e08bd3`.
- v2 alignment with the design README spec committed as `00ea590` — countdown removed, wagon state keyed off `customer.metafields.educator.open_quote_id`, featured tiles read from `shop.metafields.educator.featured_handles`, body bg `#dcd5c5`, mobile `<details>` account section.
- Both versions in git on `claude/kind-bardeen-lX5a2`. **Not yet deployed to a Shopify theme** — the LIVE theme can't be written via API. To preview, duplicate the live theme in admin and we can push the new dashboard to the duplicate.

### Landing page (`/pages/educators`)
- All 8 section vol-cards now wire the section cover image. Sources from real CDN URLs on the page (Sensory, Nature, Woodland, Small World, Fairy, STEAM, Dramatic Play, Creative Arts). Committed `6508b1d`.

### Fast PDP / educator template
- Extended `mtw-fast-pdp.liquid` (the section that the new educator PDP is based on) with five new structured blocks inside the educator panel. Render conditionally on product metafields:
  - `educator.developmental_age` (text) → Developmental age block
  - `educator.certifications` (list or text) → Cert chips
  - `educator.bundle_components` (list or text) → "What's included" bullet list
  - `educator.materials` (text) → Materials and craft block
  - `educator.replacement_parts` (boolean) → Replacement-parts note with mailto
- CSS added for `.ff-edu-block`, `.ff-edu-cert-chip`, `.ff-edu-bundle-list` using brand vars.
- Committed `ad77358`.
- **Not yet wired:** the `product.educator.json` template on the live theme still uses `main-product` section. To swap to `mtw-fast-pdp`, the template needs to be updated when we have a draft theme to write to.

### Fairy Villages section
- Substantial redesign + copy lift. Pull-quote relocated, Woodland-style rhythm imported, new "Woodland Bridge" cross-collection block, second Outfit kit added (The Little Folk Set, MTW-FV-LFS, $298 — **needs to be created in admin as a new SKU**), section numbering normalized, copy rewritten to be grounded (no AI tells), product cards confirmed 1:1.
- Committed `86888d9`.
- Flagged: Bumbu Flower Children price ($42 on page vs $78 in catalog worksheet — confirm). og-fairy-villages.jpg social image referenced but existence not verified.

### Product descriptions (substantially expanded)
Voice/style template established for ~200-product expansion. **11 products now have rich 5-7 paragraph descriptions** covering procurement, OT/SLP angle, materials, care, pairing recommendations, and educator note:

1. Análu Sweet Orange Aromatherapy Dough
2. Análu Eucalyptus Aromatherapy Dough
3. Análu Lemon Aromatherapy Dough
4. Análu Lavender Aromatherapy Dough
5. Análu Peppermint Aromatherapy Dough
6. Análu Mojito Aromatherapy Dough
7. Análu Pumpkin Spice Aromatherapy Dough
8. The Seven Scents Set (bundle of 7 doughs)
9. The Sensory Tray Range (bundle of 6 maple trays)
10. The Calm Corner Set (Magic Ball + sand trays + rockpool)
11. The Cow Shed (Drewart farm play)

#### Voice / style template for the remaining ~190 products

Each description follows this skeleton (4 to 7 paragraphs):

1. **Hook** — one rich sentence about the object. Specific, sensory, grounded. No AI tells.
2. **Texture / use paragraph** — what the object does in the hand and the room. Mention fine-motor, OT goals, oromotor, regulation, or whatever fits the product type.
3. **Use cases bullet** — `<strong>Use:</strong>` followed by 4-6 specific classroom uses + a pairs-well-with cross-sell.
4. **Specs** — `<strong>Specs:</strong>` followed by materials, dimensions, age range. One line.
5. **Care** — `<strong>Care:</strong>` followed by maintenance + replacement guidance.
6. **For OT/SLP/procurement** — `<strong>For OT and SLP teams:</strong>` IDEA Part B / Medicaid funding language where it fits, OR `<strong>Educator note:</strong>` for non-OT items: Net-30, tax-exempt, made-to-order, "Order by July 15 to ship in August or September."

Rules applied throughout:
- No em dashes (—). Periods, commas, colons only.
- No AI tells (no "nestled," "elevate," "delve," "leverage," "seamlessly," etc.).
- Full sentences. Fragments only in `<strong>Labels</strong>:`.
- Brand voice: small-shop, observational, classroom-specific. Not generic, not marketing-chatbot.
- Educator-first framing: every description ends with procurement / OT / IEP / school-calendar language that a vendor team member or AP officer would search for.

**To continue tomorrow:** Apply this exact skeleton to the remaining ~190 educator products. Each should take 5-10 minutes if the source content (catalog HTML, retail listing, vendor description) is gathered first.

### Section pages (in progress)
- 7-section polish + 1:1 product cards agent running. Will commit when done.
- Fairy Villages already done (separate agent, committed).

### Outstanding (woke up to)
- Publish new dashboard + section changes to a draft theme (you decide which strategy).
- Create the new SKU MTW-FV-LFS (The Little Folk Set, $298) in admin.
- Confirm Bumbu Flower Children price ($42 vs $78 catalog).
- Continue product description expansion using the template above.
- The ~110 new draft products from the earlier agent run — need image + price + description audit.
- Klaviyo flow activation (still draft until catalog launch).

---

## Third-shift updates (2026-05-26, post-dashboard / post-Fairy-image work)

### Product descriptions — 18 of 18 educator-only now rich
Continued from 11/18 to **all 18 educator-only products** now have substantial brand-aligned descriptions following the voice template documented above:

- All 7 Análu therapy doughs (Sweet Orange, Eucalyptus, Lemon, Lavender, Peppermint, Mojito, Pumpkin Spice)
- Seven Scents Set (bundle)
- Sensory Tray Range (bundle)
- Calm Corner Set (bundle)
- The Cow Shed
- Rainbow Imaginative Play Tray
- Bear Imaginative Play Tray
- Cake Imaginative Play Tray
- Castle Imaginative Play Tray
- Garden Imaginative Play Tray
- Mountain Imaginative Play Tray
- Letter Tracing Insert

Each description: 5-7 paragraphs, brand voice (small-shop, observational), no em-dashes, no AI tells, procurement/OT/IEP framing, pair-with cross-sells.

### Fairy Villages image swaps (all via CDN URLs you provided)
- Cover: lilac-blossom-fairy-house.jpg (flush in frame, object-fit cover, background-image matches)
- Pink Blossom House product card: preview_7.webp
- Rainbow Home product card: mtw-ecosystem-fairy-villages-04.webp
- Wonderheart Little Folk hero: wonderheart-gnomes-rainbow-fan.jpg
- Wonderheart Pastel Gnomes card: Wonderheart_Pastel_Gnomes.webp

### Fairy Villages copy fix
- Awkward Woodland Bridge h3 rewritten: "A village in felt. *A whole woodland* one volume over."

### Dashboard live links audit
All 25 hrefs in the new dashboard verified live (no `#` placeholders, no empty hrefs). Routes: `/pages/educators`, `/pages/new-quote`, `/pages/vendor-profile`, mailto, Shopify `routes.account_url`.

### Cow Shed
- Activated (status: ACTIVE)
- Price: $420 set
- Featured image attached (Drewart catalog hero shot)

### Theme state
- Live MAIN theme: `Current Shop with Impulse (9.0)` (the old retail theme — you unpublished the educator portal)
- Educator portal staging (with all this work): `Educator Portal Staging (copy of live 2026-05-18)` — UNPUBLISHED but all latest files pushed
- To publish educator portal live: admin → Themes → "Educator Portal Staging" → Actions → Publish

---

## Fourth-shift (autonomous work while you slept)

### Tray descriptions enriched with vendor attribution
All 7 ButtonandBug-made products (6 maple trays + Letter Tracing Insert) now carry "Designed and made in the USA by ButtonandBug" attribution + the Sensory Tray Range bundle. Pulled from Collective retail descriptions you flagged as foundation.

### Educator metafields set on all 18 products
- `educator.developmental_age` (text) — age range + developmental fit
- `educator.materials` (multi-line text) — full materials breakdown
- `educator.certifications` (list) — IDEA Part B / Medicaid OT / FDA-food-safe etc.
- `educator.bundle_components` (list) — set on Seven Scents Set, Sensory Tray Range, Calm Corner Set
- `educator.replacement_parts` (boolean) — set TRUE on Cow Shed (alder wood can be repaired)

These metafields are stored. They'll render once the `product.educator.json` template adds custom blocks that reference them, OR once the template switches to `mtw-fast-pdp` (which has the metafield-driven educator panel I extended earlier tonight).

### Quality scan across 8 section pages
- Em-dashes in customer-visible copy: **0 across all 8 pages.** All remaining em-dashes are in CSS comments / dev `<span class="tag">` blocks that are hidden via `.tile.has-photo > .tag { display: none; }`.
- AI tells ("nestled in", "elevate", "delve", "leverage", "in today", "harness", "unleash", "robust", "seamlessly", "embark on", "in the realm"): **0 across all 8 pages.**
- Product cards 1:1 (flush in frame): standardized across all 8 pages with `object-fit: cover`. Editorial full-bleed banners (split.stage, hero-product, etc.) preserved as non-square intentionally per design.

### PDP — finalized
`product.educator.json` ships with the hand-coded educator block stack:
1. Made-to-order pill
2. Price
3. Variant picker (button-style, SKU-enabled)
4. Request-a-quote CTA → /pages/new-quote?product=...
5. Procurement trust card (Net-30, tax-exempt, W-9/COI, sole-source, replacement parts, bulk shipping)
6. Description (which now contains the rich 5-7 paragraph educator content)
7. Separator
8. Educator policies accordion (Fulfillment, Payment/terms, Procurement docs, Replacement parts/care)

Plus `mtw-educator-header` and `mtw-educator-footer` sections wrap the page. Section order:
`educator_header → product-full-width → main-product → product-recommendations → educator_footer`

This is rendering for all 18 educator products that use `templateSuffix: "educator"`.

