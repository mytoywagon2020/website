# Educator Portal: Live Status and Handoff Record

Single source of truth for the educator portal build. If you open a new
window or session, point Claude at this file first. Last updated by the
working session on 2026-05-18.

---

## 1. The workflow (agreed)

- All educator portal work happens on an **unpublished staging theme**, a
  byte-for-byte copy of the live theme. The live store is never touched by
  this work.
- You preview privately, and **you** publish when ready. Claude cannot and
  does not publish.
- If anything is wrong, the staging theme is deleted and nothing reached
  customers.

### Theme IDs

| Theme | ID | Role | Use |
|---|---|---|---|
| Current Shop with Impulse (9.0) | `145720180906` | MAIN (live) | Production. Never edited by portal work. |
| Educator Portal Staging (copy of live 2026-05-18) | `145914462378` | UNPUBLISHED | The portal build target. All edits go here. |

Older staging themes (`133950865578` "Impulse - Educators", `138552180906`
"Copy of Impulse") are stale and **not** in use for this build.

---

## 2. The reconciliation rule (Fast PDP rollout vs portal build)

Two layers, they do not collide:

- **Store data** (product metafields, `templateSuffix`, tags, SEO, page
  content, customers) is one shared copy. The Fast PDP rollout keeps
  writing this to the live store; the staging theme inherits it
  automatically. Nothing to reconcile.
- **Theme code** (Liquid, sections, templates, CSS) is per-theme. The
  staging theme is a snapshot taken 2026-05-18.

**Divergence risk:** only theme-code edits diverge. If Fast PDP theme files
change on live after the snapshot, the staging copy will not have them, and
vice versa.

**Operational rule:** before the portal theme is published, diff the live
theme's Fast PDP files against the staging copy and sync any drift forward,
so publishing the portal carries the latest Fast PDP code and nothing
regresses. Files to diff:
`sections/mtw-fast-pdp.liquid`, `assets/pdp-fast-1.css`,
`assets/pdp-fast-2.css`, `templates/product.fast-pdp.json`,
`templates/product.json`. If Fast PDP theme code changes a lot, the simpler
option is to re-duplicate live near publish time and re-apply the
self-contained portal files on top.

---

## 3. Verified Shopify configuration (Admin API 2026-05-18, owner-confirmed 2026-05-19)

- **Plan: "Shopify" (Grow). `shopifyPlus: false`, but native Shopify B2B
  IS available on this plan via Shopify Markets.** Owner-confirmed: the
  B2B is native Shopify (no third-party app), it comes with the plan
  through Shopify Markets, and the plan allows **up to 3 catalogs**.
- **Engine for Phase 2 is therefore native Shopify B2B** (Markets +
  Catalog + price list + Companies), within the 3-catalog cap.
- **Educator pricing data already exists:** an enabled **"Educators"
  market** (`gid://shopify/Market/32754958506`), the **"Educator"** market
  catalog (`gid://shopify/MarketCatalog/64883065002`), and a USD
  **"Educators Market" price list** (`gid://shopify/PriceList/24074289322`).
  Owner set the Educator catalog to all products, no customization
  ("Step 1").
- **The Educators market has no web presence** (`webPresence: null`).
  Pricing is configured but not yet deliverable through a storefront path.
  Wiring that delivery (signed-in approved educator sees educator pricing)
  is the core Phase 2 task, not the pricing math.
- **2 B2B companies exist** and are native Shopify B2B (no third-party
  app). RESOLVED: earlier "which B2B app" question is closed.

**Repo docs:** `SHOPIFY_NOTES.md` and `README.md` describe a Plus-native
B2B build. With native B2B available on Grow (3-catalog cap), most of that
guidance applies again, with two caveats to verify in admin: (a) the
3-catalog limit constrains the pricing-tier design to at most 3 tiers,
and (b) confirm which native B2B sub-features Grow includes (payment-terms
templates, customer-built draft orders) versus what must be staff-driven
via draft orders.

---

## 4. Phase plan

### Phase 1 (does not depend on the Plus question) - IN PROGRESS

- [x] Duplicate live theme to unpublished staging (`145914462378`).
- [x] Closed-portal gate added to `templates/page.educator-portal.liquid`
      on staging (see section 5).
- [x] Static funnel pages built/finished as UNPUBLISHED drafts from the
      `designs/` source (see section 10): schools, vendor-profile,
      procurement-guide. All `templateSuffix: educator-portal`,
      `isPublished: false`, assets mapped to Shopify CDN, content rules
      enforced (American English, no em-dash, no exclamation).
- [x] Catalog editorial page (catalog-back-matter) built as draft
      `educator-catalog-guide` with QR targets wired to the live
      educator-program and procurement-guide pages.
- [ ] Live published pages (educator-program, educator-register,
      educator-login, school-affiliate) — currently OPEN and ungated on
      live until the staging theme is published. Decide whether to refresh
      their content (a live change, needs explicit go-ahead) or leave.
- [ ] Preview pass on staging, then you publish.

### Phase 2 (engine decided: native Shopify B2B)

Dynamic, account-bound pieces: educator dashboard, tiered educator pricing,
quote to draft order, PO upload, document vault, Net-30.

Engine: **native Shopify B2B via Markets** (Companies + the "Educator"
catalog + "Educators Market" price list), within the **3-catalog cap** so
at most 3 pricing tiers. Approved educator signs in, is attached to a
Company so the Educator catalog pricing applies on the storefront. The
quote-to-PO flow uses **draft orders** (`draftOrderCreate`) with Net-30
payment terms and a PO number, matching `designs/new-quote.html`.
Confirmed available (see section 6.2).

**Architecture decision still open (the real Phase 2 fork):** Shopify does
not render Liquid inside page body content, so the dashboard and quote
builder cannot show real customer/quote/order data as draft *pages*. The
draft pages built now are faithful visual/flow scaffolds with honest copy
(quote submit is a mailto request; staff create the draft order with the
Educator price list and Net 30). Making them truly dynamic requires one
of: (A) the native B2B signed-in customer-account experience plus native
quotes/draft orders, (B) a Shopify app or app-proxy backend, or (C) keep
the staff-mediated request flow as v1 (zero custom code, works today).
Recommended: ship C now, layer A as the native B2B customer accounts are
configured. No commerce write path is wired until this is chosen.

---

## 5. The closed-portal gate (deployed to staging 2026-05-18)

File: `templates/page.educator-portal.liquid` on theme `145914462378`.

- A page is **closed** if its handle is in
  `educator-dashboard, new-quote, newquote, educator-quote,
  educator-quotes` OR `page.metafields.educator.gated == true`.
- `page.metafields.educator.gated == false` force-opens a listed page.
- Closed pages render only for a signed-in customer whose tags contain
  **`educator-approved`**, and carry `noindex, nofollow`.
- Three states: not signed in (sign in plus apply panel), signed in but
  not approved (under-review panel), approved (full page content plus
  Tally).
- Public funnel, apply, and marketing pages are unaffected and stay
  indexable, so SEO does not regress.
- Approval flow: applicant uses the apply form, staff reviews, staff adds
  the `educator-approved` tag to the customer in admin, the customer is in.

Login and register links use `routes.account_login_url` and
`routes.account_register_url` (Shopify system routes, correct on classic or
new customer accounts). No page handles were hardcoded as apply targets.

---

## 6b. Layer A finding (verified 2026-05-19)

- Customer merge: NOT possible via this API token (`read_customer_merge`
  scope denied). The duplicate Erin Kim must be merged in Shopify admin
  (Customers > merge, keep `emaudlin@egusd.net` / Elk Grove / $22,777.39).
- Elk Grove Elementary School company: 1 location
  (CompanyLocation/1567097002), `checkoutToDraft: true`, payment terms
  **Net 60**, and **catalogs: [] (none assigned)**. Root cause of "pricing
  configured but not delivered": no B2B catalog/price list is attached to
  educator company locations, so signed-in educators get no automatic
  educator pricing. Pricing is currently manual on draft orders.
- Layer A core action = create/assign a B2B companyLocation catalog with
  the educator price list and publish it to educator company locations
  (counts against the 3-catalog cap). This changes real buyer pricing, so
  it requires explicit owner sign-off on price list and Net terms before
  any mutation. Not actioned.

### Owner decisions 2026-05-19 (Layer A)

- **Educator pricing: DEFERRED by owner.** Market is volatile; tiered
  pricing cannot be promised. Do NOT configure a discount price list or a
  B2B pricing catalog. Operating model stays staff-mediated: educators
  checkout to draft orders, staff apply pricing manually. Revisit when the
  owner sets a policy.
- **Payment terms: keep existing as-is, adopt a terms ladder as policy.**
  Ladder: Prepaid or Due-on-receipt for the first order or any unverified
  account; Net 30 once verified (default for educator accounts); Net 60 by
  explicit approval for large orders (>= $10K trigger) or established
  district buyers with a PO on file and clean history. Elk Grove correctly
  stays Net 60 (large district buyer). Guardrails: require a PO for any Net
  terms, per-account credit ceiling, Net 60 is an approval step not a
  default, deposit for very large custom/heirloom orders. Policy only, no
  mutation; applied per account going forward.
- Net effect: Layer A plumbing is ready; pricing intentionally on hold;
  staff-mediated draft-order flow (option C) is the live model.

## 6. Open questions (need answers before Phase 2 build)

1. RESOLVED: B2B is native Shopify via Markets, no third-party app,
   3-catalog cap, catalog named "Educator".
2. RESOLVED (verified 2026-05-19 via Admin API): native payment-terms
   templates exist (Net 7/15/30/45/60/90, Due on receipt, Due on
   fulfillment, Fixed). Companies are real and transacting (Elk Grove
   Elementary School, 1 contact, 1 location, $22,624.35 spent). Draft
   orders work (existing #D2). Phase 2 engine confirmed: native B2B
   Company + Educator catalog/price list for pricing, plus draft orders
   with Net 30 (PaymentTermsTemplate id 4) for quote-to-PO.
3. **`MTW_Website_16.zip`** (uploaded, not yet read): full source to
   deploy, or reference comps? Decides whether Phase 1 static pages are
   "wire up existing assets" or "rebuild from mockups".
4. Calendly URL for "Schedule a call" (placeholder `#` in mockups).
5. Vendor-form upload destination (email to accounting@, or storage).
6. Educator pricing tiers at launch (max 3 due to catalog cap).

---

## 7. Hard constraints (carried from the project)

- Never write the live/published theme. Staging only. You publish.
- Never modify the default `templates/product.json` for Fast PDP.
- Content rules: no em-dashes, no exclamation marks, American English only
  ("color" not "colour"), every sentence grammatically complete.
- Never invent facts, origins, certifications, or collection/range names.
- Premium products (price >= $250) go to a human review queue before
  publish.
- SEO must not regress.

---

## 8. Fast PDP API rollout status (verified 2026-05-19)

- **Infrastructure: done and stable.** Fast PDP section, template, and CSS
  are deployed. The default `templates/product.json` was restored; the
  catalog renders on the proven default PDP. No sitewide regression: the
  most-recently-updated products all carry `templateSuffix` null/empty
  (default), not skeleton.
- **Canary: live and verified.** "Felt Farm Animals Toys, Set of 10"
  (`gid://shopify/Product/8017008394410`) is on `templateSuffix: fast-pdp`
  with enriched metafields and clean SEO. The pipeline works end to end.
- **Broad rollout: not yet executed.** The owner-approved 300-product
  bestseller cohort has not been run as a batch. Premium items (>= $250),
  e.g. Drewart and Bauspiel drafts, await an explicit "approve premium".
- **Tooling caveat:** this Shopify MCP ignores `template_suffix:` (and
  likely tag) query filters in both `productsCount` and the `products`
  connection (a bogus suffix returns all 8,148). Exact rollout counts
  cannot be pulled by filter; verify by known product ID, or paginate all
  products reading `templateSuffix`, or use ShopifyQL.

## 10. Phase 1 static pages (built 2026-05-19, all UNPUBLISHED drafts)

| Page | Handle | Page ID | State |
|---|---|---|---|
| Ordering for Schools | schools | gid://shopify/Page/115575914666 | draft, educator-portal |
| Vendor Profile | vendor-profile | gid://shopify/Page/115576045738 | draft, educator-portal |
| Procurement Guide | procurement-guide | gid://shopify/Page/115575947434 | draft, educator-portal |
| Educator Catalog (ch 6-9) | educator-catalog-guide | gid://shopify/Page/115675136170 | draft, educator-portal |
| New Quote | new-quote | gid://shopify/Page/115675660458 | draft, educator-portal (Phase 2 visual; mailto submit, no Admin API) |
| Educator Dashboard | educator-dashboard | gid://shopify/Page/115675693226 | draft, educator-portal (Phase 2 visual; dynamic regions neutralized to sample data with disclaimer) |

Built from `designs/ordering-for-schools.html`, `designs/vendor-profile.html`,
`designs/procurement-guide.html`. Assets rewritten to
`https://mytoywagon.com/cdn/shop/files/<renamed>` per the asset manifest.
Sensitive business identifiers kept email-request-only as the design
intends (vendor-profile). Internal links pointed at Shopify paths.
Procurement guide keeps its 5-page printable layout and print button.
These are public funnel pages (not in the gate's closed-handle list), so
when published they render openly and stay indexable. They are invisible
now because they are unpublished drafts.

To preview a draft page: Shopify admin > Online Store > Pages > open the
page > View (adds a preview token so the draft renders). To see it with
the new gated template, also be previewing staging theme 145914462378.

## 11. Ecosystem catalog (Phase A outcome, 2026-05-19)

Artifact: `catalog/EDUCATOR_CATALOG_MAP.md` / `.json` (commit f28f4bd).

- The print catalog is a curated editorial showcase: **8 ecosystems, 25
  hero/bundle cards**, not a product database. Online build is therefore
  small and tractable; "more expansive" is deliberate expansion.
- **No prices anywhere in the catalog.** Correction: the earlier
  "printed educator price = commitment" pre-mortem risk was based on a
  misread CSS class and is largely void. Catalog has zero dollar figures.
- Catalog SKUs are internal `MTW-` curation codes, NOT live Shopify
  SKUs (0/3 sample match). Cards must be linked to live products by
  brand + concept curation, not SKU. Several cards are intentional
  multi-product bundles. This curation is the one hard dependency before
  card links work; full 25-card brand/title mapping is the Phase A.5
  follow-up.
- Catalog color system is real and per-ecosystem (eco-* accent tokens:
  Nature #5A7A5A, Woodland #2D5C3A, Small World #7A5C8A, Fairy Villages
  #C97A8A, STEAM #7A5E3A, Dramatic Play #8B6840, Creative Arts #4E7A7A,
  over warm cream/ink). The prototype must use these exact tokens, not
  invented palettes. Sensory Play token to confirm.

## 12. Pricing & anti-staleness policy (owner-agreed 2026-05-19)

**Pricing/quote validity (agreed):**
- Catalog stays evergreen and price-free (never print prices).
- Price lives on the dated quote/draft order with a hold window. Summer
  quotes are firm for fall fulfillment if the PO arrives within the
  window. Recommended window: 60 days, or seasonal ("quotes issued
  May-Aug honored for fall fulfillment if PO by Sept 30"). Catalog's
  "held 30 days" line to be updated to match.
- Internal base price list reviewed monthly (1st). Repricing affects
  only NEW quotes; already-issued quotes honored at quoted price until
  expiry. Volatility/escalation clause for out-of-window or large/long
  lead orders; deposit on very large heirloom orders (per Net ladder).
- Staff-mediated, no Shopify system change needed.

**Anti-staleness system:**
1. Evergreen by design: catalog cards carry no price and no stock claims;
   they describe the world/pedagogy (stable), not transient specifics.
2. Single source of truth: cards link to live PDPs; never duplicate
   product data. `catalog/EDUCATOR_CATALOG_MAP.json` is the card->product
   registry; all checks run against it.
3. Scheduled drift report: a recurring job walks the registry and flags
   any card whose linked product is missing, unpublished, renamed
   (404), out of stock, or (for bundles) has a dead member. Catches
   drift before a school does.
4. Stock absorbed by the quote: never assert availability in the
   catalog; "stock confirmed on every quote" is the mechanism.
5. Print vs online: print editions are versioned with a sunset note and
   QR codes point only to stable handles, never rot-prone deep URLs.
6. Ownership cadence: weekly automated drift report, monthly price-base
   review, quarterly content/photography re-curation.

Dependency: the drift report needs the card->product registry, which
needs Phase A.5 (curate the 25 cards to real product handles, since
catalog SKUs are internal MTW codes that do not resolve).

## 9. Running log

- 2026-05-18: Duplicated live theme to staging `145914462378`. Verified
  Shopify config via Admin API. Deployed the closed-portal gate to
  `templates/page.educator-portal.liquid` on staging. Created this record.
- 2026-05-19: Owner confirmed native Shopify B2B via Markets on the Grow
  plan, no third-party app, 3-catalog cap, catalog "Educator". Updated
  sections 3, 4, 6. Diagnosed the preview error: staging `145914462378` is
  complete and valid (layout/theme.liquid and config/settings_schema.json
  present, identical to live); the error came from a stale attempt during
  processing or from opening an older incomplete educator theme. Verified
  no Fast PDP regression and the Felt Farm canary is intact.
- 2026-05-19: Ran the Fast PDP sub-$250 pilot (see FAST_PDP_ROLLOUT.md):
  27 bestseller-cohort products enriched and verified live, 3 held
  (pre-order, Collective, premium). Built Phase 1 static pages as
  unpublished drafts: schools, vendor-profile, procurement-guide
  (section 10). Live published educator pages left untouched.
- 2026-05-19: Phase 1 catalog editorial page drafted
  (educator-catalog-guide). Owner approved Phase 1 and made some manual
  edits (do not overwrite). Moved to Phase 2: confirmed native B2B
  capability (payment terms incl Net 30, real spending Company, draft
  orders). Built Phase 2 visual drafts new-quote and educator-dashboard
  with honest non-committal copy and no Admin API wiring. Architecture
  fork (native B2B accounts vs app vs staff-mediated) documented, not yet
  chosen.
- 2026-05-19: educator-dashboard Phase 2 visual draft built
  (gid://shopify/Page/115675693226), dynamic regions shown as neutral
  sample data with an active-account disclaimer. Open follow-ups: unmapped
  asset bauspiel-flower-sparkling-stones.webp; Calendly URL still a
  placeholder. DATA ISSUE found: duplicate "Erin Kim" customer
  (gid Customer/9695041716394, ~$17,827.85, 1 order, no company link)
  separate from the Elk Grove company contact
  (Customer/8984220303530, $22,777.39, 4 orders). Not actioned; awaiting
  owner decision (assign as contact vs merge vs leave).
