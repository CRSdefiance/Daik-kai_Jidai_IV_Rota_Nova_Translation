# Combined V182: complete chase dialogue

2026-10-04. **Experimental**. Graphics goal remains active/incomplete.

## Source-faithful English

| Source | English | Font size |
| --- | --- | --- |
| おいらは立派な闘牛士になるんだ～～ | I'm gonna be a great bullfighter! | 9px |
| 海に出ようっていってんだろー！ | I said, let's go to sea! | 9px |
| ヤダー | No way! | 14px |
| まちやがれ コラー | Hey! Get back here! | 9px |

All four phrases retain source intent in casual American English. No unproved
speaker identity, kinship or rank is assigned. The enlarged rotated source crop
supports まちやがれ; it supersedes an older draft reading. Logical phrases are
automatically wrapped. Whole raster reconstruction rejects dropped letters even
if a corrupt payload is given a fresh checksum.

## Preservation and approximate restoration

Only four reviewed frame5 regions are owned. The two white bubble interiors use
rectangles `[20,15,73,91]` and `[230,18,268,92]`, preserving explicit source
corner rectangles. Complete phrases fit at 9px. Review caught leftover source
antialias pixels and a final right-bubble glyph row; these are now covered.

Red refusal lettering uses source maroon word4173. It moves into blank space
above the photo so the full phrase avoids the visible gray outline and photo
top border. Pursuit lettering replaces the slanted black source call. Visible
protected outlines remain exact. New alpha touching protected outlines or photo
top row51 is rejected. Review caught an inferred white stripe and accidental
soil erasure; the final source mask and strict red seed exclude these defects.

Old call masks include bounded antialias fringes. Photo restoration uses canonical
frame4, with its old title masked from training/restored from original source
samples. Modal color mapping, fallback and covered outline interpolation are
**approximate**, not exact original hidden-pixel recovery. Source-guided contour
estimates affect only original glyph/fringe pixels. No native loading, geometry,
GPU/alpha, crop, display, input or gameplay proof is claimed from offline images.

All older seven raw records, prior atlas syncs, other frames, unowned source pixels,
storage lengths and headers remain exact. Canonical source is immutable; there is
no derivative donor and no invented PXL header/crop proof for this raw block.

## Verification

- **99 focused tests pass**, including 21 chase tests and 78 inherited cases.
  Full glyph checks, source/geometry locks, protected corners/outline/border,
  source mask ownership and soil preservation are checked.
- Final code reproduces **whole V181 byte for byte** after the last renderer
  changes. Dependency hashes are pinned in the reproduction and saved proof.
- Complete 463-batch stack, inherited terminal stages, prior record IDs,
  relocation tables, golden menus and all manifest checks pass.
- Only `/GRP/SLACKIMG.DK4` differs from V181; only four frame5 regions change.
  The same 34 canonical changed paths remain listed in the adjacent manifest.
- Clean-ROM xdelta reconstruction is byte exact. Changed code/tests pass Ruff.

## Exact handoff

| Artifact | SHA-256 |
| --- | --- |
| Canonical out/raphael_natural_v2_accepted_base.nds | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base work/clean.nds | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V181 / final full reproduction | `b1df10ccd0a208b9728a51e99b63fdf376b759cbda0315a27119344f39f51d55` |
| out\all_routes_combined_v182_candidate.nds | `87513b3f8661413eaa382c22ffd684358301a3128bdbc41319ee66461ac00419` |
| ARM9, unchanged | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry | `acf367a8eb1babff602190195cba094dfe751e8097a97d1c6ec91437d8572a4c` |
| Builder, unchanged | `d58a3d5816f6cadea3982aeac86647057f3a724d3f99c7d3e8e7a925d6891e29` |
| Raw-art module | `c1790ac82a5f9f122fab5aa041f0d2c2fe2d1505a7a9fa0ffe1bb3f2958a7b03` |
| Caption-restoration module | `d4818b7f5c544d3b1c56f788ed384b8e4be9496c33eb3098bd27df076dc03c39` |
| Chase-restoration module | `7ddef0e83cacdc062b362f7479d709dbc1b58510a2350c0a43f430a9dbf24766` |
| out\all_routes_combined_v182_candidate.xdelta, 848524 bytes | `ca092818b8183a2ff0acf984344894e6d6bca2ba4a7c9ace434181bae95562d4` |

Profile **all-routes-unified-v182**, **463 experimental batches**. All accepted
layers remain baked into the canonical base; zero additional accepted batches
applied. Cumulative `translations/gallery_chase_raw_art_v4.json` replaces only
`translations/gallery_comic_captions_raw_art_v3.json`: seven earlier records exact,
four appended. All inherited terminal stages are preserved. Adjacent manifest:
`out/all_routes_combined_v182_candidate.manifest.json`.

Evidence: `work/analysis/chase_comic_v182_saved_proof.json`,
`work/analysis/v181_chase_builder_reproduction.json`/`.nds`/`.log`,
`work/analysis/v182_graphics_tests.log`, `work/analysis/v182_build.log`,
`work/qa/chase_comic_v182/evidence.json`, `review.png`, `restoration_masks.png`;
`scripts/chase_comic_v182.py`, `tests/test_raw_chase_comic.py` and
`dk4tool/graphics/raw_chase_restore.py`.

## Remaining and actual testing

**Five embedded images:** 6/7/8/11/12. **Four Online files:** Online24/27/31/33,
including Online27 chat/status. Original 12 text-bearing image count and broader
unclassified block counts remain unchanged. Source transcription, embedded/native
formats, contextual usage, full-resolution review, Latin names, image207 meaning,
prior title scenery/composition and native/gameplay gates remain open.

Cold boot without savestates: title/menu, New Game/name entry, an established
story scene, town UI and inherited repaired screens. If reachable, inspect the
frame5 chase panel's complete letters, 9px readability, bubble corners, restored
scenery/contours, colors/crops and navigation. Inspect earlier recruitment/Maria/
closing panels, Online27 and title scenes as described in prior checkpoints.
Actual raw consumer/reachability still needs mapping. No human acceptance is
assumed; explicit cold-boot acceptance is required before canonical promotion.

Keep the user-requested note to revisit older record-based checks when the full
project goal is complete.
