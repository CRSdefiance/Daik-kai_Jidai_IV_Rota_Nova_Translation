# Lil SC2 B192-B194 market-scene control note

B192-B194 contain 33 source dialogue records, all translated in
`translations/lil_deep_route_v88.json`. The scenes cover Istanbul tobacco,
Seoul chili peppers, and Hangzhou sake, including a companion's reaction to
the sake rumor.

The source-correlated presentation leads are inherited `99`/`73` for the
Istanbul townsmen, `A6`/`A7`/`A8` for the Seoul guests and cook, and `06`
for the companion. Hangzhou townsmen use `9C`/`75`, newly added to the Lil
V88 profile. Market notices use inherited `FE`. The B194 companion line
retains exactly one live `FI` name macro. English prose avoids literal
uppercase `I` and `F`, which are unsafe renderer bytes.

The B192 source names Istanbul. Earlier route batches use a fullwidth `Ｉ`
to avoid the unsafe ASCII `I`, but the exact-font preview renders that
character as a box. The Lil notice uses the historically appropriate
`Constantinople`, which renders fully and fits the native line.

All 33 records pass the fixed-byte, speaker, macro, wrap, pair-phase, and
first-glyph audit. Both exact-font contact sheets were visually reviewed;
every literal first character is intact. The `FI` macro is shown as a preview
placeholder and still needs runtime name-expansion review. Direct saved-ROM
verification confirms all 33 inserted records. Runtime cold-boot remains
necessary to check the conversations, portraits, nameplates, first letters,
live companion name, and market notices.
