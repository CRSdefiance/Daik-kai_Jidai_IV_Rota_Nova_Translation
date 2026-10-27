# Complete Lil translation, combined four-route ROM

Translation goal complete. Candidate remains experimental: emulator cold-boot
gameplay verification and explicit release acceptance are pending.

- Candidate: `out/all_routes_unified_lil_v123_candidate.nds`
- SHA-256: `c76a520489de353a1e12a9a8d3e74b628c7e34601dc315fdce531d24dcd67328`
- Unified V89: 390 batches; Lil V123: 133 batches.
- Lil coverage: **6,539 translated; zero remaining; 69 preserved control records**, out of 6,608 records.

B330-B335 adds 77 final scene texts: strongest-warrior virtues, ruins commission
and nonrefundable 5,000-gold advance, Ancient City Ruins Map and gate meeting,
sextant exchange, survey funding alternatives and Sofala report, item handoff,
Charles's Alchemy Book discovery, poisoned water, monk's sacrifice and ore search.
Three B22 companion events are classified as packed controls and left intact.

All eight sheets and four final wording refinements reviewed. Audit has zero
blockers. 77 Lil regression tests and Ruff pass. Saved-ROM verification confirms
22,249 exact experimental translations: Raphael 5,802, Hodram 5,004, Lil 6,490,
Maria 4,953; all 238 effective exclusions remain unchanged. The accepted base
contains another 49 Lil translations. Baseline invariants pass, with exactly
the established nine allowed files changed. No emulator gameplay verification
was performed for this checkpoint.

The old B61R0226 exclusion note's hex typo was corrected to `94 40`; its source
bytes and ROM contents are unchanged. See the final control note and inventory
in `work/qa/lil_deep_route_v123/inventory.json`.
