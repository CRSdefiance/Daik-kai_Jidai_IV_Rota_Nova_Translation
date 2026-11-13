# Combined four-route ROM, Lil V118 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v118_candidate.nds`
- SHA-256: `4ac1115a31dd8d4f3de1be78c641ee14c0eb71ca3351529f8e3adc3af0142b54`
- Unified V84: 385 batches; Lil V118: 128 batches.

B316 adds 94 scorpion encounter texts, all Kill/Shoo/Run branches,
sting treatment, cactus false alarm, injuries and luggage escape.
Ten sheets and two final refinements reviewed; zero blockers. 72 Lil tests,
Ruff, baseline and nine allowed changed paths pass. Saved-ROM verification:
21,958 exact records (Raphael 5,802; Hodram 5,004; Lil 6,199; Maria 4,953),
225 unchanged effective exclusions. With 49 base Lil records, coverage is
6,248/6,608; 304 remaining; 56 excluded. Continue B317.
