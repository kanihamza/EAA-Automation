# CURRENT VERSION — DGO Digital Operations R11.6

There is exactly **one** current version at any time. This file is the single source of truth.

| Field | Value |
|---|---|
| **Current version name** | `DGO_R11_6_CONSOLIDATED_R2` |
| **Build artifact (path)** | `dgo-r11-6-consolidation-r2/DGO_R11_6_CONSOLIDATED_R2.zip` |
| **Embedded state.json** | `dgo-r11-6-consolidation-r2/DGO_R11_6_CONSOLIDATED_R2.state.json` (237 files, full content, no truncation; regenerates the package self-contained — round-trip byte-identical) |
| **Root folder inside zip** | `DGO_R11_6_CONSOLIDATED_R2/` |
| **Basis** | Designer-spec execution: token reconciliation (Approach A), deterministic `@layer`, flat surfaces, deterministic KPI grid, 44px targets, mono. See package `EXECUTION_REPORT.md`. |
| **Branch** | `claude/dgo-r11-6-audit-xm3jv6` |
| **Git tag** | `dgo-r11.6-current` (annotated; local-only in the current environment — see note) |
| **Built from (input snapshot)** | `DGO_R11_6_..._ALL_RECOMMENDATIONS` (245 files, generated 2026-07-23) |
| **Status** | CURRENT |

## How to identify the current version (authoritative order)

1. **Read this file** — it is the single source of truth and is committed to the remote.
2. Optional convenience: `git show dgo-r11.6-current`. NOTE: the current agent environment's git
   proxy blocks tag pushes (HTTP 403 on `refs/tags/*`), so the tag currently exists **locally only**.
   Re-push it from an environment with tag-push rights: `git push origin dgo-r11.6-current`.

## Superseded (NOT current — do not use)

| Artifact | Status |
|---|---|
| `dgo-r11-6-consolidation/DGO_R11_6_CONSOLIDATED.zip` | SUPERSEDED (previous current) |
| `dgo-r11-6-remediation/DGO_R11_6_OBSIDIAN_FIGMA_UIUX_REMEDIATED.zip` | SUPERSEDED |
| `DGO_R11_6_..._PILOT_CANDIDATE` snapshot (226 files) | SUPERSEDED INPUT |

## Rule

When a new version is produced: update the table above, then move the tag
(`git tag -f -a dgo-r11.6-current -m "<name>"` and `git push -f origin dgo-r11.6-current`).
The current version is whatever this file and the `dgo-r11.6-current` tag point to — nothing else.
