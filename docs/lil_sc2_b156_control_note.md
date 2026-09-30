# Lil SC2 B156 Ian Dukov recruitment control note

All 69 B156 source records are translated in
`translations/lil_deep_route_v63.json`. Ian Dukov is harassed in a tavern,
dismissed, attacked by the same drunken man outside, and rescued by Lil's
crew. Lil offers him a berth as a navigator. The dialogue uses natural English
within the fixed game text windows.

The source presentation leads are `02` Lil, `09` Kamil, `0E` Emilio, `14`
Fernando, `15` Ian, `5C` the tavernkeeper, `60` the drunken thug, `A4` a male
patron, and `A5` a female patron. The two source `FI` name macros are
preserved. Ian's given name cannot be printed literally in dialogue because
uppercase `I` is a renderer macro byte; his introduction uses “Dukov.”

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audits
found zero blockers. All seven exact-font contact sheets were visually
reviewed. Direct saved-ROM verification confirms all 69 inserted records.

Runtime cold-boot remains necessary to check the tavern dismissal, outdoor
ambush, rescue and recruitment, portraits, nameplates, macros, first and
continuation letters, and scene transitions.
