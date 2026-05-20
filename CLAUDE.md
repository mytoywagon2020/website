# My Toy Wagon — project guide for Claude

This file is auto-loaded at the start of every Claude Code session in this repo.
Read the linked docs before writing copy, building pages, or touching the theme.

## Start here
- **`BRAND_VOICE.md`** — brand identity, voice rules, design system (the durable
  "training"). Read this before writing any customer-facing copy.
- **`PDP_STATUS.md`** — product-page build status and where we stopped (resume here
  for PDP / metafield work).
- **`SESSION-HANDOVER.md`** + **`SHOPIFY_NOTES.md`** — theme + deploy state and
  Shopify constraints.
- **`shopify/educator-portal/CLAUDE_CODE_HANDOVER.md`** — educator portal
  structure and the section build process.
- **`shopify/educator-portal/CATALOG_SOURCE_v22r23.html`** — source of truth for
  all product facts.

## Non-negotiable rules (full list in BRAND_VOICE.md)
1. **No em-dashes** in customer-facing copy. **No exclamation marks** in body.
2. **Never invent facts** — no made-up certifications, materials, origins, ages,
   or **prices**. The catalog is the source of truth; quote-only where there is
   no price.
3. **Do NOT delegate this work to subagents.** Build directly.
4. **Be honest about verification** — there is no browser here; don't claim a
   page renders correctly. Flag what needs visual QA.
5. **Mirror everything to git and push.** The cloud container is ephemeral; only
   committed/pushed work survives.

## Deploy reality
Theme 9.0 (`gid://shopify/OnlineStoreTheme/145720180906`) is volatile
(MAIN ↔ UNPUBLISHED). **API theme-file writes are blocked when it is MAIN.**
Always re-check `themes { role }` before any theme push; otherwise mirror to git
and apply via the admin code editor or a duplicate → publish flow.

## Working branch
`claude/fix-github-access-pFh80`
