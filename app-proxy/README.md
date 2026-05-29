# Educator Wagon — App Proxy (draft-order checkout)

Educator products are **walled** (off the Online Store), so the native Shopify cart
can't add them. The storefront wagon collects items client-side and POSTs them to this
Cloudflare Worker through a **Shopify App Proxy**. The Worker creates a **draft order**
via the Admin API and returns its `invoiceUrl`; the browser redirects to Shopify's
native checkout (Shop Pay / Apple Pay / card, or PO).

```
Storefront wagon  ──POST /apps/wagon/checkout──▶  App Proxy  ──▶  Cloudflare Worker
                                                                      │ draftOrderCreate (Admin API)
   browser ◀────────── { invoiceUrl } ◀──────────────────────────────┘
   redirect → native Shopify checkout
```

## 1. Create the custom app (issues the Admin token + secret)

Shopify admin → **Settings → Apps and sales channels → Develop apps → Create an app**
- Name: `Educator Wagon Proxy`
- **Configuration → Admin API scopes:** `write_draft_orders`, `read_products`, `read_customers`
- **Install app**, then copy:
  - **Admin API access token** → `ADMIN_TOKEN`
  - **API secret key** (under API credentials) → `APP_SECRET`

## 2. Deploy the Worker (Cloudflare, free tier)

```bash
npm i -g wrangler
cd app-proxy
wrangler deploy worker.js --name educator-wagon-proxy --compatibility-date 2024-11-01
wrangler secret put ADMIN_TOKEN   # paste the Admin API access token
wrangler secret put APP_SECRET    # paste the app's API secret key
```

Note the deployed URL, e.g. `https://educator-wagon-proxy.<your-subdomain>.workers.dev`.

(Or paste `worker.js` into the Cloudflare dashboard → Workers → Create → Quick edit,
then add `ADMIN_TOKEN` and `APP_SECRET` under Settings → Variables → **Encrypt**.)

## 3. Point the App Proxy at the Worker

In the custom app → **Configuration → App proxy**:
- **Subpath prefix:** `apps`
- **Subpath:** `wagon`
- **Proxy URL:** the Worker URL from step 2

Save. The storefront path `https://mytoywagon.com/apps/wagon/checkout` now routes to the Worker.
(The wagon front-end already posts to `/apps/wagon/checkout` — no code change needed.)

## 4. Verify

1. On a section page (signed in as an educator), add items → wagon count updates.
2. Open `/pages/educator-wagon` → **Proceed to secure checkout** → you should land on a
   native Shopify checkout for those line items, tax-exempt if your account is.
3. **Pay by PO** creates the same draft (tagged `po-request`) and shows the confirmation +
   itemized-quote link; apply Net-30 terms in admin and send the invoice.

## Maintenance / runbook

- The Worker is part of the stack now: needs uptime + occasional **Admin token rotation**
  (re-run `wrangler secret put ADMIN_TOKEN`).
- **Abandoned drafts:** each Pay click creates a draft; double-clicks / non-completions leave
  unpaid drafts. Set up a **Shopify Flow**: trigger *Draft order created* → wait N days →
  if still unpaid (and tagged `educator-wagon`), delete or tag for cleanup.
- Draft orders accept walled variants because the Admin API isn't gated by sales channel —
  products stay fully off the Online Store (no `/products.json` / sitemap leak).
