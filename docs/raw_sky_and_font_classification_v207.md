# Raw sky records and character-font classification V207

2026-10-07. No release bytes changed. V205 remains current; full goal active.

Follow-up: [V208](sky_texture_geometry_v208.md) resolves the regular source layout
as a linear 256×32 indexed texture and replaces the tiled diagnostic views for
source-art review. The "BG" transfer wording below is an earlier interpretation;
refer to these as native graphics transfers. No BG tile-map layout is established
by the V207 loader fragment.

## SKYWALL: all record boundaries loaded natively

The actual loader fragment at `0207BA3C..0207BA7C` opens
`/GRP/SKYWALL.DK4`, seeks to `index × 0x2200`, reads a normal `0x2200`
record or the exceptional `0x4200` record at index 13, and closes the file.
All 14 supplied indices execute this unchanged native fragment. Only SDK
filesystem operations are bridged to the exact ROM file. The preceding index
and buffer context are explicit fixtures; a complete scene constructor is not claimed.

| Records | Count | Pixel-transfer bytes per record | Trailing palette bytes |
|---|---:|---:|---:|
| 0–12 | 13 | 8,192 | 512 |
| 13 | 1 | 16,384 | 512 |

The following original caller instructions at `0207BA80..0207BAA8` pass
`size − 512` to the BG pixel-transfer routine and the final 512 bytes to its
palette-transfer routine. Those hardware routines are inspected, not executed
by this loader proof. Every loaded byte and both buffer guards match; fragment
registers/stack are intact, every handle closes, and all records together cover
exactly **130,048 bytes** with no gap or tail. The loader code and entire source
file remain exact to clean and V205.

All 14 diagnostic eight-bit tile views were inspected. They contain blue, grey,
sunset and night sky/weather-like components, with no readable Japanese label
in this interpretation. The tiled assembly is a diagnostic interpretation, not
proven screen geometry: visible discontinuities mean it must not serve as final
visual clearance. BG depth, tile/map arrangement, normal scene selection, full
GPU crops and assembled source-art review remain open. Original pixels and
palettes are retained pending that evidence.

## KANJI.FNT: preserve the character font

The current `/GRP/KANJI.FNT` is exactly **73,480 bytes**, matching clean SHA-256
`41b9f2f2da08e7fc80715506614dd4d0c18365b78cd89ff5982f2f9e7de3b669`.
The standard-font audit verifies the actual sorted 3,340-entry Shift-JIS map,
matching 22-byte cell records and native painter signatures. These are 16×11
packed glyphs with a 12-pixel advance, rather than composed interface labels.

Retain this font so source proper names and permitted Japanese player input can
still render. Translate composed messages and artwork, not each isolated glyph
in a source character font. This resolves the asset's classification/retain
decision; it does not declare every text consumer translated or every physical
font-loading/display path tested. Earlier native lookup/painter evidence is
documented in `docs/arm9_text_inventory_and_race_rules.md`.

## Reproducible evidence and remaining work

Script: `scripts/research_skywall_native_v207.py`.
Proof and diagnostic PNGs: `work/analysis/skywall_native_v207/`.
All native reads, source/preview hashes and the current font audit are saved in
`proof.json`. No research NDS was created for this work.

The eleven unresolved ILNK blocks remain unresolved; SKYWALL and KANJI are
separate raw files. Other raw GRP resources, four Online screenshot bodies,
confirmed-name consistency, contextual/embedded graphic consumers and the final
registered combined ROM/patch and gameplay verification remain in the full goal.
