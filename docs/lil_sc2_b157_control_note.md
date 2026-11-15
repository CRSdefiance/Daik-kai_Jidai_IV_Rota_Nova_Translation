# Lil SC2 B157 Carlo Sinato recruitment control note

All 70 B157 source records are translated in
`translations/lil_deep_route_v64.json`. Carlo Sinato notices merchant Adil's
illness, gives Lil's delayed crew first access to the market, and recounts
losing his wife and daughter to an epidemic after he put work ahead of their
care. Lil offers him a place with her crew as a new family.

The source presentation leads are `02` Lil, `09` Kamil, `0E` Emilio, `13`
Carlo, `14` Fernando, `69` Adil, `8E` Adil's wife, and `FE` Carlo's narrated
memories. Both source `FI` name macros are preserved. English prose avoids
literal uppercase `I` and `F`, which are unsafe renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audits
found zero blockers. All seven exact-font contact sheets were visually
reviewed, with the two final wording edits checked in individual previews.
Direct saved-ROM verification confirms all 70 inserted records.

Runtime cold-boot remains necessary to check Adil's illness, the return to
the trading post, Carlo's family account and recruitment, portraits,
nameplates, macros, first and continuation letters, and transitions.
