# All approved punctuation test ROM, 2026-10-27

> Revoked after the user's Lisbon Square freeze: the inherited one-pixel font helper overlaps Square bitmap scratch. Use the [separate repaired test candidate](lisbon_square_freeze_20261027.md). The original ROM and all historical proof below are preserved; those earlier targeted tests did not cover Square entry.

Candidate: `out\font_v2_all_punctuation_one_pixel_20261027_test.nds`  
SHA-256: `fbbd68ee7d1af28ec4656262e53836c52b502c3c2cd0a3dbeddd2646e98342fe`  
Manifest: `out\font_v2_all_punctuation_one_pixel_20261027_test.manifest.json`  
Experimental profile: `font-v2-all-punctuation-one-pixel-20261027`. Design approval is recorded by the user's request to apply all five
previewed revisions; no promotion of this playable candidate is inferred. Main remains V4701.

## Exact change and continuity

Built with the integrated release builder from immutable canonical base
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Complete V4749/font stack retained: 559 manifest entries and all
114 accepted layers already baked into that base.

Relative to `out/font_v2_punctuation_one_pixel_20261027_test.nds`, SHA-256
`9c2494830c3a60655fb09ab5cc67842851cbdbe8609083084ec447b81b363258`, only `/__arm9__.bin` changes:
16 byte values within five owned11-byte glyph bitmaps. Every other
glyph (including improved letters, comma, question mark and completed brackets), every code byte,
all other files, story text, Japanese font, artwork, overlays and autoload sections/extents are identical.
Canonical-base changed paths and record IDs are in the neighboring manifest.

- Semicolon: single upper dot and full comma tail through raw row10.
- Double quotation marks: two separate curved strokes, matching the approved preview.
- Period: a single baseline dot.
- Exclamation mark: shorter stem and dot/gap matching the revised question mark.
- Tilde: the approved wavy shape replaces the former flat bar. Encoded text and the yen-shaped
  backslash glyph are unchanged.

All five match the exact previously shown designs. Character advance remains6 pixels; bitmap
height remains11; native drawing offset remainsY+1. Biography pitch remains12 and dialogue pitch16.
The quote can use an additional ink column inside its existing cell; following letters do not move.

## Verification

- Integrated manifest/dependency/source locks, baseline verifier and complete predecessor file comparison pass.
- Only the five owned glyph spans change; all executable code and layout bytes are identical to the prior test.
- 592 actual native painter cases pass: both4-bit/16-bit modes, eight backing heights,
  all32 ASCII punctuation glyphs and g/j/p/q/y. Every available ink/blank pixel and memory guard matches.
- Native four-line sample includes all five revisions. Before/after painter events are identical for every
  glyph, proving quoted text and all following characters keep their x/y positions. Row pitch remains16.
- Native footer construction, rasterization and14-row copy checks pass for original captions and constructed
  stress captions containing all five new glyphs plus comma/question mark and descenders. Native allocator
  returns and final GPU copies are explicit test boundaries; actual button composition is checked separately.
- 29 existing integrated-release/font tests pass; retained log `regression_tests.log`.
- Three actual DeSmuME cold boots cover28403frames: New Game4001, Hodram7001 and town17401.
  Town uses an isolated copy of a retained battery fixture; others ordinary inputs. No loaded savestate or
  newly injected gameplay state. Original donor save preserved.
- Actual `Everything correct?`, `Warn them.`, `Aye!`, `Aye, aye!` and three Lil opening lines match complete glyph masks,
  including revised period/exclamation pixels and comma tails, with clean rows below. Three Hodram biography
  masks retain12pixel pitch. All eight startup/town button masks pass at the unchangedY+1 position.
- Semicolon, quotation marks and tilde are exercised in controlled native raster/footer checks, not a newly
  discovered ordinary gameplay occurrence. This is targeted emulator verification, not a full playthrough
  or hardware verification. Sheets and visual review are recorded separately under the evidence root.

## Evidence and reproduction

Evidence: `work/font_punctuation_all_20261027/`: registry before/after snapshots, proposed ARM9,
native pixel/guard/cursor proofs, cold-boot input plans, capture reports and hashes, full pixel masks,
regression log, applied font specimen and paired actual dialogue captures.
Patch: `dk4tool/patch/ascii_punctuation_all_20261027.py`. Locked config: `translations\ascii_punctuation_all_20261027_v1.json`.
The reviewed preview producer is also dependency-locked; the final extracted ROM glyphs are checked against it.

Build: `python scripts/build_integrated_release.py --profile font-v2-all-punctuation-one-pixel-20261027 --out out\font_v2_all_punctuation_one_pixel_20261027_test.nds`.
Previous ROMs, historical producers, failed experiments, main and canonical base are preserved.
Candidate pinned by its resolved physical E-drive path. Retention-preview result is recorded separately;
no ROMs are deleted by this handoff.

Visual review completed for the applied specimen, paired dialogue, startup/town and native footer sheets.
Retention preview: Retention preview stopped safely on the unrelated existing C-junction-path pin for lil_opening_release_v1710/patch_reconstruction_RESEARCH_ONLY.nds. Existing pin left unchanged. No deletions performed.
