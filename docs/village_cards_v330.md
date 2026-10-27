# Village caption cards and clipped source fragment V330

Current ROM remains V326, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.
No ROM, artwork or patch was changed.

## Source context and complete translations

All eight full clean/current images were extracted and visually reviewed at
256x192. The original assets are white cards with handwritten scene labels;
they do not contain painted village scenery that the translation removed.
This observation is not a claim that the cards are unused.

| Image | Current complete caption |
|---|---|
|168|Arab Village 1|
|169|New World Village|
|170|Chinese Village|
|171|North Sea Village|
|206|Arab Village (Developed)|
|207|New World Village (Developed)|
|208|Chinese Island (Developed)|
|209|North Sea Village (Developed)|

The readable Japanese preserves region and development state. Image168's
explicit numeral1 remains present. Image208 explicitly uses island, so that
distinction is retained. Image207's village context is drawn from its paired
image169, whose readable 新大陸の村 explicitly names a New World village.
No town identity, additional numeral or invented scenery is supplied.

## Image207 fragment retention

The top stroke touches the original image boundary. Its full eight-connected
component comprises **279 nonwhite source pixels**, bounded by `(137,0)` through
`(194,20)` exclusively. Every one remains source-exact. Source row20 is blank;
the main Japanese caption starts below it at row21. The preserved top20 rows
therefore contain the complete connected stroke, not an arbitrary partial tail.

The clipped stroke does not establish an unambiguous extra word or numeral.
Its identity remains unknown. The decision is to retain it verbatim and avoid
inventing or erasing a reading. This is evidence for preservation and the
retention policy, not a claim that its original meaning has been recovered.
Actual scene usage and viewer context remain separate open requirements.

## Current stored-letter verification

An independent reconstruction uses the current ROM's native ASCII glyphs at the
recorded six-pixel advance. Every stored ink, blank cell and background pixel
matches across all eight complete planes. That covers **171 character cells**
and **1,972 ink pixels**. Caption bounds fit the original256x192 images.

Sixteen negative checks erase each caption's complete first or final character;
every whole-plane comparison rejects the erasure. The numeral1 and closing
parentheses participate in the checks. Headers, flags, palettes and complete
byte extents match clean source. Image207 additionally preserves the original
top region while translating the readable caption below it.

Stored-caption correctness does not prove original parent selection, actual
scene reachability, scaling/crops, palette/alpha or final GPU readability. No
supplied fixture is relabeled as gameplay verification.

## Audit and continuing goal

Both graphics audits, the requirements ledger and progress documents record
the current source/context/lettering evidence. The mark identity and actual
scene requirements remain visible. All 18 plaque/hint entries and Armor/Weapon
variants remain incomplete. Other legacy/final-rendering/gameplay gates remain
open. Low resolution Online screenshots remain exempt by user instruction.
The graphics goal stays active; revisit older record-based checks at actual
completion.

Evidence: `work/analysis/image207_review_v330/proof.json`, all16 source/current
PNGs and the two full-size pair sheets. Verifier:
`scripts/verify_village_cards_v330.py`; focused Ruff passes.

![Base village cards](<C:/Projects/Personal Projects/g-p-6a676ab5787c819181af4a29d5cebfbc/dk4-translation-tool/work/analysis/image207_review_v330/pairs_0.png>)

![Developed village cards](<C:/Projects/Personal Projects/g-p-6a676ab5787c819181af4a29d5cebfbc/dk4-translation-tool/work/analysis/image207_review_v330/pairs_1.png>)
