# Combined four-route ROM, Lil V90 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v90_candidate.nds`
- SHA-256: `dd2557ee21672476b698f5c5ef7e72bd26ff6d9d313c07e783c66a376c6abc21`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v56`, 357 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V90, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v90_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds all 35 source-reviewed Lil B196 haggling records.
See the [B196 control note](lil_sc2_b196_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. Both exact-font contact
  sheets were visually reviewed, including all Buy/Pass first letters.
- 44 focused Lil stack tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **20,075** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 4,316, Maria 4,953. All 206
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v56/exact_records.json).
- Lil coverage: **4,365/6,608 translated**, 2,206 remaining and 37 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
all B196 haggling branches, price steps, Buy/Pass choice initials, the live
`FI` charm reward, portraits, and nameplates. Do not promote this candidate
before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B197. Three B022 controls
and the 37 exclusions still require sufficient source and control evidence
before translation.
