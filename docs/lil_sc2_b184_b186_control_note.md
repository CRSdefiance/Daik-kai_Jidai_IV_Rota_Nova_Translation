# Lil SC2 B184-B186 market-scene control note

B184-B186 contain 29 source dialogue records, all translated in
`translations/lil_deep_route_v82.json`. The scenes cover Sofala tea,
Stockholm furs, and Alexandria sweets.

Source presentation leads are `A4` and `A5` for the tea and fur
conversations, `AE` and `AF` for the sweets patron and attendant, and
`FE` for the market notices. There are no name macros in these blocks.
English prose avoids literal uppercase `I` and `F`, which are unsafe
renderer bytes.

All 29 records pass the fixed-byte, speaker, wrap, pair-phase, and
first-glyph audit. Both exact-font contact sheets were visually reviewed.
Direct saved-ROM verification confirms all 29 inserted records.

Runtime cold-boot remains necessary to check the three conversations,
portraits, nameplates, first letters, and market notices.
