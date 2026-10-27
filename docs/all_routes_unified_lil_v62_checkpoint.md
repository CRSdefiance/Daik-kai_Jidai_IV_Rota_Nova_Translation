# Combined four-route ROM, Lil V62 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v62_candidate.nds`
- SHA-256: `ebb280764fe9f7c4ea252caf27c4e3de474b20ce756745994ad31e49f81be563`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v28`, 329 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V62 and shared interface,
  graphics, layout, encounter, percent-safety and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v62_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 48 source-reviewed Lil B155 text records covering
Angelo Puccini's recruitment and African trade advice. One five-byte scene
event remains unchanged. See the [B155 control
note](lil_sc2_b155_control_note.md).

## Verification

- Exhaustive B155 dialogue audit found zero blockers. All five exact-font
  contact sheets were visually reviewed.
- 42 focused Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,265** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,506, Maria 4,953. All 203
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v28/exact_records.json).
- Lil coverage: **3,555/6,608 translated**, 3,019 remaining and 34 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help and shared names. In Lil's route, check
Angelo's confrontation, apology, recruitment, and African trade lesson;
portraits, nameplates, macros, first and continuation letters, and scene
transitions. Do not promote this candidate before user cold-boot and explicit
acceptance.

Lil's route remains incomplete. Continue at B156 (69 records). Three B022
controls and the 34 exclusions still require sufficient source and control
evidence before translation.
