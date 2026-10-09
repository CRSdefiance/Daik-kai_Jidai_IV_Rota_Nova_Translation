# Combined V176: English Porto Estado title copies

2026-10-04. **Experimental**. The full graphics goal remains active and incomplete.

## Artwork and preservation

Main 大航海時代IV: **UNCHARTED / WATERS IV**. Small ポルト・エシュタード:
**Porto Estado**. The original large gold PORTO ESTADO and ornate E remain.
Complete serif glyphs are authored into source-locked indexed pixels; there is no
runtime font/code change. Added caption word spacing keeps both words distinct.

| Original resource | Original size | Main region | Caption region | Changed indices | Exact gold pixels |
| --- | --- | --- | --- | ---: | ---: |
| `/_pxl/startmenu0.pxl` | 256×192 | `[4, 54, 252, 104]` | `[146, 120, 231, 136]` | 11440 | 1396 |
| `/_pxl/winframe00.pxl` | 256×192 | `[4, 25, 252, 75]` | `[146, 90, 231, 108]` | 9618 | 1168 |
| `/GRP/WINFRAME.DK4` | 320×240 | `[5, 31, 315, 95]` | `[182, 113, 289, 137]` | 15531 | 1774 |

The embedded image remains its own 320×240, single-bank 8-bit type-16 image;
it is never inserted as a resized loose 256×192 PXL. Native block headers,
palette, flags, dimension metadata, trailer, archive allocation and all other
blocks remain exact. Loose files retain their original palette/header/extent.
Every changed index lies inside the reviewed old-glyph restoration mask or the
complete new ink/outline. Unowned pixels, including border and copyright, remain
exact. Original gold and adjacent bevel/shadow pixels are protected; nearby
Japanese blue ink is excluded from bevel protection to avoid surviving flecks.

No text-free medallion donor was found. Selected old blue lettering/shadow holes
use bounded harmonic reconstruction from original surrounding colors; this is
**approximate scenery**, not recovery of the hidden original artwork. The water
version uses original title04 water with modal palette correspondence learned
outside the logo. Review caught and corrected an initial pale water band and
caption top-row/fleck omissions before registration. Three final full previews
were inspected. Native display still needs review for seams, palette and scale.

## Verification

- Complete previous V175 ROM reproduces byte for byte after builder support changes.
- **240 focused graphics tests pass**, including 29 new title tests. Mutations
  reject first/final blue glyph loss, source/block/region mismatch, wrong native
  type/extent, wrong payload, out-of-bounds or overlapping/duplicate ownership,
  unowned scene/copyright changes and loss of prior batches/stages. Regression
  cases cover original caption rows y=93/116 and Japanese ink beside gold bevels.
- Builder, author script, controlled probe and tests pass Ruff.
- Saved manifest/profile/registry/full stack/records/relocations, exact three-file
  delta and golden-menu checks pass; the patch reconstructs the exact candidate.
- Two controlled generic PXL header tests return original 256×192 dimensions;
  six supplied native crop constructors preserve origins/extents, owner fields,
  saved-register ABI and canaries. Embedded ILNK bytes are never used as PXL.

The source owner, table and crop inputs are supplied. These controlled probes do
not prove actual PC-title resource loading, embedded loading, parent consumers,
live crops, palette banks/alpha, GPU composition or physical input/gameplay.
No actual cold-boot result has been assumed, including the outstanding V175 check.

## Exact handoff

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V175 / exact reproduction | `55e229aa9d19d894b3197b7f0d179741e26a73619b139ce117f1c9376abaab47` |
| Candidate: `out/all_routes_combined_v176_candidate.nds` | `cd23f79777fa9f22d41dd45ce01609de335a37284494f429a96ae90c26a1f79e` |
| ARM9, unchanged from V175 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry | `b6284dd8b4cfa0fe11a4eda0f442372a1543f732a0b662396ac4db898483f416` |
| Builder | `09ad79d17085303223c6538c1dc1eb88421b9bf611fe7649c0a740be1cf833ba` |
| Patch: `out/all_routes_combined_v176_candidate.xdelta`, 831181 bytes | `6929eb43cb539a4ec4bbedfcb7d6142aba479cd49f9544d4b4e4e896a94547ea` |

Profile **all-routes-unified-v176**, experimental: all **458** V175 batches and
terminal repair stages are inherited unchanged, plus three canonical-source
batches:

- `translations/porto_title_startmenu0_art_v1.json`
- `translations/porto_title_winframe00_art_v1.json`
- `translations/porto_title_embedded_art_v1.json`

**461** experimental batches total; accepted layers remain baked into the immutable
canonical base, with zero additional accepted batches applied. The adjacent
`out/all_routes_combined_v176_candidate.manifest.json` lists every batch, required
layer, changed record, registry identity and check. Compared with V175, only
`/_pxl/startmenu0.pxl`, `/_pxl/winframe00.pxl` and `/GRP/WINFRAME.DK4` differ.
The complete 33 canonical changed paths are:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/FLS/M28.fls`, `/GRP/CMMNIMG.DK4`, `/GRP/SLACKIMG.DK4`, `/GRP/WINFRAME.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`, `/_pxl/__marker.pxl`, `/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/logo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/_pxl/startmenu0.pxl`, `/_pxl/title/title03.pxl`, `/_pxl/title/title05.pxl`, `/_pxl/winframe00.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`, `/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`, `/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`, `/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`, `/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

## Evidence and remaining scope

- `work/qa/porto_titles_v176/`: original/English comparisons, evidence and native.json.
- `work/analysis/porto_titles_v176_saved_proof.json`.
- `work/analysis/v175_ilnk_art_builder_reproduction.json` and its exact ROM.
- `work/analysis/v176_graphics_tests.log`, `v176_porto_tests.log`, `v176_build.log`.
- `scripts/porto_title_copies_v176.py`, `scripts/probe_porto_titles_v176.py`,
  `tests/test_porto_title_copies.py` and the indexed ILNK builder support.

Four historical Japanese-bearing files remain: Online24/27/31/33. Their canonical
256×192 source screenshots and hashes have been prepared under
`work/qa/online_remaining/`. Baked PC UI/chat is reduced and partly unreadable;
faithful transcription or better original source is required before replacing it.
Do not invent text based on the surrounding scene.

Additional scope remains: embedded unclassified archives/native composition,
environmental signs in kbj04/kbj08 and town32/33/35/37, image207's clipped source
mark, opening Latin name-card fidelity, broader full-resolution screening, actual
native/gameplay checks and final combined package. The completed embedded WINFRAME
storage localization still needs actual native loading/display validation.
Coverage is tracked in `translations/graphics_completion_campaign_v1.json`.

Cold-boot without savestates: opening movie, both DS title scenes, title menu/New
Game, captain/name entry, an established story, town UI and inherited repaired
screens. Check complete titles/captions, original gold/bevel/copyright, scenery
seams, scale/bounds, palette/alpha and timing/input. Validate the loose PC title
and embedded WINFRAME if used by a reachable scene; their actual consumers remain
unmapped. Explicit user cold-boot acceptance is required for canonical promotion.
Retain the user's requested note to revisit older record-based checks when the
**full project goal** is complete.
