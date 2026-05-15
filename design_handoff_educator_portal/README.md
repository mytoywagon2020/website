# Handoff: My Toy Wagon Educator Portal

A design package for the educator/B2B side of My Toy Wagon — the family-run heirloom toy shop in Arcadia, California. This bundle covers the educator portal, quote-to-order flow, and procurement back matter intended for school and institutional buyers.

---

## About the Design Files

The files in `designs/` are **design references created in HTML.** They are prototypes showing intended look and behavior — not production code to ship directly. Your task is to **recreate these designs in the My Toy Wagon Shopify store** using Shopify's **native B2B features** (Companies, Catalogs, Payment terms) and standard theme/extension patterns:

- **Liquid theme** for the marketing pages (homepage, catalog, schools landing page, procurement guide)
- **Customer Account UI Extensions** for the educator portal (dashboard, quote builder, vendor profile)
- **Native Draft Orders** for the quote → PO → order flow — built by the customer in their B2B account
- **Companies, Locations, and Catalogs** for educator status, account type, pricing tiers, and payment terms

See `SHOPIFY_NOTES.md` for the full B2B-native implementation guide.

---

## Fidelity

**High-fidelity.** All mocks are pixel-perfect with final typography, color, spacing, and copy. Treat the spec below as authoritative.

---

## Overview

My Toy Wagon serves three customer types: retail (DTC), educators (schools, therapists, homeschool co-ops), and wholesale. This handoff covers **the educator side only**:

1. **Public marketing pages** — Schools landing page, procurement guide, catalog back matter. These convince buyers to apply.
2. **Educator account flow** — Apply for an account → 1–2 day verification → sign in.
3. **Educator portal** — Once signed in, the customer sees a different experience: educator pricing on every product, a quote builder, vendor profile (W-9, COI, etc.), order history, and account settings.
4. **Quote → PO → Order workflow** — Educator builds a quote; we hold it as a Shopify draft order; school sends PO; we convert to order and ship.

---

## Screens / Views

### 1. Schools Landing Page (`ordering-for-schools.html`)

**Purpose:** Convince a school's purchasing officer that we are a viable vendor. Provide entry points to apply, download the procurement guide, or upload a vendor form.

**Layout:** Single scrolling page, 1100px max-width content, cream background `#F5F0E5`.

**Sections (in order):**
- Cover hero — title, dek, "Back to shop" link
- Story still-life — left: portrait specimen-cabinet image (4:5 aspect); right: editorial paragraph on cataloging
- 4-step procurement process (account → quote → PO → fulfillment)
- Procurement guide download CTA — dark ink-colored panel with vendor-form upload zone + "Email your form" mailto
- Procurement notes — 9 cards in 2-col grid: stock confirmed, pricing held 30 days, substitution policy, multi-classroom shipping, sole-source letters, tax-exempt, sustainability, cancellation policy, payment terms
- "References available on request" single italic line
- Resources list — W-9, COI, tax-exempt certificate downloads
- Contact section — emails + phone + Calendly-style "Schedule a 20-minute call"

**On Shopify:** Liquid template (`page.schools.liquid` or a custom section). Static content. Use Shopify pages with custom Liquid sections. The vendor-form upload zone wires to a Shopify Form (or a third-party form like Typeform) submitting to accounting@.

---

### 2. Procurement Guide (`procurement-guide.html`)

**Purpose:** Printable 5-page document for AP teams to file with vendor onboarding paperwork.

**Layout:** Five 8.5×11" pages, served as HTML with a "Print or save as PDF" button.

**Pages:**
1. Cover — logo masthead, "Procurement, plainly stated.", business info, doc version, pull quote
2. Welcome letter from Irfana & Rashid
3. 4-step process + payment terms table
4. Procurement notes (9 cards)
5. Contacts directory + 20-minute call CTA

**On Shopify:** Render as a Liquid template OR pre-generate a static PDF that gets served from Shopify Files. Recommendation: **pre-generate the PDF** quarterly and serve from Shopify Files; the HTML version stays for reference at `/pages/procurement-guide`.

---

### 3. Catalog Back Matter (`catalog-back-matter.html`)

**Purpose:** Chapters 6–9 of the catalog. Convinces catalog readers to apply for educator pricing and links them to the portal via QR codes.

**Layout:** Same as the schools page — scrolling sections, 1100px max-width.

**Chapters:**
- Ch 6 — Educator addendum (dark gate panel) with 2 QR codes:
  - QR 1: `mytoywagon.com/educator` ("Register or sign in")
  - QR 2: `mytoywagon.com/procurement-guide` ("Procurement guide")
- Ch 7 — How it works (4-step process flow)
- Ch 8 — Procurement notes (10 cards)
- Ch 9 — Contacts directory + 20-min call CTA

**On Shopify:** This is part of the printed catalog flow. The HTML is the design reference; the actual catalog is a PDF/print piece designed in InDesign. Recreate the visual style in print, but **the QR codes must resolve to working URLs on the Shopify store.**

QR target URLs must work:
- `mytoywagon.com/educator` → educator apply/sign-in page (built on Shopify customer accounts)
- `mytoywagon.com/procurement-guide` → static PDF or HTML page

---

### 4. Educator Apply / Sign In (`educator.html`)

**Purpose:** Account-creation funnel. Schools, therapists, and homeschool families apply for educator access. Verification takes 1–2 days.

**Layout:** Single page, cream background, with sections for:
- Hero with type-of-customer toggles (School / Therapist / Homeschool co-op)
- Benefits list (volume pricing, Net-30/60, vendor-form turnaround, etc.)
- Apply form OR Sign-in form (`#apply` or `#signin` anchors)

**Form fields (apply):**
- Organization name, type (school / therapist / homeschool co-op)
- Contact name, email, phone
- Role / title
- State + tax-exempt status
- For schools: district, grade levels served, enrollment range
- For therapists: license type and number
- For homeschool co-ops: number of families
- Notes / how they heard about us

**On Shopify:**
- Use **Shopify Customer Accounts** for sign-up + sign-in.
- The "apply" form should write to a custom Shopify metafield set on the customer record: `educator.application_status` = `pending`, with all application fields stored in customer metafields.
- A staff member reviews in Shopify admin → flips `educator.status` to `verified` and `educator.terms` to `net30`/`net60`/`prepaid`.
- Once verified, the customer's price list changes (see "Educator pricing" below).

---

### 5. Educator Dashboard (`educator-dashboard.html`)

**Purpose:** The home page after sign-in. Shows account summary, active quotes, recent orders, and access to the portal's sub-pages.

**Layout:** Two-column. Left sidebar (260px) with navigation; right main area with summary cards and a list of quotes/orders.

**Sidebar nav:**
- Dashboard (active)
- Educator catalog
- Quotes
- Orders
- Vendor profile (W-9, COI)
- Account settings
- (Below divider) Talk-to-our-team card with **Schedule a call** button (Calendly integration)

**Main area:**
- Greeting + account meta (org name, Net-30/60 status, sales rep)
- "How quotes become orders" explainer with two side-by-side definition cards: Draft (quote) vs Order (PO confirmed)
- Quote list (with status pills: Draft, Submitted, Approved, Converted)
- Recent orders list

**On Shopify:**
- Build as a **custom Shopify app** (embedded in customer accounts) OR as a Shopify Theme section with a customer-account-extension. Shopify Plus has full Customer Account UI extensibility.
- For non-Plus: build a custom embedded app authenticated via Shopify Customer Accounts API. Render at `/account/educator-dashboard`.
- "Quotes" list is **Shopify Draft Orders** filtered by `customer.id` and a custom metafield `draft_order.is_educator_quote` = true.
- "Recent orders" is the standard Shopify customer orders list.

---

### 6. New Quote (`new-quote.html`)

**Purpose:** Quote builder. Educator searches products, adds with quantity, sets quote metadata, adds notes, submits.

**Layout:** Two-column. Left main (1fr) with quote form; right sidebar (380px) with summary card.

**Main area:**
- Breadcrumbs + page heading
- "Connected to Shopify" status banner ("draft order will be created in admin on submit")
- Metadata card — Quote name, For (program/classroom), Needed by date
- Product search (autocomplete against the educator catalog)
- Line items table — Thumb, product name/SKU, Qty, Educator price, Total, Remove
- Notes textarea
- "How quotes become orders" reminder note

**Sidebar:**
- Quote summary — items, units, subtotal, educator discount, estimated total
- Submit / Save draft buttons
- "Need help?" link

**On Shopify:**
- On submit, hit the **Shopify Admin GraphQL API** to create a Draft Order:
  - `draftOrderCreate` mutation
  - Set `customer.id` to the signed-in educator
  - For each line item: `lineItems[].variantId`, `lineItems[].quantity`, `lineItems[].appliedDiscount` (for the educator price difference)
  - Set `note` to the notes field
  - Set custom attributes: `quote_name`, `for_program`, `needed_by`
  - Set tags: `educator-quote`, `pending-review`
- The created draft order shows up in Shopify admin → Orders → Drafts. Your team reviews, confirms stock and pricing, sends the customer an itemized invoice email.
- On PO receipt, your team **completes the draft** (`draftOrderComplete` mutation) → converts to an order → fulfillment begins.

---

### 7. Vendor Profile (`vendor-profile.html`)

**Purpose:** Single page that any AP team can find with the school's vendor onboarding info — W-9, COI, banking, contacts, tax ID. This page is meant to be share-friendly (a link AP teams can email each other).

**Layout:** Single column, ~700px wide content. Sections:
- Business info (legal name, DBA, address, tax ID, DUNS, NAICS)
- W-9 download
- COI download
- Remit-to info (check + ACH)
- Tax-exempt purchasing
- Sustainability certifications
- Contact directory (educators@, accounting@, contact@)

**On Shopify:**
- Liquid template at `/pages/vendor-profile`. Static content with downloadable PDFs hosted in Shopify Files.
- Or restrict access to verified educator customers only via a Liquid `customer.tags contains 'educator-verified'` gate.

---

## Critical Workflows

### Workflow 1: Educator account creation

1. Anonymous visitor → `/educator` → apply form
2. Form submission → Shopify customer account created with `customer.metafields.educator.application_status = "pending"`
3. Staff member in Shopify admin reviews application, sets `educator.status = "verified"` and `educator.terms = "net30"`, tags customer with `educator-verified`
4. Verification email sent to customer
5. Customer signs in → sees educator pricing across catalog

### Workflow 2: Quote → PO → Order

1. Signed-in educator → New Quote → adds items → Submit
2. Shopify Draft Order created via API with `tags: ["educator-quote", "pending-review"]`
3. Internal team reviews draft order, confirms stock, sends customer the itemized quote (Shopify email invoice)
4. School issues PO referencing the quote/draft number; emails to accounting@
5. Team attaches PO to draft order in admin, then **completes the draft** → converts to a Shopify order
6. Fulfillment begins; invoice with Net-30/60 terms is generated
7. Customer can see the order in their portal under "Recent orders"

### Workflow 3: Educator pricing

1. On verification, customer gets tag `educator-verified` AND a tag for their tier (e.g. `educator-tier-1`, `educator-tier-2`)
2. Product pricing is shown via a **Shopify B2B catalog** (Shopify Plus) OR via **Bold Custom Pricing / Wholesale Helper** app for non-Plus
3. Storefront theme reads `customer.tags` to decide whether to show educator pricing
4. Cart and Draft Order line items use educator price automatically

---

## Design Tokens

### Colors
| Token | Hex | Use |
|---|---|---|
| `--cream` | `#F5F0E5` | Body background |
| `--warm-white` | `#FFFCF7` | Card backgrounds, light surfaces |
| `--ink` | `#2C2C2A` | Primary text, dark backgrounds, primary buttons |
| `--forest` | `#3B6D11` | Accent (active nav, success, hover) |
| `--amber` | `#854F0B` | Secondary accent (alerts, callouts) |
| `--stone` | `#5F5E5A` | Secondary text, captions |
| `--card-bg` | `#EDE3CD` | Section dividers, secondary surfaces |
| `--rule` | `rgba(44,44,42,0.12)` | Subtle borders |
| `--rule-strong` | `rgba(44,44,42,0.22)` | Stronger borders, button outlines |

### Typography
- **Cormorant Garamond** (400/500/600 + italics) — All display, headings, italic accents, brand wordmark
- **Mulish** (400/500/600/700) — Body text, UI labels, navigation, buttons

| Use | Family | Size | Weight | Style |
|---|---|---|---|---|
| Hero h1 (60-80px) | Cormorant Garamond | clamp(48,8vw,80px) | 500 | regular + italic em |
| Section h2 (36-54px) | Cormorant Garamond | 36-54px | 500 | regular + italic em |
| Card title h3 | Cormorant Garamond | 20-24px | 500 | italic |
| Body | Mulish | 14-16px | 400 | regular |
| Italic prose (lede, captions) | Cormorant Garamond | 14-20px | 400 | italic |
| Label (eyebrow) | Mulish | 10.5-12px | 500-600 | uppercase, letter-spacing 0.16-0.18em |
| Button | Mulish | 12-13px | 500 | uppercase, letter-spacing 0.1em |
| Wordmark | Cormorant Garamond | 18-22px | 500 | uppercase, letter-spacing 0.22-0.24em |

### Spacing
- 4-pt base. Common increments: 4, 8, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 48, 64, 80, 96, 120
- Section vertical padding: 80-120px on desktop, 64px on mobile
- Card internal padding: 24-32px
- Page max-width: 1100-1440px (content), 880px (centered text blocks)

### Border radius
- All elements: `2px` (intentionally tight; gives a printed-paper, not web-app feel)
- No rounded buttons, no pill shapes

### Shadows
- Almost none. Use `0.5px solid var(--rule)` borders instead of shadows for separation
- Exception: print page mockups in procurement-guide.html use `0 6px 30px rgba(0,0,0,0.15)` for the page-on-table effect

### Logo
- `assets/logo-mark.png` — square mark, used as a CSS mask so it inherits ink color
- `assets/logo-wordmark.png` — text-only wordmark
- `assets/logo-primary.png` — full lockup
- Use mark + Cormorant Garamond wordmark composition (see procurement guide header for canonical example)

---

## Email Routing

Three specialized inboxes — wire mailto links and Shopify notification settings accordingly:

| Inbox | For |
|---|---|
| `educators@mytoywagon.com` | Quote-building, classroom orders, curriculum-aligned procurement, school-specific questions |
| `accounting@mytoywagon.com` | W-9, vendor onboarding forms, COI requests, remit-to info, invoice questions, payment terms |
| `contact@mytoywagon.com` | General inquiries — retail orders, returns, product questions, press, partnerships |

---

## Business Info

```
My Toy Wagon, LLC
37 W Huntington Drive
Arcadia, California 91007
Phone: 626.841.0421
Tax ID: 87-3421098
```

---

## Files in this bundle

In `designs/`:
- `educator.html` — Apply for an educator account / sign in
- `educator-dashboard.html` — Portal home (sidebar nav, summary cards, quotes list)
- `new-quote.html` — Quote builder
- `vendor-profile.html` — W-9, COI, tax-exempt info for AP teams
- `ordering-for-schools.html` — Public schools landing page
- `procurement-guide.html` — 5-page printable procurement document
- `catalog-back-matter.html` — Catalog chapters 6-9 (educator addendum, how-it-works, procurement notes, contacts) with QR codes
- `assets/` — Logos, photos, and other media referenced by the designs

`SHOPIFY_NOTES.md` — Detailed Shopify implementation notes, API mappings, and architectural decisions to make before building.

---

## Open questions to confirm with the founders

1. **Confirm B2B plan tier** — Shopify plan name and that B2B Companies / Catalogs / Payment terms are accessible in admin.
2. **Calendly integration** — get the actual Calendly URL for "Schedule a call." Currently `href="#"` placeholder.
3. **QR code generator** — The catalog back matter uses qrserver.com. For print, generate higher-quality QRs from a library or InDesign.
4. **Vendor form workflow** — Confirm: do form uploads go to Google Drive, Dropbox, or just email to accounting@?
5. **Sales rep field** — One person for all educators, or assigned per Company?
6. **Pricing tiers** — How many Catalogs / pricing tiers do you want from launch (Standard / Tier 2 / Tier 3, or just one)?
7. **First test customer** — Identify one real verified educator to use for end-to-end testing.

---

*Last updated: May 2026. Designs are pixel-final.*
