# Lil V33 translation checkpoint

Status: experimental; no cold-boot acceptance or baseline promotion.

## Build identity

- Candidate: `out/lil_deep_route_v33_candidate.nds`
- Candidate SHA-256: `c11b4df0f5b35de8f445d9a440b313e525760fd3efa7a957b7f8bd02659e15ff`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `lil-deep-route-v33`
- All 114 accepted layers remain baked into the canonical base. The profile adds
  43 experimental batches: ten shared entity/UI/layout batches and Lil V1–V33.
  The complete batch identities are in [the registry](../translations/release_stack.json)
  and [the manifest](../out/lil_deep_route_v33_candidate.manifest.json).
- Changed internal paths: `/COMMON/MESFILE.DK4`, `/__arm9__.bin`,
  `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, `/data/SC2.DK4`.

## Translation and verification

V33 adds 37 natural American English records in B115, covering Lil and Janus's
tablet discovery and the shared Maria recruitment branch. All opening text
glyphs and real presentation states are checked; source-leading LF in R0089
is staging, not a speaker selector. The FO runtime macro remains intact.
See [control evidence](lil_sc2_b115_control_note.md).

- Fixed-allocation dialogue audit: zero blocking issues.
- All 37 previews visually reviewed, including opening and continuation letters.
- V23–V33 targeted regression suite: 22 passed.
- Ruff: profiles, materializer, registration script, and V33 tests passed.
- Integrated manifest: all 13 checks passed; registry and ROM hashes verified.
- Baseline verifier: passed with exactly the five declared cumulative paths.
- Saved-ROM exact-record checks: all 37 V33 and 19 V32 records passed;
  both inherited B113 exclusions unchanged.
- Coverage: 2,492 of 6,608 source records translated; 4,092 remain and
  24 are explicitly excluded. This is a checkpoint, not a completed route.

## Cold-boot review

Restart the emulator fully without loading a save state. Check the title menu,
New Game character selection, an established story scene, town UI, the tablet
scene, and the shared Maria branch. Verify portraits/nameplates, FO faction
expansion, first and continuation letters (especially R0089), recruitment,
reward, and scene transitions. Repeat inherited temple/Sphinx/cult/lamp,
Colosseum choices, monk, rescue, jade, and cacao gate checks before acceptance.

Resume translation at B116, then B117–B118. Their source and staging fragments
still need the usual control mapping and English review.
