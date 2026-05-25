# CLAUDE.md — My Toy Wagon

**Before touching the educator portal, read the source-of-truth docs below. Do NOT re-derive, reinvent, or contradict them. Check what already exists before building anything.**

## Source-of-truth docs (read first, every time)
- **`shopify/educator-portal/EDUCATOR-PORTAL-RUNBOOK.md`** — the operating design. Re-read it before educator-portal work. Key invariants:
  - **Approval = add the `educator-approved` customer tag.** That IS the one-click approval. The gate (`snippets/educator-gate.liquid`) accepts `customer.b2b?` OR `educator-approved`.
  - **B2B pricing = the "Educators" Market** → Educator Catalog `MarketCatalog/64883065002` + price list `PriceList/24074289322`, applied to all company locations automatically. This is NOT a per-company B2B catalog — correct by design. (Shopify B2B pricing here is done via the Market.)
  - **Native + no app.** Payment status via order tags `invoice-sent` / `po-paid-external`; do **NOT** mark PO orders Paid natively (Shopify Capital workaround).
  - The **register form = Helium Customer Fields app** (theme `educator-portal`/`educator-register` template; owns `customer_fields.*`). Login = `educator-login`. Don't rebuild these. **Lifecycle via customer tags** `educator-pending`/`-approved`/`-rejected` — NOT a Company status metafield (redundant). Verification doc is **optional** (cert only for tax-exempt checkout).
- **`shopify/educator-portal/EDUCATOR-CATALOG-WORKSHEET.md`** — catalog build source of truth.
- **`SHOPIFY_NOTES.md`** — pricing/season/grid/cert rules: educator price = **regular** price; bundles **10% off (MAP cap, bundles only)**; **Autumn** (public/products) / **Fall** (schedule); center grid rows with <5 cards; SKU-only metas; verified-per-maker certs only.
- **`CATALOG_REBUILD_CHANGELOG.md`** — running web→print catalog sync log + decisions.

## Hard rules (don't relitigate)
- The **educator/print catalog is the source of truth**; when a web edit conflicts, resolve toward the catalog and log it under "Catalog updates needed."
- **Connetix stays Draft / not live on retail**; shown in-stock on educator pages (made-to-order).
- **Don't do redundant work** — search the repo + runbook first; the register/login/gate/onboarding flow already exists.

## What Claude can't do here (don't promise these)
- Create metafield definitions (API client access-denied), publish themes/pages, install/host apps, or wire live form→automation. Those are admin steps for the owner.
