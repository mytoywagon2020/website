# Merge Choreography — Editorial Design Polish into Repo

> **Audience**: Claude Code working in the `claude/fix-github-access-pFh80` branch (or whichever educator branch is current).
>
> **Source of truth**: This project's HTML files (delivered as a download bundle).
>
> **Goal**: Land the editorial design polish into the repo as a sequence of clean, atomic commits, **without** touching the work Claude Code already has there (Liquid asset paths, Sensory Play numbering fix, Nature Play catalog corrections).
>
> Apply commits in order. Each is independent; if one looks wrong on visual inspection, skip it and continue.

---

## Files affected

8 HTML pages in the repo:

```
educators.html
educator.html
educator-dashboard.html
Sensory Play v1.html
Nature Play v1.html
Woodland v3.html
Small World v2.html
Fairy Villages v3.html
```

---

## Pre-flight check before any merge

1. **Confirm repo's HEAD is clean.** No uncommitted changes.
2. **Liquid asset paths**: the delivered files use `{{ 'X' | asset_url }}` — same as repo. **No conversion needed.**
3. **Sensory Play section-numbering**: the delivered file uses `volume: "01"` and `"SENSORY PLAY"`. Same as your repo. **No conflict.**
4. **Nature Play catalog corrections**: the delivered file already includes your corrections (felt wool · Nepal, SVLK teak · Indonesia, FSC Doussie · Vietnam, GOTS/OEKO-TEX/Fair Trade). **No conflict.**

If any of the above shows a conflict, stop and report before continuing.

---

## Commit 1 — Add `<meta name="robots" content="noindex,nofollow">` to all auth-walled pages

**Why**: Auth-walled section pages, catalog landing, and dashboard should not be indexed by Google. Educator apply page (`educator.html`) and the four public-facing pages (schools, procurement-guide, vendor-profile) stay indexable.

**Where**: 7 files, right after the `<meta name="viewport">` line.

**Files affected**:
- educators.html
- educator-dashboard.html
- Sensory Play v1.html
- Nature Play v1.html
- Woodland v3.html
- Small World v2.html
- Fairy Villages v3.html

**Add this line**:
```html
<meta name="robots" content="noindex,nofollow"/>
```

**Do NOT add** to `educator.html` (apply page must be public and indexable).

**Commit message**: `chore(seo): noindex auth-walled educator pages`

---

## Commit 2 — Strengthen copyright footer line

**Why**: Editorial copy is automatically copyrighted, but adding "All rights reserved" creates clear legal standing.

**Where**: 6 files. Find the `legal` block at the very bottom (after the main footer's `foot-bottom` band).

**Files affected**: educators, educator, Sensory Play v1, Nature Play v1, Woodland v3, Small World v2, Fairy Villages v3, educator-dashboard

**Find**:
```html
<span>© 2026 My Toy Wagon &nbsp;·&nbsp; Educator Catalog</span>
```

**Replace with**:
```html
<span>© 2026 My Toy Wagon &nbsp;·&nbsp; Educator Catalog &nbsp;·&nbsp; All rights reserved</span>
```

For `educator-dashboard.html`, the change is more involved — it lacked a copyright entirely. Add inside `<footer>`:
```html
<div style="padding: 18px 40px; font-family: var(--sans, system-ui, sans-serif); font-size: 12px; color: var(--stone, #5F5E5A); text-align: center; border-top: 0.5px solid var(--rule, rgba(44,44,42,.12));">© 2026 My Toy Wagon &middot; Educator Portal &middot; All rights reserved</div>
```

**Commit message**: `chore(legal): strengthen footer copyright across pages`

---

## Commit 3 — Cover H1 sizing and positioning (fixes visible overlap with cover footer)

**Why**: The cover H1 (giant section name) overlapped the cover footer (audience block) on every section page. H1 dropped from 168px max to 132px, and bottom anchor lifted from 132px to 220px.

**Where**: 5 section pages. The `.cover h1{...}` block in the inline `<style>`.

**Files affected**: Sensory Play v1, Nature Play v1, Woodland v3, Small World v2, Fairy Villages v3

**Find**:
```css
.cover h1{
  position:absolute;
  left: clamp(28px, 5vw, 56px);
  right: clamp(28px, 5vw, 56px);
  bottom: 132px;
  z-index: 3;
  margin: 0;
  font-family: var(--serif);
  font-weight: 400;
  color: var(--cream);
  font-size: clamp(56px, 10vw, 168px);
  line-height: .92;
  letter-spacing: -.012em;
  text-shadow: 0 1px 28px rgba(0,0,0,.2);
}
```

**Replace with**:
```css
.cover h1{
  position:absolute;
  left: clamp(28px, 5vw, 56px);
  right: clamp(28px, 5vw, 56px);
  bottom: 220px;
  z-index: 3;
  margin: 0;
  font-family: var(--serif);
  font-weight: 400;
  color: var(--cream);
  font-size: clamp(48px, 8vw, 132px);
  line-height: .94;
  letter-spacing: -.012em;
  text-shadow: 0 1px 28px rgba(0,0,0,.2);
}
```

**Commit message**: `fix(cover): cover h1 no longer overlaps cover footer`

---

## Commit 4 — Breadcrumb component (replaces `.back` link in subnav)

**Why**: Retail-parallel breadcrumb. Replaces the single-link "The Catalog" with `Home / Educator Catalog / Section XX · Name`.

**Where**: 5 section pages + educators.html.

### 4a — Add breadcrumb CSS

In every section page's `<style>` block, add this CSS rule block (anywhere before `</style>`):

```css
/* Breadcrumb, retail-parallel.
   Replaces the .back link in .subnav with a Home > Educator Catalog > Section
   trail. Mirrors retail's Home > Collection > Product logic, optimized for B2B
   buyers who navigate by program tier first, then section. */
.breadcrumb{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--sans);
  font-size: 12px;
  letter-spacing: .04em;
  color: var(--stone);
}
.breadcrumb a{
  color: var(--ink);
  text-decoration: none;
  font-weight: 500;
  transition: color .2s ease;
}
.breadcrumb a:hover{ color: var(--forest); }
.breadcrumb .sep{
  color: var(--rule-strong);
  font-size: 11px;
  user-select: none;
}
.breadcrumb [aria-current="page"]{
  color: var(--stone);
  font-weight: 400;
}
@media (max-width: 720px){
  .breadcrumb{ font-size: 11px; gap: 8px; }
  .breadcrumb .home-crumb{ display: none; }
}
```

### 4b — Replace `.back` link in `.subnav-inner`

**Find** (in each section page's HTML body):
```html
<a href="educator-dashboard.html" class="back">The Catalog</a>
```

**Replace with** (substitute `SECTION_NUM` and `SECTION_NAME` per file):

```html
<nav class="breadcrumb" aria-label="Breadcrumb">
  <a href="MTW Homepage v3.html" class="home-crumb">Home</a>
  <span class="sep" aria-hidden="true">/</span>
  <a href="educators.html">Educator Catalog</a>
  <span class="sep" aria-hidden="true">/</span>
  <span aria-current="page">Section SECTION_NUM &middot; SECTION_NAME</span>
</nav>
```

| File | SECTION_NUM | SECTION_NAME |
|---|---|---|
| Sensory Play v1.html | 01 | Sensory Play |
| Nature Play v1.html | 02 | Nature Play |
| Woodland v3.html | 03 | Woodland Habitats |
| Small World v2.html | 04 | Small World &amp; Storytelling |
| Fairy Villages v3.html | 05 | Fairy Villages |

### 4c — Add breadcrumb band to educators.html

Insert just before `<!-- =========================== HERO =========================== -->`:

```html
<div style="background: var(--cream); border-bottom: 0.5px solid var(--rule); padding: 14px clamp(20px, 4vw, 44px);">
  <div style="max-width: 1440px; margin: 0 auto;">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="MTW Homepage v3.html" class="home-crumb">Home</a>
      <span class="sep" aria-hidden="true">/</span>
      <span aria-current="page">Educator Catalog</span>
    </nav>
  </div>
</div>
```

Plus the same breadcrumb CSS block (4a) into educators.html's `<style>`.

**Commit message**: `feat(nav): retail-parallel breadcrumb component`

---

## Commit 5 — Layout alternation system (gallery + split variants)

**Why**: Editorial rhythm. Adds 3 split variants (default / `.image-right` / `.stage`) and 3 gallery variants (default / `.even` / `.strip`). Used to break the "endless catalog list" feeling.

**Where**: All 5 section pages.

**Add** the following CSS rules (anywhere in `<style>`):

```css
/* Layout alternation, editorial rhythm.
   .split.image-right flips the standard split so content-left, image-right.
   .split.stage makes the image full-bleed with content centered below.
   .gallery.even = 5 equal columns. .gallery.strip = 3 hero + 2 wide. */
.split.image-right .img-side{ order: 2; }
.split.image-right .content{ order: 1; }
@media (max-width: 980px){ .split.image-right .img-side, .split.image-right .content{ order: initial; } }

.split.stage{ display: block; }
.split.stage .img-side{ width: 100%; aspect-ratio: 21 / 9; }
.split.stage .content{ max-width: 720px; margin: clamp(40px, 5vw, 64px) auto 0; padding: 0 clamp(20px, 5vw, 56px); text-align: center; }
.split.stage .content .craft, .split.stage .content .pairs-with{ text-align: left; }

.gallery.even .homes{ grid-template-columns: repeat(5, 1fr); }
.gallery.even .home{ grid-column: span 1 !important; }
@media (max-width: 1180px){ .gallery.even .homes{ grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 720px){ .gallery.even .homes{ grid-template-columns: 1fr 1fr; } }

.gallery.strip .homes{ display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: auto auto; gap: clamp(18px, 2vw, 28px); }
.gallery.strip .home:nth-child(4), .gallery.strip .home:nth-child(5){ grid-column: span 1; }
```

**Apply variants to specific sections** (already baked into the delivered files; this is the mapping for reference):

| File | Section | Variant applied |
|---|---|---|
| Sensory Play v1.html | Gallery 1 (Tray Range) | `.even` |
| Sensory Play v1.html | Gallery 2 (Therapy Dough) | `.even` |
| Sensory Play v1.html | Gallery 3 (Calm Corner) | `.even` |
| Sensory Play v1.html | Featured 2 (Letter Tracing) | `.image-right` |
| Sensory Play v1.html | Featured 3 (My Forest Floor) | `.stage` |
| Woodland v3.html | Gallery 2 (Trees) | `.even` |
| Woodland v3.html | Featured 2 (Seasonal Trees) | `.stage` |
| Small World v2.html | Featured 2 (Gruffalo Bundle) | `.stage` |
| Small World v2.html | Gallery 3 (Circle Time) | `.even` |
| Fairy Villages v3.html | Hero (Mushroom Garden) | default split (NOT stage — known issue with image, see commit 8) |

**Commit message**: `feat(layout): editorial gallery + split variants for rhythm`

---

## Commit 6 — Pull-quotes between major sections

**Why**: Editorial break between sections, anchored in catalog source text.

**Where**: 5 section pages, inserted between major sections.

**Add** the following CSS to each section page:

```css
.pull-quote{
  background: var(--cream);
  padding: clamp(56px, 7vw, 96px) clamp(20px, 5vw, 56px);
  text-align: center;
  border-top: 0.5px solid var(--rule);
  border-bottom: 0.5px solid var(--rule);
}
.pull-quote blockquote{
  max-width: 56ch;
  margin: 0 auto;
  font-family: var(--serif);
  font-style: italic;
  font-weight: 400;
  font-size: clamp(22px, 2.8vw, 32px);
  line-height: 1.25;
  color: var(--ink);
  letter-spacing: -.008em;
}
.pull-quote blockquote em{ color: var(--accent-deep); font-style: italic; }
.pull-quote cite{
  display: block;
  margin-top: 28px;
  font-family: var(--sans);
  font-style: normal;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .22em;
  text-transform: uppercase;
  color: var(--stone);
}
```

**Add** pull-quote markup (refer to delivered files for exact placement; catalog page references in `cite`):

| File | Pull-quote text | Catalog page |
|---|---|---|
| Sensory Play v1.html | "Fill it with rainbow rice on Monday morning. By Tuesday, children have sorted by color, built a story, and *asked to refill it themselves.*" | p. 6 |
| Sensory Play v1.html | "Stillness invites attention inward. *Quiet tools* for the kind of classroom transitions that keep a morning from unraveling." | p. 12 |
| Woodland v3.html | "Every child knows the forest is alive. *These pieces agree.*" | p. 18 |
| Small World v2.html | "Small hands, vast worlds. The stories children need to tell *cannot always wait for words.*" | p. 23 |
| Fairy Villages v3.html | "A child who has a fairy village has a world *she can hold, arrange, and return to.*" | p. 31 |
| Nature Play v1.html | "The garden has always been the best classroom. *These are the tools that bring it inside.*" | p. 13 |

**Commit message**: `feat(editorial): catalog-sourced pull-quotes between sections`

---

## Commit 7 — Section dividers (numbered editorial transitions)

**Why**: Magazine-style numbered transitions before each major block.

**Where**: All 5 section pages.

**Add** CSS:

```css
.section-divider{
  max-width: 1280px;
  margin: 0 auto;
  padding: 36px clamp(20px, 5vw, 56px) 0;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 24px;
  align-items: center;
}
.section-divider .num{
  font-family: var(--serif);
  font-style: italic;
  font-weight: 500;
  font-size: 16px;
  color: var(--accent-deep);
  letter-spacing: .04em;
}
.section-divider .line{
  height: 0.5px;
  background: var(--rule-strong);
}
.section-divider .label{
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .22em;
  text-transform: uppercase;
  color: var(--stone);
}
@media (max-width: 720px){
  .section-divider{ grid-template-columns: auto 1fr; gap: 16px; }
  .section-divider .label{ grid-column: 1 / -1; margin-top: -4px; }
}
```

**Markup pattern** (insert before each major section):
```html
<div class="section-divider">
  <span class="num">NN</span>
  <span class="line"></span>
  <span class="label">SECTION LABEL</span>
</div>
```

Exact placements vary by file — see delivered files for the numbered sequence (2, 4, 6 per section page typically).

**Commit message**: `feat(editorial): magazine-style numbered section dividers`

---

## Commit 8 — Caption variety (`.cap.expanded`)

**Why**: Apply small accent rule + serif italic body to ONE editorial hero card per gallery for visual hierarchy.

**Where**: 7 cards across 5 section pages.

**Add** CSS:

```css
.gallery .home .cap.stripped .desc{ display: none; }
.gallery .home .cap.stripped{ padding-bottom: 16px; }
.gallery .home .cap.expanded::before{
  content: "";
  display: block;
  width: 32px;
  height: 1px;
  background: var(--accent);
  opacity: .6;
  margin: 10px 0 12px;
}
.gallery .home .cap.expanded .desc{
  font-family: var(--serif);
  font-style: italic;
  font-size: 16px;
  line-height: 1.5;
}
```

**Apply class** by changing `<div class="cap">` to `<div class="cap expanded">` on these specific cards:

| File | Card |
|---|---|
| Sensory Play v1 | Bear Tray, Mindfulness Magic Ball |
| Woodland v3 | Squirrel Family, Green Oak |
| Small World v2 | Tiny Tale Terrains, Butterfly Puppet Set |
| Fairy Villages v3 | Pink Blossom House |

**Commit message**: `feat(editorial): cap.expanded for hero cards`

---

## Commit 9 — Per-section type personality

**Why**: Distinguish sections at the typographic level beyond just accent color.

**Where**: 4 section pages.

**Add** to the END of each file's `<style>` block (after all other rules):

**Sensory Play v1.html**:
```css
.split .content h3, .gallery h2, .intro h3 { letter-spacing: -.012em; }
.split .content .desc{ font-size: clamp(16px, 1.4vw, 18px); }
```

**Woodland v3.html**:
```css
.gallery { padding-top: clamp(80px, 9vw, 120px); padding-bottom: clamp(80px, 9vw, 120px); }
.split .content h3, .gallery h2, .intro h3 { font-weight: 400; letter-spacing: 0; }
.split .content { padding-top: clamp(72px, 9vw, 132px) !important; padding-bottom: clamp(72px, 9vw, 132px) !important; }
```

**Small World v2.html**:
```css
.gallery h2 .it, .split .content h3 .it, .intro h3 .it { font-weight: 500; }
.split .content .desc{ font-family: var(--serif); font-style: italic; font-weight: 300; font-size: clamp(17px, 1.5vw, 19px); line-height: 1.55; }
.gallery .home .name{ font-style: italic; font-weight: 400; }
```

**Fairy Villages v3.html**:
```css
.split .content h3, .gallery h2, .intro h3 { font-weight: 300; }
.gallery .home .cap .name{ font-weight: 400; }
.collection-bridge .bridge-cta{ border-radius: 999px; }
```

**Commit message**: `feat(typography): per-section type personalities`

---

## Verification after merge

After all 9 commits, run a quick visual smoke test on each page in browser:

1. ✅ Section pages: cover H1 doesn't overlap cover footer
2. ✅ Section pages: breadcrumb appears above the section stepper
3. ✅ Section pages: pull-quote appears between gallery and next section
4. ✅ Section pages: section divider with number renders cleanly
5. ✅ Section pages: hero card on each gallery shows the small accent rule
6. ✅ Auth-walled pages: `<meta name="robots" content="noindex,nofollow">` in head
7. ✅ All pages: footer reads "© 2026 My Toy Wagon · Educator Catalog · All rights reserved"

If any visual regression, the offending commit can be reverted individually without unwinding the others.

---

## What this does NOT touch

- Liquid asset paths (already correct in repo)
- Sensory Play section-numbering (already correct in repo)
- Nature Play catalog corrections (already correct in repo)
- Product names, prices, SKUs
- Page metadata (titles, descriptions, canonicals) — only adds robots meta
- The Shopify Liquid template wrappers
- Any product/collection metafield wiring

All 9 commits are scoped to **editorial design CSS and supporting markup**. Pricing, SKUs, and product data are untouched.
