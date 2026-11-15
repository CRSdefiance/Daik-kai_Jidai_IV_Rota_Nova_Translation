# Combined four-route ROM, Lil V58 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v58_candidate.nds`
- SHA-256: `16ec7b5a8db384752421e85850f637281e469f1667a72da87ea7b79d5221325c`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v24`, 325 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V58 and shared interface,
  graphics, layout, encounter, percent-safety and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v58_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 22 source-reviewed Lil dialogue records in B150:
Clifford's New World alliance proposal and two-stage strategy against
Maldonado and Escante. See the [B150 control note](lil_sc2_b150_control_note.md).

## Verification

- Exhaustive dialogue audits found zero blockers. All three exact-font
  contact sheets were visually reviewed.
- 38 targeted Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,107** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,348, Maria 4,953. All 200
  effective exclusions remain unchanged. The other 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v24/exact_records.json).
- Lil coverage: **3,397/6,608 translated**, 3,180 remaining and 31 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established
scenes in all four routes, town UI, Help and shared names. In Lil's route,
check Clifford's greeting, the alliance proposal, portraits, nameplates,
the `FO` faction macro, first and continuation letters, and the transition
to Maldonado's tavern encounter. Do not promote this candidate before user
cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B151 (55 records). Three B022
controls and the 31 exclusions still require sufficient source and control
evidence before translation.
