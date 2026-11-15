# Combined four-route ROM, Lil V56 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.
Translation work is paused at this completed set until the user resumes it.

- Candidate: `out/all_routes_unified_lil_v56_candidate.nds`
- SHA-256: `26a0db5ae7e1f42194d2e0893dcfa9dd78eb7854c49dada058ff992020736b2a`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v22`, 323 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V56 and shared interface,
  graphics, layout, encounter, percent-safety and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v56_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This set adds 68 source-reviewed Lil dialogue records in B147: Maria's
identity reveal, warning about Kuhn, possible framing of the Li family, and
the lead to Batavia. Both companion departure variants are covered. B147
R0129 is an unchanged four-byte event payload. See the
[B147 control note](lil_sc2_b147_control_note.md).

## Verification

- Exhaustive dialogue audits found zero unwaived blockers for the 68 records.
  All nine exact-font contact sheets were visually reviewed; individual
  previews confirmed ambiguous opening glyphs and the R0021 layout exception.
- 36 targeted Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes, and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **19,040** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,281, Maria 4,953. All 200
  effective exclusions remain unchanged. The other 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v22/exact_records.json).
- Lil coverage: **3,330/6,608 translated**, 3,247 remaining and 31 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established
scenes in all four routes, town UI, Help and shared names. In Lil's route,
check the Li elder, Maria's name reveal and accusation sequence, both
departure variants, name macros, portraits, nameplates, first and
continuation letters, and the Batavia lead. Do not promote this candidate
before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Resume at B148 (24 records) only when the
user requests it. Three B022 controls and the 31 exclusions still require
sufficient source and control evidence before translation.
