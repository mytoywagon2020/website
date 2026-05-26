# Educator Portal — Runbook, Tag Reference & Red Flags

Operating notes for the gated Educator Portal (theme layer + native B2B). Keep current.

---

## Status tag reference (orders)
The dashboard reads these so educators see true status **without** changing native Shopify
payment state (see Red Flag #1). Add in admin: Orders → select → Add tags.

| Tag | Where set | Dashboard effect |
|---|---|---|
| `invoice-sent` | order | Payment column shows **Invoiced** (still counts as open invoice) |
| `po-paid-external` | order | Payment shows **Paid**; removed from Open invoices + outstanding total |
| `fulfilled-external` | order | Marks **Fulfilled** only if you shipped *outside* Shopify (rarely needed — native fulfillment + tracking is read automatically) |
| `school order` | order | (existing) internal label for educator/PO orders |

Fulfillment/tracking is read **natively** (Fulfilled / Partially shipped / Processing + tracking links + "N items still to ship"). No tag needed for it.

## Customer / company tags & metafields
- Customer tag `educator-approved` → opens the gated portal (theme gate also accepts `customer.b2b?`).
- Customer tags `educator-pending` (applied, awaiting review) and `educator-rejected` (declined) for lifecycle filtering. **Do NOT add a Company `educator.status` metafield — redundant; these tags are the source of truth.**
- **Register form = Helium Customer Fields app** (owns the `customer_fields` namespace: `institution_name`, `document_upload`). **Paid monthly — leverage it fully (no extra tool/cost):** map ALL form fields (org/role/program/state) → **customer metafields** so Flow can auto-fill the Company with **no re-entry**, and use its **built-in file upload** for the **optional** cert. ⚠ Verify the field→metafield mapping is actually ON — recent signups showed those metafields empty (so they may be email-only).
- Customer metafield `educator.trusted_hold = true` → eligible for inventory hold before a PO (e.g., Erin Kim / Elk Grove).
- Product metafields: `educator.exclusive`, `educator.continue_selling`, `educator.delivery_model`, `educator.next_delivery`, `educator.terms`, `educator.min_qty`, `educator.curriculum`.

## Staff SOP — an educator order
1. Educator submits a quote (theme `/pages/new-quote` emails the team; or native B2B draft order).
2. Staff create/confirm an **unreserved draft order**, factoring shipping + tax; send the quote (price held 45 days).
3. Educator sends PO → staff record it; tag the order **`invoice-sent`** when the invoice goes out.
4. Fulfill in Shopify (with tracking) — dashboard shows it automatically.
5. When the check/ACH clears, tag **`po-paid-external`** → dashboard shows Paid. (Do NOT mark Paid natively — Red Flag #1.)
6. Inventory is allocated only at PO (or a `trusted_hold` arrangement).

---

## 🚩 Red flags / open items

1. **Shopify Capital payment workaround (TEMPORARY).** We do not mark PO orders "Paid" in Shopify because Shopify Capital remits a % on recorded sales we collected outside Shopify. Workaround: `invoice-sent` + `po-paid-external` tags drive the dashboard instead. **Remove this once the Capital loan is paid off** — then mark payments natively and retire the payment tags. (May end sooner if the program scales.)
2. **Quote visibility.** Theme quotes (draft orders) can't be shown via Liquid. Fix = **native B2B self-serve quoting** (available on this plan): educators as company contacts build/track quotes in their account. Until wired, rely on hard confirmation + emailed quote.
3. **Pricing display.** Price list is 0% + manual prices, and prices are volatile (tariff/freight), so no fixed catalog discount. Position educator **value** (PO/Net terms, tax-exempt, bulk/combined freight, curriculum letters, replacement parts, service) and label "educator pricing confirmed on your quote." Use **volume-based** quote pricing, not a flat %.
4. **Procurement self-justification.** AP/grant teams need one-click **PDF quote/invoice, W-9, COI, PO reference**. Shopify order pages provide printable invoices; draft-order invoices cover quotes. **W-9 + COI links PENDING** (owner doesn't have an updated W-9 yet; COI ~next week after insurance is set). Until then the dashboard/vendor-profile show an email-request fallback. When ready: Content → Files → upload → Copy link → wire one-click Download buttons.
5. **Reorder / saved classroom lists.** Schools rebuy seasonally. **Reorder** is native in the B2B customer account. **Saved/named "classroom lists"** likely need an **app** — see App recommendations below.
6. **Status-tag discipline.** The dashboard is only as accurate as the tags. Keep a saved admin view "PO orders missing payment tag." 
7. **Seasonal dates.** The Aug–Sep / May–Jun window + order-by dates are date-driven in the dashboard/PDP; verify rollover and keep editable.
8. **Launch dependency.** Everything is on the unpublished **Educator Portal Staging** theme; it all goes live when that theme is published (planned Tuesday). Connetix/bundles are draft + in the Educator Catalog market.

---

## App recommendations (where native isn't enough)
- **Saved/named classroom lists (wishlist/shopping lists):** native Shopify has no multi-list "saved lists." Recommend **Swym Wishlist Plus** (multiple named lists, reorder, B2B-friendly) or a B2B ordering suite like **BSS B2B/Wholesale Solution** (quick-order + lists). *Reorder alone may not need an app — the B2B account supports reordering past orders.*
- **PO file upload (customer-facing):** Shopify contact form can't attach files. Use **Shopify Forms** (native, supports file upload) or a **Tally** form (matches existing portal embeds). Staff attach emailed POs to the order/draft in admin.

---

## Architecture map — what's native vs theme (read this first in 6 months)
| Concern | Where it lives |
|---|---|
| Educator identity / approval | **Native** customer tag `educator-approved` + **native** B2B Company contact |
| Pricing / catalog access | **Native** B2B: "Educators" market (applies to ALL company locations) → Educator Catalog (`MarketCatalog/64883065002`) + price list `PriceList/24074289322` |
| Product availability (educator-only) | **Native** publication to the Educator Catalog + product status; **Theme** `educator.exclusive` gate as the storefront retail block |
| Gated portal pages (dashboard, catalog sections, quote) | **Theme** — `page.educator-*` templates + `snippets/educator-gate.liquid`, gated on `b2b?` or `educator-approved` |
| Order/invoice/fulfillment display | **Theme** dashboard reads **native** `customer.orders` + fulfillment/tracking; payment status via **tags** (`po-paid-external`, `invoice-sent`) |
| Quote building | **Theme** `/pages/new-quote` (email) **today**; target = **native** B2B self-serve draft orders |
| PO submission | **Theme** email (today); optional Shopify Forms/Tally upload |
| Crawl/SEO control | **Theme** `noindex` + `robots.txt.liquid` |

Source of truth for the catalog build: `EDUCATOR-CATALOG-WORKSHEET.md`. Page architecture: Program → Apply → Sign in → **Educator Dashboard** → Catalog / Quote / Orders.

## Erin Kim / Elk Grove (reference)
- Company: Elk Grove Elementary School (`Company/1464893610`); Location `CompanyLocation/1567097002`.
- Contact: Erin Kim (`Customer/8984220303530`, emaudlin@egusd.net) — tagged `educator-approved` + `educator.trusted_hold=true`.
- Orders (from completed B2B drafts #D395–397, all natively Fulfilled, payment pending, tag "school order"):
  - #24210 — $12,934.41
  - #24207 — $3,523.59
  - #24211 — $5,256.63
- To reflect reality on her dashboard: tag each `invoice-sent` (when invoiced) and `po-paid-external` (when paid). Tell me which are paid and I'll set them.
- Covered by the Educators market automatically (applies to all company locations) → Educator Catalog + price list.

## Easy path (RECOMMENDED DEFAULT — no app, no token, no Flow, no dev)
The only part that needs dev/token is auto-creating the Company. Skip it. Everything else is already automatic.
1. Applicant fills the **Helium form** → info saves to their **customer profile** automatically.
2. Notification arrives → glance + verify (email domain / quick lookup, ~30 sec).
3. **Add the `educator-approved` tag** to the customer. ← the one button.
4. **Done:** gate opens (login works) + **Educators Market applies educator pricing automatically** (no per-customer setup).
5. **Only if** they need **PO/Net-30** → create a B2B Company then; their details are already on the customer profile (copy-paste).

→ The Flow/`companyCreate` auto-populate below is an **OPTIONAL upgrade for later** (only worth it if step 5 is frequent; needs a Dev Dashboard app token).

## Tag vs. pricing vs. Company — what each actually does (read this)
Precise model (don't conflate these):
- **`educator-approved` tag** → opens the **gated catalog** (login + browse). One click, manual.
- **Educator pricing** → confirmed on the **quote** (your volume-based pricing), **not** a live storefront discount. The tag gets them *in*; you price the quote.
- **B2B Company** → carries **PO / Net-30 terms** + native self-serve quoting. In the easy path this is **manual, as-needed** — created only when a school is actually ready to order on terms (their details are already on the customer profile from Helium → quick copy-paste). Auto-creating it (Flow) is the **deferred automation**.

**So: the Company is NOT automated in the easy path — manual, on an as-needed basis.** The Flow that auto-creates a pending Company on every application is the piece that's deferred.

**Practical rhythm:**
1. Applicant applies (Helium) → tag `educator-approved` → they're in.
2. They request a quote → you price it.
3. First time they need a **PO/Net-30** → create their Company then (~2 min, copy-paste from their profile).

Most educators won't need a Company on day one — only when they place a PO. Manual is fine until volume makes the automation worth building. Nothing's broken by deferring it.

## Staff SOP — educator application, verification & approval
Frictionless apply; **documents collected at verification, not on the form** (the register form stays short; native theme forms can't upload files anyway).
1. Applicant submits the register form → lands as an **untagged customer** with org/role/program/state.
2. (Optional, via Flow) auto-tag **`educator-pending`** so they appear in a "to review" customer view.
3. **Verify (the one manual step) — documents are OPTIONAL.** Confirm legitimacy with the lightest sufficient signal (see "How we verify" below). Request a document only if unsure, or to enable tax-exempt checkout.
4. **Approve = add the `educator-approved` tag** (+ create/attach the B2B **Company** for PO/Net-30). Gate opens; the **Educators Market** applies pricing automatically.
5. Decline → tag **`educator-rejected`** (so they aren't re-reviewed).

**Approval/verification email (template):**
> Subject: Your My Toy Wagon educator application — one quick step
> Hi [name], thanks for applying! You're approved for **[organization]** — educator pricing and **Net-30 on purchase orders** are on. If you'd like **tax-exempt checkout**, reply with your **sales-tax exemption / resale certificate** and we'll add it (required by law to skip sales tax). Otherwise you're all set.

### How we verify (lightest → strongest; doc optional)
- **Institutional email domain** (`.edu`, `.gov`, `.k12.*`, school/district domain) — strongest low-friction signal; OK to fast-track.
- **Personal email** → ask them to confirm from / we send approval to their **institutional email**.
- **Public lookup** — confirm the institution exists: **NCES school directory** (US), state school directory, or the org's website/staff page; ideally confirm the person's role.
- **Role check** — staff directory or LinkedIn.
- **Optional document** — tax-exempt/resale cert, school ID, or PO on letterhead. **Required only to enable tax-exempt checkout** (legal: a valid exemption certificate must be on file to not charge sales tax). Account + pricing + Net-30 do NOT require it.
- **Behavioral guardrail** — first order prepaid/small; extend Net-30 after a clean payment.
- **Tiered rule:** auto-trust institutional-domain emails → light public lookup for personal emails → require the cert only for tax-exempt checkout.

## Auto-populate Companies + one-click approve — Flow wiring spec
**Goal:** applicant data auto-creates a **pending Company**; staff review + approve with one tag. **No app, no code — built in admin (Flow). Needs Shopify Plus.** (Claude cannot build Flows / mint the token / create metafield defs — these are admin steps.)

**Prereqs (one-time, admin):**
1. **Shopify Plus** (companyCreate is Plus-only).
2. **Helium Customer Fields:** map org/role/program/state → **customer metafields** (verify ON, not email-only).
3. **Admin API token:** Settings → Apps → Develop apps → create app → scope `write_companies` (+`read_customers`) → store token as a **Flow secret**.

**Flow 1 — "Create pending educator company"**
- Trigger: **Customer created**.
- ⚠ **Condition (critical — blocks bot/spam):** continue only if `customer.metafields.customer_fields.institution_name` is set (or a form-added tag like `educator-applied`). Without this, every signup makes a junk Company.
- Action: **Send HTTP request** → POST `https://<shop>.myshopify.com/admin/api/2025-07/graphql.json`, headers `Content-Type: application/json` + `X-Shopify-Access-Token: {{secret}}`, body:
```json
{ "query": "mutation($input: CompanyCreateInput!){ companyCreate(input:$input){ company{ id } userErrors{ field message } } }",
  "variables": { "input": {
    "company": { "name": "{{customer.metafields.customer_fields.institution_name}}", "note": "Educator application (pending). {{customer.email}}" },
    "companyContact": { "email": "{{customer.email}}", "firstName": "{{customer.firstName}}", "lastName": "{{customer.lastName}}" },
    "companyLocation": { "name": "{{customer.metafields.customer_fields.institution_name}}", "billingSameAsShipping": true } } } }
```

**Review + approve (the one button):** staff open the pending Company/customer → verify (see "How we verify") → add tag **`educator-approved`** → gate opens + Educators Market pricing applies. *(Optional Flow 2: on `educator-approved` tag → Send HTTP request to assign Net-30 `PaymentTermsTemplate/4` / finalize.)*

**Status now:** designed + spec'd + documented (here). **Not yet wired** — the Flow/token/Helium-mapping/metafield steps are admin tasks Claude can't perform.

### Flow 1 — click-by-click (admin; Claude CANNOT build this — hand to whoever has admin)
**Prereqs:** (1) Admin API token from a **Dev Dashboard app** with `write_companies` (legacy custom apps are closed as of 2026-01-01, so the old copy-paste token path is gone). (2) In **Helium**, on submit: add tag **`educator-applied`** (cleaner Flow trigger than a metafield condition) AND map org/role/program/state → customer metafields.
1. Admin → **Apps → Flow → Create workflow**.
2. **Trigger:** "Customer tags added" → tag `educator-applied`. *(Tag is more reliable than a metafield condition; alt: trigger "Customer created" + condition `customer_fields.institution_name` is not empty.)*
3. **Action: "Send HTTP request":**
   - Method **POST**
   - URL `https://mytoywagon.myshopify.com/admin/api/2025-07/graphql.json`
   - Headers: `Content-Type: application/json` and `X-Shopify-Access-Token: {{secret}}`
   - Store the Admin API token in the action's **secret** field.
   - Body = the `companyCreate` JSON in the spec above (uses `{{customer.metafields.customer_fields.institution_name}}`, `{{customer.email}}`, etc.).
4. **Turn the workflow ON.** Test: submit the form → a **pending Company** should appear in admin.
5. **Approve = add the `educator-approved` tag** (manual one-click). *(Optional Flow 2 on that tag → Send HTTP request to assign Net-30.)*

**Status: NOT built. This is the build checklist; Claude can't create Flows or the token (admin/dev tasks).**


## Register/quote forms = app/embed, NOT theme liquid (verified from theme 145914462378)
- `templates/page.educator-register.json` = placeholder rich-text ("Educator Account Registration / verification up to 3 business days") + an **"apps" slot** + two disabled sections. **No form liquid.**
- The visible application form is rendered by an **app/embed: Helium Customer Fields and/or Tally** (gate template `page.educator-portal.liquid` loads `tally.so/widgets/embed.js`). So **fields, logo, doc upload, and metafield-capture are configured in Helium/Tally — not theme code.** To confirm no-reentry: Helium form → each field → "save to metafield."
- `page.educator-portal.liquid` is the **gate** ({% layout none %}; closed if handle in `educator-dashboard,new-quote,...` or `page.metafields.educator.gated==true`; renders `{{ page.content }}` only for a customer tagged `educator-approved`).
- ⚠ **Routing mismatch to fix:** gate "Apply for access" → native `routes.account_register_url`; section-page "Apply" CTAs → `/pages/educator-program`. Point both at the same place.

**RESOLVED (2026-05):** Gate **"Sign in"** → `/pages/educator-login`; **"Apply for access"** → `/pages/educator-register`. Section-page "Apply" CTAs also → `/pages/educator-register`. Both pages exist and are verified. The native `routes.account_login_url` / `routes.account_register_url` defaults are **not** used on the gate — the educator-branded pages are canonical.

**Gate copy rule:** Full sentences, no em-dashes, no AI tells (see SHOPIFY_NOTES design rules).

## Pre-launch cert verification checklist (owner to confirm or remove)
- **FSC-certified** — Woodland (9), Nature (3), Sensory (4), STEAM (2), Creative Arts (2)
- **Fair Trade USA** — Nature (4), Small World (4), DP (3), STEAM (1), Woodland (1)
- **WFTO** — Nature (3), DP, Small World, STEAM, Woodland
- **BSCI** — Nature (1) — which product?
- ⚠ **IDEA Part B / Medicaid OT funding** — Sensory (2 each) — highest risk; verify or soften
- ⚠ **Junior Design Awards 2021** — Sensory (2) — **flagged for end**; verify the win or remove

---

## Educator listings — build SOP & conventions (employee-facing) — DECIDED 2026-05

**THE MODEL: every educator item is its OWN listing, fully separate from retail.**
- Educator listings are **made-to-order / pre-order**: variant **"continue selling when out of stock" = ON**, published to the **Educator catalog ONLY** — **never** on the retail Online Store. Schools order on their schedule; you fulfill from production/restock and **reconcile physical stock at the PO** ("allocate at PO"; use customer metafield `educator.trusted_hold` to set stock aside before a PO).
- **Never share one listing across retail + educator.** "Sell when out of stock" is a single **per-variant** setting (it hits every channel at once), and inventory is **one shared pool per variant** — there is **no per-channel or per-location inventory fence on our plan** (confirmed). So a shared listing can't be *retail-accurate* AND *educator-pre-order* at the same time. Two listings is the only clean way: retail keeps its real stock (stops at 0); the educator twin is its own pre-order pool. **An educator order never touches retail stock** (different SKUs). Keeping them separate is also less work than juggling shared stock.

**Build each educator listing FROM the retail listing — not a thin stub:**
1. Copy the retail listing's **full description + all images**.
2. **Clean** it: delete shipping/stock/dropship lines ("ships from our partner warehouse", "two shipping options", "limited quantity in stock", "pre-order for [holiday]"); drop the maker brand from the body **unless it's marquee** (Connetix, Bauspiel, Grimm's, Holztiger, Tara Treasures).
3. Append the **educator note**: *"Made to order for classroom use — always available to order on your school schedule. Net-30 and tax-exempt purchasing available for approved educators."*

**The 5 markers — apply to EVERY educator listing:**
| Field | Value |
|---|---|
| **Title** | clean product name — **NO "(Educator)" suffix** |
| **Vendor** | **My Toy Wagon** (one-click "filter all B2B by vendor"; also our true vendor once we manufacture) |
| **Product Type** | **Educator** (secondary identifier + Type-column filter) |
| **Tags** | `educator-only` (primary filter) + `educator-<section>` + **maker brand** tag (e.g. `ButtonandBug`, so staff know the real maker) + age tags |
| **Handle** | `-educator` suffix |

Plus: status **ACTIVE**, variant **inventory policy = continue selling**, published to the **Educator catalog** (`Publication/152026382506`) only. Price = **regular** price (never a retail sale price).

**Tell educator vs retail apart in admin:** filter **`tag:educator-only`** (save as a view "Educator"); or Vendor = **My Toy Wagon**; or Product Type = **Educator**; or handle ends `-educator`. On the storefront, educator listings are off the public store entirely (retail can't see them; they don't appear in retail search).

**Collective (dropship) items:** never link/reuse a Collective listing for educator — build a **fresh** educator listing (a dropship item can't be made-to-order/educator-only). **All Tender Leaf items are Collective → create new**, EXCEPT the **Botanical Press** (old shop-owned listing, not Collective).

**Technical do/don't (API — learned the hard way):**
- **Never activate an existing *retail* draft to "make it educator."** Retail drafts carry every sales channel, so activating them **leaks them onto retail** — and **`publishableUnpublish` is BLOCKED** (you can't pull it back via API). Instead use a clean stub or a **freshly created** product (both start with **zero** channels) and publish ONLY to the Educator catalog.
- `productCreate` = clean (no channels). `productDuplicate` = **inherits ALL the source's channels** — don't use it for educator items.
- Activating any product **auto-adds it to the "Microsoft Copilot" channel** (that channel auto-publishes). Turn that toggle off in admin if unwanted (it's not the retail storefront).
- The gated educator **pages** were leaking into on-site search; fixed in the staging theme `snippets/collection-grid.liquid` + `snippets/search-results.liquid` (skip `educator*` / `new-quote` / `vendor-profile`). The **live** theme needs the same paste (API can't write the published theme) — or it carries over when the staging theme is published.

**Plan facts (confirmed):** B2B (Companies, Catalogs, Net-30 = `PaymentTermsTemplate/4`) **works on our Grow plan**, with a **3-catalog limit**. Multi-location inventory is available, but there is **no** per-channel/per-location inventory reservation on any plan. *(Correction: the "Needs Shopify Plus / companyCreate is Plus-only" lines in the Flow section above are **stale** — B2B is live on Grow; Elk Grove proves it.)*

---

## Where the applicant's form data lives (Helium vs Shopify)

The Helium "Educator Application" form writes some fields to the **Shopify customer record** and some are only stored in **Helium's submission log**. Both matter when verifying an applicant.

**On the Shopify customer record (the verification essentials):**
- First name, Last name, Email, Phone (native customer fields)
- Full address (`default_address.address1` / `city` / `province` / `zip` / `country`)
- `customer_fields.institution_name` (the school name)
- `customer_fields.document_upload` (the tax-exempt cert, if uploaded)
- `customer_fields.form_ids` (Helium's origin tracker, value `["pvtAWd"]`)

**In the Helium app's submission log (the rest of the application):**
- Role or title
- Program or grade levels
- Anything else captured by the form that isn't bound to a native Shopify customer field

**To review an applicant's full application:**
Helium app → **Submissions** (or "Form submissions" in the left nav) → **Educator Application** → click the submission. Every form field they entered is there, including Role and Program. Treat it as the applicant's "application file." The customer record has the verification essentials. Helium has the full form context. Cross-reference both when approving.

## How to approve an applicant (the one-click action)

1. Admin → **Customers** (your main Shopify admin, not in Helium).
2. Click the applicant (or filter the list by **`tag:educator-pending`** to find everyone waiting).
3. In the **right sidebar**, find the **Tags** section.
4. Type **`educator-approved`** and press Enter to add the tag.
5. **Save** (top right).

Done. The gate opens for that customer and the Educators Market applies its pricing automatically. No other steps are required.

**Batch version (multiple applicants at once):**
1. Customers list → filter by **`tag:educator-pending`**.
2. Tick the checkboxes for the ones you are approving.
3. **More actions** at the top → **Add tags** → enter `educator-approved` → Apply.
4. Optional: also bulk-remove the `educator-pending` tag in another pass so the pending view stays clean.

## Note on B2B Companies (rare, on-demand)

Approving an educator does **not** create a B2B Company. That is a separate workflow used only when an educator specifically needs **Net-30 or PO billing**. Path: **Admin → Companies → Add company**, copy-paste their details from the customer record, set Net-30 payment terms. Skip this step until a school actually requests PO/Net-30. A Company showing as "Not approved" in the Companies list is unrelated to whether the educator catalog access works for that buyer; the customer tag is the only gate key.
