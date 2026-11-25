# Lil V36 translation checkpoint

Status: experimental; no cold-boot acceptance or baseline promotion.

- Candidate: `out/lil_deep_route_v36_candidate.nds`
- SHA-256: `718745efda5341c3253512a94f5bb00bdc560b0b6a6cb57c948b0abe7807cb17`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `lil-deep-route-v36`
- All 114 accepted layers remain baked into the base. The profile applies 46
  experimental batches: ten shared entity/UI/layout batches and Lil V1–V36.
  Full identities: [registry](../translations/release_stack.json) and
  [manifest](../out/lil_deep_route_v36_candidate.manifest.json).
- Changed paths: `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
  `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, `/data/SC2.DK4`.

V36 completes B121 with 109 new natural American English records: the ambush,
both rescue branches, Kamil's reconciliation and family history, and the farewell.
Fourteen presentation states, both bare combat choices and ten FI macros remain
intact. See [control note](lil_sc2_b121_control_note.md).

## Verification

- Exhaustive dialogue audit: zero blocking issues; all 109 previews reviewed.
- Targeted V23–V36 suite: 28 tests passed; Ruff passed.
- Manifest: all 13 checks passed; base, registry and candidate hashes verified.
- Baseline invariant: passed with exactly the five declared cumulative paths.
- Saved-ROM: 109 V36 records, 28 V35 records and the inherited V21 tutorial
  refusal verified exactly.
- Coverage: 2,659/6,608 translated, 3,923 remaining, 26 explicitly excluded.

## Cold-boot review and continuation

Restart fully without loading a save state. Check title menu, New Game,
an established scene and town UI. Test both ambush choices, both rescue
branches, Kamil's return and the Proof-map key farewell. Verify portraits,
nameplates, FI expansion, opening and continuation letters, rewards and scene
transitions. Repeat inherited scene checks before acceptance.

The route goal remains active and incomplete. Next untranslated block: B122
(30 records). The three unresolved B022 records and explicit exclusions still
require sufficient source and control evidence.
