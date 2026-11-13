# V702: complete copyright and ship texture coverage through native tiles

## New coverage

The previous goal turn made progress through V701's six actual control-widget
displays. V550 already supplied isolated display evidence for two title images;
repeating that title experiment would not locate their original consumers. This
checkpoint instead adds actual pixel coverage for two remaining standalone files:

|Original retained file|Extent|Complete bytes|Native tiles|Source pixels|
|---|---:|---:|---:|---:|
|`/_pxl/copyright.pxl`|256x16|4,628|6|4,096|
|`/_pxl/ship_eurL.pxl`|312x246|77,284|63|76,752|

Both entire files are byte-exact to clean Japanese-ROM sources. The copyright
line is already Latin text, including its original1999–2006 date. The ship file
is a texture sheet with mast,sail,rail and panel/inset material,not an untranslated
scene caption. Retain both without wording,colour,palette,alpha or geometry changes.

All80,848 source pixels are covered exactly once,including transparent positions,
first/final copyright characters,and the ship's complete right/bottom edges.
All69 full upper screens match independent source/palette/background models:
3,391,488 native five-bit comparisons. Upper RGB differences from each baseline
occur at exactly the independently predicted changed pixels,without exclusions.

## Explicit file-slot and widget fixtures

Two research-only ROM copies replace only the data in the existing
`/_pxl/kakutei.pxl` file slot with one entire unmodified source file. All other
file data,ARM9,ARM7,overlay tables,file IDs and banner are exact to production.
Rebuilt ROM layout/FAT offsets are not claimed byte-identical. The actual source
files remain present unchanged at their original paths as well.

These copies are stored under the analysis directory's `research_roms` on E:,named
`BORROWED_SLOT_NOT_PLAYABLE_RELEASE`. They are not registered combined releases,
patches,canonical candidates or updates to the latest playable ROM pointer.

Four terminal cold boots use the unchanged prepared V476 equipment donor:
two research cases and two production baselines. Copyright runs end at7000 frames;
ship runs end at12700,total39,400 frames. Normal inputs open Sailor Info. Its
original image widget then loads the borrowed slot through the real SDK filesystem
and native cache. No SDK bridge or decoded picture/palette injection is used.

Each case starts with an uncached owner and a real original SDK Open request for
`_pxl/kakutei.pxl`. This is deliberately **not** evidence that the original game
requests `copyright.pxl` or `ship_eurL.pxl` in normal scenes.

Only six widget-source words are changed at installation. Subsequent source tiles
change four source-coordinate/extent words. Temporary CPU R3 redirects use the
unchanged registered `(192,64)` coordinate pair. Tiles never exceed48x28,so the
312x246 source is not resized or forced into a256x192 whole-scene canvas.

Every install,tile update and restore verifies the complete4 MiB RAM,with only its
declared words changed,and unchanged CPU/DTCM/ITCM at each data write. Argument
redirects change only R3 in its separate host CPU region. Source inputs restore
before normal menu exit. Fifteen native host-prefix/ABI and eight bounded-read
controls pass; all hooks restore and the core file remains exact.

## Binding and restored behavior

All69 original copy calls bind their exact source file bytes,actual source XYWH,
palette0 and destination. All69 held source views also resolve complete exact
files through native hot-cache getters,with complete ABI and no I/O bridge.
Every executed getter word matches clean original code.

All30 pre-fixture whole RGB pairs match production baselines. All six restored
Info/roster whole RGB pairs match too. Live input fields are checked before parent
destruction; freed/reused heap bytes are not treated as persistent UI fields.
Whole pre-fixture RAM equality is not claimed across research ROMs whose file
layout/FAT data differ. The same donor remains byte-exact throughout.

## Cursor timing: retained failure and correct limit

The initial model required both complete screens to match the production baseline
except the substituted image. At ship tile6/frame6680,it failed at236 pixels in
the lower equipment cursor,with **zero** differences in the upper tile/source
model. Every address and actual/expected colour from that failure is retained.

The final verifier independently checks each complete lower screen against the
two full original-native cursor compositions from V663. It does not mask the ring
or fit a partial source region. All660 production PXL files and all recorded
instructions for both original paints remain byte-exact to the current version;
binary outputs,ABI,complete write coverage and hashes are bound to that evidence.

All138 complete lower planes (research plus baseline) match exactly one whole
native on/off composition. Ship's research captures include56 on/7 off; its
baseline54 on/9 off. Both copyright sets show six on states. This establishes
intact lower-screen content and source-defined cursor states. It does **not**
predict current SDK ticks or assert equal blink phase across the differing
research-ROM loading workloads. No timing defect,production fix or full-clock
equivalence is inferred. V694/V698's separate replay-model gaps remain open.

An earlier import failure occurred before emulation because a removed unused
re-export was imported through the preparer. Both logs,initial producer and initial
preflight remain retained. The corrected producer hash is pinned before all four
actual runs and remains frozen throughout; research ROMs and all other preflight
fields remain unchanged from the initial preparation.

## Visual review and evidence

Three sheets were opened: original versus assembled actual copyright tiles,
original versus assembled actual ship tiles,and four unmodified full fixture
screens. Both reconstructions match in native five-bit colours and source alpha.
Copyright wording and punctuation remain complete; the ship texture's blank/
transparent regions and black panel material are retained,not repainted.

The reconstructions are labelled **tile composites,not one game frame**. Source
alpha determines their checkerboard previews; invisible RGB is protected by whole
file hashes rather than inferred from the framebuffer. No fixture or composite is
a guide candidate or proof of a normal whole-picture scene.

- Analysis: `work/analysis/standalone_tiles_v702/`.
- Captures: `E:/Rota Nova translations/Generated/work/emulation_v193/standalone_tiles_v702_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V702 Standalone source tiles`.
- Scripts: prepare/run/verify/record/archive verification with suffix `v702`,plus
  `scripts/lower_native_reference_v702.py`.

## Unchanged release and open goal

V692 remains the production experimental ROM,SHA256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
Production ROM,art,patch,manifest,registry,canonical baseline and pointers remain
unchanged. No production compile,commit,push or guide promotion is created.

This adds complete fixture-based native display coverage for both retained
standalone source files. Original filename consumers,normal parent scenes,
intended whole-picture composition and other legacy/embedded copies remain open.
It does not change the historical656/660 original-loader-consumer census to a
660/660 claim. All18 original plaque/hint entries remain incomplete and all22
historical requirement objects stay exact. Broader graphics/restoration review,
comic playback,older record-based checks and final acceptance remain open.
The full graphics goal remains active.
