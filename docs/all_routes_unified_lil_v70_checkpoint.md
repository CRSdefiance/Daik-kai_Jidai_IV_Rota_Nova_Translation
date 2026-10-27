# Combined four-route ROM, Lil V70 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v70_candidate.nds`
- SHA-256: `61cf07962603ba16240375636afc0596dbae239f3274af8952aa12074cb12ec3`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v36`, 337 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V70, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v70_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 36 source-reviewed Lil B169 text records covering
Mikhail's Proof of Conqueror explanation and search advice. See the
[B169 control note](lil_sc2_b169_control_note.md).

## Verification

- Exhaustive B169 dialogue audit found zero blockers. Both exact-font
  contact sheets were visually reviewed.
- 50 focused Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,618** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,859, Maria 4,953. All 205
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v36/exact_records.json).
- Lil coverage: **3,908/6,608 translated**, 2,664 remaining and 36 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
Mikhail's Proof explanation, portraits, nameplates, macros, first and
continuation letters, and transitions. Do not promote this candidate
before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B170. Three B022 controls
and the 36 exclusions still require sufficient source and control evidence
before translation.
