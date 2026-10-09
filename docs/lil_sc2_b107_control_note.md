# Lil SC2 B107 temple clue

B107 contains 17 source records. Sixteen are ordinary dialogue with established
Lil presentation states: `FE` for the temple voice, `02` for Lil, `09` for Kamil,
and `97` for a sailor. Their lines are translated in Lil V28.

The first record, B107 R0003, is exactly four bytes, `10 46 94 80`. Although
the first byte resembles Gerhard's speaker selector, the remainder does not
form a coherent Japanese sentence or a valid standalone name macro. It is
explicitly excluded from translation and retained byte-identical pending a
runtime map. Treating `46` as a literal English `F` would also invoke renderer
macro behavior. No portrait or dialogue claim is made for this fragment.

The dialogue still needs cold-boot review for the voice's presentation, the
repeated star clue, first glyphs, and transition into the following scene.
