#!/usr/bin/env python3
"""Transform educator-portal design HTML into Shopify Page bodies.

Output goes to shopify/pages/<handle>.html. Each body is the design's
<style> block plus its <body> inner markup, with the FILES_BASE_URL
image token and local .html links rewritten to live Shopify routes.
The body is stored in the Shopify admin Page (theme-update resilient);
the theme only supplies the generic page.educator-portal template.
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESIGNS = ROOT / "designs"
OUT = ROOT / "shopify" / "pages"

LOGO_URL = "https://cdn.shopify.com/s/files/1/0522/0882/8586/files/mytoywagon-logo-mark.png?v=1778880482"
SPECIMEN_URL = "https://cdn.shopify.com/s/files/1/0522/0882/8586/files/schools-cinematic-specimen-cabinet.webp?v=1778880669"

# Image token -> real Shopify Files CDN URL
IMAGE_REPLACEMENTS = {
    "{{ FILES_BASE_URL }}/logo-mark.png": LOGO_URL,
    "{{ FILES_BASE_URL }}/procurement-specimen-cabinet.webp": SPECIMEN_URL,
}

# Local design link -> live Shopify route
LINK_REPLACEMENTS = {
    'href="MTW Homepage v3.html"': 'href="/"',
    'href="catalog.html"': 'href="/pages/catalog"',
    'href="educator.html"': 'href="/pages/educator-program"',
    'href="vendor-profile.html"': 'href="/pages/vendor-profile"',
    'href="collaboration.html"': 'href="/pages/collaboration"',
    'href="terms.html"': 'href="/pages/terms-of-service"',
    'href="privacy.html"': 'href="/pages/privacy-policy"',
    'href="ordering-for-schools.html"': 'href="/pages/schools"',
}

# Page-specific fixes applied after the generic passes. The procurement
# guide is a live printable page (not yet a static PDF), so its dead
# placeholder links resolve to that page instead.
PER_PAGE_REPLACEMENTS = {
    "schools": [
        ('<a href="#" class="btn btn-primary">\n          <svg width="16" height="16" viewBox="0 0 24 24"',
         '<a href="/pages/procurement-guide" class="btn btn-primary">\n          <svg width="16" height="16" viewBox="0 0 24 24"'),
        ('<h4>Procurement guide</h4>\n        <p>Full guide for schools, 5 pages</p>\n      </div>\n      <div class="resource-actions">\n        <a href="#" class="action-btn primary">Download PDF</a>',
         '<h4>Procurement guide</h4>\n        <p>Full guide for schools, 5 pages</p>\n      </div>\n      <div class="resource-actions">\n        <a href="/pages/procurement-guide" class="action-btn primary">View / print</a>'),
    ],
}

PAGES = [
    ("ordering-for-schools.html", "schools"),
    ("procurement-guide.html", "procurement-guide"),
    ("vendor-profile.html", "vendor-profile"),
]


def transform(src_html: str, handle: str) -> str:
    style = re.search(r"<style>.*?</style>", src_html, re.S)
    body = re.search(r"<body[^>]*>(.*?)</body>", src_html, re.S)
    if not style or not body:
        raise ValueError("could not locate <style> or <body>")
    out = style.group(0) + "\n" + body.group(1).strip() + "\n"
    for token, url in IMAGE_REPLACEMENTS.items():
        out = out.replace(token, url)
    for old, new in LINK_REPLACEMENTS.items():
        out = out.replace(old, new)
    for old, new in PER_PAGE_REPLACEMENTS.get(handle, []):
        if old not in out:
            raise ValueError(f"{handle}: per-page anchor not found: {old[:60]!r}")
        out = out.replace(old, new)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for src_name, handle in PAGES:
        src = (DESIGNS / src_name).read_text(encoding="utf-8")
        body = transform(src, handle)
        dest = OUT / f"{handle}.html"
        dest.write_text(body, encoding="utf-8")
        leftover_token = "{{ FILES_BASE_URL }}" in body
        leftover_local = bool(re.search(r'href="[^"/#:]+\.html"', body))
        print(f"{handle}: {len(body)} bytes  "
              f"token_left={leftover_token}  local_link_left={leftover_local}")


if __name__ == "__main__":
    main()
