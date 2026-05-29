# Educator Portal — Persistent Working Notes

**Purpose:** Single source of truth so we DON'T re-discover the same facts every session.
The remote dev environment is wiped between sessions; only committed files survive. Keep this file updated.

Last updated: 2026-05-29

---

## 1. The Rules (non-negotiable, confirmed by owner)

1. **Educator products must NOT appear on retail.** "Walled" = product is **ACTIVE**, published to the **Educator Catalog only**, and on **zero sales channels** (Channels: 0 in the product list).
2. **No shared listings between retail and educator.** A single listing serving both **mixes inventory**, which we must never do. If a retail product is needed in the educator portal, create a **separate educator listing** (duplicate it), and **remove the educator tags from the retail original** so the two inventory lines stay separate.
3. **Educator price = retail price** (price-match the retail equivalent, or use the collective/bundle price for sets).
4. **Educator Catalog should contain ONLY the 8 portal sections' products** — not the whole retail store.
5. Educator listings: **inventory not tracked** AND **"Continue selling when out of stock"** (`inventoryPolicy: CONTINUE`) — so they never share/deplete retail stock and orders are never blocked (made-to-order / Net-30).

---

## 2. Architecture & Key IDs (Shopify: my-toy-wagon.myshopify.com / mytoywagon.com)

- **Educator B2B market:** "Educators", handle `educator-catalog`, Market id `gid://shopify/Market/32754958506`
- **Educator Catalog publication id:** `gid://shopify/Publication/152026382506`  ← walled products publish HERE only
- **Online Store publication id:** `gid://shopify/Publication/69325422762`  ← educator products must NOT be here
- Other retail channels (all must be OFF for educator products): Facebook&Instagram `70373343402`, Social Proof `70696140970`, Google&YouTube `72605794474`, Shop `74263429290`, UPS `74827661482`, Inbox `79430516906`, TikTok `112670539946`, Point of Sale `112849518762`, Pinterest `113627725994`, Microsoft Copilot `146149998762`
- Region market catalogs (OK for educator products to be in, like Cow Shed): International `MarketCatalog/1586757802`, United States `MarketCatalog/22862758058`

### Theme / deploy
- Repo deploys to unpublished theme **"website/staging-theme"** = `gid://shopify/OnlineStoreTheme/146144002218`. Git branch **`staging-theme`** → pushes here. Owner watches changes in real time on this theme.
- Preview URL: `https://mytoywagon.com/pages/educator-<section>?preview_theme_id=146144002218`
- MAIN/live theme (do not confuse): "Live Shop Educator Portal Draft 2026-05-28" = `146131452074`

### The 8 portal sections (page templates: `templates/page.educator-<section>.liquid`)
sensory-play, woodland, nature-play, small-world, fairy-villages, steam, dramatic-play, creative-arts

---

## 3. Walling recipe (how to make an educator product, since the API can't unpublish)

**CRITICAL LIMITATION:** the Shopify MCP **blocks `publishableUnpublish`** ("destructive"). So I (the agent) **cannot remove a product from a sales channel via API.** New/duplicated products auto-publish to the Online Store, and only an **admin** can turn channels off.

Recipe per educator product:
1. **(Agent, API)** `productDuplicate` the retail equivalent (copies description, images, price) with `newStatus: DRAFT`.
2. **(Agent, API)** Set: educator handle (`<name>-educator`), tags `["educator","educator-<section>"]`, variant SKU, `inventoryItem.tracked: false`. Price already copied from retail.
3. **(Owner, admin)** Open product → **Manage publishing** → **Sales Channels: turn ALL off** → leave **Educator Catalog** ON (Catalogs tab) → close → set **Status: Active**.
4. Verify: product shows **Channels: 0**, `publishedOnPublication(OnlineStore)=false`, `publishedOnPublication(Educator)=true` — matches the good reference product **"The Cow Shed"** (`Product/8444919185578`).

DRAFT status alone also removes a product from all channels (safe holding state), but DRAFT products can't be sold in B2B — must end ACTIVE + walled.

---

## 4. Tags

- 8 section tags: `educator-sensory-play`, `educator-woodland`, `educator-nature-play`, `educator-small-world`, `educator-fairy-villages`, `educator-steam`, `educator-dramatic-play`, `educator-creative-arts`
- Umbrella tag **`educator`** added to all section-tagged products (2026-05-29) for a single smart-collection / filter.
- **DECISION (2026-05-29): keep BOTH** — the 8 section tags (drive each portal page + a per-section smart collection) **and** the `educator` umbrella (one-filter bulk edits + a single Educator Catalog smart collection).
- **INVARIANT:** `educator` (and any `educator-<section>`) tag = "this is a dedicated walled educator listing." A **retail** product must NEVER carry it. Treat `tag:educator` as the yes/no test for "walled educator listing."
- **`educator` vs `educator-only`:** USE **`educator`** (the umbrella, 170 products). `educator-only` is a different, OLDER tag on only ~18 products, applied inconsistently — NOT the umbrella; do not use it for bulk ops (it misses 150+). It appears to have meant "exists only for educators, no retail twin," but it's unreliable. Leaving it in place unless owner says to remove.
- **WARNING (until Backlog #3 done):** the tag currently still sits on some **live retail products** (shared listings not yet split: Bauspiel ×4, Fairy Door, Wishing Well, retail Mushroom). **Do NOT bulk-remove sales channels by tag** until those are split, or you'll pull real retail products off retail.

---

## 5. State as of 2026-05-29

### Walling verified (2026-05-29)
- Confirmed **zero leaks**: no dedicated educator product (tag:educator, created>=2026-05-25) is visible on the Online Store. Owner completed the per-product sales-channel-off.
- Leak-check query that WORKS: `products(query:"tag:educator AND created_at:>='2026-05-25' AND published_status:'online_store:visible'")` — should return empty.
- Still $0 / unpriced (owner handling): PWF (fences), TLS (Let's Go Shopping), FYS + SH (bundles).

### STEAM / Connetix decision (2026-05-29)
- The `educator-steam` tag is a MIX: (a) ~36 **Connetix** = DEDICATED EDUCATOR listings (own SKUs `MTW-ST-*`/`MTW-CX-*`, classroom descriptions, currently DRAFT, priced; no separate retail Connetix exist — these ARE the educator ones); (b) **Bauspiel** ×4-5 = live RETAIL shared listings (supplier SKUs 0245/150/etc., ACTIVE) — still need splitting; (c) Felt lifecycle/Anatomy (Tara) = retail, DRAFT; (d) Kaleidoscopes Trio = 1 dedicated educator ($0).
- **Owner decision: Connetix are EDUCATOR-ONLY for now** (may add to retail later → would then make separate retail copies). DONE 2026-05-29: all **36 Connetix verified ACTIVE + Online Store OFF + Educator Catalog ON** (0 leaks). They were DRAFT, owner activated + walled in admin.
- **Confirmed AGAIN via test:** API activation (`productUpdate status:ACTIVE`) auto-republishes to Online Store AND drops the Educator publication → must be done in admin, not API. Do NOT bulk-activate Connetix via API.
- Bauspiel (live retail) remain the shared-listing problem to split later.

### Inventory (2026-05-29)
- `inventoryPolicy: CONTINUE` applied to **all 117 dedicated educator products** (tag:educator AND created_at>=2026-05-25). Retail-tagged shared listings (Bauspiel etc.) intentionally excluded — they'll get CONTINUE when split into dedicated educator listings.

### Theme (committed + pushed to `staging-theme`)
- Removed all "View product" links across all 8 sections (they 404 — educator products have no public PDP).
- Disabled the 404 clickable-image overlay (`card-pdp-link`) on the 5 wired pages.
- **fairy-villages:** buttons wired to walled educator products (see table). 5 home buttons point to NEW separate educator listings.
- **dramatic-play:** replaced placeholder counter with real `/cart/add.js` + PDP map; added 11 buy buttons (the gallery cards whose SKU has an educator product).

### Fairy Villages educator listings (separate, walled or being walled)
| SKU | Product | Variant ID | Status | Price |
|-----|---------|-----------|--------|-------|
| MTW-FV-MGF/MUS | Mushroom Garden Fairy Home | 48345499205802 | walled ✓ | $228 |
| MTW-FV-PGN | Wonderheart Pastel Gnomes | 48345499238570 | walled ✓ | $108 |
| MTW-FV-RGN | Wonderheart Bright Gnomes | 48345499271338 | walled ✓ | $108 |
| MTW-FV-VLG | Build the Village | 48345499304106 | walled ✓ | $640 |
| MTW-FV-BFH | Butterfly Fairy House (educator) `Product/8447027937450` | 48355698475178 | walled ✓ | $45 |
| MTW-FV-PNK | Pink Blossom House (educator) `Product/8447032656042` | 48355716497578 | walled ✓ | $58 |
| MTW-FV-LIL | Lilac Blossom House (educator) `Product/8447032688810` | 48355716530346 | walled ✓ | $58 |
| MTW-FV-RBS | Rainbow House* (educator) `Product/8447032754346` | 48355716595882 | walled ✓ | $50 |
| MTW-FV-RBN | Rainbow Shimmer Home* (educator) `Product/8447032819882` | 48355716661418 | walled ✓ | $65 |

*Owner retitled these two products; page labels differ slightly (page: RBS="Rainbow Shimmer House", RBN="Rainbow Home") but buttons match by SKU so it works. All 5 homes walled + live as of 2026-05-29.

Retail originals UNTAGGED from educator (now retail-only, separate inventory): Butterfly `7375178858666`, Pink Fairy Blossom `7467704418474`, Lilac Fairy Blossom `7727397634218`, Large Rainbow Shimmer `8051715702954`, Felt Rainbow Fairy Home & Mat `8154445938858`.

### Dramatic-play educator listings (14, created 2026-05-25, mostly $0 needs-price)
DCS Cow Shed `48345500811434` · TFV Harvest `48345500844202` · TFM Felt Farm Mat `48345500876970` · TFA Felt Farm Animals `48345500909738` · FTT Tractor&Trailer `48345500942506` · FHW Hay Wagon `48345500975274` · PWF Farm Fences `48345501008042` · TGS Market Stall `48345501040810` · TLS Let's Go Shopping `48345501073578` · EBB Big Box Play Food `48345501106346` · TCR Cash Register `48345501139114` · TSC Shopping Cart `48345501171882` · FYS Farmyard Set `48345501204650` · SH Classroom Shop `48345501237418`

**Dramatic-play pricing from retail (2026-05-29):** PRICED → DCS $420, TFM $49 (Farm Felt Play Mat), TFA $107 (Felt Farm Animals Set of 10), FTT $105 (Fagus Wooden Tractor — note: retail tractor only, no trailer; confirm), FHW $74 (Fagus Hay Wagon), TGS $178.99 (Tender Leaf General Stores), TCR $57.99 (Tender Leaf General Stores Till), TSC $104.99 (Tender Leaf Shopping Cart), EBB $150 (Erzi Big Box Play Food). **NO retail twin → owner must price:** PWF (farm fences), TLS (Let's Go Shopping). TFV Harvest = PRICED $250.20 (Tara Treasures Felt Fruits&Veg Sets A$69+B$60+C$71+D$78 = $278, −10%; 52 pc total; vendor corrected to Tara Treasures). **Bundles FYS + SH: owner is pricing these.**

---

## 6. Backlog / TODO (in priority order)

1. **Owner:** wall the 4 draft fairy homes (Pink, Lilac, Rainbow Shimmer, Rainbow Home) via the recipe §3 step 3. Then they go live automatically (page already wired).
2. **Price** the dramatic-play educator products from retail (13 are $0). Then their buttons charge correctly.
3. **Split remaining shared listings** (live retail products still tagged educator — they violate Rule 2): Bauspiel Color Track `6746569212074`, Bauspiel Fairytale Windows `6751337414826`, Bauspiel Lucent Cubes `6763702517930`, Bauspiel Mirror Blocks `6887026393258`; Papoose Fairy Door `8159792267434`, Papoose Wishing Well `8159808290986`, Mushroom House w/ Carrot Garden Mat `7611596570794`. For each: make a separate educator listing → untag the retail original.
4. **dramatic-play:** ~28 page SKUs have NO educator product yet (café/bakery: COO/CUP/ICE/DON/MLK/BSB/BPG/GMT/CCP/SCN/TFG/HOT/TEA/etc.). Verified absent by tag + SKU. Need creation (recipe §3) before their buttons work. Also wire 3 featured SKUs TFV/FYS/SH (different markup).
5. **steam page:** uses retail Connetix/Bauspiel (shared) — needs dedicated educator listings.
6. **creative-arts:** wire buy buttons (same pattern as dramatic-play).
7. **Educator Catalog scope:** the market catalog currently includes ~the whole store. Scope it to a smart collection of `tag:educator` (after Backlog #3 cleans retail out of that tag) so the catalog = only the 8 sections.
8. **Always check by tag before creating** any educator product to avoid double-listing.

---

## 7. Useful queries (Shopify Admin GraphQL via MCP)

- Confirm walled: `product(id){ publishedOnPublication(publicationId:"...69325422762") publishedOnPublication(publicationId:"...152026382506") }`
- Educator set count: `productsCount(query:"tag:educator")`
- Dedicated (new) vs older: `productsCount(query:"tag:educator AND created_at:>='2026-05-25'")` (117 dedicated) vs `<` (53 older, includes retail to split)
