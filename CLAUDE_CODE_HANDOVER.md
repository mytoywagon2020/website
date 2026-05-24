# MTW Educator Portal — Handover to Claude Code

**Project:** My Toy Wagon Educator Portal — 8 ecosystem catalog pages for school buyers, plus supporting back-matter pages.
**Source of truth (design + content):** This Claude.ai project (project ID is in the URL when you open it; the bookmark is *MTW Educator Portal*).
**Status at handover:** All 8 ecosystem pages are content-complete and ready for Shopify deployment. Woodland is the only ecosystem with images already wired; the other 7 need their image sets gathered + wired.

---

## What you're inheriting

### 8 deployable ecosystem pages (Liquid-ready)

Each is a single self-contained `.html` file with `{% layout none %}` at the top, ready to be dropped into Shopify as a page template. Canonical URLs are already declared inside each file. **Filenames in this bundle match contents** — verify with the SHA-256 manifest before trusting anything else.

| Vol | File | Canonical | H1 | Notes |
|---|---|---|---|---|
| 01 | `Sensory Play v1.html` | educator-sensory-play | Sensory Play | Clean, images TBD |
| 02 | `Nature Play v1.html` | educator-nature-play | Nature Play | Clean, images TBD |
| 03 | `Woodland v1.html` | educator-woodland | The Woodland. | **14/14 images wired** ✓ |
| 04 | `Small World v2.html` | educator-small-world | Small World & Storytelling | 17/17 images wired ✓ |
| 05 | `Fairy Villages v3.html` | educator-fairy-villages | Fairy Villages | **Canonical** — has `{% layout none %}` |
| 05 | `Fairy Villages v4.html` | educator-fairy-villages | The Fairy Villages. | **DUPLICATE — discard** (missing `{% layout none %}`) |
| 06 | `STEAM v1.html` | educator-steam | STEAM Wonder & Investigation | Clean, images TBD |
| 07 | `Dramatic Play v1.html` | educator-dramatic-play | Dramatic Play | Clean, images TBD |
| 08 | `Creative Arts v1.html` | educator-creative-arts | Creative Arts | Clean, images TBD |

### Images bundle

- `assets/` — 30+ image files already wired into the HTML
  - `sw-*` files belong to Small World (17 images)
  - `wd-*` files belong to Woodland (15 images, including spare deer-family variant)
  - Other files (e.g. `ambrosius-gnome-family.webp`, `papoose-gnome-family.webp`) belong to Fairy Villages but are not yet referenced by the HTML

### Supporting pages (back-matter)

- `uploads/MTW Website (17)/designs/` — 8 supporting pages (catalog-back-matter, educator-dashboard, ordering-for-schools, procurement-guide, new-quote, school-affiliate, vendor-profile, educator). These are reference materials and may not need deployment.

---

## File integrity verification (do this first)

The other deployment agent reported file-rotation bugs that were NOT in the source — they were caused by zip-extract / directory-walk off-by-one in their tooling. **Before trusting any filename, verify by SHA-256 hash.**

```bash
shasum -a 256 *.html
```

If hashes don't match the manifest the design team provides, your tool is matching files by directory-listing position instead of content. Fix that first.

**Canonical conventions every page declares:**
- `{% layout none %}` on line 1
- `<title>` containing the section name + "for Schools · My Toy Wagon Educator Catalog"
- `<link rel="canonical">` pointing to its own `/pages/educator-<slug>` URL
- `og:url`, `og:title`, `og:image` meta tags
- A `CATALOG` JS const with `{ volume: "0N", ecosystem: "...", makers: [...] }`

---

## Image wiring conventions

Images in the HTML reference local paths: `<img src="assets/wd-deer-family-hero.png" alt="...">`. For Shopify deployment, these need to become Liquid asset references.

**Two options:**

### A — Theme assets (recommended for catalog templates)
1. Upload images via theme code editor → Add asset → into `/assets/` folder
2. Replace `src="assets/<filename>"` with `src="{{ '<filename>' | asset_url }}"`
3. Bulk-replace command:
```bash
# Mac/Linux
sed -i '' 's|src="assets/\([^"]*\)"|src="{{ '"'"'\1'"'"' | asset_url }}"|g' *.html
```

### B — Files section (use if images persist across theme changes)
1. Upload images via Shopify Admin → Content → Files
2. Replace `src="assets/<filename>"` with `src="{{ '<filename>' | file_url }}"`

**Already-wired example (Woodland):** see `Woodland v1.html` — 14 image tags, all pointing to `assets/wd-*` paths.

---

## Pages still needing image wiring

These 7 ecosystem pages have image placeholders (`<span class="tag">[ ... ]</span>` markers in empty `.tile` divs) instead of real `<img>` tags. The design team is gathering product photos for each. Until images land:

- **Sensory Play** — 14 image slots
- **Nature Play** — 14 image slots
- **Small World** — fully wired (no action needed) ✓
- **Woodland** — fully wired (no action needed) ✓
- **Fairy Villages** — 15 image slots
- **STEAM** — 14 image slots
- **Dramatic Play** — 14 image slots
- **Creative Arts** — 14 image slots

**Wire-up pattern** (replace empty placeholder):
```html
<!-- BEFORE -->
<div class="tile t-soft">
  <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>
  <span class="tag">[ HERO PRODUCT · PRODUCT NAME, description... ]</span>
</div>

<!-- AFTER -->
<div class="tile t-soft has-photo">
  <img src="assets/<slug>-<product>.webp" alt="Detailed alt text describing the photo."/>
  <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>
  <span class="tag">[ HERO PRODUCT · PRODUCT NAME ]</span>
</div>
```

The `has-photo` class hides the gradient backdrop. The descriptive paragraph inside `[ ... ]` gets replaced with a short hand-off tag.

---

## Style + content conventions (already applied across all 8 files)

- **No em-dashes in body copy** — use periods or semicolons
- **Complete sentences** — no fragment captions
- **Section numbering** — eyebrow text reads `"03. What a Woodland Is"` (number prefix on every editorial eyebrow from section 03 onward; cover + quick facts are unnumbered)
- **No section-divider numbers** — the decorative numeric chapter marks have been stripped (they were duplicating the eyebrow numbers)
- **No "For Educators" pill on covers** — removed
- **Cover section number** — 88px italic serif, `clamp(48px, 5.6vw, 88px)` responsive
- **`--mono`** — set to real monospace stack (`ui-monospace, ...`) so SKU codes read code-y
- **Pair labels** — `EXTEND THE PLAY`, `PAIRS WITH`, etc. wrapped in an accent-tinted pill with left accent bar
- **Empty pair-thumbnail tiles** — removed (only present where a real image was wired)
- **Date references** — "2026 Fall Edition" (was "2026 Spring Edit" before — schools-calendar-aligned for August release)

---

## Layout system

Each ecosystem page follows the same structural rhythm:

1. **01 Cover** — full-bleed photo, masthead, section number, audience strip
2. **02 Quick Facts** — anchor strip with cross-section links + key promises
3. **03 Editorial Intro** — 2-column: photo + literary essay (the "what is this ecosystem" piece)
4. **04 Hero Product** — `.split` layout, image-left, content-right
5. **05 Gallery 1** — 5-card grid (`.gallery`) with `<article class="home">` cards
6. **06 Gallery 2** — alternate-pattern 5-card grid (`.gallery.even`)
7. **07 Featured Product 2** — `.split.image-right` mirror layout (creates left-right rhythm with section 04)
8. **08 Pull-quote / bridge** — optional editorial pause
9. **09 Educator Program · Custom Combo** — bundle CTA with whole-ecosystem pricing
10. **Quote form** — Klaviyo embed (`mtw-quote-form-id` placeholder)
11. **Trust strip** — fair trade / lead-free / lifetime repair badges
12. **Footer outro** — "From the Educator Catalog" cross-link grid

**CSS rotation rules** (in every file):
- Section 04 (Hero Product) → `.split` (image-left)
- Section 07 (Featured 2) → `.split.image-right` (image-right) — creates visual rhythm

---

## CSS architecture cheat-sheet

Each file has these CSS variable presets (top of `<style>`):

```css
--accent:       #...     /* primary signature color */
--accent-deep:  #...     /* darker accent for hover/focus */
--accent-soft:  #...     /* soft accent for tinted backgrounds */
--cream:        #FAF6ED  /* page background */
--card-bg:      #F5F0E5  /* card / well backgrounds */
--ink:          #2C1A0E  /* primary body text */
--ink-soft:     #5A4A3C  /* secondary text */
--stone:        #8A7868  /* labels, meta */
--rule:         #D8CFC0  /* hairline borders */
--gilt:         #...     /* accent for editorial highlights */
--serif:        "Cormorant Garamond", Garamond, Georgia, serif;
--sans:         "Mulish", "Helvetica Neue", system-ui, sans-serif;
--mono:         ui-monospace, "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;
```

Ecosystem color presets vary per file (Woodland = forest greens; Small World = lavender/plum; Sensory Play = terracotta; etc.). The structural CSS is shared; the palette is per-file.

---

## Known issues / decisions still open

1. **Fairy Villages v4** — duplicate of v3, missing `{% layout none %}`. **Discard.**
2. **Bundle thumbnails** — many "Pairs with" / "Extend the play" blocks reference bundles for which no photo exists. We removed the empty placeholder tiles; pair blocks now flow as text-only. If product-bundle photos are commissioned later, they can be added back.
3. **Liquid logo asset** — every file references `<img src="{{ 'mtw-logo-full.png' | asset_url }}">` in the header. This will 404 in local preview but works correctly when deployed to a Shopify theme that has `mtw-logo-full.png` in its `/assets/` folder.
4. **Klaviyo form ID** — every quote form has `data-klaviyo-form="mtw-quote-form-id"`. Replace this with the actual Klaviyo embed ID before deployment.
5. **Hardcoded URLs** — internal links use `/pages/educator-<slug>` (relative). External maker links should be audited before launch.

---

## Where to find things in this project

This is the Claude.ai project where the design + content work happened. To return here:

1. Go to **claude.ai/projects** (logged in)
2. Look for **"MTW Educator Portal"** in the project list
3. Open it — you'll see all 9 HTML files + the `assets/` folder + this handover doc

**Files in the project root:**
- All 9 `.html` ecosystem files (latest versions)
- `assets/` — all wired product photos
- `uploads/` — raw source images (some not yet wired into HTML)
- `downloads/` — packaged bundles I've prepared for delivery
- `screenshots/` — local QA captures (can delete)
- `CLAUDE_CODE_HANDOVER.md` — this file
- `CLAUDE_CODE_ORIENTATION.md` — earlier orientation notes (if present)
- `MERGE_CHOREOGRAPHY.md` — earlier merge plan notes (if present)

**To get a fresh export of everything:** ask the design team to re-zip the project root or to package by file.

---

## Suggested deployment order

1. **Verify file integrity** (SHA-256 hash check)
2. **Delete Fairy Villages v4** (duplicate, missing layout directive)
3. **Wire images for the 7 unwired ecosystem pages** (Sensory, Nature, Fairy Villages, STEAM, Dramatic Play, Creative Arts — and verify Small World wiring) as image sets become available
4. **Apply Liquid asset rewrite** (`assets/foo.webp` → `{{ 'foo.webp' | asset_url }}`)
5. **Upload theme assets** via theme code editor
6. **Push templates** to staging Shopify theme
7. **Create Shopify Pages** at each `/pages/educator-<slug>` handle
8. **Set up `catalog.volume` metafield** on each page (values: 01–08)
9. **Replace Klaviyo form placeholder** with real form ID
10. **Audit** — catalog ↔ portal consistency (SKUs, brand origins, pricing, conventions)

---

## Contact points

- **Design + content questions:** ask the human (this project's owner) — they have direct access to the source Claude.ai project
- **Image gathering:** in-progress; new images arrive as drag-and-drop uploads here
- **Shopify staging access:** confirm with the human before pushing to staging

---

*Generated by the design assistant for handover to Claude Code. Last updated: May 24, 2026.*
