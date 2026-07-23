# CURRENT VERSION — DGO Digital Operations R11.6

There is exactly **one** current version at any time. This file is the single source of truth.

| Field | Value |
|---|---|
| **Current version name** | `DGO_R11_6_CONSOLIDATED` |
| **Build artifact (path)** | `dgo-r11-6-consolidation/DGO_R11_6_CONSOLIDATED.zip` |
| **Root folder inside zip** | `DGO_R11_6_CONSOLIDATED/` |
| **Branch** | `claude/dgo-r11-6-audit-xm3jv6` |
| **Git tag** | `dgo-r11.6-current` (annotated; always moved to the current version) |
| **Built from (input snapshot)** | `DGO_R11_6_..._ALL_RECOMMENDATIONS` (245 files, generated 2026-07-23) |
| **Status** | CURRENT |

## How to identify the current version (authoritative order)

1. Read this file.
2. Or: `git show dgo-r11.6-current` — the `dgo-r11.6-current` tag always points to the current version's commit.

## Superseded (NOT current — do not use)

| Artifact | Status |
|---|---|
| `dgo-r11-6-remediation/DGO_R11_6_OBSIDIAN_FIGMA_UIUX_REMEDIATED.zip` | SUPERSEDED |
| `DGO_R11_6_..._PILOT_CANDIDATE` snapshot (226 files) | SUPERSEDED INPUT |

## Rule

When a new version is produced: update the table above, then move the tag
(`git tag -f -a dgo-r11.6-current -m "<name>"` and `git push -f origin dgo-r11.6-current`).
The current version is whatever this file and the `dgo-r11.6-current` tag point to — nothing else.
