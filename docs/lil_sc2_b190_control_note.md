# Lil SC2 B190 Havana medicine control note

B190 contains 17 source dialogue records, all translated in
`translations/lil_deep_route_v86.json`. Two townsmen discuss a
store-bought remedy said to have cured a mysterious illness and to work
against many others.

Source-correlated presentation leads are `9F` and `77` for the speakers and
`FE` for the market notice. The first two are added to the Lil V86 profile;
`FE` is inherited. There are no name macros. English prose avoids literal
uppercase `I` and `F`, which are unsafe renderer bytes.

All 17 records pass the fixed-byte, speaker, wrap, pair-phase, and first-glyph
audit. The exact-font contact sheet was visually reviewed; every first
character is intact. Direct saved-ROM verification confirms all 17 inserted
records. Runtime cold-boot remains necessary to check the conversation,
portraits, nameplates, first letters, and market notice.
