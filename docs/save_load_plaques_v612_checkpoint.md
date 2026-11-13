# V612: original Save/Load plaque frames and actual normal screen verification

The preceding batch found and repaired regional-fleet asset defects, but its
attempted native backdrop selector did not display those plaques. This batch
addresses the additional Save/Load material finding through its actual normal
screen. The full graphics goal remains active.

## Source-based correction and translation

Original `/_pxl/saveloadinfo.pxl` has two 40x16 plaques at `[96,40,136,56]` and
`[96,64,136,80]`. The historical English edits leave conspicuous horizontal fills
and overwrite original right/bottom rims. Actual Save/Load captures reproduce
the source atlas and those old fills; this is not just an isolated image lead.

The source-framed repair restores the original two-pixel rims at their exact
original coordinates: 416 samples across both plaques. Each 36x12 interior uses
one contiguous unlettered original towninfo sample `[3,62,39,74]`, with its
nearest original destination palette colours. There is no repeated join,
stretching, new palette or moved/resized frame. Concealed interior material is
reconstruction; the hidden original texture is not claimed recovered.

`Level` faithfully labels レベル. `Power` retains the existing natural noun for
勢力値, the faction power value, consistent with the existing faction interface.
No new wording, numerical formatter, rank, model or dialogue is introduced.
Complete original native ASCII glyphs use five-pixel advance. Independent masks
verify all 123 ink points, first/final letters and blank cells; four explicit
first/final-letter erasure controls fail. Only 1,037 palette indices change.
Every original header, palette bank, dimension and unowned pixel is preserved.

The selected historical edit rectangles are restored before the final face and
letter pass. Visible native frame geometry is checked independently of English
font matching. Enlarged original/current/final art and actual framebuffer sheets
were visually inspected; neither broad row bands nor vertical repeat seams remain
in these observed plaques.

## Actual ordinary Save/Load navigation

All runs cold boot, without a savestate, using a byte-identical isolated copy of
the existing Syracuse save. Its source SHA256 remains
`958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.
No inventory, location, condition, unlock, outcome, code or other synthetic fixture
is applied. The donor's older historical progress is not newly earned progress.

The V611 control was navigated interactively first, then its exact full schedule
was replayed against V612 and the original Japanese ROM for 14,200 frames each.
The Common wheel rotates when changing its focused item; touching an already
focused item can activate it immediately. The first Route Map excursion and
returns remain in the recorded schedule rather than being erased as though the
initial touch selected Functions. Six UP inputs later leave the load selection
unchanged; they receive no six-slot coverage credit. The six actual slot previews
are reached by observed stylus selections at frames 11000..13000.

The sequence verifies:

- Functions > Save and its real current-game preview.
- Back, then Functions > Load.
- All six existing save-slot previews through normal stylus input.
- A Load confirmation and cancellation, followed by selection/re-entry.
- Selection of the first existing save and the ordinary Yes action.
- Actual return to Stockholm gameplay after loading. Its whole frame is exact
  to the unchanged V611 control at frame 14200. The original source/copy save
  history remains separate from new travel, acquisition or route progress.

The current and original Japanese plaques match their respective whole atlas
crops in all 18 observed active Save/Load states, including confirmation overlays.
There are 26,568 complete restoration-region pixel checks. The whole V612 pair
of screens matches an independent V611-plus-repaired-regions composition at all
32 sampled frames: 3,145,728 native5 pixel positions. All other screen pixels,
including live numerical fields, captions, portraits, selection, menus and the
loaded-game result, are retained. These are targeted emulator tests, not a complete
route playthrough or hardware verification.

## Actual resource and flag ABI

Executing the original initializer `0210FA44..0210FA68` identifies resource owner
`02312CDC` and filename `_pxl/saveloadinfo.pxl`. Source instructions are verified
exact to the clean Japanese ROM. The real active full 256x192 views are found
in each original/current snapshot, rather than supplied as hypothetical owners.
Executing the original `020D4170` getter on all 36 views returns the complete
exact named source or current PXL. No cache, getter or loaded-header bridge is
used. The current native header is at `02342FD0` in this run; addresses are
captured evidence, not permanent allocation promises.

The first verifier incorrectly required an entire zero word at view+24h. The
original constructor `020D40A0` writes a halfword, and the draw adapters
`020D3A5C/020D3C5C` read a halfword. Load mode retains a nonzero upper padding
halfword. Exact original opcodes establish the real ABI; the verifier checks the
actual 16-bit flag and records the retained padding explicitly. No ROM change or
emulator rerun was needed for this verifier correction. An optional trial to read
the unchanged tiny town title with the ordinary/compact 6x11 masks did not match;
it receives no title-font or clipping diagnosis. The actual load is supported by
observed ordinary input, visual inspection and the complete unchanged final frame.

## Registered complete integration

- Experimental candidate: `out/all_routes_combined_v612_candidate.nds`, physically
  `E:/Rota Nova translations/Generated/out/all_routes_combined_v612_candidate.nds`.
- Candidate SHA256: `06a7970275450cebbd0887777ba93df196980fe17e290ce76c142307acb22ac2`.
- Profile: `all-routes-unified-v612`.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- All 470 inherited batches, 114 accepted layers and the entire V611 profile are
  retained. Added terminal stage: `translations/save_load_plaques_v1.json`.
- Only `/_pxl/saveloadinfo.pxl` differs from V611. All code, staged pools,
  startup/cache/heap geometry, other graphics, scripts and translations are exact.
- Exact clean-ROM patch SHA256:
  `97b7985f7abd4ef478bc93469403ff356f36b7ed11bac73ae96926136c23919c`.
- Patch input: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- A separate 24,100-frame ordinary New Game/Market run has no existing save or
  synthetic fixture. All 19 sampled complete screens match V611 exactly.
- Fresh preservation retains all 660 PXL headers/indexed palette banks/extents,
  261 FLS textures and 57 embedded block extents.
- The full registered builder, manifest, independent static/native verifier,
  exact clean patch reconstruction and targeted Ruff pass.

V612 has actual native coverage for its changed Save/Load plaques, but inherits
V611's still-unverified regional-fleet artwork. V610 remains the latest verified
candidate pointer. V612 is recorded separately as the latest compiled combined
experimental work with that explicit inherited gap. No canonical promotion or
user/device acceptance is inferred.

## Artifacts, reproduction and remaining work

1. `scripts/prepare_save_load_plaques_v612.py` produces the source-framed asset,
   review sheet, source locks and full inherited profile.
2. `scripts/build_integrated_release.py --profile all-routes-unified-v612`.
3. Replay `work/analysis/save_load_plaques_v612/complete_inputs.json`, the unchanged
   named source save and exact capture frames from each report for 14,200 frames.
4. Replay the ordinary Market schedule for 24,100 frames.
5. `scripts/audit_graphics_preservation_v574.py --rom out/all_routes_combined_v612_candidate.nds
   --out work/analysis/save_load_plaques_v612/preservation_proof.json`.
6. `scripts/verify_save_load_plaques_v612.py` reproduces all named evidence.
7. `scripts/record_save_load_plaques_v612.py` archives comparisons, proofs and
   unmodified normal guide candidates on E, and records the inherited open gate.

The Golden Route material/wording findings, regional native context, original
18-plaque wider audit and all 22 historical requirements remain open with their
full scope retained. No other generated atlas is silently cleared. Village cards,
comic/legacy/movie consumers and broader gameplay gates remain. Revisit older
record-based checks at actual full graphics-goal completion.
