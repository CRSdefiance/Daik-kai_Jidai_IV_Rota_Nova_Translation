# Combined V162: fleet row graphics

V162 is the latest **experimental** combined candidate. Five complete English
captions replace the Japanese fleet list lettering in `/Iseki/dock.pxl`.
All earlier translations and repairs remain exact. The full translation goal
remains incomplete; canonical promotion and final commit/push remain pending.

## Source and English

| Japanese | English | Meaning |
| --- | --- | --- |
| 旗艦 | Flagship | First ship in the fleet. |
| 2番艦 | Ship 2 | Second ship. |
| 3番艦 | Ship 3 | Third ship. |
| 4番艦 | Ship 4 | Fourth ship. |
| 5番艦 | Ship 5 | Fifth ship. |

The canonical resource matches the original clean Japanese ROM and V161 exactly.
The labels retain every original English font pixel, with six-pixel advance and
the existing gray palette index 226. All words fit inside the left fleet area.
Each owned rectangle is x3–52 inclusive, sixteen pixels high, starting at y18,
46, 74, 102 and 130. The old lettering and antialias/shadow background are
reconstructed from the untouched repeating pattern two periods to the right
(x+64). No source text appears in those donor rectangles. The header, palette,
dimensions, row dividers, right half and every pixel outside these rectangles
remain exact. The background within each owned rectangle is reconstructed,
not claimed pixel-identical to the Japanese source.

Full source and English previews were reviewed side by side:
`work/qa/fleet_row_graphics_v162/review.png`.
Source/localization/artwork evidence:
`work/analysis/fleet_row_graphics_v162_artwork.json`.

## Verification and limits

**31 focused graphics tests pass**, including nine new fleet tests and all 22
earlier button/name/treasure graphics tests. They cover five complete native
font rasters, negative missing-first-letter cases in both native output and
packed eight-bit artwork, complete visible bounds, source-lock rejection,
exact unowned art/header/palette preservation and full profile inheritance.
New script and test files pass Ruff.

The original font lookup and paletted primitive execute with all eleven rows
of each native glyph cell, stack/register checks and canaries. The four-bit
scratch raster uses palette index 15 to verify shape; the actual eight-bit
fleet image separately verifies every English glyph pixel at source palette
index 226. This does not claim that the four-bit primitive draws eight-bit
textures directly.

The actual native initializer `0210DAF4` also executes and verifies the dock
resource descriptor at `022A44B8`, its original vtable `02160538`, path
`Iseki/dock.pxl`, resource links and sentinel. This is descriptor initialization
evidence, not complete file loading or live crop proof. Actual loaders, complete
widget/GPU palette/alpha presentation, controller input, all display contexts
and physical gameplay remain pending.
Native evidence: `work/analysis/fleet_row_graphics_v162_native.json`.

Saved-ROM verification proves every other V161 component/resource exact,
including ARM9, shared text, all four routes, previous name/treasure graphics
and button prompt. All inherited terminal stages, relocations and changed
records remain exact. Canonical menu/graphics invariants pass. The clean-ROM
xdelta reconstructs the candidate byte-for-byte.
Saved proof: `work/analysis/fleet_row_v162_saved_proof.json`.

## Candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V161 comparison | `a3cf17dd8b434c5c93af39c89fe3623da3f00832a03a59f5993d4aa9126b4835` |
| V162: `out/all_routes_combined_v162_candidate.nds` | `0ece3348fd68b3c3ef9fb8e4104360806bd4cc007aef21d3780e28f9352b1f9c` |
| ARM9, exact V161 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V162 build | `fd42cb33506689537d6536a90e648011704bbef0aad76d44eca0552af002d86f` |
| V162 patch: `out/all_routes_combined_v162_candidate.xdelta`, 765501 bytes | `fdac8a9b3ade1065f9f643f3078d76b409b4001c0be58c4a129feb3a9acd2944` |

Profile: `all-routes-unified-v162`, experimental. The registered builder starts
from the immutable canonical base and reproduces every one of the 440 V161
batches and terminal stages. The additional source-locked experimental batch
is `translations/fleet_row_graphics_v1.json`, bringing the total to **441**.
All accepted layers are baked into the canonical baseline; zero additional
accepted batches are required. The adjacent `.manifest.json` records the full
batch list, changed paths/records, inherited stages and checks.

Compared with V161, **only `/Iseki/dock.pxl` differs**.

Compared with the canonical baseline, fourteen internal paths differ:
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/SLACKIMG.DK4`,
`/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`,
`/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/data/SC0.DK4`,
`/data/SC1.DK4`, `/data/SC2.DK4` and `/data/SC3.DK4`.

Before acceptance, cold-boot without a savestate and test the title, New Game
captain selection/name entry, one established story, town UI, inherited changed
item/Advice/Gallery screens, treasure list and button prompt. Find the actual
fleet-image display contexts and check all five rows with one through five
ships: full text visibility, row alignment, palette/alpha and input behavior.
Explicit user acceptance is required before canonical promotion.

## Full goal remaining

245 COMMON selections / 133 physical owners still need actual consumer/layout
integration. Other ARM9/UI, name/source fidelity, Reports/Sailing Help persistence,
BGM physical audio/input, downloaded items and complete gameplay checks remain.
The historical graphics inventory now has **22** other confirmed Japanese
loose/FLS resources, one remaining matching embedded title copy, the separate
CMMNIMG atlas and unclassified artwork. This is inventory bookkeeping, not
clearance of all in-game screens. Final packaging/progress and GitHub commit/push
remain campaign tasks. On full goal completion, retain the requested note to
revisit older record-based checks.
