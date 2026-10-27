# Lil SC2 B191 Calicut dye control note

B191 contains 13 source dialogue records, all translated in
`translations/lil_deep_route_v87.json`. A father and son debate whether
to buy a popular dye before other shops exhaust the supply.

Source-correlated presentation leads are `56` for the father, `9A` for the
son, and `FE` for the market notice. The first two are added to the Lil V87
profile; `FE` is inherited. There are no name macros. English prose avoids
literal uppercase `I` and `F`, which are unsafe renderer bytes.

All 13 records pass the fixed-byte, speaker, wrap, pair-phase, and first-glyph
audit. The exact-font contact sheet was visually reviewed; every first
character is intact. Direct saved-ROM verification confirms all 13 inserted
records. Runtime cold-boot remains necessary to check the conversation,
portraits, nameplates, first letters, and market notice.
