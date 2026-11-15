# V631: Hodram photo timing and complete translucent composition

## Result

The four Hodram photo findings retained in V630 are resolved for the sampled
states. Nine opaque and three translucent upper-screen compositions match every
one of 49,152 RGB pixels. No border is masked, no color tolerance is used, and no
artwork or ROM change is required.

V630 made progress by verifying Maria's sampled zoom. This checkpoint addresses
the distinct Hodram failures; it does not redefine the full graphics goal around
these movies. Wider movie, legacy, village, miniature/Confirm, material and plaque
requirements remain open.

## One new targeted cold boot

The current experimental V627 ROM cold boots using the verified Hodram donor
and V594 input schedule. The authorized original ending-state fixture changes
only one byte at frame 3000. The original captain selector chooses M30. No movie
is substituted, no savestate is loaded, and no ending is claimed as earned.

The run stops normally at frame 14080. Read-only GPU/RAM exports cover five
consecutive frames around each earlier failure:

- 13358..13362
- 13518..13522
- 13758..13762
- 13998..14002

All 20 exports match their recorded hashes and same-frame direct main RAM.
Export leaves RAM unchanged. Original donor, clean-source M30 file, original
ending/draw/update/math code, current ROM and existing patch remain unchanged.

Run: `E:/Rota Nova translations/Generated/work/emulation_v193/ending_gpu_v631_hodram_adjacent`.

## Submission geometry and displayed image are different stages

The pinned core's `gfx3d_doFlush` latches the completed geometry for rendering,
then switches to a different list for subsequent submissions. Its state writer
serializes that currently building list, while the saved GPU color buffer and
video callback represent rendering output. These are not automatically the
same animation state.

The adjacent captures establish an observed **two-frame submission-to-display
delay** in this test. For each of the three opaque windows, source geometry at
anchor−2, anchor−1 and anchor reproduces display atanchor, anchor+1 and anchor+2.
The same fixed relationship also reproduces all three translucent frames.

Offsets 0, 1 and 3 are tested across every overlapping available frame and each
fails. Offset 2 passes all available pairs. There is no per-screenshot best-match
choice, modified timing, or shifted output image. The earlier matrix of failed
same-frame comparisons is retained. This establishes the relationship in this
run and core; it is not a universal DS hardware latency claim.

Primary source: pinned
[list swapping and serialization](https://github.com/libretro/desmume/blob/95b4d79/desmume/src/gfx3d.cpp),
functions `twiddleLists`, `gfx3d_doFlush`, `gfx3d_VBlankEndSignal` and
`gfx3d_savestate`. The source explains the distinct stages; the adjacent-frame
observations establish the measured delay.

## Opaque photo: nine complete frames

The unchanged V630 source sampler now matches full native RGB at13520..13522,
13760..13762 and14000..14002 using the observed fixed stage relationship.
The newer bounded compositor independently produces the same complete frames.
This closes the6,810/9,947/18,103 earlier same-frame model differences without
changing, erasing or recoloring any source pixels.

## Translucent photo, scenery and star: three complete frames

The source model uses the original M30 tiles, photo and shooting-star texture,
their actual texture-coordinate and viewport geometry, and source palettes.
The underlying star-field tiles retain their slight original overlap. The photo
is a single translucent layer over opaque scenery; this is a bounded model for
these constant-depth, axis-aligned, flat-white-lit polygons.

It reproduces the renderer's original six-bit palette and alpha arithmetic:

- Five-bit palette component0 maps to0; each nonzero componentc maps to2c+1.
- For photo alphaa, the channel result is
  `((a+1)*source + (31-a)*destination) >> 5`.
- The transparent-zero shooting-star texels are skipped. Opaque star strokes
  remain at their actual closer depth. Source colors then pass through the
  same five-bit display and RGB565 expansion used in the captures.

Full RGB frames13360/13361 match source alpha8. Frame13362 matches alpha10.
Their complete star contributions contain46,46 and19 visible source points
respectively, including the clipped exit. No source stroke is invented outside
the viewport. Every background, blended picture and star pixel is included.

For every verified frame, changing an unoccluded source photo texel, shifting
the photo one screen pixel, or replacing the picture with blank output fails.
For each translucent frame, removing the star, removing the underlying scenery,
or using opaque photo alpha also fails. The actual and reconstructed frames
were visually inspected. There is no additional Japanese caption in these
retained contextual illustrations.

Primary implementation references are the pinned
[alpha blend and rasterizer](https://github.com/libretro/desmume/blob/95b4d79/desmume/src/rasterize.cpp)
and
[palette conversion](https://github.com/libretro/desmume/blob/95b4d79/desmume/src/utils/colorspacehandler/colorspacehandler.cpp).
This is not a complete GPU emulator, arbitrary depth-order proof, every-frame
movie verification, earned route finish or hardware test.

## Artifacts and preservation

- Sampler/compositor: `scripts/research_ending_blend_v631.py`.
- Verifier: `scripts/verify_ending_composition_v631.py`; targeted Ruff passes.
- Proof: `work/analysis/ending_gpu_v631/native_composition_proof.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V631 Hodram composition`.
- Raw run retains the exact inputs, source-save identity, navigation journal,
  twenty unmodified GPU exports, RAM and screenshots on E.

Reproduce with current V627, V594's `hodram_inputs.json`, verified
`hodram-ending-test-only.dsv`, `--frames 14080 --pause-at 3000`, the20 specified
`--capture-gpu-state-at` frames, RAM export flags and `--allow-ending-fixtures`.
At the pause send `{"ending_captain":1,"until":14080}`, then normal
`{"stop":true}` at the end. Run the verifier with `PYTHONPATH=.;.deps`.

No V631 playable ROM is created. Latest compiled experimental V627 remains
SHA256 `0a03862a0a0a75c748e2f806016d2316f881eb9799907590715c41d251bf2a09`.
Its exact patch remains SHA256
`fb4b3acb17f69174a53759c8ab74053737eade38c11d5cdee6c7d0afe3062966`.
The canonical baseline, registry, all previous proofs and release pointers are
retained. All18 original plaques remain incomplete and all22 historical objects
retain their original scopes. Online low-resolution body exemptions and original
brown-mark retention remain. The full graphics goal remains active; revisit older
record checks at its actual completion.
