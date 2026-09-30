# Combined four-route ROM, Lil V102 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v102_candidate.nds`
- SHA-256: `ceaf827a2ddf3b87cb253d2e9ceaf4d40afe18f1c31fcb03de6d539faa8e6f66`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Registered profile: `all-routes-unified-v68`, 369 experimental batches;
  Lil profile `lil-deep-route-v102`, 112 batches.

B215-B226 add 155 source-reviewed natural-English records: Solomon, Vivian
and Avalon, Ares, Lucia, the Crusades and Saladin, Noritsune, Dukov's Timur
letter, Safia's Medusa shield clue, Charles Martel and Attila. B219 is empty.
See [control note](lil_sc2_b215_b226_control_note.md).

All 16 exact-font contact sheets were reviewed. Dialogue QA has zero error
or warning blockers. The opt-in wrap planner reserves room for native glyph
phase protection and avoids weak line endings; earlier profiles retain their
existing wrapping. All 57 formatter/control tests, 56 focused Lil tests and
Ruff pass. All 13 build checks, baseline invariants and nine allowed changed
paths pass.

Saved-ROM verification confirms 20,575 exact experimental route records:
Raphael 5,802, Hodram 5,004, Lil 4,816 and Maria 4,953, plus all 211 unchanged
exclusions. Another 49 Lil opening records are in the accepted base. See
[exact records](../work/qa/all_routes_unified_v68/exact_records.json).

Lil coverage: 4,865/6,608 translated, 1,701 remaining, 42 excluded.
Continue at B227. Runtime checks must cover first glyphs, portraits,
nameplates, macros, bare choices and all letter variants before promotion.
