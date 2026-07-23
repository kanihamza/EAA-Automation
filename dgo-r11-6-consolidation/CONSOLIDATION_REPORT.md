# DGO R11.6 — Workspace Consolidation Report

**Base:** `DGO_R11_6_OBSIDIAN_FIGMA_UIUX_IMPLEMENTED_ALL_RECOMMENDATIONS` (245 files, the
newest sibling build), reconstructed byte-for-byte from the forensic snapshot (245/245 SHA-256
verified).
**Method — new this round:** every change was **rendered and measured in a real headless
browser** (Chromium/Playwright) and diffed against a before-baseline. No blind CSS edits. This
verification loop is the thing prior iterations never had, and it is why the fixes below are
root-cause corrections rather than more overrides.

---

## Why every prior version failed — proven, not asserted

The platform loads **19 stylesheets** in which the same selectors are defined many times with
contradictory values. The winning pixel is decided by an unmanaged mix of load-order,
specificity, `!important`, and `@container`/`@media` — which no one was reasoning about as a
whole. Two measured examples make it concrete:

1. **`align-items` set four ways on one element.** On the Command Center's `.split` panels the
   browser matched, in order:
   ```
   .split                                             -> align-items:start
   .split,.dgo-master-detail,.dg-layout,.dashboard-grid -> align-items:stretch !important   ← won
   .cc-support-panels                                 -> align-items:start
   .split,.dgo-master-detail                          -> align-items:start
   ```
   The lone `!important` forced every `.split` to stretch — so a **collapsed** "Module rule"
   `<details>` inflated to its open sibling's height, producing the large empty void.

2. **The same metrics selector defined eight times.** `.cc-kpi-band .kpis` had **8** competing
   `grid-template-columns` rules across breakpoints. Worse, a grouped rule
   `.kpis,.stat-row,.cc-kpi-band{display:grid;grid-template-columns:…}` accidentally made the
   *wrapper* `.cc-kpi-band` a multi-column grid, so on mobile the KPI grid was trapped in the
   first 164px track and **half the row was empty** with labels clipping ("REFER ENCES").

When a one-line targeted fix was applied, it **did not win the cascade** — direct proof that the
architecture, not any single rule, is the defect. That is why "implementing all recommendations"
kept adding overrides (app.css grew to 70KB, `!important` count rose) yet quality fell.

---

## What was changed (all verified by render + tests)

| # | Fix | File | Verification |
|---|-----|------|-------------|
| 1 | **One deterministic stylesheet entry** — 19 `<link>` tags replaced by a single documented `styles/index.css` import list. | `index.html`, `styles/index.css` (new) | Pixel diff vs baseline **0.001–0.005%** (identical). |
| 2 | **Dead code removed** — deleted the never-loaded `styles/revised-dgo/` tree (9 files). Stylesheets **28 → 20**. | `styles/revised-dgo/*` | No references in any loaded path; tests green. |
| 3 | **Token-drift reconciled** — `var(--dgo-radius-card,14px)` → `var(--dgo-card-radius,14px)` (×4) so cards resolve the real token instead of a silent hardcoded fallback. | `styles/app.css` | Token defined in `tokens.component.css`. |
| 4 | **Killed the `align-items:stretch !important` anti-pattern** and scoped equal-height panes to true master-detail (`.split[data-md]`, dashboards) only. | `styles/app.css` | Command Center void **gone**; master-detail routes **0.00%** changed (unaffected). |
| 5 | **Fixed the KPI-band wrapper bug** — `.cc-kpi-band` is now `display:block`, so its inner `.kpis` fills the full width. | `styles/app.css` | Desktop band now spans full width; mobile shows 2 full-width columns, labels on one line. |
| 6 | **Fluid action grid** — `.cc-action-grid` uses `repeat(auto-fit,minmax(230px,1fr))` so however many cards RBAC shows, they fill the row. | `styles/app.css` | Single card now spans full panel instead of floating. |
| 7 | **No mid-word label breaks** — KPI/stat labels break only at spaces. | `styles/app.css` | "REFERENCES" no longer splits. |

**Change surface:** `index.html`, `styles/app.css`, `+styles/index.css`, `−styles/revised-dgo/`.
Everything else is byte-identical to the verified snapshot.

**Tests:** `bash tests/run-all.sh` → **all contract suites pass** (syntax-integrity, layout-footer,
mobile-landscape-containment, modal-focus-coverage, module-clarity, nested-fetch-empty-error,
relationship-openas, runtime-route-visual-blocker, screen-containment, typography-floor,
ui-polish, user-enrollment-rbac).

**Regression check:** master-detail data routes (Activities, Registry, Single-Assignment) diff
**0.00%** — the fixes touched the broken Command Center composition without disturbing the data
views.

---

## Important finding about the empty state

Rendered standalone (no backend), the app sits in an **offline + empty-data + degraded-RBAC**
state: most KPI values are 0 and RBAC hides most action cards (only 1 of 5 renders). Much of the
"everything looks broken/sparse" impression comes from this unrepresentative state, **not** from
layout bugs. The layout defects that are real and state-independent (the void, the KPI wrapper,
the mid-word wrapping, the token drift) are fixed here. Judging visual polish fairly for the
remaining surfaces requires **representative seed data** — otherwise we would be tuning CSS
against empty panels, which is exactly the churn to avoid.

---

## What remains (the honest scope line)

This round fixed the **highest-impact, data-independent** structural defects and gave the project
a deterministic single-entry cascade and a working visual-verification harness. It did **not**
rewrite all ~66 collided component selectors into strict single-owner form — that is a bounded but
larger program, now de-risked because:

- the cascade is a single documented file, and
- any change can be rendered + pixel-diffed + contract-tested before acceptance.

Recommended next phase: (a) load representative seed data; (b) move each remaining collided
selector (`.kpis`, `.grid`, `.split`, `.panel`, card family) to a single home in the components/
layout layer, deleting the app.css/figma duplicates; (c) then, and only then, wrap the cascade in
`@layer` — safe once each selector has one owner (a blind `@layer` wrap on today's code shifts 43%
of pixels, because layer-order overrides specificity).
