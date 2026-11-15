# Combined four-route ROM, Lil V82 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v82_candidate.nds`
- SHA-256: `81997a3f6e70e5db51b80caff9f4e2754cac66329fca5f586c79a8e75cbcee24`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v48`, 349 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V82, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v82_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 29 source-reviewed Lil B184-B186 records for
Sofala tea, Stockholm furs, and Alexandria sweets. See the
[B184-B186 control note](lil_sc2_b184_b186_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. Both exact-font contact
  sheets were visually reviewed.
- 62 focused Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,913** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 4,154, Maria 4,953. All 206
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v48/exact_records.json).
- Lil coverage: **4,203/6,608 translated**, 2,368 remaining and 37 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
the Sofala, Stockholm, and Alexandria market scenes, portraits, nameplates,
first letters, and notices. Do not promote this candidate before user
cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B187. Three B022 controls
and the 37 exclusions still require sufficient source and control evidence
before translation.
