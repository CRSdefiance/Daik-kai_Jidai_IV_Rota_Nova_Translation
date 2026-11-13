# Combined four-route ROM, Lil V38 checkpoint

Status: experimental; awaiting cold-boot testing and explicit acceptance.

- Candidate: `out/all_routes_unified_lil_v38_candidate.nds`
- SHA-256: `8fba208bdd8844b5d9baf2dc8e9dcb54607835b0a41cf3cc46d47010679f0285`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v4`
- All 114 accepted layers remain baked into the immutable base. The profile
  applies 305 experimental batches: the full unified V3 stack plus Lil V38.
  It combines Raphael V93, Hodram V32, Maria V111, Lil V38, and registered
  shared interface, graphics, layout, encounter, percent-safety and COMMON
  repairs. Exact layer identities: [registry](../translations/release_stack.json)
  and [manifest](../out/all_routes_unified_lil_v38_candidate.manifest.json).
- Changed internal paths: `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`,
  `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`,
  `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`.

V38 adds all 22 B123–B124 records. Christina's grandfather invites Lil to
bring Christina aboard in London; Julian discusses tavern leads and thoughtful
gifts, including Sakura's Snowfall Robe. The dialogue was localized into
natural American English from clean Japanese, reviewed in scene order and
checked in every preview. See [control note](lil_sc2_b123_b124_control_note.md).

## Verification

- Exhaustive B123–B124 dialogue audit: zero blockers, all 22 previews reviewed.
- 35 targeted route, inheritance and scene tests passed; Ruff passed.
- All 13 integrated-build checks, registry/base/candidate hashes and the
  baseline invariant passed. Only the nine declared paths changed.
- Direct saved-ROM verification found 18,421 exact experimental route records:
  Raphael 5,802, Hodram 5,004, Lil 2,662, Maria 4,953. All 195 effective
  exclusions remain unchanged. The other 49 Lil opening records are baked
  into the accepted base. [Exact-record report](../work/qa/all_routes_unified_v4/exact_records.json).
- Lil coverage: 2,711/6,608 translated, 3,871 remaining, 26 excluded.

## Cold-boot review

Restart without a save state. Check title menu, New Game and an established
scene in each route, town UI, shared names, supplies/cargo, Help and encounter
directions. In Lil, review Christina's grandfather and London invitation,
Julian's tavern advice and Snowfall Robe clue, then the previously changed
sailing, ambush, reconciliation and Clifford scenes. Verify portraits,
nameplates, macro expansions, opening and continuation letters, items and
transitions. The candidate remains experimental until these are tested and
explicitly accepted.

Lil's route is still incomplete. Next untranslated block: B125 (44 records).
Three B022 records and 26 explicit exclusions need sufficient control evidence.
