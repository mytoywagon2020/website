# PDP (Product Page) — Status & Where We Stopped

> Snapshot of the MTW Fast PDP work so it can be resumed cleanly. Read this plus
> `SESSION-HANDOVER.md` (theme/deploy state) and `BRAND_VOICE.md` (rules) before
> touching the product page.

---

## 1. What was built

The **MTW Fast PDP** — a custom, brand-matched product page for the 9.0 theme.

### Files (mirrored in git, all scoped under `[data-mtw-pdp="fast-v1"]`)
| File | Purpose |
|---|---|
| `shopify/theme/sections/mtw-fast-pdp.liquid` | The PDP section (~31.6 KB). Wrapper: `<div data-mtw-pdp="fast-v1"><div class="ff-page">…</div></div>` |
| `shopify/theme/assets/pdp-formats-base.css` | Scoped `:root` tokens + `.dot` primitives |
| `shopify/theme/assets/pdp-fast-1.css` | Component CSS (part 1) |
| `shopify/theme/assets/pdp-fast-2.css` | Component CSS (part 2) + 4-tone canvas fix + Judge.me restyle + age-chip CSS |
| `shopify/theme/templates/product.json` | Wires `main` → `mtw-fast-pdp` with settings: `preorder_collection`, `shipping_text`, `returns_text` |
| `shopify/theme/sections/mtw-footer.liquid` | Newsletter "Sign up" button hardened (mobile clip fix) |

### Features implemented
- **Metafield-driven with graceful fallback:** reads `details.*`, falls back to
  `custom.*`, then to `product.description`. Pages never look empty.
- **4-tone canvas** (`#E4DCC9` / `#F5F0E5` / `#FFFCF7` / `#EDE3CD`) — darker
  frame, not flat cream. (See `BRAND_VOICE.md` §3.)
- **Fulfillment states:** 3 states + low-stock + sold-out. Sold-out uses Klaviyo
  client back-in-stock API (company_id `SZm3nN`, revision `2024-10-15`,
  catalog-variant id form `$shopify:::$default:::VARIANTID`).
- **Origin** rendered with a 3-pattern (made-in variants).
- **Conditional choking-hazard warning.**
- **Schema.org** dynamic JSON-LD: Product + Offer + BreadcrumbList. No fake
  `aggregateRating` (only real review data).
- **Judge.me** review widgets, restyled to brand tokens.
- **Age recommendations accordion** with the circular age-chip treatment, ported
  from `custom.age_band`: `0–12 mo` → pill "Under 1 yr"; `18 mo` → pill
  "18 months"; numeric bands → `.ff-age-circle`.

---

## 2. Deploy state (IMPORTANT)

- The PDP was deployed and wired on theme **9.0 "Current Shop with Updated
  Impulse"** (`gid://shopify/OnlineStoreTheme/145720180906`) **while 9.0 was
  unpublished/API-writable.**
- **9.0 has since flipped to MAIN/LIVE at times, which BLOCKS all API theme-file
  writes.** Theme state is volatile (MAIN ↔ UNPUBLISHED). **Always re-check
  `themes { role }` before any theme push.**
- When 9.0 is MAIN, push PDP changes via the **admin code editor** or a
  **duplicate → edit → merchant-publish** flow, not the API.
- Everything is mirrored in git on `claude/fix-github-access-pFh80`.

Last PDP commits (newest first):
`a5f8b0e` age-chip port · `81b29a5` 4-tone canvas restore · `2088224` bg fix +
footer harden · `a3afc13` add template + wire · `ac826d5` mirror to git.

---

## 3. Where we stopped — open items / next session

### A. Metafield content fill — 300 products via API, vet-gated
- **STATUS: PAUSED (intentionally).** Owner paused this mid-run to focus on the
  website / educator portal build. Not abandoned — resume when the portal work
  reaches a stopping point.
- **Scope: 300 products**, metafields written **through the Shopify API**
  (`metafieldsSet`), generated **from each product's description in a
  high-converting way.**
- **Workflow with owner: vetting gate.** Claude generates the metafield content
  and **shares a sample batch (2, or up to ~26) for the owner to vet/approve
  before it is applied** across the rest. Do not bulk-write all 300 unvetted.
- Phased / in waves, not all at once — owner's directive, to avoid a disruptive
  Google re-crawl.
- Confirmed reference example already written: Gus + Mabel Busy Bee
  (`gid://shopify/Product/8390716424362`, 21 metafields).
- Metafield namespaces: `details.*` / `custom.*` / `fulfillment.*` (the PDP reads
  `details.*`, falls back to `custom.*`, then `product.description`).
- **Next session:** confirm how many of the 300 are already written, then
  continue generating the next vet batch for owner approval.

### B. Matrixify batch fixes (queued)
- **`age_band` is wrong on many products.** Concrete example: a product whose
  description says "Recommended Age: 3+" has `age_band` = `0–12 mo, 1, 18 mo`.
  Felt trays should sit in **age collections 3–8** (tags `age:3-years` …
  `age:8-years`). Fix `age_band` catalog-wide.
- **Pre-order signal mismatch.** Example: "Coralwhim Cove" has an SEO title
  starting "Pre-Order …" but **no** fulfillment/preorder metafield, so the PDP
  can't show the pre-order state. Add the fulfillment/preorder metafield where
  the title/intent says pre-order.
- Apply via an **Update-mode Matrixify sheet keyed by Handle** (least
  disruptive).

### C. Missing trust asset
- Trust-icon row needs the **free-shipping / wagon** SVG. Owner supplied 2 of 3
  URLs (`trust-30day-returns`, `trust-packed-with-care`); the **shipping/wagon
  icon is still missing.** Either get the third asset or adjust the row to 2.

### D. Visual QA
- The PDP has **not** been visually verified (no browser in this environment).
  Needs a desktop + mobile pass on a real product once it's viewable.

---

## 4. Quick resume checklist
1. Re-check theme role: is 9.0 MAIN or UNPUBLISHED? (Decides API vs admin editor.)
2. Resume the **300-product** metafield fill (§3A): query which products already
   have `details.*` written, then generate the next **vet batch (2 or ~26)** for
   owner approval before applying broadly.
3. Build the Matrixify Update sheet for `age_band` + pre-order metafields (§3B).
4. Source or drop the third trust icon (§3C).
5. Visual QA on desktop + mobile (§3D).
