# Launch Ops SOP — Educator Portal

**Read this before approving educators or replying to quotes.** Covers the four operational flows that aren't fully automated yet: B2B Company creation, tax-exempt cert handling, the educator welcome/approval email flow (Klaviyo), and the staff workflow for activating a quote's "Awaiting PO" state on the dashboard.

This sits next to `EDUCATOR-PORTAL-RUNBOOK.md`. The runbook covers the system architecture; this covers the human steps.

---

## 1. When to create a B2B Company for an educator

**Default: don't.** Most approved educators pay by card / Shop Pay / Apple Pay / ACH at checkout. The `educator-approved` tag is all they need to see educator pricing and submit quotes. A Company record is only required when they need **Net-30 / Net-60 terms on a Purchase Order**.

### Trigger — create a Company when ANY of these is true

- The educator's quote reply or PO request says any of: "pay by PO", "Net-30 required", "Net-60", "AP department needs to invoice us"
- The quote total is **$500+** and they ask for terms
- The institution is a school district or government entity (they almost always require PO)
- It's a recurring buyer who's previously paid by PO (set them up once, reuse)

### Step-by-step (~3 minutes per Company)

1. **Shopify admin → Customers → Companies → Create company**
2. **Company name** = institution legal name (e.g. "Bright Beginnings Elementary" or "Elk Grove USD")
3. **Locations** → add at least one
   - Billing-to address (where invoices go)
   - For districts: add each school as a separate location
4. **Contacts** → "Add existing customer" → search the educator's email → link as the primary contact
5. **Payment terms** → assign template
   - Default: **Net-30** (`PaymentTermsTemplate/4`)
   - For >$2k orders or proven districts: **Net-60**
6. **Catalog** → confirm "Educators Market" is the assigned catalog (this should default automatically — verify)
7. **Save**

### Effect downstream — verify these landed

- Customer record now shows `b2b = true` (visible in Customer detail)
- Educator's dashboard subtitle now reads "**Net-30 / Net-60 on file**" (was "Approved educator" only)
- Quote form pre-fills "School / organization" from `customer.current_company.name`
- At checkout, educator can choose "Bill via PO" with the assigned terms

---

## 2. Tax-exempt purchasing — how to collect, store, apply

Schools, libraries, 501(c)(3) organizations, and government entities don't pay sales tax. We need to verify their exemption status before applying it at checkout.

### Collection — where the certificate comes from

- **Pre-launch:** ask during the educator application (Helium form has an optional cert upload field)
- **Post-application:** the educator emails their state-issued exemption certificate to `accounting@mytoywagon.com` (the vendor-profile page directs them here)
- **At first PO:** if they didn't send one earlier, ask before processing the order

### Verification — what makes a cert valid

| Item | Why it matters |
|---|---|
| Issuing state matches the ship-to state | Tax exemption is state-by-state — a CA cert doesn't exempt OR sales tax |
| Effective date current (not expired) | Most expire annually or every 3-5 years; reject expired |
| Organization name matches the Customer's institution | The cert must be for THIS buyer, not their parent district unless they're the same legal entity |
| Cert type allows our product category | "Resale" certs do NOT apply to schools buying for classroom use (different cert) |

### Storage

1. Save the PDF to a folder per customer in your secure file system
   - Suggested path: `MTW/Educator certs/[Year]/[Customer name].pdf`
2. Note the expiration date in the Customer's "Notes" field in Shopify admin
3. Tag the customer with `tax-exempt-verified` so staff can filter at-a-glance

### Application at checkout

Shopify-native path (B2B customers only):

1. In Shopify admin → Customers → [customer] → **Tax settings**
2. Add a **tax exemption** for the relevant state(s)
3. At checkout (or when staff creates the draft order), Shopify auto-removes sales tax for that state's orders

For non-B2B approved educators ordering by card / Shop Pay:

- Apply the exemption at the **order level** in admin: open the order → "Edit shipping & taxes" → "Remove taxes"
- Or do it before they check out by creating a draft order on their behalf

### When to reject

- Cert is expired
- Cert is from a state different from ship-to (ask them to send the right one)
- Cert is for a different entity (e.g. they're trying to use the district's cert for a personal classroom purchase)
- They claim exempt but can't produce a cert within 7 business days — proceed with tax collected; refund the tax line if cert arrives later

---

## 3. Educator welcome + approval Klaviyo flow (to build)

Right now: no automatic emails fire when an educator applies or gets approved. The educator submits the Helium application, gets nothing back, and waits for staff to manually approve. That's the most common conversion-loss moment in the funnel.

**The flow to build in Klaviyo** (two triggers, three emails):

### Trigger 1 — Educator applies (Helium form submission)

When the Helium form writes to Shopify, the customer record gets a `educator-pending` tag (or list membership, depending on Helium config).

**Email A — "Application received"** (sent immediately)
- Subject: "We received your educator application, [first_name]"
- Body: "Thanks for applying for educator access at My Toy Wagon. Our team reviews each application within **one to two business days**. Most are approved on the same day they come in. We'll email you the moment your access is activated."
- CTA: "Browse the public shop while you wait →" (link to /collections/educator-favorites or similar)
- Footer: "Questions? Reply to this email or call (626) 841-0421."

### Trigger 2 — Educator approved (customer tag added: `educator-approved`)

When staff adds the `educator-approved` tag, fire:

**Email B — "Your educator access is live"** (sent immediately on tag add)
- Subject: "Your educator access is live, [first_name]."
- Body: "Welcome. Your educator account is active — sign in to browse the catalog, build a quote, and submit a PO when you're ready. Quotes are non-binding; nothing's reserved until you confirm."
- CTA: "Sign in to your dashboard →" (link to /pages/educator-dashboard)
- Secondary: "Email your tax-exempt cert to accounting@mytoywagon.com so we can set you up for tax-free purchasing."

**Email C — Day 7 follow-up if no engagement** (sent 7 days after approval, only if customer hasn't placed an order or submitted a quote)
- Subject: "Anything we can help you find, [first_name]?"
- Body: "Wanted to check in. If you're shopping for a specific classroom or grant deadline, we can pull a quote in under a day. Just reply with what you're after."
- CTA: "Reply with what you need"

### Build steps in Klaviyo

1. **Flow A** — trigger: "List membership: Educators Pending" (or "Property: educator_application_submitted = true")
   - Action: Send Email A immediately
   - Exit condition: customer tagged `educator-approved` OR `educator-rejected`

2. **Flow B** — trigger: "Customer property change: tags contains `educator-approved`"
   - Action: Send Email B immediately
   - Time delay: 7 days
   - Conditional split: "Has placed order OR submitted quote in last 7 days?" → if no, send Email C

3. **Templates** — build all three using Klaviyo's DND editor (matching the visual style of the existing Welcome Series). Each template should reference `event.organization_name` if pulled from the Helium application.

---

## 4. Activating the "Awaiting PO" wagon state on the dashboard

The dashboard has three wagon-card states (Empty / Draft / Awaiting PO). The Awaiting-PO state appears when `customer.metafields.educator.open_quote_id` is set on the customer record. Currently this is set in two ways:

1. **Automatically (immediate, JS-only):** When the educator submits the quote form, the dashboard's localStorage fallback fires within seconds. Educator sees Awaiting-PO state on their next dashboard visit. This is the fast path that already works.

2. **Manually by staff (durable, server-rendered):** When staff replies to the quote email, they should also set the `educator.open_quote_id` metafield on the customer's record. This makes the Awaiting-PO state survive across browsers/devices for that customer (localStorage is browser-specific).

### Staff workflow when responding to a quote

1. Read the incoming `Educator quote request` email (forwarded from contact form to `educators@`)
2. Build the formal quote (PDF or in-email itemized estimate) with educator pricing, shipping, tax, total
3. Email the educator back with the quote, including the generated Quote ID from the email header (Q-YYYYMMDD-XXXX format)
4. **In Shopify admin:**
   - Open the educator's customer record
   - Scroll to Metafields → "Educator · Open quote ID"
   - Paste the Q-YYYYMMDD-XXXX from your reply
   - Save
5. The educator's dashboard now displays the Awaiting-PO state with this quote ID, regardless of which browser they use

### Clearing the open quote ID

When the PO is confirmed and the order is created in Shopify:

1. Open the customer record → Metafields → "Educator · Open quote ID"
2. Clear the value (set to empty string)
3. Save
4. The dashboard's wagon-card returns to its appropriate state (empty if cart is empty, draft if they've started a new wagon)

---

## 5. Updating season copy

The dashboard's order-by date and delivery window come from a metaobject. Update each season before the date passes.

**Admin → Settings → Custom data → Metaobjects → "Educator delivery windows" → "default"**

Fields:
- `fall_window` → "August–September"
- `fall_order_by` → e.g. "July 15"
- `spring_window` → "May–June"
- `spring_order_by` → e.g. "March 15"

The dashboard switches automatically between fall (current year, shown Jan–Jun) and spring (next year, shown Jul–Dec).

---

## Maintenance schedule

| Cadence | Action |
|---|---|
| **Each new educator approval** | Add `educator-approved` tag (triggers Klaviyo Email B) · log institution in spreadsheet |
| **Each new quote** | Reply within 1 business day · set `educator.open_quote_id` metafield · move tag to `quote-pending` if you use that |
| **Each new PO** | Clear `open_quote_id` · move to `po-confirmed` · create order |
| **Each new Net-30 customer** | Follow Section 1 — create Company record |
| **Each tax-exempt cert** | Save PDF · tag customer · add to Tax settings · note expiration |
| **Twice yearly (June + Dec)** | Update season metaobject for upcoming season |
| **Quarterly** | Audit Companies for stale terms, tax-exempt certs nearing expiration |
