# Combined four-route ROM, Lil V120 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v120_candidate.nds`
- SHA-256: `cb46d8772cc4e7155af47fbbdf850728789243fb8ee6c67ab6d4ce92ffc241e5`
- Unified V86: 387 batches; Lil V120: 130 batches.

B323 adds 66 fog encounter texts: map requirement, advance/wait, dead-end
choices, alternate paths, fatigue and one-day wait. Four packed events stay
unchanged with exact cross-route evidence. Seven sheets reviewed, including
direct inspection of R0204's intact first letters; zero blockers. 74 Lil tests,
Ruff, baseline and nine allowed changed paths pass. Saved-ROM verification:
22,059 exact records (Raphael 5,802; Hodram 5,004; Lil 6,300; Maria 4,953),
229 unchanged effective exclusions. With 49 base Lil records, coverage is
6,349/6,608; 199 remaining; 60 excluded. Continue B324.
