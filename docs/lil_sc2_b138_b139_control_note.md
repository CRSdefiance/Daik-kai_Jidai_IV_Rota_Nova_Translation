# Lil SC2 B138–B139 tavern aftermath and southern Proof map

All 55 translated records were reviewed against the clean Japanese in
scene order, audited with `natural-dialogue-v2`, and visually checked in
exact-font preview sheets. There are no audit blockers, authored prose
breaks, or unsafe literal uppercase `I`/`F` renderer bytes. Individual
previews confirm opening glyphs that appeared cropped on contact sheets,
including B138 R0011/R0236/R0246/R0268 and B139 R0033/R0037/R0048.

- B138 (42): After Nagalpur Co. is absorbed by `FO`, the barkeep's sales
  collapse and Nagalpur's men leave unpaid tabs. A dubious treasure map
  can be bought for **100 gold**; if Lil lacks the money, he gives it to
  her for listening. Both branches remain translated. Lil reflects on
  Nagalpur's isolation and the barkeep says her words about money restored
  his pride. He gives her an unidentified leaf that leads into B139.
  `5C` is the barkeep; `02` Lil, `14` Fernando, `15` Ian, `0E` Emilio,
  `16` Samwell, and `17` Manuel. The `FO` faction macro is exact.
- B139 (13 translated, 1 excluded): Lil and Fernando combine the
  **Evergreen Lotus Leaf** and **Kushan Platter**. Lil accidentally
  spills water onto the leaf; its veins reveal the southern ocean's
  Ruler's Proof map when floated on the platter. Fernando's teasing and
  Lil's response remain intact. R0035 is an opaque four-byte
  `23 48 9E A8` event payload during the map reveal. It remains unchanged
  and is verified byte-for-byte. The source says Indian Ocean; the line
  uses "southern sea" because literal uppercase `I` is an unsafe renderer
  byte, consistent with other route localization of this region.

Cold-boot both map-price branches, the barkeep's later conversation,
leaf handoff, water-spill transition, map reveal, portraits, nameplates,
macro expansion, and first and continuation glyphs before accepting a
candidate.
