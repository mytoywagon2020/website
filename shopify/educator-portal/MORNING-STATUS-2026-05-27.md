# Morning Status — 2026-05-27

## Connetix line: 43/43 products now have real-spec deep-dive descriptions ✓

Every Connetix product in the shop now has:
- Vendor: **My Toy Wagon**
- Real piece-count breakdown verified against Connetix official + 5+ major retailers (Amazon, Staples, Bright Bean, Toppings Kids, Maude Kids, Smallable, Mindware, Toy Insider, Lil Tulips, Hello Archie, etc.)
- Educator-voice paragraph framing + Educator notes paragraph
- Materials/safety boilerplate (ABS plastic, ultrasonic welding + rivets, BPA-free + phthalate-free, bevel design, strong magnets)
- Ages 3+ with choking hazard warning
- Origin: Designed in Australia by Connetix; manufactured responsibly

### Source mix (43 total)

**User-provided real specs (5):**
1. PRO Constructor Set 70pc — Smart-Spin tech, ages 5+
2. Bright Portal Pack 48pc — 8 bright colors, Portal pieces, Smart-Spin mini-squares
3. Star Light Pack 28pc — rechargeable light-up tile, LR44 battery, 3 dimming settings
4. Glitter Castle Pack 48pc — iridescent glitter, inspiration book
5. Glitter Unicorn Pack 56pc — full piece breakdown, pink/yellow/teal/purple brights

**Web-research verified specs (38):**

Mega + Starter + Creative (6):
- 212 Rainbow Mega Pack
- 202 Pastel Mega Pack
- 102 Rainbow Creative Pack
- 120 Pastel Creative Pack
- 60 Rainbow Starter Pack
- 64 Pastel Starter Pack

Mini (2):
- 24 Rainbow Mini Pack
- 32 Pastel Mini Pack

Ball Run + Expansions (5):
- 92 Rainbow Ball Run
- 106 Pastel Ball Run
- 134 Super Ball Run
- 66 Rainbow Ball Run Expansion (note: includes X-tubes + spiral tubes)
- 80 Pastel Ball Run Expansion (note: includes X-tubes + spiral tubes)

Replacement balls (2):
- 12 Rainbow Replacement Ball Pack
- 16 Pastel Replacement Ball Pack

Transport / Motion / Roads / Car (5):
- 50 Rainbow Transport Pack
- 50 Pastel Transport Pack
- 24 Motion Pack
- 2 Car Pack
- 48 Creative Roads Pack
- 16 Ramps & Intersections Pack

Base Plates (4):
- 2 Base Plate Blue & Green
- 2 Base Plate Lemon & Peach
- 2 Base Plate Pink & Berry
- 2 Clear Base Plate Pack

Shape Expansions (3):
- 36 Rainbow Shape Expansion Pack
- 48 Pastel Shape Expansion Pack
- 24 Clear Shape Expansion Pack

Geometry (2):
- 30 Rainbow Geometry Pack
- 40 Pastel Geometry Pack

Squares (2):
- 40 Pastel Square Pack
- 42 Rainbow Square Pack

Rectangles (3):
- 18 Rainbow Rectangle Pack
- 24 Pastel Rectangle Pack
- 12 Clear Rectangle Pack

Clear Starter (1):
- 34 Clear Starter Pack

Charity (2):
- Charity Pack Pink 20pc → breast cancer research (20% to Australian Breast Cancer Research)
- Charity Pack Teal 20pc → MND/ALS research (20% to FightMND) ⚠️ **CORRECTION**: was previously described as "ovarian cancer awareness"; the official Connetix Teal pack is MND awareness, not ovarian. Updated accordingly.

## Non-Connetix product status

All 18 educator-only products (ButtonandBug trays, Análu doughs, Cow Shed, kaleidoscopes, sets) already had rich educator-voice descriptions, vendor "My Toy Wagon", and full educator metafields (developmental_age, materials, certifications, bundle_components, replacement_parts). No deep-dive needed on those.

Other shop-wide vendors (Tara Treasures, Wonderheart, Drewart, Bumbu, Wooden Story, Brin d'Ours, Papoose) — these are NOT in the educator-only set; their PDPs are retail-side and were not part of the educator portal scope. Flag for the morning whether you want descriptions enriched on those too — if yes, I'll start with the highest-revenue items first.

## Fairy Villages page

- Cover: **MushroomHousewithCarrotGardenMat1.png** (Toadstool House) — wired
- Section 04 Hero Product: **MushroomHousewithCarrotGardenMat4.webp** — wired
- Cover tag label: updated to "TOADSTOOL HOUSE"

## Vendor / origin reference (from CLAUDE.md + SHOPIFY_NOTES.md)
- Connetix → designed in Australia, manufactured responsibly
- Drewart → Poland (NOT Germany)
- Análu → USA
- ButtonandBug → USA (Furniture Grade Hard Maple)
- Wonderheart → Vermont, USA
- Bumbu → Romania
- Tara Treasures → Australia/Nepal
- Wooden Story → Poland
- Brin d'Ours → France
- Papoose → Australia/Nepal
- All educator-only products: Shopify `vendor` field = "My Toy Wagon"

## Retail-side vendor catalog scale (scouted, not yet deep-dived)

The store has ~50+ vendors beyond Connetix. Spot-check on three priority vendors:
- **Drewart (Poland)**: 100+ products, most with passable existing descriptions ("The Drewart Collection is exempt from discounts. This item ships for free...") but no per-product real-spec deep dives. Includes Camper Van $410, Kitchen $455, Cupboard $530, Large Fastness $770, Medium Castle $320, Sink $420, Stove $399, Catapult $98, Cash Register $140, Doll Wardrobe $190, Jeep variants $320–$338, Chopping Board $12, Duck Push Toy $32, Dwarf's House $142, Flower Press $60, plus 80+ more.
- **Tara Treasures (Australia/Nepal)**: hundreds of products — finger puppets, play mats, dolls, garlands, life cycle sets, mobiles. Pricing $22–$62 typical. Already has decent narrative descriptions per item.
- **Wonderheart (Vermont)**: 30+ wooden gnomes (mini + standard, rainbow + pastel palettes), Colors of the Week set $112. Existing descriptions are all the same template ("Meet our enchanting wooden gnomes..."), would benefit from per-product differentiation.

A deep dive on all retail-side vendors at the depth I gave Connetix would be hundreds of products and is too broad to tackle without owner priority. **Recommended approach to discuss in the morning:**
1. Pick a vendor tier to start with (suggest Wonderheart first — small catalog, current copy is uniform, biggest lift-per-hour)
2. Or pick a specific product type (e.g. Drewart "signature" items: Camper, Kitchen, Castle, Fastness — the big-ticket SKUs that justify rich copy)
3. Or skip retail-side entirely and focus on educator portal final polish before launch

## Open questions for the morning
1. **Retail-side vendor priority**: pick from above options (Wonderheart first / Drewart big-ticket / skip retail). Tell me an ordered list and I'll work through it tomorrow night.
2. Confirm the Teal Charity Pack correction (MND/ALS, not ovarian). If you have a contradicting source, push back and I'll revert.
3. Preview the Fairy Villages cover at /pages/educator-fairy-villages once the theme is republished — confirm the Toadstool House image renders flush-in-frame at the new aspect.

## Files changed tonight
- `shopify/educator-portal/templates/page.educator-fairy-villages.liquid` — Mushroom House #1 cover + Mat 4 in Section 04 Hero Product
- 43 Connetix products updated in Shopify Admin (no git change — remote API)
- This file
