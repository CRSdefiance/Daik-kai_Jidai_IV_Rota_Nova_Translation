# Combined four-route ROM, Lil V40 checkpoint

Status: experimental; cold-boot testing and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v40_candidate.nds`
- SHA-256: `66f38a04ccfdbdd1b1cef1fe47f798c40e61e71dcde5f600296ab326efcb1b47`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v6`
- All 114 accepted layers remain baked into the immutable base. The profile
  applies 307 experimental batches: Raphael V93, Hodram V32, Maria V111,
  Lil V40, and the registered shared interface, graphics, layout, encounter,
  percent-safety and COMMON repairs. Complete identities:
  [registry](../translations/release_stack.json) and
  [manifest](../out/all_routes_unified_lil_v40_candidate.manifest.json).
- Changed internal paths: `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`,
  `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`,
  `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`.

This continuation added 81 Lil records across B123–B126. B123 invites
Christina aboard; B124 covers Julian's tavern advice and the Snowfall Robe;
B125 covers Lil's doubt, both responses, the Guiding Staff clue and spirit
reward; B126 teaches Bruges trading, cargo holds and market share. Every line
was localized from clean Japanese into natural American English and reviewed
in scene order. See the [B123–B124 note](lil_sc2_b123_b124_control_note.md)
and [B125–B126 note](lil_sc2_b125_b126_control_note.md).

## Verification

- Exhaustive audits of all 81 new records: zero blocking issues; all previews
  visually reviewed, including both choice paths and the reward.
- 39 targeted route, inheritance and scene tests passed; Ruff passed.
- All 13 integrated-build checks, registry/base/candidate hashes and baseline
  invariant passed with exactly the nine declared changed paths.
- Direct saved-ROM verification found **18,480** exact experimental route
  records: Raphael 5,802, Hodram 5,004, Lil 2,721, Maria 4,953. All 195
  effective exclusions remain unchanged. The other 49 Lil opening records
  are baked into the accepted base. [Exact-record report](../work/qa/all_routes_unified_v6/exact_records.json).
- Lil coverage: **2,770/6,608 translated**, 3,812 remaining and 26 excluded.

## Cold-boot review and continuation

Restart without a save state. Check title menu, New Game, an established scene
in each route, town UI, shared names, supplies/cargo, Help and encounter
directions. For Lil, test the Christina invitation, Julian tavern advice,
both B125 response paths, Guiding Staff lead and spirit reward, and both
Bruges trading answers. Check the older sailing, ambush, reconciliation and
Clifford scenes. Verify portraits, nameplates, macro expansion, first and
continuation letters, items, choices and transitions. Do not promote this
candidate until the user cold-boots and explicitly accepts it.

Lil's route remains incomplete. Continue at B127 (38 records). Three B022
records and the 26 exclusions need adequate source and control evidence.
