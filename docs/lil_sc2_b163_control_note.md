# Lil SC2 B163 Jam recruitment control note

B163 contains 44 source records: 43 dialogue records translated in
`translations/lil_deep_route_v68.json`, and one opaque scene event. The
ship returns with Jam Jack Ludwyan aboard. Lil confronts him, Kamil admires
his solo sailing, and Jam joins the crew after a teasing refusal.

The source presentation leads are `02` Lil, `09` Kamil, `0B` Jam, `0F`
Angelo, `14` Fernando, and `74` dockworker. The one source `FI` name macro
is preserved. `DK4_MES_B163_R0034` is an opaque seven-byte ship-return
event with exact hex `20 95 46 E2 80 2C 63`; it is excluded unchanged.
English prose avoids literal uppercase `I` and `F`, which are unsafe
renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audit
found zero blockers. All three exact-font contact sheets were visually
reviewed. Direct saved-ROM verification confirms all 43 inserted records
and the unchanged event payload.

Runtime cold-boot remains necessary to check the ship's return, Jam's
entrance and recruitment, portraits, nameplates, macros, first and
continuation letters, and transitions.
