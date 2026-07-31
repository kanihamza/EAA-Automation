# DGO R11.6.1 — Modules & Platform Workspace Review

Scope: full review of the R11.6 OBSIDIAN parity-hardened runtime against three mandates —
(1) proper sectioning of all modules/workspaces including responsiveness and state management,
(2) correct formatting/styling/theming/branding with no generic styling left, and
(3) logically sound end-to-end provisioning, module relationships, inline/per-row behaviours
and user journeys. Every defect below was resolved in this pass; the full contract suite
(103 checks, including three new contracts) passes.

## 1. Sectioning, responsiveness, state management

| # | Finding | Resolution |
|---|---------|------------|
| S1 | `modules/archive.js` was the only module rendering outside the sectioned `.workspace` container — no KPI band, no toolbar, tables unthemed. | Rebuilt into the standard sectioned layout (workspace wrapper → KPI band → toolbar with readiness-queue filter → split panels); inspect action now pre-fills the archive form. |
| S2 | `routes.config.js` phase groups contradicted the sidebar (`nav.config.js`) for registry, acknowledgment, comments, executive and lookup — the command palette and shell described the same workspace as belonging to different phases. | Route groups aligned to the nav phase map; locked by `journey-provisioning-contract`. |
| S3 | Two competing state-management patterns: activities/correspondence/registry used the shared `UIState` store; eleven other workspaces used ad-hoc module-level `let` variables for filters/selection. | All fifteen stateful workspaces now manage filters, tabs, selection, pagination, templates and recipients through `UIState`. |
| S4 | Acknowledgment mutated tracked tasks in place (`t.acknowledged = true`) before patching; FastTrack row actions mutated tasks and re-patched the same array reference. | All updates rebuilt immutably via mapped copies. |
| S5 | Several state patches bypassed audit metadata (comments, approvals creation, registry lifecycle, single/bulk assignment, user administration), producing generic `state.patch` audit entries. | Every mutation now carries `{module, action, ref}` audit meta. |
| S6 | Responsive gaps: DG/CEO three-pane layout jumped from 3 columns straight to 1 at 1000px; recipient chip input overflowed small screens; record action grids cramped at 560px. | Added 1001–1280px two-column stage for `.dg-layout`, small-screen fixes for `.recip-input-row`, `.action-ribbon`, `.actions`, and toolbar label/select styling. |
| S7 | Browser tab title was static. | Shell now mirrors the active workspace into `document.title`. |

## 2. Formatting, styling, theming, branding

| # | Finding | Resolution |
|---|---------|------------|
| T1 | 18+ hard-coded, off-brand colors in `app.css`: Microsoft-blue recipient chips (#0078D4), grey Tailwind-derived tag palettes, teal SLA bars (#00A69D), orange danger buttons (#E05606), fixed light backgrounds on pills/tags/threads/alerts/matrix cards/report templates — all of which broke the dark and high-contrast themes. | Introduced theme-aware tone-surface tokens (`--ok-soft`, `--warn-soft`, `--danger-soft`, `--info-soft`, `--accent-soft`, `--neutral-soft`) and brand `--gold`, each with dark/high-contrast overrides; every component rule now derives from tokens. Locked by `theme-token-contract`. |
| T2 | Registry minute-sheet "paper" skeuomorph was unreadable in dark mode (near-white theme text on cream paper). | Fixed ink colors declared on the paper surface (deliberate skeuomorphic exception, documented in the contract). |
| T3 | Static inline styles scattered through nine modules (cursor, margins, widths, flex, grid-column, min-heights) — generic formatting outside the design system. | Replaced with design-system classes (`.panel-eyebrow`, `.flex-1`, `.row-link`, `.row-active`, `.col-narrow`, `.check-inline`, `.grid-title`, `.btn.compact`, `.stack-panel`, `.role-details`, `.result-group`); banned going forward by `workspace-sectioning-contract`. Data-driven widths (progress bars, chart values) remain inline by design. |
| T4 | Hand-built tables in acknowledgment, archive, FastTrack, user-admin and the correspondence email desk bypassed the canonical `dgo-table` design-system classes. | All now carry `dgo-table-wrap`/`dgo-table`. |
| T5 | Runtime title still declared "R11.2 Revised Design System Runtime". | Corrected to the R11.6 Obsidian designation. |

## 3. Provisioning, module relationships, per-row behaviour, user journeys

| # | Finding | Resolution |
|---|---------|------------|
| J1 | Dispatch ignored its provisioned closure gate: any non-closed task (including untouched work) could be dispatched, and the `dispatches` state collection was never written — Home KPIs and Statistics that read it were permanently blind. | Queue now admits only completed work (or already in-flight dispatches); dispatching captures channel + recipient and writes a dispatch record; closure stamps receipt evidence onto the record. |
| J2 | Dispatch lacked its provisioned `no-dispatch` disposition. | Governed no-dispatch path with mandatory reason, confirmation, and closure eligibility. |
| J3 | Acknowledgment provisioned `remind` and ageing but implemented neither. | Per-task remind action queues a notification with audit trail; ageing badges (with ≥2-day escalation tone) shown per row and in the detail pane. |
| J4 | Approval decisions vanished on decision — no history, no record of the deciding actor. | Pending/Decided view chips; decisions record actor, timestamp, signature and minute, rendered in a decision detail grid. |
| J5 | Row affordances inconsistent: some tables signalled clickability via inline cursor styles, some not at all; no hover/selected feedback. | Standardized `row-link`/`row-active` classes with hover and selection states across orchestrator, response-tracking, acknowledgment, user administration. |
| J6 | Response-tracking search rebuilt the DOM per keystroke and lost input focus. | Debounced with caret restoration (matching the orchestrator/lookup pattern). |

## Verification

- `bash tests/run-all.sh` — all contracts pass, including the three added by this review:
  `workspace-sectioning-contract` (mounts all 23 modules; asserts sectioned rendering; bans static inline styles),
  `theme-token-contract` (asserts token definitions and per-theme overrides; bans off-brand hexes),
  `journey-provisioning-contract` (nav/route agreement; dispatch gate + records; acknowledgment remind; approvals history; uniform UIState adoption).
- Mount simulation confirms all 23 route modules render non-empty sectioned output without error.

## Runtime location

The reviewed and enhanced R11.6.1 runtime (all 23 modules, design system, contract suite) lives in the EAA-Cloud repository under `dgo-platform/` on branch `claude/modules-workspace-review-wp8srf`. The legacy HTML screens in this repository are the parity sources that runtime consolidates.

## Addendum — R11.6.2

A follow-up pass resolved four platform-wide UI defect classes: portrait view switching with explicit list/detail states and back controls; row selection now switching to the expected view; independent per-pane scroll regions (detail stays fixed while queues scroll); and de-merged detail columns rebuilt as stacks of independent panels with reveal-on-request forms. Locked in by the new `view-pane-contract` in the EAA-Cloud `dgo-platform/` runtime (117 checks passing).

## Addendum — R11.6.3 Consolidation

All findings of the duplication/redundancy/overlap assessment are fully implemented in the
EAA-Cloud `dgo-platform/` runtime: canonical domain transitions (acknowledgment, task
update/creation, correspondence disposition), one priority scale, shared report/export
engine, single sync façade, notifications inbox, escalation queue, dispatch analytics and
backend retry, real governance execution via the ownership façade, OTP-protected bulk
batches, all orphan services wired or retired, shared classifiers/lineage/UI helpers, and
HUD/Diagnostics delineation. Enforced by the new provisioning-drift and consolidation
contracts — 119 checks pass.
