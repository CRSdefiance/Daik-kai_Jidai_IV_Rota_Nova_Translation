# Lil V34 translation checkpoint

Status: experimental; no cold-boot acceptance or baseline promotion.

- Candidate: `out/lil_deep_route_v34_candidate.nds`
- Candidate SHA-256: `a84f93aa47163fb7fc3840c7b23ef5007c0f76f2a11253be744e6976b0f33680`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `lil-deep-route-v34`
- All 114 accepted layers remain baked into the base. The profile adds 44
  experimental batches: ten shared entity/UI/layout batches and Lil V1–V34.
  Complete batch identities: [registry](../translations/release_stack.json)
  and [manifest](../out/lil_deep_route_v34_candidate.manifest.json).
- Changed internal paths: `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
  `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, `/data/SC2.DK4`.

V34 adds 30 natural American English records in B116–B118: the India building
tip, figurehead discovery, and tribal knife reward. Source-correlated C6/D1/DC/B3
states are preserved; ordinary 82/91 starts retain their first English letters.
The short non-prose B117/B118 R0004 fragments remain unchanged.
See [control evidence](lil_sc2_b116_b118_control_note.md).

## Verification

- Exhaustive dialogue audit: zero blocking issues; every preview reviewed.
- V23–V34 regression suite: 24 tests passed.
- Ruff: profiles and new materializer, registration script, and tests passed.
- All 13 manifest checks passed; registry and candidate hashes verified.
- Baseline verifier passed with exactly the five declared cumulative paths.
- Saved-ROM checks: all 30 V34 and 37 V33 records exactly match their batches;
  both new staging exclusions remain unchanged.
- Coverage: 2,522/6,608 translated; 4,060 remaining; 26 explicitly excluded.

## Cold-boot review and continuation

Restart the emulator fully without loading a save state. Check title menu,
New Game selection, an established story scene, and town UI. Sample the gift
trigger and India/map hint, figurehead variants and acquisition, recovered
knife ownership, 24,000-gold reward, and return to the fleet. Verify portraits,
nameplates, first and continuation letters, pagination, and scene transitions.
Repeat the inherited V33 and earlier scene checks before acceptance.

The full route goal remains unfinished. Continue with the 28 untranslated B120
sailing-tutorial records, then B121. B120 contains FI runtime macros and Lil,
Kamil, and system states; 82/95 starts are ordinary Japanese text. One B120
record is already translated by an earlier layer and must not be overwritten.
