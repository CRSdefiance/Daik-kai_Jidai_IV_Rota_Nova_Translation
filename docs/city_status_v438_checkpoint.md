# Source-owned city-status localization V438

Experimental candidate:out/all_routes_combined_v438_candidate.nds.
SHA256:b27626ba00b1dba22fbde000afb11ffeb3cb3b20e8de14ccb96ed5200b15d0ff.
Patch SHA256:fb1d1a0ed7127cf3343ff58e7d482803207ef9f4fe48019c202f6654fca3c5eb.
Profile:all-routes-unified-v438. Canonical baseline remains
out/raphael_natural_v2_accepted_base.nds, SHA256
3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
All470 inherited batches, accepted dependencies and V436 stages remain.

## Complete providers with no memory growth

All12 formerly Japanese active status names are English:War,Plague,Famine,Boom,
Slump and Seasoning/Spice/Luxury/Alcohol/Fiber/Dye/Ore Shortage. Normal remains
Normal. The complete13 names require144 bytes and fit within148 explicitly owned
status/fallback bytes:132 at ARM9 offset15633C and16 at1565D0. Ore Shortage uses
the latter block; Normal's fallback aliases its primary name. All table/pointer
owners are pinned. No declared overlay has a status-allocation pointer candidate.
Unowned bytes, fonts, effects and section data remain exact.

Three compact consumers preserve the original long-name fallback. Their generic
Shortage pointers share a complete suffix in Spice Shortage. The helper that
returns a name and length now reports the actual eight-character ASCII length,
instead of the old six-byte Japanese length. No abbreviation or missing terminator.
No file/section/pool/arena size change; all ITCM/DTCM/owned main-pool data remain
byte-exact. No new assembly helper or arena expansion is used.

## Native and actual evidence

All256 full/compact provider cases pass original ABI/input guards. Both direct
compact selector fragments pass all13 states. All26 complete native full/compact
rasters match independent font pixels; the invisible odd-pair guard is included.
All13 actual packed string pointers, including unaligned addresses, paint complete
glyphs. Compact Shortage occupies48 pixels, ending atx104 in the supplied x56
context. These are isolated provider/painter contracts, not complete live variants.

A genuine Copenhagen read-only snapshot contains Valencia in Boom state3; this is
recorded as real world-state evidence only, not a rendered Valencia display.
The fresh V438 normal-input boot produces67 full title/New Game/story/town/HELP
frames pixel-exact to V436 with no callback errors. Only ARM9 differs from V436;
all non-ARM9 components,470 batches and208-topic HELP are preserved. The clean
patch reconstructs the complete ROM exactly. Targeted Ruff passes.

## Remaining scope and handoff

Genuine non-Normal city displays, full detailed status-notice composition and all
caller geometry remain open. Native input/raster checks are not full gameplay or
hardware verification. All18 plaques,69 historical HELP generic matches, legacy/
environment/movie/Gallery/equipment requirements and the full goal remain open.
No canonical promotion. Revisit older record-based checks at actual completion.

ROM, patch and manifest are copied to E and hash-verified. No simulated status
preview is placed in the finalized screenshot archive. User checks:cold boot,
New Game, city/sea information and any naturally occurring War/Plague/Famine/Boom/
Slump/Shortage state. Candidate remains experimental.

Evidence:work/analysis/city_status_v437/native_proof.json,
actual_pointer_raster_proof.json,genuine_state_and_overlay_proof.json and
work/analysis/city_status_release_v438/release_proof.json. Production:
dk4tool/patch/city_status_labels.py. Verifiers:verify_city_status_v437.py and
verify_city_status_release_v438.py.
