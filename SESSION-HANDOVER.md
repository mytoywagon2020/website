# Session Handover — Educator Portal + Theme Work

Branch: `claude/fix-github-access-pFh80` (all work mirrored to GitHub).
Theme: **"Current Shop with Updated Impulse (9.0)"** — `gid://shopify/OnlineStoreTheme/145720180906`, **NOW `role: MAIN` (LIVE/published)** as of 2026-05-16. It was treated as unpublished earlier this session but has since been published. **Shopify API blocks all theme-file writes to the live theme** — theme changes can no longer be pushed via API; they must be mirrored in git and applied by the merchant (admin code editor) or via a duplicate→edit→merchant-publish flow. Earlier "pushed to theme" claims below predate this and may already be live.
Store: My Toy Wagon (mytoywagon.com), plan Shopify.

This documents everything done/pending in this session so work can continue. It does **not** replace the original `HANDOVER.md` (designer → build handoff); this is the implementation-status companion.

---

## 1. GitHub access — FIXED
Read+write confirmed. The Claude GitHub App had to be installed/authorized by the owner (it was OAuth-only before). All changes are committed and pushed to the branch above. Nothing is at risk in-session.

## 2. Architecture principle in use
Per the owner's directive: **maximize Shopify-admin-native storage so a theme update can't wipe work.** Page content lives in Shopify **admin Pages** (not theme files); URL redirects are admin-native; the theme only holds thin renderers, mirrored to Git for instant re-push.

## 3. Educator portal — public marketing pages (DONE, unpublished)
Created as Shopify **admin Pages**, body HTML stored in admin, rendered via the existing standalone `templates/page.educator-portal.liquid` (`{% layout none %}`). Mirrored at `shopify/pages/*.html`; reproducible via `scripts/build_pages.py`.

| Page | Handle | Shopify ID | Status |
|---|---|---|---|
| Ordering for Schools | `schools` | Page/115575914666 | Draft |
| Procurement Guide (5-pg printable) | `procurement-guide` | Page/115575947434 | Draft |
| Vendor Profile | `vendor-profile` | Page/115576045738 | Draft |
| School Affiliate | `school-affiliate` | (pre-existing) | Untouched — owned elsewhere |

Corrections applied & live: DUNS removed (procurement cover + vendor-profile row); email is **`accounting@mytoywagon.com`** (an earlier `accounts@` rename was reverted); EIN/Tax ID `87-3421098` kept; catalog header/footer/resource links removed from the schools page (no catalog link yet).

**Open before publish:** owner review + publish the 3 drafts; replace placeholder document links (`#`) on resale cert / business license / quote-request-form with real uploaded PDFs; `/pages/catalog` links depend on the other (retail) window's catalog page; plain-text `mytoywagon.com/educator` / `/educator-dashboard` in the procurement guide are placeholders. Pages not visually QA'd (no browser; drafts not public).

## 4. URL redirects (DONE, admin-native, theme-safe)
- `/educator` → `/pages/educator-program` (pre-existing; correct)
- `/procurement-guide` → `/pages/procurement-guide` (created this session — `UrlRedirect/443810742442`)

## 5. Header (DONE, live on theme + mirrored)
`sections/header.liquid` replaced with the **Stacked sticky header** — centered logo masthead that collapses on scroll into a compact nav row with the wagon mark. Namespaced `.mtw-hdr` (no Impulse collisions). Cart drawer + mobile nav drawer kept wired (hamburger → Impulse `NavDrawer`); section `{% schema %}` preserved so theme editor / `header-group.json` still work; logo via `{{ 'mytoywagon-logo-mark.png' | file_url }}`; cart count dynamic. Utility + free-shipping bars intentionally **not** duplicated (they render from `mtw-utility-bar` above the header). Mirrored: `shopify/theme/sections/header.liquid`.

**Open — header nav links not yet wired to real collections.** Current links are the design defaults and several handles are wrong. Resolved real handles:
- Shop → `/collections/all` (valid built-in)
- New → `/collections/new-arrivals` ("What's New", 2,621)
- Pre-order → `/collections/pre-order` ("Pre-Order", 35)
- Sale → `/collections/sale` ("Sale Collection", 1,474)
- **Ages** → no umbrella collection (see §7); pending
- **Brands** → no umbrella collection; options: `/collections` (all-collections page) · `featured-brands` (3,159) · `selected-brands` (2,535) — pending owner pick

## 6. Footer (NO net change)
The footer star = the **"Top Quality Store / Awarded by Google" badge** in `sections/mtw-footer.liquid` (no Judge.me code anywhere in theme). It was hidden then **reverted** at owner request — currently `show_badge: true` (original state). Mirrored: `shopify/theme/sections/footer-group.json`.

## 7. Age collections (CREATED by owner, EMPTY — population pending decision)
Owner created 4 **manual, empty** collections (`ruleSet: null`):

| Handle | Title | ID |
|---|---|---|
| `0-to-12-months` | 0 to 12 Months | Collection/355725738154 |
| `1-to-3-years` | 1 to 3 Years | Collection/355725770922 |
| `3-to-5-years` | 3 to 5 Years | Collection/355725803690 |
| `5-to-8-years` | **8 Years and Up** (handle/title mismatch — treat as 8+) | Collection/355725836458 |

Decision so far: convert to **smart collections** with disjunctive (match-ANY) TAG rules. Age tags in the store are highly inconsistent. Approved per-bucket tag mapping (NOT yet applied):

- **0 to 12 Months** ← `0 Years`, `0 Years+`, `3 Months+`, `6 months+`, `10 months+`, `12 Months+`, `12  Months`
- **1 to 3 Years** ← `1 Year`, `1 Year+`, `18 Months`, `18 Months+`, `2 Year`, `2 Years`, `2 Years+`
- **3 to 5 Years** ← `3 Years`, `3 Years+`, `4 Years`, `4 Years+`, `5 Years`, `5 years+`
- **8 Years and Up** ← `8 years`, `9 years`, `10 years`, `11 Years`, `12 Years` (explicitly **excludes** `6 years`, `6 Years+`, `7 years`)

**Coverage gap (owner-accepted):** products tagged only `6 years` / `6 Years+` / `7 years`, and range tags (`2 - 5 Years`, `3-8 Years`, `4-7 Years`, `7-11 Years+`) fall into no bucket.

**Status: NOT applied.** The `collectionUpdate` mutation is validated and ready. Owner is deciding between:
- **Layer 1 (pragmatic):** apply the OR-tag smart rules now — instant, ~approximate, known gaps.
- **Layer 2 (durable fix):** normalize age into one signal (recommended: product metafield e.g. `custom.age_bucket` = `0-12m | 1-3y | 3-5y | 8+`) interpreted from existing tags with spot-checking, then key the smart collections off that.
Recommendation given: do Layer 1 now (unblocks), schedule Layer 2 as the real fix.

## 8. Judge.me floating "Reviews" tab (NOT theme code — owner action)
The vertical "Reviews" tab on the left edge is the **Judge.me app's Floating Reviews Tab**, injected by the app (confirmed: no Judge.me markup in `layout/theme.liquid`, header, or footer). Cannot be toggled via API/from here. Disable via: Judge.me app → Settings → Widget/look-and-feel → Floating Reviews Tab → Off; or Online Store → Themes → (9.0) → Customize → Theme settings → App embeds → toggle off the Judge.me embed.

## 9. Scope / coordination
- This session: **educator portal** + (reassigned by owner) the **header** and footer badge.
- Other (retail) window: retail theme, PDPs, collections, marketing, shared chrome generally.
- Owner-owned elsewhere, do **not** touch: catalog **back-matter** / catalog.
- "Three icons (2, 3, 4)" the owner mentioned never arrived (no attachment received) — purpose unknown; open.

## 10. Commits this session (branch `claude/fix-github-access-pFh80`)
```
a4bb0fb Revert: restore footer Google badge (show_badge=true)
4f5ab62 Hide footer Google "Top Quality Store" badge
4a7b049 Add stacked sticky header section
1542569 Revert educator pages back to accounting@ email
8db02b5 Apply educator-page content corrections
efaa539 Add educator-portal public marketing pages (schools, procurement, vendor)
1f69ac3 Mirror educator-portal design handoff v12
```

## 11. Immediate next actions
1. Decide age-collection population: Layer 1 (apply approved OR-tag smart rules) or Layer 2 (metafield scheme) — then execute.
2. Pick the **Brands** and **Ages** header-nav targets; then wire all 6 header nav links to real handles and push.
3. Owner: disable Judge.me floating tab in the app/app-embeds.
4. Owner: review + publish the 3 educator drafts; upload real PDFs for placeholder document links.
5. Re-share the "three icons" with intended placement.

---

## 12. Session continuation log (2026-05-16, later)

**⚠️ Theme state is volatile — always re-check `themes{ role }` before any push.** It flipped MAIN↔UNPUBLISHED many times. As of this log: **LIVE/MAIN = old "Current Shop " (`132143448234`)**; **9.0 (`145720180906`) = UNPUBLISHED** and API-writable again. The §4 header line above is stale — 9.0 is NOT currently live.

### Production incident — store-wide "out of stock" (RESOLVED)
- Symptom: entire live storefront showed every product (incl. pre-orders) sold out, on both themes; Admin showed healthy inventory.
- Root cause: **primary market "International" had its catalog in `DRAFT`** (`gid://shopify/MarketCatalog/1586757802`).
- Fix applied: `catalogUpdate` → status `ACTIVE`. Price list is base USD at 0% adjustment (no price change). Reversible. Confirmed resolved by owner. Not theme/code related.
- Follow-up (owner, optional): consider making "United States" the primary market (can't be done via API; admin only).

### Theme/store changes shipped (mirrored to git, pushed to 9.0 draft unless noted)
- **mtw-collection** section + `templates/collection.json` — story-anchored collection template (hero/stats/sticky filters/grid/interlude/maker/related; native filters/sort/paginate). Fixes: removed invalid `pluralize`; fixed `image_tag` alt; `new_days` range; **sold-out now computed from variant inventory** (was false-flagging via `product.available`); **low-stock badge removed**; **Brand/Category/Product type filter groups hidden**.
- Caveat: collections with a **custom template suffix** (e.g. "Gifts under $50" → `collection-landing`) do NOT use the new default template — owner must switch them to **Default** in admin, or roll mtw-collection into those suffix templates.
- **header.liquid** — desktop nav now **menu-driven** from the section's `main_menu_link_list` (default `main-menu`); search-bar text darkened to ink for contrast.
- **mtw-product-rail** — cards now render **vendor → title → ★ → price** (category line removed; price kept).
- **Shop by Age page** — `/pages/shop-by-age` (`gid://shopify/Page/115585122474`, published), tiled grid with photos → the 5 age collections (`0-to-12-months`, `1-to-3-years`, `3-to-5-years`, `5-to-8-years-1`, `5-to-8-years`). `main-menu` "Shop by Age" item (`453152899242`) repointed to it via `menuUpdate` (full tree + dropdown children preserved). Admin-native → works on both themes.

### Still open
- Footer/homepage link fixes (footer `e-gift-card`→`my-toy-wagon-digital-gift-card`, hero "Find a gift under $50" CTA → `/collections/gifts-under-50`, `mtw_age` a2 "Toddler" → `1-to-3-years`, `mtw_gift` pills). Header link fixes are now moot (menu-driven).
- Age smart-collection population (owner owns the age-tag/metafield cleanup) — the 4/5 age collections are still empty.
- Optional: rebuild Shop by Age as an editable theme section; per-collection story content via metafields for mtw-collection.
- Judge.me floating tab (owner, app settings).
- When 9.0 is to go live, owner publishes it; if it's MAIN, API theme writes are blocked (use admin code editor or duplicate→publish).
