# Handover — Educator Portal Build (Second Claude Code Session)

You are the **second Claude Code session** working on the My Toy Wagon Shopify build. Your scope is **the educator portal only**. The first Claude Code session is handling retail homepage, PDPs, catalog, policies, blog, and marketing pages. You will not touch those.

This document explains what to build, what's already in place, and where the two sessions need to coordinate.

---

## 1 — Read first

Open these three files in your project root before starting:

1. **`README.md`** — full design spec for the educator portal
2. **`SHOPIFY_NOTES.md`** — Shopify B2B implementation notes (Companies, Catalogs, Payment terms, draft orders, Customer Account UI Extensions)
3. **`IMAGES.md`** — how images and asset paths work (Shopify Files-based, `{{ FILES_BASE_URL }}` token pattern)

Then skim the eight design HTML files in `designs/` so you understand the visual target.

---

## 2 — Your scope

You are responsible for **everything an educator, school, therapist, or homeschool buyer touches.** That means:

### Pages to build
| Page | Source design | Shopify implementation |
|---|---|---|
| Schools landing | `designs/ordering-for-schools.html` | Liquid template at `/pages/schools` |
| Procurement guide | `designs/procurement-guide.html` | Liquid template `/pages/procurement-guide` + static PDF in Shopify Files |
| Catalog back matter (Chapters 6–9) | `designs/catalog-back-matter.html` | Final destination is the printed catalog PDF; web version lives at `/pages/educator-info` for QR code resolution |
| School Affiliate Program | `designs/school-affiliate.html` | Liquid `/pages/school-affiliate` |
| Vendor profile | `designs/vendor-profile.html` | Liquid `/pages/vendor-profile` |
| Educator apply / sign in | `designs/educator.html` | Customer Account UI Extension at `/account/educator-apply` |
| Educator dashboard | `designs/educator-dashboard.html` | Customer Account UI Extension at `/account/educator` |
| New quote builder | `designs/new-quote.html` | Customer Account UI Extension at `/account/quotes/new` |

### Shopify configuration
| Task | Reference |
|---|---|
| Enable B2B (Companies, Catalogs, Payment terms) | The store confirmed has access to B2B catalog |
| Create Catalogs (Educator Standard, Educator Tier 2 / Tier 3) | `SHOPIFY_NOTES.md` § Catalogs |
| Set up Net-30 and Net-60 payment terms templates | `SHOPIFY_NOTES.md` § Payment terms |
| Define metafield schemas on Company + Location + Customer | `SHOPIFY_NOTES.md` § Companies: data model |
| Set up URL redirects (`/educator` → portal, `/procurement-guide` → PDF) | `SHOPIFY_NOTES.md` § Pages and routes |
| Customize "Customer account invite" notification email (educator welcome) | Already designed — pull from prior session's notes |

### Workflows to wire
| Workflow | Reference |
|---|---|
| Educator application → Company creation via Flow | `SHOPIFY_NOTES.md` § Application form |
| Quote builder → Draft Order via Admin API | `SHOPIFY_NOTES.md` § Quote builder |
| Quote → PO → Order conversion (manual or Net-30 trusted auto) | `README.md` § Critical workflows / Workflow 2 |

---

## 3 — What you must NOT touch

The first Claude Code session owns these. Do not edit, override, or restyle:

- The main retail homepage (`/`)
- Retail product pages and the PDP template
- Retail collection pages
- Public catalog (`/pages/catalog`)
- Marketing pages: Our Story, Privacy, Terms, Returns, Shipping, FAQ, Accessibility, Collaboration, Wishlist, Rewards
- The retail blog
- The site header and footer (shared chrome)
- The retail brand tokens (cream / ink / forest / amber, Cormorant + Mulish, 2px radius)

You will inherit these as-is. If you need to extend them, **coordinate with the first session** rather than forking.

---

## 4 — Build sequence

Recommended four-week sequence. Adjust based on Shopify B2B feature availability.

### Week 1 — Shopify configuration
- Enable B2B if not already on
- Create Catalogs (Educator Standard at 15% off retail, plus tiered options)
- Set up Net-30 and Net-60 payment terms templates
- Define metafield schemas on Company / Location / Customer (`educator.account_type`, `educator.application_status`, etc. — see `SHOPIFY_NOTES.md`)
- Create URL redirects: `/educator` and `/procurement-guide`
- Customize the Customer Account Invite email template

### Week 2 — Public marketing pages
- Build Liquid templates for `/pages/schools`, `/pages/procurement-guide`, `/pages/vendor-profile`, `/pages/school-affiliate`
- Upload the procurement guide as a downloadable PDF in Shopify Files
- Set up the procurement guide QR codes to resolve to the correct URLs
- Test the vendor-form upload flow (Shopify Forms or Typeform → Drive + email to accounting@)

### Week 3 — Apply flow
- Build the educator application form (Shopify Forms or Tally embed) on `/pages/educator`
- Set up Shopify Flow workflow to create a Company + Location + Contact on submission
- Verify the Customer Account Invite email is sent post-approval
- Test the full path: anonymous visitor → applies → admin approves → customer receives welcome email → signs in → sees educator pricing

### Week 4–5 — Customer Account UI Extensions
- Build the dashboard extension (`/account/educator`)
- Build the new-quote extension (`/account/quotes/new`) with custom attributes on draft orders
- Wire the quote → draft order → review → PO → conversion flow
- Build the vendor profile gate (educator-verified only)
- End-to-end QA

---

## 5 — Shared chrome (inherit from first session)

The header and footer are shared between retail and educator pages. They render the same on every page. The first session's snippets to use:

- **Header**: `header-logo-snippet.html` (drop-in HTML + CSS + Liquid notes)
- **Footer**: `footer-snippet.html` (drop-in HTML + CSS + Liquid notes)
- **Announcement bar + free-shipping progress**: `announcement-bar-snippet.html`

When educators sign in, the **same header and footer** still render — but for signed-in educators, the cart and account icons show educator-specific state.

---

## 6 — Things the first session has already done

To avoid duplicate work, here's what's complete or in progress on the retail side:

- ✅ Brand tokens defined (`--cream`, `--ink`, `--forest`, `--amber`, etc.)
- ✅ Cormorant Garamond + Mulish typography stack established
- ✅ Logo lockup (Option B, ink color, wagon + Cormorant uppercase wordmark)
- ✅ Shopify Files images uploaded with descriptive filenames (`mytoywagon-logo-mark.png`, `product-tara-treasures-garden-of-the-moon-playscape.webp`, etc.)
- ✅ Customer account invite email template customized for educator welcome
- ✅ Top utility bar + free-shipping progress bar
- ✅ Site header and footer
- ✅ Cookie consent banner + "Do Not Sell or Share My Personal Information" footer link

These you inherit. Do not rebuild them.

---

## 7 — Open decisions to confirm with the founders before building

1. **Confirm B2B feature access in admin** — Companies, Catalogs, Payment terms should appear in the Shopify admin sidebar. If they don't, escalate.
2. **Calendly URL** for the "Schedule a 20-minute call" button on the educator dashboard. Currently `href="#"` placeholder.
3. **Educator pricing tiers** — confirm tier structure (Standard / Tier 2 / Tier 3) and percentages. Defaults in `SHOPIFY_NOTES.md`.
4. **Vendor form workflow** — does the file go to Google Drive, Dropbox, or just email to accounting@? Confirm.
5. **Sales rep assignment** — one person for all educators, or assigned per Company? Defaults to one inbox: `educators@mytoywagon.com`.
6. **First test customer** — identify one real educator (school, therapist, or homeschool co-op) to run end-to-end testing.
7. **Pre-order item handling for educators** — when an educator orders a pre-order item, does Net-30 trigger at order conversion or at shipment? (Recommend: shipment.)

---

## 8 — Coordination protocol with first Claude Code session

Two parallel sessions means stepping on each other's work is the main risk. Mitigations:

### File ownership

| First session owns | Second session (you) own |
|---|---|
| `sections/header.liquid` | `sections/footer.liquid` (no — both shared) |
| `sections/main-product.liquid` | `sections/main-product.liquid` (NO — first session) |
| All `templates/page.*.liquid` for marketing pages | `templates/page.schools.liquid` etc. (educator pages only) |
| `assets/theme.css` (or main stylesheet) | Append to it via a new `assets/educator.css` partial |
| `snippets/product-card.liquid` | DO NOT touch |
| `snippets/educator-*.liquid` | All snippets prefixed `educator-` belong to you |

**Rule of thumb:** if a file does not contain "educator," "school," "quote," "vendor," "procurement," or "affiliate" in its name, you don't touch it. If you need to add educator-specific behavior to a shared file, ask first.

### Customer Account UI Extensions
These are entirely yours. They live in `extensions/` and are namespaced by handle. Build under `extensions/educator-portal/`.

### Theme settings
Add educator-related theme settings under a new `educator` section in `config/settings_schema.json`. Don't touch existing sections.

### Communication
Use this handover doc as the canonical reference. If you make a decision that affects shared chrome, update this doc with a note for the first session.

---

## 9 — Acceptance criteria (end-to-end smoke test)

Before considering the educator portal done:

- [ ] Anonymous visitor lands on `/pages/schools` and sees the full marketing page
- [ ] They click "Apply for an account" → fill out the form → submit
- [ ] A new Company + Location + Contact is created in Shopify admin with `educator.application_status = "pending"`
- [ ] Internal team receives a notification email at `educators@mytoywagon.com`
- [ ] Staff manually approves → assigns Catalog + payment terms → flips to verified
- [ ] Customer receives the welcome email with the activate-account link
- [ ] Customer clicks → activates → signs in → lands on `/account/educator` (dashboard)
- [ ] Dashboard shows: greeting, account terms, pending quotes (zero), recent orders (zero), "How quotes become orders" explainer, sidebar nav
- [ ] Customer clicks "New quote" → searches products → sees educator pricing on every product → adds items → adds notes → submits
- [ ] Draft Order appears in Shopify admin with tags `educator-quote`, `pending-review` and custom attributes `quote_name`, `for_program`, `needed_by`
- [ ] Staff reviews, completes the draft → order is created with Net-30 terms
- [ ] Customer sees the order in their portal "Recent orders" list
- [ ] All emails route correctly (educators@, accounting@, contact@)
- [ ] Tax exemption applies for Locations with a tax-exempt certificate uploaded
- [ ] QR codes on printed catalog Chapter 6 resolve to the correct URLs
- [ ] Procurement guide PDF downloads cleanly from `/pages/procurement-guide`

---

## 10 — Files in this handover

```
design_handoff_educator_portal/
├── README.md               ← full design spec
├── SHOPIFY_NOTES.md        ← B2B implementation guide
├── IMAGES.md               ← asset path workflow
├── HANDOVER.md             ← this file (read first)
├── asset-rename-manifest.csv
├── path-replacement-guide.txt
└── designs/                ← the eight HTML reference files
    ├── educator.html
    ├── educator-dashboard.html
    ├── new-quote.html
    ├── vendor-profile.html
    ├── ordering-for-schools.html
    ├── catalog-back-matter.html
    ├── procurement-guide.html
    └── school-affiliate.html
```

---

## 11 — Start here

1. Read `README.md`, `SHOPIFY_NOTES.md`, `IMAGES.md`, and this file
2. Verify Shopify B2B access in admin (Companies + Catalogs visible in sidebar)
3. Confirm the 7 open decisions in Section 7 with Irfana and Rashid
4. Begin Week 1 Shopify configuration
5. Coordinate with the first Claude Code session before touching any file that isn't clearly educator-scoped

If any of this is unclear, ask before building.

*Last updated: May 15, 2026 — handover from designer to second Claude Code build session.*
