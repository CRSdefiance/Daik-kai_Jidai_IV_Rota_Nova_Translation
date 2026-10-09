# Combined V164: Won/Lost score graphics

V164 is the latest **experimental** combined candidate. It replaces the two
Japanese score tally symbols in `/_pxl/deck04.pxl` with complete English words.
Every other V163 resource/component and inherited repair remains exact.
The full translation goal remains incomplete; canonical promotion and final
commit/push remain pending.

## Source and natural English

| Japanese | English | Meaning/context |
| --- | --- | --- |
| 勝 | Won | Games or matches won; victory tally. |
| 敗 | Lost | Games or matches lost; defeat tally. |

Won/Lost express the original tally meanings in natural English. Both are
complete words. The first source symbol occupies x160–183/y0–23; the second
occupies x184–207/y0–23. The source ink spans both complete 24×24 cells.
The English uses the original compact five-pixel advance and every visible
native font pixel. It is centered within those original cells: Won's visible
bounds are `[164,8,178,17]`, Lost's are `[186,8,205,17]` (exclusive right/bottom).
All eleven rows of each native glyph cell execute, including blank rows; no
visible row is trimmed. The source palette's index 15 supplies the light ink.

Only the two old lettering cells are cleared to the original black index 0 and
redrawn. All ten digit sprites, the full cursive **Perfect!** artwork, headers,
palettes, dimensions, extents and every other pixel remain exact. The source
image matches the clean Japanese ROM, canonical baseline and V163 exactly.
Complete source and English previews were reviewed at 4× nearest-neighbor with
the original aspect ratio.

Preview: `work/qa/score_graphics_v164/review.png`.
Source/artwork: `work/analysis/score_graphics_v164_artwork.json`.

## Native evidence and limits

**60 focused graphics tests pass**: ten new score tests and all 50 earlier
button/name/treasure/fleet/village tests. They check complete native glyphs,
negative missing-first-character cases, full original four-bit geometry and
packing, native selector/sizing/crop descriptors, original art/header/palette
preservation, source-lock rejection and full profile/stage inheritance.
New implementation and tests pass Ruff.

The actual native font lookup/pixel primitive executes every character in a
blank image with the **original 208×72 four-bit PXL header and palette**. Its
complete output matches independent font masks and the packed English cells.
Saved registers, stack, full source header/palette and memory canaries pass.
Two separate compact-glyph scratch cases also verify full letter shapes and
first/final characters. This batch's actual image format supports the native
four-bit primitive directly.

The native selector `02011D2C` maps type 33 through the original table to owner
`023139FC`; the original file descriptor names `_pxl/deck04.pxl`. The type
virtual is a **controlled input** bound to existing native code returning 33;
this does not prove construction of a live score object. Common native sizing
confirms 208×72 with a controlled loaded header/resource and selector binding.

The real crop constructor `020D3B34` and helpers execute the two original
24×24 cells and preserve resource, source origin, extent, ABI and canaries.
These crop requests are **supplied source-cell contracts**. The complete score
parent caller has not yet been mapped; no live parent crop or GPU output is
claimed. Actual file loading, all score contexts, parent composition, GPU
palette/alpha, hardware input and physical gameplay remain pending.
Native evidence: `work/analysis/score_graphics_v164_native.json`.

Saved-ROM checks prove all prior V163 components/resources, terminal stages,
relocations and changed records exact. ARM9, shared text/HELP, all four routes
and previous graphics remain byte-identical. Canonical menu/graphics invariants
and exact clean-ROM patch reconstruction pass.
Saved proof: `work/analysis/score_v164_saved_proof.json`.

## Candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V163 comparison | `e37d81b0ba5f12c21d5a586966944f087b9ec348ce85e5fdc03c8d02d4721cd9` |
| V164: `out/all_routes_combined_v164_candidate.nds` | `b09e54f664c51cadb40ecc8287b19069cc4c544199e3c4eb3cde9b1d4ddf43fb` |
| ARM9, exact V163 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V164 build | `32ab14eae79dcf5957f6b054f05111e1a3d76e99b677c0278696cd63aad280fa` |
| V164 patch: `out/all_routes_combined_v164_candidate.xdelta`, 768610 bytes | `2ebe595ad67025445911deda80fdffd987bade70fc5f7b817641f9dca44c6aeb` |

Profile: `all-routes-unified-v164`, experimental. The registered builder starts
from the immutable canonical base and reproduces all 449 V163 batches and
terminal stages. The additional source-locked experimental batch is
`translations/score_won_lost_graphics_v1.json`, bringing the total to **450**.
All accepted layers are baked into the canonical base; zero additional accepted
batches are required. The adjacent `.manifest.json` records every batch,
changed path/record, inherited stage and build check.

Compared with V163, **only `/_pxl/deck04.pxl` differs**.

Compared with the canonical baseline, 23 internal paths differ:
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/SLACKIMG.DK4`,
`/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/deck04.pxl`,
`/_pxl/dividecrewinfo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`,
`/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`,
`/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`,
`/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`,
`/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`,
`/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`,
`/evstill/evstill208.pxl` and `/evstill/evstill209.pxl`.

Before acceptance, cold-boot without a savestate and test title, New Game
captain selection/name entry, an established story, town UI and inherited
changed item/Advice/Gallery/treasure/fleet/village/button screens. Find every
score-atlas context and check complete Won/Lost labels with the digits and
Perfect artwork, actual crop/alignment, palette/alpha and input behavior.
Explicit user acceptance is required before canonical promotion.

## Full goal remaining

245 COMMON selections / 133 physical owners still need actual consumer/layout
integration. Other ARM9/UI, name/source fidelity, Reports/Sailing Help
persistence, BGM physical audio/input, downloaded items and full gameplay
checks remain. The historical graphics inventory now has **13** other confirmed
Japanese loose/FLS resources, one matching embedded title copy, the separate
CMMNIMG atlas and unclassified art. Live graphic use/crops and image 207's
clipped source mark remain review tasks. These counts describe inventory after
the edits; they do not clear all physical screens. Final packaging/progress and
GitHub commit/push remain. On full goal completion, retain the requested note to
revisit older record-based checks.
