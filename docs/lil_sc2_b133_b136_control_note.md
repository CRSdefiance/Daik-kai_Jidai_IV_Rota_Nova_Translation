# Lil SC2 B133–B136 localization and control note

All 109 new dialogue records were reviewed against the clean Japanese in scene
order, audited with `natural-dialogue-v2`, and visually inspected in exact-font
preview sheets. No audit blockers, unsafe literal uppercase `I`/`F` renderer
bytes, or authored prose breaks remain. The guarded pair-phase formatter
protects opening and continuation glyphs. The cropped B133 contact sheet
appeared to hide the first letter of R0075 and R0194; both individual preview
images show their full opening words, `You` and `Hmph`.

- B133 (47): Lil meets Raphael Castor and Claudio. The proposed exchange is
  two percentage points of Nantes share for one of Lisbon share. Both response
  choices and the transaction panel are translated. B133 R0022 begins with
  the `FO` faction macro (`46 4F`) followed by `FI`; `46` is not a speaker byte
  in this batch. The Raphael and choice lines with `82/83/8E/8F/96` leads
  begin directly with visible English text. `02` is Lil, `05` Claudio, `09`
  Kamil, and `FE` the transaction panel.
- B134 (27): Silveira claims West Africa as his trading territory. Both the
  withdrawal (`95` visible text) and defiance (`8F` visible text) branches are
  translated. Withdrawal transfers some of Lil's Sao Jorge town share.
  `23` is Silveira and `FE` is the share-loss panel.
- B135 (27): Espinosa raises the price of Goddess' Temptation after a buyer
  has sold their land; Lil resolves to end his narcotics trade. `24` is
  Espinosa, `2F` his guard, `60` the desperate buyer. The `FO` macro is kept.
- B136 (8 translated, 1 excluded): Lil and Emilio join the Upper and Lower
  Stone Tablets, exposing Africa's Ruler's Proof map. Emilio mistakes "map"
  for "cheese". `02` is Lil, `0E` Emilio. R0020 is an opaque four-byte
  `23 48 9D A8` event payload between joining the tablets and the map
  reveal; it remains unchanged and is verified byte-for-byte.

Cold-boot the scenes before acceptance. Check names, portraits, both B133 and
B134 branches, transaction/share panels, `FI`/`FO` expansion, the tablet
transition, first and continuation glyphs, and the cheese joke.
