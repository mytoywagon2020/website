# Retail footer "For educators" snippet

A four-link group to add to your **retail** theme's footer. This is what bridges public retail traffic into the educator portal funnel.

## What to add to your retail footer

A new column / link group titled **"For educators"** with four links:

```html
<div class="footer-block footer-block--for-educators">
  <h3 class="footer-heading">For educators</h3>
  <ul class="footer-list">
    <li><a href="/pages/educator-program">Apply for an educator account</a></li>
    <li><a href="/pages/funding-your-classroom">Funding your classroom</a></li>
    <li><a href="/pages/vendor-profile">Vendor profile</a></li>
    <li><a href="mailto:accounting@mytoywagon.com">Contact accounts payable</a></li>
  </ul>
</div>
```

> Match the `footer-block`, `footer-heading`, and `footer-list` class names to whatever your retail theme uses. The actual class names will be visible if you inspect any existing footer column.

## Why each link

| Link | Why it's there |
|---|---|
| Apply for an educator account | Conversion CTA — for teachers ready to sign up now |
| Funding your classroom | Top-of-funnel asset — for teachers still researching how to pay |
| Vendor profile | For school AP departments verifying us as a vendor |
| Contact accounts payable | Direct line for grant officers and procurement teams |

## Where in the footer

Best placement: a **third column** in your existing footer grid (alongside your existing "Shop" and "Support" or equivalent columns). If your retail footer is single-column, add it as a section below your main links.

## SEO benefit (the actual reason for this)

Linking these four educator pages from the retail homepage footer:

1. **Tells Google these pages are first-class assets.** Pages with sitewide footer links inherit some of the retail home page's authority.
2. **Helps Google crawl + index them.** The funding page especially needs to be crawled to start ranking for "fund classroom materials," "Title I classroom supplies," "DonorsChoose Montessori," etc.
3. **Creates internal-link signal.** Three or four hub-and-spoke links in a footer is a standard SEO move that costs nothing and compounds over months.

## Optional: also add to retail header nav

If your retail header has room, add **"For educators →"** as a single link. Goes to `/pages/educator-program`. This is the "I came here as a teacher" express lane. Even higher impact than the footer link because top-nav placement signals importance to both users AND Google.

## How to actually paste this in your retail theme

1. Online Store → Themes → Live theme → Customize → Footer section (settings panel)
   - If your theme supports custom footer blocks via the theme editor, add a new column with the link group above.
2. OR: Online Store → Themes → Live theme → Edit code → find your footer.liquid (usually `sections/footer.liquid` or `snippets/footer.liquid`)
   - Add the HTML block in the appropriate footer-columns area
   - Save → preview → confirm the new column appears
3. **Verify links work** by clicking each — they should resolve to live pages (the funding page lands after you've created its page record in admin).
