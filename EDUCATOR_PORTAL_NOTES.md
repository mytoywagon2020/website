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
6. **IMAGES + SPECS across the board (owner rule 2026-05-29):** EVERY educator listing must carry the real product **images** AND **specs** pulled from its source/retail listing. Splits via productDuplicate get these automatically; products created blank or SKU-assigned-in-place need images+specs pulled manually. Audit by per-product `featuredMedia` (NOT media_count — that filter is broken).

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

## 8. Section-by-section completion ledger

**Section 1 — Sensory Play (audited 2026-05-29):** 23 page items ↔ 23 dedicated educator products — COMPLETE match, nothing missing to create. All 23 PRICED. Walled (no leaks). IMAGES: pulled retail images for MBALL (Mindful&Co) + PRT (Papoose Rockpool). REMAINING 3 missing images = Wooden Story sand trays w/ NO retail twin → **OWNER must supply photos**: Sand Tray w/ Accessories (MTW-SP-SAND), Sand Tray w/ Flashcard Holder (MTW-SP-2PART), Sand Tray Tools Set of 4 (MTW-SP-TOOLS). Otherwise Section 1 COMPLETE. (Page also pulls 8 aromatherapy doughs MTW-CA-AN* + forest-floor tray MTW-NP-TLF — all priced + present.)
**Section 2 — Nature Play (PRICED 2026-05-29):** 19 page SKUs; 20 products. NO listings missing. 16/20 PRICED from retail twins (Acorns $24, Autumn Leaves $14, Pinecones $12, Pumpkins $16.50, Forest Mushrooms $28, Teak Spoon Set $28, Teak Slotted Spoon $22, Busy Bee Tray $165, Turkey Pair $42, Woodland Leaves $52, Forest Mushrooms Basket $62, Bird Eggs $65, Nesting Bowls $20, Tongs $9, Coconut Sieve $12, Forest Floor Tinker Tray $78). STILL $0: Bumbu Pumpkin Harvest (HRV, combined Bumbu trio+patch — owner/compute), + 3 bundles owner-handled (Autumn Set AUT, Nature Tools Set NTS, Everything Play Bundle WMC-EPB). Images: left per owner instruction.
**Section 3 — Woodland (audited 2026-05-29):** 14 page SKUs ↔ 14 dedicated products, EXACT match. NO listings missing. ALL 14 PRICED already (incl. both bundles: Woodland Family Set $398, Woodland Tree Set $310). COMPLETE (images left per owner).
**Section 4 — Small World (audited 2026-05-29):** 22 page SKUs ↔ 22 dedicated products, EXACT match. NO listings missing. ALL 22 PRICED (play mats $58-168, puppet sets $48-78, 3 bundles: Complete Felt Habitats $360, Natural World Set $278, Songs & Stories Set $268). COMPLETE (images left per owner).
**Section 5 — Fairy Villages (audited 2026-05-29):** 9 page buttons all map to dedicated priced products (homes + gnomes + Build the Village). COMPLETE for wired buttons. (MTW-FV-LFS was a false grep hit — text mention in bundle desc, not a real button.) 4 extra educator-tagged products exist but NOT on page: Bumbu Flower Children (walled, clean, no SKU — safe to add once SKU'd) + 3 SHARED RETAIL listings still on Online Store needing split: Papoose Fairy Door (W/P166, $26, prod 8159792267434), Papoose Wishing Well (W/P105, $20, 8159808290986), Mushroom House w/ Carrot Mat (blank SKU, $55, 7611596570794). Owner said "add them" — but 3 are retail; defer to shared-listing split.

**Section 6 — STEAM (catalog = source of truth, pgs 34-44; audited 2026-05-29):**
- DECISION (owner): KEEP the full Connetix line (all 37 existing MTW-CX/ST products) — selling entire line even though catalog lists only curated picks. OK to split Bauspiel from retail + create science/life-cycle items in batches of <=10.
- Catalog STEAM has NO prices anywhere. Price Bauspiel from retail twins; new science/life-cycle items will be $0 until owner prices (like bundles).
- Page lists 42 SKUs; only 6 have products (CMP, CBR, CCP, CGP, QTM, KAL). KAL=$0 needs price.
- CATALOG STEAM GROUPS (43 SKUs): Kaleidoscopes AMB/FOR/BLU + KAL(trio set); Connetix singles CMP/CCP/CGP/CBR/CRR + specialty CPR/CGC/CGU/CLS/CBP + bundle sets CCS/CCM/CCF/SCT + CRM(overview, not sellable); Bauspiel BCT45/BCU(Lucent100)/BFW/BMB/BTW + BSOB(Optical); Q Toys QTM/QTBINO; observation HBMS/HBLM/COMP/JDSB + OBS(set); June&December JDB-S1/S2; Papoose life cycles BLC/BEE/FRG/BEN/ANA + CBS(set) + PDM(Jurassic set); Bumbu BPS/BDE; Tara TLC.
- B1 DONE (2026-05-29): Bauspiel split — created 5 DRAFT educator copies + untagged retail originals. NEW educator products (OWNER must wall: Active + channels off in admin):
  - MTW-ST-BCT45 Color Track 45 $290 — prod 8447063589034 / variant 48355998531754
  - MTW-ST-BFW Fairytale Windows 12 $139 — prod 8447063621802 / variant 48355998564522
  - MTW-ST-BLC Lucent Cubes 100 $225 — prod 8447063687338 / variant 48356002136234
  - MTW-ST-BMB Mirror Blocks 12 $97 — prod 8447063720106 / variant 48356002169002
  - MTW-ST-BTW Transparent Windows 25 $152 — prod 8447063752874 / variant 48356002201770
  Retail originals untagged (retail-only now): 6746569212074, 6751337414826, 6763702517930, 6887026393258.
  MTW-ST-BSOB Optical Blocks 12 $179 — DONE: split from retail twin 8297775792298 → educator prod 8447064637610 / variant 48356069048490 (DRAFT, owner wall). Retail original was NOT educator-tagged, no cleanup needed.
- B2 DONE (2026-05-29): Science tools — all DRAFT, OWNER must wall. Split from retail twins (twins NOT educator-tagged, no cleanup): MTW-ST-JDSB Specimen Collecting Kit $26 (prod 8447065456810/var 48356111319210, twin June&December 7705331794090); MTW-ST-HBLM My Little Museum Bug Box $18 (8447065915562/48356136878250, twin Huckleberry 7620700274858); MTW-ST-COMP Wooden Compass $16 (8447065948330/48356136911018, twin Huckleberry 7716802822314). Created NEW ($0, owner price): MTW-ST-QTBINO Wooden Binoculars Q Toys (8447066276010/48356157030570); MTW-ST-HBMS Magnifier Set of 2 = BUNDLE of Huckleberry Dual Magnifier $17 + Wooden Magnifying Glass $20 (8447066308778/48356157063338).
- B2 FIX: MTW-ST-QTBINO Wooden Binoculars — was created blank, but retail twin EXISTS (Q Toys Wooden Binoculars, prod 7915296751786, SKU 425, $44, DRAFT, not educator-tagged). Updated educator copy to $44 + pulled image. Clean (twin not educator-tagged).
- B3 DONE (2026-05-29): Life cycles + anatomy. KEY: Butterfly/Frog/Dino/Anatomy ALREADY EXISTED as Tara Treasures educator-steam DRAFTs (off retail, off edu catalog) — just assigned SKU + price + CONTINUE (NO split needed, not on retail). OWNER must wall:
  - MTW-ST-LCB Felt Lifecycle Monarch Butterfly $32 (prod 7437808697514/var 43151518040234)
  - MTW-ST-LCF Felt Lifecycle Toy Frog $39.50 (7690046668970/44405657862314) [we DO have a frog]
  - MTW-ST-TLC Dinosaur Life Cycle $42 (7708337537194/44537077825706)
  - MTW-ST-ANA Felt Anatomy Set $54 (7787483725994/44891631059114)
  B3 CLOSED: MTW-ST-BEE Honey Bee split from retail twin 7437680476330 ($26) → educator 8447070994602/48356354818218, retail original untagged. MTW-ST-BEN created NEW "Felt Lifecycle of a Bean Plant" $0 (8447070929066/48356353605802) from specs — OWNER adds image + price.
  (was) STILL OPEN in B3:
  - MTW-ST-BEE Bee Life Cycle = Felt Lifecycle of a Honey Bee (Tara, prod 7437680476330, $26) is a LIVE RETAIL listing (onOnline true, not educator-tagged) -> needs SPLIT, not direct tag.
  - MTW-ST-BEN "Bean Life Cycle" — does NOT exist. We have Chicken/Sea Turtle/Redback Spider/Honey Bee life cycles instead. OWNER decision: create a felt bean life cycle, or substitute?
- BUILD PLAN (batches <=10): B1 Bauspiel split (BCT/BFW/BLC/BMB/BTW have retail twins; BOB/Optical no twin). B2 science tools (microscope exists; create binoculars/magnifier/bug box/compass/specimen kit/optical). B3 Papoose life cycles + anatomy. B4 dinosaurs/deep time (BPS/BDE/TLC/PDM). B5 Connetix specialty + bundle sets + kaleidoscope variants. Then wire page (it currently has 0 buttons — needs PDP map + buttons added).

Sections 7-8: Dramatic Play (partly done, ~28 cafe/bakery SKUs missing) + Creative Arts (unwired, ~21 missing) — not yet fully audited.

CAVEAT: `media_count:0` search filter is BROKEN here (false positives). Audit images via per-product `featuredMedia{id}` instead.

---

### FULL image+spec audit — 145 products, deduped, zero sampling (2026-05-29)
- SPECS: 100% — all 145 have substantial descriptions, 0 thin/placeholder.
- IMAGES: 123/145 have images. 22 WITHOUT images = exactly the no-retail-twin / owner-buildout items: CA maker items (JHP/ECBF/FFRN/FPET/FLVS/FBLO/FSTM/THB/EMB/TLM/FLC/THC), DP $0 bundles (PWF/TLS/FYS/SH), owner-supplied (SP-SAND/2PART/TOOLS sand trays, NP-MSH forest mushrooms), no-twin (WD-PST Papoose Seasonal Trees, ST-BEN Bean Plant). Nothing pullable-from-twin is missing.
- DP page WIRED: 27 buy buttons (PDP map extended to 30 SKUs). 12 cards still button-less pending owner-created products.

### Image+spec completeness audit (2026-05-29)
- Split-created products (Bauspiel, World Foods, Chocolate Cake, fairy homes, etc.): VERIFIED have real retail image + full retail spec description.
- FIXED: Wooden Binoculars (MTW-ST-QTBINO) now full Q Toys spec + 4 imgs; Magnifier Set (MTW-ST-HBMS) now both component imgs + combined spec.
- STILL skeletal (no retail twin): Bean Plant Life Cycle (MTW-ST-BEN) — short agent-written desc, NO image. Owner buildout (or use sibling life-cycle hero).

## DRAMATIC PLAY — creating 34 missing page products (owner approved "create all 34", 2026-05-29)
- DP1 DONE: 8 World Foods split from Papoose twins (DRAFT, owner wall): MTW-DP-BNS Beef Noodle Soup $42 (8447076925610), MTW-DP-MEM Middle Eastern Mezze $82 (8447076958378), MTW-DP-MSR Mixed Sushi Rolls $56 (8447076991146), MTW-DP-SBB Sushi Bento Box $36 (8447077023914), MTW-DP-ERH Egg Rolls&Hand Rolls $46 (8447077056682), MTW-DP-YUM Yum Cha Dim Sum $114 (8447077089450), MTW-DP-PSF Peruvian Street Food $94 (8447077122218), MTW-DP-EFE Ethiopian Feast $108 (8447077154986). Twins not educator-tagged, no cleanup.
- DP2 DONE: 3 bakery split from clean twins (DRAFT): MTW-DP-DON Felt Donuts Set of 4 $30 (8447077187754), MTW-DP-TPV Pavlova $10 (8447077220522), MTW-DP-HOT Hot Drinks Set 16pc $50 (8447077253290).
- DP3 PENDING — AMBIGUOUS twins (multiple candidates, need catalog spec to pick exact product/price; DON'T guess): COO Cookies·4 Styles (sugar $35 / choc-chip $46 / gingerbread $8?), CUP Cupcakes·5 Flavors (only Halloween cupcakes $30 found), MLK Milkshakes (choc $15 / mango $26), ICE Ice Cream&Holder (Ice Cream Set $70 + Cone Holder $33 — combine?), LOL Lollipops (peppermint lollies $3?), SCN Scones&Preserves (no twin found), CHC Chocolate Cake on Stand (no twin found). Owner: confirm exact catalog products/prices.
- DP3 DONE (CORRECTED — real IDs, verified 29 total products): MTW-DP-LOL Lollipops $3 (prod 8447077875882), MTW-DP-SCN Scones & Preserves $32 (8447077908650), MTW-DP-PAS Pasta $34 (8447077941418), MTW-DP-CCP Charcuterie & Cheese Platter $34 (8447077974186). NOTE: a buggy earlier attempt created/left some stray duplicate Scones/Pasta/Charcuterie/Lollipop drafts with guessed IDs that failed config — CHECK for and clean up orphan untagged duplicate drafts (Scones/Pasta/Lollipops/Charcuterie) if any exist.
- DP VERIFIED 29 products in tag:educator-dramatic-play (2026-05-29).
- DP4: MTW-DP-CHC Chocolate Cake on a Stand $95 (Sabo Concept twin 8306857476266) → educator 8447323373738/48357830164650, DRAFT. DP now 30.
- DP CREATION DONE (agent side): owner says all REMAINING DP page SKUs are bundles or unique listings the OWNER will create (cookies/cupcakes/milkshakes/ice cream/food groups/pantry+farm bundles/Jollof/Fika/etc.). 30 products created by agent. Remaining = owner buildout. Also owner pricing the 4 $0 (PWF/TLS/FYS/SH). Then page wiring (add data-sku buttons for newly-created SKUs + extend PDP map). — AMBIGUOUS twins, owner to confirm exact Tara product/price: COO Cookies·4 Styles, CUP Cupcakes·5 Flavors, MLK Milkshakes, CHC Chocolate Cake on Stand, BND Bundt Cake Slices·2 Sets, ICE Ice Cream&Holder (combine Ice Cream Set $70 + Cone Holder $33?), MSR done, TFG Food Groups Nutrition Set, BPB Bread&Pantry Bundle, BPG Wooden Pumpkins&Gourds (Bumbu), BSB Bumbu Straw Bale, GMT Grapat Mandala Tulips, WAJ West African Jollof (no twin), SWF Swedish Fika (no twin), WK/WEA/PNT/BAK/TRT/SBB-done bundles. Plus existing $0: PWF/TLS/FYS/SH.
- (PRIOR REMAINING list, superseded): World Foods no-twin (WAJ West African Jollof, SWF Swedish Fika) → new $0. Bakery/sweet shop (BND/CHC/COO/CUP/DON/LOL/MLK/PAS/SCN/TPV/ICE/HOT/BAK/TRT bundles). Pantry/farm extras (BPB/BPG/BSB/GMT/SBB done/PNT/TFG/WK/WEA bundles + WAJ). + existing $0: PWF/TLS/FYS/SH. Continue batches of 10.

## IMAGE BACKFILL PROGRESS (from retail twins; per owner rule #6)
- Audit: ~90 of 117 dedicated educator products had NO image (all the ones built from scratch by the original process; split-created ones already have images). media_count filter is broken — use per-product featuredMedia.
- NO SUBAGENTS (owner instruction 2026-05-29) — do image backfill directly.
- **Woodland (§3) DONE 13/14:** added hero images from Bumbu/retail twins (Deer, Raccoon via earlier; Bear, Fox, Hedgehog, Oak, Birch, Fir, Willow, Acacia, Squirrel, + 2 bundles Woodland Family Set=deer hero, Woodland Tree Set=oak hero). **OPEN: Papoose Seasonal Trees Set (MTW-WD-PST 8444883730602) — no confident retail twin found, owner to image.** Squirrel used single "running squirrel" image (no family twin exists).
- **Small World (§4) DONE 21/22:** hero images from twins — play mats (Forest Caves=Papoose, Fairy Streamlet/Coralwhim=Gus&Mabel, Garden of Moon/Hobbit Hollow=Himalayan Felt, Featherfloat=Papoose pond) + puppet sets (Tara finger-puppet twins: Insect/Bugs, Ocean, Polar, Butterflies, Aus Birds, Old MacDonald, Speckled Frogs, Itsy Bitsy, Monkeys, Ducks, Gruffalo's Child) + 3 bundles + Tiny Tale Terrains (placeholder hero=fairy streamlet, replace later). Wispy Waters Way DONE (twin Gus&Mabel 8390714654890). Tiny Tale Terrains DONE (real twin Gus&Mabel "Tiny Terrains Mat Set of 4" 8430401913002 — placeholder removed, 6 real images + spec desc copied). **§4 Small World 22/22 COMPLETE, no placeholders.**
- **Nature Play (§2) DONE 15/20:** imaged from twins — Forest Floor Tinker Tray (had), Woodland Leaves/Forest Mushrooms Basket/Bird Eggs (Moon Picnic), Turkey Pair (Bumbu), Tongs/Teak Spoon Set/Slotted Spoon/Nesting Bowls/Coconut Sieve (Papoose), Busy Bee Tray (Gus&Mabel), + felt loose-parts from Tara twins: Acorns (orange 7566756380842 + green 7566759493802, both imgs), Autumn Leaves (7933068181674), Pinecones (8022493266090), Pumpkins (7787490279594). Bundles hero-imaged (owner OK): Autumn Set=acorns, Bumbu Pumpkin Harvest=Bumbu Pumpkin Set, Nature Tools Set=teak spoons, Everything Play Bundle=Wild Mountain dish. **§2 now 19/20. OPEN (1): Felt Forest Mushrooms Red&Brown (MTW-NP-MSH 8444898967722 — curated 5 red+5 brown, NO single twin; owner to image).**
- **Fairy/Kaleidoscope DONE 5/5:** Pastel Gnomes (Wonderheart PastelGnomes9), Bright Gnomes (Wonderheart Rainbow Gnome Set), Kaleidoscope Trio (Huckleberry Kaleidoscope hero), Mushroom Garden Fairy Home + Build the Village (both used Mushroom House w/ Carrot Garden Mat image — IMPERFECT heroes: MGF is a larger different home, Build the Village is a multi-home bundle; owner may want better photos). (The 5 fairy homes + Butterfly already had images from their splits.)
- **Creative Arts (§8) PARTIAL:** 9 already had images (7 aromatherapy doughs + Seven Scents bundle had image too; actually doughs ANO/ANE/ANL/ANV/ANR/ANM/ANP + ANS imaged). This round added 2: Weaving Station (Q Toys twin 7547994734762), Lacing Beads (Plan Toys twin 8102490505386). **OPEN ~11 — NO clean retail twin found in store (owner to image):** Heirloom Flower Press (MTW-CA-JHP; candidates exist: Sow'n'Sow/Goki/Tender Leaf presses — owner pick), Eco-Cutters Set (MTW-CA-ECBF), Felt Ferns/Petals/Leaves/Blossoms/Stems — STRUCTURED 2026-05-29: set vendor=Global Goods Partners, SKUs MTW-CA-FFRN(ferns 8444921053354)/FPET(petals 8444921086122)/FLVS(leaves 8444921118890)/FBLO(blossoms 8444921151658)/FSTM(stems 8444921184426), untracked+CONTINUE. Retail twins NOT listed in store yet → OWNER building out images/price/specs.), Threading Boards, Felt Embroidery Kit, Table Loom (Q Toys — no separate twin found), + bundles Felt Florals Collection (MTW-CA-FLC) & Threading Companions (MTW-CA-THC, hero=weaving station). NOTE: many Creative Arts also still $0 unpriced + no SKU.
- Creative Arts STRUCTURED 2026-05-29: assigned missing SKUs Threading Boards=MTW-CA-THB, Embroidery Kit=MTW-CA-EMB, Table Loom=MTW-CA-TLM; fixed Felt Florals Collection vendor→Global Goods Partners; continue-selling+untracked on all. ALL Creative Arts now have SKU+vendor+CONTINUE. Owner still building out: images (felt florals, eco-cutters, presses, looms, embroidery — retail twins not listed yet) + prices (most CA still $0).
- STILL TO BACKFILL: Dramatic Play bundles (PWF/TLS/FYS/SH), STEAM Magnifier/Bean/Forest Mushrooms images. Specs (descriptions) still generic on many. Creative Arts pricing outstanding (owner buildout).

## 9. Section order (from page.educators.liquid hub)
1 Sensory · 2 Nature Play · 3 Woodland · 4 Small World · 5 Fairy Villages · 6 STEAM · 7 Dramatic Play · 8 Creative Arts

---

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

---

## 10. Wagon / Checkout architecture — DECIDED 2026-05-29

**CONTEXT / THE BUG:** Educator products are WALLED (off Online Store). Shopify's native cart
(`/cart/add.js`) and checkout permalinks ONLY work for Online-Store-published variants — so the
native cart CANNOT be used for walled products. Verified: MTW-FV-MGF variant 48345499205802 has
`onlineStoreUrl=null`, `availableForSale=true` (CONTINUE), published only to "Microsoft Copilot".
`/cart/add.js` silently fails → wagon stays at 0 / shows empty (the bug owner reported).

**OWNER DECISIONS:**
- Keep products FULLY WALLED. Do NOT publish to Online Store. (`/products.json`, `/search`,
  `/sitemap.xml`, `/collections/all` must stay empty — confirmed via gate test that price/spec
  data (`MTW_FV_SPECS`) is INSIDE the server-side `{% if is_approved %}` block, so non-approved
  visitors never receive catalog HTML/prices. Server-side Liquid gate = real protection.)
- Rejected "publish to Online Store + page gate" because `/products.json` would leak prices.
- Rejected separate/multi-store (2nd subscription + permanent duplication overhead).
- Plan is "Shopify" (NOT Plus, `shopifyPlus:false`) → native B2B (company catalogs, price lists,
  self-serve Net-30 at checkout) NOT available. `customer.b2b?` is always false → the
  `educator-approved` TAG is the real gate (b2b? branch is dead weight on this plan).

**CHOSEN APPROACH: instant app-proxy DRAFT ORDER flow ("slow goods" pace is fine per owner).**
1. Client-side wagon: "Add to wagon" stores items in `localStorage` (sku, variantId, title,
   price, qty, img). Nav count + wagon page read localStorage. Across all 8 section pages.
2. "Pay now" POSTs the cart to a Shopify APP PROXY (`mytoywagon.com/apps/wagon/checkout`) →
   backend (Cloudflare Worker, free tier) VERIFIES Shopify signature → Admin GraphQL
   `draftOrderCreate` (line items by variantId — works for walled products, Admin API not gated
   by sales channel) → returns `invoiceUrl` → browser redirects to NATIVE Shopify checkout
   (Shop Pay/Apple/Google/card + PO). Draft-order origin is invisible to buyer.

**BOTH PATHS THROUGH THE DRAFT ORDER (owner rec accepted):**
- Card: instant — redirect to invoice checkout.
- PO/Net-30: SAME draft order, flagged (tag `po-request` + note); OWNER applies payment terms in
  admin (self-serve Net-30 at checkout needs B2B/Plus).

**QUOTE BUILDER vs DRAFT:** Draft order is the SPINE for standard catalog orders (itemized,
tax-exempt, becomes a real order, has pay link). Keep `page.new-quote.liquid` + the in-page
"tell us about your classroom" form ONLY as the custom/consultation intake (custom mixes,
district planning, formal pre-commit quote doc). Do NOT route standard orders through it.

**BUILD INTO WORKER (conversion + correctness):**
- Pass `logged_in_customer_id` (proxy appends it, signed) → attach customer to draft order
  (pre-fills checkout) + read customer tags.
- `taxExempt:true` on the draft order ONLY for tax-exempt-tagged educators.
- Show running total on wagon page before redirect.

**PROVISIONING (OWNER — touches account/billing; agent owns the code):**
1. Custom app (Settings→Apps→Develop apps): scopes `write_draft_orders`, `read_products`,
   `read_customers` → Admin API token.
2. App Proxy on that app: prefix `apps`, subpath `wagon` → Worker URL.
3. Deploy Cloudflare Worker (free tier); set `ADMIN_TOKEN` + `APP_SECRET` (app shared secret) as
   Worker secrets.

**RUNBOOK / MAINTENANCE:**
- The Worker is now part of the stack: needs uptime + occasional Admin TOKEN ROTATION.
- Shopify FLOW to auto-expire abandoned (unpaid) draft orders (owner approved 2026-05-29): each
  Pay click creates a new draft; double-clicks / non-completions leave unpaid drafts. Flow:
  trigger "Draft order created" → wait N days → if still unpaid, delete (or tag for cleanup).
- PREVIEW BYPASS caveat: `theme.role!='main'` / `request.design_mode` shows the catalog on
  PREVIEW links to anyone — staging only, not live. Don't share preview links publicly.

**FOOTER:** Switched from heavy BLACK inline footer to the cream `mtw-educator-footer` section
(deduped the double-footer across all 8 pages). Cream is on-brand & kept. TODO: RE-ADD a compact
terms/payment band (PO · Net-30 · Tax-exempt text badges + monochrome card logos) — it was lost
in the switch but is B2B-conversion-relevant.

### Educator PDP page (gated, walled) — added 2026-05-29
- `templates/page.educator-product.liquid` + Shopify Page handle `educator-product`
  (templateSuffix `educator-product`, Page id 116049641642). URL:
  `/pages/educator-product?sku=MTW-FV-PNK`. It's a PAGE (not a product) → never in
  /products.json. Renders premium PDP (image gallery + thumbnails, value badges,
  accordion sections) from a data island keyed by ?sku=. Gated like the section pages.
- ROADMAP (use metafields / live data): Liquid can't read walled products' metafields
  (off-channel). Plan: add a READ endpoint to the app proxy `/apps/wagon/product?sku=`
  returning title/price/media/metafields from Admin API; page fetches live, same markup,
  still off /products.json. Until then the data island is baked (FV 9 SKUs done; PNK/LIL
  have full accordion bodies, others fall back to short body).

### PRE-MORTEM / launch risks (consultant review 2026-05-29) — MUST address before launch
- **FM1 App JS clash:** storefront-optimization apps (sticky cart, upsell sliders,
  exit-intent) can hijack the custom Add-to-wagon / draft-order flow and force the native
  cart → wall failure. PREVENT: do NOT install storefront apps without dev review; keep
  MTWWagon isolated.
- **FM2 Fulfillment/accounting:** orders are DRAFT ORDERS; ShipStation/QuickBooks/Xero may
  treat drafts as invoices and not import until completed. PREVENT: run a real test order
  end-to-end (pay-link → warehouse software → accounting ledger) before launch.
- **FM3 Metafield/content trap:** the single dynamic PDP relies on complete data per SKU;
  a missing field / bad SKU / wrong-ratio image breaks the layout. PREVENT: strict product
  creation checklist; treat metafields as mandatory; validate before pushing a SKU live.
- **FM4 Abandoned-draft black hole:** Shopify abandoned-checkout automations DON'T see
  draft-order pay links → Klaviyo/Shopify won't recover them. PREVENT (already in runbook):
  Shopify Flow flag drafts pending/invoice-sent >48h for manual follow-up.

### PDP UX gaps (consultant 2026-05-29) — status
- DONE: #4 removed "✓N" from Add button (now clean "Add to wagon"; in-wagon count shown as
  a separate line). #5 stronger "Back to Fairy Villages" (larger, padded, top rule).
  #2 thumbnails + main both 1:1 (consistent). #3 badges are bordered pills (scannable).
- OPEN: #1 PO PDF upload field — needs the app proxy to accept multipart + file storage
  (e.g., upload to a bucket/Files, attach URL to the draft order note/metafield). Best
  placed on the WAGON Path-B (PO) flow, not the PDP. Build with the proxy.
- App blocks (reviews/upsell): most need a native /products/ URL or product on Online
  Store → conflict with walling. Verify per-app (Judge.me/Loox/etc.) before injecting.

### FV "Complete the Village" accessories — created 2026-05-29
- **MTW-FV-FLC Bumbu Flower Children** — prod 8444833726634 / variant 48345339297962. Already
  WALLED (off Online Store), ACTIVE, CONTINUE. Just SKU'd. **PRICE = $78** (the FV page card
  previously said $42 — DISCREPANCY; owner verify which is correct in admin).
- **MTW-FV-FDR Papoose Fairy Door** — split from retail twin 8159792267434. Educator copy prod
  8447608979626 / variant 48359113818282, $26, CONTINUE, **DRAFT → OWNER WALL** (channels off,
  Educator Catalog on, Active). Retail original untagged (retail-only now).
- **MTW-FV-WSH Papoose Wishing Well** — split from retail twin 8159808290986. Educator copy prod
  8447613730986 / variant 48359133511850, $20, CONTINUE, **DRAFT → OWNER WALL**. Retail original
  untagged.
- All 3 wired on FV page ("Complete the Village" cards now have add-to-wagon + content-page
  links) and on the content page (data island + full accordion templates). Content page now
  covers 12 FV SKUs.

**STATUS (2026-05-29):** Front-end client-cart + Worker + setup doc = NOT yet built (next).

## 11. "Complete the section" audit — 2026-05-29 (page cards vs real products)
- **COMPLETE (cards wired, products exist + priced):** Sensory Play (23), Woodland (14),
  Small World (22), Nature Play (19). No action.
- **Dramatic Play:** page shows ~48 SKUs; 27 wired. Products: 10 priced+ACTIVE (live);
  16 DRAFT (World Foods/bakery I created — priced, need OWNER WALLING); 4 $0 ACTIVE
  (PWF/TLS/FYS/SH — need price); ~18 page SKUs have NO product (café/bakery/bundles:
  BAK/BND/BPB/BPG/BSB/COO/CUP/GMT/ICE/MLK/PNT/SWF/TEA/TFG/TRT/WAJ/WEA/WK — owner create).
  My side is done; blocked on owner wall/price/create.
- **STEAM:** page = 0 buy buttons; ~43 page SKUs (curated MTW-ST-* codes). ~50 products exist
  but mostly **Connetix MTW-CX-*** variants (PCR120/PMG202/etc.) whose SKUs DON'T match the
  page codes; ~16 page SKUs DO match products (CMP,CBR,CGP,CCP,KAL($0),QTM,BFW,BLC,BMB,BTW,
  HBLM,JDSB,LCB,LCF,TLC + BCT→BCT45, BOB→BSOB mismatches). NEEDS: SKU reconciliation
  (page↔product), price KAL, decide Connetix display, then add PDP map + buttons. Big job.
- **Creative Arts:** page = 0 buy buttons; ~51 page SKUs. Only ~22 products, ~8 priced
  (7 doughs $15 + Seven Scents $94.50); ~14 are $0; SKU schemes barely overlap (only
  JHP/ECBF/FLC/THC + doughs + ANS match). Heavy OWNER buildout (price + create + reconcile).
- CONCLUSION: the 4 complete sections need nothing. DP/STEAM/CA are blocked on OWNER-side
  product work (walling drafts, pricing $0s, creating missing items, reconciling STEAM/CA SKU
  schemes) — not front-end gaps. Wire each subset as its products become ready/priced.
Already done this session: wagon link added to sticky nav on all 8 pages (live count), double
footer removed on all 8, preview bypass unified on all 8. NOTE: the nav wagon link currently
points to `/pages/educator-wagon`; the wagon page still uses the broken native-cart assumption
and must be rebuilt to the client-side localStorage cart.
