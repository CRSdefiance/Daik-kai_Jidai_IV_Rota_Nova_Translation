# Lil SC2 B112 control mapping

B112 is the sandbar rescue and the grandfather's gift. The clean Japanese source
and source-identical SC0 B121, SC1 B121, and SC3 B95 rescue records corroborate
`A3` for the boy, `AA` for his grandfather, `D6` for the lookout, and `D7` for the
rescuer. `02` is Lil and `D0` is a selected companion. V31 retains each single-byte
presentation state through `{SPEAKER:XX}`.

The `81`, `82`, `8E`, and `94` beginnings in companion variants are ordinary
Shift-JIS text. In particular, `94 43` is the first character of 任せて, not a
speaker selector. Their English starts directly with its first visible character.
The child explicitly calls the elderly man his grandfather; his familiar address
to Lil is localized as a farewell without inventing a sibling relationship.

B112 R0010 is the seven-byte non-prose scene fragment `46 8F 80 80 43 1E 63`.
V31 excludes it and leaves its bytes unchanged pending runtime mapping. All
30 dialogue records passed the fixed-box audit and visual preview review.
Portraits, the rescue transition, short companion variants, first glyphs, and
the gift event still need a cold-boot scene sample.
