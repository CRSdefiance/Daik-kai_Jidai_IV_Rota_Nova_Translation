# Textured plaque restoration

Use the original Japanese ROM as the texture reference. A translated atlas is
an integration dependency, not evidence of the original background's quality.

For new or revised textured plaques:

Verify that every owned region actually contains the source text being replaced.
Do not infer caption positions from a regular row size. V568 found that the
historical marker batch treated two 12-pixel price rows as 16-pixel slots and
painted an invented Sell label over a bag illustration. Source text, illustration
boundaries and native crops are separate evidence requirements. Restore artwork
when a historical translation occupied a region with no corresponding writing.

1. Compare the original and current art at native resolution and an enlarged
   nearest-neighbor scale. Identify the original frame, visible grain, lettering,
   shadows, surrounding wallpaper, and any live fields that overlap the region.
2. Preserve original visible texture and frame pixels wherever possible. Define
   an explicit source stroke region before reconstructing concealed pixels. Do
   not erase dark bevels or wallpaper simply because they resemble text colors.
3. Reconstruct concealed texture from reviewed unlettered original pixels with
   the appropriate material and palette. Record donor bounds, any joins or
   repeated periods, remapping, and uncertainty. Reconstruction is not exact
   recovery of pixels hidden by the original lettering.
4. Avoid nearest-row fill for textured interiors. It stretches individual
   background samples into conspicuous bands and blocks. Do not reuse the old
   translated town Type plaque as a supposedly pristine donor.
5. Verify complete English glyphs independently. Keep source wallpaper pixels
   that share the ink palette index separate from the actual text band.
6. Check overlapping outer restoration rectangles. A later background pass can
   overwrite another plaque's interior rows even when every label fits.
7. Verify palettes, dimensions, original visible pixels, borders, and all unowned
   pixels. Compare the result to original source art, not only generated output.
8. Verify the actual native loading/crops and first/final letters where available.
   Register the complete integration, preserve inherited layers, and reconstruct
   its patch exactly. Keep any unverified contexts or visual defects open.
   For original software frame helpers, identify source tiles separately from
   destination rectangles. Styles can contain nine or three tiles, and a zero-size
   tiled descriptor can fill from one source pixel. Follow the verified contracts
   in `docs/frame_source_contracts_v584_checkpoint.md`; inspecting only a style's
   first tile or treating the destination as an atlas crop is insufficient.
9. Check for residual Japanese glyph-shaped texture seams after reconstruction.
   V554's per-pixel restoration passed palette, English-mask and border checks
   but exposed faint Japanese ghosts where source grain surrounded reconstructed
   stroke pixels. Reject that result. Review a contiguous reconstruction region
   or matched local texture before integrating; a dark-pixel exclusion alone is
   insufficient proof of a clean background.
10. Map original shadows and outlines independently of white glyph faces. The
    Temporary Storage banner's old white-only erasure retained 125 uncovered dark
    Japanese shadow pixels and sometimes sampled those shadows as background.
    Its original diagonal shadow uses palette indices 2/3; other assets require
    their own source mapping. Do not generalize these indices to every plaque.
    Review coherent local source patches for concealed strokes and shadows,
    preserve visible material, and verify the complete live banner after repair.

For raw/archive art, distinguish cached-file compatibility, software pixel copies
and the actual scene loader. V587 binds the event-still loader020B7158 to a
preallocated canvas: it reads the file, then rejects a format or geometry mismatch.
A substituted filename can therefore leave an unchanged scene even when the file
was read. Do not alter raw high bits or artwork to force an incompatible widget;
trace a suitable native descriptor/consumer and retain the test's explicit limits.

Historical generators and proof dependencies remain unchanged for reproduction.
Repeated source patches must also be checked at their wrap boundaries, at native
size and enlarged. V580 found that an unlettered but frame-adjacent column in a
40-column wood sample repeated as a pale vertical band on long equipment labels.
V581 moves the contiguous sample one source pixel inward, preserving the original
grain and existing period; glyph/source equality alone had not detected this.
V542-V544 add source-locked corrections after those inherited stages. Their
pixel/glyph passes do not close the global plaque audit. All 18 existing entries
remain incomplete under the user's explicit instruction.

The integrated builder also checks final plaque output after all registered
stages. Profiles carrying `local_plaque_texture` must retain both complete
reviewed atlas files, original metadata/palettes and all 17 independent English
glyph masks. Profiles carrying `equipment_grain_join` must retain the full
1408-byte hint backing tile derived from the original frame and the reviewed
40-column source wood period. The manifest records this final contract.
This protects the current reconstruction; it does not establish user acceptance
or exact recovery of concealed Japanese-source pixels. A deliberate later art
revision needs fresh source/material review and an updated registered contract.
Never regenerate a target hash merely to silence a failed material check.
