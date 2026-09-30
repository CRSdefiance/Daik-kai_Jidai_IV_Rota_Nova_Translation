# Combined four-route ROM, Lil V77 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v77_candidate.nds`
- SHA-256: `1032a6defbcf0ff794f223e53751206737985936bb11a0844bbcdffab94c57a6`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v43`, 344 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V77, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v77_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 10 source-reviewed Lil B177 records for the
Genoa tomato boom. See the [B177 control note](lil_sc2_b177_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. The exact-font contact
  sheet was visually reviewed.
- 57 focused Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,809** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 4,050, Maria 4,953. All 206
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v43/exact_records.json).
- Lil coverage: **4,099/6,608 translated**, 2,472 remaining and 37 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
the Genoa tomato-boom scene, portraits, nameplates, first letters, and
market notice. Do not promote this candidate before user cold-boot and
explicit acceptance.

Lil's route remains incomplete. Continue at B178. Three B022 controls
and the 37 exclusions still require sufficient source and control evidence
before translation.
