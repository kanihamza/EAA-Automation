# Repo directives

## Versioning: every generated version ships an embedded state.json (STANDING RULE)

Whenever a new or updated version of a DGO package is generated, it MUST be accompanied by a
**full-content-embedded `state.json`** for that exact version. Non-negotiable requirements:

- **Every file included, no truncation.** Text files embedded inline (UTF-8); binary files
  embedded as base64. Each file carries its `sha256`, `size`, and relative `path`.
- **Self-contained regeneration.** The JSON alone must be able to recreate the complete package
  with no external inputs. Schema: `dgo-embedded-state/v1`.
- **Proven round-trip before delivery.** Regenerate from the JSON into a fresh directory, verify
  every `sha256`, and confirm the tree is byte-for-byte identical to the source. Only then ship.

Tooling (in this repo):
- Generate: `python3 tools/state-json/embed_state.py <package_dir> <out.state.json> --name <NAME>`
- Verify/regenerate: `python3 tools/state-json/regenerate_state.py <state.json> <out_dir>`
  (use `--verify-only` to check hashes without writing).

Placement: the `state.json` lives next to the version's build artifact and is named
`<VERSION_NAME>.state.json`. Update `CURRENT_VERSION.md` to point to it.

## Current version pointer

`CURRENT_VERSION.md` at the repo root is the single source of truth for which version is current.
There is exactly one current version at any time. Keep it and the `dgo-r11.6-current` tag in sync.
