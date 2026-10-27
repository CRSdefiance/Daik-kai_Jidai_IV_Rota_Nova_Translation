# Combined four-route ROM, Lil V78 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v78_candidate.nds`
- SHA-256: `2a0e5326680d90089171def03699994bcea233769003d7c7eb972a9801475314`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v44`, 345 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V78, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v78_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 13 source-reviewed Lil B178 records for the
Amsterdam wheat boom. See the [B178 control note](lil_sc2_b178_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. The exact-font contact
  sheet was visually reviewed.
- 58 focused Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,822** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 4,063, Maria 4,953. All 206
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v44/exact_records.json).
- Lil coverage: **4,112/6,608 translated**, 2,459 remaining and 37 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
the Amsterdam wheat-boom scene, portraits, nameplates, first letters, and
market notice. Do not promote this candidate before user cold-boot and
explicit acceptance.

Lil's route remains incomplete. Continue at B179. Three B022 controls
and the 37 exclusions still require sufficient source and control evidence
before translation.
