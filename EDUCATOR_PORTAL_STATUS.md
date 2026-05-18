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

## 3. Verified Shopify configuration (read from the Admin API 2026-05-18)

- **Plan: "Shopify" (not Plus).** `shopifyPlus: false`. Full native B2B
  (companies + B2B catalogs + native payment terms + Customer Account UI
  Extensions) is **not** the engine here.
- **Educator pricing data already exists:** an enabled **"Educators"
  market** (`gid://shopify/Market/32754958506`), an **"Educator Catalog"**
  market catalog (`gid://shopify/MarketCatalog/64883065002`), and a USD
  **"Educators Market" price list**
  (`gid://shopify/PriceList/24074289322`).
- **The Educators market has no web presence** (`webPresence: null`).
  Educator pricing is configured but not deliverable through any storefront
  path yet. Closing that delivery gap is the real Phase 2 problem, not the
  pricing math.
- **2 B2B companies exist** despite the non-Plus plan. This almost
  certainly means a B2B/wholesale app created them. The API token is denied
  access to `appInstallations`, so the app name must be confirmed in admin
  (Settings > Apps).
- You created a B2B catalog with all products and no customization
  ("Step 1").

**Conflict with repo docs:** `README.md` and `SHOPIFY_NOTES.md` assume
full native Plus B2B. That assumption is contradicted by the verified plan.
Treat those docs as design intent, not the platform plan, until Phase 2 is
decided.

---

## 4. Phase plan

### Phase 1 (does not depend on the Plus question) - IN PROGRESS

- [x] Duplicate live theme to unpublished staging (`145914462378`).
- [x] Closed-portal gate added to `templates/page.educator-portal.liquid`
      on staging (see section 5).
- [ ] Finish and stage the static funnel pages (catalog, educator program
      and apply, ordering-for-schools, vendor-profile, procurement guide).
- [ ] Preview pass on staging, then you publish.

### Phase 2 (blocked on platform decision)

Dynamic, account-bound pieces: educator dashboard, tiered educator pricing
on the PDP, quote to draft order, PO upload, document vault, Net-30.

Recommended engine on the "Shopify" plan: the **quote / draft-order
model**. Approved educator submits a request, a **draft order** is created,
staff applies the Educator price list (or matching discount) plus Net-30
payment terms and a PO number, then sends the invoice. `draftOrderCreate`
and `paymentTermsCreate` work on this plan with no Plus and no app. This
matches `designs/new-quote.html`.

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

## 6. Open questions (need answers before Phase 2 build)

1. **Which B2B / wholesale app is installed?** Source of the 2 companies
   and possibly a second pricing-delivery path. Claude cannot read it
   (API denies `appInstallations`). Check Settings > Apps.
2. **`MTW_Website_16.zip`** (uploaded, not yet read): full source to
   deploy, or reference comps? Decides whether Phase 1 static pages are
   "wire up existing assets" or "rebuild from mockups".
3. Calendly URL for "Schedule a call" (placeholder `#` in mockups).
4. Vendor-form upload destination (email to accounting@, or storage).
5. Number of educator pricing tiers at launch.

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

## 8. Running log

- 2026-05-18: Duplicated live theme to staging `145914462378`. Verified
  Shopify config via Admin API (plan Shopify, not Plus; Educators market
  and price list exist but no web presence; 2 companies; appInstallations
  access denied). Deployed the closed-portal gate to
  `templates/page.educator-portal.liquid` on staging. Created this record.
