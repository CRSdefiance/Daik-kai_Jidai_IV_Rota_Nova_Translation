# Combined four-route ROM, Lil V57 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v57_candidate.nds`
- SHA-256: `e31e356eed71036439b2d55eff70f5d0c75c51a93aed005d0b8a8712f3b4cf35`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v23`, 324 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V57 and shared interface,
  graphics, layout, encounter, percent-safety and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v57_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 45 source-reviewed Lil dialogue records in B148-B149:
Kamil's identity clue in Batavia and the Tang Bamboo Craft Proof-map puzzle,
including both companion variants. See the [B148-B149 control
note](lil_sc2_b148_b149_control_note.md).

## Verification

- Exhaustive dialogue audits found zero blockers. All five exact-font
  contact sheets were visually reviewed, with a revised line checked in an
  individual preview.
- 37 targeted Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,085** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,326, Maria 4,953. All 200
  effective exclusions remain unchanged. The other 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v23/exact_records.json).
- Lil coverage: **3,375/6,608 translated**, 3,202 remaining and 31 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established
scenes in all four routes, town UI, Help and shared names. In Lil's route,
check the Batavia witness and identity revelation, both bamboo-puzzle
branches, nameplate and portrait changes, macro expansion, first and
continuation letters, and the East Asia Proof-map transition. Do not
promote this candidate before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B150 (22 records). Three B022
controls and the 31 exclusions still require sufficient source and control
evidence before translation.
