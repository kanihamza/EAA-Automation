# DGO R11.6 "Obsidian / Figma UI-UX" — Remediation Report

**Scope:** Resolves the actionable items from the *corrected* evidence-cited audit.
**Source of truth:** Files reconstructed byte-for-byte from the forensic snapshot
(`forensic-platform-state/v1`, 225/226 files SHA-256-verified; the 1 unverifiable entry is the
binary `.woff2` font, unrelated to these changes).
**Verification:** `bash tests/run-all.sh` → all 7 contract suites pass
(`syntax-integrity`, `cascade-downstream`, `cascade-summary`, `layout-footer`, `module-clarity`,
`relationship-openas`, `ui-polish`). `node --check` clean on the changed runtime.
**Change surface:** exactly **2 files** — `styles/app.css`, `shared/figma-uiux-runtime.js`.
Apply with `git apply -p1 dgo-r11-6-remediation.patch` from the DGO project root.

---

## What was changed, and why

### R1 — [P2] Micro-typography floor (`styles/app.css`)
Raised the three genuinely-small **persistent** label sizes to an 11px floor. These are the
only effective (post-cascade) sizes below 11px that render on-screen at all times; the audit's
other cited targets (`.dgo-nav-group__label`, `.eyebrow`) were already overridden to 11px and
needed no change.

| Selector | Before | After | Note |
|---|---|---|---|
| `.ministry` | `font:700 8px` | `font:700 11px` | 22px-tall bar (`--ministry:22px`), ample room; hidden ≤768px regardless. |
| `.grid label` | `font:700 10px` | `font:700 11px` | Form field labels. |
| `.preview-table .pill` | `font-size:10px` | `font-size:11px` | Inline preview badges. |

**Deliberately not changed:** `.action-card.cc-action p` at `10.25px` (`app.css`, density block).
This value applies **only** inside a `@media(max-height:…)` short-viewport compaction mode whose
purpose is to prevent card overflow. Raising it would re-introduce the overflow it exists to
avoid — a regression. Left as an intentional density trade-off.

### R2 — [P2] Drawer focus-trap coverage (`shared/figma-uiux-runtime.js`)
This is the correctly-scoped version of the prior audit's "modals have no focus trap" claim. The
shell already traps its palette/dialog/confirm surfaces (`shared/shell.js:_trapFocus`), **but**
drawers opened via `[data-open-drawer]` in the Figma runtime received only *initial* focus — no
Tab containment and no focus return. Added:

- **Tab focus-trap** cycling within the open `.dgo-drawer` (forward and Shift+Tab), matching the
  shell's implementation. → WCAG **2.1.1 Keyboard**, **2.4.3 Focus Order**.
- **Focus restoration** to the opener element on close (via `[data-drawer-close]` click or
  `Escape`), with a `null`-safe `try/catch`.
- **Listener hygiene:** the keydown trap is removed on every close so drawers can reopen without
  leaking handlers.

No markup or endpoint changes; the drawer already carried `role="dialog" aria-modal="true"`
(`shared/components.js` `Drawer()`), so this completes the contract behaviourally.

### R3 — [P3] Dynamic-text overflow guards (`styles/app.css`, additive block)
Record-row titles/metas **already** truncate (`.dgo-record-row__main{min-width:0}` +
`white-space:nowrap;overflow:hidden;text-overflow:ellipsis`). Extended the same protection to the
remaining surfaces that render fetched strings, so long real-world content cannot break layout:

- Single-line ellipsis: `.dgo-card__title`, `.dgo-stat__label`, `.dgo-kpi-card__top` label,
  `.dgo-detail-pane > h2`.
- 3-line clamp: `.dgo-card__body p`, visible `.action-card.cc-action p`.
- `.dgo-table td{max-width:44ch}` cap (tables retain their existing horizontal-scroll strategy).

The prior audit's `.route-title .desc` target was a **non-existent selector** and was dropped.

---

## Verified already-resolved (no change made)

| Prior-audit concern | Finding | Evidence |
|---|---|---|
| "No `:focus-visible`" | 35 rules across 6 stylesheets + `--dgo-focus-ring` token | `app.css:168`, DS sheets |
| "`.action-card` focus-visible undefined" | Already defined, matches hover | `app.css:145` |
| "Shell modals not trapped" | Real trap w/ focus return | `shell.js:68` |
| "768px responsive gap" | Off-canvas drawer + 1-col shell at 768px | `app.css` `@media(max-width:768px)` |
| "Add pill fallback token" | Base `.pill` already carries default background | `figma-uiux-implemented.css:5` |
| Empty/error/timeout states | `LoadingState` (loading/refreshing/success/error/idle, `retryable`, `lastGoodAt`) + `loadRuntimeData` primary→fallback→catch chain; `EmptyState()` used across ~10 modules; `Table()` renders EmptyState on no rows | `loading-state.js:7-14`, `data-loader.js:16`, `components.js` |

## Still requires runtime tooling (cannot be resolved statically)
- Measured color-contrast ratios (the prior "4.7:1" figure had no computation behind it).
- Screen-reader announcement order for live regions.

Both are consistent with the artifact's own status: `implemented-ready-for-assisted-audit`
(`evidence/ACCESSIBILITY_AUDIT_MATRIX.json`).
