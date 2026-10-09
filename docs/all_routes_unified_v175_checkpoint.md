# Combined V175: three English Rota Nova title copies

2026-10-04. V175 is **experimental**. The standalone logo and both DS title-screen
copies now use complete English franchise and phonetic-caption lettering. All
previous graphics/text/code/repair stages remain exact. The all-graphics goal
remains active and incomplete.

## Localization and exact ownership

Main title: **UNCHARTED / WATERS IV**. Small ロッタ ノヴァ caption: **Rota Nova**.
This retains the English series naming and original Latin subtitle treatment
established by V174. The original large gold ROTA NOVA and stylized N remain.
English glyphs are rendered whole, with no runtime font/code change and no rescaling
or cropping of an existing runtime glyph. Both full lines fit above the original
Latin ornament. The new artwork uses original palette colors and source-hash-bound
serif glyphs; the playable builder needs only serialized indexed pixels.

| Original resource | Owned main region | Owned caption region | Changed indices | Exact overlapping gold pixels |
| --- | --- | --- | ---: | ---: |
| `/_pxl/logo.pxl` | `[4, 50, 252, 101]` | `[151, 121, 201, 133]` | 9605 | 112 |
| `/_pxl/title/title03.pxl` | `[4, 8, 252, 57]` | `[150, 81, 198, 90]` | 11277 | 24 |
| `/_pxl/title/title05.pxl` | `[4, 47, 252, 96]` | `[150, 120, 198, 129]` | 11100 | 29 |

All files remain **256×192, 8-bit indexed**, with original palettes, headers,
metadata, storage extent and every unowned pixel exact. The existing Latin ornament
is mapped from the canonical original separate Rota Nova texture with explicit
composition offsets; English ink cannot overlap protected ornament pixels. Each
original gold pixel overlapping the main lettering rectangle is independently
checked unchanged. Gold Latin body and copyright outside the owned cells remain
byte-exact. Old Japanese blue caption lettering is replaced without erasing gold.

The standalone background remains original black. DS scene restoration uses the
original logo-free `/_pxl/title/title00.pxl` ship/sky and `title04.pxl` water images.
The source images have different palettes; donor colors are mapped into each exact
original target palette only in owned text regions. All other scenery remains exact.
This is source-backed scene restoration, not a claim of recovering hidden original
pixels byte-for-byte. Original title orientation/layout and palette mapping still
need actual native/gameplay validation. Full original/English comparisons for all
three files were reviewed.

The builder's new indexed PXL region format locks the original file and region
SHAs; checks rectangle bounds, nonoverlapping ownership, unique IDs, exact payload
size/SHA and palette range; and preserves source headers/palette/allocation. The
complete prior **V174 ROM reproduces byte for byte** before V175 is built.

## Verification and limitations

**211 focused graphics tests pass**, including 20 new title-copy checks. They
reject removal of first/final blue letter ink in all six cells, loss of Latin/body/
copyright/scenery pixels, wrong source/region hashes, invalid bounds, wrong payloads,
overlapping/duplicate ownership and loss of inherited batches/stages. Original
donor hashes and complete glyph bounds are pinned. Builder, author script and tests
pass Ruff. Saved identity/profile/layer/record/relocation and golden-menu checks pass.
The clean-ROM xdelta reconstructs the exact saved candidate.

Three controlled native PXL header tests return 256×192; six supplied main/caption
crop constructor calls check origins/extents, owner fields, ABI/canaries. Controlled
source-owner/table/crop inputs do not establish actual title loaders/parent consumers,
live crops, GPU palette/alpha or physical playback/input. Gameplay feedback has been
requested for the concrete V175 candidate; no result has been assumed. V175 remains
experimental until explicit cold-boot acceptance.

## Full graphics scope remaining

Six historical Japanese-bearing entries remain:

- `/_pxl/startmenu0.pxl`
- `/_pxl/winframe00.pxl`
- `/_pxl/online/Online24.pxl`
- `/_pxl/online/Online27.pxl`
- `/_pxl/online/Online31.pxl`
- `/_pxl/online/Online33.pxl`

PC Porto Estado title and subtitle need localization in the two loose copies and
the separate **320×240** embedded WINFRAME block 0. That embedded copy cannot be
replaced as if it shared the loose 256×192 dimensions. Source previews are prepared
under `work/qa/porto_title_research/`. The spare startmenu1 image is ship/sky art;
winframe02/03 are window textures, not a proven logo-free medallion background.
Native usage, source/background ownership and all text need actual review.

Other embedded/unclassified/contextual art, environmental signs, image207's clipped
source mark, opening Latin name-card fidelity, broader full-resolution screening
and actual native/gameplay verification remain additional scope. Six known remaining
entries do not constitute graphics completion. The full active goal coverage is
recorded in `translations/graphics_completion_campaign_v1.json`.

## Exact handoff and inherited stack

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out\raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V174 / exact reproduction | `15df894e0661552af6d1d3f279f84601eb4b9802c0571d8adac07e32398ab089` |
| Candidate: `out\all_routes_combined_v175_candidate.nds` | `55e229aa9d19d894b3197b7f0d179741e26a73619b139ce117f1c9376abaab47` |
| ARM9, unchanged V174 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry | `46048ce42dad1cf68e836e8970debd243408f73c86d146810e4af3daa6ce49f2` |
| Builder | `1f4fd57da285e38c945f4302d3f79c499d2ed0fe274ef4e94b3841588e2f198c` |
| Patch: `out\all_routes_combined_v175_candidate.xdelta`, 804376 bytes | `fb0df9a18b69559348dd2de7b40222a3461f62e68bbef9419d6dcd059f9f7526` |

Profile **all-routes-unified-v175**, experimental, **458 batches**: all 455 V174
batches/stages unchanged, plus the three canonical-source title-art batches.
Accepted layers remain baked into immutable canonical; zero additional accepted
batches are needed. Adjacent candidate manifest names baseline/registry/full
stack/changed paths/record IDs/relocations/checks. Against V174, only
`/_pxl/logo.pxl`, `/_pxl/title/title03.pxl` and `/_pxl/title/title05.pxl` differ.
The 30 canonical changed paths are:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/FLS/M28.fls`, `/GRP/CMMNIMG.DK4`, `/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`, `/_pxl/__marker.pxl`, `/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/logo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/_pxl/title/title03.pxl`, `/_pxl/title/title05.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`, `/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`, `/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`, `/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`, `/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Evidence:

- `scripts/rota_title_copies_v175.py`, `tests/test_rota_title_copies.py`
- `work/qa/rota_titles_v175/logo_review.png`, `title03_review.png`, `title05_review.png`
- `work/qa/rota_titles_v175/evidence.json`, `native.json`
- `work/analysis/v175_graphics_tests.log`, `v174_pxl_art_builder_reproduction.json`
- `work/analysis/rota_titles_v175_saved_proof.json`

Cold-boot without savestates: opening movie and both DS title scenes, title menus/
New Game, captain/name entry, an established story, town UI and inherited repaired
screens. Check complete UNCHARTED/WATERS IV and Rota Nova lettering, original gold
ornament, scenery/seams/copyright, scale/margins, palette/alpha, timing and input/skip
behavior. Check actual standalone/embedded resource usage where reachable. Explicit
user acceptance is required before canonical promotion. Retain the requested
older record-based checks follow-up when the full project goal is complete.
