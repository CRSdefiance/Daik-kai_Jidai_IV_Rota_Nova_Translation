# V563–V564: cargo banner shadows and original source wood

## Corrected defect

Ordinary Port > Cargo Setup testing exposed another affected wooden graphic:
`/_pxl/tempcargo.pxl`, the full-width Temporary Storage banner. Its Japanese
source reads 一時置き場, a place to keep cargo temporarily. “Temporary Storage”
is a natural, faithful heading for this screen and remains unchanged.

The historical generator erased only white palette index15. The original image
also has 158 dark diagonal shadow points at (+1,+1), using indices2/3. In V558,
125 of these points remained uncovered by the English lettering. The erasure
also sometimes sampled those dark shadows as replacement background. The visible
black shapes were not ordinary wood grain: unlettered source rows in the reviewed
donor region contain none of indices2/3/15.

The repair maps all 216 original white points and those 158 shadow points. Each
connected component uses a coherent original wood patch from the same image,
x128–247, selected by color agreement with its visible source neighbours.
Concealed texture is inferred; it is not claimed as exact recovery. All 241
English ink pixels and 3,555 original visible material points outside the owned
strokes/shadows and English remain exact. Dimensions, palettes, borders and all
other original pixels remain exact. The corrected banner differs from V558 at
275 pixels. Visual review shows the Japanese shadow remnants removed without
the former black shapes behind the English heading.

The required texture workflow now explicitly requires mapping shadows separately
from white faces. Palette indices2/3 apply to this source; other graphics require
their own mapping. No generic palette rule was applied across unrelated assets.

## Registered combined release

- Profile: `all-routes-unified-v564`, experimental; canonical baseline unchanged.
- Base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- ROM: `out/all_routes_combined_v564_candidate.nds`, SHA256
  `cffcaa93ef99e506004760a7dbb911502bc9257d2946a48462b626d36c18b32b`.
- Patch: `out/all_routes_combined_v564_candidate.xdelta`, SHA256
  `947e35f4db3b8796669f3d9df652cde37b64675ffed74fbffb9f997ccefd6a4c`.
- Patch source: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The complete V558 profile is inherited, including all 470 batches and 114 accepted
layers. The only changed internal file relative to V558 is the banner above.
All code, other artwork and other translations are byte-identical to V558.
The manifest records the registered stage and source/config/target hashes.
Applying the patch to the exact clean ROM reconstructs the candidate byte-for-byte.

## Native and regression evidence

Two ordinary copied-save cargo states at frames4300 and4600 pass complete
98,304-pixel comparisons, including every pixel of the 256x16 banner at (0,261).
Across both frames, all 8,192 banner pixels match the corrected source, all English
letters are visible, and exactly 275 pixels per frame differ from V558. No other
screen pixel changes. The source battery save remains unchanged; no savestate,
location/inventory/condition fixture or cheat is used.

A separate 21,200-frame New Game cold boot passes all 56 unique startup captures
against V558, covering the established title, character selection, opening story
and town schedule. Ruff passes for the new module, review script, verifier and
integrated builder. This is targeted emulator evidence, not a complete route
playthrough or physical-device verification.

Evidence:

- `scripts/review_cargo_banner_v563.py`: original/current/repaired source review.
- `dk4tool/patch/cargo_banner_texture.py`: locked original stroke/shadow repair.
- `translations/cargo_banner_texture_v1.json`: source and target locks.
- `scripts/verify_cargo_banner_v564.py`: full release, font, native and patch checks.
- `work/analysis/action_consumers_v563/v564_release_proof.json`.
- `work/analysis/action_consumers_v563/temporary_storage_review.png`.
- Captures on E under `Generated/work/emulation_v193/cargo_banner_v564_actual`
  and `cargo_banner_v564_fresh`.
- Ordinary guide candidate and provenance on E under
  `Screenshots/Guide candidates/V564 Cargo Setup`; publication remains unapproved.

## Remaining native-control and plaque scope

The V563 ordinary Cargo Setup initial/selected states contain no matching 12-word
frame views whose source rectangles intersect the five remaining miniature
captions, under owner02313F60. The bounded census is preserved in
`cargo_native_census.json`; it does not prove global non-use or cover other view
layouts/owners. A provisional static constructor search also retains unresolved
dynamic coordinates and unrelated marker matches. These are research leads, not
proof that the five captions display correctly.

Done, Rank, Cancel, Pick Cargo and Pick Ship retain their complete stored masks,
but actual native consumers remain open. All 18 original plaque/hint entries
remain incomplete; all 22 historical requirements retain their original scope.
The full graphics goal remains active. This correction does not close the global
texture defect or authorize promotion of the experimental ROM.
