# Combined four-route ROM, Lil V74 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v74_candidate.nds`
- SHA-256: `1d1088494e40021a7b517e7c2bb784c545a6a0fb931e137d74ee5e5895a4ff25`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v40`, 341 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V74, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v74_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 44 source-reviewed Lil B173-B174 records covering
the Golden Crown tomb lead, Mihwa's crown handoff, and Julian's recruitment.
See the [B173-B174 control note](lil_sc2_b173_b174_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. All three exact-font
  contact sheets were visually reviewed.
- 54 focused Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,757** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,998, Maria 4,953. All 205
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v40/exact_records.json).
- Lil coverage: **4,047/6,608 translated**, 2,525 remaining and 36 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
the Golden Crown lead, Mihwa's gift, Julian's recruitment, portraits,
nameplates, first and continuation letters, and transitions. Do not promote
this candidate before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B175. Three B022 controls
and the 36 exclusions still require sufficient source and control evidence
before translation.
