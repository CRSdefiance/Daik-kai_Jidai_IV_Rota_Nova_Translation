# V630: complete Maria ending zoom and source renderer edge rules

## Result

The Maria photo sampling/edge discrepancies retained in V629 are resolved for
the entire sampled interval. Seven fresh V627 GPU-state checkpoints and all24
existing V593 sequence captures match independently reconstructed source pixels.
Every comparison covers all49,152 upper-screen RGB pixels, with no masked edge,
color tolerance, temporal offset or best-match search.

There are31 complete plane comparisons across two ROM versions/runs, not31
distinct animation timestamps. The seven new snapshots include25 unique sampled
timestamps when combined with the earlier sequence. These checks do not establish
every intermediate frame, all movie compositions or hardware behavior.

No ROM or artwork correction is needed. The latest compiled candidate remains
experimental V627, profile `all-routes-unified-v627`:

- ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v627_candidate.nds`
- SHA256: `0a03862a0a0a75c748e2f806016d2316f881eb9799907590715c41d251bf2a09`
- Existing patch SHA256: `fb4b3acb17f69174a53759c8ab74053737eade38c11d5cdee6c7d0afe3062966`

## Why the former model failed

The exact core's source explains three omitted operations:

1. The polygon is clipped against the six homogeneous planes before sampling.
   The clipped vertices carry newly interpolated source texture coordinates.
2. `performCoordAdjustment` calls `iround`, whose source implementation actually
   casts to integer. This truncates the coordinate to1/16 pixel; it does not round
   to the nearest1/16 pixel.
3. The edge and scanline interpolants determine the first source coordinate and
   subsequent float32 steps. Directly dividing an unclipped source rectangle by
   its screen width does not reproduce those steps.

The new bounded sampler implements those operations for these axis-aligned,
opaque, constant-w pictures. It retains the original source palette, texture
indices and viewport. The original black background and geometric coverage
predict the late leftmost black column; none of its192 pixels is waived.

Pinned primary sources:
[renderer](https://github.com/libretro/desmume/blob/95b4d79/desmume/src/rasterize.cpp),
[clipping and serialization](https://github.com/libretro/desmume/blob/95b4d79/desmume/src/gfx3d.cpp).
The downloaded source retains its license. This is a scoped sampler, not a port
or independent verification of the complete DS GPU.

## Fresh actual V627 tests

Two targeted DeSmuME cold boots use the previously authorized ending-state
fixture. Atframe3000, the original gameplay-state field changes from1 to4;
the original selector chooses the actual active captain's movie. Original donor
saves retain their source hashes. No savestate is loaded or movie substituted.

| Captain | Terminal frame | Read-only GPU export checkpoints |
|---|---:|---|
| Maria |10400|8320,8640,8960,9280,9360,9600,10240|
| Hodram |14400|13360,13520,13760,14000|

Both emulator sessions stopped normally. An initial Hodram launch named a
nonexistent donor and failed before any emulated frame; it receives no display
credit. The successful run uses the verified `hodram-ending-test-only.dsv`.

`--capture-gpu-state-at` is a new opt-in read-only frontend diagnostic. It
serializes and inspects the core state, verifies the same-frame4MiB RAM against
the direct API, and verifies that export did not change RAM. No serialized state
is loaded. It saves GPU matrices, the tagged GPU chunk, geometry and the GPU's
own RGBA output separately from the screenshots. Default frontend behavior and
the older CPU/TCM exporter are retained.

The positive fixture and wrong-version/captain/RAM guards pass. All five original
ending ranges, full native draw/update/selection/math ranges and complete M30/M32
files match clean source. The V627 fixture accepts only its exact pinned ARM9 hash;
no permissive version fallback is added.

## Complete photo proof

The seven fresh Maria checkpoints independently provide the actual transformed
polygon, viewport, opaque alpha, flat white vertex colors and clamp texture
parameters. All four matrices remain identical across those checkpoints. The
source coordinate extent is256x192, preserving its actual header instead of
the256-row backing allocation. All seven final RGB planes match exactly.

The emitted native vertices from V629's controller replay reproduce the new
serialized geometry at their shared checkpoints. The same fixed source matrices
and sampler then match all24 earlier captures at frames8400..10240, every80
frames, with zero remaining RGB differences. Historical V629 proofs remain
unchanged; this later proof resolves their explicitly retained Maria failures.

For every complete comparison, a changed sampled source texel, a blank picture
and a one-pixel geometry shift are rejected. No screen color or geometry is fitted
to the actual screenshot. The GPU's saved color output is diagnostic provenance,
not the expected image used by the source reconstruction. Full source/replayed
views and native captures were visually inspected; no Japanese caption is found.

## Hodram remains separate

The four new Hodram exports positively identify the original photo polygon.
Frame13360 has alpha10 and overlaps other original polygons. At13520/13760/14000,
the opaque sampler still has6,810/9,947/18,103 RGB differences respectively. Those
results are retained without tolerance or defect claims. Its frame binding,
sampling and composition remain to be resolved; Maria's result is not generalized
to this different transition. In particular, the serialized geometry list and
the already rendered GPU output must not be assumed to represent the same stage
without checking the original submission/render timing.

## Artifacts and remaining scope

- Exporter: `scripts/inspect_desmume_gpu_v630.py`.
- Sampler: `scripts/research_photo_sampler_v630.py`.
- Verifier: `scripts/verify_ending_gpu_v630.py`; targeted Ruff checks pass.
- Proof: `work/analysis/ending_gpu_state_v630/native_gpu_photo_proof.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V630 Ending GPU pixels`.
- Full runs: E's `Generated/work/emulation_v193/ending_gpu_v630_maria` and
  `ending_gpu_v630_hodram_actual`, with original reports and GPU exports.

Run the verifier with `PYTHONPATH=.;.deps` and `C:/Python314/python.exe`. The capture
reports retain the exact schedules, donor identities and requested export frames.
Both runs use `headless_desmume_v193.py`, current V627, `--pause-at3000` (as the
two separate arguments `--pause-at 3000`), and `--allow-ending-fixtures`; at the
pause request `ending_captain:3` or1 with the corresponding terminal `until`,
then normal `stop:true`. These are test-fixture screenshots, not earned endings
or approved guide publication.

All18 plaques remain incomplete. All22 historical requirement objects, other
audit entries and release pointers remain exact. The wider comic/legacy, village,
miniature/Confirm, logo, material and movie requirements remain open. The four
low-resolution Online exemptions and preserved brown marks remain in force.
The full graphics goal remains active; revisit older record checks at its actual
completion. No canonical promotion is claimed.
