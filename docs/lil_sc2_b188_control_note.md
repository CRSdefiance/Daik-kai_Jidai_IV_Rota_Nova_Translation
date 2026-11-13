# Lil SC2 B188 Osaka glass control note

B188 contains 11 source dialogue records, all translated in
`translations/lil_deep_route_v84.json`. An Osaka lord admires an object
called giyaman, learns it is glass, and orders his attendant to gather more.

The source-leading `82` and `96` bytes are Shift-JIS text leads, not
presentation states. Their English replacements therefore start directly
with visible letters. The final `FE` is the market notice state and is
preserved. There are no name macros. English prose avoids literal uppercase
`I` and `F`, which are unsafe renderer bytes.

All 11 records pass the fixed-byte, speaker, wrap, pair-phase, and first-glyph
audit. The exact-font contact sheet was visually reviewed; every first
letter is intact. Direct saved-ROM verification confirms all 11 inserted
records. Runtime cold-boot remains necessary to check the lord and attendant
scene, portraits, nameplates, first letters, and market notice.
