# Lil SC2 B154 Al recruitment control note

B154 contains 41 source records: 40 dialogue records translated in
`translations/lil_deep_route_v61.json`, and one opaque scene event. Al argues
with his employer over being treated as an errand boy, is fired, and meets Lil,
who recruits him on the spot. Kamil, Emilio, and Fernando react. The dialogue
uses natural English within the fixed game text windows.

The source presentation leads are `02` Lil, `09` Kamil, `0E` Emilio, `11` Al,
`14` Fernando, `73` the employer's attendant, and `94` the employer. The last
two states agree with the previously identified Al recruitment scene in the
Raphael route. Source name macros `FI` (twice) and `FA` (once) are preserved.
Al's canonical surname, Fasi, cannot be printed literally in dialogue because
uppercase `F` is a renderer macro byte; his introduction uses “Al.”

`DK4_MES_B154_R0003` is an opaque ten-byte scene event payload with exact hex
`95 46 7D 80 29 63 05 05 2C 63`. It is excluded unchanged. English prose
avoids literal uppercase `I` and `F`. The fixed-byte, speaker, macro, wrap,
pair-phase, and first-glyph audits found zero blockers. All four exact-font
contact sheets were visually reviewed, and ambiguous initial `W` glyphs were
checked in individual previews. The glyph is narrow but present. Direct
saved-ROM verification confirms all 40 inserted records and the unchanged
event payload.

Runtime cold-boot remains necessary to check Al's departure and recruitment,
portraits, nameplates, macros, first and continuation letters, and scene
transitions.
