# V469 genuine occupied Armor verification

V468 remains unchanged. This turn completes the first legitimate occupied Armor
context, without claiming all equipment variants or the full graphics goal.

## Ordinary acquisition and ownership

The normally saved London fleet sails through the Channel to the earned Blue Oak
Shield clue. Search is reached through Inspect→Search Mode, not the Survey room.
Closing the sails holds position before entering the modes. Original item/fleet
point virtuals return19464,5192 and19463,5178; squared distance197 is within the
original32-map-unit radius squared1024. No position, item, stat or unlock edits.

Normal Search produces the discovery message and Blue Oak Shield description.
Completing the dialogue changes original found getter4A368 from0→2 and consumes
clue getter4A394 from1→0. The actual player Items menu contains the Armor item.
Items→Y Equip→Hodram gives the complete equipped confirmation. Original owner
descriptor49DE8 then returns kind2/index1; unused descriptor fields are ignored.

The original clean COMMON block30 describes a small round shield made from
mysterious oak that is very hard and blue. The existing English is faithful and
natural: “Mysterious, rock-hard blue oak forms this small, round shield.”

## Actual occupied-slot pixels

- Full Blue Oak Shield tooltip:182 independent font pixels, including first B,
  final d and every intervening glyph/blank cell; bounds66,210–156,221.
- All1504 native94×16 paper/edge/corner pixels match; paper bounds64,208–158,224
  remain inside the256×384 framebuffer.
- All1024 original item49 icon pixels match the source atlas in the Armor slot.
- The complete owner name, ten complete skill lines, discovery/equip/save messages,
  item category and both description lines pass.
- Item data uses native five-pixel tracking; the tooltip uses ordinary six-pixel
  cells. Early broad-region/font-format checks failed diagnostically, not because
  characters were missing. Explicit format/color checks prove complete text.
- All20 Sailor Info plaque instances match the ROM in pre-save and cold-load views.

## Save and cold-load evidence

Normal slot6 overwrite finishes with4100 more frames before terminal stop. An
isolated byte-exact battery copy cold-loads, and ordinary Info→Sailors selects the
Armor slot. All98,304 pixels of the whole equipped screen match the pre-save view.
The original London donor is unchanged. Acquired/equipped state survives through
original getters. Every report and captured PNG is hash checked.

Verifier: `scripts/verify_occupied_armor_v469.py` (Ruff passes).
Proof: `work/analysis/shield_search_v469/armor_proof.json`.
Reports: `work/emulation_v193/shield_search_v469/capture_report.json` and
`work/emulation_v193/shield_armor_reload_v469/capture_report.json`.

Normal equipped save on E:
`Saves\hodram-blue-oak-equipped-v468.dsv`

SHA-256: `6907e30c307b7f28ab3abc7da2fd330c47990d69b7b92b327a50f77e56437f0a`

Two actual finalized guide PNGs are copied unchanged to E Screenshots. No image
editing, synthetic state or hardware/full-playthrough claim.

## Remaining scope

This verifies Blue Oak Shield in one Healthy/Normal Hodram context. Occupied
Weapon, other armor names/conditions/owners, legacy/environment/Gallery/ending
consumers and every other open historical requirement remain. All22 requirements
and all18 plaque entries are retained with fully_completed:false. V468 ROM/patch/
manifest remains the existing verified release; no new ROM or canonical promotion.
Revisit older record-based checks at actual full-goal completion.
