# Lil SC2 B152-B153 coin map control note

B152 has six dialogue records and B153 has nine. All 15 text records are
translated in `translations/lil_deep_route_v60.json` using the established
Ancient Kingdom Coin and Lotion Jar item names. A local identifies the coin
as a hidden Ruler's Proof map; Lil and Kamil use the jar to reveal the
Southeast Asian map. The source `FI` name macro in B153 R0029 is preserved.

`DK4_MES_B153_R0024` is an opaque four-byte map-reveal event payload with
exact hex `23 48 9F A8`. It is excluded unchanged. The dialogue source
leads are `02` Lil, `09` Kamil, and `5C` the local. English prose avoids
literal uppercase `I` and `F`, which are unsafe renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audits
found zero blockers. Both exact-font contact sheets were visually reviewed.
Direct saved-ROM verification confirms all 15 inserted segments and the
unchanged reveal control.

Runtime cold-boot remains necessary to check the item combination, map
reveal, name macro, first and continuation letters, and the next scene.
