# Complete BGM title rendering research

## Integrated result: V130

The complete title manuscript and exact scoped tracking renderer are now registered
and integrated in experimental `all-routes-unified-v130`. All 38 title meanings and
formatting gates are reviewed for that renderer; 31 visible wordings change.
All 3,668 saved selections and 151 item owners pass, with 72 combined tests.
Promotional IDs 3289-3290 remain explicitly preserved untranslated and count as
Japanese; full source/current byte locks replace no translation requirement.
Live rendering/playback remains unverified. See the current campaign checkpoint
and `docs/common_preserved_native_neighbors.md`. Earlier sections below record
pre-integration research, including the former baseline-renderer formatting defect.

## Current result

The isolated ARM9 probe uses the native character-spacing field in the BGM
draw function's stack-local text context. All 38 reviewed complete English
titles fit the existing 128-pixel panel at a five-pixel ASCII advance.
**Southeast Asian Village** occupies 115 pixels, beginning at x=7 and ending
at x=122. Every title retains its complete wording and first/last characters
in the diagnostic previews. All five contact sheets and the following `Vol`
heading preview were visually reviewed. These are exact-font diagnostic panels;
live rendering and playback are still unverified.

The current playable candidate remains V129, with SHA-256
`468de4b2e9236c9c48f8a5e02e78ad3fc97c41b7c020ee02ab1eb45041b9133e`.
No ROM, profile, release layer, progress-count increase or canonical promotion
has been produced by this research.

## Mapped context and instruction change

At `0x020D5A98..0x020D5AF4`, the context constructor initializes horizontal
tracking at object + `0x1C` to zero. At `0x020D57E8..0x020D57F8`, the ordinary
horizontal text path adds that field to the font's ASCII advance before storing
the next x coordinate. The BGM draw routine creates the context at its own `sp`
with `0x020D5160`. This is the object passed to the title draw at `0x021092A8`.
Its source code measures titles at six pixels per ASCII byte; the previously
mapped standard ASCII font also has a six-pixel cell. The field therefore permits
a local tracking adjustment of -1. Actual runtime font metrics need cold-boot
confirmation with this probe.

The exact canonical ASCII font hash is
`427776b1266289206333d94cf27c292df0d15d6f26f7c52f3846fee641c32058`.
Every printable ASCII glyph has an empty sixth bitmap column. At five-pixel
advance the occupied pixels of consecutive glyphs do not overlap. The preview
uses all original glyph pixels and the resulting tighter spacing.

Four instructions at ARM9 `0x109280..0x109290` are replaced:

```asm
mvn r2, #0                  ; signed -1
str r2, [sp, #0x1c]         ; draw-local horizontal tracking
add r1, r0, r0, lsl #2      ; strlen * 5
asr r0, r1, #1              ; floor(width / 2), positive ASCII length
```

The following original `rsb r3,r0,#0x40` centers the text at x=64. The original
pointer, title y=50, draw call, native message loader, track-change code and
panel dimensions remain byte-identical. All bytes outside those 16 instruction
bytes remain unchanged; there is no added code cave or ARM9 size change.

The tracking field persists for the following volume heading drawn through the
same local context at x=24, y=98. Its accepted text is `Vol`, at ARM9 `0x1702C8`,
referenced by the literal at `0x10930C`. The diagnostic preview confirms all three
glyphs fit at five-pixel advance. This local-context scope includes that heading;
it must be included in the runtime check. The existing abbreviated ARM9 label
can be reviewed for full `Volume` wording during the broader UI inventory.

## Reproduction and evidence

```text
python scripts/plan_bgm_title_tracking_probe.py
python scripts/audit_common_bgm_titles.py --manuscript translations/common_bgm_complete_titles_v2.json --renderer-probe work/analysis/bgm_title_tracking_probe/ARM9.bin --out work/qa/common_bgm_tracking_probe
```

- Component: `work/analysis/bgm_title_tracking_probe/ARM9.bin`, SHA-256
  `d1d766233acc73f8d315589c77f634a2a746049aa6b31e696526d7e174b56332`.
- Full source/replacement instruction disassembly:
  `work/analysis/bgm_title_tracking_probe/arithmetic_disassembly.txt`.
- Geometry/source/font proof: `work/qa/common_bgm_tracking_probe/report.json`;
  no overflow among 38 titles. All five sheets and `volume_heading.png` reviewed.
- Seven probe regressions cover the 16-byte scope, unchanged ARM9 size, code/font
  lock rejection, complete village title geometry and native centering arithmetic.
  The combined integration/translation/sound/geometry suite passes **64 tests**.
  New and changed tools pass Ruff.

`dk4tool/patch/bgm_title_tracking.py` locks the original title function,
tracking addition and constructor ranges, plus the font and patch-site bytes.
The audit accepts only the exact probe derived from the canonical baseline;
an arbitrary advance setting cannot approve a modified renderer component.

## Integration requirements

The full BGM manuscript still shares one clean native owner with promotional
messages 3289-3290. Their full selected spans, source meaning and renderer must
be accounted for before integration through the complete-owner gate. The current
reblock transform permits only fully authored owners; the research preview does
not bypass that requirement. The baseline renderer still overflows title 3265,
so its manuscript formatting gate remains false until renderer integration is
explicitly accounted for by the profile.

A future experimental combined profile needs the full 428 inherited layers,
all 38 reviewed title selections, complete mixed-owner accounting, a source-locked
renderer layer, a renderer-aware saved-title verifier, manifest/inventory/item/
baseline/copy-cache gates, and cold-boot testing of first/last title selection,
all complete names, playback toggle, volume and return navigation. Do not promote
the canonical baseline without explicit user acceptance.
