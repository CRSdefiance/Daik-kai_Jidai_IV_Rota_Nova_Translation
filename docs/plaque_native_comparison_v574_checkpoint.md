# V574: all 18 plaques compared in actual original and English UI

The previous goal turn completed the V573 Confirm repair and exact patch. This
checkpoint adds current source/display evidence. V573 remains the experimental
candidate, SHA256
`f987f1c56ba5641544e5c84698c59351e39465b15001601adddf697698d89a77`.

## Paired ordinary UI captures

The clean Japanese ROM and V573 each cold booted with an isolated copy of the same
Syracuse battery save. Both ran 7,100 frames with identical inputs, reaching
Assign Sailors, Sailor Info, the empty Weapon slot and occupied Blue Oak Shield.
Only ordinary menu/controller/touchscreen actions were used. No inventory,
location, condition or code fixture was applied. The already-owned shield is not
new acquisition evidence. Actor/company names are already Latin in the source
save; the clean ROM captures are not pristine New Game screenshots.

The source save remains SHA256
`958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.
Both emulator processes finalized normally; neither used a savestate. The complete
14-action schedule is `work/analysis/plaque_current_v574/complete_replay_inputs.json`.

The paired sheets use actual framebuffer crops on both sides. This corrects the
limitation of the older stored-art comparisons: the six original stat labels and
the equipment heading are drawn at runtime and were absent from original PXL
crops. The new source side includes their complete Japanese lettering. Original
pink stat plates/gauges and the white equipment hint remain visible as the source
design; the English wood redesign is intentional under the user's instructions.

## Results and wording

All 17 stored English masks are complete. All 14,272 native static plaque pixels
match their actual current PXL art, including wood, bevels and letters. All eleven
original stored-label plaques also match their original PXL regions. The six
original runtime stat labels are reviewed in their actual Japanese screenshots.
The current plaque files remain byte-identical to verified V555.

Equipped Items, Weapon and Blue Oak Shield pass 3,552 complete native hint pixels,
including full font masks and the actual compiled wood/bevel tile. The entire
current ARM9 remains exact V546. The original hint and shield name are visible in
the paired source captures, including 装備アイテム and 蒼き樫の盾.

The context supports the existing natural English labels:

- Fleet Crew/Unassigned distinguish assigned and unassigned sailors.
- Endurance labels the available sailing-day estimate, not a distance.
- Quarters labels the marine quarters; Cannon precedes the cannon type/count.
- Fore/Aft and Square distinguish the two sail-performance figures.
- Health/Mood label condition states. Spirit is the numeric 精神 attribute;
  Mood describes the separate mental-state field with the same Japanese heading.
- Level/HP and Stamina/Agility/Charm/Wits/Spirit/Luck match the source attributes.
- Equipped Items, Weapon and Blue Oak Shield remain faithful, readable English.

Both enlarged native sheets were visually inspected. No new missing letters,
large pale blocks or distinct vertical streaks were identified in these observed
crops. Concealed grain is still reconstruction, not exact recovery. Source-local
repair history and the global plaque material defect remain documented.

## Current complete preservation audit

A fresh clean/current check passes all 660 PXL files and 261 FLS textures: all
original headers/flags, dimensions, indexed palette banks and payload extents
remain exact. The PXL check includes all banks before the pixel offset and treats
16-bit images as direct color rather than mistaking their pixels for a palette.
All 57 embedded ILNK blocks retain their original extents. There are 84 changed
PXL/FLS entries. These checks do not prove text accuracy, hidden-source fidelity
or native use of every entry. The requirements audit's stale V546/V525 preservation
pointers now name V573 and the fresh proof; former pointers are retained.

The bounded miniature-caption investigation recorded 48 PC-relative frame-owner
reference candidates. It did not resolve the remaining five ordinary miniature
caption consumers. No non-use or complete consumer-coverage claim follows from
that census. Other legacy/FLS/art-restoration contexts remain open.

## Artifacts and reproduction

- `scripts/review_current_plaques_v574.py` and `native_review_proof.json` under
  `work/analysis/plaque_current_v574/`.
- `scripts/audit_graphics_preservation_v574.py` and
  `work/analysis/plaque_current_v574/current_preservation_proof.json`.
- Capture reports: E:/Rota Nova translations/Generated/work/emulation_v193/
  plaque_compare_v574_original and plaque_compare_v574_current.
- Two paired sheets and eight full original/current captures with hashes:
  E:/Rota Nova translations/Screenshots/Audit comparisons/V574 Plaques.
- Four unaltered ordinary English screenshots with provenance:
  E:/Rota Nova translations/Screenshots/Guide candidates/V573 Plaques.
  Guide publication is not approved.

Use the complete replay schedule, the named unchanged source battery save,
`--frames 7100 --capture-at 4300 6300 6700 7100 --touchscreen` and
`--battery-save` with `scripts/headless_desmume_v193.py` to reproduce each run in a
new output directory. Run the two named audit scripts to reproduce the checks.
This is targeted emulator evidence, not full-route or hardware verification.

All 18 plaque/hint entries remain `fully_completed:false`, and all 22 historical
requirements are unchanged. The graphics goal remains active. Revisit older
record-based checks at actual full completion.
