# DGO R11.6 — Designer-Spec Execution Report (R4, data-verified)

**Base:** `DGO_R11_6_CONSOLIDATED` (aa62fef). **This version:** `DGO_R11_6_CONSOLIDATED_R4`.
**Verification:** headless render at all breakpoints/routes **+ representative data** driven through
the platform's real data path (endpoint requests intercepted, fixture returned; the app's own
`parseFetchAll`→`State` pipeline runs) **+ `tests/run-all.sh` 16/16 green** + pixel-diff /
computed-style measurement. Owner decisions D1–D6, token Approach A, P0-4=(a) applied.

## Representative data
`fixtures/representative-fetch-all.json` — 18 documents, 16 tasks, 9 users (incl. enrolled profile
`dgsregistry@nitda.gov.ng`), 6 categories, 5 departments, 6 emails, 6 approvals; varied
statuses/priorities/overdue. Drives KPIs, record lists, tables, source-view counts and pills.

## Executed and verified
| Item | Result |
|---|---|
| **P0-1 Tokens (Approach A)** | `tokens.legacy-bridge.css` sole owner; `tokens.css` + duplicate PA bridge deleted; only the 4 mandated corrections changed; themes + live dims preserved; body→Inter (D1); `--strong`#1B1A1A (D2). |
| **P0-2 `@layer` cascade** | `@layer tokens,base,layout,components,overrides`; 0.00% render shift. |
| **P0-3 KPI grid** | One canonical auto-fit rule; home/executive/statistics consistent (4-col @1024, was 2/3/3). |
| **P0-4 `!important`** | Kept containment `!important` (decision a; contract tests mandate them). |
| **P1 Flat surfaces (D5)** | figma layer deleted; gradients/backdrop-blur gone (verified with data). |
| **P1-2 Touch targets (D6)** | buttons + nav 44px; button radius/pad per §E. |
| **P1-3 Pills (data-verified, complete)** | Canonical `.dgo-pill` end to end (`statusClass`/`priorityClass` + shared `badge()` helper emit `.dgo-pill .dgo-pill--<tone>` with label-derived tone). **components.css is the sole pill owner** — removed the partial `.dgo-pill*` set from `platform-authority.css` that left `pending`/`warning` neutral. **All tones now colour-code:** Not Started/Awaiting→amber, In Progress/Normal→blue, Low/Completed→green, Urgent/High→red. |
| **P2-1 Command palette** | Removed dead `command-palette.css` (factory uses `.dgo-cmdk__list`; sheet used the orphan `.dgo-cmdk__listbox`). Palette styling unaffected (app.css owns it). |
| **P2-3 Brand mono** | `--dgo-family-mono` leads with Cascadia Mono. |
| **P3 z-index** | topbar → `var(--dgo-z-sticky)`. |
| **§E** | KPI cards: 3px smart-green left accent. Inputs: radius 6px (via `--rc`→`--dgo-radius-control`). Pills: see P1-3. |
| **§F** | Drawer focus-trap: Tab containment + focus-return on `[data-open-drawer]` surfaces (WCAG 2.1.1/2.4.3). |

## Flagged spec errors (ruled by owner, corrected)
Live layout dims are not dead (retained); the bridge was incomplete (completed); §C.4 "tests green
without !important" false (kept them); 24 routes not 25; ministry has both width+height triggers (kept both).

## Remaining (smaller refinements; all now verifiable with the shipped harness)
- **Welcome-overlay focus-trap (§F):** drawer done; the multi-phase welcome/OTP overlay still lacks a Tab trap.
- **§G config coherence:** nav/routes single source + group-taxonomy unification (`routes.config.js` canonical) — a config refactor.
- **Dead legacy `.shell/.top/.nav` selector deletion (P2-2):** entangled with the containment `!important` the tests mandate; left intact.
- **§E table row-height/hover tokens** (cosmetic; tables render correctly).

## Harness (shipped for continuation)
`fixtures/` + render/measure scripts reproduce populated verification: serve the tree, intercept
`powerplatform.com`, return the fixture, drive routes via `Router.go`. Enrollment requires the
profile to be an active user (included in the fixture).

Ships full-content-embedded `state.json` (round-trip byte-identical) per the repo standing rule.


## R5 — data-surfaced layout fix
**Toolbar/filter-bar clipping (found via populated render, user-reported).** The workspace is a
fixed-height flex column (`overflow:hidden`, single-scroll invariant). Sticky toolbars had default
`flex-shrink:1`, so with a tall populated record list they were compressed from ~54px to ~26px and
their controls (search, filters, action buttons) were clipped/hidden. Fix: `.toolbar/.dgo-toolbar/
.dgo-filterbar{flex:0 0 auto;overflow:visible}` — the bar keeps natural height; the list pane owns
the scroll. Verified: activities/response-tracking/registry toolbars now full-height, no clip.
This class of defect is invisible in the empty state — only the fixture harness surfaces it.
