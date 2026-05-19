# Fast PDP Rollout: Pilot Batch Tracking

Status: **PILOT COMPLETE** — 27 products written and verified, 3 held.
All 5 enrichment agents finished. Results below.

Last updated: 2026-05-19.

---

## What this pilot is

- 25-target pilot, **sub-$250 only**, drawn from the bestseller cohort
  (top products by gross sales, last 365 days).
- 30-title candidate pool (over-provisioned so premium/held items still
  net ~25 written).
- Reference standard: "Felt Farm Animals Toys, Set of 10" canary, already
  live on `templateSuffix: fast-pdp`, verified.

## Guardrails enforced by every agent

- Price >= $250 -> PREMIUM-HOLD, not written (awaits explicit
  "approve premium").
- Bumbu -> BUMBU-HOLD, human-only (prior owner corrections make Bumbu
  copy manual).
- Pre-order / Shopify Collective / thin or dirty description /
  missing age -> flagged and skipped, never guessed.
- Every field grounded only in the product's own title, description,
  tags, and image. No invented facts, origins, certifications, or
  collection names.
- American English, complete sentences, no em-dashes, no exclamation
  marks. Exact canary metafield schema.

## Candidate pool by agent slice

**Felt food:** Felt Ice Cream Set; Felt Fruits & Veg Set C; Set B; Set A;
Set D; Felt Pasta Play Food Set.

**Felt mats:** Large Felt Farm Mat; Gruffalo Playscape Play Mat; Felt
Safari Animal Toys Set of 6; Papoose Forest Caves Play Mat; Papoose
Rockpool Tray; Felt Rainbow Fairy Home and Mat.

**Puppets:** Gruffalo Finger Puppets Set; Room On The Broom Finger Puppets
Set; Ingenious Insects Finger Puppets and Book Set; Five Little Ducks
Finger Puppet Set of 6; Itsy Bitsy Spider Finger Puppet Set of 3; Sabo
Concept Nutcracker Play Theater and Magnetic Figurine Set.

**Seasonal/decor:** Felt Christmas Play Food Grazing Box Set B; Set A;
Colorful Rainbow Hedgehog; Wild Mountain Child Leaf Cup; Bauspiel Tooth
Fairy Box; Tender Leaf Stacking Forest.

**Fairy/accessories:** Fairyshadow Strawberry Baby Necklace Red;
Fairyshadow Love Bug in Leaf Necklace; Lilac Fairy Blossom House; Papoose
Fairy Door; Puff Kids World Map; Toverlux Magic Wooden Lamp.

## Premium bestsellers auto-held (not in pilot, await "approve premium")

Drewart Camper Van; Drewart Kitchen Cupboard; Magic Wood Tree House;
Magic Wood Giant Marble Tree; Bauspiel Large/Small Fairytale Castle;
Bauspiel Color Track 45; Bauspiel Lucent Cubes 100; Mesasilla Bookshelf;
Forest Gnome Family; Red Mushroom Family; and other cohort items priced
at or above $250.

## Results (PILOT COMPLETE: 27 written, 3 held, 0 errors)

DONE = written to Shopify on `templateSuffix: fast-pdp`, verified by
re-query, zero userErrors.

| # | Product | Status | Live URL | Flags |
|---|---------|--------|----------|-------|
| 1 | Sale Felt Christmas Play Food Grazing Box, Set B | DONE | https://mytoywagon.com/products/felt-christmas-play-food-grazing-box-set-b | none |
| 2 | Sale Felt Christmas Play Food Grazing Box, Set A | DONE | https://mytoywagon.com/products/felt-christmas-play-food-grazing-box-set-a | none |
| 3 | Colorful Rainbow Hedgehog | DONE | https://mytoywagon.com/products/felt-colorful-rainbow-hedgehog | none |
| 4 | Bauspiel Tooth Fairy Box | DONE | https://mytoywagon.com/products/bauspiel-tooth-fairy-box | non-Tara vendor; origin_made Germany + EN71 from explicit description; origin_designed omitted |
| 5 | Large Felt Farm Mat | DONE | https://mytoywagon.com/products/large-felt-farm-mat | none |
| 6 | The Gruffalo Playscape Play Mat | DONE | https://mytoywagon.com/products/the-gruffalo-playscape-play-mat | none |
| 7 | Felt Safari Animal Toys, Set of 6 | DONE | https://mytoywagon.com/products/felt-safari-animal-toys-set-of-6 | none |
| 8 | Papoose Forest Caves Play Mat | DONE | https://mytoywagon.com/products/papoose-forest-caves-play-mat | none |
| 9 | Papoose Rockpool Tray | DONE | https://mytoywagon.com/products/papoose-rockpool-tray | origin/cert omitted (not grounded) |
| 10 | Felt Rainbow Fairy Home and Mat | DONE | https://mytoywagon.com/products/felt-rainbow-fairy-home-and-mat | origin_designed omitted (not grounded) |
| 11 | Felt Ice Cream Set, Waffle Cones and 9 Scoops | DONE | https://mytoywagon.com/products/felt-ice-cream-set-waffle-cones-and-9-ice-cream-scoops | none |
| 12 | Felt Fruits and Vegetables, Set C, 15 pcs | DONE | https://mytoywagon.com/products/felt-fruits-and-vegetables-set-c-15-pcs | none |
| 13 | Felt Fruits and Vegetables, Set B, 11 pcs | DONE | https://mytoywagon.com/products/felt-fruits-and-vegetables-set-b-11-pcs | none |
| 14 | Felt Fruits and Vegetables, Set A, 14 pcs | DONE | https://mytoywagon.com/products/felt-fruits-and-vegetables-set-a-14-pcs | none |
| 15 | Felt Fruits and Vegetables, Set D, 12 pcs | DONE | https://mytoywagon.com/products/felt-fruits-and-vegetables-set-d-12-pcs | none |
| 16 | Felt Pasta Play Food Set | DONE | https://mytoywagon.com/products/felt-pasta-play-food-set | none |
| 17 | Fairyshadow Strawberry Baby Necklace, Red | DONE | https://mytoywagon.com/products/fairyshadow-strawberry-baby-necklace-red | non-developmental gift item |
| 18 | Fairyshadow Love Bug in Leaf Necklace | DONE | https://mytoywagon.com/products/fairyshadow-love-bug-in-leaf-necklace-assorted-colors | non-developmental gift item |
| 19 | Lilac Fairy Blossom House | DONE | https://mytoywagon.com/products/lilac-fairy-blossom-house | none |
| 20 | Papoose Fairy Door | DONE | https://mytoywagon.com/products/papoose-fairy-door | none |
| 21 | Toverlux Magic Wooden Lamp | DONE | https://mytoywagon.com/products/toverlux-magic-wooden-lamp | non-developmental gift item, MISSING-AGE (age omitted, not guessed) |
| 22 | The Gruffalo Finger Puppets Set | DONE | https://mytoywagon.com/products/the-gruffalo-finger-puppets-set | none |
| 23 | The Room On The Broom Finger Puppets Set | DONE | https://mytoywagon.com/products/the-room-on-the-broom®-finger-puppets-set | none |
| 24 | Ingenious Insects Finger Puppets and Book Set | DONE | https://mytoywagon.com/products/ingenious-insects-finger-puppets-and-book-set-by-sarah-allen | none |
| 25 | Five Little Ducks, Finger Puppet Set of 6 | DONE | https://mytoywagon.com/products/five-little-ducks-finger-puppet-set-of-6 | none |
| 26 | Itsy Bitsy Spider, Finger Puppet Set of 3 | DONE | https://mytoywagon.com/products/itsy-bitsy-spider-finger-puppet-set-of-3 | none |
| 27 | Sabo Concept Nutcracker Play Theater and Magnetic Figurine Set | DONE | https://mytoywagon.com/products/sabo-concept-the-nutcracker-play-theater | non-Tara vendor; origin_made Ukraine grounded; origin_designed and certifications omitted |

## Holds for human follow-up

| Product | Reason | Note |
|---------|--------|------|
| Wild Mountain Child Leaf Cup | PREORDER-HOLD | Pre-order tag and ship-date paragraph; mine ETA then enrich |
| Tender Leaf Stacking Forest | COLLECTIVE-HOLD | Shopify Collective item; needs Collective-aware copy |
| Puff Kids World Map | PREMIUM-HOLD | $259, at/over the $250 floor; awaits "approve premium" |

## Spot-check recommendations before scaling

- Compare 3 against the Felt Farm canary: a felt-food item (Felt Ice
  Cream Set), a non-Tara vendor (Bauspiel Tooth Fairy Box, Sabo
  Nutcracker), and a non-developmental gift (Fairyshadow necklace).
- Confirm origin/cert omissions read cleanly when a field is absent
  (Papoose Rockpool Tray, Felt Rainbow Fairy Home, Sabo).
- Confirm the "non-developmental gift item" flag products
  (Fairyshadow x2, Toverlux) position as gift/decor, not as
  developmental toys.
- After sign-off: clear the 3 holds (mine pre-order ETA; Collective
  copy; approve premium) and ramp the next cohort increment.
