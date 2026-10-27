# Combined four-route ROM, Lil V97 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v97_candidate.nds`
- SHA-256: `4699e527c9d3e17b84d7882dce7619ea90776a8b8b9b76bdff3f3e1144bce9d3`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v63`, 364 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V97, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v97_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds all 21 source-reviewed Lil B203 medicine-book
records. See the [B203 control note](lil_sc2_b203_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. Three exact-font contact
  sheets were visually reviewed, including both prices and the charm reward.
- 51 focused Lil stack tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **20,229** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 4,470, Maria 4,953. All 208
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v63/exact_records.json).
- Lil coverage: **4,519/6,608 translated**, 2,050 remaining and 39 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
B203's caterpillar-fungus explanation, book handoff, 1,000 and 100 coin
lines, reward name expansion, portraits, and nameplates. Do not promote
this candidate before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B204. Three B022 controls
and the 39 exclusions still require sufficient source and control evidence
before translation.
