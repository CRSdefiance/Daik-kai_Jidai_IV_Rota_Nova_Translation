# Combined four-route ROM, Lil V99 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v99_candidate.nds`
- SHA-256: `ef4be089c3f1b2200a3405e542d7b520bc4956a2438fc80d3d32200c55b6caa5`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v65`, 366 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V99, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v99_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 17 source-reviewed Lil B205 parrot text records and
excludes one proven nontext packed event unchanged. See the [B205 control
note](lil_sc2_b205_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. Both exact-font contact
  sheets were visually reviewed, including all parrot echoes.
- 53 focused Lil stack tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **20,266** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 4,507, Maria 4,953. All 209
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v65/exact_records.json).
- Lil coverage: **4,556/6,608 translated**, 2,012 remaining and 40 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
B205's parrot echoes, capture timing, final joke, portraits, nameplates,
and first letters. Do not promote this candidate before user cold-boot and
explicit acceptance.

Lil's route remains incomplete. Continue at B206. Three B022 controls
and the 40 exclusions still require sufficient source and control evidence
before translation.
