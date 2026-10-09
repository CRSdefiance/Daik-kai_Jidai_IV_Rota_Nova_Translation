# Combined four-route ROM, Lil V55 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v55_candidate.nds`
- SHA-256: `cdec3ad9981f3586736ce5f8ae9d74e179bb95d99c4627f4863e46bd00699332`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v21`, 322 experimental batches.
- The immutable base still contains 114 accepted layers. The stack combines
  Raphael V93, Hodram V32, Maria V111, Lil V55 and shared interface,
  graphics, layout, encounter, percent-safety and COMMON repairs. Exact
  identities are in the [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v55_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation added 136 source-reviewed Lil dialogue records in B140–B146:
the Lelystad polder funding, shipyard armor upgrade, Mediterranean Proof map
reveal, and Kamil's encounter with Hodram. B145 R0021 is an unchanged
four-byte event payload. See the [B140–B145 note](lil_sc2_b140_b145_control_note.md)
and [B146 note](lil_sc2_b146_control_note.md).

## Verification

- Exhaustive dialogue audits found zero blockers for all 136 records; every
  exact-font contact sheet was visually reviewed, with ambiguous opening
  glyphs confirmed in individual previews.
- 35 targeted Lil and integrated-build tests and Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes and the
  accepted-baseline invariant passed.
- Direct saved-ROM verification found **18,972** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 3,213, Maria 4,953. All 199
  effective exclusions remain unchanged. The other 49 Lil opening records
  are baked into the accepted base. [Exact-record
  report](../work/qa/all_routes_unified_v21/exact_records.json).
- Lil coverage: **3,262/6,608 translated**, 3,316 remaining and 30 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established
scenes in all four routes, town UI, Help and shared names. In Lil's route,
test both polder funding paths, the shipyard armor upgrade and system notice,
the lamp/cloth map reveal, and B146 Kamil's separation, Hodram encounter
and ship invitation. Check portraits, nameplates, macro expansion, first and
continuation letters, and transitions. Do not promote this candidate before
user cold-boot and explicit acceptance.

Lil's route remains incomplete. Continue at B147 (69 records). Three B022
controls and the 30 exclusions still require sufficient source and control
evidence before translation.
