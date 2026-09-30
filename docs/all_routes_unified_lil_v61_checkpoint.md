# Combined four-route ROM, Lil V61 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v61_candidate.nds`
- SHA-256: `edee2e49b136c0623e725b7c445a23c7e43a6012a143f537d01ac9dc5534dfe3`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v27`, 328 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V61 and shared interface,
  graphics, layout, encounter, percent-safety and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v61_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 40 source-reviewed Lil B154 text records covering
Al's dismissal and recruitment. One ten-byte scene event remains unchanged.
See the [B154 control note](lil_sc2_b154_control_note.md).

## Verification

- Exhaustive B154 dialogue audit found zero blockers. All four exact-font
  contact sheets were visually reviewed, with ambiguous `W` initials checked
  in individual previews.
- 41 focused Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,217** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,458, Maria 4,953. All 202
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v27/exact_records.json).
- Lil coverage: **3,507/6,608 translated**, 3,068 remaining and 33 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help and shared names. In Lil's route, check the
B154 employer confrontation, Al's dismissal and recruitment, companion
reactions, portraits, nameplates, macros, first and continuation letters, and
transitions. Do not promote this candidate before user cold-boot and explicit
acceptance.

Lil's route remains incomplete. Continue at B155 (49 records). Three B022
controls and the 33 exclusions still require sufficient source and control
evidence before translation.
