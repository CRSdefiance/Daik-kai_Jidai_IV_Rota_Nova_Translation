# Lil SC2 B111 control mapping

B111 is the gold-temple argument between Lil and the monk, followed by the
monk's demand that she train and buy rice. The clean Japanese source shows
`02` before Lil, `09` before Kamil, and `89` before every spoken monk record.
Removing the single `89` byte from those monk records exposes coherent Japanese
starting with ordinary Shift-JIS text. The `89` state is therefore mapped only
in the V30 dialogue profile; B109 records that begin with `89` still use the
earlier profile and retain their first text character.

The monk's B111 R0062 and R0138 are both exactly `89 81 63`, a state plus a
language-neutral ellipsis. They are explicitly excluded and left byte-identical.
Kamil's B111 R0112 preserves the three-byte `FI` runtime macro for Lil's name.
All 33 translated records passed the fixed-box audit and visual preview review.
The monk's portrait, nameplate, first glyphs, and scene transition still need
cold-boot confirmation.
