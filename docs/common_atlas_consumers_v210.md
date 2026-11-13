# Common atlas readers, source review and market display V210

2026-10-07. The previous turn verified SLACK image-view mappings. This turn adds
native atlas-read/crop evidence, complete source reviews and a normal market visit.
**No ROM bytes changed. V205 remains current; the full graphics goal stays active.**

## Native consumers

The real resource registry and cache are initialized by original game code. Only
SDK filesystem operations are bridged to the exact current ROM. Native code and
source atlases remain exact to clean.

| Resource/path | Native operation | Cases |
|---|---|---:|
| `/GRP/CMMNIMG.000` | Parent read fragment at `02047A28..02047A60`: 3,584 bytes at `512 + index × 3584` | 178 |
| `/_pxl/item.pxl` | Complete reader at `02047864`: 1,024 bytes at `532 + index × 1024` | 218 |
| `/_pxl/itemtrade.pxl` | `02047940` selects source origin `(0,index × 24)` and resolves its full native cache | 124 |
| `/_pxl/item16.pxl` | `02047774` constructs the original 16×16 crop and resolves the complete atlas | 218 |
| `/_pxl/itemtrade16.pxl` | `020478D0` constructs the original 16×16 crop and resolves the complete atlas | 124 |
| Total | | **862** |

Every loaded byte, cache palette/pixel payload, tested crop/source origin and
buffer guard matches. Complete routine cases return with stack/saved registers
intact and all file handles closed. Portrait indices/preceding stack context are
supplied for the parent fragment; its subsequent target-header copy is not run.
The large trade helper selects an origin, leaving the caller's clip extent open;
the compact helpers explicitly produce complete 16×16 extents. These distinctions
are recorded rather than inferred from matching icon dimensions.

## Complete source-art decisions

All **684** cells across the four item/trade atlas variants were inspected on ten
bounded sheets at integer enlargement. Every saved cell includes all source pixels;
whole original files, indices and palettes remain intact. Retain the original goods,
equipment and artifact paintings. Book-cover/scroll markings are physical object
decoration, not a separate UI caption or instruction; do not invent their readings
or titles. Item names/lore supplied by text consumers remain separate.

The native portrait atlas's earlier full 178-cell source review remains applicable
because this exact file is unchanged. V195's full Lil framebuffer match concerns
that `.000` file, not the similarly sized legacy ILNK block.

RGB source sheets alone do not establish alpha or every live composition. The four
legacy CMMNIMG blocks are not equated to these native atlases: their palettes and
indices differ. Main/ARM9-overlay literal searches find `CMMNIMG.000` but no fixed
`CMMNIMG.DK4` filename. This does not rule out generated names or indirect readers,
and does not globally declare the legacy archive unused. Its relationships remain
open and the eleven-block unresolved census is unchanged.

## Normal market visit and visible quantities

Fresh V205 cold boots use normal controller input, without savestates or memory
injection. The first market visit triggers Julio's introduction; the initial run
is retained as dialogue evidence, not trade-icon proof. A second fresh boot advances
that event and reaches the real Deal screen. Frame 19700 was visually reviewed.

Five original 24×24 trade cells (indices 13,14,27,78,86) appear at x=84,116,148,180,212
and y=286. Every full image rectangle fits within the bottom viewport. The observed
quantity strings **3, 5, 8, 7, 5** overlay these images. Their complete original-font
masks, lower-right shadows and underlying image area match, including first/last
digits and blank cells. This checks displayed glyphs, not inventory-value arithmetic.

Source images plus those quantity overlays match **2,855 of 2,880** compared pixels.
The remaining five pixels per icon are tiny white upper-right GUI indicators.
Their observed shapes/locations are saved explicitly; the indicator's source asset
or draw path has not been independently mapped. Therefore **the entire composite
is not claimed exact** and those 25 pixels are not silently excluded. This is no
new artwork change or evidence that an original icon was damaged. That small
indicator mapping and broader scene/alpha/crop checks remain open.

## Artifacts and remaining scope

- `scripts/research_common_atlas_consumers_v210.py` and `work/analysis/common_atlas_consumers_v210/proof.json`.
- `scripts/review_native_item_atlases_v210.py` and the `source_reviews/` inventory/PNGs.
- `scripts/verify_market_icon_composition_v210.py` and `live_market_icon_proof.json`.
- Two cold-boot runs and their input schedules under `work/emulation_v193/common_atlas_consumers_v210/`.

Focused Ruff passes. Four Online screenshot bodies, remaining name consistency,
other raw/embedded/contextual/native consumers and the final combined ROM/patch
and gameplay audit remain in the full goal. No candidate is promoted.
