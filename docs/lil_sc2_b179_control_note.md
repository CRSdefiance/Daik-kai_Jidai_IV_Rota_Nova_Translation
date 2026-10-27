# Lil SC2 B179 San Jorge wine-boom control note

B179 contains eight identified source text records, all translated in
`translations/lil_deep_route_v79.json`. A drinker tries wine at a San
Jorge tavern, and the market notice predicts local demand.

Source presentation leads are `60` the drinker, `5C` the barkeep, and
`FE` the market notice. There are no name macros in this block. English
prose avoids literal uppercase `I` and `F`, which are unsafe renderer bytes.

All eight records pass the fixed-byte, speaker, wrap, pair-phase, and
first-glyph audit. The exact-font contact sheet was visually reviewed.
Direct saved-ROM verification confirms all eight inserted records.

Runtime cold-boot remains necessary to check the drinker's first line,
barkeep response, portraits, nameplates, and the market notice.
