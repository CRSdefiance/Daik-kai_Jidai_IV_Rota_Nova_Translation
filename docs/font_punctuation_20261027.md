# Comma and question-mark test ROM, 2026-10-27

Experimental profile: `font-v2-punctuation-one-pixel-20261027`. User acceptance pending; promoted main remains V4701.

Candidate: `out\font_v2_punctuation_one_pixel_20261027_test.nds`  
SHA-256: `9c2494830c3a60655fb09ab5cc67842851cbdbe8609083084ec447b81b363258`  
Manifest: `out\font_v2_punctuation_one_pixel_20261027_test.manifest.json`

Rebuilt by the integrated release builder from immutable canonical base
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
The complete V4749/font stack is retained: 558 manifest entries,
including all 114 accepted layers already baked into the canonical base.

Compared with the prior Y+1 trial (`out/font_v2_draw_down_one_20261027_test.nds`,
SHA-256 `fed25c1b5c360d32164e6530ca8106d1abaf87167531c66ce2dda01328341a6f`),
only `/__arm9__.bin` changes: 7 byte values within the two owned
11-byte comma and question-mark bitmaps. All other glyphs, including improved descenders and
brackets, are identical. Every instruction, helper, advance, drawing offset and line-spacing byte
is identical to the prior Y+1 trial. Biography pitch remains12 pixels; dialogue pitch remains16.
Other files, story text, Japanese font, artwork, overlays, autoload sections and extents are unchanged.
Complete canonical-base changed paths and record IDs are listed in the neighboring manifest.

The comma now has a head at baseline row8 and a tail through rows9/10. The question mark has
an open hook, shorter stem, two blank rows before a single-pixel baseline dot. Both retain the
6-pixel advance and11-row cell. The existing Y+1 drawing position fits all12 available cell rows.

## Verification

- Integrated manifest/source/dependency locks, canonical baseline verifier and exact predecessor file comparison pass.
- 592 actual native painter cases cover both4-bit and16-bit surfaces,
  eight backing heights, all32 ASCII punctuation glyphs and g/j/p/q/y. Full available pixels and memory guards pass.
- Native footer constructor, caption rasterization and complete14-row copies pass, including comma/question-mark
  stress captions and descender tails. Allocator-return and GPU-copy boundaries are declared in the proof.
- 29 existing integrated-release/font regression tests pass.
- Three actual DeSmuME cold boots cover28403frames: Lil startup4001, Hodram7001 and town17401.
  Town uses an isolated copy of the retained battery fixture; other runs use ordinary controller inputs.
  No loaded savestate or newly injected gameplay state. Original donor save unchanged.
- The actual question mark in `Everything correct?` matches the complete revised glyph mask
  (210 ink pixels for the whole sentence), with no stray ink below.
  `Aye, aye!` matches every ink and blank pixel, including the comma's final tail row.
  `Aye!`, three Lil opening lines and three Hodram biography lines also pass complete masks and empty-row checks.
- All eight startup/town button masks remain complete and at the same Y+1 placement.
  Native stress captions preserve full punctuation/letter tails. This is targeted emulator verification,
  not a full playthrough or hardware verification.

## Other punctuation found, unchanged in this ROM

- Semicolon: tail stops at baseline; strongest candidate for a further below-baseline correction.
- Double quotation marks: connected top row makes the two strokes less distinct.
- Period/exclamation mark: dot weights/orientations differ from the revised question mark; a consistency review may help.
- Tilde: flat top bar. Check the legacy Japanese overline mapping and actual uses before changing it into a wave.
- Backslash position contains a yen-shaped glyph, consistent with legacy Japanese font conventions.
  Check currency/encoding uses before replacement. No automatic currency-symbol change was made.
- Existing completed brackets, parentheses, braces, dollar sign and underscore remain intact.

## Evidence and reproducibility

`work/font_punctuation_20261027/` contains source/registry snapshots, proposed ARM9,
native proofs, exact cold-boot plans, capture reports/hashes, complete mask results,
32-glyph audit, before/after specimens and actual paired screenshots. The patch producer is
`dk4tool/patch/ascii_punctuation_20261027.py`, locked by `translations\ascii_punctuation_20261027_v1.json`.
Build command: `python scripts/build_integrated_release.py --profile font-v2-punctuation-one-pixel-20261027 --out out\font_v2_punctuation_one_pixel_20261027_test.nds`.
Historical modules, prior test ROMs, failed experiments and main/baseline artifacts are preserved.
Candidate pinned using its resolved physical E-drive path. Retention preview is recorded separately;
no ROMs were deleted.

Retention preview result: Retention preview stopped safely on an unrelated existing C-junction-path pin for lil_opening_release_v1710/patch_reconstruction_RESEARCH_ONLY.nds; approved generated storage requires its resolved E-drive path. Existing pin left unchanged. No deletions performed.
