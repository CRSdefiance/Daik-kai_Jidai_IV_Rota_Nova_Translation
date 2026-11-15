# Lil SC2 B178 Amsterdam wheat-boom control note

B178 contains 13 source dialogue records, all translated in
`translations/lil_deep_route_v78.json`. Three neighbors decide to bake
bread, and the market notice predicts an Amsterdam wheat boom.

Source presentation leads are `A6`, `A7`, and newly observed `A8` for the
three neighbors, plus `FE` for the market notice. `A8` is registered in
`lil-story-deep-route-v78-live`. There are no name macros in this block.
English prose avoids literal uppercase `I` and `F`, which are unsafe
renderer bytes.

All 13 records pass the fixed-byte, speaker, wrap, pair-phase, and
first-glyph audit. The exact-font contact sheet was visually reviewed.
Direct saved-ROM verification confirms all 13 inserted records.

Runtime cold-boot remains necessary to check the neighbors' portraits,
nameplates, first letters, and the market notice.
