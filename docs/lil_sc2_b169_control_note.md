# Lil SC2 B169 Proof of Conqueror control note

B169 contains 36 source dialogue records, all translated in
`translations/lil_deep_route_v70.json`. Mikhail explains the seven Proofs
of Conqueror, the maps left by the Seven Sages, and the route to clues
through regional power, city ruins, and tavern informants.

The source presentation leads are `02` Lil, `06` Lil's grandfather, `09`
Kamil, `14` Fernando, `15` Ian, and `4C` Mikhail. All five source `FI`
given-name and two `FO` fleet-name macros are preserved. English prose
avoids literal uppercase `I` and `F`, which are unsafe renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audit
found zero blockers. Both exact-font contact sheets were visually reviewed.
Direct saved-ROM verification confirms all 36 inserted records.

Runtime cold-boot remains necessary to check Mikhail's explanation,
speaker portraits, nameplates, macro substitutions, first and continuation
letters, and the transition from recruitment into the Proof tutorial.
