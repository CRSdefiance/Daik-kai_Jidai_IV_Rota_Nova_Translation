# Combined V172: translated embedded shared-menu copy

2026-10-04. **Experimental** V172 synchronizes the accepted English shared-menu
marker atlas into CMMNIMG's exact original-matching left half. All V171 translations,
22 frame labels/units, code and repair stages remain exact. The full goal is incomplete.

## Change and evidence

The clean Japanese `/_pxl/__marker.pxl` matches every original CMMNIMG left-half
pixel index. The canonical loose marker is already accepted English, but the
embedded left half still had Japanese. This batch reuses the complete canonical
English image indices exactly, including the 24 major captions: Functions, Crew
Setup, Deck View, Info, Route Map, Items, Redo, Confirm, Cancel, Report, Delegate,
Port, Attack, Classic, Orders, Sold, Local, Cargo, Disc., Buy, Sell, Temp Store,
Issued and Spoils. It introduces no new wording or font rasterization.

Only **4312 pixel indices** differ from V171. Every unchanged source ornament,
border, zodiac icon and male/female symbol remains exact. Male/female kanji still
need localization; the twelve remaining historical loose resources are unchanged
as a backlog count. Other embedded title/artwork and unclassified assets remain.

Two source-locked regions now share CMMNIMG block 5: marker at x=0 and frame at
x=256. The builder merges their disjoint packed-byte rectangles and rejects any
partial/full overlap, inconsistent block geometry or duplicate record ID. Each
batch remains locked against canonical original bytes. The full previous V171 ROM
reproduces **byte for byte** with this builder before V172 is built. Existing
single-region and different-block sync behavior remains exact.

**150 existing graphics tests and 16 new tests pass**, across the recorded focused
runs. The new cases cover both atlas halves, first/final caption edge ink, overlap,
geometry, source/reference hashes, single-sync compatibility, order independence,
header/other-block preservation and complete inherited profile stages. Builder,
new script and tests pass Ruff.

The saved ROM verifier checks the complete canonical English marker, every V171
frame pixel, all 83 palette banks, block headers/flags, unrelated archive blocks,
extent, prior resources/components/record IDs, full batch stack and relocations.
The clean-ROM xdelta reconstructs the candidate exactly. Bank-zero previews were
reviewed. Actual native resource loading, parent consumers/crops, palette selection,
GPU alpha, input and physical gameplay remain unverified; no global screen guarantee
or canonical acceptance is claimed.

Evidence:

- `work/qa/marker_v172/review.png` and `evidence.json`
- `work/analysis/v172_graphics_tests.log` and `v172_marker_tests.log`
- `work/analysis/v171_region_builder_reproduction.json`
- `work/analysis/marker_v172_saved_proof.json`
- `scripts/marker_cmmnimg_v172.py`
- `tests/test_marker_cmmnimg.py`

## Exact candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out\raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Prior V171 / exact reproduction | `7a51d00eae25b50c9b914b6e3a26cff6ca7b0940b445f67107f7328c60759888` |
| Candidate: `out\all_routes_combined_v172_candidate.nds` | `051ffe4725434a9dcff1d1d1b34be72c81fc8d1d8cde76d7d59bac92ce0fdc92` |
| ARM9, unchanged V171 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Release registry | `ac9d2c5f3ef91efca2e7a714024c669b72be6de5c67f15194c10cf405842e979` |
| Builder | `97391ce61446ba585273e2a6deb5ff21f534ef7e3daf342cfff57a0d0becc368` |
| Patch: `out\all_routes_combined_v172_candidate.xdelta`, 780501 bytes | `4e85b619ed93d057c6bbbf0535659b882aeed22b14abc0fdad1a7c9b5290964e` |

Profile **all-routes-unified-v172** is experimental. **453 experimental batches**:
all 452 V171 batches unchanged, plus `translations/marker_cmmnimg_sync_v1.json`.
Accepted layers are baked into immutable canonical; zero additional accepted batches
are required. Every inherited terminal stage is retained. Adjacent
`out/all_routes_combined_v172_candidate.manifest.json` names baseline/registry,
complete batch list, changed paths/record IDs, relocations and checks.

Against V171, **only `/GRP/CMMNIMG.DK4` differs**. The 25 canonical changed paths
retain membership:

`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/CMMNIMG.DK4`, `/GRP/SLACKIMG.DK4`, `/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/__frame.pxl`, `/_pxl/deck04.pxl`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`, `/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`, `/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`, `/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`, `/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`, `/evstill/evstill208.pxl`, `/evstill/evstill209.pxl`.

Before acceptance, cold-boot without savestates: title/New Game, captain/name entry,
an established story, town UI and inherited repaired screens; inspect shared-menu,
trade, cargo and command captions in actual contexts, complete first/final letters,
bounds/colors/alpha, all 22 frame labels and controller behavior. Actual embedded
consumer reachability still needs checking. Explicit user acceptance is required
before canonical promotion.

## Full goal remaining

COMMON: 245 Japanese selections / 133 physical owners needing actual consumer/layout
integration. ARM9/UI classification, names/source fidelity, Reports/Sailing Help
persistence, BGM audio/input, downloaded states and full gameplay remain. Twelve
historical loose graphics resources retain Japanese; marker gender icons, title/
online/FLS art, embedded title copy and unclassified art need work. Image 207's
clipped source mark remains unresolved. Final canonical acceptance, packaging/progress,
GitHub commit/push remain. On full goal completion, revisit older record-based checks
as requested.
