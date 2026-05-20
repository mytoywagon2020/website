#!/usr/bin/env python3
"""Transform educator catalog section design HTML into Shopify Page bodies.

Source: the owner's latest uploaded section designs (newest content: breadcrumb,
noindex, type refinements). We clean the surface artifacts those downloads
picked up (Cloudflare email obfuscation, relative asset paths) and rewrite for
Shopify: real CDN image URLs, /pages/ routes, inlined image-slot.js.

Output: shopify/pages/<handle>.html  (the body stored in the admin Page;
the educator-catalog template supplies the <head>/fonts chrome).
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path("/root/.claude/uploads/b9902c1c-5ab9-4f1b-a9b7-f21737e60693")
OUT = ROOT / "shopify" / "pages"

CDN = "https://cdn.shopify.com/s/files/1/0522/0882/8586/files"
ASSET_URLS = {
    "assets/mtw-logo-full.png": f"{CDN}/mtw-logo-full.png?v=1779249224",
    "assets/mtw-wagon-only.png": f"{CDN}/mtw-wagon-only.png?v=1779249224",
    "assets/folk-1.webp": f"{CDN}/folk-1.webp?v=1779249224",
    "assets/folk-2.webp": f"{CDN}/folk-2.webp?v=1779249224",
    "assets/folk-3.webp": f"{CDN}/folk-3.webp?v=1779249224",
    "assets/folk-4.webp": f"{CDN}/folk-4.webp?v=1779249224",
    "assets/lilac-blossom-house.jpg": f"{CDN}/lilac-blossom-house.jpg?v=1779249224",
    "assets/pink-blossom-house.webp": f"{CDN}/pink-blossom-house.webp?v=1779249224",
    "assets/mushroom-garden-set.png": f"{CDN}/mushroom-garden-set.png?v=1779249226",
    "assets/mushroom-garden-fairy-home.png": f"{CDN}/mushroom-garden-fairy-home.png?v=1779249226",
    "assets/toadstool-house-context.png": f"{CDN}/toadstool-house-context.png?v=1779249226",
    "assets/toadstool-house-alt.png": f"{CDN}/toadstool-house-alt.png?v=1779249226",
    "assets/ambrosius-gnome-family.webp": f"{CDN}/ambrosius-gnome-family.webp?v=1779249224",
    "assets/papoose-gnome-family.webp": f"{CDN}/papoose-gnome-family.webp?v=1779249224",
    "assets/wonderheart-group.webp": f"{CDN}/wonderheart-group.webp?v=1779249224",
    "assets/pink-flower-fairy-house.webp": f"{CDN}/pink-flower-fairy-house.webp?v=1779249224",
}

LINK_REPLACEMENTS = {
    'href="MTW Homepage v3.html"': 'href="/"',
    'href="educators.html"': 'href="/pages/educators"',
    'href="educator.html"': 'href="/pages/educator-program"',
    'href="educator-dashboard.html"': 'href="/pages/educator-dashboard"',
    'href="new-quote.html"': 'href="/pages/new-quote"',
    'href="sensory-play.html"': 'href="/pages/educator-sensory-play"',
    'href="nature-play.html"': 'href="/pages/educator-nature-play"',
    'href="woodland.html"': 'href="/pages/educator-woodland"',
    'href="small-world.html"': 'href="/pages/educator-small-world"',
    'href="fairy-villages.html"': 'href="/pages/educator-fairy-villages"',
    'href="steam.html"': 'href="/pages/educator-steam"',
    'href="dramatic-play.html"': 'href="/pages/educator-dramatic-play"',
    'href="creative-arts.html"': 'href="/pages/educator-creative-arts"',
    'href="vendor-profile.html"': 'href="/pages/vendor-profile"',
    'href="procurement-guide.html"': 'href="/pages/procurement-guide"',
    'href="ordering-for-schools.html"': 'href="/pages/schools"',
    'href="school-affiliate.html"': 'href="/pages/school-affiliate"',
    'href="Woodland v3.html"': 'href="/pages/educator-woodland"',
    'href="Small World v2.html"': 'href="/pages/educator-small-world"',
    'href="Sensory Play v1.html"': 'href="/pages/educator-sensory-play"',
    'href="Nature Play v1.html"': 'href="/pages/educator-nature-play"',
    'href="Fairy Villages v3.html"': 'href="/pages/educator-fairy-villages"',
}

EMAIL = "educators@mytoywagon.com"

# upload filename, output handle, page title, per-page extra replacements
JOBS = [
    ("dac6ae27-Fairy_Villages_v3.html", "educator-fairy-villages", "Fairy Villages", []),
    ("4f15d3b3-Sensory_Play_v1_3.html", "educator-sensory-play", "Sensory Play",
        [('small-world.html">04 &middot; Sensory Play', 'small-world.html">04 &middot; Small World &amp; Storytelling')]),
    ("2d1d2b5a-Nature_Play_v1_1.html", "educator-nature-play", "Nature Play", []),
    ("4a5e7892-Woodland_v3.html", "educator-woodland", "Woodland Habitats", []),
    ("b3d33b94-Small_World_v2.html", "educator-small-world", "Small World & Storytelling", []),
]


def transform(src_html: str, extra) -> str:
    # Apply per-page fixes BEFORE link rewrites (anchors use raw .html links).
    for old, new in extra:
        if old not in src_html:
            raise ValueError(f"per-page anchor not found: {old[:50]!r}")
        src_html = src_html.replace(old, new)

    style = re.search(r"<style>.*?</style>", src_html, re.S)
    body = re.search(r"<body[^>]*>(.*?)</body>", src_html, re.S)
    if not style or not body:
        raise ValueError("could not locate <style> or <body>")
    out = style.group(0) + "\n" + body.group(1).strip() + "\n"

    # Drop Cloudflare email-decode script.
    out = re.sub(r'<script[^>]*email-decode\.min\.js[^>]*></script>', '', out)
    # Restore obfuscated emails.
    out = re.sub(r'href="/cdn-cgi/l/email-protection[^"]*"', f'href="mailto:{EMAIL}"', out)
    out = re.sub(r'<span[^>]*__cf_email__[^>]*>\[email&#160;protected\]</span>', EMAIL, out)
    out = re.sub(r'<span[^>]*__cf_email__[^>]*>.*?</span>', EMAIL, out)
    out = out.replace('[email&#160;protected]', EMAIL).replace('[email protected]', EMAIL)

    # Asset paths -> CDN.
    for rel, url in ASSET_URLS.items():
        out = out.replace(rel, url)
    # Local links -> routes.
    for old, new in LINK_REPLACEMENTS.items():
        out = out.replace(old, new)
    # Remove image-slot.js (a localStorage preview-editor, not for live pages).
    out = re.sub(r'<script[^>]*src="image-slot\.js"[^>]*></script>', '', out)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for src_name, handle, title, extra in JOBS:
        src = (SRC / src_name).read_text(encoding="utf-8")
        body = transform(src, extra)
        (OUT / f"{handle}.html").write_text(body, encoding="utf-8")
        checks = {
            "cf_junk": ("cdn-cgi/l/email-protection" in body) or ("email-decode" in body),
            "rel_assets": bool(re.search(r'(src|href)="assets/', body)),
            "local_html_link": bool(re.search(r'href="[^"/#:]+\.html"', body)),
            "image_slot_ref": "image-slot.js" in body,
        }
        print(f"{handle}: {len(body)} bytes  {checks}")


if __name__ == "__main__":
    main()
