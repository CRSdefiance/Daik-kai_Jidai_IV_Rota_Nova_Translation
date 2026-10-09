# Lil SC2 B158 Christina dance control note

All 19 B158 source records are translated in
`translations/lil_deep_route_v65.json`. Lil's crew enjoys a tavern song,
Christina dances to it, and the patrons and crew applaud her performance.

The source presentation leads are `02` Lil, `07` Christina, `09` Kamil,
`0E` Emilio, and `FE` audience voices and applause. The source `FI` name
macro is preserved. English prose avoids literal uppercase `I` and `F`,
which are unsafe renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audits
found zero blockers. Both exact-font contact sheets were visually reviewed.
Direct saved-ROM verification confirms all 19 inserted records.

Runtime cold-boot remains necessary to check the song, dance scene, audience
reaction, portraits, nameplates, macro, first and continuation letters, and
transition.
