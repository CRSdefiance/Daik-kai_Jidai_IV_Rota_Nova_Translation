# Lil SC2 B155 Angelo recruitment control note

B155 contains 49 source records: 48 dialogue records translated in
`translations/lil_deep_route_v62.json`, and one opaque scene event. Angelo
Puccini offends Kamil and Lil, apologizes, and joins Lil's crew. He then
explains why trade beyond the crowded Mediterranean, especially in Africa,
could be more profitable. Lil's grandfather confirms his advice.

The source presentation leads are `02` Lil, `06` her grandfather, `09`
Kamil, `0F` Angelo, and `14` Fernando. Five source `FI` name macros and one
`FA` name macro are preserved. `DK4_MES_B155_R0059` is an opaque five-byte
recruitment event payload with exact hex `20 31 46 EA 80`; it is excluded
unchanged. English prose avoids literal uppercase `I` and `F`, which are
unsafe renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audits
found zero blockers. All five exact-font contact sheets were visually
reviewed. Direct saved-ROM verification confirms all 48 inserted records
and the unchanged event payload.

Runtime cold-boot remains necessary to check Angelo's recruitment, portraits,
nameplates, name macros, first and continuation letters, and the transition
into his African trade advice.
