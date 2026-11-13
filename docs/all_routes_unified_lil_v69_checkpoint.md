# Combined four-route ROM, Lil V69 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v69_candidate.nds`
- SHA-256: `8b3ce57b83b3276cca342b2026328301ec5dd6a446d3615c0958262ef3ea3a91`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v35`, 336 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V69, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v69_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 52 source-reviewed Lil B168 text records covering
Mikhail Lett's recruitment and the item-information tutorial. See the
[B168 control note](lil_sc2_b168_control_note.md).

## Verification

- Exhaustive B168 dialogue audit found zero blockers. All three exact-font
  contact sheets were visually reviewed.
- 49 focused Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,582** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,823, Maria 4,953. All 205
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v35/exact_records.json).
- Lil coverage: **3,872/6,608 translated**, 2,700 remaining and 36 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
Mikhail's recruitment, the item-information tutorial, portraits,
nameplates, macros, first and continuation letters, and transitions. Do
not promote this candidate before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B169 (36 source records).
Three B022 controls and the 36 exclusions still require sufficient source
and control evidence before translation.
