# Lil SC2 B199 portrait and book control note

B199 contains 32 source records: 31 natural-English text records and one
four-byte packed item/scene event. Samwell asks about Rocco Alemkel's portrait;
Lil interrupts, chases him, and leaves Kamil to clean up. Kamil finds an old
book and offers it to Lil, who mistakes it for a gift. The payload at R0086
is `95 48 53 A8`, between the handoff and Lil's gift question. It has no
Japanese text and is explicitly excluded unchanged.

Samwell's `16`, Kamil's `09`, Lil's `02`, and the crash effects' `FE`
presentation states are preserved. Kamil's call to the admiral retains
exactly one live `FI` name macro. English prose avoids literal uppercase
`I` and `F`, which are unsafe renderer bytes.

All 31 text records pass the fixed-byte, speaker, macro, wrap, pair-phase,
and first-glyph audit. Four exact-font contact sheets were visually reviewed;
all initials and the macro placeholder render cleanly. Direct saved-ROM
verification confirms every text insertion and the unchanged payload.
Runtime cold-boot remains necessary to check scene timing, the book handoff,
the name expansion, portraits, nameplates, and first letters.
