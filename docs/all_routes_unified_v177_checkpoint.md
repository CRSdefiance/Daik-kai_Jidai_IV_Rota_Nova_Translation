# Combined V177: four source-backed Online27 speech bubbles

2026-10-04. **Experimental**. The all-graphics goal remains active and incomplete.

## Translation and preserved artwork

The publisher's [bazaar screenshot](https://www.gamecity.ne.jp/dol/game/image04/m_02.png)
shows the same four speech bubbles clearly. Its wider UI and crop differ from the
ROM screenshot; it supplies these phrases, not a replacement whole screenshot.

| Source phrase | Natural English | Owned interior `[left, top, right, bottom]` |
| --- | --- | --- |
| ありがとうございます | Thank you! | `[47, 66, 81, 76]` |
| もってけ！どろぼー | It's a steal! | `[68, 78, 100, 89]` |
| ではまたご贔屓くださいませ | Come again! | `[221, 68, 252, 80]` |
| いらっしゃーい | Welcome! | `[105, 106, 133, 113]` |

The bargain call is a playful vendor idiom; the English preserves that effect.
Complete Arial glyph rasters, including first and final characters, are quantized
to the original palette's greys. There is no runtime dialogue, font or command
change. **1078 indices** change inside these four source-locked interiors only.
Original bubble borders/tails, scenery, header, allocation, palette and all
unowned pixels remain exact. Reduced chat, status text and player labels remain
Japanese and need faithful transcription. **Online27 is only partly localized.**

Source image SHA-256: `842e2440bdd21cc2ac0a9bea8025e6f1f6527c7d63773fb81bb1f18b5b050e51`.
The complete comparison preview was reviewed. Native small-letter readability
and actual gallery presentation still need checking.

## Verification

- **65 focused tests pass**: 16 new bubble tests, 29 Porto title tests and 20 Rota
  title tests. First/final letter loss, source mismatch, unowned pixel changes,
  wrong bounds and lost inherited batches are rejected. This is not a rerun of
  V176's full 240-test suite.
- Authoring, source inspection, portrait audit and bubble tests pass Ruff.
- Saved profile/registry/manifest, every inherited batch/stage, golden menus and
  record identities pass. Builder and ARM9 are unchanged from V176.
- Only `/_pxl/online/Online27.pxl` differs from V176. The canonical delta contains
  34 internal files, all listed in the adjacent manifest and saved proof.
- The clean-ROM patch reconstructs the exact candidate byte for byte.
- One controlled PXL header returns 256×192; four supplied crop contracts preserve
  owner/origin/extent, ABI and canaries. Supplied inputs do not prove the actual
  gallery loader, parent consumer, live crop, palette/alpha or GPU composition.

## Reference-art inspection

Six environmental resources were inspected at source resolution and enlarged:
`/_pxl/kbj04.pxl`, `/_pxl/kbj08.pxl`, and `/towngrp/towngrp32.pxl`,
`towngrp33.pxl`, `towngrp35.pxl`, `towngrp37.pxl`. Retain their original physical
lantern/plaque/shop decoration. The lantern has 酒; the smaller signs cannot be
faithfully transcribed. No English shop names, city or language assignment are
invented. All six files are byte-identical to canonical in V177. Actual consumer
usage and any separate facility/help captions remain pending. Decisions and
observations are in `translations/contextual_graphics_decisions_v177.json`.

All words in `/GRP/SLACKIMG.DK4` block 13 yield 42 coherent 320×240 BGR555
portrait previews; all 42 full-size images were visually inspected. No Japanese
caption was observed. Existing Latin **El Gato** apparel wording is retained.
The block remains byte-identical to canonical. Preview hashes, source partitions,
word roundtrip and observations are in
`work/qa/embedded_raw_v176/portrait13/inventory.json`. The partition/encoding have
not been proved by native metadata or a mapped loader, so the block is not counted
as a cleared native format. Other raw-block hypotheses remain unclassified.

**New text-bearing discovery:** all words in SLACKIMG block 19 produce 21 coherent
320×240 sketch/comic images. All 21 full-size images were reviewed; 12 contain
East Asian text, including Japanese captions/dialogue/effects, a Chinese speech
balloon and small creator signatures. Indices **4/5/6/7/8/10/11/12/13/16/18/19**
need translation or an explicit creator-credit decision. This is additional work
outside the historical four-file Online remainder. The source block is unchanged
in V177, SHA `c95b9d4b968638d488158c8971c03f4116ac6e6ceb8a6863a4de5a1b05b54464`.
`scripts/inspect_raw_sketches_v177.py` pins all source words, previews and review
observations in `work/qa/embedded_raw_v177/sketch19/inventory.json`.
Native encoding/partition/usage remain unproved; unclassified-block counts are
unchanged. No comic panel is shipped as translated in this checkpoint.

The old publisher Flash site was inspected statically without executing its
scripts. Its extracted artwork did not supply the four remaining PC screenshots.
Other official screenshots found this session have different dialogue/UI and are
not valid substitutes for unreadable source wording.

## Exact handoff

| Artifact | SHA-256 |
| --- | --- |
| Canonical `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V176 | `cd23f79777fa9f22d41dd45ce01609de335a37284494f429a96ae90c26a1f79e` |
| `out/all_routes_combined_v177_candidate.nds` | `a5dba05534ec334167d0ffd9f506050f35ca11555eaa38cd5d1a17fbf3034d45` |
| ARM9, unchanged from V176 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry | `a53e38f14331263910065289ebbfb228a3d3bfa6d2a088ef8834adaaa2f52239` |
| Builder, unchanged from V176 | `09ad79d17085303223c6538c1dc1eb88421b9bf611fe7649c0a740be1cf833ba` |
| `out/all_routes_combined_v177_candidate.xdelta`, 832003 bytes | `504939cb2d013aad20d5ac39a6da80378990ffaf65b794787f55a72ab65558ba` |

Profile **all-routes-unified-v177** inherits all **461** V176 experimental batches
and terminal repair stages unchanged, plus
`translations/online27_bubbles_art_v1.json`: **462 batches** total. All accepted
layers remain baked into the immutable canonical base; zero extra accepted
batches are applied. The adjacent
`out/all_routes_combined_v177_candidate.manifest.json` names the complete stack,
registry, changed paths/records, dependencies and checks.

Evidence: `work/analysis/online27_bubbles_v177_saved_proof.json`,
`work/qa/online27_bubbles_v177/evidence.json`, `native.json`, `review.png`,
`work/analysis/v177_graphics_tests.log`, `v177_build.log`;
`scripts/online27_bubbles_v177.py`, `scripts/audit_portrait13_v177.py` and
`tests/test_online27_bubbles.py`.

## Remaining work and cold-boot review

Four historical Japanese-bearing files still remain: Online24/27/31/33. Obtain
faithful wording for their reduced baked PC dialogue/UI/chat before replacing it.
Also resolve the newly discovered 12 text-bearing block-19 comic/credit images.
Also finish embedded/unclassified resources and native composition, full-resolution
screening, image207's clipped source mark, opening Latin name-card consistency,
actual loaders/parents/crops/palette banks/alpha/input/gameplay and final packaging.
Six contextual-art decisions are documented; their actual consumer usage is open.
Earlier V174–V176 title/scene reconstruction checks remain open.

Cold boot without savestates: opening, both title scenes and menu, New Game,
captain/name entry, established story, town UI and inherited repaired screens.
Inspect Online27 if reachable in Extras/Online: all four complete phrases, bubble
borders/tails, original scenery and readability. Check prior title scale/bounds,
scenery seams, palette/alpha, timing/input and reachable embedded consumers.
No human cold-boot acceptance, including V175, has been assumed. Repository
build-continuity rules require explicit human acceptance before canonical promotion.

Keep the user's note to revisit older record-based checks when the **full project
goal** is complete. Coverage is in `translations/graphics_completion_campaign_v1.json`.
