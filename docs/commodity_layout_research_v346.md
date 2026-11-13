# Commodity layout research V345–V346

Status: incomplete. No registered release or canonical promotion. The current
registered combined candidate remains V342.

## What the actual captures established

The five specialty crops originally use 72-pixel widths. Compact five-pixel ASCII
tracking permits all 49 newly translated names to fit within 96 pixels. All124
native name getters and98 complete native rasters passed in the verifier before
its actual-screen regression assertion failed.

V345 widened specialty crops at source x108. Every letter of the three supplied
long names appeared, but their final characters also appeared in percentage
widgets: the original percentage sources begin at x180. This disproves the earlier
assumption that source space through x204 was available exclusively to specialties.

The first V346 probe moved specialties below y72. Its actual labels disappeared.
Read-only V345 runtime memory identifies the city bitmap's logical dimensions as
228x72. The separate320x320 limit is not the usable text bitmap geometry. Do not
use the allocation limit as a layout contract.

The second V346 probe kept specialties in their original source rows and moved
three percentage sources into apparently unused cells. All six actual labels
matched their full native font masks, including every first and final character:
China, Silk Cloth, Jade, Black Glacier Sword, North Sea Ambergris, Fire and Ice
Rubies. However, both normal and long-name captures have155 unexpected changed
pixels outside the specialty column, including percentage and date widgets.
The full-screen preservation gate failed. Descriptor non-overlap alone does not
prove those source cells are unused by every consumer.

## Evidence and reproducibility

- `scripts/prepare_commodity_layout_v346.py`: prepares unregistered research ROMs.
- `scripts/verify_commodity_layout_v346.py`: intentionally fails the unresolved
  outside-column preservation assertion; its native getter/raster checks pass.
- `work/analysis/commodity_layout_v346/failed_regression.json`: capture report
  hashes, ROM hashes, exact font masks, and unexpected pixel counts/bounds.
- `work/emulation_v193/commodity_normal_labels_v346_repacked/`: normal names.
- `work/emulation_v193/commodity_long_labels_v346_repacked/`: supplied long names.

Both are targeted cold-boot DeSmuME tests with ordinary game input, no savestate,
and a documented one-byte fourth-captain visibility fixture. Long names replace
three commodity label pointers solely to exercise the actual painter; this is
not normal stock availability, a legitimate Maria unlock, or a complete playthrough.
No heap, runtime pool, backing bitmap dimensions, save flags, or source metadata
are expanded. The source-owned name storage and49 full translations are retained.

## Next work

Trace every consumer of the city backing bitmap, especially the market-share and
date widgets, before selecting safe source cells. Verify all changed-screen pixels
again. Then audit market/cargo/price name contexts and integrate through the
registered builder with all inherited layers and an exact clean-ROM patch.

All18 Assign Sailors/Sailor Info plaques and hint variants remain incomplete.
The low-resolution Online images remain exempt at the user's request. The full
graphics goal remains active. At actual completion, revisit older record-based checks.
