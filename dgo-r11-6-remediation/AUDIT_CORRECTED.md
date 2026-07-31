# DGO R11.6 "Obsidian / Figma UI-UX" — Corrected UX/UI & Accessibility Audit

**Mode:** Advisory / read-only — no files were modified.
**Artifact audited:** `DGO_R11_6_OBSIDIAN_FIGMA_UIUX_IMPLEMENTED` forensic snapshot
(`forensic-platform-state/v1`, generated `2026-07-22T23:23:38Z`, 226 files, 13 dirs).
**Method:** Every finding below is anchored to a `file:line` citation taken directly from the
snapshot's embedded file contents. Where a stylesheet is minified, several rules share one
physical line; the cited line is the line the quoted declaration sits on.

> **Why this replaces the prior audit.** The previous report is rejected on provenance and
> accuracy. It claimed to audit `src/prototype/dgo-prototype.html.txt` and
> `src/imports/dgo_r11_6_ob_state.json` — **neither path exists in this artifact.** The real UI
> is `index.html` plus a 19-file design system under `styles/`. Its headline numbers
> (`.pill height:22px`, `.ministry 9px`, "no `:focus-visible`", "no focus trap", "768px gap")
> do not match the code: `height:22px` appears **nowhere**; `:focus-visible` appears **35 times**;
> a real focus trap exists in `shared/shell.js`; and the 768px breakpoint is fully specified.
> Several of its "P0 fixes" are already implemented. Details and corrected findings follow.

---

## 1. Executive Summary & Corrected Top Risks

The platform ships a mature, token-driven, zero-build design system with a layered cascade
(`index.html` loads the full DS first, then `styles/app.css` and
`styles/dgo-design-system/figma-uiux-implemented.css` as override layers — `index.html:12–33`).
Accessibility infrastructure is **substantially present and shipped**, and is self-documented in
`evidence/DESIGN_SYSTEM_ACCESSIBILITY_UI_CONTRACT_MATRIX.json` and
`evidence/ACCESSIBILITY_AUDIT_MATRIX.json`. The prior audit's picture of a system lacking focus
management, focus-visible states, and responsive reflow is **not supported by the code**.

After verification, the genuine residual risks are narrow:

- **[P2] Micro-typography floor.** A handful of *effective* type sizes remain small: ministry
  bar `8px` (`styles/app.css:3`), grid field labels `10px` (`styles/app.css:7`), action-card body
  `10.25px` (`styles/app.css:149`), preview-table pills `10px` (`styles/app.css:207`). These are
  legibility (not WCAG-AA text-size failures — WCAG 2.2 AA has no minimum font-size SC). Worth a
  deliberate minimum-size pass on **persistent** labels.
- **[P2] Focus-trap coverage completeness.** `shared/shell.js:68` implements a real trap for
  shell-managed transient surfaces (command palette, detail pane, persona menu, drawer). What is
  **unverified** is whether every module-level modal in `modules/*.js` routes through that shell
  path. This is the correctly-scoped version of the prior audit's "no focus trap" claim.
- **[P3 / UNVERIFIED] Dynamic-text overflow & empty/error states.** No explicit
  truncation/`text-overflow` contract was located for dynamically-loaded table cells or
  `.route-title .desc`; empty/error states for deeply-nested fetches were not confirmed present.
  Flagged as assumptions to verify, not defects.

No P0 or P1 accessibility blockers were confirmed.

---

## 2. Corrected 7-Pillar Scorecard (0–5)

| Pillar | Prior | **Corrected** | Basis |
|---|---|---|---|
| A. Layout | 4.5 | **4.5** | Master-detail `.split` + single scroll region confirmed (`styles/app.css:7,11`). |
| B. Responsiveness | 3.5 | **4.5** | Full breakpoint ladder incl. 768px off-canvas drawer + self-collapsing `auto-fit` grid (§4). |
| C. Interactivity | 3.0 | **4.0** | Real focus trap, Escape-to-close, keyboard palette (`shared/shell.js:68`, `shared/accessibility.js:7`). |
| D. Visual / Style | 4.5 | **4.5** | Layered token system + theming; unchanged. |
| E. Component consistency | 4.0 | **4.0** | Canonical components; some density overrides vary (`styles/app.css:145–160`). |
| F. Accessibility (WCAG 2.2 AA) | 2.5 | **4.0** | 35 `:focus-visible` rules, focus-ring token, aria-modal, skip link, HC theme, reduced-motion (§6). |
| G. Content / Data presentation | 4.0 | **3.5** | Good density; truncation/empty-state rules genuinely unverified (§8). |

The prior **F = 2.5** is not defensible against the shipped accessibility contract; corrected to **4.0**.

---

## 3. Corrected Design-System Spec Sheet

| Element | Prior "current" claim | **Verified actual** | Verdict on prior recommendation |
|---|---|---|---|
| `.pill` size | `height: 22px` | **No `height` declared.** Padding-sized `inline-flex`; winning layer `padding:4px 9px; font-size:11px` (`figma-uiux-implemented.css:5`). `height:22px` is **absent everywhere**; only `height:24px` in file is on `.footer img` (`styles/app.css:149`). Pills carry **no** click handler / `role` / `href`. | **Reject.** Fabricated value; WCAG 2.5.8 target-size does not apply to non-interactive badges. |
| `.pill` font | — | Base `font:700 9px` (`styles/app.css:7`) is **overridden** to `11px` by the later `figma-uiux-implemented.css:5`; `.preview-table .pill` is `10px` (`styles/app.css:207`, higher specificity). | Effective pill text is **11px**, not 9px. |
| `.ministry` text | `font-size: 9px` → 11px | **`font:700 8px`** (`styles/app.css:3`); bar is `display:none` and `--ministry:0px` at ≤768px (`styles/app.css`, `@media(max-width:768px)`). | Wrong value (8px). Legibility note has partial merit on desktop; treat as **P2**. |
| `.dgo-nav-group__label` | `9px` → 11px | Base `10px` (`styles/app.css:179`) **already overridden to `11px`** (`styles/app.css:268`). | **Already implemented.** |
| `.eyebrow` | `9px` micro | Base `9px` (`styles/app.css:7`) **overridden to `11px`** (`figma-uiux-implemented.css:5` and `.dgo-card__eyebrow` group). | **Already implemented.** |
| Status pill tokens | "6 mapped; add fallback" | **4** variants — `ok/warn/danger/info` (`figma-uiux-implemented.css:5`). Base `.pill` already carries a default background (`styles/app.css:7`, `figma-uiux-implemented.css:5`), so unmapped statuses render **styled**, not generic. | Count wrong; **fallback already exists.** |
| Focus rings | "browser default for some" | Token `--dgo-focus-ring: 0 0 0 3px rgba(23,178,85,.28)` (`styles/app.css:168`), applied via 35 `:focus-visible` rules across 6 stylesheets. | **Reject.** Standardized ring already shipped. |

---

## 4. Corrected Responsive Matrix

Verified breakpoint behaviour (all from `styles/app.css` unless noted):

| Concern | Evidence | Behaviour |
|---|---|---|
| Cards / KPI grid | `.grid{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}` (`:7`) | **Self-collapsing** — columns drop automatically as width shrinks; cannot "squish" below the 220px floor. Explicit `.grid{grid-template-columns:1fr}` at `@media(max-width:560px)`. |
| Master-detail | `.split{...minmax(230px,1fr) minmax(0,1.7fr)}` (`:11`) → `.split{grid-template-columns:1fr}` | Reflows to single column; `data-md` toggles list/detail panes (`:11`). |
| Sidebar / nav | `@media(max-width:768px)` block | Shell → 1 column; nav becomes **off-canvas drawer** (`transform:translateX(-105%)`, `.nav.open{transform:none}`). Drawer arrives at **768px**, not 600px as the prior matrix stated. |
| Ministry / footer | `@media(max-width:768px)` | `--ministry:0px`, `.ministry{display:none}`, `--footer:40px`. |
| Density | `@media(max-height:…) and (min-width:1000px)` blocks (`:145–160`) | Height-aware compaction of action cards. |

**Conclusion:** the prior report's "768px gap / 3-col squished" is a **false gap** — the breakpoint
exists and the grid is intrinsically responsive.

---

## 5. Interaction / State — Corrected

**Modals / drawers / palette — focus management.** `shared/shell.js:68` defines
`_trapFocus(surface)`, which captures the opener for focus return
(`const opener = document.activeElement…`, `shared/shell.js:69`), enumerates focusables, and
cycles Tab within the surface; `aria-modal` / `role="dialog"` are set (`shared/shell.js:86`), and
`Escape` closes transient surfaces (`shared/accessibility.js:7`). The prior "focus escapes to
background / no trap" finding is **not reproduced** for shell-managed overlays.
→ *Correctly-scoped residual (P2):* audit `modules/*.js` modals for whether they all route through
this shell path; only shell surfaces are verified.

**`.action-card` focus visibility.** Already defined:
`.action-card.cc-action:hover, .action-card.cc-action:focus-visible{ border-color:var(--a);
transform:translateY(-1px); box-shadow:var(--shadow) }` (`styles/app.css:145`). The focus-visible
state already matches hover — i.e. exactly the prior audit's "recommendation." **Already implemented.**

---

## 6. Corrected Accessibility Audit (WCAG 2.2 AA)

| Element / check | Prior result | **Verified** | Pass/Fail |
|---|---|---|---|
| `.pill` hit-target | FAIL (22px) | Non-interactive status badge; no `height:22px` exists; 2.5.8 not applicable | **N/A (not a target)** |
| `.ministry` text | FAIL (9px) | `8px` decorative bar, hidden ≤768px (`styles/app.css:3`) | **Advisory (P2)**, not AA SC |
| `.dgo-nav-group__label` | FAIL (9px) | Already `11px` (`styles/app.css:268`) | **Pass** |
| Modals / drawers focus | FAIL (escapes) | Real trap + return + aria-modal (`shared/shell.js:68,69,86`) | **Pass** |
| `:focus-visible` presence | "lacks" | 35 rules: app.css 4, components.css 9, figma-uiux-implemented.css 7, platform-authority.css 7, revised-dgo/platform-authority.css 7, reset.css 1 | **Pass** |
| Skip link | not noted | Present (`index.html:30`) | **Pass** |
| Keyboard / Escape | FAIL implied | Cmd/Ctrl-K palette + Escape close (`shared/accessibility.js:7`) | **Pass** |
| High-contrast theme | not noted | `[data-theme=hc]` tokens (`tokens.theme-hc.css`) | **Pass** |
| Reduced motion | not noted | `@media (prefers-reduced-motion)` (multiple files) | **Pass** |
| Icon-button labels | not noted | aria-labels per accessibility contract matrix | **Pass** |

Shipped self-evidence corroborating the above: `evidence/ACCESSIBILITY_AUDIT_MATRIX.json`
(lists `focus-ring-token`, `dialog-role-modal`, `escape-close-surfaces`, `route-focus-management`,
`skip-link-retained`, `high-contrast-theme`, `reduced-motion`) and
`evidence/DESIGN_SYSTEM_ACCESSIBILITY_UI_CONTRACT_MATRIX.json`.

**Not verified (do not claim pass):** actual measured color-contrast ratios (e.g. the prior
"4.7:1" for `.btn--ghost` is unsupported by any measurement in the snapshot — no
contrast-computation evidence exists), and screen-reader announcement order. These require a
runtime/assisted audit as the artifact's own status field concedes
(`"implemented-ready-for-assisted-audit"`).

---

## 7. Corrected Remediation Roadmap

**Reclassified — nothing rises to P0/P1.**

- **P2 — Typography floor (S).** Set a minimum size for *persistent* labels; targets are
  `styles/app.css:3` (ministry 8px), `:7` (grid label 10px), `:149` (action-card body 10.25px),
  `:207` (preview-table pill 10px). *Do not* touch `.dgo-nav-group__label` / `.eyebrow` — already 11px.
- **P2 — Modal-trap coverage audit (M).** Confirm every `modules/*.js` overlay uses
  `shell._trapFocus`; wire any that bypass it. (Infrastructure exists — this is coverage, not build.)
- **P3 — Truncation contract (S).** Add explicit `text-overflow`/clamp rules for dynamic table
  cells and `.route-title .desc` if runtime testing shows overflow.
- **P3 — Empty/error states (S).** Verify nested-fetch empty/error/timeout states in `core/fetch-manager.js` / `config/fetch-policy.config.js`.

**Explicitly withdrawn from the prior roadmap (already satisfied or invalid):** pill height→24px;
9px→11px for nav-group-label & eyebrow; "add focus-visible to action-card"; "standardize focus
ring"; "add 768px breakpoint"; "add pill fallback token."

---

## 8. Coverage Log

- **Verified against embedded content:** `index.html`; `styles/app.css`;
  `styles/dgo-design-system/figma-uiux-implemented.css`, `components.css`, `colors_and_type.css`,
  tokens (`tokens.theme-hc.css` etc.); `shared/shell.js`, `shared/accessibility.js`;
  `evidence/ACCESSIBILITY_AUDIT_MATRIX.json`,
  `evidence/DESIGN_SYSTEM_ACCESSIBILITY_UI_CONTRACT_MATRIX.json`.
- **Corrected provenance error:** prior audit's `src/prototype/dgo-prototype.html.txt` and
  `src/imports/dgo_r11_6_ob_state.json` **do not exist** in this artifact.
- **Genuinely unverified (assumptions, not defects):** runtime color-contrast ratios; dynamic-text
  truncation; nested-fetch empty/error/timeout states; screen-reader announcement order. These need
  a runtime/assisted pass, consistent with the artifact's own
  `"implemented-ready-for-assisted-audit"` status.
