# Market indicator composition review V248

The previous goal turn made concrete progress on V247 plaque artwork and shared
skill formatting. This turn resolves25 unexplained market-icon pixels. V248 is
research evidence; the registered playable ROM remains combined V247. All17
plaques and the Equipped Items hint remain explicitly incomplete in the ongoing
audit, as requested by the user on2026-10-09.

## Actual source and native loading

The original resource registry resolves owner `02313F60` to `/_pxl/__frame.pxl`.
It does not resolve to `__marker.pxl`; nearby vtable metadata is not a filename.
Native registration, cache allocation, resource resolution, whole-image view
construction and virtual copy verify all35,444 bytes from the current ROM.
Only SDK file operations are bridged to the exact ROM. Both source/destination
view guards, complete headers/palettes/indices and caller ABI pass.

The original parent fragment `02085430..02085488` constructs five8×8 views at
`(80+8*n,216)` with palette bank9. The bank is stored in the low16-bit field;
upper bits can remain unspecified and must not be interpreted as another bank.
Every complete source cell and its bank9 palette remain identical to clean.
These cells are Latin digits **1,2,3,4,5**, retained without translation.

The original cargo-widget selection fragment `02085AE4..02085B50` selects view
`type-1` and places it at `(icon_x+20, icon_y-4)`. Five bounded input cases verify
that selection and location. Original view and widget constructors run. The
preceding parent/geometry/type are explicit research inputs, and execution stops
before the virtual GPU call. This is not proof that the current Market scene
dispatches through this particular cargo-widget method.

## Fresh current-ROM display

A fresh normal-control cold boot of exact V247 replays the recorded market visit,
without a savestate, fixture ROM or RAM injection. All captured PNG hashes,
ROM identity and callback status pass. The full final framebuffer is frame19700.

| Goods atlas cell | Quantity | Complete indicator | Indicator ink pixels |
|---|---|---|---|
| 13 | 3 | 4 | 28 |
| 14 | 5 | 4 | 28 |
| 27 | 8 | 5 | 23 |
| 78 | 7 | 5 | 23 |
| 86 | 5 | 4 | 28 |

Each full indicator matches exactly one independently decoded frame cell. All130
source ink pixels are checked, including portions above and right of the goods
rectangle. Their lower strokes predict the five formerly unexplained pixels per
icon; no screenshot-derived coordinate exclusions are used. The native quantity
font, its shadow, original24×24 source image and indicator jointly match all2,880
rectangle pixels. There are zero unexplained pixels in these five rectangles.
The previous2,855/2,880 report remains historical rather than being overwritten.

## Limits and remaining scope

This verifies these five visible icon compositions and indicator lettering. It
does not establish every icon, quantity arithmetic, the gameplay meaning of the
indicator type, all transparent pixels outside the icon rectangles, physical
hardware or the exact current Market widget dispatch. Those scopes remain open.
The eleven unresolved legacy blocks, four Online transcripts, broader embedded/
environmental/native coverage and the user-required continuing plaque audit are
not closed by this result. The full goal remains active.

## Evidence

- `scripts/verify_market_indicator_v248.py` (Ruff passing).
- `work/analysis/market_indicator_v248/proof.json`.
- `work/analysis/market_indicator_v248/live_review.png`.
- `work/emulation_v193/market_indicator_v248/capture_report.json` and final PNG.
- The script reuses the unchanged native resource helper from V229; retaining
  its machine only enables subsequent original-code fragments, without changing
  the factory implementation or source resources.
