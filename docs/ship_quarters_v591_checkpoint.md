# V590-V591: ordinary sailing inspection and consistent Quarters label

## Finding and source decision

An ordinary V581 cold boot, loading a copied unchanged Syracuse save, reaches
Sail > Y Inspect > select the fleet > ship selection. For the same Vestaros
brigantine, Ship Info displays **Marines 1** and Assign Sailors displays
**Quarters 1**. Complete native digit masks verify the value in both screens.
There is no inventory, location, condition, unlock or other RAM fixture.

The original ship plaque reads **海兵詰所**, the same label already reviewed as
Quarters in Assign Sailors. It denotes the number of marine quarters, not the
number of marines. Ship Info now uses **Quarters** for consistent, faithful
English. The original-source crop in the V556 comparison sheet was reviewed;
this is not a wording decision made only from the old English label.

The inspection screen did not expose the inherited `%s Admiral` heading. That
format is not changed or credited as context-verified. The five miniature
caption parents and Confirm parent also remain open. The investigation shifted
to a concrete observed terminology defect rather than repeating earlier direct
frame-owner searches.

## Exact graphical change

Only `/_pxl/shipinfo.pxl` changes from V581. The old Marines glyphs are removed
using the exact reviewed V557 source-grain recipe; the whole existing 63x16 face
must first match that recipe plus its old 94-point glyph mask. Quarters uses the
original game font at five-pixel advance, without resizing or missing strokes.

- Exactly **144 pixel indices** change, all in the old/new lettering masks.
- The complete new word has **100 ink points**, bounds `[16,105,55,114]`.
- Every nonlettered background pixel, outer frame, palette, header, dimension,
  other plaque, unrelated file, route, ARM9/ARM7 and overlay remains exact.
- The wording change does not flatten, tile again or repaint the plaque face.
- Concealed texture was already reconstructed in V557. Matching its original
  source-grain recipe does not claim recovery of hidden original Japanese pixels.

The new registered terminal stage is `ship_quarters_label`, with config
`translations/ship_quarters_label_v1.json` and module
`dk4tool/patch/ship_quarters_label.py`. Existing accepted batches are unchanged.

## Registered combined build

- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Immediate comparison parent: `out/all_routes_combined_v581_candidate.nds`, SHA256
  `542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68`.
- Experimental candidate: `out/all_routes_combined_v591_candidate.nds`, SHA256
  `7f2d10824e18d276adb23b01be48dac2d27adc2c4ec8ec16bb39a93a90dc3d73`.
- Profile: `all-routes-unified-v591`; all **470 batches and 114 accepted layers**
  are inherited. The canonical parent is not promoted.
- Manifest: `out/all_routes_combined_v591_candidate.manifest.json`.
- Patch: `out/all_routes_combined_v591_candidate.xdelta`, SHA256
  `ec2c735d82b3d7a2692f5b361b6f00fef589c9d2aa30cce629ba9716b5b27989`.
- Patch input: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The ROM, manifest and patch physically reside under
`E:/Rota Nova translations/Generated/out/`. The registered integrated builder
rebuilds from the canonical base; it does not use an isolated route or research
clone. The patch reconstructs the exact entire candidate from the exact clean ROM.

## Ordinary native verification

Matched V581 control and V591 actual runs both finish 5,840 frames with exit0,
the same 29 scheduled ordinary inputs, same core options and byte-exact copied
save. The source save remains SHA256
`958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.
No gameplay save acceptance is performed.

Twelve complete paired captures check **1,179,648 two-screen pixel positions**.
The three Ship Info frames at5320/5340/5360 differ at exactly the expected144
lettering positions each. Every other pixel and all nine other startup/menu/
sailing/Back/Assign Sailors frames are exact. All three complete 1,008-pixel
plaque faces and the whole 100-point word match the source independently.
First-Q and last-s erasure controls are rejected by the complete mask check.

Actual captured original view0218A4D0 has owner02313C90, source `[0,0,256,192]`
and filename `_pxl/shipinfo.pxl`. The complete original020D4170 resolver returns
resident02351210 with every byte equal to the candidate resource. No filesystem
bridge or supplied header is used. The face appears at its native source
coordinates: an initial guessed Y-24 projection failed111/1008 and was rejected;
the actual zero-offset comparison matches1008/1008. No failed projection points
are excluded from the final test.

The two final ordinary screens were visually reviewed at native resolution.
Guide candidates are unmodified PNGs with ROM/report/input/save provenance and
publication approval false. Older control screenshots retain their diagnostic
labels, not final guide status.

## Evidence and remaining work

- `scripts/prepare_ship_quarters_v591.py`.
- `scripts/verify_ship_quarters_v591.py` and
  `work/analysis/ship_quarters_v591/release_proof.json`.
- `scripts/record_ship_quarters_v591.py`, chained preservation proof and archive
  receipts in the same analysis directory.
- Ordinary discovery run: E under `Generated/work/emulation_v193/menu_context_v590`.
- Matched control/actual: E under `Generated/work/emulation_v193/ship_quarters_v591_*`.
- Final screenshots: `Screenshots/Guide candidates/V591 Quarters` on E.
- Source/control comparisons: `Screenshots/Audit comparisons/V591 Quarters` on E.

The existing921-entry format/palette/extent proof carries forward through exact
file equality except the one checked ship atlas. All57 embedded blocks remain
exact to V581. All18 original plaque/hint entries remain incomplete, and all22
historical requirement objects remain deep-identical. The global material review,
other terminology contexts (including gun-platform wording), miniature/Confirm,
legacy/comic/village and remaining movie gates stay open. These targeted emulator
tests are not a full-route or hardware playthrough. The graphics goal remains
active; older record-based checks remain a follow-up at its full completion.
