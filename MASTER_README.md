# Master README — My Toy Wagon Website / Educator Portal

> Operational guide to this repo, the Shopify store, the Git→Shopify
> pipeline, and the gotchas we keep rediscovering. Read this first when
> picking up work — it exists so you don't have to re-learn the setup
> every session.
>
> Last updated: 2026-05-28

---

## 1. What this repo is

- **GitHub repo:** `mytoywagon2020/website`
- **Shopify store:** My Toy Wagon — `mytoywagon.com` (Shopify plan, USD, timezone PDT)
- The repo holds the Shopify **theme** (on the `staging-theme` branch) plus
  design handoff docs and prior-session working branches.

---

## 2. Branch map

| Branch | Purpose |
|---|---|
| `main` | Repo default. Docs only: `README.md` (design handoff), `SHOPIFY_NOTES.md`, this file, `designs/`. **No theme code.** |
| `staging-theme` | The **full Shopify theme**. Connected to Shopify via the GitHub integration → syncs to the `website/staging-theme` draft theme. Edits here flow to Shopify automatically *once an import succeeds*. |
| `claude/kind-bardeen-*` | "Bardeen" session: educator-portal source (dashboard v2, funding pages, SEO lockdown, tax-exempt upload, category page templates). Source/working branch, not theme-structured. |
| `claude/friendly-curie-*` | "Curie" session: design bundle (HTML mockups), image→WebP optimization. |
| `claude/vigilant-fermi-*` | A Claude working branch. |
| other `claude/*` | Prior session work. |

**Naming note:** Claude session/branch names use scientist surnames
(fermi, curie, bardeen…). When someone says "Curie" or "Bardeen" they
mean those branches.

---

## 3. Shopify themes (IDs)

Theme IDs are stable except the GitHub-connected one, which gets a **new
ID every time it's deleted and reconnected**.

| Theme | ID | Role |
|---|---|---|
| Live Shop Educator Portal Draft 2026-05-28 | `146131452074` | **MAIN (live/published)** |
| `website/staging-theme` (GitHub-connected) | changes on reconnect | UNPUBLISHED draft |
| Educator Portal Staging (copy of live 2026-05-18) | `145914462378` | UNPUBLISHED |
| Old Shop before First Educator Update | `145720180906` | UNPUBLISHED |

The **MAIN** theme is what customers see. The **GitHub-connected draft**
is the target of the `staging-theme` branch sync.

---

## 4. The Git → Shopify pipeline

The `staging-theme` branch is connected to a Shopify draft theme via:

**Shopify admin → Online Store → Themes → Add theme / Import → Connect from GitHub**
- Account: `mytoywagon2020`
- Repository: `website`
- Branch: `staging-theme`  ← type **exactly** `staging-theme`, NOT
  "staging-theme branch" (the field is literal; extra words = "No
  branches were found").

Once connected and successfully imported, pushes to `staging-theme`
auto-sync to the draft theme.

### Verifying sync (via Shopify Admin API / MCP)
Query the theme's `processing`, `processingFailed`, and `files`:
- `processing:false, processingFailed:false` + files present → healthy.
- `processing:true, processingFailed:true`, 0 files, `updatedAt` frozen at
  `createdAt` → **stuck failed import** (see gotcha #2).

---

## 5. CRITICAL GOTCHAS (the issues we hit)

### #1 — 50MB total theme size limit
Shopify's GitHub import rejects themes over **50MB total** with:
> `Error: /, Theme is too large. Maximum theme size is 50MB.`

(Seen via the theme's **"View logs"** link in the admin error message.)

- The bloat lives in `assets/`. Keep it lean.
- **Use WebP, not PNG.** Don't commit multi-MB PNGs to `assets/`.
- Check before pushing: `du -sh --exclude=.git .` must be **< 50MB**.
- This is a **total-size** limit, **not** a per-file limit (see #3).

### #2 — Failed imports get STUCK and do NOT auto-retry
When an import fails, the theme shows a perpetual spinner
(`processingFailed:true`, `updatedAt` frozen at creation time). **New
pushes do not fix it.** You must:
1. Theme ⋯ menu → **Delete** the stuck draft.
2. **Connect from GitHub** again (new theme ID).

Deleting the **Shopify theme** does NOT delete the **git branch** — the
branch lives in GitHub, untouched. Always click **"View logs"** on the
failed theme first to read the real error.

### #3 — Per-file size is NOT the limit (red herring)
Shopify stores large Liquid files fine — the live MAIN theme contains
180–190KB educator page templates with no problem. Only **total** theme
size matters for the GitHub import. (We did extract the big inline
`<style>` blocks from the 8 educator templates into `assets/edu-*.css`
anyway — smaller, cacheable, good practice — but that was not the fix.)

### #4 — `file_url` vs `asset_url`
- `'img.png' | asset_url` → served from the theme `assets/` folder.
- `'img.png' | file_url` → served from **Shopify Files** (CDN), uploaded
  separately. The `assets/` copy is **not used** for rendering.

The educator pages reference their images via `file_url`, so any `assets/`
copies of those images are dead weight — safe to delete with zero visual
impact. (This is how we cut the theme from 103MB → 25MB.)

### #5 — JSON files with `/* comments */` are fine
Shopify theme JSON (templates, `settings_data.json`, section groups) is
**JSONC** — it allows `/* ... */` comment blocks (often an
"auto-generated" header). Strict JSON validators flag these as invalid;
**they are not broken.** Don't "fix" them.

---

## 6. Current status (2026-05-28)

- `staging-theme` trimmed from **103MB → ~25MB** (35 unused/duplicate/
  `file_url` images removed); 8 educator templates CSS-extracted to
  `assets/edu-*.css`. Branch is import-ready.
- **Recent content edits are NOT yet live.** The therapy-dough origin fix
  (California → North Carolina) and the removed "For Educators" hero pill
  (Sensory Play, Creative Arts, Dramatic Play) are committed to
  `staging-theme` but the live MAIN theme still shows the old copy. They
  reach Shopify only when the `staging-theme` import succeeds — or via a
  manual paste into the MAIN theme.

---

## 7. Outstanding owner / manual follow-ups (from prior sessions)

These need Shopify-admin or third-party-app actions (not just code):
- Create Shopify **page records** for the new templates (funding,
  tax-exempt, etc.).
- Configure **Helium Customer Fields** for the tax-exempt upload form
  (spec in `HELIUM-TAX-EXEMPT-CONFIG.md` on the Bardeen branch).
- Build **Klaviyo** flows: educator welcome/approval (3 emails) +
  tax-exempt 30-day expiration reminder.
- Add the four educator links to the **retail theme footer**
  (`RETAIL-FOOTER-SNIPPET.md`).
- **DonorsChoose** vendor application follow-up.
- **B2B Company** creation for Net-30 educators.

---

## 8. Quick reference

```bash
# Check theme size before pushing to staging-theme
du -sh --exclude=.git .            # must be < 50MB

# Find large assets
find assets -type f -size +1M -printf '%s\t%p\n' | sort -rn

# Is an image referenced (and how)?
grep -rn "myimage" --include='*.liquid' --include='*.json' .
#   ...| asset_url  -> needed in assets/
#   ...| file_url   -> served from Files; assets/ copy is deletable
```
