# Combined four-route ROM, Lil V101 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v101_candidate.nds`
- SHA-256: `52f8926665e75694d5ad8d46c79c598f38fc4b05314eb21be87988de7b9eda97`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v67`, 368 experimental batches;
  Lil profile `lil-deep-route-v101`, 111 batches.

B207-B214 add 126 source-reviewed text records covering Emilio's axe request,
Cristina's lost pirate-sword and swan clues, Yukihisa's Muramasa letter, Al's
blood-red sword rumor, all Three Kingdoms choices, Kublai Khan's prophecy,
and Janus's Judas-sword letter. One packed sword event remains unchanged.
See the [control note](lil_sc2_b207_b214_control_note.md).

The exhaustive dialogue audit has zero error or warning blockers. All 13
exact-font contact sheets were reviewed, then four editorial improvements
were re-audited and visually checked. All 55 focused Lil tests and Ruff pass.
All 13 build checks and the accepted-baseline invariant pass. Exactly the
nine allowed internal ROM paths changed.

Independent saved-ROM verification confirms 20,420 exact experimental route
records: Raphael 5,802, Hodram 5,004, Lil 4,661, Maria 4,953. All 211 effective
exclusions remain unchanged. Another 49 Lil opening records are in the accepted
base. See the [exact-record report](../work/qa/all_routes_unified_v67/exact_records.json).

Lil coverage is 4,710/6,608 translated, 1,856 remaining and 42 excluded.
Continue at B215. Runtime review must include all optional treasure scenes,
each companion's letter delivery and reaction, all five Three Kingdoms choices,
name macros, portraits, nameplates and first glyphs before promotion.
