# Improved font with drawing position lowered two pixels - test ROM

Candidate: `font_v2_draw_down_two_v2_20261027_test.nds`. Experimental; user gameplay acceptance is pending.
Load this ROM with a fresh emulator boot. The previous font test and promoted
main are preserved for rollback. No existing save, source ROM or release is replaced.

The improved font pixels are unchanged. The common ASCII painter now draws them
two pixels lower in both4-bit and16-bit formats. Character advance, wrapping,
line spacing, dialogue, Japanese glyphs, controller icons and baked artwork retain
their existing data and behavior. Some baked artwork does not use this live font.

Button captions use a14-row text strip rather than12 rows. Their original visible
frame and horizontal placement remain intact: text copies occupy screen rows178
through191. A single zeroed1792-byte buffer is allocated through the original native
allocator at the first nonempty footer draw and reused for later labels. The old
1536-byte DTCM scratch and neighboring SDK data are not enlarged or overwritten.
The common painter limits writes to the actual backing image height. Tight text
surfaces can still crop at their own existing boundaries; no claim is made that
every compact field in the game was visually tested.

## Provenance

- ROM SHA-256: `0202eff66c9df96cfce2f2e60d243a1954f7bfcc74441100f25db529b68f2df1`
- Profile: `font-v2-draw-down-two-v2-20261027`
- Exact predecessor: `out\font_descenders_symbols_v2_20261027_test.nds`
- Predecessor SHA-256: `789cb44c05e2c3d5272f562980e641d2697df4cb9a23963327face1e9dc976c7`
- Immutable construction base: `out/raphael_natural_v2_accepted_base.nds`
- Construction-base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Only `/__arm9__.bin` differs from the previous font test: seven source-locked
  instructions and a256-byte previously blank reserved helper slot. The improved
  1045-byte font table itself is identical. All other internal files/components,
  staged payload, DTCM initialization data, autoload extents and artwork are exact.
- Complete V4749 plus prior font test plus this registered offset layer:
  557 manifest entries and all114 accepted baked layers.
- Promoted main remains V4701. Canonical baseline and accepted-layer status unchanged.

## Verification

- Exact predecessor, candidate, frozen registry, profile, complete manifest,
  baseline and unchanged-file/code ownership checks pass. No original absolute
  word or ARM branch references point into the declared helper slot across
  6 loaded ARM9/overlay units.
- Four-line native dialogue matches independent pixels withY+2 and unchanged
  16-pixel row spacing.128 guarded glyph tests cover both pixel formats and
  backing heights0,2,10,11,12,13,14,16, including all five descenders and symbols.
- Original footer initializer, view constructor, placement, complete label
  raster and copy rectangles execute. Independent full pixel planes include
  `g j p q y` and `[gyp]`; their last row fits. The native allocator return and
  final GPU copy are explicit offline test boundaries, separately covered by
  actual cold-boot gameplay.
- Existing integrated-release/font tests:29 passed.
- Actual cold boots:4001 New Game frames,17401 town/refit frames and32800 sailing
  frames (54202 total). No loaded savestate or callback errors. The town
  run uses the existing isolated battery fixture; the others use ordinary inputs
  without injected gameplay state. These are targeted emulator checks, not a
  complete route or hardware verification.
- Eight complete actual button masks (Back,Select,Finish,Undo,Edit across sampled
  states) are exactly two pixels lower with unchangedX. Twelve sailing button
  masks pass, including the full `p` descender in `Inspect` at all three sampled
  frames. All font ink and blank cells match the actual screenshots.
- Viewed title, captain selection, opening dialogue, town/refit and sailing
  screens, button comparison and native descender sheet. No blocking clipping
  found in those samples. The later original Food-has-run-out popup is normal
  replay gameplay and is not counted as footer coverage.

## Preserved failed experiment

`font_v2_draw_down_two_20261027_test.nds` and profile
`font-v2-draw-down-two-20261027` are revoked: allocating during the static footer
constructor caused a white startup/entry into original exception handling before
the logo. Its ROM, config, producers, native passes and read-only CPU failure
snapshot remain preserved. Valid video callbacks alone did not prove startup.
The successor defers allocation until a nonempty footer label is drawn. Both
early startup and actual complete button masks now pass. The small disposable
startup probe is research-only and is not the handoff ROM.

Evidence: `work/font_offset_test_20261027_v2/`.
Please check other short button captions, brackets, nameplates and multiline
dialogue during play before accepting this experiment as the main build.

Retention preview stopped safely on an existing workspace-junction pin outside its approved physical archive path. No ROMs were deleted; the new test, rollback comparator and failed experiment are pinned.
