# One-pixel font offset - experimental test ROM

`font_v2_draw_down_one_20261027_test.nds` keeps the improved letters and draws the live ASCII font one pixel
below its original drawing origin. This is one pixel higher than the previous
two-pixel-offset trial. The biography line spacing remains12 pixels. No letter
shapes, dialogue, wrapping, line-spacing instructions or other layout settings change.

Use a fresh emulator boot for testing. Your previous ROMs and promoted main are
preserved. This candidate is experimental and awaits your gameplay acceptance.

## Exact build provenance

- Candidate SHA-256: `fed25c1b5c360d32164e6530ca8106d1abaf87167531c66ce2dda01328341a6f`
- Profile: `font-v2-draw-down-one-20261027`
- Registered construction predecessor stack: `out\font_descenders_symbols_v2_20261027_test.nds`
- Predecessor SHA-256: `789cb44c05e2c3d5272f562980e641d2697df4cb9a23963327face1e9dc976c7`
- Immutable canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Canonical SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Complete V4749 plus improved-font stack and registered one-pixel guarded painter:
  557 manifest entries and all114 accepted baked layers.
- Only `/__arm9__.bin` changes from the improved-font predecessor. The integrated
  builder reconstructs the full stack from the canonical base; no revoked ROM or
  research ROM is used as a construction parent or byte source.
- Read-only comparison with the previous two-pixel trial shows exactly one changed
  ROM byte: the drawing instruction's immediate2 becomes1. Every other ROM byte,
  including the improved1045-byte font, biography settings,14-row button strip and
  lazy1792-byte button buffer, is identical. The output also exactly matches the
  previously verified one-pixel diagnostic ROM.
- Original staged pool, autoload extents, Japanese font, controller icons, artwork,
  source files, accepted status and promoted main V4701 are preserved.

## Verification

- Canonical baseline, complete registry snapshot/profile/manifest, unchanged-file
  and code ownership, helper-slot references and exact font identity pass.
-128 guarded native glyph cases across both pixel formats and tight buffer heights
  pass. Full descenders and completed brackets/symbols remain inside the tested
  drawing bounds. Four-line native dialogue retains its original16-pixel row pitch.
-29 existing integrated-release/font regression tests pass.
- Four fresh cold boots cover7001 Hodram frames,4001 Lil New Game frames,17401
  town/refit frames and32800 sailing frames. No loaded savestate or callback errors.
  The town run uses the existing isolated test battery; the other replays use
  ordinary inputs without injected gameplay state. This is targeted emulator
  evidence, not a complete route or hardware test.
- Hodram's `Everything correct?` matches all213 glyph-ink pixels and all blank
  cells; the former stray-dot rows below are clean.
- Actual `Aye!` and `Aye, aye!` replies have complete masks and no pixels below
  their glyph cells. The Lil opening's three complete lines and rows below also pass.
- All three biography lines have complete masks atY330/342/354: unchanged12-pixel
  spacing. This change intentionally does not increase the gap between those lines.
- Eight actual startup/town button masks are exactly one pixel below the original
  high-font test. Twelve sailing button masks pass, including the full `p` tail in
  `Inspect` at all three sampled frames. No tail clipping found in these samples.
- Title, selection/biography, confirmation, short replies, opening dialogue,
  town/refit and sailing screenshots were viewed. Other game screens remain for
  your gameplay testing before acceptance.

The prior two-pixel profiles remain revoked and their failures/proofs preserved.
They had passed button checks, but did not fit the original12-pixel modal glyph
cell. This candidate uses11 glyph rows plus a1-pixel offset and adds explicit
checks for stray pixels outside the normal glyph rectangle.

Evidence and previews: `work/font_offset_one_20261027/`.

Retention preview stopped safely on an existing pin outside its approved physical archive path; no ROMs were deleted. The new test is pinned. Sailing button masks use frames24000,28000,30800; the original Food has run out panel hides the footer at30000, which is excluded explicitly without changing input or capture timing.
