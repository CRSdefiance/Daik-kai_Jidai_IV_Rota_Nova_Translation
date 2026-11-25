# Hodram ending pan: original tile order and star-field usage V597

This checkpoint resolves the V578/V583 pan-order ambiguity and verifies the third
tile's actual use during the subsequent movement/zoom. Production stays V593.

## Original artwork and observed path

Two fresh14,600-frame cold boots use the original unmodified Hodram donor copy,
the established inputs and the authorized one-byte ending-state fixture at3000.
Both emulator processes exit successfully. This is targeted native ending
evidence, not earned route completion. The lower screen retains the underlying
Charles dialogue in these fixtures; it is not a normal ending composition.

The original M30 movie remains byte-identical to clean. Texture3 is a256x128
star-field painting without a readable Japanese caption, reviewed at full size.
It is retained unchanged in production. All three pan textures retain their
original palettes, dimensions and records.

The earlier opaque captures matched two possible whole-canvas permutations
because they showed tiles2/1 while tile3 remained above the viewport. Fifteen
actual captured controller states now execute the original selector and quad
code. Fourteen contain the three active pan tiles; their top-to-bottom order is
unambiguously **3,2,1**. The source3 quad has the original small fractional offset,
so it is not silently snapped to an ideal stitched-canvas grid. Adjacent edges
remain within the declared2-pixel comparison tolerance.

All836 complete opaque upper-screen frames match windows of the independently
assembled source3/2/1 canvas. Their origins run192 down to129. Later states show
tile3 entering the viewport: its bottom reachesY2.7 at12960, Y122.1 at13200 and
Y153.23 during the zoom at13360. It is inactive by13440. The star-field tile is
therefore not classified as unused or permanently outside the screen.

## Positive source-tag control

A clearly labeled research clone changes only2,048 indices in eight16x16 tags
within texture3. The existing opaque palette supplies the markers. All headers,
palettes, records, extents, timeline, other textures, ARM9 and other ROM files
remain exact. The movie fits the original slot. This clone is not a playable
candidate or release handoff.

All15 original controller objects match their control objects byte for byte at
the same frame. There is no phase offset in this test; Lil V596's offset is not
assumed to apply. The original selector and geometry independently project each
source tag into the viewport with the explicit2-pixel raster margin used by V594.

Eight captured states show11,981 changed native RGB pixels, all inside those
projected tag regions. Every other pixel of those entire two-screen frames is
exact. Across those states all eight source tags become visible, including the
top tag during the transition. Seven other captured states have no tag effect.
Across all1,467 selected frame pairs,1,022 whole pairs remain identical and all
lower screens remain identical. The remaining445 full pairs contain changes;
the per-pixel projection claim is limited to the15 actual RAM-bound cases.

An initial verification assumption that the entire linear decoded tile must
remain in main RAM was rejected: neither original nor marked32,768-byte sequence
is found in those captured main-RAM buffers. That fact is retained. No temporary
buffer lifetime, VRAM layout or complete decoded-CPU-copy claim is substituted
for the positive GPU marker evidence.

## Preservation and remaining scope

The source order and actual third-tile transition use are now bound. This does
not prove every source texel, every intervening alpha operation, all ending
movies, earned completion or physical-device behavior. Other graphics-consumer,
material and final acceptance gates remain open. All18 original plaque/hint
entries remain incomplete and all22 historical objects retain their exact scope.

The proof is `work/analysis/hodram_pan_tags_v597/pan_tags_proof.json`. Reports and
raw captures are under E:/Rota Nova translations/Generated/work/emulation_v193/
ending_pan_v597_hodram*. Full unmodified test screenshots, the original source
extraction, scripts and provenance are under Screenshots/Test fixtures/
V597 Hodram pan tiles on E. No guide/publication credit is claimed.

V593 ROM SHA256 remains
`d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642`;
its exact patch and canonical baseline remain unchanged.
