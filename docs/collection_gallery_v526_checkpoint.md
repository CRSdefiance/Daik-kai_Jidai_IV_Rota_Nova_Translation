# V526 collection survey (production V525 unchanged)

The user permits verified DS travel unlocks and useful isolated testing cheats.
The collection survey uses copied saves, with original route slots and donor saves
preserved. No cheat is added to the translation ROM or patch. A verified Maria
selection code exposes that captain; it does not establish a travel-route unlock.
No DS travel-route unlock code has yet been confirmed.

## Items

Original Gallery dispatch selects the first 198 item-history bits, not all 218
inventory records. The fixture sets only those known bits and recomputes the
original signed-byte checksum. Original controls open all 14 pages and wrap back
to page 1. All 28 heading/selected-name masks include complete first and final
letters and blank cells. The 14 selected 32x32 icons match every opaque source
atlas pixel at native five-bit color precision. The first page's entire upper
screen matches its wrapped display exactly.

This verifies 14 selected item descriptions visually, and complete masks for
their names and headings. It does not verify every individual description,
tooltip, grid icon, acquisition event, or plaque. All 18 plaques remain incomplete.

## Historic Sites

Original dispatch reads 21 site-history bits. Separate single-site copied saves
test all IDs 0-20. Nineteen display their original list and world map successfully.
IDs 1 (Poitiers Cathedral) and 4 (Santa Maria Maggiore Basilica) fault before the
list displays. Failed screenshots receive no display credit. All 21 original name
pointers and Japanese bytes are present in the actual exported RAM.

The all-site fixture, a 20-site fixture, and a normal-game-load-before-Gallery
attempt also fault. The all-site fixture and the isolated ID 1 fixture reproduce
the same undefined instruction in the untouched Japanese ROM:
`0x26322A11`, PC `0xE5881234`; exported instruction address `0xE5881238`.
The cause remains unproven. These results do not establish a translation
regression, a retail-game defect, or the safety of the synthetic unlock for normal
progression. One- and two-frame A presses are not sampled by this menu and leave
it unopened; a subsequent four-frame press reproduces the fault. They are not a
workaround. Original source code has not been patched to hide the failure.

All 21 site names remain Japanese in V525. Their clean-source English review is
saved as `historic_site_name_review.json`. Eight names exceed their original
aligned slots: IDs 1, 2, 4, 16, 17, 18, 19, and 20. They require owned relocation
and consumer/layout checks; the reviewed complete names are not shortened to fit.
The original site-name getter supplies shared metadata, so a later change must
check gameplay and macro consumers as well as these Gallery screens.

## Evidence and next work

- `scripts/prepare_collection_gallery_v526.py`: bounded save fields and checksum.
- `scripts/capture_collection_sites_v526.py`: 21 individually labeled outcomes.
- `scripts/verify_collection_gallery_v526.py`: native lettering, selected icons,
  wrap, capture hashes, original-ROM control, and audit retention.
- `work/analysis/collection_gallery_v526/collection_survey_proof.json`.
- `work/analysis/collection_gallery_v526/single_site_captures.json`.
- Recorded inputs, logs, review, and inspection sheets in the same folder.
- Screenshots archived to `E:/Rota Nova translations/Screenshots/Test fixtures/collection_gallery_v526`.

Targeted Ruff passes. Production remains experimental V525, SHA-256
`c84d292ac756cd91c817637c1bdf9257c4f4a16512eadedba698e7d10024a605`.
Its ROM, manifest and reconstructable patch are unchanged. Canonical unchanged.
Next: apply the full site-name review through a registered, source-locked layer,
verify the separate list/map text consumers, and resolve the two fixture failures.
All 22 historical requirements and all 18 incomplete plaques remain. Full graphics
goal active; revisit older record-based checks when the full goal is complete.
