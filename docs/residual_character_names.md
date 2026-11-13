# Residual ordinary character names

Integrated in experimental V150. Saved components/COMMON/manifest/canonical
preservation and exact clean-ROM patch reconstruction pass. Thirty focused tests
and lint pass. See `all_routes_unified_v150_checkpoint.md`; earlier build-pending
statements below describe preparation. Physical gameplay and older fidelity
remain open.

Clean ordinary-name indices 61 and 77 contain ヴェルス and アカブー.
The project already uses **Vels** in Raphael dialogue, including SC0 block 24
record 8 in `raphael_deep_route_v89.json`. **Akaboo** is a phonetic project
localization of アカブー, representing the long final vowel without inventing a
title or relationship. No official Latin spelling is claimed. Both choices are
recorded in `glossary.md`; the clean ROM supplies the source wording.

## Ownership and native checks

Each source label occupies twelve bytes at 15C1E8 or 15C7D0. Complete English
plus NUL fits without relocation. All-byte ARM9/decompressed-overlay scanning
finds exactly the two ordinary table start references, 121320 and 121520, with
no interior or overlay matches. Only those two twelve-byte slots change.

The actual SDK copier and BSS clear execute before all 207 ordinary
constructor/index/name getter selections. Pointer identity is preserved;
only the two reviewed names change. No Japanese syllabaries/ideographs remain
in these given-name results. This is table-scoped evidence, not full ARM9 text
coverage or proof that every older English role is semantically complete.

Five inherited full-width Latin initials are retained: indices 20 (Ｆernando),
35 (Ｆernan), 178 (Ｆollower), 186 (Ｆrancisca) and 194 (Ｆaticia). They are
English letters, not residual Japanese words. Their formatting/fidelity stays
in the older-English review; this release does not normalize them silently.

Both actual paired-character given-name preparations execute native raw-image
setup, ordinary getter/virtual dispatch, text context and glyph painting.
All four rows independently match complete pixels with intact headers,
descriptors and guards. Two inspected panels preserve the leading V/A and final
s/o without clipping or row overlap. Even-length four/six-character names emit
no extra blank glyph, correcting the prior shopkeeper-only odd-length assumption.
Four fixed/centered fleet rasters also preserve Pirate Vels and Pirate Akaboo.

Thirty focused tests and lint pass. Durable manuscripts/native review/release
inputs reproduce research bytes exactly. Registered V150 retains all 435 V149
batches and postprocessing stages; full rebuild/saved-ROM/patch checks are
underway. Native actor/scene eligibility, upstream live allocation, bitmap clear,
full physical composition/gameplay and other name consumers remain open.

Evidence: `work/analysis/residual_character_names_proof.json`,
`residual_character_names_paired_pixels_proof.json`,
`work/qa/residual_character_names_native/native_sheet.png`, and production inputs
under `translations/residual_character_names_*`.
