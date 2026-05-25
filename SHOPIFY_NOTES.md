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

**Lifecycle:** Educator listings start `DRAFT` + `needs-price`. When priced, activate on the Educator catalog to go live. Portal card links are set by product **handle** in the templates now, so each card resolves the moment its educator listing is activated — no template change needed later.
