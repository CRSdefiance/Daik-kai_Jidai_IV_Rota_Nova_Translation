# V632: fresh V627 plaque review and guide candidates

## Result

A fresh ordinary V627 cold boot verifies all18 original plaque/hint entries in
Assign Sailors and Sailor Info. The two review sheets compare actual Japanese
screens with actual current English screens, including the six runtime Japanese
stat labels and the equipment heading. These are not mockups or stored-art-only
comparisons.

All18 entries remain incomplete, as requested. The packet makes the retained
user visual-review requirement concrete; no answer or approval is inferred.
Other variants and the broader graphics goal remain open. No ROM or artwork
changes result from this checkpoint.

## Actual run and source comparison

- Current candidate: experimental `out/all_routes_combined_v627_candidate.nds`.
- SHA256: `0a03862a0a0a75c748e2f806016d2316f881eb9799907590715c41d251bf2a09`.
- New run: `E:/Rota Nova translations/Generated/work/emulation_v193/plaque_review_v632_current`.
- Frames:7100; source/current menu anchors4300,6300,6700,7100.
- Schedule: `work/analysis/plaque_current_v574/complete_replay_inputs.json`.
- Donor: the unchanged Syracuse copy, SHA256
  `958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.

The run uses normal controller/touchscreen inputs. No location, inventory,
equipment, condition or code fixture is applied, and no savestate is loaded.
The shield was already owned in the donor; these screenshots do not demonstrate
new acquisition. Existing Latin names also come from the donor.

The original side reuses V574's hash-verified clean-ROM cold boot with the same
donor, same14 actions and same core options. It is labeled historical original
evidence, not a second new run or pristine Japanese New Game. The source6 stat
labels and equipment header are actual runtime pixels, not guessed atlas crops.

## Complete current checks

- All17 static English plaques match their independent complete original-font
  masks, including first/final letters and all blank cells.
- All14,272 static plaque pixels match the current ROM's native PXL planes.
  This includes the material and bevels, not just the English lettering.
- Equipped Items, Weapon and Blue Oak Shield match3,552 complete native hint
  pixels, including the actual1408-byte wood tile and full font masks.
- The two current plaque atlases remain byte-exact to V555. The hint tile is
  byte-exact to V581's source-grain join correction, rather than the older V546
  tile used in the historical V574 comparison.
- Headers, indexed palette data and dimensions in the reviewed atlases retain
  the original source bytes. Existing broader preservation proofs remain their
  own evidence; this is not a newly executed921-asset audit.

Both enlarged review sheets were visually inspected. The formerly reported
broad pale blocks and distinct repeated vertical bands were not observed in
these current crops. Texture concealed by the original lettering remains a
documented reconstruction; it is not exact recovery of hidden original pixels.
Original pink stat plates and white equipment paper are shown honestly on the
source side. Their English wooden redesign follows the requested style change.

## Wording and context retained

| Japanese | Current English | Context |
|---|---|---|
|艦隊水夫数|Fleet Crew|Fleet sailor count|
|未編成水夫数|Unassigned|Sailors not allocated to ships|
|航行可能日数|Endurance|Estimated sailing duration in days|
|海兵詰所|Quarters|Marine quarters, not a marine-person count|
|砲種|Cannon|Type of cannon displayed beside the plaque|
|縦帆性能|Fore/Aft|Fore-and-aft sail performance|
|横帆性能|Square|Square-sail performance|
|身体|Health|Current physical condition|
|精神|Mood|Current mental condition|
|レベル|Level|Character level|
|HP|HP|Current hit points|
|体力|Stamina|Physical stamina attribute|
|敏捷|Agility|Agility attribute|
|魅力|Charm|Personal charm attribute|
|知力|Wits|Intellectual ability attribute|
|精神|Spirit|Mental fortitude attribute, distinct from Mood|
|運勢|Luck|Luck attribute|
|装備アイテム|Equipped Items|Currently equipped items|

No new translation is authored. The prior source/context decisions are retained
and checked against the unchanged current strings and actual display.

## Review sheets and saved evidence

- [Assign Sailors](<E:/Rota Nova translations/Screenshots/Audit comparisons/V632 Plaques/Assign_Sailors_V627_SOURCE_REVIEW_4x.png>)
- [Sailor Info](<E:/Rota Nova translations/Screenshots/Audit comparisons/V632 Plaques/Sailor_Info_V627_SOURCE_REVIEW_4x.png>)

The archive contains two4× nearest-neighbor sheets, all36 original/current native
crops, four whole original and four whole current screens, reports and hash-bound
proof. Crops and enlarged sheets are explicitly separate from unmodified captures.
Four current whole screens are also saved under
`E:/Rota Nova translations/Screenshots/Guide candidates/V627 Plaques`, with donor
and run provenance. They are candidates for the later guide, not publication or
new-game/acquisition evidence.

Verifier/generator: `scripts/review_current_plaques_v632.py`; targeted Ruff passes.
Proof: `work/analysis/plaque_review_v632/current_plaque_review_proof.json`.
Reproduce the new run using the named ROM, donor and schedule with
`--frames 7100 --capture-at 4300 6300 6700 7100 --dump-capture-ram --touchscreen`.
No pause or fixture flag is needed.

## Scope preserved

The user-review question concerns current wood grain and borders. It is not
permission to generate more previews or continue work; those are already allowed.
All18 original `fully_completed:false` objects and all22 historical requirement
objects remain exact. Canonical/latest-verified/latest-compiled pointers, the
release registry, ROM and patch remain unchanged. Other health/mood/equipment
variants and wider legacy, miniature/Confirm, village, movie and material gates
stay open. Online low-resolution exemptions and original brown marks remain.
The full graphics goal remains active and incomplete.
