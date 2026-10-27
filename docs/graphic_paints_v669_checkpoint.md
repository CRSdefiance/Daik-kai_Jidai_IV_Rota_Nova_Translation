# V669: indexed-image calls, cached views and complete source-file bindings

V668 made progress through actual indirect resource requests, source-view fields
and three-run evidence. Its request trace could miss cached-direct views. This
checkpoint observes original pixel-primitive entries directly on unchanged V666.
It creates no new ROM, artwork, patch or release profile.

## Original entry and observer contracts

| Original primitive | PC | Source argument contract |
|---|---|---|
| Scaled copy |01FF8E4C|r3 source XY; stack0 size pointer; stack1 destination LTRB pointer|
| Corner copy |01FF92D8|r3 source XY; stack0 size pointer; stack1 destination XY pointer|
| Tiled copy |01FFAE70|r3 source XYWH; stack0 destination LTRB pointer|

The instructions at all three entries match the clean source in declared main
sections/overlay. All use source interpreter slot92F. The diagnostic changes
only this private process's one host opcode pointer. It records CPU parameters,
bounded main-RAM descriptors/stack words and source headers, preserves host
registers/flags/stack, and tail-jumps to the unchanged original handler once.
The pointer is restored and the DLL file remains exact. No game ROM, RAM, VRAM,
register or input is written by observation.

Thirteen isolated native host controls verify corner/scaled/tiled arguments,
Frame/Confirm/Marker identity, identical headers, whole-file comparisons, changed
last bytes, disabled/overflow paths, unsupported source pointers and unexpected
PC/instruction values. They compare all supplied source RAM and original return
behavior. They are scratch controls, not gameplay or rendered-pixel evidence.

## The header collision and its resolution

Frame and Marker are different35444-byte files with identical20-byte headers.
A complete ROM census finds only those two PXLs sharing this header. The first
observer's whole-Frame comparison therefore correctly declines4559 New Game and
1340 equipment candidates. Header-only identification would misclassify them.

The extended observer compares every candidate against the complete expected
Frame and Marker files in host memory. It also compares the complete532-byte
Confirm file when its header matches. These are byte-for-byte comparisons, not
hash fingerprints or selected palette/header samples. Fresh repeats resolve
all5899 earlier candidates as exact current Marker files. Every original entry
register, descriptor, header and guard field remains identical across versions.
No live runner/helper was edited; initial runs, source files and controls remain
retained separately.

One scratch expectation initially retained the old unknown ID3 for a corrupted
Frame. After Marker fallback, shared metadata matching neither complete atlas
correctly receives joint unknown ID7. The expectation is corrected; the same
corruption remains rejected. No game or source asset bytes changed.

## Actual runs and selected sources

Four observed and two unmodified baseline cold boots finish normally. New Game
uses the ordinary24100-frame title/selection/story/town schedule; equipment uses
an isolated byte-exact cartridge save and the ordinary8063-frame five-slot cursor
schedule. No savestate or live gameplay fixture is used. All828 observed/baseline
sampled whole two-screen pairs match:89 New Game and325 equipment frames for
each of the two observer versions.

| Case | Primitive entries per observer version | Whole Frame matches | Whole Marker matches | Other headers |
|---|---:|---:|---:|---:|
|New Game/town|285527|110053|4559|170915|
|Equipment|122243|16843|1340|104060|

All407770 entry records repeat in the same order between observer versions.
No capacity overflow, instruction mismatch or unsupported argument/header read
occurs. All target source coordinates, dimensions, palettes, screen indices and
direct original caller bindings validate. The two cases have67 and54 distinct
target geometry/palette/primitive tuples respectively.

Every whole-Frame-bound selected source footprint avoids the five miniature
Done/Rank/Cancel/Pick Cargo/Pick Ship cells. Zero-sized tiled descriptors are
treated as repeating one source pixel, following the original helper contract;
they are not silently counted as unused. Confirm is not selected through these
three functions in either schedule. Equipment additionally records535 selections
of the current male-symbol source cell. These statements concern selected source
inputs and complete resource identity, not individual finished paints or proof
that every glyph survives subsequent clipping/overlays.

## Limits, evidence and retained scope

Other headers are not assigned filenames by guesswork. Other native primitives,
runtime copies, input contexts and the six actual control display contexts remain
open. The observer requires no resource-getter request, so these entry paths can
cover a cached-direct view too. This is not a count or independent identification
of every view type, global non-use or coverage of every rendering path.
Per-entry return/paint completion and complete individual destination pixels are
not inferred from an entry trace. Whole-screen baseline equality covers only the
declared sampled frames.

- Verify: `scripts/verify_graphic_paints_v669.py`; targeted Ruff passes.
- Proof and complete contracts/controls: `work/analysis/graphic_paints_v669/`.
- Captures/logs: E Generated/work/emulation_v193/graphic_paints_v669_*.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V669 Indexed image calls`.
- ROM: `out/all_routes_combined_v666_candidate.nds`, SHA256
  `706350a55a058b7a87b67d396333ed397dac664ba36ea378161d18fd085ba121`.

All six reports, complete traces, unmodified PNGs, executed sources, initial
unresolved candidates and final proofs are retained. No guide promotion, commit,
push or canonical promotion. ROM, patch, registry and release pointers stay exact.
All18 original plaque/hint entries remain incomplete; all22 historical scopes
remain unchanged. Card/legacy/material/equipment/movie contexts, older record
checks and final acceptance remain in the active graphics goal.
