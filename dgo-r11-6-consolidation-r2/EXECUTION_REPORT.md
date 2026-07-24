# DGO R11.6 — Designer-Spec Execution Report (R2)

**Base:** `DGO_R11_6_CONSOLIDATED` (aa62fef). **This version:** `DGO_R11_6_CONSOLIDATED_R2`.
**Method:** every change verified by headless render (all breakpoints/routes) + `tests/run-all.sh`
(16 contract suites, all green) + pixel-diff. Decisions D1–D6 and token Approach A ruled by owner.

## Executed and verified

| Roadmap | Item | Result |
|---|---|---|
| **P0-1** | Token reconciliation (Approach A) | `tokens.legacy-bridge.css` is sole owner of all legacy short-vars; `tokens.css` deleted; duplicate `platform-authority.css` bridge removed. Only the 4 mandated corrections changed (`--rc`7→6, `--bd`/`--mut`→DGO, `--strong`→#1B1A1A per D2); live layout dims retained; body→Inter (D1); themes preserved. |
| **P0-2** | Deterministic `@layer` cascade | `@layer tokens, base, layout, components, overrides` in `index.css`. **0.00% render shift.** |
| **P0-3** | KPI grid single owner | One canonical auto-fit `.kpis` rule; the non-monotonic fixed-column divergence is gone — home/executive/statistics now all **4 cols @1024** (was 2/3/3). |
| **P0-4** | `!important` reduction | **Decision (a):** kept the containment `!important` — they are asserted by `screen-containment`/`layout-footer` contract tests (spec §C.4's "green without them" was incorrect; verified). |
| **P1** | Flat surfaces (D5) | `figma-uiux-implemented.css` deleted; gradients on cards/KPIs/panels, the gradient top-bar, and dialog `backdrop-filter:blur` removed. Flat "Governed Calm". |
| **P1-2** | Touch targets (D6) | `.dgo-btn` and `.dgo-sidebar__item` → 44px (`--dgo-control-target-min`); button radius→`--dgo-radius-control`, pad 0 16. Nav item measured 44px. |
| **P2-3** | Brand mono | `--dgo-family-mono` now leads with `'Cascadia Mono'` (the shipped `@font-face` in `colors_and_type.css` is present). |
| **P3** | Topbar z-index | `.dgo-topbar` z-index → `var(--dgo-z-sticky)` (100). |

## Verified misalignments in the spec (flagged; ruled by owner)
1. Spec "delete `--ministry/--header/--footer/--nav-*` as dead" — **false**; consumed by live `app.css` calcs (`.split --pane-max`). Retained (Approach A).
2. Spec "delete `tokens.css`, one bridge covers all" — bridge covered only ~18/37 vars. Completed the bridge (Approach A).
3. Spec §C.4 "containment tests green without `!important`" — **false**; tests assert the literal string. Kept `!important` (decision P0-4=a).
4. Spec DoD "25 routes" — actual **24** (`boot.js`). 
5. Spec §D "ministry hides on height only" — a width rule (`≤768`) also exists; retained both (decision D4).

## Not executed in R2 — reason: cannot be verified against the empty/offline state
Per the spec's own §J.4, fair visual work on these needs **representative seed data**; doing them
blind against empty panels would reintroduce the churn this program exists to end.
- **Pill unification** (adapter → `.dgo-pill`): pills barely render offline (no records) → unverifiable here. The worst pill defect (figma `.dgo-status-pill` mismatch) is already resolved by the figma deletion.
- **§E component detail** requiring populated data: KPI left-accent, table row/hover tokens, populated-state spacing.
- **§G config coherence** (nav/routes single source, group taxonomy): config refactor touching `routes.config.js`/`workflow-clarity.config.js` — needs route-render verification with data.
- **P2-1 command-palette convergence**, **P2-2 dead legacy `.shell/.top/.nav` selector deletion**, **§F drawer/welcome focus-trap**: safe but unverified visually in this pass.

Recommendation: run the next pass with seed data loaded, using the same render+measure+test harness, starting from this version.

## Verification artifacts
`tests/run-all.sh` → 16/16 green. Token/@layer/!important-safe changes: 0.00–0.02% pixel shift.
KPI determinism measured. This version ships its full-content-embedded `state.json`
(`DGO_R11_6_CONSOLIDATED_R2.state.json`, round-trip byte-identical, per the repo standing rule).
