# Combined four-route ROM, Lil V98 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v98_candidate.nds`
- SHA-256: `cd9a95e3a113c39787dfec6a542fc786d5e402177d0d3366ccfb3ee2bbbb293a`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v64`, 365 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V98, and shared interface,
  graphics, layout, encounter, percent-safety, and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v98_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation adds all 20 source-reviewed Lil B204 shachihoko and
letter records. See the [B204 control note](lil_sc2_b204_control_note.md).

## Verification

- Exhaustive dialogue audit found zero blockers. Both exact-font contact
  sheets were visually reviewed, including the letter and signature.
- 52 focused Lil stack tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **20,249** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 4,490, Maria 4,953. All 208
  effective exclusions remain unchanged. Another 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v64/exact_records.json).
- Lil coverage: **4,539/6,608 translated**, 2,030 remaining and 39 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established scenes
in all four routes, town UI, Help, and shared names. In Lil's route, check
B204's castle and ship transitions, the shachihoko, the retainer and lord,
Jam's letter and signature, portraits, nameplates, and first letters. Do
not promote this candidate before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B205. Three B022 controls
and the 39 exclusions still require sufficient source and control evidence
before translation.
