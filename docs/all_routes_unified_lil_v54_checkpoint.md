# Combined four-route ROM, Lil V54 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v54_candidate.nds`
- SHA-256: `d74e21082ad700d024f65aec14bb82db4a7c4b2053d46594313b6943c4b4d830`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v20`, 321 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V54 and shared interface,
  graphics, layout, encounter, percent-safety and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v54_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation added 101 source-reviewed Lil dialogue records in B140–B145:
the Lelystad polder pledge and funding branches, shipyard armor research and
completion, and the Patterned Cloth/Brass Lamp reveal of the Mediterranean
Proof map. B145 R0021 is one unchanged four-byte event payload. See the
[B140–B145 control note](lil_sc2_b140_b145_control_note.md).

## Verification

- Exhaustive dialogue audits found zero blockers for all 101 records; every
  exact-font contact sheet was visually reviewed, with ambiguous opening
  glyphs confirmed in individual previews.
- 34 targeted Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **18,937** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,178, Maria 4,953. All 199
  effective exclusions remain unchanged. The other 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v20/exact_records.json).
- Lil coverage: **3,227/6,608 translated**, 3,351 remaining and 30 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established
scenes in all four routes, town UI, Help and shared names. In Lil's route,
test both B141–B142 funding paths, the 300,000-gold shipyard investment,
armor-upgrade notice, and B145 lamp/cloth map reveal. Check portraits,
nameplates, macro expansion, first and continuation letters, and transitions.
Do not promote this candidate before user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B146 (35 records). Three B022
controls and the 30 exclusions still require sufficient source and control
evidence before translation.
