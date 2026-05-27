# Helium Customer Fields — tax-exempt cert upload form config

What to set up in **Helium Customer Fields admin** to make the tax-exempt upload page (`/pages/tax-exempt-upload`) work end-to-end.

The template is already pushed and live on staging. It includes a placeholder `<div id="helium-tax-exempt-form">` that Helium will render the form inside, plus an email fallback so the page works even before Helium is configured.

---

## Step 1 — Create the metafield definitions (one-time)

In **Shopify admin → Settings → Custom data → Customers → Add definition** (do this 5 times):

| # | Namespace | Key | Name (display) | Type | Pinned |
|---|---|---|---|---|---|
| 1 | `educator` | `tax_exempt_cert_url` | Tax-exempt cert (file) | URL or `file_reference` | Yes |
| 2 | `educator` | `tax_exempt_state` | Tax-exempt issuing state | Single line text | Yes |
| 3 | `educator` | `tax_exempt_type` | Tax-exempt cert type | Single line text | Yes |
| 4 | `educator` | `tax_exempt_effective` | Tax-exempt effective date | Date | Yes |
| 5 | `educator` | `tax_exempt_expires` | Tax-exempt expiration date | Date | Yes |

If any are blocked by Shopify Admin API permissions, create them manually in admin UI as the owner.

---

## Step 2 — Create the Helium form

Open **Helium Customer Fields** app in Shopify admin → **Forms** → **Create form**.

| Setting | Value |
|---|---|
| Form name (internal) | `tax-exempt-upload` |
| Form title (shown to customer) | Tax-Exempt Certificate Upload |
| Form type | Custom form (post-login) |
| Visible to | Logged-in customers only (Helium will check session) |

---

## Step 3 — Add fields (six total)

### Field 1 — Issuing state
- Type: **Dropdown**
- Label: *"Issuing state"*
- Required: Yes
- Options: all 50 US states + DC
- Bind to metafield: `customer.educator.tax_exempt_state`

### Field 2 — Certificate type
- Type: **Dropdown**
- Label: *"Certificate type"*
- Required: Yes
- Options:
  - `school` → School district / public school
  - `library` → Public library
  - `501c3` → 501(c)(3) nonprofit
  - `government` → Government entity
- Bind to metafield: `customer.educator.tax_exempt_type`

### Field 3 — Effective date
- Type: **Date**
- Label: *"Effective date"*
- Required: Yes
- Bind to metafield: `customer.educator.tax_exempt_effective`

### Field 4 — Expiration date
- Type: **Date**
- Label: *"Expiration date (if any)"*
- Required: No
- Bind to metafield: `customer.educator.tax_exempt_expires`

### Field 5 — Certificate file
- Type: **File upload**
- Label: *"Upload your certificate (PDF, JPG, or PNG)"*
- Required: Yes
- Accept: `.pdf, .jpg, .jpeg, .png`
- Max size: 10 MB
- Upload destination: Shopify Files (Helium default)
- Bind to metafield: `customer.educator.tax_exempt_cert_url` (URL returned by Shopify Files)

### Field 6 — Notes (optional)
- Type: **Textarea**
- Label: *"Anything we should know about this certificate?"*
- Required: No
- Bind to: Customer note (or skip if you prefer)

---

## Step 4 — On-submit actions

In Helium form settings → **Actions**:

1. **Add customer tag**: `tax-exempt-pending`
2. **Success message** (shown after submit):
   ```
   Thanks. We received your certificate. Our team verifies within 1–2 business days
   and will email you to confirm. You can come back to this page anytime to update.
   ```
3. **Optional — fire Klaviyo event**: `Tax exempt cert uploaded`
   - Event properties: customer_email, state, cert_type, effective_date, expires_date, cert_url

---

## Step 5 — Bind form to the page

In Helium form → **Embed mode** → **Custom container**:
- Target selector: `#helium-tax-exempt-form`
- Click "Generate embed code" if Helium asks

The template already has `<div id="helium-tax-exempt-form">` — Helium will replace its placeholder content with the rendered form when the page loads.

---

## Step 6 — Enable the Helium app embed in your live theme

Online Store → Themes → Customize live theme → **App embeds** (left sidebar near the bottom) → toggle on **Helium Customer Fields**. Save.

This makes Helium's JavaScript load on every page, which it needs in order to detect and replace the `#helium-tax-exempt-form` container.

---

## Step 7 — Test the flow

1. Sign in as a customer with the `educator-approved` tag
2. Go to `/pages/tax-exempt-upload`
3. Confirm the Helium form appears in place of the dashed placeholder box
4. Submit a test cert (use a sample PDF)
5. Confirm:
   - File appears in Shopify admin → Settings → Files
   - Customer record now has `tax-exempt-pending` tag
   - Metafields populated correctly on customer profile
   - Success message displayed
6. Test the email fallback path: send a test email to `accounting@mytoywagon.com` and confirm receipt

---

## Step 8 — Staff verification SOP (after submission)

When a `tax-exempt-pending` customer appears in your daily check:

1. Open the customer record → view `educator.tax_exempt_cert_url` → download the PDF
2. **Verify**:
   - Cert state matches the customer's ship-to state (e.g., California cert, California ship-to)
   - Cert is current (effective date in the past, expiration date in the future)
   - Cert covers our product category (classroom-use, not "resale")
   - Organization name matches the customer's institution
3. **If valid:**
   - Add tag: `tax-exempt-verified`
   - Remove tag: `tax-exempt-pending`
   - Go to Customer → Tax settings → add a tax exemption for the relevant state(s)
   - Save the cert PDF to your secure file system (suggested: `MTW/Educator certs/[Year]/[Customer name].pdf`)
   - Email the customer: *"Your tax-exempt status is active. Future orders will be tax-free at checkout."*
4. **If invalid:**
   - Leave the `tax-exempt-pending` tag in place
   - Email the customer with the specific reason (expired, wrong state, wrong category, organization mismatch)
   - Ask for an updated cert; do NOT add the `tax-exempt-verified` tag

---

## Step 9 — Expiration reminder flow (Klaviyo)

After Helium populates `customer.educator.tax_exempt_expires`, set up a Klaviyo flow:

- **Trigger**: scheduled daily check
- **Filter**: customer where `educator.tax_exempt_expires` is within 30 days from today
- **Action**: send email *"Your tax-exempt certificate expires in 30 days. Please upload a renewed certificate at [link to /pages/tax-exempt-upload]."*
- **Suppress**: don't re-send if already sent in the last 7 days

---

## Cross-reference

- Template file: `templates/page.tax-exempt-upload.liquid`
- Page URL once you create the page record: `/pages/tax-exempt-upload`
- Page is gated to `educator-approved` customers — non-approved visitors see the educator gate
- Email fallback always works (mailto:accounting@) even before Helium is configured
