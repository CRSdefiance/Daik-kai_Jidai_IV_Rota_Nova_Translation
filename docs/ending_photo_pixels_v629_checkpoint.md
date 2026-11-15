# V629: original ending draw commands and complete Maria photo frames

## Progress and scope

V628 resolved the capital-I palette comparison. This checkpoint advances the
remaining ending-illustration checks: it executes the complete original draw
routine, validates its emitted GPU commands, reproduces the Maria animation
controller, and independently reconstructs two complete native photo frames.

There is no V629 playable ROM. Experimental V627 remains unchanged:
`E:/Rota Nova translations/Generated/out/all_routes_combined_v627_candidate.nds`,
SHA256 `0a03862a0a0a75c748e2f806016d2316f881eb9799907590715c41d251bf2a09`.
No artwork, translation, patch, release registry or canonical baseline changes.

## What the previous evidence established

V594 positively identified M30 texture5 and M32 texture4 with source-locked
marker controls and native geometry. Its tests stopped before the GPU-writing
part of the original quad routine. They established source use and projected
crop bounds, rather than complete picture reconstruction.

The reused V594 cold-boot runs use the disclosed one-byte ending-state fixture.
They are targeted ending tests, not earned route finishes or new V627 gameplay.
The full M30/M32 files and relevant native code remain byte-identical across
clean source, captured V593 and current V627.

## Complete original draw routine

The new verifier loads each actual captured RAM image into an isolated native
replay and executes original020FEB28 through its return at020FF9C4. It observes
the actual memory writes to the GPU registers; none of the native geometry,
selectors, arithmetic, draw calls or GPU-write instructions is stubbed.

Eleven existing photo snapshots now supply complete command streams, including
texture coordinates, texture/palette configuration, polygon color/alpha, begin,
four vertices and end. Only the controller's original polygon-ID byte changes.
The complete calls preserve their stack and saved-register ABI. Dummy mapped IO
receives these writes; it does not simulate the GPU or create screenshots.

An important distinction from the earlier geometric bounds is now explicit:
the function quantizes X by256 and Y by192 before emitting signed VTX16 values.
The native texture coordinates for M32 texture4 cover256x192, preserving its
native header height rather than the256-row backing allocation.

## Original controller continuity

Starting from actual Maria frame8320, the verifier executes1,920 original update
calls and5,760 complete original draw calls through frame10240. All6,936 bytes of
the controller match actual RAM at frames8640,8960,9280,9600,9920 and10240. The
polygon-ID byte is included. Neither geometry nor a timing offset is injected.

This checks the supplied captured-controller replay. It does not claim a trace
of the running emulator, resource loading before the initial snapshot, GPU
execution in the replay, or a complete ending-controller model beyond this span.

## Two complete native photo reconstructions

The declared simple sampling model converts the actual emitted vertices back
to screen coordinates, floors source coordinates, and converts source palette
colors to the capture's RGB565 output. It is tested against every one of49,152
pixels in each upper-screen frame, without a masked border or pixel tolerance.

Maria frames9280 and9360 both match **all49,152 RGB pixels exactly**. These are
full viewport compositions of the retained illustration, including blank areas
and the visible flowers, clothing and face. The frame9280 command coordinates
are `[0,-295],[0,4672],[4968,4672],[4968,-295]`; source texture coordinates are
`[0,0],[0,3072],[4096,3072],[4096,0]` in12.4 units. Blank-picture, one-pixel-shift
and source-texel alteration controls fail as required.

The complete native frames and independent reconstructions were visually
inspected. They do not reveal additional Japanese text. The prior decision to
retain the original contextual illustrations remains appropriate.

## Explicit model failures and next investigation

The simple model is **not accepted for the whole zoom sequence**. All24 sampled
Maria frames within the replayed interval are recorded, along with the eleven
independent original snapshots. Earlier Maria zoom states have3,167–8,066 RGB
differences in that interval. After frame9360, the simple clamped model differs
at the192 pixels of the leftmost column. The four Hodram states also do not
match this simple opaque projection; their transition/composition remains open.

Those differences are retained as failed sampling hypotheses. They do not
establish a ROM defect, justify changing the art, or receive display clearance.
The next question is the post-command viewport clipping, texture sampling and
background/alpha composition. Repeating a pre-quantization vertex calculation
or waiving a border would not resolve it.

For reference, the exact captured core identifies git95b4d79. Its published
[rasterizer source](https://github.com/libretro/desmume/blob/95b4d79/desmume/src/rasterize.cpp)
was inspected for vertex adjustment, edge coverage and texture sampling. That
source is research context, not a claim that the full rasterizer has been
ported or that it proves this independent reconstruction.

## Artifacts and retained requirements

- Verifier: `scripts/verify_ending_photo_pixels_v629.py`; targeted Ruff passes.
- Proof: `work/analysis/ending_photo_pixels_v629/native_photo_pixels_proof.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V629 Ending photo pixels`.
- The archive retains unmodified captures, separately labeled source views and
  reconstructed previews, original reports, hashes and the verifier.
- This is existing V593 capture evidence bound to unchanged V627 code/art inputs.
  No new emulator run, hardware verification or earned completion is claimed.

All18 original plaque entries remain incomplete. All22 historical requirement
objects and other audit entries retain their original scopes. Remaining comic,
legacy, village, miniature/Confirm, material, logo and movie-context checks stay
open. The four low-resolution Online exemptions and preserved brown marks remain
in force. The full graphics goal remains active and incomplete; revisit older
record-based checks at its actual completion.
