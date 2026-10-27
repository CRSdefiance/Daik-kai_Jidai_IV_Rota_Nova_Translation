# Lil SC2 B100–B104 presentation-state map

This map is for the experimental church and temple scenes. It compares the clean
`/data/SC2.DK4` source bytes with source-identical records in SC0, SC1, and SC3.
Those routes' existing batches encode the same single-byte presentation states.

| SC2 block | Lead byte | Effect supported by matching routes | SC2 evidence |
|---|---|---|---|
| B100 | `BC` | local woman | `B100 R0007` matches SC0/SC1 `B109 R0007` and SC3 `B82 R0006` byte-for-byte at the start |
| B101, B103 | `8B` | priest | `B101 R0005` matches SC0/SC1 `B110 R0005`; `B103 R0009` matches SC1 `B112 R0021` |
| B102 | `BF` | cathedral guide | `B102 R0007` matches SC0/SC1 `B111 R0007` and SC3 `B84 R0006` |
| B103, B104 | `D0` | selected crew speaker | `B104 R0015` matches SC0/SC1 `B113 R0015`; the party branch controls the identity |
| B104 | `FE` | temple voice | `B104 R0029` matches SC0/SC1 `B113 R0029` and SC3 `B86 R0028` |

Lil's `02` and `09` selectors retain their established Lil and Kamil meanings.
The B103 companion variants beginning with `82` and B104 variants beginning with
`82` or `92` start with ordinary Shift-JIS text, not a presentation byte. The
byte-aware source inspection decodes them without stripping their first glyph.

This is static, cross-route evidence. A cold-boot test of the integrated Lil
candidate must still confirm portraits, nameplates, first glyphs, choices, and
scene transitions before any promotion or player handoff.
