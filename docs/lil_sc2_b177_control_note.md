# Lil SC2 B177 Genoa tomato-boom control note

B177 contains 10 source dialogue records, all translated in
`translations/lil_deep_route_v77.json`. A patron orders her attendant to
sell tomato dishes, and the market notice predicts a Genoa boom.

Source presentation leads are `AE` the patron, `AF` her attendant, and
`FE` the market notice. There are no name macros in this block. English
prose avoids literal uppercase `I` and `F`, which are unsafe renderer bytes.

All 10 records pass the fixed-byte, speaker, wrap, pair-phase, and
first-glyph audit. The exact-font contact sheet was visually reviewed.
Direct saved-ROM verification confirms all 10 inserted records.

Runtime cold-boot remains necessary to check the scene's portraits,
nameplates, first letters, and the market notice.
