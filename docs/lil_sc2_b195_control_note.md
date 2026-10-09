# Lil SC2 B195 Veracruz cheese control note

B195 contains 20 source dialogue records, all translated in
`translations/lil_deep_route_v89.json`. Two patrons smell a barkeep's
cheese-rich house specialty, order it, and predict it will become popular.

Source-correlated presentation leads are `77` for one patron, `67` for his
friend, `5C` for the barkeep, and `FE` for the market notice. `67` is added
to the Lil V89 profile; the others are inherited. There are no name macros.
English prose avoids literal uppercase `I` and `F`, which are unsafe
renderer bytes.

All 20 records pass the fixed-byte, speaker, wrap, pair-phase, and first-glyph
audit. The exact-font contact sheet was visually reviewed; every first
character is intact. Direct saved-ROM verification confirms all 20 inserted
records. Runtime cold-boot remains necessary to check the conversation,
portraits, nameplates, first letters, and market notice.
