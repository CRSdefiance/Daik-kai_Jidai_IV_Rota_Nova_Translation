# Combined four-route ROM, Lil V44 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v44_candidate.nds`
- SHA-256: `3cc2be4c1a5788cb43bdebd5520d33fb767ab253ccd16b68af9808c3b4325c87`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v10`, 311 experimental batches.
- The immutable base still contains all 114 accepted layers. The
  registered stack combines Raphael V93, Hodram V32, Maria V111, Lil V44,
  and the shared interface, graphics, layout, encounter, percent-safety
  and COMMON repairs. Exact identities are in the
  [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v44_candidate.manifest.json).
- Exactly nine internal paths changed: `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
  `/_pxl/personinfo.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
  `/data/SC2.DK4`, and `/data/SC3.DK4`.

This continuation added 145 Lil records in B127–B132: Fernando's gamble,
Speyer and the market-share lesson, the polder, Clifford's map key and
Crimson Pigment reveal, and the southern Mediterranean warning. One
four-byte B131 event payload is an explicit unchanged exclusion. See the
[scene and control note](lil_sc2_b127_b132_control_note.md).

## Verification

- Exhaustive dialogue audits found zero blockers for all 145 records;
  every exact-font preview sheet was visually reviewed.
- 41 targeted Lil and unified regression tests passed; Ruff passed.
- All 13 integrated-build checks, candidate/base/registry hashes and
  the accepted-baseline invariant passed.
- Direct saved-ROM verification found **18,625** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 2,866, Maria 4,953. All 196
  effective exclusions remain unchanged. The other 49 Lil opening records
  are baked into the accepted base. [Exact-record report](../work/qa/all_routes_unified_v10/exact_records.json).
- Lil coverage: **2,915/6,608 translated**, 3,666 remaining and 27 excluded.

## Runtime review and next block

Cold-boot without a save state. Check title menu, New Game, established
scenes in all four routes, town UI, Help and shared names. In Lil's route,
test Fernando's bluff and Old Maid account, both Speyer choice paths,
war/investment tutorial, polder conversation, letter/map/pigment event,
and the southern trade warning. Check the earlier Lil scenes as well.
Watch portraits, nameplates, macro expansion, first and continuation
letters, choices and transitions. Do not promote the candidate before
the user cold-boots and explicitly accepts it.

Lil's route remains incomplete. Continue at B133 (47 records, Raphael
Castor crossover). Three B022 controls and the 27 exclusions still
require adequate source and control evidence before translation.
