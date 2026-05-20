# My Toy Wagon — Brand & Voice Guide

> Canonical rules for all customer-facing copy and design on the My Toy Wagon
> site (retail + educator portal). This file is the durable "training": any
> session, any instance, should read it before writing copy or building pages.
> If something here conflicts with a one-off instruction, follow the live
> instruction and update this file.

---

## 1. Who we are

- **My Toy Wagon (MTW)** — a small family shop selling natural, heirloom-quality
  toys. Based in Los Angeles (Arcadia, CA). Online since **2020**.
- **Founders:** Irfana and Rashid. Replies to educators come from a real person
  on a small team, never a bot or ticket queue.
- **Mission / north star:** become **the go-to for felt and wood.**
- **Audience:** parents buying for home, and educators/schools buying for
  classrooms (Pre-K through early grades). The educator portal is the
  school-buyer surface.

### Public contact (footer / educator pages)
- Educators: `educators@mytoywagon.com`
- Accounting: `accounting@mytoywagon.com`
- Phone: (626) 841-0421 · Mon to Fri, 9 am to 5 pm PT
- Address: 37 W Huntington Drive, Arcadia, CA 91007

---

## 2. Voice — hard rules (do not break)

These are non-negotiable. They exist because the brand reads as calm, honest,
and editorial — not salesy.

1. **No em-dashes in customer-facing copy.** Use commas, periods, or restructure
   the sentence. (Internal docs like this one may use them.)
2. **No exclamation marks in body copy.** The tone is quiet and confident.
3. **Never invent facts.** No made-up certifications, materials, origins,
   awards, ages, dimensions, or **prices**. If the catalog doesn't state it,
   it does not go on the page.
4. **The catalog is the source of truth.** All product names, descriptions,
   SKUs, set names, scenarios, testimonials, and pull-quotes come from
   `shopify/educator-portal/CATALOG_SOURCE_v22r23.html`. Do not paraphrase facts
   into something the catalog doesn't support.
5. **No prices unless they exist in the catalog.** Several sections (e.g. Nature
   Play) have SKUs but no prices. Those stay quote-only ("Request a quote"),
   never placeholder or invented numbers.
6. **Don't duplicate cross-listed products.** Items the catalog cross-lists into
   another section (e.g. Análu Therapy Dough and Tender Leaf My Forest Floor in
   §01 Sensory) are flagged in an HTML comment, not re-sold in two places.

### Tone qualities
- Calm, warm, editorial, specific. Concrete classroom scenarios over hype.
- "Slow goods, on purpose." Craft, provenance, and longevity over novelty.
- Sentences are plain and declarative. Serif italic is used for emphasis moments,
  not for shouting.

---

## 3. Design system (the "chassis")

Shared across the site; per-section accents layer on top.

### Type
- **Headings:** Cormorant Garamond (weights 300, 400, 500, 600).
- **Body:** Mulish (weights 300–700).
- **Hierarchy:** h1 `clamp(56px, 8vw, 112px)` italic · h2 `clamp(40px, 5vw, 60px)`
  · h3 `clamp(32px, 4vw, 52px)`. Body 17px / 1.55 line-height.
- **Letter-spacing:** -0.014em on h1, -0.008em on h2/h3.

### Brand color tokens (chassis — do not vary)
```css
--cream:      #F5F0E5;  /* neutral-warm canvas */
--warm-white: #FFFCF7;  /* card surface over cream */
--card-bg:    #EDE3CD;  /* warm beige card surface */
--ink:        #2C2C2A;  /* primary text */
--ink-soft:   #44423E;  /* body text */
--stone:      #5F5E5A;  /* muted grey */
--forest:     #3B6D11;  /* brand primary accent (micro use) */
--amber:      #854F0B;  /* brand secondary accent (wagon badge) */
```

### PDP 4-tone canvas
The product page uses a deliberately layered, **darker-to-lighter** tone system,
not a flat cream. Tones: `#E4DCC9` (darkest canvas) / `#F5F0E5` / `#FFFCF7` /
`#EDE3CD`. Do not flatten this to a single light color.

### Per-section accent palette (educator catalog)
| § | Section | Accent | Hex |
|---|---|---|---|
| 01 | Sensory Play | teal-green | `#3D7A6A` |
| 02 | Nature Play | sage | `#6B8C3A` |
| 03 | Woodland Habitats | forest | `#2D5C3A` |
| 04 | Small World & Storytelling | plum | `#7A5C8A` |
| 05 | Fairy Villages | rose | `#B86A7E` |
| 06 | STEAM, Wonder & Investigation | amber | `#9B7A3F` |
| 07 | Dramatic Play | tan | `#8B6840` |
| 08 | Creative Arts | teal-slate | `#436F6F` |

Each section also gets a subtle type "personality" (tracking/weight tweak) on
top of the accent — distinct voice without breaking the chassis.

---

## 4. SKU convention

```
MTW-[SECTION]-[PRODUCT]
```
Section codes: `SP` Sensory · `NP`/`NT` Nature Play · `WD` Woodland · `SW` Small
World · `FV` Fairy Villages · `ST` STEAM · `DP` Dramatic Play · `CA` Creative
Arts. Always copy SKUs verbatim from the catalog (some are cross-listed under a
different brand's section code — keep them as written and note in a comment).

---

## 5. Working rules (how to build, not just what to write)

- **Do NOT delegate this work to subagents.** Owner's standing instruction: build
  it directly, do not spawn agents for educator/site tasks.
- **Be honest about verification.** There is no browser to render in this
  environment. Don't claim a page "looks right" — say what was changed and what
  still needs visual QA at desktop + mobile.
- **Verify against the catalog before replicating.** When cloning a section page,
  re-check every fact against the catalog source rather than carrying over the
  previous section's facts (origins, materials, brands differ by section).
- **Mirror everything to git** and push to the working branch. The cloud
  container is ephemeral; only committed/pushed work survives.

---

## 6. Source-of-truth files
- Product facts: `shopify/educator-portal/CATALOG_SOURCE_v22r23.html`
- Educator portal structure & build process: `shopify/educator-portal/CLAUDE_CODE_HANDOVER.md`
- Theme / deploy state & constraints: `SESSION-HANDOVER.md`, `SHOPIFY_NOTES.md`
