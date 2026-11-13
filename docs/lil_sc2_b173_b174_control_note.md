# Lil SC2 B173-B174 Golden Crown and Julian control note

B173-B174 contain 44 source dialogue records, all translated in
`translations/lil_deep_route_v74.json`. Lil follows the Golden Crown of
Silla lead to King Muryeong's Tomb. Julian gives the crown to Mihwa and
joins Lil's crew.

Source presentation leads are `02` Lil, `0E` Emilio, `1A` Julian, `C9`
Mihwa, and `CA` the Seoul tavernkeeper. Newly observed `CA` is registered
in `lil-story-deep-route-v74-live`. These blocks contain no name macros.
The English prose avoids literal uppercase `I` and `F`, which are unsafe
renderer bytes.

All 44 records pass the fixed-byte, speaker, wrap, pair-phase, and
first-glyph audit. All three exact-font contact sheets were visually
reviewed; no leading glyphs are dropped. Direct saved-ROM verification
confirms all 44 inserted records.

Runtime cold-boot remains necessary to check the tavern lead, the crown
handoff, Julian's recruitment, portraits, nameplates, first and
continuation letters, and transitions.
