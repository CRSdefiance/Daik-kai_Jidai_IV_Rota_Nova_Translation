# Combined V181: recruitment heading/credits and comic end

2026-10-04. **Experimental**. Full graphics goal active/incomplete.

## Source-faithful English

| Frame | Source | English |
| --- | --- | --- |
| 4 | 新人勧誘編 | Recruiting New Crew |
| 4 | 絵・ホソカワナナエ 原作・ナカムラキョウコ（窓際デカ） | Art: Nanae Hosokawa; Story: Kyoko Nakamura (Madogiwa Deka) |
| 10 | おわり。 | The End. |

Names transliterate explicit source kana, with given name first. Madogiwa Deka
romanizes the source parenthetical; its status as title, alias or other credit
annotation is not inferred. No character identity, rank or kinship is invented.
English remains one logical phrase per record; automatic wrapping places the
credits on three lines. Layout bounds keep all new ink outside the photographs.

## Bounded restoration and its limits

Old white glyphs touch scenery and photo frames. The source-derived mask includes
a two-pixel antialias fringe; the first prototype left colored ghost letter edges,
which full review caught. The final whole comparisons and red restoration masks
were inspected after correcting that defect. Original high color bits, archive
headers/lengths, unowned art/borders and all previous artwork remain exact.

Concealed scenery is estimated from canonical copies of the same photographs:
frame5 for frame4, frame9 for frame10. Modal BGR555 channel correspondence maps
bright donor colors to the dim panel. Frame5's speech/call overlays are excluded;
where its photograph is obscured, adjacent original samples provide bounded
interpolation. Donor mapping is measured inexact and **does not recover the exact
original hidden scenery**. Only old glyph/fringe masks receive this restoration.
Gray canvas uses its original word15855; border colors are drawn from unoccluded
source references (horizontal1057, vertical7399). Added border-mask pixels must be
within two pixels of the fixed original glyph/fringe mask; no recursive growth.

| Region | Owned rectangle | Relative English layout | Estimated scenery pixels | Donor / local fallback |
| --- | --- | --- | --- | --- |
| Recruitment heading | `[33,24,230,61]` | `[0,0,197,27]` | 789 | 399 / 390 |
| Creator credits | `[152,176,295,234]` | `[0,18,143,58]` | 1048 | 1048 / 0 |
| Comic end | `[179,178,296,213]` | `[0,7,117,35]` | 112 | 112 / 0 |

Actual native partition/loader/geometry/crops/alpha/GPU/display/input/gameplay
remain unproved. This raw block has no invented PXL header/crop callback. Offline
source-word preservation and visual review do not prove actual native behavior.
Approximate scenery needs native/source-fidelity review before final clearance.

## Verification

- **78 focused tests pass**: 19 new caption cases plus 59 inherited raw-art,
  atlas/button/source-mark cases. Six actual rehashed first/final-glyph deletions
  fail, as does rehashed scenery corruption. Full glyph bounds, source/geometry
  gates, original high bits, restoration-mask scope, fixed border growth, old hand
  edge pixels, creator marks and exact cumulative batch/stage replacement pass.
- The final renderer/restoration modules reproduce **entire V180 byte for byte**,
  including all 463 batches and terminal stages. Earlier exploratory runs do not
  substitute for the final dependency proof. Builder is unchanged.
- Saved manifest/profile/registry, prior changed-record prefixes, relocations,
  golden menus and complete inherited stack pass. Only SLACKIMG differs from
  V180, inside three reviewed frame4/10 regions. Frames13/16 and old atlas blocks
  12/20 remain exact. All other raw frames and ROM files remain exact versus V180.
- Clean-ROM xdelta reconstruction is byte exact. Changed code/tests pass Ruff.

## Exact handoff

| Artifact | SHA-256 |
| --- | --- |
| Canonical out/raphael_natural_v2_accepted_base.nds | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base work/clean.nds | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V180 / full reproduction | `05de18b9ebf552023b4fda5ce7086171277f8fa4a22ed30d432ec93fe84d44db` |
| out/all_routes_combined_v181_candidate.nds | `b1df10ccd0a208b9728a51e99b63fdf376b759cbda0315a27119344f39f51d55` |
| ARM9, unchanged | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry | `f21739c70d7ed5dcedcf537dce404cfa5554b2809dd3c97b9b9500d9f2387f97` |
| Builder, unchanged | `d58a3d5816f6cadea3982aeac86647057f3a724d3f99c7d3e8e7a925d6891e29` |
| Raw-art module | `a19581158128efda703eb85f0c76121fdb12140b8a5c90a8710330f96086c127` |
| Caption-restoration module | `d4818b7f5c544d3b1c56f788ed384b8e4be9496c33eb3098bd27df076dc03c39` |
| out/all_routes_combined_v181_candidate.xdelta, 842162 bytes | `d5d9d2612a34c0e59b027f6d9c70ca6ad9f4db707cec903b4d9a6ecd611205b5` |

Profile **all-routes-unified-v181**, **463 experimental batches** and all inherited
terminal stages. Cumulative `translations/gallery_comic_captions_raw_art_v3.json`
replaces `translations/gallery_closing_maria_raw_art_v2.json` only. Earlier four
records are exact; three captions/credit records are appended. Historical v2 is
unchanged. Accepted layers remain baked into the immutable canonical base;
zero additional accepted batches applied. Adjacent manifest:
`out/all_routes_combined_v181_candidate.manifest.json`.
Only `/GRP/SLACKIMG.DK4` changes versus V180; the same 34 canonical changed paths
are listed in the manifest and proof.

Evidence: `work/analysis/comic_captions_v181_saved_proof.json`,
`work/analysis/v180_caption_builder_reproduction.json`/`.nds`/`.log`,
`work/qa/comic_captions_v181/evidence.json`, `review.png`, `restoration_masks.png`,
`work/analysis/v181_graphics_tests.log`, `v181_build.log`;
`scripts/comic_captions_v181.py`, `tests/test_raw_comic_captions.py`,
`dk4tool/graphics/raw_caption_restore.py`, `dk4tool/graphics/raw_bgr555_art.py`.

## Remaining and actual testing

**Six embedded images remain:** 5/6/7/8/11/12, including dialogue/effects and Maria
captions. **Four Online files remain:** Online24/27/31/33, including Online27
chat/status. Original 12 text-bearing source count and unclassified-block counts
are unchanged. Other embedded formats, full-resolution/source review, opening
Latin names, image207 meaning, earlier title scenery/composition and actual
native/gameplay gates remain. Canonical story/shared search for うみうし/ウミウシ/
海牛/海の魔物 yielded zero hits in the four route scripts/MESFILE;
`work/analysis/comic_creature_terminology_v181.json` pins that narrow search.
This does not prove the comic creature's official name or native consumer.

Cold boot without savestates: opening/title/menu, New Game/name entry, established
story, town UI and inherited repaired screens. Inspect recruitment and ending
comic panels if reachable: full English/credits/end caption, restored photo edges
and scenery, colors/alpha/crops/readability/navigation/input. Actual consumer and
reachability mapping are still needed. Review prior Maria/closing gallery art,
Online27, image207 and title scenes as in [V180](all_routes_unified_v180_checkpoint.md).

No human cold-boot acceptance is assumed. Repository instructions require explicit
acceptance before canonical promotion. Keep the user-requested note to revisit
older record-based checks when the full project goal is complete.
