# V581: repeating equipment wood joins

## Defect and original source

The fresh V573 inventory run exposes a pale vertical join in long equipment
plaques. Their 40-column repeat included original towninfo column2, adjacent to
the source frame. It became conspicuous when repeated at local x42/82/122.
This is a material defect even though the prior paper/font equality checks pass.

The source-backed correction moves the contiguous unlettered wood sample from
original towninfo bounds[2,62,42,74] to[3,62,43,74]. These are half-open native
coordinates in the original256x192 atlas. Both were examined with surrounding
source pixels. No smoothing, synthesized grain, palette conversion or stretching
is introduced. The period remains40 and the existing tile remains44x16.

Over12 interior rows, the sum of adjacent-column RGB5 absolute differences at
the old repeat join was123; the revised join is31. Ordinary revised-strip
transitions range14..41, median26. These measurements support the visually
reviewed source and native comparisons; they are not a general visual-quality
score. Concealed Japanese background reconstruction remains an inference.

Only328 interior BGR555 words in the existing ARM9 tile change. Its borders,
bevels, every instruction, heap/cache setup, section address/extent and all
English strings remain exact V573. Every separate ROM file is unchanged,
including all921 PXL/FLS entries and57 embedded graphics block extents.

## Native verification

Fresh cold boots of V573 and V581 replay the same66 scheduled inputs on an
isolated copy of the Maria save. The authorized native inventory fixture changes
only11 selected equipment/history bytes. Original and copied source saves remain
byte exact. The only helper change admits the new exact ARM9 SHA; its native
transfer/getter/history code is unchanged. Item acquisition is synthetic.

The actual native item getters enumerate103 equipment names:28 weapons,26 armor
and49 accessories. These five cases reach the maximum current width in their
respective categories:

| Item | Native width | Frame | Slot x |
| --- | --- | --- | --- |
| Red-Haired Pirate Sword |142|15600|16|
| Saladin's Silver Armor |136|15400|64|
| Alexander's Campaigns |130|15200|112|
| Self-Sharpening Plane |130|15000|160|
| Aristarchus Telescope |130|14800|208|

All10,688 complete long-paper pixels match independently mapped original wood,
source bevels and complete native English masks. The three accessory papers
retain their automatic leftward positioning and full right edges. Every item
owner resolves to the active Maria captain; all5,120 original icon pixels pass.
All paired screen pixels outside the corrected paper interiors are identical.
Empty Weapon/Armor/Equipped Items hints add2,592 complete-paper pixel checks.
Native-size full screens and enlarged before/after crops were visually reviewed.

The actual ARM painter passes all235 supported widths10..244 on both screens
(470 cases), complete framebuffer/guard/stack/register checks, and nine invalid
contracts delegated without new writes. This establishes shared painter width
coverage, not ordinary gameplay for all103 items.

An independent21,200-frame New Game cold boot retains all56 distinct recorded
startup/story/town regression captures exactly. The new integrated patch
reconstructs the complete ROM byte for byte from the clean source.

The first release-verifier attempt incorrectly required RAM-export keys in the
startup-only report. That report intentionally has no RAM export. The verifier
now hashes exports when present; both inventory runs' requested RAM exports
remain required by their subsequent fixture/ownership checks. No emulator rerun
or ROM edit was needed for that verifier correction.

## Release identity

- Experimental candidate: `out/all_routes_combined_v581_candidate.nds`.
- Candidate SHA256: `542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68`.
- Profile: `all-routes-unified-v581`; all470 batches and114 accepted layers retained.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`.
- Base SHA256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Patch SHA256: `e411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415`.
- Changed internal file from V573: `/__arm9__.bin`, existing tile interior only.
- Build: `scripts/build_integrated_release.py --profile all-routes-unified-v581`.
- Verifier: `scripts/verify_equipment_join_v581.py`; targeted Ruff passes.
- No canonical promotion or user acceptance is inferred.

For manual cold-boot acceptance, check the title/New Game selection, an opening
story/town screen, Sailor Info empty slots and long equipment-name popups. The
automated runs cover targeted native frames and do not constitute a complete
route playthrough or hardware-device verification.

## Evidence, reproduction and remaining work

Proofs, original save provenance, input schedules, source context and the paired
review sheet are in `work/analysis/equipment_material_v580` (the E-drive junction).
`v581_release_proof.json` records complete source/native/patch checks.
`v581_native_width_proof.json` records all470 width cases and the pinned ARM/tile.
Regenerate that width proof with the verifier's `--probe-widths` option before
running the main verifier when reproducing the batch.

Raw runs are on E under Generated/work/emulation_v193:
`equipment_material_v580_current`, `equipment_join_v581_slots` and
`equipment_join_v581_fresh`. The first two use15600 frames, the recorded inventory
inputs, pause3000, exact captures3000/6200/7000/12000/14800/15000/15200/15400/15600,
RAM export and the copied source save. At3000 apply the five documented inventory
items and continue to15600; then stop normally. The fresh run uses21200 frames,
`fresh_inputs.json`, capture period400 and additional frames60/180 without a save.
Use new output directories for reproduction.

Ten paired full screenshots, the enlarged review sheet, capture reports and
hashed provenance are saved under E:/Rota Nova translations/Screenshots/Test
fixtures/V581 Equipment wood joins. They are labeled synthetic inventory evidence
and are not guide candidates. The ROM, manifest, patch and reconstruction are on
E through the existing output/analysis junctions.

This repairs one shared equipment texture defect. The global plaque/material
audit, five miniature captions' normal consumers, Confirm parent and remaining
legacy/event/movie contexts stay open. All18 original plaque inventory entries
remain incomplete and all22 historical requirement objects remain deep-identical.
The graphics goal remains active. Revisit older record-based checks at actual
full goal completion.
