# My Toy Wagon — Educator Print Catalog Structure Map

_Source: `ff093a24-MTW_Catalog_v22r23_EMBEDDED.html` (My Toy Wagon, 2026 Educator Catalog, Vendor Edition). Parsed in document order; images stripped._

## Summary

- Ecosystems: **8**
- Sections (distinct ecosystem + sub-section pairs, including ecosystem-opener products with no sub-section): **21**
- Products: **25**
- Products with a SKU: **18** (missing: 7)
- Products with an educator price: **0**
- Products with any other price: **0**
- Products with an eyebrow/kicker: **25**

### Scale note

This is a curated print catalog, not a full product database. It presents **8 ecosystems** and **25 hero/bundle product cards** drawn from a much larger range — each card represents a flagship item or curated bundle rather than every SKU My Toy Wagon sells. The original brief anticipated ~64 sub-sections and inline educator pricing; the actual file contains 8 `opener-title` ecosystems, ~32 styled section headers (of which the ones following the first ecosystem opener are real product sub-sections), and **25** `product-title` cards. Therefore the true catalog is far larger than these 25 hero cards; a complete SKU-level catalog would need the full price list / line-item workbook, which is not embedded in this HTML.

### Parsing assumptions

- **No prices of any kind exist in this HTML.** There are no dollar figures, and the `educator-price` / `cell-educator-pricing` classes appear only in CSS, never as populated elements. The order form table and the standards-mapping table are both price-free. `educator_price` and `other_price` are therefore empty for every product, by faithful design — not omitted.
- Ecosystems = `<h1 class="opener-title">`. Sub-sections = styled `<h2>` headers that are not product titles, attributed to the preceding ecosystem. Front-matter headers before the first ecosystem (e.g. "Built Around How Children Learn") are excluded.
- The first product in each ecosystem appears directly under the ecosystem opener spread, before any sub-section header; its section is shown as _(ecosystem opener)_.
- One SKU span (`Specimen Study Station`) embeds a bundle descriptor after a middot; the SKU field keeps only the leading code (`MTW-ST-JDB-S1`), faithfully, with no invented data.

---

## Sensory Play

### _(ecosystem opener)_

- Rainbow Imaginative Play Tray — MTW-SP-IPT — (no price) _[Buttonandbug · Featured]_

### The Imaginative Play Range

- Letter Tracing Insert — MTW-SP-LTI — (no price) _[Buttonandbug · Literacy]_

### Therapy Dough

- My Forest Floor — MTW-NP-TLF — (no price) _[Tender Leaf Toys · Featured]_

## Nature Play

### _(ecosystem opener)_

- Busy Bee Tray — MTW-NP-BBT — (no price) _[Gus + Mabel · Featured]_

### Nature Tools

- The EverythingPlay Bundle — MTW-SP-WMC-EPB — (no price) _[Wild Mountain Child · Featured]_

## Woodland Collection

### _(ecosystem opener)_

- The Deer Family — MTW-WD-DEER — (no price) _[Bumbu · Featured]_

### Woodland Trees

- Seasonal Trees — MTW-WD-PST — (no price) _[Papoose · Featured]_

## Small World & Storytelling

### _(ecosystem opener)_

- The Forest Caves Play Mat — MTW-SW-FCV — (no price) _[Papoose · Featured]_

### Hobbit Hollow + Gnomes

- The Gruffalo Bundle — MTW-SW-GRF — (no price) _[Tara Treasures · Story Bundle]_
- Puppets for the Natural World — (no SKU) — (no price) _[Tara Treasures · Science & Nature Puppets]_
- Circle Time Puppets for Numbers & Songs — (no SKU) — (no price) _[Tara Treasures · Counting Puppets]_

## Fairy Villages

### _(ecosystem opener)_

- Mushroom Garden Fairy Home — MTW-FV-MUS — (no price) _[Tara Treasures · Felt Fairy Home]_

### Five Fairy Homes for the Nature Table

- Every Village Needs Its People — MTW-FV-RGN — (no price) _[Wonderheart · Little Folk]_

## STEAM · Wonder & Investigation

### _(ecosystem opener)_

- Kaleidoscopes of Natural Materials — MTW-ST-AMB — (no price) _[Amber Kaleidoscope · Featured]_
- Magnetic Tiles for the Classroom — MTW-ST-CRM — (no price) _[Connetix Tiles · To Construct]_

### Specialty Connetix: Beyond the Rainbow

- Gem Blocks & Mirror Geometry — MTW-ST-BCT45 — (no price) _[Bauspiel · To Illuminate]_
- Wooden Microscope — MTW-ST-QTM — (no price) _[Q Toys · To Observe]_

### The Complete Observation Station

- Specimen Study Station — MTW-ST-JDB-S1 — (no price) _[June & December · Curated Bundles]_

### Cycles, Bodies & Systems

- Deep Time in Felt & Wood — (no SKU) — (no price) _[Papoose, Bumbu & Tara Treasures · A Small-World Study]_

## Dramatic Play

### _(ecosystem opener)_

- The Cow Shed — MTW-DP-DCS — (no price) _[Drewart · Featured Heirloom]_

### The Shop Scene

- The Harvest — MTW-DP-TFV — (no price) _[Tara Treasures · From Garden to Shop]_

### The Pantry

- When the Pantry Becomes a Shop — (no SKU) — (no price) _[The Range · In Practice]_

## Creative Arts

### Eco-Cutters & Stamps

- The Stamp, the Shape, the Story — (no SKU) — (no price) _[Eco-Cutters · STEAM & Creative Arts]_

### Pigment & Paper

- The Heirloom Press — (no SKU) — (no price) _[June & December · Featured]_

### Small Alchemies

- The Floral Collection — (no SKU) — (no price) _[Felt Florals · Collection]_

---

## Reconciliation (ecosystem 1 sample)

Read-only check against the live Shopify store for the first ecosystem only
(**Sensory Play**), to bound API cost. Each catalog SKU was looked up via
`productVariants(query:"sku:<SKU>")`.

- SKUs checked: **3** (`MTW-SP-IPT`, `MTW-SP-LTI`, `MTW-NP-TLF`)
- Matched in Shopify: **0**
- Not found: **3**

Not-found SKUs:

- `MTW-SP-IPT` — Rainbow Imaginative Play Tray
- `MTW-SP-LTI` — Letter Tracing Insert
- `MTW-NP-TLF` — My Forest Floor

**Match rate (ecosystem 1): 0 / 3 (0%).** The catalog uses internal
`MTW-`-prefixed vendor SKUs that do not correspond to live Shopify variant
SKUs in this store, so none resolved. This is a sampled check by design;
**full reconciliation across all 8 ecosystems (18 SKUs) is a follow-up task**
and was intentionally not run here to bound API cost.
