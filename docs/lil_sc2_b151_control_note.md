# Lil SC2 B151 Maldonado tavern control note

All 55 clean-source B151 records are translated in
`translations/lil_deep_route_v59.json`. Maldonado privately doubts his
alliance with Escante, then encounters Lil in a tavern, throws a bottle,
intimidates the barkeep, and decides her defeat could win royal permission
to expand. Both alternate early monologues, companion reactions, and
aftermath branches are included. No B151 record is excluded.

The source `2A` lead is Maldonado's presentation state, so the
`lil-story-deep-route-v59-live` profile adds it to the inherited speaker
states. The other source leads are `02` Lil, `09` Kamil, `0B` Jam, `0C`
Yukihisa, `0E` Emilio, `10` Gerhard, `11` Al, `14` Fernando, `15` Ian,
`16` Samwell, `1B` Aziza, `5C` barkeep, and `FE` the impact caption. The
source has two `FI`, one `FA`, and two `FO` macros; all are preserved exactly.
English prose avoids literal uppercase `I` and `F`, which are unsafe
renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audits
found zero blockers. All six exact-font contact sheets were visually
reviewed. R0079, R0279, and R0295 were also checked individually because
their first glyphs looked ambiguous at sheet scale; the opening letters are
present. Direct saved-ROM verification confirms all 55 inserted segments
and every prior exclusion.

Runtime cold-boot remains necessary to check Maldonado's speaker and
portrait state, both monologue and aftermath branches, the bottle effect,
macro expansion, first and continuation letters, and the tavern transition.
