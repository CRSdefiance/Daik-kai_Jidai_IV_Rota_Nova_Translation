# Combined four-route ROM, Lil V50 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v50_candidate.nds`
- SHA-256: `bd4bc044969e5f0abb9bc60babd94a4c87e20628b4ed11e006f29955e4c014d4`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v16`, 317 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V50 and shared interface,
  graphics, layout, encounter, percent-safety and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v50_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation added 102 source-reviewed Lil dialogue records:
B137 Nagalpur's tavern confrontation, B138 the barkeep's aftermath and
two map-price branches, and B139 the lotus-leaf map reveal. B139 R0035
is an unchanged four-byte event payload. See the [B137 scene note](lil_sc2_b137_control_note.md)
and [B138–B139 control note](lil_sc2_b138_b139_control_note.md).

## Verification

- Exhaustive dialogue audits found zero blockers for all 102 records; every
  exact-font contact sheet was visually reviewed, with ambiguous opening
  glyphs confirmed in individual previews.
- 30 targeted Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **18,836** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,077, Maria 4,953. All 198
  effective exclusions remain unchanged. The other 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v16/exact_records.json).
- Lil coverage: **3,126/6,608 translated**, 3,453 remaining and 29 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established
scenes in all four routes, town UI, Help and shared names. In Lil's route,
test Nagalpur's tavern scene, both B138 map-price branches, the barkeep's
pride conversation, leaf handoff and the B139 water-spill map reveal, as
well as earlier scenes. Check portraits, nameplates, macro expansion,
first and continuation letters, and transitions. Do not promote this
candidate before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B140 (49 records). Three
B022 controls and the 29 exclusions still require sufficient source and
control evidence before translation.
