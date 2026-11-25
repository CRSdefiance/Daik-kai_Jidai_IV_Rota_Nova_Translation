# Lil SC2 B205 parrot control note

B205 has 18 source records: 17 natural-English text or sound-effect records
and one four-byte packed scene payload. Angelo and Lil encounter and catch a
talking parrot; it repeats Angelo's words throughout the chase. R0007 is
`41 48 93 A8`, the same verified nontext parrot payload in Maria SC3 B178,
and is explicitly excluded unchanged.

Angelo's `0F`, Lil's `02`, and the parrot/effects `FE` presentation states
are preserved. The parrot echoes Angelo's English phrases exactly. Its
uppercase lines avoid literal `I` and `F`, which are unsafe renderer bytes.

All 17 text records pass the fixed-byte, speaker, wrap, pair-phase, and
first-glyph audit. Both exact-font contact sheets were visually reviewed,
including every echo and the final joke. Direct saved-ROM verification
confirms all 17 insertions and the unchanged payload. Runtime cold-boot
remains necessary to check event timing, capture, portraits, nameplates,
and first letters.
