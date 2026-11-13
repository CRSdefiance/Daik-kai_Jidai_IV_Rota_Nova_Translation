# Combined four-route ROM, Lil V106 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v106_candidate.nds`
- SHA-256: `299c1ef66fd668c0c5c9e459c5eefe6774beb422610ff9b2839e227cb5c2b5e8`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Unified V72: 373 batches; Lil V106: 116 batches.

B255-B282 adds 154 source-reviewed natural-English guild quest records,
including captured-person scenes, all rewards, share changes and ruin hints.
All 16 exact-font sheets and three final wording refinements were reviewed.
Zero dialogue blockers; 60 Lil tests and Ruff pass. Baseline invariants and
exactly nine allowed changed paths pass.

Saved-ROM verification confirms 21,113 exact experimental route records:
Raphael 5,802, Hodram 5,004, Lil 5,354 and Maria 4,953. All 213 effective
exclusions remain unchanged. Another 49 Lil opening records are in the base.
Lil coverage: 5,403/6,608 translated, 1,161 remaining, 44 excluded.
Continue B283. Runtime confirmation remains pending before promotion.
