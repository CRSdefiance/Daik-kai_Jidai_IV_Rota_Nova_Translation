# Lil SC2 B168 Mikhail recruitment control note

B168 contains 52 source dialogue and tutorial records, all translated in
`translations/lil_deep_route_v69.json`. Lil's crew meets scholar Mikhail,
recruits him for his item knowledge, and unlocks the item-information
display. The scene includes Mikhail's inappropriate remarks and Lil's
rebuke, rendered in natural English without changing the plot.

The source presentation leads are `02` Lil, `06` Lil's grandfather, `09`
Kamil, `14` Fernando, `4C` Mikhail, `57` townsman, `A5` and `A6` young
women, and `FE` system instructions. Newly observed `57` and `A6` are
registered in `lil-story-deep-route-v69-live`. All seven `FI` given-name,
one `FA` surname, and one `FO` fleet-name macros are preserved. English
prose avoids literal uppercase `I` and `F`, which are unsafe renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audit
found zero blockers. All three exact-font contact sheets were visually
reviewed. Direct saved-ROM verification confirms all 52 inserted records.

Runtime cold-boot remains necessary to check the townsman's lead-in,
Mikhail's demonstration and recruitment, macro substitutions, portraits,
nameplates, first and continuation letters, transitions, and the X Button
item-information tutorial.
