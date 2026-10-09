# Combined English patch: Unified V245

Experimental combined candidate with the full cumulative translation/graphics
stack. The graphics goal is still active; this package does not declare the game
fully localized or promote the accepted baseline.

## Apply the patch

Use your own unmodified Japanese ROM with SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
Keep `release_manifest.json` beside `translation.xdelta`, then run:

```powershell
python -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v245/translation.xdelta --out out/all_routes_combined_v245_candidate.nds
```

Expected reconstructed ROM SHA-256:
`57b7f42f04f60c5e6f06d03ebe91eacbaff04204dde27967fd3e3b205634d3c4`.
Patch SHA-256:
`3503984bbfcc34df11ccca3ecca4b3db66f2f8da41508f2c2c5562161c3fbc68`.
The exact clean-ROM patch reconstruction has been verified. Full ROMs and RAM
dumps are excluded under the repository's ROM-free policy.

## Latest changes and preservation

Six inherited menu bitmap captions are repaired with complete native-font English,
including removal of original Japanese lower strokes. Both marker copies match;
all previous captions, gender symbols,83 palette banks, headers, borders and other
archive blocks remain intact. One concealed background pixel per plate is inferred
from the same original diagonal stripe; it is not claimed as recovered source art.

Only `/_pxl/__marker.pxl` and `/GRP/CMMNIMG.DK4` differ from V241. ARM9, ARM7 and
every other internal file remain identical. All467 batches and terminal stages
are retained through two explicit batch supersessions.

Eight live captions, twelve earlier complete frames and six real cached marker
views pass verification. The selected menu screenshots remain unchanged from
V241, confirming no visible regression in the observed DS path. These scoped
checks do not clear every alternate consumer, palette state or physical device.

## Build identity and evidence

Profile: `all-routes-unified-v245`, experimental.
Immutable build parent: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
The clean ROM is the patch input; the immutable accepted parent is the build input.

`build_manifest.json` preserves the exact original build registry/hash, batch list,
changed paths/records and stage checks. The JSON files are stored without Git line
ending conversion to preserve their byte hashes.

Included evidence:

- `verification/saved_proof.json`: preservation, glyphs and exact patch checks.
- `verification/live_proof.json`: cold-boot captions, earlier frames and native views.
- `verification/repair_plan.json`: source bounds and background reconstruction.
- `verification/repair_preview.png`: before/after stored caption comparison.
- `verification/selected_menu.png`: actual V245 selected menu capture.

See the [full V245 checkpoint](../../docs/all_routes_unified_v245_checkpoint.md),
[progress](../../docs/translation_progress.md) and
[settled naming policy](../../docs/glossary.md).
Four Online bodies, remaining native/embedded/environmental coverage, name
consistency and full gameplay verification remain open. Research scripts and
unintegrated naming manuscripts are preserved in the repository and explicitly
distinguished from the compiled candidate.

Cold-boot test the title, captain selection/openings, town and the menu entries.
For the observed path, reach Amsterdam in Lil's route, then open X/Menu.
Do not use old savestates for candidate acceptance. User acceptance remains pending.
