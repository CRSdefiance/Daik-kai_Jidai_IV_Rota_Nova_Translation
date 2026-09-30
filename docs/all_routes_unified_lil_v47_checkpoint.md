# Combined four-route ROM, Lil V47 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v47_candidate.nds`
- SHA-256: `1be6b03e0c44e05a9b7bf193281b19e8c7f543df5cbca0cd3907a1b89c9b75aa`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v13`, 314 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V47, and shared interface,
  graphics, layout, encounter, percent-safety and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v47_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation added 109 source-reviewed Lil dialogue records in B133–B136:
Raphael Castor's Nantes–Lisbon share exchange, Silveira's West Africa demand,
Espinosa's Goddess' Temptation trade, and the Africa tablet map. B136 R0020
is an unchanged four-byte event payload. See the [scene and control
note](lil_sc2_b133_b136_control_note.md).

## Verification

- Exhaustive dialogue audits found zero blockers for all 109 records; every
  exact-font contact sheet was visually reviewed, with ambiguous opening
  glyphs confirmed in individual previews.
- 28 targeted Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **18,734** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 2,975, Maria 4,953. All 197
  effective exclusions remain unchanged. The other 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v13/exact_records.json).
- Lil coverage: **3,024/6,608 translated**, 3,556 remaining and 28 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established
scenes in all four routes, town UI, Help and shared names. In Lil's route,
test both B133 and B134 choice paths, share panels, Espinosa's confrontation,
the tablet-map transition, and the earlier scenes. Check portraits,
nameplates, macro expansion, first and continuation letters, choices and
transitions. Do not promote the candidate before the user cold-boots and
explicitly accepts it.

Lil's route remains incomplete. Continue at B137 (47 records). Three B022
controls and the 28 exclusions still require sufficient source and control
evidence before translation.
