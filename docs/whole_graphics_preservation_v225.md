# Whole graphics preservation gate V225

The previous turn added raw FLS support and reproduced V218 exactly. This turn
checks the preservation requirements against every current PXL/FLS entry and
prepares exact original screenshot material for the remaining translations.
**The full graphics goal remains active; V218 is unchanged.**

## Whole-inventory result

All **921 entries** pass the preservation gate:

| Family | Entries checked |
|---|---:|
| PXL, including 42 direct-color portraits | 660 |
| FLS textures, including the raw harbor illustration | 261 |

The current combined ROM differs from the clean source in **84 graphic entries**.
Every PXL header's format flags, pitch and height remain exact. Every FLS texture's
flags and decoded dimensions remain exact; its archive compression mode is also
preserved. Every palette and complete pixel-payload extent is preserved across the
whole inventory. No asset is omitted because the indexed reader rejects a direct-
color portrait or because an FLS slot is raw rather than compressed.

The current candidate SHA-256 is
`be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f`.

This gate proves **dimensions/formats/flags/palettes/extents**. It does not claim
that every changed pixel is a translated letter, every border is unchanged, every
line fits a native crop, every alpha state is correct or all translation is complete.
Those requirements retain their own evidence and open items.

## Four translations still require readable source

Online24, Online27, Online31 and Online33 remain only partially localized. Their
source-backed headers/bubbles/Julien name are retained, but the complete body UI,
dialogue/chat and relevant names/status fields have not been faithfully transcribed.
The reduced ROM screenshots do not provide enough detail to safely invent those
lines. Earlier primary-source searches did not locate exact larger counterparts.

The user has been asked for higher-resolution originals or Japanese manual scans
containing those exact screenshots. This is a source-material request, not approval
to generate previews. Independent remaining work can continue while awaiting it.

Exact original Japanese PNGs, source hashes and nearest-neighbor enlargements are
saved under `work/analysis/graphics_preservation_v225/online_source_request/`.
`all_four_originals.png` shows the four images together. Enlargement adds no new
detail and is not a recovered transcript or a completed translation.

## Remaining requirements

- Complete faithful English for the four screenshot bodies and their residual UI.
- Complete-letter/border/crop/alpha/readability evidence for all changed graphics.
- Remaining embedded/raw consumers and contextual artwork/display decisions.
- Confirmed-name consistency in the applicable graphics and text consumers.
- Whole-scope visual/gameplay audit and final registered combined ROM/exact patch.

Preservation passing does not close any of these requirements or reduce the goal.
Older record-based checks remain to revisit after the full goal is complete.

## Reproduction

- `scripts/audit_graphics_preservation_v225.py`, focused Ruff passing.
- `work/analysis/graphics_preservation_v225/whole_asset_proof.json`: all 921 rows.
- `online_source_request/source_request_inventory.json`: exact original source
  image/file hashes and explicit enlargement limits.

No new graphics layer, candidate or patch is generated for this read-only audit.
The existing registered V218 and its verified exact patch remain current.
