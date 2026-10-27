# Combined four-route ROM, Lil V92 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v92_candidate.nds`
- SHA-256: `b6855ac0e500396de4403b68a53d198f1c1d8e5544a0783668f5616a3c86312f`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v58`, 359 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V92, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v92_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds all 15 source-reviewed Lil B198 namahage-dream
records. See the [B198 control note](lil_sc2_b198_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. Both exact-font contact
  sheets were visually reviewed, including first letters on short lines.
- 46 focused Lil stack tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **20,114** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 4,355, Maria 4,953. All 207
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v58/exact_records.json).
- Lil coverage: **4,404/6,608 translated**, 2,166 remaining and 38 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
B198's repeated namahage prompts, dream transition, discovery, portraits,
nameplates, and first letters. Do not promote this candidate before user
cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B199. Three B022 controls
and the 38 exclusions still require sufficient source and control evidence
before translation.
