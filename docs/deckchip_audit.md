# DECKCHIP audit

## Classification

`/data/DECKCHIP.DK4` is an ILNK-wrapped binary deck/ship-chip asset. It is not a normal dialogue or label string table.

## Evidence

- Container blocks: 16
- Blocks are 456-736 bytes long and contain 11-17 variable-length binary fragments.
- Those fragments do not decode as stand-alone Shift-JIS text records and do not have a shared text layout.
- Decoding arbitrary asset bytes as CP932 produces accidental Japanese glyphs, which is why the generic MESFILE scanner reported 29 false-positive records.

| Block | Bytes | Binary fragments | Classification |
|---:|---:|---:|---|
| 00 | 724 | 16 | Binary asset payload |
| 01 | 616 | 16 | Binary asset payload |
| 02 | 492 | 12 | Binary asset payload |
| 03 | 736 | 16 | Binary asset payload |
| 04 | 616 | 17 | Binary asset payload |
| 05 | 504 | 13 | Binary asset payload |
| 06 | 692 | 17 | Binary asset payload |
| 07 | 544 | 13 | Binary asset payload |
| 08 | 464 | 11 | Binary asset payload |
| 09 | 700 | 13 | Binary asset payload |
| 10 | 596 | 14 | Binary asset payload |
| 11 | 456 | 13 | Binary asset payload |
| 12 | 712 | 16 | Binary asset payload |
| 13 | 568 | 15 | Binary asset payload |
| 14 | 468 | 14 | Binary asset payload |
| 15 | 504 | 13 | Binary asset payload |

## Translation path

1. Locate the deck/ship screen that consumes each block through runtime tracing or a resource-map search.
2. Determine the asset format: tile graphics, tile map, palette, compressed sprite data, or a combination.
3. Render each block to an image only after the format is known; do not insert CP932 text into it.
4. Redraw any Japanese labels as English tiles, preserving dimensions and palette indices.
5. Repack the edited assets and verify the deck screen in-game for corruption and alignment.

Until steps 1-3 are complete, DECKCHIP has **zero confirmed text records** to translate.
