# Lil SC2 B180-B182 market-rumor control note

B180-B182 contain 29 source dialogue records, all translated in
`translations/lil_deep_route_v80.json`. The scenes cover a Lisbon scent
that drives spice demand, an Athens ruby necklace, and a London princess's
engagement ring that drives gem demand.

Source presentation leads are `A6`-`A8` for the townspeople and `FE` for
the market notices. There are no name macros in these blocks. English
prose avoids literal uppercase `I` and `F`, which are unsafe renderer bytes.

All 29 records pass the fixed-byte, speaker, wrap, pair-phase, and
first-glyph audit. Both exact-font contact sheets were visually reviewed.
Direct saved-ROM verification confirms all 29 inserted records.

Runtime cold-boot remains necessary to check the three rumors, their
portraits and nameplates, first letters, and market notices.
