# Common embedded-bank source review V250

Previous goal turn: progress on market-specific native crops and CPU/TCM source
verification. Current turn: whole source review of four historically unresolved
CMMNIMG blocks, complete palette/index accounting and rejected native-copy leads.
V250 is source research; V247 remains the unchanged registered candidate.

## Whole source accounting and visual evidence

The immutable canonical `/GRP/CMMNIMG.DK4` supplies the exact blocks below. Every
palette byte and payload byte is accounted for under the stated interpretation.
Decode/re-encode reconstructs each whole source block exactly, and the same blocks
in V247 remain byte-identical. The candidate source lock includes its exact SHA.

| Block | Palette prefix | Interpretation | Cells | Source content |
|---|---|---|---|---|
|0|512 bytes|8-bit56×64|178|Coherent full portraits|
|2|512 bytes|8-bit24×24|100|Coherent trade-goods paintings|
|3|32 bytes|four-bit32×32 test partitions|475|Striped output; intended layout unresolved|
|7|512 bytes|8-bit32×32|188|Coherent item/artifact paintings|

The complete accounting covers **1,132,832 bytes**. 9 bounded contact sheets
show all cells; the sheets include every source pixel. All178 portraits,100 goods
and188 item/artifact paintings were visually reviewed. No separate Japanese UI
caption or instruction was observed in these three coherent interpretations.
Keep the original contextual paintings. Small headwear, book-cover and scroll
marks are not assigned invented readings, item names or city/character identities.
Existing textual names/lore remain separate consumers.

These are complete source interpretations, not native-format declarations.
Palette prefixes, cell dimensions, bank choice, transparency and rendered usage
still require their native relationships. The source-review decision does not
claim that every tiny object mark is legible or that the raw banks are unused.

## Four-bit block3 remains open

The16-color prefix and remaining byte count permit a four-bit expansion and
exact repacking. That alone does not establish the intended picture.47532×32
partitions and eight320×190 slices produce striped patterns. Two8×8 tiled-order
variants also fail to establish an intended scene or caption layout. None is
adopted as the native image format, and **block3 receives no content clearance**.
The original bytes remain intact. Previous rejected whole-block decompression is
not repeated or treated as proof of an uncompressed format.

## Native-copy hypotheses rejected by complete comparisons

Visual resemblance is not sufficient to synchronize a raw bank from a native
atlas. Same-order full pixel comparisons and index-remapping tests were run:

| Raw block | Native comparison | Pixel positions | Equal RGB pixels | Ambiguous source-index mappings |
|---|---|---|---|---|
| 0 | `/GRP/CMMNIMG.000` | 637952 | 46192 | 220 |
| 2 | `/_pxl/itemtrade.pxl` | 57600 | 18350 | 204 |
| 7 | `/_pxl/item.pxl` | 192512 | 60388 | 209 |

No tested pair has identical rendered colors or a single consistent index remap.
One source index maps to as many as10/11/12 native indices in the portrait/goods/
item comparisons. These tests reject the tested same-order equivalence; they do
not rule out reordered, resampled or differently encoded relationships. No copy,
palette borrowing, synchronization or destructive rewrite follows from them.

## Remaining scope and user-directed plaque status

The historical11 unresolved legacy blocks remain11. This source review does not
silently promote raster interpretations to native-format or runtime clearance.
Unresolved raw/native relationships, block3's intended layout, legacy SLACKIMG
sources, four Online screenshot bodies and wider graphics/native/gameplay gates
remain in the full goal.

All17 redesigned plaques and the Equipped Items hint stay **incomplete, pending
continued audit and user review** in both authoritative audits. This batch does
not close any of those18 entries. No ROM, patch, release stack or production
renderer changes. The full graphics goal stays active.

## Artifacts

- `scripts/review_common_raw_banks_v250.py`, Ruff passing.
- `work/analysis/common_raw_banks_v250/proof.json` and all9 full review sheets.
- `paper_pages_320x190.png` and `paper_cell_tile_hypotheses.png`: unadopted layouts.
- `native_portraits_first8.png`: visual comparison only, not identity evidence.

## V256 correction to the block3 source classification

V194 already decoded block3 as eight304x200 map paintings. V250 wrong-width
partitions did not supersede that evidence. V256 revalidates every cell hash and
current ROM preservation, and retains the unlabeled maps. Native legacy use remains
open; see `map_source_and_native_cache_v256.md`. Historical diagnostic images remain.
