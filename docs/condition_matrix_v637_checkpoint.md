# V637: current-ROM Sailor Info condition matrix

## Result

One fresh V636 cold boot covers all42 combinations of seven Health states and
six Mood states on both Maria and Xien:84 actual Sailor Info views. This adds the
previously untested cross combinations and replaces reliance on V518 for current
condition-display evidence. V520's historical seven paired states per actor are
retained as earlier evidence, not relabeled as current tests.

No production ROM, patch, profile, source save or canonical pointer changes.
V637 identifies this evidence checkpoint; there is no V637 release ROM.
The preceding status-only response supplied no new test evidence. This turn
makes progress through the new terminal-successful emulator run and its proof.

## Exact candidate and setup

- Candidate: `out/all_routes_combined_v636_candidate.nds`.
- SHA256: `c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d`.
- Profile: `all-routes-unified-v636`; inherited470 batches and114 accepted layers.
- ARM9 SHA256: `1f6ed33c8ee91bdeb1667e3f7524f3731ac7b0ba89a07f4be4ee1422cd7851bb`.
- Run: `work/emulation_v193/condition_matrix_v637`,38600 frames, DeSmuME
  interpreter, original256x192 screens, touchscreen enabled, no savestate load.
- Donor: `E:/Rota Nova translations/Saves/maria-nagasaki-namahage-v514.dsv`,
  SHA256 `fbae21aa2c5a695bde0eddfc10a3bbeb80d01478bd6a9ed743d824595dc3096e`.
  The emulator receives a separate byte-exact battery-save copy before cold boot.

Ordinary inputs open Sailor Info. Each case changes only the selected actor's
original Health and Mood bytes in isolated live RAM, then B/A rebuilds the view.
Maria follows the original dedicated active-captain record; Xien follows the
ordinary indexed crew record. Original actor identity, captain and pointer bounds
are checked before each change. There are86 receipts:84 matrix cases, Maria's
reset and Xien's initial selection setup. All86 independently replay exactly
from their read-only before-RAM exports, including allowed write addresses and
whole before/after hashes. Six negative controls reject the wrong ROM, wrong RAM
size, unreviewed actor, invalid health, invalid mood and a boolean state value.

Some synthetic combinations are unusual, such as Dead/Excited. They exercise the
display catalogue and do not establish natural injuries, recovery, deaths or
story events. Historical RAM is used only for fixture preflight; it is never
loaded into the emulator. The donor remains byte-identical and no Save input runs.

## Complete actual pixels

- All168 Health/Mood fields pass independent original-font masks over their full
 48x16 areas:129024 foreground/blank-cell comparisons. First and final visible
 glyphs are included; deliberately removing a pixel from either is rejected.
- Every actual field is bound to the captured actor state and executed original
 selector result. Original Japanese labels/pointers are retained in the proof.
 Health: Healthy, Tired, Hurt, Wounded, Dying, Sick, Dead. Mood: Excited, Good,
 Relaxed, Normal, Upset, Confused. Existing reviewed translations are unchanged.
- All84 complete Maria Huamei Li/Xien Yan name masks pass.
- All11 Sailor Info plaque/header crops match the prior source-reviewed V632
 packet in every view:924 full crops,697872 pixels. These include Health, Mood,
 Level, HP, the six stat plaques and Equipped Items. Their underlying personinfo
 and dividecrewinfo resources remain byte-exact to that packet's V627 candidate.
- Visible non-font background pixels inside condition fields remain consistent
 across all state redraws. There is no stale lettering or unexpected non-font
 residue in those comparisons.

## Original skill changes and selection effect

An initial whole-context equality assertion correctly found differences outside
Health/Mood. Investigation showed that changing conditions also changes original
derived skills. Their source methods at0207DCC8 and the surrounding0207D000..
0207EF00 region remain byte-exact to the Japanese ROM. The original painter's
ten descriptor positions and its getter-call loop also remain exact.

All840 complete60x12 skill fields are independently checked against the actual
original name getter0207EEB0, skill calculation0207DCC8 and current `%7s%3d`
format. This verifies changing numbers, labels, spaces, first/final glyphs and
unused rows, instead of ignoring their differences. For example, Maria's Command
value changes from118 in Excited to120 in Good with the same base actor data.
This is retained game behavior, not a translation correction.

The two-pixel selection ring around equipment slot4 varies between captures.
Its outer rectangle is[206,222,242,258], with the32x32 icon interior
[208,224,240,256] retained in the exact comparison. Only the272 ring pixels are
excluded; its animation timing is not newly verified here. After independently
checking the condition and skill fields and declaring this ring exclusion,
7322272 remaining context pixels match each actor's first view exactly across82
comparisons. This is explicitly not an unqualified whole-frame equality pass.

The first verifier draft also used the receipt key `actor` instead of `actor_id`
and attempted to remove an ink pixel from a leading alignment space in a skill
field. Both verifier issues were fixed before accepting the proof; neither
changed the ROM, emulator inputs or captured evidence.

## Reproduction and archive

- Prepare: `scripts/prepare_condition_matrix_v637.py`.
- Fixture: `scripts/native_condition_fixture_v637.py`; exact V636 ARM9 guard.
  The existing frontend dispatches to it only for that hash; the historical V520
  helper remains unchanged for its original build.
- Run the frontend with the prepared `commands.jsonl` on standard input,
  `--rom out/all_routes_combined_v636_candidate.nds --out
  work/emulation_v193/condition_matrix_v637 --frames 38601 --pause-at 4400
  --capture-every 999999 --dump-pause-ram --dump-ram --allow-condition-fixtures
  --touchscreen --battery-save <donor> --inputs-json
  work/analysis/condition_matrix_v637/initial_inputs.json`.
- Verify: `scripts/verify_condition_matrix_v637.py`.
- Proof: `work/analysis/condition_matrix_v637/current_condition_matrix_proof.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V637 Condition matrix`.
  All84 selected views are unmodified captures. Review contact sheets are clearly
  labeled derived enlargements. Synthetic states are excluded from guide images.

Both derived sheets were visually inspected, covering all84 condition-field
strips. Four unmodified full screens were also inspected: Maria Healthy/Good
(5200), Healthy/Confused(6800), Wounded/Confused(14000), and Xien Dead/Confused
(38600). No missing leading/trailing letters or condition-field clipping was
identified in these views. This is not a claim that all84 full screens received
individual visual review. `visual_review.json` records their hashes and scope.

## Remaining scope

All18 original plaque/hint objects remain `fully_completed:false`. This batch
adds current evidence for two actors' condition combinations and the11 Sailor
Info plaques; it does not close Assign Sailors, every other character/equipment
combination, normal acquisition, hardware checks or user approval of wood texture
and borders. Concealed original wood grain remains a documented reconstruction,
not recovered original pixels.

All22 historical requirement objects/scopes remain exact. The registry, ROM,
patch, canonical and every release pointer remain unchanged. Miniature/Confirm
ordinary parents, village cards, legacy/environment/raw comic consumers, other
movie/material variants and final visual acceptance remain open. Older
record-based checks are still due at actual full-goal completion. Goal active.
