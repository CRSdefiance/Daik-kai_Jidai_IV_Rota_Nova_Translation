# Lil SC2 B159 Samwell recruitment control note

B159 contains 42 source records: 41 dialogue records translated in
`translations/lil_deep_route_v66.json`, and one opaque scene event. Lil's crew
encounters elephants and Samwell's market stall. Samwell asks to join them,
provokes Lil, then wins the crew over by proving his skill as a cook.

The source presentation leads are `02` Lil, `09` Kamil, `0E` Emilio, `14`
Fernando, and `16` Samwell. All four source `FI` name macros are preserved.
`DK4_MES_B159_R0045` is an opaque five-byte market scene event payload with
exact hex `21 51 46 EE 80`; it is excluded unchanged. English prose avoids
literal uppercase `I` and `F`, which are unsafe renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audits
found zero blockers. All five exact-font contact sheets were visually
reviewed. Direct saved-ROM verification confirms all 41 inserted records
and the unchanged event payload.

Runtime cold-boot remains necessary to check the elephant encounter,
Samwell's entrance, the cooking test and recruitment, portraits, nameplates,
macros, first and continuation letters, and transitions.
