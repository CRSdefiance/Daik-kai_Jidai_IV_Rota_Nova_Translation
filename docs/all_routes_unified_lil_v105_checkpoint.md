# Combined four-route ROM, Lil V105 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v105_candidate.nds`
- SHA-256: `7ee5d967d30bd2a9a17ddc726ceb84bf27f6a74511590d0102679f245d24b683`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Unified V71: 372 experimental batches; Lil V105: 115 batches.

B250-B254 adds 83 source-reviewed natural-English records: benevolent
figurehead, Luck/Charm branches, melting-ice puzzle, all collapse variants,
demon figurehead answers and tavern ruin hints. One packed curse control
remains unchanged. All nine exact-font sheets were reviewed and three
editorial refinements were re-audited and visually checked. Zero dialogue
blockers. All 59 Lil tests and Ruff pass; all 13 build checks, baseline
invariants and exactly nine allowed changed paths pass.

Saved-ROM verification confirms 20,959 exact experimental route records:
Raphael 5,802, Hodram 5,004, Lil 5,200 and Maria 4,953. All 213 exclusions
remain unchanged. Another 49 Lil opening records are in the accepted base.
See [exact records](../work/qa/all_routes_unified_v71/exact_records.json).
Lil coverage: 5,249/6,608 translated, 1,315 remaining, 44 excluded.
Continue B255. Runtime must exercise every puzzle answer, collapse variant,
figurehead choice, curse branch, macros and first glyphs before promotion.
