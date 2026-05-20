# Collection Audit — 2026-05-20

> 339 collections total. NOTHING has been deleted. This lists cleanup candidates
> by tier. Per the owner's rule, anything linked on the site (nav, footer, theme,
> apps, or with SEO equity) must be flagged and confirmed before deletion. Link
> and app status must be verified per item before removing any collection.

## Known linked collections (do not delete)
From the live menus and footer section: `new-arrivals`, `pre-order`, `sale`,
`all-products` (via /collections/all). The mega-menu design also references some
collections that do not exist yet (Handmade Toys, Montessori Inspired, STEM Toys,
The Playroom Collection, Made in the USA, Spring Nature Table), so that menu is
partly aspirational.

## Tier 1 — Empty (0 products). Safe to delete after a link check.
5-to-8-years-1, cocoletes, drewart-pre-orders, estella, ewas-gnomes,
fairies-and-gnomes-1, for-grandparents, gemmed-blocks, growth-chart, gry-and-sif,
labor-day, last-minute-gifts, lily-and-river, nanchen, new-markdowns,
oshkin-wooden-craft-pre-order-collection, oyoy, seasonal-sale, shop-by-age (the
collection, not the /pages/shop-by-age page), tara-treasures-pre-orders,
three-hearts-modern-teething-accessories, timber-play, wooden-story,
wooderful-life, yaya-eco-design. (~25)

## Tier 2 — Duplicates. Merge contents, then delete the redundant one.
- `fathers-factory-1` (31) into `fathers-factory` (54)
- `love-note-co-1` (8) into `love-note-co` (8)
- `nanchen` (0) is a dead duplicate of `nanchen-natur` (98)
- `fairies-and-gnomes-1` (0) and `gnomes-fairies-princes-peg-dolls` (865) overlap
  `fairies-and-gnomes` (862); consolidate to one
- `dress-up-and-costumes` (1) into `costumes-and-dress-up` (45)
- `waytoplay` (3) and `way-to-play` (3) are the same brand
- `spring-collection-1` (196) into `spring-collection` (1815)
- `magnetic-play` (18) into `magnetic-tiles` (37)
- `wooden-art-easels` (2) and `easel` (2) are the same thing

## Tier 3 — Internal alphabet-split artifacts. Not customer-facing; delete after link check.
`a-to-b` (1308), `c-to-g` (377), `d-to-g` (24), `h-to-k` (365), `h-to-o` (523),
`l-to-o` (139), `p-to-q` (166), `p-to-s` (264), `s-to-t` (721), `t-to-u` (41),
`v-to-z` (148). These look like migration or export buckets, not shop categories.

## Tier 4 — Giant auto-collections. DO NOT delete without checking app dependencies.
These likely belong to discount, loyalty, or product-feed apps and deleting them
could break those apps:
- `promotional-collection` (7991), `end-of-summer` (7984), `rewards` (6330),
  `discount-collection` / "Welcome Collection" (6125), `holidays` (6236),
  `holidays-1` (6551).
- `no-discounts` (2001) is functional (excludes items from discounts); keep.

## Tier 5 — Age collections. Broken and overlapping; rationalize, do not just delete.
Single-year and band collections coexist and the counts are clearly wrong
(e.g. `3-years` shows 5,947 of 8,138 products). Rebuild to the five-band model:
First year, Toddler, Preschool, Early school, School age. Affected: `0-12-months`,
`6-months`, `1-year`, `18-months`, `2-years`, `3-years`, `4-years`, `5-years`,
`4-6-years`, `5-to-8-years-1`, `8-years`, `age-1-3-years`, `age-3-5-years`,
`age-5-8-years`.

## Tier 6 — Seasonal overlaps. Consolidate.
`autumn-collection` (943) / `fall` (483); `spring-collection` / `spring-collection-1`;
`summer-collection` (1132); `winter-collection` (1613) / `winter` (1);
holiday cluster `the-holiday-shop` (1588) / `holidays` (6236) / `holidays-1` (6551) /
`holiday-collection` (93) / `christmas-magic` (58); `easter-collection` (271) /
`easter-toys-for-kids` (1269); `halloween` (225); `valentines-collection` (378);
`stocking-stuffers` (958); `seasonal-sale` (0).

## Keep
- Brand collections (these power Featured Brands).
- Category collections that map to the taxonomy (arts-crafts, build-and-construct,
  kitchen-play, play-food, puzzles, wooden-animals, wooden-transportation-toys,
  sensory-discovery, etc.).
- The whimsical browse collections (e.g. Trees and More Trees) can stay as
  landing pages even after products get clean product_types underneath.

## Recommended order
1. Tier 1 empties (lowest risk).
2. Tier 2 duplicates (merge then remove).
3. Tier 3 alphabet artifacts.
4. Then tackle Tier 5 age rebuild and Tier 6 seasonal consolidation as projects.
5. Tier 4 only after confirming no app or feed depends on each.
