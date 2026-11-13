# Combined V180: Maria heading and player thanks

2026-10-04. **Experimental**. The all-graphics goal remains active and incomplete.

## Source and English

SLACKIMG block19, reviewed raw 320×240 frame13:

| Source | Natural English | Owned rectangle |
| --- | --- | --- |
| まりあもーど | Maria Mode | `[269,36,307,199]` |
| さいごまでプレイしてくれて、ありがとうございます… | Thanks for playing all the way through... | `[0,214,280,240]` |

The complete heading rotates clockwise within the original title strip. The
closing sentence thanks the player for playing to the end and preserves the
trailing pause. Both original painted creator marks and their explicit Latin
`by` labels remain exact. No romanized creator identity is invented. Retention
decisions: `translations/gallery_maria_creator_marks_v180.json`, rectangles
`[239,91,267,199]` and `[280,211,320,240]`.

Full comparison review caught leftover original ellipsis dots beyond the first
footer rectangle. Final ownership extends to x280, erasing the complete source
sentence/pause while preserving the creator region. The corrected full preview
and enlarged boundary were reviewed. Portrait, veil, gold frame, connected art,
high color bits, archive headers/allocation and unowned pixels remain exact.

## Renderer and verification

Clockwise glyph bounds are transformed from the full unrotated mask. Explicit
black ink allows the cream title background. On the black footer, the new
background-aware protection connects colored scene pixels to neutral foreground
edges without flooding through the black canvas. The previous V179 background
rule keeps its exact behavior. Payloads must equal complete English raster
reconstruction from source, logical text and the locked font; a recomputed
checksum cannot legitimize deleted letters.

- **59 focused tests pass**: 12 Maria cases, 17 earlier closing-art cases and 30
  atlas/button/source-mark regressions. Actual rotated/footer first/final-letter
  deletion with recomputed hashes fails; creator/unowned corruption, invalid
  rotation/ink/background rules, full glyph extents, old gray-hand preservation,
  old atlas composition and exact cumulative batch replacement are covered.
- The changed renderer reproduces the **entire V179 ROM byte for byte**, including
  all 463 batches and terminal stages. Builder hash is unchanged.
- Saved V180 manifest/profile/registry, full batch/stage inheritance, prior
  record-ID prefixes, golden menus and one-file delta pass. Frame16, other raw
  frames and SLACKIMG atlas blocks12/20 remain exact.
- The patch against the locked clean ROM reconstructs V180 byte for byte.
  Changed code/tests pass Ruff.

Raw 320×240 partitioning remains a reviewed storage interpretation. Actual native
loader/geometry/crops/alpha/GPU/display/input/gameplay are **unproved**. No invented
PXL header/crop callback is used as raw-art native evidence. Offline visual review
and complete-letter tests do not substitute for actual display acceptance.

## Exact handoff

| Artifact | SHA-256 |
| --- | --- |
| Canonical `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V179 / full reproduction | `9187eae3b0fe2c0187d84d678611ae03014244a0f0ed9f22c2b4a6a3b13f76ad` |
| `out/all_routes_combined_v180_candidate.nds` | `05de18b9ebf552023b4fda5ce7086171277f8fa4a22ed30d432ec93fe84d44db` |
| ARM9, unchanged | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry | `bc57f2cd6229fb08f79ecdc8238903a6e995e0537a2b24a3277da6a91b436111` |
| Builder, unchanged | `d58a3d5816f6cadea3982aeac86647057f3a724d3f99c7d3e8e7a925d6891e29` |
| Raw-art module | `29744365aff45ee97dd12c5a98238ac7a67e9babf61ff43737053c906aff26a9` |
| `out/all_routes_combined_v180_candidate.xdelta`, 836844 bytes | `11f855664f397700d1eb09efe128e44da2e97293fa1f9270883817e119fccad8` |

Profile **all-routes-unified-v180** preserves all V179 stages and **463 experimental
batches**, replacing `translations/gallery_closing_raw_art_v1.json` with cumulative
`translations/gallery_closing_maria_raw_art_v2.json`. The first two records are
exact V179 records; two frame13 records are appended. Historical v1 is unchanged.
All accepted layers are baked into the immutable canonical base; zero additional
accepted batches applied. Adjacent manifest:
`out/all_routes_combined_v180_candidate.manifest.json`.

Only **`/GRP/SLACKIMG.DK4`** differs from V179, within two frame13 text rectangles.
The same 34 canonical changed paths remain in the manifest and saved proof.

Evidence: `work/analysis/maria_gallery_v180_saved_proof.json`,
`work/analysis/v179_maria_builder_reproduction.json`/`.nds`/`.log`,
`work/qa/maria_gallery_v180/evidence.json`, `review.png`, `footer_source_zoom.png`,
`work/analysis/v180_graphics_tests.log`, `v180_build.log`;
`scripts/maria_gallery_v180.py`, `tests/test_raw_gallery_maria_art.py`.

## Remaining and actual testing

**Eight embedded caption/dialogue/credit images remain:** 4/5/6/7/8/10/11/12.
Frames13/16 have complete English content; frame13's two creator credits and
frames18/19's corner marks retain original attribution styling. **Four historical
Online files remain:** Online24/27/31/33, including reduced Online27 chat/status.
Original 12 text-bearing source count and unclassified-block counts are unchanged.
Other embedded formats, broad full-resolution/source review, opening Latin names,
image207 meaning, earlier title scenery/composition and native/gameplay gates
remain open. Campaign `complete` remains false.

Cold boot without savestates: opening/title/menu, New Game and name entry,
established story, town UI and inherited repaired screens. Inspect this Maria
gallery picture if reachable: complete readable heading and thanks, original
creator marks/portrait/veil/gold borders, dimensions/crops/colors/alpha and input.
Actual consumer/reachability mapping remains necessary. Check earlier title
scenes, Online27, image207 and the closing frame16 picture as documented in
[V179](all_routes_unified_v179_checkpoint.md).

No human cold-boot acceptance, including V175, is assumed. Canonical promotion
requires explicit acceptance under repository instructions. Keep the user-requested
note to revisit older record-based checks when the full project goal is complete.
