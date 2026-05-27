# Launch Follow-Ups — Educator Portal

A single source of truth for what's been built, what's pushed live, and what you still need to action before/after launch. Mirrors the Lakeshore-comparable feature set we worked through.

**Read this in tandem with:**
- `EDUCATOR-PORTAL-RUNBOOK.md` (architecture)
- `LAUNCH-OPS-SOP.md` (human workflows)
- `CLAUDE.md` (hard rules)

---

## Status legend
- ✅ **Done & pushed live** to staging theme (`Educator Portal Staging — UNPUBLISHED`)
- 🟡 **In repo, NOT pushed** (need either GitHub theme integration, paste via Shopify code editor, or shopify CLI)
- ⏳ **Specced, not built** (waiting on your input)
- 🔵 **Your action required** in Shopify admin / third-party tools

## Public vs gated — which pages are SEO-indexable

| Page | Gated to educator-approved? | Indexable by Google? |
|---|---|---|
| `/pages/funding-your-classroom` (hub) | NO | ✅ Yes (intentional SEO play) |
| `/pages/donorschoose-for-classrooms` (deep) | NO | ✅ Yes |
| `/pages/grants-for-natural-materials-classrooms` (deep) | NO | ✅ Yes |
| `/pages/educator-program` (apply for account) | NO | ✅ Yes (already in retail nav/footer) |
| `/pages/vendor-profile` | YES | No (closed-portal nav, gated) |
| `/pages/educators` (landing) | YES | No |
| `/pages/educator-dashboard` | YES | No |
| 8 section pages | YES | No |
| `/pages/new-quote` | YES | No |

**Deliberate split**: top-of-funnel (public + indexable) → portal (gated). Funding pages drive SEO traffic to the portal door; everything past the door is private.

## Retail footer — add the four educator links

See `RETAIL-FOOTER-SNIPPET.md` in this folder for the exact HTML and SEO logic. Summary:
- 🔵 **You: add a "For educators" link group to your retail theme footer** with these four links:
  - Apply for an educator account → `/pages/educator-program`
  - Funding your classroom → `/pages/funding-your-classroom`
  - Vendor profile → `/pages/vendor-profile`
  - Contact accounts payable → `mailto:accounting@mytoywagon.com`
- This is the SEO connection — it tells Google these pages are first-class assets and passes some homepage authority to them.

---

## The 10 Lakeshore-comparable features

### 1. Grant / funding guidance pages (hub-and-spoke, 3 pages total)
Public/indexable funnel-top assets. NOT gated. Drive SEO traffic to the portal door.

**Hub page**: `/pages/funding-your-classroom` — overview of 6 programs
- ✅ Template pushed (staging + repo) + pasted to live theme
- ✅ SEO title updated: *"Funding Your Classroom: Title I, ESSER, DonorsChoose & Grants for Hand-Made Materials"*
- ✅ Internal links added to deep pages
- 🔵 **You: create the page record** in admin (Pages → Add → template `page.funding-your-classroom`)

**Deep page A**: `/pages/donorschoose-for-classrooms` — DonorsChoose deep dive
- ✅ Template pushed + committed (19 KB)
- Includes: 4-step how-it-works, 5 winning-project tips, 6 sample project item lists keyed to our 8 sections, DonorsChoose disclosure (we are NOT a DonorsChoose-approved vendor — page is purely educational)
- 🔵 **You: create the page record** in admin (Pages → Add → template `page.donorschoose-for-classrooms`)

**Deep page B**: `/pages/grants-for-natural-materials-classrooms` — foundation + federal grants deep dive
- ✅ Template pushed + committed (22 KB)
- Includes: 6 grant cards (Title I, ESSER, NEA Foundation, McCarthey Dressman, Fund for Teachers, Voya Unsung Heroes) with award sizes + cycles + MTW catalog-fit; 5 application-writing tips; 3 sample budgets ($500 / $2,000 / $5,000+)
- 🔵 **You: create the page record** in admin (Pages → Add → template `page.grants-for-natural-materials-classrooms`)

**Future-investigation TODO**: DonorsChoose vendor application
- We are NOT currently a DonorsChoose-approved vendor
- If accepted into their vendor catalog, teachers could buy MTW materials directly through funded DonorsChoose projects (separate funnel)
- Apply via donorschoose.org/about/partners

### 2. Vendor packet & remit-to (TWO-TIER DISCLOSURE PATTERN)
**Important:** Bank account / routing numbers are NOT published publicly. Public Shopify Files URLs would expose them to any scraper. Pattern used:
- **Public on `/pages/vendor-profile`:** EIN, legal name, mailing/remit-to address, contact, W-9/COI/resale by email request
- **Bank/ACH/wire details:** sent ONLY on request from a verified school/district email after vendor setup is approved
- ✅ Vendor-profile page updated live with this pattern (Remit-to card live; EIN 87-4237224 visible; mailing 288 E Live Oak Ave Ste 119 Arcadia CA 91007; closed-portal nav applied)
- 🔵 **Optional follow-up:** assemble a public-safe vendor packet PDF (W-9 + COI + remit-to + EIN + NAICS — NO bank info) and upload to Shopify Files; share URL; I'll add a "Download vendor packet" button. Even this PDF should NOT contain bank info.

### 3. Self-serve tax-exempt cert upload (Helium)
- ✅ Template pushed (staging) + committed: `templates/page.tax-exempt-upload.liquid` (12.5 KB)
- ✅ Helium config spec written: see `HELIUM-TAX-EXEMPT-CONFIG.md` for the full step-by-step
- Page is gated to educator-approved customers; includes a Helium form embed container, three sidebar info cards (what we accept / how verification works / what might delay it), and an email-fallback path to `accounting@` that works even before Helium is configured
- Status pill at the top of the page shows current cert state based on customer tags (`tax-exempt-pending` / `tax-exempt-verified`)
- 🔵 **You: create the page record** in admin (template: `page.tax-exempt-upload`, URL: `tax-exempt-upload`)
- 🔵 **You: configure Helium form** per `HELIUM-TAX-EXEMPT-CONFIG.md` (5 metafields + 6 form fields + on-submit tag/event + bind to `#helium-tax-exempt-form` container + enable Helium app embed in live theme)
- 🔵 **You: build Klaviyo expiration-reminder flow** (30 days before `educator.tax_exempt_expires`)

### 4. Printable PDF quote
- ⏳ Deferred to staff workflow (no code change)
- 🔵 **You: use Shopify draft-order "Send invoice" feature** when replying to quote requests
  - Customers → Draft orders → Create draft order → Add educator's items + educator pricing
  - "Send invoice" generates a PDF and emails it
  - That PDF is what they send to their admin for approval
- Future enhancement (post-launch): wire a Liquid email template via Klaviyo for branded quote PDF

### 5. Print catalog request form
- ✅ Form pushed in landing v2 (form + email field in `/pages/educators` footer)
- 🔵 **You: build the Klaviyo flow**
  - Trigger: `Submitted Form` where `mailing_address contains "REQUEST_PRINT_CATALOG"`
  - Action 1: notify fulfillment via internal email (`fulfillment@mytoywagon.com`)
  - Action 2: add subscriber to "Print Catalog Requested" list
  - Action 3 (optional): auto-reply asking for confirmed shipping address

### 6. Lead time pill on section heros
- ⏳ NOT YET PUSHED (8 section files exceed MCP push limit — see "Theme push workflow" below)
- Once pushed, each section hero gets a pill:
  - Sensory Play / Nature Play / Woodland / Small World / Fairy Villages: *"Ships from our LA workshop in 1–2 weeks"*
  - **Connetix**: *"Connetix · 2–3 week ship from CA"* (not made-to-order; just longer lead time)
  - **Papoose**: *"Papoose · hand-felted, allow 5–6 weeks"*
  - **Bumbu / Drewart / Buttonandbug / June & December**: *"Hand-made in small batches · 3–4 weeks"*

### 7. PO # lookup + "Order again" on dashboard
- ✅ Built and committed (page.educator-dashboard.liquid)
- ✅ Pasted into live theme by owner
- Includes:
  - MAP-protected trust strip with 10% bundle savings pill
  - "Contact your educator team" mailto CTA pre-filled with customer email
  - PO# / order# client-side filter input above the orders table
  - "Reorder" button on each past-order row — re-adds every line item to cart via POST to `/cart/add`
  - PO tag surfaced inline on each order row (parsed from `po-XXXX` order tag)

### 8. Chatbot for B2B
- 🔵 **Tidio + Lyro AI** chosen (free tier, AI-powered, page-targeted)
- 🔵 **You: sign up at tidio.com (free)**, install, then paste their JS snippet into the `mtw-educator-header` section (NOT into `theme.liquid` — that would load on retail too)
- Configure Lyro to ingest: this runbook, `LAUNCH-OPS-SOP.md`, the funding page copy, Net-30 / tax-exempt FAQs
- Free tier: 50 AI conversations / month — sufficient for launch
- Existing retail AI bot stays untouched
- ❌ **Shopify Inbox** decided AGAINST — single-instance per shop, retail-flavored, no portal isolation

### 9. Bundle savings visibility (10% off bundles)
- ✅ "Saves 10%" pill on every Vol card on `/pages/educators` (8 pills, top-right of cover image)
- ✅ MAP-protected explainer line in landing intro: *"Curated bundles ship together at 10% off the individual price. Single items hold their full price so the makers we represent stay supported."*
- ⏳ Anchor pricing ("$487 · was $541 · saves $54") — placeholder CSS hook in place; **needs your bundle totals**:
  - 🔵 **You: provide per-volume bundle totals** (was/now per Vol 01–08) so I can populate the anchors
  - Format: `Vol-01 Sensory Play: total $X, anchor was $Y, customer saves $Z (10%)`
  - I'll store as shop metafields and render conditionally — until you set them, cards show the generic "Saves 10%" pill only
- ⏳ Trust strip on dashboard hero: *"MAP-protected pricing · 10% bundle savings"* — to add in dashboard push

### 10. Closed-portal rules
- ✅ Landing: logo → `/pages/educator-dashboard`, breadcrumb home → dashboard, "Back to shop" → "Sign out" (`/account/logout`), all absolute `mytoywagon.com` URLs converted to relative
- ✅ All 8 section pages: same rules applied (in repo, NOT pushed — see "Theme push workflow")
- ✅ Reviews carousel: fake seed reviews removed; replaced with placeholder until Klaviyo Reviews is wired
- ✅ Cover images: 8 sections show real images via `file_url` or `asset_url` (no frozen CDN URLs to break on re-upload)
- ✅ Pullout quote: *"You trust **our picks** more than you trust your research time."* (between hero and Vol grid)

---

## Theme push workflow

**The blocker:** The MCP harness available in this session can push files up to ~16 KB raw / ~22 KB base64 (verified by direct push of the 15 KB funding-page template). Larger files (the 8 section pages at 150–190 KB each, and the landing at 61 KB) require a different push path.

**Your three options to deploy the 8 section files + landing to a theme:**

### A. Shopify GitHub theme integration (recommended, set up once)
- Shopify admin → Online Store → Themes → Add theme → Connect from GitHub
- Connect to this repo's branch
- Every commit auto-syncs to the connected theme
- One-time setup, then we never have this problem again

### B. Manual paste via Shopify admin code editor (works now, tedious)
- For each file: Themes → Edit code → Templates → Add a new template (page) → paste contents from this repo
- 8 sections + landing + funding page = ~10 paste jobs

### C. Shopify CLI from your local machine
```bash
shopify theme push --theme=145914462378 --only="templates/page.*.liquid"
```
- Requires shopify CLI installed and authenticated on your computer
- One command, pushes all matching files

**Files currently in repo (need pushing via A/B/C):**
- `templates/page.educators.liquid` (61 KB — landing v2 with all features)
- `templates/page.educator-sensory-play.liquid`
- `templates/page.educator-nature-play.liquid`
- `templates/page.educator-woodland.liquid`
- `templates/page.educator-small-world.liquid`
- `templates/page.educator-fairy-villages.liquid`
- `templates/page.educator-steam.liquid`
- `templates/page.educator-dramatic-play.liquid`
- `templates/page.educator-creative-arts.liquid`
- `templates/page.educator-portal.liquid`
- `templates/page.new-quote.liquid`
- `templates/page.funding-your-classroom.liquid` (NEW — pushed to staging, also in repo)

---

## Section-by-section changes applied across the 8 section pages

Every section page (`page.educator-{section}.liquid`) had these fixes applied locally:

| Change | Why |
|---|---|
| Breadcrumb home → `/pages/educator-dashboard` (was `/`) | Closed portal — no retail-home leaks |
| All `https://mytoywagon.com/products/X` → `/products/X` (relative) | Keep educator in portal context for Market pricing |
| Retail-exit paragraph removed (*"Shopping for home? Browse the full retail shop"*) | Closed portal |
| `/pages/school-affiliate` references removed | Page is unpublished; the link was broken |
| `/collections/[name]` "Shop all" bridge CTAs removed | Avoid leaking to retail collection pricing |
| `https://mytoywagon.com` standalone → `/account/logout` (Sign out) | Sign out is the only intentional exit door |
| `{% section 'mtw-educator-header' %}` injected after `<body>` | Brand-consistent chrome |
| `{% section 'mtw-educator-footer' %}` injected before `</body>` | Brand-consistent chrome |

---

## What you need to provide to finish each TODO

| Item | What I need from you |
|---|---|
| Vendor packet PDF | Upload assembled PDF (W-9 + COI + remit-to + EIN + NAICS) to Shopify Files; share URL |
| Remit-to letter content | Legal business name, mailing address, EIN, ACH/wire bank info (or "leave bank info off, request directly") |
| Helium tax-exempt cert form | Confirm form created in Helium admin + share the form ID |
| Klaviyo print-catalog flow | Confirm flow built (trigger on `Submitted Form` with `mailing_address contains "REQUEST_PRINT_CATALOG"`) |
| Bundle anchor pricing | Per-Vol totals: `was $X / now $Y / saves $Z` for Volumes 01–08 |
| Tidio + Lyro install | Sign up + share the embed snippet for me to inject into `mtw-educator-header` |
| GitHub theme integration | Connect Shopify staging theme to a branch in this repo (Online Store → Themes → Add → Connect from GitHub) |

---

## Maintenance schedule (add to existing one in LAUNCH-OPS-SOP.md)

| Cadence | Action |
|---|---|
| **Monthly** | Audit bundle anchor pricing — refresh metafields if maker prices have shifted |
| **Each catalog request submission** | Confirm shipping address before mailing (Klaviyo flow handles auto-reply) |
| **Each tax-exempt cert upload** | Verify cert validity → add `tax-exempt-verified` tag → add exemption in Shopify Tax settings |
| **Each Tidio AI handoff** | Review AI chat transcript → expand Lyro training docs if a question came up that Lyro couldn't answer |
| **Quarterly** | Audit funding-page links → confirm each program URL still active |

---

## Quick-fix follow-ups not Lakeshore-specific but caught during this pass

- ⏳ Sensory-play / nature-play / steam pages all reference `/collections/[name]` bridge CTAs — those are removed in this push; replace with portal-internal CTAs (e.g., link to `/pages/new-quote?section=woodland`) if you want a parallel "request quote for whole section" prompt
- ⏳ Reviews carousel CSS + JS are still in the landing file (unused since we removed the seed reviews) — they're harmless; restore from git when Klaviyo Reviews is wired
- ⏳ Cover-image `srcset` for retina + mobile bandwidth — small Lighthouse score win, easy follow-up
- ⏳ Per-card "Add to wagon" button on section pages (Tier B+) — currently each card has "View product →" linking to PDP. The full per-item add-to-cart needs per-product variant_id which is brittle to maintain statically; defer until volume justifies it
