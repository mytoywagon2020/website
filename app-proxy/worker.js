// Cloudflare Worker — My Toy Wagon educator wagon app proxy.
//
// Educator products are WALLED (off the Online Store), so Shopify's native cart
// can't be used. The storefront wagon (snippets/educator-wagon-cart.liquid) POSTs
// the selected items here; this Worker creates a Shopify DRAFT ORDER via the Admin
// API and returns its invoiceUrl, which the browser redirects to (native checkout).
//
// Deploy as the target of a Shopify App Proxy (prefix "apps", subpath "wagon"),
// so the storefront calls same-origin: https://mytoywagon.com/apps/wagon/checkout
//
// Secrets (wrangler secret put ...):
//   ADMIN_TOKEN  — Admin API access token of the custom app
//                  (scopes: write_draft_orders, read_products, read_customers)
//   APP_SECRET   — the custom app's API secret key (used to verify proxy signature)

const API_VERSION = '2025-01';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Verify the request actually came from Shopify's app proxy.
    if (!(await verifyProxySignature(url.searchParams, env.APP_SECRET))) {
      return json({ error: 'Invalid signature' }, 401);
    }

    const shop = url.searchParams.get('shop');
    if (!shop) return json({ error: 'Missing shop' }, 400);

    // GET → live product read (powers the content PDP page for ANY walled SKU).
    if (request.method === 'GET') {
      return handleProductRead(shop, env.ADMIN_TOKEN, url.searchParams.get('sku'));
    }
    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405);

    let body;
    try { body = await request.json(); } catch { return json({ error: 'Bad JSON' }, 400); }

    const items = Array.isArray(body.items) ? body.items : [];
    const lineItems = items.map((it) => ({
      variantId: toVariantGid(it.variantId),
      quantity: Math.max(1, parseInt(it.quantity, 10) || 1),
    })).filter((li) => li.variantId);
    if (!lineItems.length) return json({ error: 'empty' }, 400);

    const isPO = body.paymentMethod === 'po';
    const customerGid = customerToGid(url.searchParams.get('logged_in_customer_id'));

    // 2) Tax-exempt? Read it straight from the customer record.
    let taxExempt = false;
    if (customerGid) {
      try { taxExempt = await fetchCustomerTaxExempt(shop, env.ADMIN_TOKEN, customerGid); } catch {}
    }

    // 3) Build + create the draft order.
    let note = isPO ? 'Educator wagon — purchase order / Net-30 requested' : 'Educator wagon — pay now (card)';
    if (body.poNumber) note += ' | PO# ' + String(body.poNumber).slice(0, 60);
    const input = {
      lineItems,
      taxExempt,
      tags: isPO ? ['educator-wagon', 'po-request'] : ['educator-wagon'],
      note,
    };
    if (customerGid) input.purchasingEntity = { customerId: customerGid };

    let data;
    try {
      data = await adminGraphQL(shop, env.ADMIN_TOKEN, DRAFT_MUTATION, { input });
    } catch (e) {
      return json({ error: 'Admin API error' }, 502);
    }

    const res = data && data.draftOrderCreate;
    const errs = (res && res.userErrors) || [];
    if (errs.length) return json({ error: errs.map((e) => e.message).join('; ') }, 422);

    const draft = res && res.draftOrder;
    if (!draft || !draft.invoiceUrl) return json({ error: 'No invoice URL returned' }, 502);

    return json({ invoiceUrl: draft.invoiceUrl, draftOrderId: draft.id, paymentMethod: isPO ? 'po' : 'card' });
  },
};

// Live product read for the content PDP page. Returns title/price/media/description/
// metafields for a walled product by SKU. Products stay off the Online Store, so this
// data never appears in /products.json — it's only reachable through the signed proxy.
async function handleProductRead(shop, token, sku) {
  if (!sku) return json({ error: 'Missing sku' }, 400);
  const query = `query($q: String!) {
    products(first: 1, query: $q) {
      edges { node {
        title
        descriptionHtml
        media(first: 10) { edges { node { ... on MediaImage { image { url } } } } }
        variants(first: 1) { edges { node { id sku price } } }
        metafields(first: 40) { edges { node { namespace key value } } }
      } }
    }
  }`;
  let data;
  try { data = await adminGraphQL(shop, token, query, { q: 'sku:' + JSON.stringify(sku) }); }
  catch (e) { return json({ error: 'Admin API error' }, 502); }
  const node = data && data.products && data.products.edges[0] && data.products.edges[0].node;
  if (!node) return json({ error: 'Not found' }, 404);
  const v = node.variants && node.variants.edges[0] && node.variants.edges[0].node;
  const images = (node.media ? node.media.edges : []).map(function (e) { return e.node && e.node.image && e.node.image.url; }).filter(Boolean);
  const metafields = {};
  (node.metafields ? node.metafields.edges : []).forEach(function (e) { metafields[e.node.namespace + '.' + e.node.key] = e.node.value; });
  return json({
    title: node.title,
    sku: (v && v.sku) || sku,
    variantId: v && v.id ? v.id.split('/').pop() : null,
    price: v && v.price ? v.price : null,
    descriptionHtml: node.descriptionHtml || '',
    images: images,
    metafields: metafields,
  });
}

const DRAFT_MUTATION = `mutation CreateWagonDraft($input: DraftOrderInput!) {
  draftOrderCreate(input: $input) {
    draftOrder { id invoiceUrl }
    userErrors { field message }
  }
}`;

async function adminGraphQL(shop, token, query, variables) {
  const r = await fetch(`https://${shop}/admin/api/${API_VERSION}/graphql.json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Shopify-Access-Token': token },
    body: JSON.stringify({ query, variables }),
  });
  const j = await r.json();
  if (j.errors) throw new Error(JSON.stringify(j.errors));
  return j.data;
}

async function fetchCustomerTaxExempt(shop, token, customerGid) {
  const d = await adminGraphQL(shop, token, `query($id: ID!){ customer(id:$id){ taxExempt } }`, { id: customerGid });
  return !!(d && d.customer && d.customer.taxExempt);
}

function toVariantGid(v) {
  if (!v) return null;
  v = String(v);
  return v.startsWith('gid://') ? v : `gid://shopify/ProductVariant/${v.replace(/\D/g, '')}`;
}

function customerToGid(v) {
  if (!v) return null;
  v = String(v).trim();
  if (!v || v === '0') return null;
  return v.startsWith('gid://') ? v : `gid://shopify/Customer/${v.replace(/\D/g, '')}`;
}

// App-proxy signature: HMAC-SHA256 over sorted "key=value" params concatenated with
// no separators (array values joined by ","); compare hex digest to `signature`.
async function verifyProxySignature(searchParams, secret) {
  const sig = searchParams.get('signature');
  if (!sig || !secret) return false;
  const map = {};
  for (const [k, v] of searchParams.entries()) {
    if (k === 'signature') continue;
    (map[k] = map[k] || []).push(v);
  }
  const message = Object.keys(map).sort().map((k) => `${k}=${map[k].join(',')}`).join('');
  const expected = await hmacHex(secret, message);
  return timingSafeEqual(expected, sig);
}

async function hmacHex(secret, message) {
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const buf = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(message));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let out = 0;
  for (let i = 0; i < a.length; i++) out |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return out === 0;
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json' } });
}
