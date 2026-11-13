# Lil SC2 B187 Malacca almond-medicine control note

B187 contains 16 source dialogue records, all translated in
`translations/lil_deep_route_v83.json`. Two men discuss a spreading cough,
an almond-based remedy, and a likely Malacca almond boom.

Source-correlated presentation leads are `9B` for the coughing man, `57`
for his friend, and `FE` for the market notice. `9B` is added to the Lil
V83 dialogue profile; `57` and `FE` are inherited. There are no name macros.
The English prose avoids literal uppercase `I` and `F`, which are unsafe
renderer bytes.

All 16 records pass the fixed-byte, speaker, wrap, pair-phase, and first-glyph
audit. The exact-font contact sheet was visually reviewed; each first
character is intact. Direct saved-ROM verification confirms all 16 inserted
records. Runtime cold-boot remains necessary to check the conversation,
portraits, nameplates, first letters, and market notice.
