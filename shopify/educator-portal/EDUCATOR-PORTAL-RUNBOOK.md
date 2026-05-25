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
