# Combined four-route ROM, Lil V104 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v104_candidate.nds`
- SHA-256: `acb7a4e0d2c687d870229353a9cbd961808017016d69747e05970ab0f2bb7a83`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Unified V70: 371 experimental batches; Lil V104: 114 batches.

B239-B249 adds 135 source-reviewed natural-English records: the stolen
rose, Havana fraud, wooden church, complete figurehead challenge, ruin hints
and Lebaque survey request/reward. One two-byte figurehead event remains unchanged.
All 14 exact-font sheets were reviewed, and three editorial refinements
were re-audited and visually checked. Dialogue QA has zero blockers.
All 58 focused Lil tests and Ruff pass; all 13 build checks, accepted-baseline
invariants and exactly nine allowed changed ROM paths pass.

Saved-ROM verification confirms 20,876 exact experimental route records:
Raphael 5,802, Hodram 5,004, Lil 5,117 and Maria 4,953. All 212 exclusions
remain unchanged. Another 49 Lil opening records are in the accepted base.
See [exact records](../work/qa/all_routes_unified_v70/exact_records.json).
Lil coverage: 5,166/6,608 translated, 1,399 remaining, 43 excluded.
Continue B250. Runtime review must cover both rose choices, all figurehead
outcomes, first glyphs, FI names, portraits and nameplates before promotion.
