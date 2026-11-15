# Separately reserved persistent names

## Status

**V148–V150 revoked on 2026-10-02:** the user reports a black screen and confirms
V147 reaches the title screen. The fourth-section transition is under diagnosis.
The selected native fixtures below do not prove full cold-boot viability. Preserve
their evidence, but do not ship this allocation until the boot regression is fixed.

Integrated in experimental V148. Saved ARM9 matches the native research exactly;
all other V147 components and 3,668 COMMON selections are preserved. Manifest,
canonical baseline and exact clean-ROM patch reconstruction pass. Forty focused
tests and lint pass. See `all_routes_unified_v148_checkpoint.md`. Physical
gameplay and broader display/allocation checks remain open. Earlier pending
integration statements below are retained as research chronology.

Strict production inputs are prepared under `translations/persistent_name_*`.
The production transform reproduces the verified research ARM9 exactly, restores
all native DTCM bytes, preserves ITCM, and guards the 239 relocated references,
two shopkeeper references and reserved heap boundary. All ten shopkeeper rows
have native formatting review, backed by the twenty rasters and ten inspected
panels; physical gameplay is still pending. Eight new positive/rejection checks
bring the focused suite to 40 passing tests. V148 is registered after all 435
V147 batches and postprocessing stages; combined build/verification is underway.

The complete native consumer stack is now repeated on this allocation:
218 initialized item objects/getters, 30 native mutable-name pointers and ten
metadata pairs, 218 static catalogue selections, 436 actual virtual caller
segments, 207 ordinary-name getters and four native map-label selections pass.
Neither persistent text nor restored DTCM changes after these consumers.
Evidence: `work/analysis/persistent_name_consumers_proof.json`.

`scripts/audit_persistent_name_references.py` classifies every all-byte direct
address match in the new range. Both clean and V147 sources have only the BSS
end and initial main-arena low references; current code has 239 complete-name
fields, unchanged BSS end and new autoload destination. There are no overlay
matches. Two residual old-pool address matches are unchanged cross-word
instruction/data bytes, not pointers. Evidence:
`work/analysis/persistent_name_reference_proof.json`. Thirty-two focused tests
and lint pass. Strict registered integration and saved-ROM/patch verification
are next; V147 remains unchanged.

Research only; V147 and the canonical ROM are unchanged. This replaces the
rejected DTCM name allocation with a separately reserved SDK-loaded section.

## Placement

`scripts/probe_persistent_name_section.py` appends a fourth autoload section at
`0x02387A20`, exactly after the original main BSS region. All 117 aligned owners
use 1,480 bytes; 32-byte alignment reserves 1,504 bytes through `0x02388000`.
All 239 known references point to complete strings in this section. Both static
square-shopkeeper labels and eight revised shared labels retain their full text.

The native main-arena initial low literal at `0xE45DC` advances to `0x02388000`.
All other arena bounds remain unchanged. BSS start/end are unchanged, so clearing
stops before the new section. Native DTCM data is restored exactly to clean bytes,
including the scratch image's initial contents and SDK state. The ITCM section
is byte-exact to V147. Main-code preservation is checked across all bytes outside
the name fields, two shopkeeper references, their 24-byte shared text, main-arena
low and required autoload-list bounds.

## Native evidence

- Actual SDK copying and BSS clearing preserve the complete appended section.
- Actual arena initialization reserves the section. The same startup-loaded
  machine verifies six active arena slots and preserves three unused slots;
  a separate before/after comparison checks all unrelated bounds.
- All 207 ordinary given-name getters preserve reviewed wording.
- Actual native scratch construction/rendering performs 173 scratch writes,
  while every byte of persistent text and all 239 referenced names remain intact.
- All 20 shopkeeper native raw-image rasters pass independent pixel comparison
  on this new allocation. Headers/descriptors/guards are preserved; ten two-row
  panels are visually reviewed with full leading/final glyphs and no clipping.
- Three persistent-section checks plus inherited focused tests: 32 passing;
  Ruff passes.

Artifacts: `work/analysis/persistent_name_section_arm9.bin`,
`persistent_name_section_proof.json`,
`persistent_square_shopkeeper_paired_name_context_proof.json`, and
`work/qa/persistent_square_shopkeeper_native/native_sheet.png`.

## Remaining

Verify broader name displays and other computed allocation producers, prepare
strict registered integration and inspect the saved combined ROM/patch.
Actual scene eligibility and physical boot/gameplay remain open. Cache maintenance
and initially zero image clearing remain explicit emulation contracts.
