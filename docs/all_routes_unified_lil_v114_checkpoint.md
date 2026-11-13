# Combined four-route ROM, Lil V114 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v114_candidate.nds`
- SHA-256: `f381cd025df20693f232562141f92b01187ff623a7518a30a046232ec8c17a85`
- Unified V80: 381 batches; Lil V114: 124 batches.

B306 adds 39 natural-English river encounter records; two packed events
unchanged. One bare Japanese 97AC companion variant is handled in V115,
separately from real state 97. All four sheets and one refinement reviewed;
zero blockers. 68 Lil tests, Ruff, baseline and nine allowed changed paths
pass. Saved-ROM verification: 21,698 exact experimental records: Raphael
5,802, Hodram 5,004, Lil 5,939, Maria 4,953; 221 effective exclusions unchanged.
Another 49 Lil records are in the base. Coverage 5,988/6,608; 568 remaining;
52 excluded. Continue B306R0081 and B307.
