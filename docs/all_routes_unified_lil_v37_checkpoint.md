# Combined four-route ROM checkpoint

Status: experimental. The Lil route goal is paused at the user's request.
This build combines the existing reviewed work; it does not claim every route
record is translated or authorize baseline promotion.

## Build identity

- Candidate: `out/all_routes_unified_lil_v37_candidate.nds`
- SHA-256: `b5eecc91403fbdef91e955f04a8ec0251863c0ba701f6960ae19401c5b86757f`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Profile: `all-routes-unified-v3`
- All 114 accepted layers remain baked into the immutable base.
- 304 experimental batches apply: the complete unified V2 stack and Lil
  V24–V37. This combines Raphael V93, Hodram V32, Maria V111, Lil V37,
  and the registered shared interface, graphics, layout, encounter-direction,
  literal-percent and COMMON repairs.
- Exact layer identities and hashes are recorded in the
  [registry](../translations/release_stack.json) and
  [candidate manifest](../out/all_routes_unified_lil_v37_candidate.manifest.json).

Changed internal files: `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`,
`/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`,
`/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`.

## Current scene and verification

The current Lil B122 scene is completed with 30 natural-English records:
Clifford's burning Galahad, his refusal of rescue, Lil's grief, Kamil's reflection,
and the recovery of the stolen Proof and farewell letter. The existing
02/09/97/FE states and three FI macros remain intact. FE presents Clifford's
offscreen voice and letter; source staging line breaks are removed, with guarded
pair-phase wrapping applied by the encoder. All 30 previews were reviewed and
the exhaustive audit has zero blockers. No additional scene was started after
the pause request.

- Seven targeted stack, scene and inherited-rescue tests passed.
- Ruff passed on the new materializer, registrar, verifier and tests.
- All 13 integrated-build checks passed.
- Candidate, canonical base and registry hashes were verified.
- The baseline invariant passed with exactly the nine paths above.
- The full saved-route record verification is recorded in
  [exact-record report](../work/qa/all_routes_unified_v3/exact_records.json).
  All 18,399 experimental route records match exactly: Raphael 5,802, Hodram
  5,004, Lil 2,640, Maria 4,953. All 195 effective route exclusions are unchanged.
  Lil's other 49 translated opening records remain baked into the base.
- Lil coverage: 2,689/6,608 translated, 3,893 remaining, 26 explicitly excluded.

## Cold-boot review and later resumption

Restart without loading a save state. Check title menu, New Game character
selection, each route opening and an established scene, town UI, shared
names, supplies/cargo, encounter directions, and Help. Review Lil's recent
sailing tutorial, both ambush choices and rescue branches, Kamil's return,
and Clifford's burning ship and letter reward. Verify portraits/nameplates,
macro expansion, first and continuation letters, rewards and transitions.
Runtime acceptance remains pending; do not promote the candidate automatically.

When the user resumes Lil, continue at B123 (seven records). The three B022
records and explicit exclusions remain pending sufficient control evidence.
