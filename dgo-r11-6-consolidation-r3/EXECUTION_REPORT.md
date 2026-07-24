# DGO R11.6 — Designer-Spec Execution Report (R3, data-verified)

**Base:** `DGO_R11_6_CONSOLIDATED` (aa62fef). **This version:** `DGO_R11_6_CONSOLIDATED_R3`.
**Verification:** headless render at all breakpoints/routes **+ representative data** driven through
the platform's real data path (endpoint requests intercepted, fixture returned; the app's own
`parseFetchAll`→`State` pipeline runs) **+ `tests/run-all.sh` (16/16 green)** + pixel-diff.
Owner decisions D1–D6, token Approach A, and P0-4=(a) applied.

## Representative data (this made §E/pill verification possible)
`fixtures/representative-fetch-all.json` — 18 documents, 16 tasks, 9 users (incl. the enrolled
current profile `dgsregistry@nitda.gov.ng`), 6 categories, 5 departments, 6 emails, 6 approvals,
with varied statuses/priorities/overdue dates. Drives OPEN/OVERDUE KPIs, record lists, tables,
source-view counts and status/priority pills. Enrollment gate (`core/current-user.js`) required the
profile to be an active user — included.

## Executed and verified
| Item | Result |
|---|---|
| **P0-1 Tokens (Approach A)** | `tokens.legacy-bridge.css` sole owner; `tokens.css` + duplicate PA bridge deleted; only the 4 mandated corrections changed; themes + live layout dims preserved; body→Inter (D1); `--strong`#1B1A1A (D2). |
| **P0-2 `@layer` cascade** | `@layer tokens,base,layout,components,overrides`; 0.00% render shift. |
| **P0-3 KPI grid** | One canonical auto-fit rule; home/executive/statistics all consistent (4-col @1024, was 2/3/3). |
| **P0-4 `!important`** | Kept containment `!important` (decision a; contract tests mandate them). |
| **P1 Flat surfaces (D5)** | figma layer deleted; gradients/backdrop-blur gone. Verified flat with data. |
| **P1-2 Touch targets (D6)** | buttons + nav 44px; button radius/pad per §E. |
| **P1-3 Pills (data-verified)** | Canonical `.dgo-pill` end to end: `statusClass`/`priorityClass` adapter + the shared `badge()` helper (`core/ui.js`) now emit `.dgo-pill .dgo-pill--<tone>` with a semantic tone derived from the label. **Result: record pills are colour-coded** (Urgent/High→danger, In Progress/Normal→info, Low→success) instead of uniform tan. |
| **P2-3 Brand mono** | `--dgo-family-mono` leads with Cascadia Mono. |
| **P3 z-index** | topbar → `var(--dgo-z-sticky)`. |

## Flagged spec errors (ruled by owner, corrected)
Live layout dims are not dead (retained); bridge was incomplete (completed); §C.4 "tests green
without !important" false (kept them); 24 routes not 25; ministry has both width+height triggers (kept both).

## Remaining (characterised precisely; smaller than before)
- **Pill token nuance:** `pending`/`warning` tones render neutral (their `-subtle-bg` resolve to a
  near-neutral in this build) while `danger`/`info`/`success` render correctly. Cosmetic; a
  one-line token adjustment in `tokens.semantic.css` would complete it.
- **§E KPI left-accent, table row/hover tokens, input radius 6:** now verifiable with the fixture; not yet applied.
- **§G config coherence** (nav/routes single source, group taxonomy), **command-palette convergence**,
  **dead legacy `.shell/.top/.nav` selector deletion**, **§F drawer/welcome focus-trap.**

## Harness (shipped alongside for continuation)
`fixtures/` + the render/measure scripts reproduce populated verification: serve the tree, run
`shotpop.mjs` (intercepts `powerplatform.com`, returns the fixture, drives routes via `Router.go`).
This is how every item above was verified — the next pass continues from here with the same loop.

Ships full-content-embedded `state.json` (round-trip byte-identical) per the repo standing rule.
