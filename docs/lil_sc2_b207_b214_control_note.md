# Lil SC2 B207-B214 control note

The eight blocks contain 127 source records: 126 text records and one packed
sword event. B213 R0022 is `21 48 96 A8`, matching Maria SC3 B186 R0021's
verified nontext payload; it is excluded unchanged.

Presentation states are `02` Lil, `04` Janus's letter, `07` Cristina, `09`
Kamil, `0B` Jam, `0C` Yukihisa's letter, `0E` Emilio, `11` Al, `17` Manuel,
`95` the book enthusiast, `AA` an old man, `D0` the initial companion report,
and `FE` sound effects or the Charm notice. The V101 profile adds `95` and
removes Japanese text-leading `82/92/93/8A/8F/E6` from state detection.

There are 24 bare entries: 19 alternative companion reports/reactions and
five choices. The short names Zhao, Guan and Zhuge fit the original 4/4/6-byte
choice slots and identify Zhao Yun, Guan Yu and Zhuge Liang. Every bare entry
is tested to retain its first English glyph. Both FI name macros are preserved.

All 126 records pass byte limits, wrap, page, speaker, macro and glyph-phase
QA with no error or warning waivers. All 13 contact sheets were reviewed.
Saved-ROM verification confirms every insertion and the unchanged payload.
Runtime event and presentation checks remain pending.
