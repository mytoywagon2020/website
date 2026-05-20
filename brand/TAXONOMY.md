# My Toy Wagon — Product Taxonomy

> Canonical category structure for the retail store. The source of truth is the
> live shop-by-category mega-menu. Product `product_type` must use the exact
> category names below. Any session classifying products reads this first.
> Last updated 2026-05-20.

## How the taxonomy works

Four axes describe every product. Only the first is the `product_type`.

1. **Department and category** (`product_type`): one canonical category per
   product, taken from the mega-menu below. This drives nav, breadcrumbs, and
   Google Shopping type.
2. **Material** (tag or metafield, a facet, never a category): Felt and Wood are
   the brand north star. Also Cotton & wool, Silicone, Paper & card, Polyester.
   Polyester is labeled honestly on the few items that use it (e.g. Mon Ami); the
   brand otherwise favors natural materials. Material is how shoppers filter to
   natural goods and how we win on-brand long tail like "organic stuffed animals."
3. **Age** (`custom.age_band`, a facet): five bands, First year (0 to 12 months),
   Toddler (1 to 3), Preschool (3 to 5), Early school (5 to 8), School age (8+).
   Re-derived from the manufacturer's grade and safety certification
   (ASTM F963 / EN 71 / CPSIA), NOT from inherited import tags (those are about
   60 percent accurate).
4. **Pedagogy** (a facet): Montessori, Waldorf, Reggio.

## Classification rules

- **One canonical category per product.** A product that legitimately belongs in
  several places gets its category from its primary identity, and is cross-listed
  elsewhere through collections and tags, not through `product_type`.
- **Different-category safeguard.** When a product already carries a type that
  names a genuinely different category, do not blindly overwrite it from its
  collection. Example: little dolls that live in the rattles collection are dolls,
  not rattles.
- **Brand or maker identity drives the default.** Example: Nanchen defaults to
  Waldorf Dolls, unless the piece has a rattle (Rattles & Grasping Toys) or is a
  flat comfort cloth (Loveys).
- **Normalize, do not just fill blanks.** Set the canonical category on the whole
  category-defining collection, overwriting messy legacy types, except where the
  safeguard above applies.
- **Process specific before broad** so a product in both a specific and a broad
  collection lands on the specific category. Broad umbrellas
  (small-world-play, natural-baby-toys, nursery-and-playroom, pretend-play,
  educational-play, outdoor-play, the-holiday-shop) are processed last as
  catch-alls.
- **STEM vs STEAM:** retail uses "STEM Toys" (parent search volume). The educator
  portal keeps STEAM (arts-inclusive, the term educators use). Do not change the
  educator catalog.

## Execution and safety

- Product data is shared store-wide and goes live immediately. There is no
  staging buffer for it.
- A full pre-change backup of every product (id, handle, product_type, status,
  tags) lives at `backups/product-categorization-backup-2026-05-20.jsonl`. All
  changes are reversible against it.
- Changes are applied via the Admin API (`productUpdate`), collection by
  collection, verified after each batch.

## The canonical menu

Departments and their categories. Items marked (added) extend the menu but are
not yet shown in nav. `product_type` strings must match these exactly.

### Featured Collections (merchandising, not product_type)
Bestsellers · Wooden Toys · Handmade Toys · Montessori Inspired · STEM Toys ·
The Playroom Collection · Made in the USA · Spring Nature Table

### Blocks & Building
- Wooden Blocks
- Marble & Ball Runs
- Stacking & Sorting

### Pretend Play
- Kitchen & House Play
- Stuffed Animals
- Wooden Animals
- Toy Vehicles
- Dress-ups & Costumes

### Arts & Crafts
- Painting & Drawing
- Handwork
- Other Crafts

### Dolls & Dollhouses
- Dolls
- Doll Accessories
- Dollhouses
- Dollhouse Dolls & Furniture
- Maileg Collection

### Waldorf Essentials
- Waldorf Dolls
- Waldorf Home
- Waldorf Birthday
- Playsilks
- Fairies & Gnomes

### Developmental Toys
- Early Learning
- Musical Instruments
- STEM Toys
- Montessori Toys

### Baby
- Rattles & Grasping Toys
- Plush Baby Toys
- Baby Walkers & Pull Toys
- Teethers (added)
- Loveys (added)
- Blankets & Swaddles (added)

### Games & Puzzles
- Games
- Puzzles
- Books

### Active Play
- Outdoor Toys
- Riding & Climbing Toys (ride-ons and hobby horses)
- Swings & Hammocks

## Naming notes

- "Stuffed Animals" names the form, not the material. Natural-fiber soft animals
  live here; the rare polyester ones are tagged Polyester. Bella Luna uses the
  same term.
- "Loveys" is the chosen term over "Comforters" to avoid confusion with bedding.
- "Blankets & Swaddles" keeps flat textiles together, separate from Loveys.
- "Rattles & Grasping Toys" matches the menu and Bella Luna; rattles and grasping
  toys are one category, not two.

## Progress log

- 2026-05-20: backup taken; pilot and first passes complete.
  - Marble & Ball Runs (17), Teethers (14), Riding & Climbing Toys / hobby horses
    (15), Musical Instruments (33).
  - Nanchen brand cleanup (98): Waldorf Dolls (63), Loveys (18),
    Rattles & Grasping Toys (13), Stuffed Animals (4).
