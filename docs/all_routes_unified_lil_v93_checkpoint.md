# Combined four-route ROM, Lil V93 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v93_candidate.nds`
- SHA-256: `3cf1abde5319d6638df4385d5fb4ba1bb2cf605f03d0b78fc42fe773160c4568`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v59`, 360 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V93, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v93_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds 31 source-reviewed Lil B199 text records and excludes
one proven nontext packed event payload unchanged. See the [B199 control
note](lil_sc2_b199_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. Four exact-font contact
  sheets were visually reviewed, including the live name-macro placeholder.
- 47 focused Lil stack tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **20,145** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 4,386, Maria 4,953. All 208
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v59/exact_records.json).
- Lil coverage: **4,435/6,608 translated**, 2,134 remaining and 39 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
B199's portrait conversation, Samwell chase, crash effects, book handoff,
the `FI` name expansion, portraits, nameplates, and first letters. Do not
promote this candidate before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B200. Three B022 controls
and the 39 exclusions still require sufficient source and control evidence
before translation.
