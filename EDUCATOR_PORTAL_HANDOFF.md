# Educator Portal — Session Handoff (2026-05-30)

> Companion to `EDUCATOR_PORTAL_NOTES.md` (the long-term architecture + per-section ledger). **This file** is a tight pickup-from-here doc for the next editor or agent. Read both together.

---

## 1. Where things stand right now

### Shipped (merged to `staging-theme` today)

| PR | Commits | What landed |
|---|---|---|
| **#8** | 1 | Installed `ui-ux-pro-max` design-knowledge skill (project-scoped, `.claude/skills/`) |
| **#9** | 6 | Educator portal a11y polish + Fairy Villages content updates |
| **#10** | 2 | Retail-side mirror of the same a11y polish + perf quick wins (**still draft as of writing**) |

### Educator portal a11y/perf changes now live on staging
- Portal-wide `:focus-visible` 2px ring in `sections/mtw-educator-header.liquid`
- Skip-link to `#main-content` (first Tab press)
- `prefers-reduced-motion` block honoring OS-level setting
- `sections/educator-login.liquid` — `autocomplete=email/current-password/email` on the 3 inputs
- 174 gallery images marked `loading="lazy"` across CA / DP / STEAM / FV / Nature / SW (logos + named cover/hero images stay eager)

### Fairy Villages content cleanup landed in PR #9
1. **Cover paragraph** (line 3519) — brand swap: *"Hand-felted Tara Treasures homes, Wonderheart Little Folk, and Papoose accessories"* → *"Hand-felted woodland and fairy homes, Ambrosius fairies, and Papoose accessories"*
2. **SEO meta description** (line 26) — mirror of above
3. **Artisan paragraph** (lines 3540-3541) — rewritten by owner; *"Tara Treasures house"* → *"woodland home and fairy house"*; *"Fair Trade USA certification"* → *"Fair Trade conditions"*; pluralized *"Kathmandu valley workshops"*
4. **4 Tara Treasures chip/label/eyebrow cleanups** (lines 3605, 3639, 3647, 3652) — brand name dropped from SKU chip, section divider, eyebrow, and Nepal/certification sentence

---

## 2. Brand attribution rules (verified with owner 2026-05-30)

| Brand | Status | Use for | Origin | Certification |
|---|---|---|---|---|
| **The Happy Women Handicraft** | ✅ Correct (newly added) | The felt fairy + woodland homes (FV) | Kathmandu, Nepal (women's cooperative) | "Fair Trade conditions" (no formal cert) |
| **Tara Treasures** | ✅ Correct for: felt leaves/pinecones/acorns/feathers (Nature), Garden of the Moon WAS misattributed → actually Himalayan Felt Co (now corrected), story bundles + science/nature puppets + counting/songs (SW) | Per-product, not the fairy homes | Australia (workshops in Nepal) | **Fair Trade USA Certified** |
| **Wonderheart Little Folk** | ✅ Correct | The gnome SKUs (MTW-FV-RGN, MTW-FV-PGN) | Vermont, USA | n/a |
| **Ambrosius** | ✅ Correct | Fairy figurines (NOT gnomes) | Germany / Bavaria | n/a |
| **Papoose** | ✅ Correct | Accessories: Fairy Door, Wishing Well, Forest Caves Play Mat, nature loose parts | Indonesia / Bali | **WFTO + Fair Trade USA Certified** |
| **Himalayan Felt Co.** | ✅ Correct | Garden of the Moon felt playscape (SW) + narrative landscapes | Nepal | "Fair Trade conditions" (no formal cert) |
| **Bumbu** | ✅ Correct | Flower Children, Mushrooms, Trees | Romania | n/a |
| **Gus + Mabel** | ✅ Correct | Felt habitats (SW), Busy Bee Tray (NP) | n/a | n/a |

### Certification phrasing rules
| Brand | Use this exact phrasing | Don't use |
|---|---|---|
| Papoose | *"WFTO & Fair Trade USA Certified"* | n/a |
| Tara Treasures | *"Fair Trade USA Certified"* | n/a |
| The Happy Women Handicraft (FV felt homes) | *"in Fair Trade conditions"* / *"made in Fair Trade conditions"* | ❌ *"Fair Trade USA Certified"* |
| Himalayan Felt Co. | *"in Fair Trade conditions"* | ❌ *"Fair Trade USA Certified"* |

### Geographic phrasing
- ✅ *"Kathmandu valley workshops"* (plural) — for The Happy Women Handicraft + Himalayan Felt Co. felt work
- ✅ *"hand-stitched from 100% New Zealand and Australian wool"* — Small World materials (SW pull paragraph)
- ✅ *"100% natural sheep's wool"* — Fairy Villages materials (FV artisan paragraph)

---

## 3. Open content questions (owner to resolve)

### Fairy Villages
1. **Awkward line at `templates/page.educator-fairy-villages.liquid:3558`** (still unresolved):
   > *"Every house here is needle-felted by hand in Nepal. **The wool keeps a child's body heat the way a real cottage does.** The petal roofs curl a little differently on every piece. That difference is the work."*

   Owner flagged the bolded sentence as awkward. Rejected 6 candidate rewrites (3 plain, 3 editorial). **Needs owner's own copy.**

2. **Line 4528** — *"Bumbu mushrooms and **Tara Treasures finger puppets** for cross-vendor small-world scenes"*. Tara Treasures does make puppets, so this might be legitimate. Owner to confirm or remove.

3. **Section eyebrow `06. Wonderheart · Little Folk`** (line 3814) and the `Wonderheart` references throughout the gnome section — all confirmed correct, leave alone.

---

## 4. Per-section status ledger (from `EDUCATOR_PORTAL_NOTES.md`)

| Section | Wired? | Priced? | Images? | Owner blocker |
|---|---|---|---|---|
| **Sensory Play** | ✅ 23/23 | ✅ All | ⚠️ 3 missing | Owner photo: sand-tray products (MTW-SP-SAND / 2PART / TOOLS) |
| **Nature Play** | ✅ 19 SKUs | ⚠️ 16/20 | ⚠️ | Bumbu Pumpkin Harvest + 3 bundles owner-handled |
| **Woodland** | ✅ 14/14 | ✅ All | (owner) | None — content complete |
| **Small World** | ✅ 22/22 | ✅ All | (owner) | None — content complete |
| **Fairy Villages** | ✅ | ✅ | ⚠️ | Bauspiel ×4, Fairy Door, Wishing Well, retail Mushroom need sales-channel split |
| **STEAM** | ✅ 30 cards | (owner) | (owner) | Connetix sales-channel decision (must be done in admin, not API) |
| **Dramatic Play** | ✅ 27 + 11 created | ⚠️ 4 at $0 | ⚠️ | Owner creating remaining bundle SKUs + pricing PWF/TLS/FYS/SH |
| **Creative Arts** | ✅ Structured | ⚠️ Most $0 | ⚠️ | Owner pricing + supplying felt-florals / eco-cutters / press / loom / embroidery images |

---

## 5. File map — where to edit content per section

All ecosystem pages follow the same structure. Use these line numbers as landmarks (CA shown — DP/FV/Nature/SW/STEAM/Sensory/Wood follow the same skeleton ±50 lines):

| Section | Line range | What's there |
|---|---|---|
| Head + meta | 1–50 | SEO meta description, OG/Twitter tags |
| Body open + header section include | ~3270 | `{% section 'mtw-educator-header' %}` |
| Custom nav (inline, not shared header) | ~3300–3320 | Page-specific nav with quote builder link |
| **Cover section** | ~3500 | Hero image + H1 + lede/audience copy |
| **Quick facts strip** | ~3525 | Section number, ages, count |
| **Editorial intro (`<section class="intro gut">`)** | ~3545 | Long-form intro paragraph with dropcap |
| Product card grid + bundles | 3600–4200 | Per-product `<article class="home">` blocks |
| Reviews carousel | ~4400 | Pull-quote cards |
| Quick-view modal | ~4480 | `#qv` modal markup |
| JS (cart sync + add-to-wagon) | 4200+ | Don't touch unless intentional |

### Common edit anchors
- **Copy edits** — `<p>` tags inside `<section class="intro gut">` or `<section class="cover">`
- **Product card name** — `<span class="name">` inside `<article class="home">` 
- **Product card description** — `<span class="desc">` (the small editorial blurb)
- **Pricing display** — `<span class="price">` (often "Price on request" if $0)
- **Bundle copy** — under `<h2>` headings like *"Every village needs its people"*

---

## 6. Patterns established (apply consistently across sections)

1. **Brand attribution in chip labels** — if the brand attribution is wrong, drop the brand from the chip rather than substitute. Pattern: `<span class="label">SKU &middot; BrandName</span>` → `<span class="label">SKU</span>`.

2. **Brand attribution in eyebrows** — same. `<span class="eyebrow">05. BrandName · Felt Homes</span>` → `<span class="eyebrow">05. Felt Homes</span>`.

3. **Origin claims in paragraph copy** — when removing a brand, also verify the origin claim still holds. Many brands tie to specific countries/certifications.

4. **Wonderheart references stay** — multiple places: section eyebrow, product card names, "pairs with" lines, alt text, JSON catalog. All correct. Don't touch.

5. **Tara Treasures finger puppets cross-references** — flag for owner before changing. Tara Treasures genuinely makes puppets; the cross-reference may be intentional.

---

## 7. Quick reference: live preview

Theme `staging-theme` branch → Shopify theme ID `146144002218` (auto-deploys on push to staging-theme).

**Preview URL pattern:**
`https://mytoywagon.com/pages/educator-<section>?preview_theme_id=146144002218`

**The 8 ecosystem pages:**
- `/pages/educator-creative-arts`
- `/pages/educator-dramatic-play`
- `/pages/educator-fairy-villages`
- `/pages/educator-nature-play`
- `/pages/educator-sensory-play`
- `/pages/educator-small-world`
- `/pages/educator-steam`
- `/pages/educator-woodland`

**Hub pages:**
- `/pages/educators` (catalog landing)
- `/pages/educator-dashboard`
- `/pages/educator-portal` (gated)
- `/pages/educator-product?sku=<SKU>` (PDP)
- `/pages/educator-wagon` (cart)
- `/account/login` (uses `sections/educator-login.liquid` when on educator pages)

---

## 8. Deferred / lower-priority follow-ups (audit findings)

From the educator audit (PR #9) — NOT yet shipped:

| Item | Where | Effort |
|---|---|---|
| `aria-label` on hub-page landmarks (catalog/portal/dashboard) | 3 files | Small |
| Dashboard 🟢/🟡 tax-status emoji → CSS dots | `templates/page.educator-dashboard.liquid:544-575` | Small (cosmetic; a11y already passes since text follows emoji) |
| Login password show/hide toggle | `sections/educator-login.liquid` | Medium |
| Catalog directory body-text under 14px | `templates/page.educator-catalog.liquid` (16 declarations) | Medium |
| Lazy-load Woodland + Sensory remaining images | Wood: 13 more, Sensory: 3 more | Small |

From the retail audit (PR #10) — NOT yet shipped:
- 5 `outline:none` declarations in `theme.css.liquid` (need context check each)
- Verify `img_tag` filter outputs `loading="lazy"` for retail collection/product pages
- `.hidden-label` CSS implementation audit (reset_password + activate_account)
- `<button>...</a>` mismatched closing tag at `customers/addresses.liquid:16`

---

## 9. Open PR — pick up here

**PR #10 — Retail polish** (https://github.com/mytoywagon2020/website/pull/10)
- Currently draft, 2 commits, mergeable_state clean
- No CI configured, no review comments
- Mark "Ready for review" then "Squash and merge" when comfortable. Shopify auto-deploys within ~30s of merge.

---

*Generated by Claude Code session, 2026-05-30. Update this file at the end of each editing session so the next person/agent walks in oriented.*
