# Lil SC2 B183 Basra painting-craze control note

B183 contains 25 source text records, all translated in
`translations/lil_deep_route_v81.json`. Three collectors argue over
paintings, and the shopkeeper explains the craze to a visitor.

Source presentation leads are `99` the visitor, `94`, `6E`, and `84` for
the collectors, `55` for the shopkeeper, and `FE` for the door-slam cue
and market notice. Newly observed `55`, `6E`, and `84` are registered in
`lil-story-deep-route-v81-live`. The five-byte `99 82 F1 81 48` record
is a short interjection, not an opaque payload; its speaker byte and
visible first letter are preserved. There are no name macros in this block.
English prose avoids literal uppercase `I` and `F`, which are unsafe
renderer bytes.

All 25 records pass the fixed-byte, speaker, wrap, pair-phase, and
first-glyph audit. Both exact-font contact sheets were visually reviewed.
Direct saved-ROM verification confirms all 25 inserted records.

Runtime cold-boot remains necessary to check the interjection, collector
portraits and nameplates, shopkeeper conversation, door cue, and market
notice.
