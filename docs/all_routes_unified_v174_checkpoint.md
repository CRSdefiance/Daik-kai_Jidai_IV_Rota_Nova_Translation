# Combined V174: English opening-movie title artwork

2026-10-04. V174 is **experimental**. The opening-movie title textures now use
complete English title lettering, preserving all earlier graphics/text/code and
repair stages. The all-graphics goal remains active and incomplete.

## Source-faithful title treatment

| Texture | Original Japanese | English artwork | Owned rectangle |
| --- | --- | --- | --- |
| M28 4 | 大航海時代IV | UNCHARTED / WATERS IV | `[6,1,251,50]` |
| M28 5 | ロッタ ノヴァ | Rota Nova | `[151,39,201,50]` |

Koei's English corporate title lists use **Uncharted Waters IV**; its original
catalog identifies the handheld game as 大航海時代IV ROTA NOVA. The project
localizes the franchise name while retaining the subtitle. Primary references:
[Koei English title list](https://www.koeitecmo.co.jp/e/ir/docs/ird1_20250212_09e.pdf),
[original Koei Rota Nova catalog](https://www.gamecity.ne.jp/products/products/ee/Rldai4rn.htm).
This is project-authored English artwork, not a claim of an official English DS edition.

The main title uses two complete serif lines in the original Japanese ink envelope,
with original-palette blue shading, white outline and shadow. Every complete glyph
and outline remains inside the original 245×49 envelope. No runtime font or code
changed. The small phonetic caption repeats Rota Nova in English; only original
blue lettering is erased to the existing white backdrop and the complete English
caption drawn. Gold Latin **ROTA NOVA**, its large stylized N, white silhouette,
shadows and every unowned pixel remain exact. The serif font is source-hash-bound
in the artwork proof; the playable builder consumes reviewed indexed pixels and
does not depend on an installed font.

Both textures remain **256×64**. All original palette bytes, texture records,
flags, dimensions, offsets, compressed-slot sizes and resource allocation remain
exact. All other movie data, textures, animation/material/consumer bytes remain
byte-identical. Indexed artwork is applied only inside source-locked rectangles;
the builder validates source resource, original decoded texture SHA, exact native
record, rectangle bounds, payload size/SHA and palette range. It rejects duplicate
ownership and compressed-slot overflow. New builder support reproduces the complete
previous **V173 ROM byte for byte** before V174 is built.

## Verification and limits

**191 focused graphics tests pass**, including 15 new title tests. Edge-letter
checks were additionally verified to remove blue letter ink, rather than only
outline/background. Tests cover complete first/final title and caption ink,
original gold logo preservation, palette/record/source locks, payload identity,
bounds, duplicate ownership and every inherited profile stage. Builder, title
script and tests pass Ruff. Full previews and the enlarged English caption were
visually reviewed. Saved candidate identity, full layer list, changed resources,
prior record IDs, relocations and canonical menu checks pass. The clean-ROM patch
reconstructs the exact candidate.

These checks prove storage/artwork preservation and full source-envelope fit.
They do not prove native movie UVs, actual loading/composition, palette-bank/alpha
selection or physical playback/controller behavior. These remain required before
acceptance; no complete graphics goal or global display guarantee is claimed.

Nine historical Japanese-bearing entries remain in nine files:

- `/_pxl/logo.pxl`
- `/_pxl/startmenu0.pxl`
- `/_pxl/winframe00.pxl`
- `/_pxl/online/Online24.pxl`
- `/_pxl/online/Online27.pxl`
- `/_pxl/online/Online31.pxl`
- `/_pxl/online/Online33.pxl`
- `/_pxl/title/title03.pxl`
- `/_pxl/title/title05.pxl`

Embedded title copies, unclassified/contextual artwork, image207's clipped source
mark, opening Latin name-card consistency, broader full-resolution review and
actual native/gameplay verification remain additional scope. The inventory count
is not completion. Original logo-free ship/sky and water backgrounds were found
and rendered for the next title batch. Exact sampled RGB correspondence is not
established; palette quantization, scene alignment and precise title ownership
must be reviewed before copying scenery. Exploratory comparisons are saved in
`work/qa/title_research_v174/background_correspondence.json`.

## Exact handoff and inherited stack

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out\raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V173 / exact reproduction | `19df444510eca115d1facc118180a793ef99cdcbc104f484428d3c0575b4f29f` |
| Candidate: `out\all_routes_combined_v174_candidate.nds` | `15df894e0661552af6d1d3f279f84601eb4b9802c0571d8adac07e32398ab089` |
| ARM9, unchanged V173 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Release registry | `d1914f639864968959f6a34d82b0cf3a76f7753a53c5c6f981e48b8a3980172b` |
| Builder | `1227b6daf8150c8e070aef3ed67f270b2ca902804089e41bf058898e814e84ab` |
| Patch: `out\all_routes_combined_v174_candidate.xdelta`, 786344 bytes | `de1cee88d4db0ad06b16cc1ffcac5eb7a2c15a5546c57e162fea8dab8429c49a` |

Profile **all-routes-unified-v174**, experimental, **455 batches**: all 454 V173
batches/stages unchanged, plus `translations/opening_m28_title_art_v1.json`.
Accepted layers remain baked into immutable canonical; zero additional accepted
batches are required. The adjacent candidate manifest records the baseline/registry,
complete batches, changed paths/record IDs, relocations and checks. Against V173,
**only `/FLS/M28.fls` differs**. The 27 canonical changed paths are:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/FLS/M28.fls`, `/GRP/CMMNIMG.DK4`, `/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`, `/_pxl/__marker.pxl`, `/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`, `/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`, `/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`, `/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`, `/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Evidence and reproducibility:

- `scripts/opening_title_v174.py`, `tests/test_opening_title_art.py`
- `work/qa/opening_title_v174/review.png`, `english_caption.png`, `evidence.json`
- `work/analysis/v174_graphics_tests.log`, `v174_edge_ink_tests.log`
- `work/analysis/v173_title_builder_reproduction.json`
- `work/analysis/opening_title_v174_saved_proof.json`
- `translations/graphics_completion_campaign_v1.json`

Cold-boot without savestates: title/New Game, captain/name entry, an established
story, town UI and inherited repaired screens. Let the opening movie reach both
logos; verify complete UNCHARTED / WATERS IV lines and Rota Nova caption, correct
order/timing/UVs, margins, scale, palette/alpha and input/skip behavior. Recheck
prior title prompts and translations. Explicit user acceptance is required before
canonical promotion. On full project-goal completion, retain the requested note
to revisit older record-based checks.
