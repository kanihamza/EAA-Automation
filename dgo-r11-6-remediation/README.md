# DGO R11.6 UI/UX — Audit Correction & Remediation Package

This folder contains the corrected accessibility/UX audit for the DGO R11.6
"Obsidian / Figma UI-UX" build and the resolved remediations for its actionable findings.

> **Note on location.** The DGO R11.6 design-system source is *not* checked into this
> repository — it was supplied as a forensic snapshot. Files here were reconstructed
> byte-for-byte from that snapshot (225/226 SHA-256-verified) and the changes validated against
> the project's own test suite. Apply the patch in the DGO project itself.

## Contents

| File | Purpose |
|---|---|
| `AUDIT_CORRECTED.md` | Evidence-cited audit that replaces the original report. Every finding anchored to a `file:line`. |
| `REMEDIATION_REPORT.md` | What was changed and why; what was verified already-resolved; what still needs runtime tooling. |
| `dgo-r11-6-remediation.patch` | Unified diff for the two changed files. Verified `git apply --check` clean. |
| `changed-files/` | Full post-remediation copies of the two changed files, for reference or drop-in. |

## Applying the remediation

From the root of the DGO R11.6 project:

```bash
git apply -p1 dgo-r11-6-remediation.patch
bash tests/run-all.sh        # expect all 7 contract suites to pass
```

Changed files: `styles/app.css`, `shared/figma-uiux-runtime.js`.

## Summary of resolved items

- **[P2] Micro-typography floor** — ministry / grid-label / preview-pill raised to an 11px floor.
- **[P2] Drawer focus-trap coverage** — Tab containment + focus-return added to Figma-runtime drawers
  (WCAG 2.1.1, 2.4.3), matching the shell's existing dialog behaviour.
- **[P3] Dynamic-text overflow guards** — ellipsis/clamp extended to card titles, stat labels,
  detail headings, card/action body copy, and table cells.

Verified already-implemented (no change): `:focus-visible` + focus-ring token, `.action-card`
focus state, shell modal trapping, 768px responsive reflow, pill default fallback, and
empty/error/timeout state handling. See `REMEDIATION_REPORT.md` for evidence.
