# Common raw raster source review V194

2026-10-05. Goal active/incomplete. Latest combined candidate remains V190;
V194 is source research, not a new ROM build.

The previous goal turn added the verified Online layout correction. This turn
recovers coherent complete artwork from the four unresolved CMMNIMG blocks.
Earlier whole-block compression and tile-layout guesses did not establish their
encoding. Palette-prefix row correlation identifies clear raster widths, and
exact byte partition/repacking preserves every original source byte.

| Block | Palette prefix | Interpretation | Complete cells | Observation |
| --- | ---: | --- | ---: | --- |
| 0 | 512 bytes | 8-bit, 56Ã—64 | 178 | Character portrait paintings |
| 2 | 512 bytes | 8-bit, 24Ã—24 | 100 | Trade goods/object icons |
| 3 | 32 bytes | 4-bit, 304Ã—200 | 8 | Unlabeled regional/world map paintings |
| 7 | 512 bytes | 8-bit, 32Ã—32 | 188 | Items, gear, consumables and artifacts |
| Total | | | 474 | |

The palette words all fit BGR555. Each complete palette/index stream and source
block repacks exactly. All 474 saved individual images and their full strips are
source-hashed, and V190's blocks remain byte-identical to canonical. The observed
cell dimensions and grouping are coherent interpretations, not declared native
metadata. Native palette/bank/alpha and actual usage remain open; the historical
eleven-unresolved-block census is not reduced from visual plausibility alone.

## Complete visual/source review

All 14 bounded review sheets were inspected. Each shows complete cells at native
scale or an integer enlargement; the 178-portrait catalogue is split into five
sheets so a tall contact sheet cannot hide details through display downsampling.
No written UI caption or instruction was observed in these cells.

Retain the original portraits, goods and map paintings. Small clothing markings,
book-cover motifs and ink on illustrated scrolls/papers are physical artifact
decoration, not a separate nameplate, menu label or player instruction. Retain
their painted design; do not invent exact book/scroll titles, a language reading,
character identities or item associations from indistinct strokes. Written item
names and lore presented by the UI remain separate translation/verification work.
This decision is limited to the 474 reviewed interpretations and does not clear
other archives or any native display gate.

## Loose/native equivalence checks

Native `itemtrade.pxl` uses 24Ã—24 cells and contains 124 icons; `item.pxl` uses 32Ã—32
cells and contains 218 icons. Their palettes, initial indexed payloads and rendered
icon hashes do not exactly match these legacy blocks. No correspondence is
asserted merely from matching dimensions or appearance. A search for the proposed
Lil portrait in the existing V190 dialogue capture did not establish exact pixel
equality. The native `CMMNIMG.000` resource has the same byte length as block 0,
but different content; it is not treated as an empty placeholder or an equivalent
copy without further mapping.

## Evidence and next work

- `scripts/research_common_raw_v194.py`.
- `work/analysis/common_raw_row_lags_v194.json`.
- `work/analysis/common_raw_v194.json`.
- `work/qa/common_raw_v194/block0_review_0.png` through `_4.png`.
- `work/qa/common_raw_v194/block2_review_0.png` through `_2.png`.
- `work/qa/common_raw_v194/block3_review_0.png`.
- `work/qa/common_raw_v194/block7_review_0.png` through `_4.png`.
- Complete source strips and all 474 individual PNGs in the same directory.

Ruff and exact source/palette/index/saved-image roundtrips pass. No ROM, patch,
runtime code or translated label changed. Further work should map these source
rasters to actual native consumers or metadata, rather than repeating failed
compression/tile guesses. Four Online body/dialogue/chat translations, seven
other raw ILNK blocks, these four native-format relationships, other format/source
fidelity and remaining visual/gameplay gates continue to hold the full goal open.
