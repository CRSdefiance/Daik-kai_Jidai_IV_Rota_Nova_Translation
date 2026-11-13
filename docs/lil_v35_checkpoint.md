# Lil V35 translation checkpoint

Status: experimental; no cold-boot acceptance or baseline promotion.

- Candidate: `out/lil_deep_route_v35_candidate.nds`
- SHA-256: `6ca22311b6f1f02d49431ceebe8cfa1fd9cd8cf33eb04dcf0104ae3f1f41971a`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `lil-deep-route-v35`
- All 114 accepted layers remain baked into the base. The profile adds 45
  experimental batches: ten shared entity/UI/layout batches and Lil V1–V35.
  Full identities: [registry](../translations/release_stack.json) and
  [manifest](../out/lil_deep_route_v35_candidate.manifest.json).
- Changed paths: `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
  `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, `/data/SC2.DK4`.

V35 completes B120's sailing tutorial with 28 new natural American English
records. R0012 remains inherited from V21. Both FI macros, Lil/Kamil/system
states, and the bare-text first letters are preserved. All directions and
control actions were reviewed against clean Japanese.
See [control note](lil_sc2_b120_control_note.md).

## Verification

- Exhaustive audit: zero blocking issues; all 28 previews visually reviewed.
- Targeted V23–V35 regression suite: 26 tests passed; Ruff passed.
- Manifest: all 13 checks passed; registry and candidate hashes verified.
- Baseline invariant: passed with exactly the five declared cumulative paths.
- Saved-ROM: 28 V35 and one inherited V21 B120 record exactly verified;
  30 V34 records verified and both staging exclusions unchanged.
- Coverage: 2,550/6,608 translated, 4,032 remaining, 26 explicitly excluded.

## Cold-boot review and continuation

Restart fully without loading a save state. Check title menu, New Game,
an established scene, and town UI. Run the first sailing tutorial through all
answers and reminders. Verify FI expansion, portraits/nameplates, opening and
continuation letters, heading, L/R sails, automatic stylus sail angle, tapping
the flagship to stop, speed-meter instructions, and arrival in Bruges.
Repeat inherited scene checks before acceptance.

The route goal remains active and incomplete. Continue at B121 (109 records).
