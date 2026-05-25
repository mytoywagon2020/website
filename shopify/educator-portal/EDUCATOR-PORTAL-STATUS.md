# Educator Portal — Master Status & Run List
_Last updated: 2026-05-25. Pick up here if disconnected. Companion docs: `EDUCATOR-PORTAL-RUNBOOK.md` (tags/SOP/red flags), `EDUCATOR-CATALOG-WORKSHEET.md` (not-on-retail items)._

Branch: `claude/kind-bardeen-lX5a2` (PR #6). Staging theme: `gid://shopify/OnlineStoreTheme/145914462378` ("Educator Portal Staging"). Live theme (MAIN): `145720180906`. Everything below is on the staging theme/branch; **publishing that theme = go-live**.

## Key IDs
- Educator Catalog (market catalog): `gid://shopify/MarketCatalog/64883065002` · publication `gid://shopify/Publication/152026382506` · price list `gid://shopify/PriceList/24074289322` (0% + manual).
- Educators market: `gid://shopify/Market/32754958506` (applies to ALL company locations).
- Seasonal windows metaobject: `gid://shopify/Metaobject/202418421930` (Content → Metaobjects → "Educator delivery windows"); shop metafield `educator.settings`.
- Fast PDP: section `sections/mtw-fast-pdp.liquid`, template suffix `fast-pdp` (`templates/product.fast-pdp.json`).
- Erin Kim (live-data demo): `Customer/8984220303530`, Company "Elk Grove Elementary School" `Company/1464893610`, location `CompanyLocation/1567097002` (checkoutToDraft + Net-60). Orders #24207/#24210/#24211 tagged `po-paid-external`; #25583 = `invoice-sent`.

## DONE
- Gate funnel: `snippets/educator-gate.liquid` + all 8 section templates + `page.educators` + portal pages; gate accepts `customer.b2b?` OR `educator-approved` tag. noindex + robots.txt crawl-block.
- Small World → "Small World & Storytelling" rename.
- Educator Dashboard (`page.educator-dashboard`): snapshot stats, seasonal banner (auto-swap photo, reads metaobject), guided first-order state, color, mobile cards, live orders+invoices, native fulfillment/tracking, payment via `po-paid-external`/`invoice-sent` tags, account/vendor-docs/support, quote routing by account type (B2B → cart-as-quote, tag-only → /pages/new-quote).
- Quote builder `page.new-quote` (cart-as-quote, 45-day hold, no allocation, shipping/tax manual).
- Fast PDP educator panel: terms, seasonal pre-order (reads metaobject), curriculum, min, add-to-quote, pricing clarifier; `educator.exclusive` (retail→"educator program") + `educator.continue_selling` controls.
- Connetix (35): draft + fast-pdp + `educator.exclusive` + `educator-steam` + in Educator Catalog.
- Fairy seeded (8) incl. confirmed rainbow matches; Bumbu Flower Children DRAFT bundle (exclusive, made_to_order).
- Pages: 17 educator pages published; retired po-legacy (deleted), catalog-guide/schools/login (unpublished). educator-program SEO (broad: "Natural Classroom Toys for Schools & Districts").
- Metafield defs: product `educator.{terms,delivery_model,next_delivery,min_qty,curriculum,exclusive,continue_selling}`; customer `educator.trusted_hold`; shop `educator.settings`.

## RUN LIST (outstanding)
1. **Catalog product build-out** — a background agent was creating draft listings / re-pointing retail products to fast-pdp + tagging into sections + publishing to Educator Catalog + setting `details.audience_educator` benefits. **Owner rule: no agents — verify everything it did, then continue MANUALLY.** Verify per product: status, templateSuffix=fast-pdp, educator-<section> tag, in Educator Catalog publication, no duplicates.
2. **Section images — outstanding:**
   - **creative-arts (08): 0 product images.** Candidate Files: `preview_1/2/5/6/7/8/9/10.webp` (weaving/dough/press/petals/felt-flowers — names ambiguous, CONFIRM which is which), `specimen_kit_preserve_and_display_1.webp`, `specimen_collecting_kit_by_june___december3...webp`, `Untitled_design_95...png`.
   - **dramatic-play (07): 0 product images.** Files: `Egg_Rolls_Hand_Rolls.png`, `Sushi_Bento_Box.png`, `Yum_cha.png`, `Mixed_Sushi_roll.png`, `pasta.png`, `Milkshakes.png`, `Felt_Fruits_and_Vegetables_A_B_C_D.png`, `Felt_Donuts_Set_of_4_900x...webp`, `PapooseHotDrinksSet_...webp`, `TL8239-birdie-tea-set-8_900x...webp`, `ErziWoodenBigBoxPlayFoodAssortmentSet_720x...webp`, `FeltFarmAnimalsToys_Setof10...webp`, `safariplayset...webp`, `2J2A2060-2...webp`, `Untitled_design_61...png`.
   - **STEAM (06): 7 "Coming soon" slots** (products without images). New Connetix Files available: `Connetix_Mega_Pack_212pc`, `Connetix_Creative_Pack_102pc`, `Connetix_Geometry_Pack_30pc`, `Connetix_Ball_Run_92pc`, `Connetix_Roads_Ramps_64pc`, `PRO_Constructor_70pc`, `Glitter_Castle_48pc`, `Glitter_Unicorn_56pc`, `Light_Star_28pc`, `Bright_Portal_48pc`; Bauspiel: `Lucent_Cubes.png`, `wooden_mirror_blocks.png`, `fairytale_windows.png`, `Bauspiel_Color_Street.png`, `Bauspiel-Glittering-Sparkling-Stones-Flower-13.webp`; `pg34_*kaleidoscopes`, `pgX_opener03_science-tinkering.webp`.
3. **Degraded image refs (owner-flagged).** Sensory uses `file_url` (20 refs); some may point to filenames no longer in Files. Files-inventory diff (2026-05-25): `Rainbow_Play_Tray.webp` ✅ present in Files, `wooden-story-montessori-sand-tray.png` ✅, `wooden-story-2-part-sand-tray-flashcard-holder.png` ✅, `wooden-story-sand-tray-tools-set-of-4.png` ✅ (all four present, NOT broken). STILL SUSPECT: `buttonandbug-cake-sensory-tray.png` — only `buttonandbug-cake-tray-product.png` / `buttonandbug-cake-tray-lifestyle*.png` are in Files; the `-sensory-tray` filename may be a theme ASSET only, so a `file_url` ref to it would break. **TODO: verify that one ref on the sensory page renders; repoint to `buttonandbug-cake-tray-product.png` if broken.** Other sections use `asset_url` (theme assets) which are present.
4. **Educator landing page (`page.educators`)** — build the hub: 8-section grid with **cover images**, value stack, how-it-works, Apply/Sign-in. Covers available: `sensory-cover`, `np-cover-busy-bee-feet`, `wd-cover-acorn-house`, `sw-cover-lifestyle`, `fairy-cover-pink-blossom`; **STEAM/dramatic/creative covers may need selection.**
5. **Links live everywhere** — ensure the 8 section links + portal links work on: landing, footer (every page), each section page, and every portal page.
6. **W-9 / COI** — pending (no updated W-9; COI ~next week). Email-request fallback live; wire one-click downloads when files arrive (Content → Files → Copy link).
7. **PO-upload Shopify Form** — create in admin (native, file upload), link from dashboard.
8. **Saved classroom lists** — needs app (Swym Wishlist Plus rec); reorder is native.
9. **Launch (Tue):** owner publishes the staging theme. Then publish remaining drafts as desired.

## Alt-text SEO pass (Files) — IN PROGRESS (2026-05-25)
Setting descriptive, keyword-rich SEO alt on every empty-alt File via `fileUpdate`. Pattern: "[Brand] [product], [detail] for [play type]" (e.g. "Connetix 212-piece magnetic tiles mega pack… for classrooms"). DONE so far: ALL educator-portal imagery (section products + covers for sensory/nature/woodland/small-world/fairy/STEAM/dramatic-play/creative-arts), all Connetix/Bauspiel STEAM packs, dramatic-play felt food (Papoose/Tara/Erzi), creative-arts specimen kits, fairy houses, Bumbu woodland animals+trees, small-world storytelling sets, sensory trays (Button&Bug/Gus&Mabel/Análu), nature-play loose parts, logos/trust-marks, and the bulk of the retail marketing set (`product-*`/`category-*`/`brand-*`/`age-*`/`hero-*`/`lifestyle-*` — note these were uploaded in 2+ duplicate batches, all alt'd). **REMAINING: keep paging older retail Files (sortKey CREATED_AT desc) until none left.**
**Skipped as AMBIGUOUS — need owner to identify before alt/section use:** `preview_1/2/5/6/7/8/9/10.webp` (creative-arts candidates), `Untitled_design_35/61/95*.png`, `2J2A2060-2*.webp`, `212mega_1.png` (set generic Connetix alt), `Gry_Sif*.png` (brand only), `magica-3856-ls3*.webp`, `Ganapati_Crafts_Co.png` (brand only), `bigsister.png`, UUID-only names (e.g. `9d3337fa-…png`, `3_0ad9cad3-…webp`, `fd5800ca-…png`), `Photo*`/`Screenshot_*` (reference shots), and the `Frame*`/`Side.gif`/`Angled.jpg`/`RustPatrol*`/`TokyoHeat*`/`Banks.jpg` block (design exports + what look like NON-toy leftover assets — confirm these belong here). `GenericFile` entries are the theme `.liquid` uploads (their "alt" is a build note) — leave as-is. Videos: alt left blank (content unknown).

## Red flags (see RUNBOOK for detail)
- **Shopify Capital workaround (temporary):** never mark PO orders "Paid" natively (Capital remits); use `po-paid-external`/`invoice-sent` tags. Remove after the loan is paid.
- **Status-tag discipline** determines dashboard accuracy — keep a saved admin view for untagged PO orders.
- **Pricing:** 0% list + volatile prices → no catalog discount; value-position + quote pricing.
- **Order API access:** Erin's B2B orders aren't reachable via this connection — tag in admin.
