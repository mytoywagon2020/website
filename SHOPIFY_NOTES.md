# Shopify Implementation Notes — B2B Native

Platform-specific guidance for building the My Toy Wagon educator portal on Shopify, **using the native B2B feature set** (Companies, Catalogs, Payment terms). Pair this with the design files in `designs/` and the spec in `README.md`.

---

## Platform context

**Shopify plan: confirmed B2B catalog access.** Native B2B features available — Companies, Catalogs, Payment terms templates, customer-built draft orders.

This is the **easy path**. Most of the educator portal implementation is **configuration + theme styling**, not custom code. Estimated build: 3-5 weeks (1-2 weeks Shopify configuration + 2-3 weeks theme/template implementation).

---

## The native B2B model

Shopify's B2B feature set maps almost 1:1 onto this design. Use it.

| Design concept | Shopify B2B object | Notes |
|---|---|---|
| Educator account (the school / therapist / co-op) | **Company** | Top-level B2B customer entity |
| Sarah Chen, the actual buyer | **Company Contact** (a Customer linked to a Company) | One Company can have many Contacts |
| Maple Tree Montessori — Toddler Room A | **Company Location** | Locations have their own catalog assignments, payment terms, addresses, tax overrides |
| Educator pricing on every product | **Catalog** assigned to the Location | Catalogs are price lists scoped to locations |
| Net-30, Net-60 terms | **Payment terms template** on the Location | Net-30, Net-60, prepaid, custom |
| Quote builder | Customer-built **Draft Order** | B2B customers can build their own draft orders in their account |
| Tax-exempt status | **Tax override** on the Location | One toggle per Location |
| Sales rep | **Customer assigned to Company** | Optional |
| Drop-ship to multiple classrooms | Multiple **Locations** under one Company | Each Location has its own shipping address |

### The mental model

**One Company = one school/practice/co-op.** Inside that Company:
- Each *Location* is a classroom, building, or shipping address
- Each *Contact* is a person who can place orders on behalf of the Company
- The *Catalog* assigned to a Location determines what products and what prices show
- The *Payment terms* on a Location determine Net-30 vs Net-60 vs prepaid

For a small Montessori with one address and one buyer: 1 Company, 1 Location, 1 Contact. For a multi-building district: 1 Company, N Locations (one per school), N Contacts.

---

## Companies: data model

Every approved educator account becomes a **Company** in Shopify. The metafields you'll need on the Company resource:

| Namespace.key | Type | Values | Purpose |
|---|---|---|---|
| `educator.account_type` | single_line_text | `school`, `therapist`, `homeschool_coop`, `library` | Filtering, reporting, sales rep routing |
| `educator.verified_at` | date | — | Audit trail |
| `educator.verified_by` | single_line_text | — | Internal — staff name who approved |
| `educator.application_notes` | multi_line_text | — | Original application content |
| `educator.internal_notes` | multi_line_text | — | Running notes from your team |
| `educator.sales_rep_email` | single_line_text | — | Assigned rep |
| `educator.sustainability_required` | boolean | — | For green-school questionnaires |
| `educator.sole_source_letters_count` | number_integer | — | Tracking, not customer-visible |

On the **Location** resource:
| Namespace.key | Type | Values | Purpose |
|---|---|---|---|
| `educator.program_name` | single_line_text | "Toddler room A" | Display in dashboard greeting |
| `educator.grade_levels` | list.single_line_text | `["pre-k", "k"]` | For curriculum match |
| `educator.enrollment_range` | single_line_text | `"15-30"` | Sizing context |

---

## Catalogs: pricing strategy

Create one or more **Catalogs** for educators. Recommended structure:

| Catalog name | Assigned to | Pricing rule |
|---|---|---|
| Educator Standard | Verified educators with terms = prepaid or Net-30 | 15% off retail |
| Educator Tier 2 | Verified educators with annual volume > $5K | 20% off retail |
| Educator Tier 3 | Bulk / district / partnerships | 25% off retail OR custom per-product |

Assign Catalogs to Locations. Customer signs in → catalog is automatically applied → they see educator prices everywhere on the storefront, in the quote builder, and in their cart.

**Don't** try to do per-customer pricing with metafields and Liquid hacks. The native Catalog feature is what you have B2B for.

---

## Payment terms

Set up these payment terms templates:

| Template name | Net days | Available to |
|---|---|---|
| Prepaid | 0 | New accounts before clean payment history |
| Net-30 | 30 | Default for verified educators |
| Net-60 | 60 | Larger or recurring orders, approved case-by-case |

Assign per Location. The terms flow automatically into draft orders and invoices.

---

## Quote builder — use native, not custom

The B2B customer account UI now supports **customer-built draft orders**. This is the quote builder.

**What's native:**
- Customer signs into their B2B account
- "Create a quote" / "New order" entry point
- Product search across their assigned Catalog
- Add line items with quantities
- See educator pricing automatically
- Submit for review → creates a Draft Order tagged with the Company

**What you customize via theme:**
- The visual styling of the customer account pages (B2B account UI is customizable via Customer Account UI Extensions)
- The "How quotes become orders" explainer (theme content)
- The notes textarea, quote name, "for program", "needed by" fields — add as custom attributes via a Customer Account UI Extension

**Custom attributes to add to the Draft Order on submission:**
- `quote_name`
- `for_program`
- `needed_by`
- `submitted_via` = `educator_portal`

**Tags on the Draft Order:**
- `educator-quote`
- `pending-review` (initial)
- Then your team flips through: `approved` → `awaiting-po` → `po-received` → completes draft

---

## Customer Account UI Extensions

The dashboard, vendor profile, and new-quote screens go in here. Shopify Customer Account UI Extensions let you add custom blocks, pages, and full-page extensions inside the signed-in B2B account experience.

For each design, the implementation target:

| Design | Implementation |
|---|---|
| Educator dashboard (`educator-dashboard.html`) | **Customer Account UI Extension** — full page extension at `/account/dashboard` |
| New Quote (`new-quote.html`) | **Customer Account UI Extension** — `/account/quotes/new`, OR rely on Shopify's native quote/order builder with custom-attribute extension |
| Vendor profile (`vendor-profile.html`) | Liquid page at `/pages/vendor-profile`, OR Customer Account UI block if you want to gate it to verified educators only |

UI Extensions are built with **React + Shopify's UI Extensions API** (similar to checkout extensions). No need to build a full custom embedded app — extensions run inside the customer account shell.

---

## Marketing pages: pure Liquid

These three are theme-side only. Standard Liquid templates:

| Page | Template |
|---|---|
| Schools landing page (`ordering-for-schools.html`) | `page.schools.liquid` |
| Procurement guide (`procurement-guide.html`) | `page.procurement-guide.liquid` OR static PDF in Shopify Files |
| Catalog back matter (`catalog-back-matter.html`) | Design reference for print, not a live web page (though chapter 6 could live at `/pages/educator-info` for QR resolution) |

The QR code targets in the printed catalog:
- `mytoywagon.com/educator` → URL Redirect → `/account/login?return_to=/account/dashboard` (or to apply if not logged in)
- `mytoywagon.com/procurement-guide` → `/pages/procurement-guide`

---

## Application form → Company creation

When a school applies via the form on `educator.html`:

1. Form submission goes to a **Shopify Form** (native) or **Tally/Typeform**
2. Webhook fires to a **Shopify Flow** workflow:
   - Creates a new Company with the submitted name
   - Creates a new Location under the Company with the address
   - Creates a new Customer Contact under the Company with the buyer's email
   - Sets `educator.account_type` metafield on the Company
   - Sets `educator.application_notes` with the form content
   - Sends internal notification to `educators@mytoywagon.com`
3. Staff reviews in Shopify admin → assigns a Catalog and payment terms → emails the customer

Once the Catalog is assigned and the customer signs in, they see educator pricing automatically.

---

## Tax exemption

For verified Locations with a tax-exempt certificate on file:
- Set **Tax override** on the Location to exempt from sales tax
- Upload the certificate as a file metafield on the Location
- The override applies automatically on every order from that Location

No Liquid logic, no custom code.

---

## Email notifications

Customize these notification templates:

| Notification | Customization |
|---|---|
| New customer welcome | Replace with: "Application received. Verification in 1-2 business days." |
| Draft order invoice | Subject: "Quote #{{ order_number }} — pricing held 30 days". Footer adds procurement notes summary. |
| Order confirmation | For orders tagged `educator-quote`, reference the original quote number and PO. |

Use **Shopify Flow** for trigger-based emails (e.g. "send welcome email when Company is updated with verified status").

---

## What's still custom

Even with native B2B, three things need build work:

1. **Apply form** — Not native. Build with Shopify Forms or Tally; pipe to Flow for Company creation.
2. **Custom-styled Customer Account pages** — Use Customer Account UI Extensions to match the design.
3. **Theme templates** for the schools page, procurement guide, and any custom marketing pages.

Everything else is configuration.

---

## Build sequence

1. **Week 1** — Shopify configuration
   - Enable B2B if not already on
   - Create Catalogs (Educator Standard, Tier 2, Tier 3)
   - Set up Payment terms templates
   - Define metafield schemas on Company / Location
   - Set up URL redirects for `mytoywagon.com/educator` and `mytoywagon.com/procurement-guide`

2. **Week 2** — Marketing pages
   - Build theme template for `/pages/schools`
   - Build theme template for `/pages/procurement-guide` (or upload PDF)
   - Build vendor profile page

3. **Week 3** — Apply flow
   - Build Shopify Form (or Tally embed) on educator.html
   - Set up Shopify Flow workflow to create Company on submission
   - Customize verification email

4. **Week 4-5** — Customer Account UI Extensions
   - Build dashboard extension
   - Build new-quote extension (custom attributes on draft order)
   - Build vendor profile gate
   - QA the full quote → PO → order flow

---

## Testing checklist

End-to-end smoke test:

1. [ ] Anonymous visitor applies → Shopify Form submits → Flow creates Company + Location + Contact
2. [ ] Staff assigns Catalog + payment terms → flips verified
3. [ ] Customer receives welcome email
4. [ ] Customer signs in → sees educator pricing on every product
5. [ ] Customer builds a quote via new-quote → submits → Draft Order appears in admin with tags
6. [ ] Staff completes Draft Order → order created with correct Net-30/60 terms
7. [ ] Tax exemption applied for Locations with override
8. [ ] All emails route to correct inboxes
9. [ ] QR codes resolve to correct URLs

---

## What changed from the previous version of this doc

Earlier draft assumed non-Plus Shopify with apps and Liquid hacks. **Discard that.** With B2B catalog access, you're using native features. Build is smaller and cleaner.

---

*Reach out to the original design conversation for any pixel-level clarifications.*

---

## Educator portal — design rules (standing)

- **All product & hero images sit FLUSH in frame** (`object-fit: cover`, fill — no padding/letterbox/`contained`). Apply automatically, don't wait to be told.
- **Product cards are square** (`aspect-ratio: 1/1`) so square product photos fit without cropping.
- **American spelling throughout** — color (not colour), fiber (not fibre), center (not centre).
- **Educator titles:** descriptive + MTW-branded; **no maker brand in the title unless it's a marquee credibility name** (Connetix, Bauspiel, Grimm's, Holztiger, Tara Treasures). **Gry & Sif is NOT marquee** — drop it. (Brand/cert/provenance still go in the body/specs.)
- **Catalog citation:** "From the 2026 **Fall** Edit" (twice-yearly cadence: Fall + Spring).
- **No "Request a quote"** CTAs — cards link to the product PDP ("View product →").
- **Remove redundancy *unless it adds value*.** Cut repeated copy/labels (e.g. "Creative Arts" on every card meta, the same opener line across sections, "Price on request"). BUT keep intentional repetition that earns its place — e.g. a hero product also shown in its grid when the two images are *different and complementary* (lifestyle hero + clean product-shot grid card). Different media (web ≠ print): make the online version superior, not a literal clone of the catalog.
- **Each featured hero sits directly before its matching grid** (The Floral → felt florals, Eco-Cutters → eco-cutters grid, Heirloom Press → Pressing & Preserving, etc.).
- **No blanket spec strip over a mixed-maker grid.** A section header may only state material/origin/cert that is true for *every* product in it. When makers/origins differ (e.g. Grapat/Spain + Harrisville/US in one grid), keep it neutral ("Natural materials and child-safe finishes; maker and origin vary by piece") and put specifics per product.
- **Only claim certs/materials we can verify.** Don't assert OEKO-TEX/GOTS/Fair Trade or a material (metal vs biodegradable bioplastic; glass vs paper press) unless confirmed for that product. Conceal a little for marketing, but never inaccurately.

---

## Card meta line — SKU rule (educator portal)

The product-card **meta** line shows the **SKU only** — never a section/category token (the category just repeats down the row and is noise). Keep a **useful per-item spec** when it varies card-to-card (piece count "· 48 pieces", set size "· Set of 5", dimensions, tin size, "· Single tree") — those aren't repetition. Drop generic category words ("STEAM", "World Kitchen", "Farmyard", "Bakery", "Café", "Felt play food", "Life cycle set", "Prehistoric", "Science model"). Maker/material (e.g., "Hand-felted wool", "June & December") may stay where it's a credibility signal, but prefer SKU-only when the maker repeats across the row.

**Provisional SKUs (owner to confirm against catalog/inventory):** the cards that previously lacked a SKU were given placeholder MTW-XX-### codes so the layout reads correctly — Dramatic Play (Cow Shed MTW-DP-DCS, Straw Bale BSB, Pumpkins BPG, Mandala Tulips GMT, Bread/Pantry BPB, Charcuterie CCP, Scones SCN, Cookies COO, Bundt BND, Choc Cake CHC, Cupcakes CUP, Ice Cream ICE, Lollipops LOL, Beef Noodle BNS, Peruvian PSF, Ethiopian EFE, Mezze MEM, Jollof WAJ, Fika SWF) and STEAM (Bauspiel BMB/BLC/BFW/BCT/BSS/BOB, Life cycles LCF/LCB/LCE/LCN/LCD, Dino Eggs DNE, Prehistoric PHS, Jurassic PJS, Anatomy HAN, Food Groups FGN). Replace with real SKUs when available; flag clashes.

## Season naming — Autumn (public) / Fall (schedule)

Deliberate split:
- **Autumn** = product names, public-facing display copy, and the catalog edition name (*Autumn Leaves*, *The Autumn Set* / MTW-NP-AUT, *2026 Autumn Edition*). Premium register.
- **Fall** = anything **schedule/calendar** — booking windows, delivery windows, "book in the fall" — because that's the vernacular schools think in. (e.g., "Fall booking", "Fall delivery (Aug–Sep)").
- **"fall"** as an SEO tag/keyword is fine but minor; real SEO is generic high-intent terms (e.g., "magnetic tiles for classrooms", "Montessori sensory materials"), not the season word.
- **Spring**: removed from all theme/edition copy. Still under review for the *schedule* (the spring booking/delivery window) and the **Papoose 4-season Seasonal Trees** product, where spring is a literal calendar/product feature.

## Grid symmetry rule — center partial rows

In the **uniform** product grids (`.gallery .homes` with plain `<article class="home">` — STEAM, Dramatic Play, Creative Arts), any row with **fewer than 5 cards** must be **centered** for symmetry. Implementation: on that grid's `<div class="homes">` use inline `style="grid-template-columns: repeat(auto-fit, minmax(190px, 222px)); justify-content: center;"` (keeps 5-up rows identical, centers orphan rows at all widths). Does **not** apply to the intentionally asymmetric `size-hero/size-tall/size-std` compositions (Sensory, Nature, Woodland, etc.) — those are designed and already balanced.

## Educator pricing rule — REGULAR price only

**In-stock rule (educator track):** educator products **always show as in-stock / orderable** — never "Coming soon" or sold-out — because they're **made-to-order** (Shopify "continue selling when out of stock" for the educator catalog, not retail). So even items that are Draft / 0-inventory in the retail store (e.g., the whole Connetix line) show a price and an order CTA on the educator pages.

**Bundle pricing:** a bundle = **sum of its component regular prices, then 10% off** — flat **10% on all bundles**. ⚠️ **10% is a hard ceiling: the maker (Connetix) does not allow more than 10% off (MAP policy).** Never advertise a steeper discount. Not graduated (no 12/15% tiers — would breach MAP, and shipping is costly in a volatile market). **Individual packs are full retail — the discount applies to bundles only.** Indicate the contents, the list total, the bundle price, and the savings. (e.g., Connetix Full = Mid + Roads&Ramps $89 + Mega $209 → $592 list → **$533**. Starter $154→$139, Mid $294→$265.)

Educator-catalog prices must use the **regular price**, never a retail sale/markdown — these are **made-to-order** purchases, so they don't ride retail promotions. In Shopify terms: use the variant **`compareAtPrice`** when the item is on sale (that's the regular price); use `price` only when `compareAtPrice` is null (not on sale). Many retail titles are even prefixed "Sale …". ⚠️ Owner will audit **every** educator price before go-live. Known mismatch to revisit: **Wonderheart** gnome sets — Shopify regular is **$144** (Rainbow Wooden Gnome Set) / **$84** (Mini sets); educator cards currently show $108.

## Brand → Certification — vendor cross-reference trigger

Educator titles are often brand-agnostic, so don't guess the maker from the title. **Authoritative source: the Shopify product `vendor` field.** Workflow when sourcing/verifying a Files image: image → its product → `vendor` (brand) → apply that brand's cert from the table below. Where `vendor` = **"My Toy Wagon"** (house brand, maker not surfaced), fall back to the branded **filename** or the maker named in the card, and verify.

| Brand (vendor) | Cert / provenance to cite |
|---|---|
| Tara Treasures | **Fair Trade USA™ Certified** · felt, designed Melbourne, made Nepal |
| Papoose Toys (felt P/P + cotton) | **WFTO & Fair Trade USA Certified** · Nepal |
| Papoose Toys (teak tools) | generic "fair-trade conditions" (felt/cotton cert does not cover teak) |
| Himalayan Felt Co. | felt, Nepal — **cert unverified**, keep generic until confirmed |
| Wonderheart | **Made in USA** (birch + felt) — not fair-trade |
| Bumbu | FSC maple/basswood, Romania, water-based paint + organic oils, CE/EN71 |
| Bauspiel | Germany, EN71 — **FSC unverified** |
| Connetix | non-toxic, ASTM/EN71/CE (plastic + magnets; not FSC) |
| Tender Leaf | FSC reclaimed rubberwood, ASTM F963/CPSIA |
| Wooden Story | FSC, Poland, organic oils |
| Análu | made in California, USA (therapy dough) |
| June & December | reclaimed Michigan wood |
| Kinfolk Pantry | Australia, plant-based biodegradable PLA |
| Gus + Mabel | felt habitats, Nepal — **cert unverified**, keep generic until confirmed |
| Buttonandbug | trays — **origin unverified**, do not claim "made in USA" until confirmed |

Unverified above (Himalayan, Bauspiel FSC, Gus + Mabel, Buttonandbug) → owner to confirm; keep generic meanwhile.

## Fair-trade certifier terminology (do not mix up)

Two different bodies — match the maker:
- **Tara Treasures → "Fair Trade USA™ Certified"** (their exact wording).
- **Papoose felt → "WFTO &amp; Fair Trade USA Certified"** — Papoose felt items (code "P/P") and 100% cotton carry **both** WFTO and Fair Trade USA certification (company + product level). Does **not** cover their **teak** items — keep those generic ("fair-trade conditions").
- **Mixed-maker** grids (e.g., Small World mixes Papoose/Himalayan/Tara): don't over-claim a certifier that doesn't cover every maker (Himalayan unverified) — use a generic "made under fair-trade conditions," or name each.

## Supplier provenance — verified facts (safe to cite)

Maker/origin/cert claims must be verifiable (see design rule above). Confirmed so far:

- **Tara Treasures** (felt play food, finger puppets, fairy homes, habitats, story sets): Designed in **Melbourne, Australia** (founders Jag & Jooli Chan); handmade by **women artisans in Nepal** (home + small community workshops; women-empowerment mission). **Fair Trade USA™ Certified.** Felt is **100% natural wool sourced from New Zealand**, eco-friendly non-toxic dyes; meets **OEKO-TEX® STANDARD 100**. → Fair Trade + OEKO-TEX are verified **for Tara Treasures specifically** — fine to cite on Tara items, but do **not** blanket them across a mixed-maker grid (Papoose/Himalayan/etc. aren't covered).
- **June & December** (Heirloom Flower Press): handmade from **reclaimed Michigan wood**, hand-assembled in their **Michigan** studio; acid-free neutral-pH boards + reusable specimen separators; FSC-certified, 100% recycled paper/boards/packaging; steel hardware standard, brass upgrade. (Not Brooklyn.)
- **Kinfolk Pantry** (Eco-Cutters): handcrafted in small batches in **Australia** from **plant-based, biodegradable** material (PLA / recycled wood-mill sawdust); non-toxic. Ages 3–8. Not metal.
- **Drewart** (Cow Shed, etc.): hand-finished alder, **Poland**. ("Cow shed" = the European term; for US educators it functions as the barn.)
- **Bumbu**: hand-carved maple/basswood, **Romania**, water-based paint + organic oils.
- **Papoose Toys** (felt play food incl. World Kitchen / world cuisines, hot drinks, felt shapes): **World Fair Trade Organization (WFTO) certified** — wool felt products with product code **"P/P"** are WFTO Guaranteed; 100% of their cotton items are WFTO certified. Handmade from **100% natural, biodegradable wool and cotton** with **non-toxic, colorfast dyes**. Crafted primarily by **women in Nepal** under fair-trade conditions (fair wages, safe workspaces, stable employment). ⚠️ The body is **WFTO** (World Fair Trade Organization) — do NOT mistype as "WTFO".
- **Verify-before-claiming** still pending: exact makers/certs for threading looms (LapLoom/Potholder read as Harrisville/US; Weaving Frame = Grapat/Spain), Tender Leaf origin, Himalayan certs.

---

## Educator products: separate listings, never Collective (RULE — for staff)

**Rule:** The educator portal and the Educator catalog use their OWN product listings — **never the retail "Collective" listings.** We do **not** sell Collective items on Educator.

**For every educator portal product card:**
1. If a Collective (retail) listing exists, **duplicate** it into a new **Educator listing** (copy title, description, images; add educator-specific info from the educator catalog).
2. Make the new listing visible **only in the Educator catalog** (B2B) — not retail.
3. Link the portal card's "View product" to the **Educator** listing's PDP (`/products/<handle>`).

**Tag convention — apply to every educator listing:**
- `educator-only` — non-Collective, educator-exclusive listing (never sell on retail/Collective). *(new — the "makes sense" tag.)*
- `educator-<section>` — section it belongs to, e.g. `educator-dramatic-play`, `educator-creative-arts`, `educator-steam`, `educator-sensory`, `educator-nature-play`, `educator-woodland`, `educator-small-world`, `educator-fairy-villages`.
- `needs-price` — temporary; remove once an educator price is set.

**Naming & type (decided):**
- **Title stays the clean product name** — do **NOT** append "(Educator)". The title is customer-facing (PDP, cart, receipts); the educator already knows they're in the educator catalog.
- **Brand in title — differs by channel:** *Retail/Collective* **keeps the maker brand** (Fagus, Bumbu, Tara Treasures…) because it matters for **SEO / brand search**. *Educator* titles are **brand-agnostic & descriptive** — on the Educator catalog **My Toy Wagon is the brand** — so use the clean name that matches the portal tile (e.g., "Wooden Hay Wagon," "Cow Shed," "Felt Farm Animals, Set of 10," not "Fagus…/Drewart…"). When duplicating a Collective listing into an educator one, **rename it to the descriptive educator name.**
  - **Nuance — don't throw brand away for educators:** (a) keep **recognized-quality brands** (Connetix, Bauspiel, Grimm's, Holztiger, Tara Treasures) in the educator title or prominently in specs — they're *credibility signals* to Montessori/Waldorf-literate buyers; (b) always surface **provenance + certifications** (Fair Trade, made in Nepal/Germany, OEKO-TEX/GOTS/ASTM/CE) in the product details — these are major trust factors for schools/procurement. So: MTW-branded descriptive title + brand/cert/provenance in the body; lead with the maker brand in the title only for the marquee credibility names.

**Catalog architecture — prefer one product, two catalogs (avoid duplicate inventory):** Don't duplicate *every* Collective item into an educator twin — two listings for one physical product = two inventory pools (overselling risk) + double maintenance. Use Shopify B2B's **one product → retail price + Educator price-list/catalog** for most items. Reserve *new* educator listings for: **bundles**, **educator-exclusive** items, or items needing a **different educator title/description**.

> **⚠ SUPERSEDED (2026-05) — we chose FULL SEPARATION.** *Every* educator item now gets its **own** listing (continue-selling, Educator catalog, **off retail**), not "one product, two catalogs." Why: "sell when out of stock" is a **per-variant** setting (applies to all channels) and inventory is **one shared pool per variant** with **no per-channel/location fence on our plan** — so a single shared listing can't be retail-accurate *and* educator-pre-order at once. Build each educator listing **from the retail listing's full content** (description + images), cleaned. Conventions (clean title, Vendor = My Toy Wagon, Product Type = Educator, tags `educator-only` + `educator-<section>` + maker-brand + age, `-educator` handle) and the API do/don't are in **EDUCATOR-PORTAL-RUNBOOK.md → "Educator listings — build SOP & conventions."**
- **Handle:** use a `-educator` suffix (e.g., `the-cow-shed-educator`) so the listing is recognizable by URL.
- **Product Type:** set to `Educator` for an at-a-glance admin column.
- Distinguish/filter the whole set in admin with **`tag:educator-only`** (primary method).

**Visibility / channels (how "educators only" works):**
- **Sales channel:** the product must be on the **Online Store** channel so its `/products/<handle>` PDP renders.
- **Educator (B2B) catalog:** controls educator pricing + access. A B2B-catalog product is reachable by logged-in approved educators but is **not** surfaced to retail browsing.
- Keep educator listings **out of all public/retail collections** and the retail market catalog so retail shoppers don't find them.
- Net: **Active + in the Educator/B2B catalog + out of retail collections = educators see it, retail doesn't.**

**Avoid duplicate educator listings (guardrail):** Before creating an educator listing, **search for an existing one** — `tag:educator-only` or handle ending `-educator`. If one exists, **reuse/link it**; do not create a second. (A *Collective/retail* listing existing is NOT a reason to skip — only an existing *educator* listing is.)

**Matching tip (avoid false "missing"):** Our product titles usually include the **brand** (Fagus, Bumbu, Tara Treasures, Papoose, Tender Leaf, Q Toys, Drewart, Gry & Sif, Análu, Connetix, Bauspiel…) and felt items often include **"felt"**. A portal tile named "Hay Wagon" is the product "Fagus Wooden Hay Wagon"; "Farm Animals" is "Felt Farm Animals, Set of 10." Always search by the **core noun + brand/felt variants** before concluding a listing is missing — otherwise you'll create a duplicate.

**Bundles = educator convenience ("one-click instant corner play space").** Each section offers a bundle that buys the whole corner at once (Farmyard, Classroom Shop, Play Café, World Foods, etc.). Create these as **educator-only bundle products** (tags `educator-bundle` + `educator-<section>` + `educator-only`), linked from the section's "See the bundle" CTA. Bundle SKUs already referenced in the templates: `MTW-DP-SH` (shop), `MTW-DP-CAFE` (café), `MTW-DP-WEA` (East Asian East-Asian), plus farmyard/world-kitchen sets, and the Creative-Arts collections.

**Lifecycle:** Educator listings start `DRAFT` + `needs-price`. When priced, activate on the Educator catalog to go live. Portal card links are set by product **handle** in the templates now, so each card resolves the moment its educator listing is activated — no template change needed later.
