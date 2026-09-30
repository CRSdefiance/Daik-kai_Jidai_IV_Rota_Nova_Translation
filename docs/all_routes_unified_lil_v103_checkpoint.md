# Combined four-route ROM, Lil V103 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v103_candidate.nds`
- SHA-256: `5d9ff025155f5db20423dc7dfdc67769410f90cb177cc7bc55f191e5fec3184e`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Unified V69: 370 experimental batches; Lil V103: 113 batches.

B227-B238 add 166 source-reviewed natural-English records covering Yifa's
robe, Sanghyeon's shield and helmet clues, Herophilus, Phidias, papal trade,
Charles and Jam letters, Cesare's arrow complaint and Janus's glove clue.
B232 is empty. All 17 exact-font sheets were reviewed; five refined lines
were re-audited and visually checked. Dialogue QA has zero blockers.
All 57 focused Lil tests and Ruff pass, along with all 13 build checks,
accepted-baseline invariants and exactly nine allowed changed ROM paths.

Saved-ROM verification confirms 20,741 exact experimental route records:
Raphael 5,802, Hodram 5,004, Lil 4,982 and Maria 4,953. All 211 exclusions
remain unchanged. Another 49 Lil opening records are in the accepted base.
See [exact records](../work/qa/all_routes_unified_v69/exact_records.json).
Lil coverage: 5,031/6,608 translated, 1,535 remaining, 42 excluded.
Continue B239. Runtime must verify all letter variants, first glyphs,
portraits and nameplates before promotion.
