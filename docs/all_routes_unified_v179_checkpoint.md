# Combined V179: English closing gallery artwork

2026-10-04. **Experimental**. The all-graphics goal remains active and incomplete.

## Source-faithful translation and protection

SLACKIMG block 19, reviewed 320×240 frame 16:

| Source | Natural English | Owned rectangle |
| --- | --- | --- |
| おつかれさまでした。 | Well done! | `[101, 119, 195, 141]` |
| 大航海時代IV | Uncharted Waters IV | `[273, 172, 305, 188]` |

The closing group picture expresses warm appreciation at completion. The English
adds no story facts or relationships. The title plaque retains its original gold
border. Automatic paragraph wrapping produces the full two-line English title;
there are no runtime dialogue controls or authored alignment spaces. Original
high color bits, archive offsets/headers/allocation, unowned pixels and every
other frame/block remain exact. The original painted artwork is retained.

Review caught 13 neutral gray edge pixels connected to a nearby hand. The final
restoration protects colored art, its connected dark neutral edges and faint
antialias fringes. No English ink may overlap that protection. These exact hand
pixels have a dedicated regression. The corrected full comparison was reviewed.

## High-level complete-letter check and regression evidence

The new raw-art builder reconstructs each full English phrase from its logical
text, exact font, declared bounds and source background rule. The serialized
payload must match that raster. First/final glyph deletion fails even if the
payload checksum is recomputed. Individual nonspace glyphs must have complete,
nonempty bounds; out-of-frame/overlapping ownership and missing per-record
source/context/localization/naturalness/formatting/visual gates are rejected.

- **47 focused tests pass**, including 17 new raw-art cases and 30 existing
  atlas/button/source-mark cases. Four rehashed first/final-letter mutations,
  the 13 gray-hand pixels, original color flags, archive/frame/unowned-pixel
  preservation, font/source/payload/bounds/review guards and mixed-layer
  dependency ordering are covered.
- Final builder/module changes reproduce the **entire V178 ROM byte for byte**.
  This includes all 462 batches and terminal stages, not just the edited image.
- Saved V179 profile/manifest/registry/full stack, prior record IDs, relocations,
  golden menus and exact one-file delta pass. Old SLACKIMG atlas translations in
  blocks 12 and 20 are byte-identical to V178.
- The clean-ROM patch reconstructs V179 byte for byte. Changed code/tests pass Ruff.

This is a headerless raw storage partition, not a loose PXL. No invented PXL
header, native-size callback or supplied crop is presented as loader evidence.
The 320×240 partition is supported by complete source-word extent and coherent
full-picture review; actual native loader/geometry/alpha/crops/GPU/gameplay remain
unproved. Small-title readability still needs actual display review.

## Exact handoff

| Artifact | SHA-256 |
| --- | --- |
| Canonical `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V178 / full reproduction | `e03c0c0aee3787ff0b0813e270faadd3c7fdb6fc5ac7d62582b3fdb5e4b0778d` |
| `out/all_routes_combined_v179_candidate.nds` | `9187eae3b0fe2c0187d84d678611ae03014244a0f0ed9f22c2b4a6a3b13f76ad` |
| ARM9, unchanged | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry | `339e44f28790e195f6f1c1457995e2903d4dda14b30d3f3c027bdf617ab280ad` |
| Builder | `d58a3d5816f6cadea3982aeac86647057f3a724d3f99c7d3e8e7a925d6891e29` |
| Raw-art module | `e5b8a1271fb1c2a775ee1b3a46d9c3c5a42f685cb72378d680f643d4e118ef0e` |
| `out/all_routes_combined_v179_candidate.xdelta`, 833415 bytes | `3e9d2e00797c33e6575ea8d751d0f5376591eb691ed542907b33259ce575a975` |

Profile **all-routes-unified-v179**: all **462** V178 experimental batches and
terminal stages unchanged, plus `translations/gallery_closing_raw_art_v1.json`:
**463 experimental batches**. All accepted layers remain baked into the immutable
canonical base; zero additional accepted batches applied. Adjacent manifest:
`out/all_routes_combined_v179_candidate.manifest.json`. Only **`/GRP/SLACKIMG.DK4`**
differs from V178, within the two reviewed frame-16 text regions. The same 34
canonical changed paths remain listed in the manifest and saved proof.

Evidence: `work/analysis/gallery_closing_v179_saved_proof.json`,
`work/analysis/v178_raw_art_builder_reproduction.json`/`.nds`/`.log`,
`work/qa/gallery_closing_v179/evidence.json`, `review.png`,
`work/analysis/v179_graphics_tests.log`, `v179_build.log`;
`dk4tool/graphics/raw_bgr555_art.py`, `scripts/closing_gallery_v179.py` and
`tests/test_raw_gallery_closing_art.py`.

## Remaining scope and human testing

Two small painted corner marks in frames 18/19 retain their original creator
attribution styling, consistent with the neighboring M. Uno/momoko/Yura signed
paintings. Exact name/identity is not inferred from unclear kana. Their original
bytes remain exact in V179; decisions are in
`translations/gallery_creator_mark_decisions_v179.json`. Native usage is open.

Of the 12 newly discovered text-bearing block-19 images, frame 16 has complete
English and frames 18/19 have explicit retain decisions. **Nine caption/dialogue/
credit images remain**: 4/5/6/7/8/10/11/12/13. Four historical Online files still
remain: Online24/27/31/33, including Online27 chat/status. Other embedded raw
formats, broader full-resolution/source review, opening Latin names, image207
mark interpretation, earlier title scenery/native gates and full gameplay remain.
Unclassified-block counts are unchanged; no archive-wide clearance is claimed.

Cold boot without savestates: opening, title/menu, New Game, captain/name entry,
established story, town UI and inherited repaired screens. Inspect this gallery
closing image if reachable: complete phrase/title, original hands/portraits/gold
border, readability, size, color/alpha, navigation and input. Actual consumer
mapping is still required; reachability is not assumed. Review prior title scenes,
Online27 and image207 as documented in [V178](all_routes_unified_v178_checkpoint.md).
No human acceptance, including V175, has been assumed. Repository rules require
explicit human cold-boot acceptance before canonical promotion. Keep the note to
revisit older record-based checks when the **full project goal** is complete.
