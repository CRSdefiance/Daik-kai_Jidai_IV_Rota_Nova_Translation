# V687: final build protection for the 18 open plaque/hint entries

## What changed

The integrated builder now checks plaque material after every registered stage
has finished, before saving a playable ROM. Earlier repair stages checked their
own outputs, but the final menu/placeholder checks did not detect a later
overwrite of those materials. Six in-memory controls demonstrate that gap and
the new rejection. No corrupted test ROM is written.

For profiles carrying `local_plaque_texture`, the final contract requires both
complete reviewed atlas files, their original metadata, palettes and dimensions,
and independent complete English glyph masks for all 17 static labels. It
protects background, borders and unowned pixels as well as lettering.

For profiles carrying `equipment_grain_join`, all 1408 bytes of the 44×16 hint
backing tile must match an independent model of the original source frame and
the reviewed 40-column wood repeat. Source columns 3..42 avoid the old pale
frame-adjacent column. The real startup-copy contract binds the tile in its
staged payload to its live destination; the section's staging address is not
mistaken for the final runtime address.

The first draft made precisely that staging/destination mistake and rejected
the unchanged current tile. Its code and diagnostic are retained. Correcting
the address model required no game byte or material change.

## Verification

- Current V685 passes all 17 complete masks and the whole source-derived hint tile.
- Two changed wood pixels, a deleted leading-letter pixel, a palette change, a
  changed hint wood word and the old pre-V581 repeat boundary are rejected.
- All six pass the older final menu/placeholder check, demonstrating why that
  check alone was insufficient for material preservation.
- Unrelated story changes do not trigger the art guard.
- Historical V555 retains its static contract without acquiring V581's later
  hint requirement. Profiles without these material stages report not applicable.
- The full registered `all-routes-unified-v685` rebuild is byte-exact to V685.
  All 470 batches, 114 accepted layers, prior checks, changed paths, records,
  relocations and the final story-format contract remain exact.
- The reproduction manifest adds the final plaque contract. The production V685
  ROM, manifest, patch, registry, canonical baseline and release pointers remain
  unchanged. The existing V685 patch still reconstructs the identical ROM bytes.

The reproduction is `out/all_routes_combined_v685_plaque_contract_rebuild.nds`,
SHA256 `83e7bdc7c4926ad69eb04704e8327aba50d0fe29b00cce7f5f59d4be8c203150`.
It is a reproduction of the current experimental V685, not a new release or
canonical promotion. No new cold boot is claimed for an unchanged binary.

## Texture review remains open

Both retained V671 original/current native-resolution comparison sheets were
opened again. They contain the earlier grain repairs, rather than the large
blocks in the user's historical example. That comparison does not establish
user acceptance or exact recovery of material originally hidden by Japanese
strokes. The six originally pink runtime stat labels and equipment banner were
deliberately restyled as wood; their original surfaces are shown honestly.

All 18 original plaque/hint entries remain `fully_completed:false`. All 22
historical requirements remain exact. This gate preserves current review-pending
artwork; it does not close missing gameplay contexts, legacy/comic/card/control
coverage, older record checks, route playthroughs, hardware or final acceptance.
A future intentional art revision requires fresh source/material review and an
updated registered contract, not automatic target-hash regeneration.

## Evidence

- Gate: `dk4tool/graphics/plaque_contract.py`.
- Controls: `scripts/verify_plaque_final_contract_v687.py`.
- Rebuild verification: `scripts/finish_plaque_final_contract_v687.py`.
- Analysis: `work/analysis/plaque_final_contract_v687`.
- Original/current review: `work/analysis/plaque_review_v671`.
- Archive: `E:/Rota Nova translations/Screenshots/Audit comparisons/V687 Final plaque contract`.
- No guide promotion, commit or push. Full graphics goal remains active.
