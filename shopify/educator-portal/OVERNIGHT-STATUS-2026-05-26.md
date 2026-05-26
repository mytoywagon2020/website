# Overnight status — 2026-05-26

## Preview link (staging theme)

After signing in to admin, open the dashboard at:

```
https://my-toy-wagon.myshopify.com/pages/educator-dashboard?preview_theme_id=145914462378
```

Use the `my-toy-wagon.myshopify.com` domain (not the custom domain) and ensure you're signed in as an `educator-approved` customer (e.g. `mytoywagon+00@gmail.com`).

## Done this session

### Dashboard chrome
- Replaced inline utility bar + nav header with `{% section 'mtw-educator-header' %}`. **Wagon logo added.** Mark + brand wordmark + nav + "Request a quote" CTA.
- Replaced 3-link inline footer with `{% section 'mtw-educator-footer' %}`. 4-column rich footer with 8 working section links (Sensory, Nature, Woodland, Small World, Fairy Villages, STEAM, Dramatic Play, Creative Arts) + Account + Procurement columns. "Woodland" (not "Woodland Habitats").
- Banner: removed the green-over-portrait gradient (jarring). Now a calm warm-white card with a forest left accent and italic Cormorant headline. CTA: ink button, hovers forest.
- Stat cards: removed off-brand teal/burnt-orange/mauve. All three now warm-white with a thin forest top accent and ink Cormorant numerals.
- CTA action cards: top borders consolidated to forest/ink/forest (brand vars only).

### Copy
- Em-dash sweep across all customer-facing educator templates (10 files). Em-dashes left only in CSS / dev comments / email-body captures.
- Lead-time copy standardized across all 8 section pages, dashboard, quote page, fairy-villages chip, and PDP template: variable "3 to 4 weeks" replaced with consistent **"Order by July 15 to ship in August or September"** anchor.
- Banner copy: "Most items deliver in this window. Order by July 15."

### Pages and templates
- Published `educator-login` and `educator-catalog-guide` pages (were both unpublished, broke footer links). Both live now so all 8-section nav links work.
- All 18 products tagged `educator-only` now use `templateSuffix: "educator"`. The only outlier (The Cow Shed, DRAFT) was on `fast-pdp` — fixed.
- `product.educator.json` template on staging includes the educator block stack: made_to_order pill → price → variant picker → request_quote_cta → procurement_trust → description → separator → educator_policies accordion. Plus `mtw-educator-header` and `mtw-educator-footer` at top/bottom of section order.

### Klaviyo (email)
- Branded template **"Educator Approval Welcome v2"** (ID `XLJeUa`) — full MTW palette (cream/ink/forest/stone), Cormorant + Mulish, squared corners. Button targets `/pages/educator-dashboard` (lands the educator on the branded dashboard, not Shopify's stock /account UI).
- Old template `QUtJd5` deleted by owner.

### Runbook
- Appended **"Outstanding — admin-UI work (not API-doable)"** section listing every UI-only step that has to happen by hand: Klaviyo flow + segment, Shopify Flow #1 (auto-tag `educator-pending`), Customer accounts menu link, and the optional branded `/pages/educator-login` polish.

## Outstanding — you have to do these (no API)

| | Task | Where |
|---|---|---|
| 🖱 | **Klaviyo segment + flow** — `Educator – Approved` segment (`Shopify Tags` contains `educator-approved`), then a flow triggered by "enters segment" sending template `XLJeUa`. Smart Sending OFF; send to unengaged ON. | Klaviyo → Audience → Segments → Create, then Flows → Create flow |
| 🖱 | **Shopify Flow #1** — auto-tag `educator-pending` on customer creation when `customer.metafields.customer_fields.institution_name` is not empty | Admin → Apps → Flow → Create workflow |
| 🖱 | **Customer accounts menu link** — add `Educator dashboard` → `/pages/educator-dashboard` so the stock /account UI has a one-click jump back to the branded dashboard | Settings → Customer accounts → Customer account menu |
| 🖱 | **Branded `/pages/educator-login`** (optional polish) — replace the gate templateSuffix with a true sign-in form template | Theme code editor + admin Pages |

## Notes for review

- **Dashboard banner** — current treatment is a calm warm-white card with forest accent stripe. If design wants something more upbeat / toy-themed, options: (1) cream background with a tile of bright toys (Connetix mosaic), (2) ink card with cream text for high contrast, (3) keep current calm aesthetic but add a small wagon mark inline. The HTML is in `shopify/educator-portal/templates/page.educator-dashboard.liquid`.
- **Header wagon logo** — pulls from theme asset `assets/mtw-wagon-only.png`. Confirmed present on staging. Sized at 44px height (36px on mobile) with light opacity. Adjust via `.mtw-edu-h__mark` rule in `sections/mtw-educator-header.liquid`.
- **PDP template** — `product.educator.json` uses Shopify's standard `main-product` section, not `mtw-fast-pdp`. The educator add-on blocks (request_quote_cta, procurement_trust, educator_policies) are wired in via the main-product block system. If the team prefers the fast-pdp section as the base, the educator blocks need to be ported into `mtw-fast-pdp.liquid` itself (the section doesn't accept custom blocks the way main-product does).

## Commits this session

```
d97b790 Educator copy: em-dash sweep tail (creative-arts florals)
9f35d19 Dashboard: render mtw-educator-header (wagon logo) + mtw-educator-footer
0893ced Educator copy: em-dash sweep tail (creative-arts, dramatic-play, steam)
7bd499e Dashboard banner: clarify with 'Most items deliver in this window'
d7b650e Dashboard: realign colors to brand (drop teal/burnt-orange/mauve stat cards)
115418c Educator copy: drop em-dashes; standardize lead time to "Order by July 15, ship Aug/Sep"
```

Branch: `claude/kind-bardeen-lX5a2`
