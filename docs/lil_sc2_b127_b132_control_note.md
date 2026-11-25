# Lil SC2 B127–B132 localization and control note

All 145 translated records were source-reviewed in scene order, audited with
`natural-dialogue-v2`, and visually checked in exact-font preview sheets. No
authored prose breaks, unsafe literal uppercase `I`/`F` bytes, or audit
blockers remain. The guarded pair-phase formatter protects first and
continuation glyphs.

- B127 (38): Fernando's card bluff, his lesson to Kamil about luck and
  insight, and the Old Maid bet that brought him aboard. `14` is Fernando,
  `09` Kamil, `5F` the losing opponent, and `5C` the barkeep. The `FI`
  name macro occurs in the two recruitment questions. The `5F` and `5C`
  source leads are presentation selectors, not visible punctuation.
- B128 (53): Martin Speyer's quarrel with Lil, both Lil response choices,
  and the town-share tutorial. `1D` is Speyer; the existing `97` selector
  precedes a crew voice saying “Admiral”. `82` and `83` at R0214/R0216
  are ordinary choice text, so English starts directly with `S`/`D`.
  The tutorial keeps the order: declare war or attack a ship, invest in
  rival-held towns to shift share, and fight near a town to break a rival's
  100% share. Exact `FI` and `FO` runtime macros remain intact.
- B129 (26): Amsterdam's Crimson Pigment lead and the future Lelystad
  founder's polder plan. `AB` is the founder and `10` Gerhard. The dialogue
  retains coastal dikes, pumping seawater, a one-million-gold estimate,
  insufficient government aid, and Lil's hope for her hometown.
- B130–B132 (28 translated): Clifford's letter and map key, the Old
  Parchment and Crimson Pigment revealing the North Sea Ruler's Proof map,
  and a local man's warning about southern Mediterranean trade. `5C`
  remains the local man's source presentation state in these blocks.

B131 R0080 is a four-byte `23 48 9B A8` event payload between the map
reveal and Lil's reaction. It has no parseable Japanese dialogue or
speaker. The batch explicitly excludes it and saved-ROM verification
confirms it stays byte-identical. Cold-boot the scenes, including the
R0214/R0216 response paths, portraits, nameplates, FI/FO expansions,
first and continuation glyphs, the pigment-map transition, and the
southern warning before accepting a candidate.
