# Catalog Rebuild Changelog — Web → Print/PDF sync

Running list of changes made to the **web educator portal** that the **print/PDF catalog must be rebuilt to reflect**. Grouped by topic/section. Newest work at top of each list. Branch: `claude/kind-bardeen-lX5a2`.

> Web exceeds catalog on purpose: the print catalog had to fit one page per section (8.5×11); the web is infinite, so some grids carry extra products (flagged below). The print rebuild should adopt the **structure, naming, pricing, and corrections** here even where it can't carry every extra SKU.


## How to use this for the rebuild

**The Educator Catalog is the source of truth.** When a web edit conflicts with the catalog: default to the catalog, UNLESS the web edit is a genuine correction or newer data (real prices, new SKUs, fixed mis-bindings) — in which case keep the web version and record it under **"Catalog updates needed"** below so the print/PDF is brought in line on the next rebuild.

## Catalog updates needed (web is now ahead of print)

- **Connetix Creative Pack is 102pc / $99** (current; the **100pc is discontinued**). Catalog is already at 102 — no change needed; noted to avoid re-introducing 100pc.
- **Connetix prices → current retail (regular):** Mega 212 $209 · Creative 102 $99 · Geometry 30 $55 · Ball Run 92 $85 · PRO Constructor 70 $99 · Glitter Unicorn 56 $79 · Portal 48 $69. (To confirm: Roads & Ramps 64, Glitter Castle 48, Light Star 28.)
- **Connetix bundles priced** (component sum − 10%, MAP cap): Starter $139 · Mid $265 · Full $533.
- **STEAM split into three sections** (was merged): Observation Station / Hand-Felted Biology / Deep Time.
- **Specimen Study Station** hero added (June & December bundles).
- **Transparent Windows 25pc ($152)** replaces Sparkling Stones.
- **DP Kitchen split** into Pantry / Sweet Shop·Bakery / Sweet Shop·Treats; **Food Groups now the Pantry anchor** (moved from STEAM).
- **6 new Connetix products** added to the range (see table).
- **Use latest Connetix counts/prices** from the site screenshots for Starter (62/$65), Square (40/$59), etc.
- **Edition name = "2026 Autumn Edition"** (was a Spring/Fall mix).
- **Creative Pack:** keep at **102pc** (100pc discontinued); image `Connetix_Creative_Pack_102pc.webp` is correct.

---

## Global rules (apply catalog-wide)

- **Season naming — Autumn (public) / Fall (schedule).**
  - **Autumn** = product names, public display copy, and the edition name → **"2026 Autumn Edition"** (was a mix of "Spring"/"Fall").
  - **Fall** = schedule/calendar only (booking + delivery windows, "book in the fall").
  - **Spring removed** from all theme/edition copy. Kept only as a *delivery/booking* window (Fall-first) and in the literal 4-season Seasonal Trees product.
- **Educator price = REGULAR price** (never a retail sale/markdown).
- **In-stock rule:** educator items always show a price + order CTA (made-to-order / continue-selling). No "Coming soon."
- **Bundle pricing:** sum of component regular prices − **10%** (flat; **10% is the maker MAP ceiling**; bundles only, never individual packs). Show contents + list total + savings.
- **Grid symmetry:** in uniform card grids, any row with **<5 cards is centered**.
- **Card metas = SKU-only** (drop repeated maker/category; keep genuine piece-count specs like "3 sets").
- **Cert claims:** only cite verified-per-maker. Papoose = **WFTO + Fair Trade USA**; Tara Treasures = **Fair Trade USA Certified** (designed Melbourne, made by women artisans in Nepal). Removed unverified OEKO-TEX/GOTS where not confirmed. **Still to verify:** FSC, GOTS, OEKO-TEX, BSCI, IDEA Part B / Medicaid OT funding, Junior Design Awards 2021.

---

## STEAM

- **De-conflated into three distinct sections** (were merged into one grid):
  1. **The Complete Observation Station** (`MTW-ST-OBS`): Wooden Microscope, Magnifier Set, My Little Museum Bug Box, Binoculars, Compass, Specimen Collecting Kit, **Optical Blocks** (moved in).
  2. **Hand-Felted Biology:** Frog / Butterfly / Bee / Bean life cycles + Human Anatomy (dinos/optics/nutrition removed).
  3. **Deep Time** (NEW): Papoose Jurassic hero (`MTW-ST-PDM`) + Prehistoric Set (`MTW-ST-BPS`), Dinosaur Eggs (`MTW-ST-BDE`), Dinosaur Life Cycle (`MTW-ST-TLC`).
- **Specimen Study Station** hero added (June & December): Starter (26 bottles/2 forceps/36 labels, `MTW-ST-JDB-S1`) + Complete (58/4/72, `MTW-ST-JDB-S2`); priced as a package on quote.
- **Sparkling Stones → Bauspiel Transparent Windows 25pc** (`MTW-ST-BTW`, **$152**). Bauspiel section index now MIRROR · LUCENT · FAIRYTALE · COLOUR · TRANSPARENT.
- **Bauspiel specialty grid** images updated: Mirror Blocks, Lucent Cubes 100, Fairytale Windows, Color Track 45, Transparent Windows 25.
- **Food Groups Nutrition Set removed from STEAM** → moved to DP Pantry.
- **Kaleidoscope hero**: dedicated image, shown contained (full image / child's face visible, sharp).
- **Connetix prices corrected to real retail (regular):** Mega 212 **$209**, Creative 102 **$99**, Geometry 30 **$55**, Ball Run 92 **$85**, PRO Constructor 70 **$99**, Glitter Unicorn 56 **$79**, Bright/Pastel Portal 48 **$69**. ⚠ *Estimates to confirm:* Roads & Ramps 64 **$89**, Glitter Castle 48 **$79**, Light Star 28 **$55**.
- **Connetix tiered bundles priced (component sum − 10%):**
  - Starter (Creative 102 + Shape Expansion) **$154 → $139** (`MTW-ST-CCS`)
  - Mid (Starter + Ball Run + Geometry) **$294 → $265** (`MTW-ST-CCM`)
  - Full (Mid + Roads & Ramps + Mega) **$592 → $533** (`MTW-ST-CCF`)
- All "Coming soon" replaced with prices (Kaleidoscope from $34, etc.).

## Dramatic Play

- **Kitchen & Café split** into: **The Pantry** (5), **Sweet Shop · Bakery** (6, adds Pavlova), **Sweet Shop · Treats** (5).
- **The Pantry** now anchored by **Food Groups, Nutrition Set** (`MTW-DP-TFG`) → Food Groups, Bread, Pasta, Charcuterie & Cheese, Artisan Preserves & Scones. (Replaces the old standalone produce card.)
- **Farmyard** reordered (Cow Shed hero + grid card, Farm Mat, Animals set-of-10, Tractor, Hay Wagon, Fences, harvest extras); 9-card grid centered.
- **Shop Scene** gains a lead lifestyle image ("Pantry Becomes a Shop"), shown at natural ratio.

## Sensory Play

- Therapy-dough index lists all **7 scents** (incl. Mojito `MTW-CA-ANM`, Pumpkin Spice `MTW-CA-ANP` — web extras beyond the 5 in print).
- Calm Corner origins alphabetized; Calm Corner intro de-duplicated from the pull-quote; "coming soon" cross-link label removed.

## Nature Play

- Section is **Autumn**-themed (Spring removed from copy).
- **Fix:** Felt Pinecones "Add to cart" now fires `MTW-NP-PNC` (was mis-bound to `MTW-NT-MSH-G`).
- "Nature Tools · Papoose" divider repositioned before the Nature Tools grid.
- "Autumn Folk" Bumbu/Moonpicnic wood grid is a web extra (not in print).

## Woodland

- Papoose **Seasonal Trees** kept as a true 4-season product (spring/summer/autumn/winter is its literal feature).
- Cert copy: FSC-certified (to verify), WFTO & Fair Trade USA.

## Small World

- **Fix:** Gus + Mabel felt habitats corrected from "**eight**" to "**five**" everywhere (matches the `MTW-SW-FB5` bundle + the 5-card grid: TTT/FST/FPP/CCV/WWW).

## Fairy Villages

- **Fix:** Mushroom Garden hero "Add to cart" now fires `MTW-FV-MUS` (was a text slug). Hero $228.
- Wonderheart pairing price corrected ($118 → $108).

## Creative Arts

- Sections present & grouped (Florals, Threading, Dough, Eco-Cutters, Modeling Tools, Paints, Presses, Mindful Potion).
- Card metas reduced to SKU-only (stripped repeated "Hand-felted wool", maker names; kept piece-counts).
- Play Dough Tool Set (10pc) new image; eco-cutters standardized to Ages 3–8; intro copy fixes.
- ⏳ *Pending:* grid order differs from print (print leads with Weaving p59; web leads with Florals) — reorder TBD.

---

## New Shopify products created (DRAFT, our SKUs)

Created to fill gaps in the Connetix range. **Need maker barcodes + product images** (important for Google/Shopping once public). Barcode = keep maker's; SKU = ours.

| Product | Price | Our SKU |
|---|---|---|
| Glitter Unicorn Pack 56pc | $79 | MTW-ST-CGU |
| PRO Constructor Set 70pc | $99 | MTW-ST-CPR |
| Super Ball Run Pack 134pc | $149 | MTW-ST-CSB |
| Charity Pack Pink 20pc | $45 | MTW-ST-CHP |
| Charity Pack Teal 20pc | $45 | MTW-ST-CHT |
| Pastel Portal Pack 48pc | $69 | MTW-ST-CPP |

---

## Open items (owner input needed)

- **Barcodes + images** for the 6 new products (matters for Google Shopping when public).
- **Confirm prices:** Roads & Ramps 64 ($89?), Glitter Castle 48 ($79?), Light Star 28 ($55?) — not in retail screenshots; Glitter Castle / Light Star may be discontinued.
- **Variant ambiguities** (new SKU vs rename): Rainbow Creative 100 vs existing 102; Rainbow Starter 62 vs 60; Rainbow Square 40 vs 42.
- **Existing ~35 Connetix products** have blank SKUs → assign ours (in progress).
- **Cert verifications:** FSC, GOTS, OEKO-TEX, BSCI, IDEA Part B / Medicaid OT funding, Junior Design Awards 2021.
- **Public catalog landing page** (the one real SEO lever — HTML page hosting the PDF; gated portal pages are not indexed).
