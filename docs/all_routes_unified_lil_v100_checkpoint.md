# Combined four-route ROM, Lil V100 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v100_candidate.nds`
- SHA-256: `43809c90b4a59ff33382f61d3b6d66455c12d70fe26c90362062118e1a79b96c`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v66`, 367 experimental batches;
  Lil profile `lil-deep-route-v100`, 110 batches.

B206 adds all 28 ceramic-earrings dialogue and choice records. Its one
packed item payload is excluded unchanged. See the
[control note](lil_sc2_b206_control_note.md).

The dialogue audit has zero error or warning blockers. All three exact-font
contact sheets were visually reviewed; every choice keeps its first letter.
All 54 focused Lil tests and Ruff pass. The integrated build checks and
accepted-baseline invariant pass; exactly the nine allowed internal paths
changed.

Independent saved-ROM verification confirms 20,294 exact experimental route
records: Raphael 5,802, Hodram 5,004, Lil 4,535, Maria 4,953. All 210 effective
exclusions are unchanged. Another 49 Lil opening records are in the accepted
base. See the [exact-record report](../work/qa/all_routes_unified_v66/exact_records.json).

Lil coverage is 4,584/6,608 translated, 1,983 remaining and 41 excluded.
Continue at B207. Runtime review must check the ceramic-earrings purchase,
both initial responses, both purchase choices, rejection branches, portraits,
nameplates and first glyphs before promotion.
