# V594: original ending-illustration usage and projected crop checks

Production remains experimental **V593**, SHA256
`d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642`.
Its ROM, patch, registry, translations and original artwork do not change.

## Gap addressed

Earlier ending checks matched whole scenes, credits, split-image pans and the
shooting star. They did not establish a complete source match for M30 texture5
(woman at a window) or M32 texture4 (seated woman with flowers). Both retained
illustrations were reviewed again at their actual header bounds. Neither contains
a readable Japanese caption or instruction; the contextual art remains original.

The original timeline scales these pictures. Treating them as an unscaled256x192
window was insufficient. This checkpoint positively identifies the actual source
texture and checks its changing native crop using paired source markers and
captured original runtime geometry. It does not invent a full photo compositor.

## Source-locked research controls

Two explicitly named `*_RESEARCH_ONLY.nds` clones derive from V593. Each changes
only its one original FLS file. Eight16x16 patterned tags use existing opaque
palette indices; only2,037 M30 or2,027 M32 source indices differ. All other decoded
texture indices, palettes, flags, dimensions, record tables, timelines, container
extents, code and internal files remain exact. The compressed edit stays inside
the original allocated pixel slot; nothing is repacked into a larger extent.

M30 texture5 has native/stored256x256 dimensions. All eight tags are inside that
header. M32 texture4 has native256x192 dimensions in256x256 storage; six tags are
inside the native header and two are in stored rows below it. These research tags
are diagnostic data, never integrated translations or guide artwork.

The opt-in ending helper admits the exact V593 ARM9 only after checking all five
original ending/captain/teardown/playback ranges against clean source, four
additional FLS update/quad/selection/upload ranges, and whole V593/V581 ARM9
continuity except15 bytes in the two documented Deck text slots. It still rejects
wrong captains and unverified ARM9 versions. No permissive fallback is added.

## Four native runs

| Captain | Actual production control | Marked counterpart | Frames each |
| --- | --- | --- | ---: |
|Hodram|V593 original M30|Only M30 texture5 tagged|14,600|
|Maria|V593 original M32|Only M32 texture4 tagged|11,200|

Each fresh DeSmuME run uses an isolated byte-exact copy of its existing donor.
At frame3000 the authorized fixture changes only temporary state022796BC from1
to4. The original ending selector requests M30/M32 for the active captain.
All four processes finalize exit0. No savestate, replacement movie slot, changed
story instruction, invented resource header or framebuffer insertion is used.
This is forced-ending test setup, not earned route completion. Underlying lower
gameplay can persist, so these composite screenshots are not normal ending-guide
evidence. No gameplay Save is accepted.

Original source saves remain:

- Hodram Athens donor: SHA256
  `83fe3317eee3bca21b70be69bf34febd12d3aea09a83e75003b1f848d5fea937`.
- Maria Nagasaki donor: SHA256
  `fbae21aa2c5a695bde0eddfc10a3bbeb80d01478bd6a9ed743d824595dc3096e`.

## Actual runtime source and geometry

The full movie file is not assumed resident. The actual original controller is
located through its retained complete FLS prefix, source table pointer and
allocation pointer. A scratch prefix with different bytes is rejected. The two
paired controllers match across every0x1B18 object byte in each checked snapshot,
including their actual frame counter, buffers, alpha and transform state.

On isolated copies of those real captures, original100390 selects the target
texture and originalFEB28 calculates its FX12 quad. No selector or geometry
argument is fabricated. Source-tag rectangles are projected through those actual
quads, clipped to the native viewport and given an explicit two-pixel raster-edge
margin. All changed pixels across the complete two-screen captures must fall
inside those independently predicted rectangles.

| Photo | Positive captured geometry states | Changed pixels checked within projected bounds | Tags positively observed |
| --- | ---: | ---: | --- |
|M30 texture5|4|5,444|0,1,2,3|
|M32 texture4|7|7,714|0,1,2,3,4,5|

Hodram's original selector input is12 for texture5; Maria's is11 for texture4.
These are observed selector results, not direct assumptions that input equals
texture index. Both examples demonstrate zoom/cropping, explaining the failed
unscaled-window model. M32's two below-header tags require no additional native
rectangles to account for any observed change. Unobserved M30 tags do not receive
display credit.

There are **331 paired native frame cases**:291 entire two-screen pairs are
identical, and40 show the marker effect. Every lower screen is exact. Eleven
explicit live-state cases independently constrain **13,158 changed native RGB
pixels**, with every other pixel in those complete frames unchanged. Matching
whole frames before/after the marker intervals provide negative controls.

This establishes these two original source consumers and their bounded native
zoom/crop behavior under the original ending path with authorized setup. It does
**not** prove a full per-texel photo/alpha compositor, exact GPU interpolation,
every intermediate frame, every source row, normal earned endings or hardware.

## Evidence and retained scope

- `scripts/prepare_ending_photo_markers_v594.py` and `fixture_manifest.json`.
- `scripts/verify_ending_photo_markers_v594.py` and
  `work/analysis/ending_photo_markers_v594/native_photo_usage_proof.json`.
- Guarded helper: `scripts/native_ending_fixture_v537.py`.
- Four raw runs under E's `Generated/work/emulation_v193/ending_photos_v594_*`.
- Source views,32 selected source/control/marker PNGs, four reports, input
  schedules and hash receipts under
  `E:/Rota Nova translations/Screenshots/Test fixtures/V594 Ending photos`.

All screenshots remain test evidence with guide/publication approval false.
V593's exact patch remains SHA256
`e6e1097e9caa7577a4c51d9bcc175274eb68e4f8041d86acd05d8ba1f4ad52c7`.
All18 original plaque/hint entries remain incomplete and all22 historical
requirement objects remain deep-identical. Other legacy/comic/village, miniature/
Confirm, material and remaining movie-context gates stay open. The graphics goal
remains active; older record-based checks remain a follow-up at full completion.
