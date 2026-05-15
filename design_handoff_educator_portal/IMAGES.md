# Images and Asset Paths

## How this bundle handles images

The design HTML files in `designs/` reference images using a token: `{{ FILES_BASE_URL }}/filename.ext`

**You will replace `{{ FILES_BASE_URL }}` with your real Shopify Files CDN base URL** before deploying:

- During local development: `{{ FILES_BASE_URL }}` = `https://mytoywagon.com/cdn/shop/files` (after upload)
- Or use Liquid: `{{ 'filename.ext' | file_url }}` in your final theme code

## The asset workflow

1. **All photography lives in Shopify Files** (Settings → Files in admin). Upload everything there once.
2. Use the `asset-rename-manifest.csv` to rename files before upload so each filename describes its product/role (e.g. `product-tara-treasures-garden-of-the-moon-playscape.webp` instead of `garden-of-the-moon.webp`).
3. Once images are in Shopify Files, copy the CDN URLs and replace `{{ FILES_BASE_URL }}/filename.ext` in the design files.

## Files included

- `asset-rename-manifest.csv` — Original filename → Shopify Files filename → Description. 100+ entries.
- `path-replacement-guide.txt` — Direct find/replace lookup for the HTML files.

## Why this bundle has no `assets/` folder

The original design HTML used local relative paths (`assets/garden-of-the-moon.webp`). For Shopify production, images must live in Shopify Files, not in the theme. This bundle strips the local assets folder and replaces every path with a portable token so your developer (or Claude Code) can wire to real CDN paths in one find-and-replace pass.

## Bonus: the original images

If you need the original images for reference (to upload to Shopify Files), they live in the project at `assets/` and `assets/blog/`. Ask Irfana/Rashid for a separate download of just the image library.
