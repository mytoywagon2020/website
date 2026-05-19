# Fast PDP Rollout: Pilot Batch Tracking

Status: **PILOT RUNNING** (5 parallel enrichment agents). This file is
filled with live URLs and per-product status the moment the agents report
back. Until then the Results table reads "pending".

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

## Results (pending — fills on agent completion)

| # | Product | Price | Status | Live URL | Flags |
|---|---------|-------|--------|----------|-------|
| _pending_ | | | | | |

## Holds for human follow-up (pending)

| Product | Reason | Note |
|---------|--------|------|
| _pending_ | | |
