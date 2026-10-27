# Lil SC2 B105 Sphinx presentation states

This map uses the clean B105 source and source-identical records on the other
routes. It supports an experimental profile, pending a cold-boot scene check.

- `02` and `09` retain Lil and Kamil's established route selectors.
- `FE` is the Sphinx voice, continuing the temple voice from B104. B105 R0010
  matches SC0/SC1 B114 R0011/R0010 at the source-byte level.
- `CF` is the party reaction after a failed answer. B105 R0047 and R0063
  match SC0 B114 R0067 and R0083 byte-for-byte; the SC0 profile treats `CF`
  as presentation state.
- `82`, `8E`, and `92` begin ordinary Shift-JIS choice text here. For example,
  R0083 begins `8E A9` for 自, and R0027 begins `92 6D` for 知. These bytes must
  stay part of the source word, not become speaker selectors.
- Kamil's R0213 contains the `FI` runtime name macro after its `09` selector.
  The Lil profile models its three-byte ASCII expansion and pair phase.

The candidate must still be cold-boot tested for the Sphinx's portrait, choices,
answer branches, first glyphs, and transition out of the temple.
