# Lil SC2 B170 Yifa recruitment control note

B170 contains 33 source dialogue records, all translated in
`translations/lil_deep_route_v71.json`. Yifa runs into Lil, explains why
she left her Taoist master, and asks to travel and train aboard Lil's ship.

The source presentation leads are `02` Lil and `19` Yifa. The one `FI`
given-name and one `FO` fleet-name macro are preserved. English prose
avoids literal uppercase `I` and `F`, which are unsafe renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audit
found zero blockers. Both exact-font contact sheets were visually reviewed.
Direct saved-ROM verification confirms all 33 inserted records.

Runtime cold-boot remains necessary to check Yifa's encounter and
recruitment, portraits, nameplates, macro substitutions, first and
continuation letters, and transitions.
