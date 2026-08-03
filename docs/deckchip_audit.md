# DECKCHIP audit

## Classification

`/data/DECKCHIP.DK4` is an ILNK-wrapped binary deck/ship-chip asset. It is not a normal dialogue or label string table.

## Evidence

- Container blocks: 16
- Blocks are 456-736 bytes long and contain 11-17 variable-length binary fragments.
- Those fragments do not decode as stand-alone Shift-JIS text records and do not have a shared text layout.
- Decoding arbitrary asset bytes as CP932 produces accidental Japanese glyphs, which is why the generic MESFILE scanner reported 29 false-positive records.
- The ROM manifest maps `deckchip00.pxl` through `deckchip15.pxl` one-to-one with the 16 DECKCHIP blocks. Rendering `deckchip00.pxl` confirms these are ship-deck layouts with no Japanese labels.

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

1. The resource-map pass is complete: blocks 00-15 correspond to `deckchip00.pxl` through `deckchip15.pxl`.
2. The companion PXL files are deck-layout graphics, not label sheets.
3. Do not insert CP932 text or redraw these layouts; no Japanese label has been found in this asset family.
4. If a deck screen still shows Japanese, trace the on-screen text to the shared UI/font resources instead of DECKCHIP.

DECKCHIP has **zero confirmed text records** to translate and is now classified as non-translatable layout data.
