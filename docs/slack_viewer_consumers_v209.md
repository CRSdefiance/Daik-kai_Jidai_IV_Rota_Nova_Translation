# SLACK image-view consumers V209

2026-10-07. Previous goal turn: progress on sky texture geometry and complete source
reviews. Current turn: all native SLACK image-view slots, actual cache loads and
caller mapping. **No release bytes changed; V205 remains current and goal active.**

## Actual image-view helper

The real resource initializer constructs all owners. The unchanged helper at
`020470B4` selects its owner, obtains the actual loaded header, calculates the
width from the native pixel depth, constructs a source view, invokes the
destination's original virtual copy method and returns. A genuine native
destination constructor is used; no owner, header, cache pointer, virtual method
or dimensions are substituted.

Every valid slot 0–20 executes that complete helper and native cache resolution.
All 21 view extents/owners, complete PXL headers/palettes/pixels, buffer guards,
stack/saved-register returns and file handles pass. Only SDK filesystem
open/read/seek/close is bridged to the exact ROM's resources. There are no reads
from the legacy shared archive buffer in these helper/cache paths.

| Slots | Actual loose resources | Native extent |
|---|---|---|
| 0–10 | `/_pxl/slackimg00.pxl` through `slackimg10.pxl` | 128×160 |
| 11 | `/_pxl/slackimg11.pxl` | 256×192 |
| 12 | `/_pxl/slackimg12.pxl` | 44×60 |
| 13–19 | **the same `/_pxl/slackimg12.pxl` owner** | **44×60** |
| 20 | `/_pxl/slackimg20.pxl` | 156×24 |

The small shared sprite contains the already translated Name/Middle/Last/Company/
Birth labels. Slot 20 contains the existing English “Press a button!” graphic.
All fourteen unique full source images were reviewed. Creature paintings and
backgrounds stay original; existing English label/button artwork is preserved.

Slots 13–19 do **not** select their same-numbered raw archive blocks through this
helper. In particular, calling slot 19 is not evidence of a 320×240 comic display;
it selects the name-label sprite. Do not manufacture a gallery fixture by forcing
this helper to display the raw comic payload and present it as the original viewer.
This routine is a general image-view helper, not an identified interactive comic
Gallery implementation.

## Caller census, including the overlay

All `MainCodeFile` sections and the one declared ARM9 overlay are scanned for
direct aligned ARM BL, direct Thumb BL/BLX and literal pointers to both SLACK
helpers. The overlay is original and unchanged, at `01FFA000`, with 6,208 code/data
bytes and 32 BSS bytes. No additional helper calls or literal pointers occur there.

| Direct call | Target | Observed caller context |
|---|---|---|
| `02028F34` | `020470B4` | Supplied parent image index from object +8 |
| `020640EC` | `020470B4` | Explicit image-view slot 11 |
| `0209EDE8` | `0204704C` | Captain creation selects archive blocks 14–17 |

No direct Thumb calls or literal function-pointer references to these helpers
are found in the scanned units. The captain raw-read/display distinction was
already proved in V202: its displayed portraits bind separate loose PXL owners.
The scan does not rule out generated filenames or computed/indirect branches.
It is not a global claim that raw comics, thumbnails or portraits are unused.

## Consequence for remaining work

The raw comic translations remain integrated in SLACKIMG block 19. Existing
source reviews, faithful localization and source-preservation evidence still
apply; this investigation supplies no actual raw-comic GPU crop or readability
proof. Alternate raw consumers remain to identify. The eleven unresolved ILNK
blocks are not silently removed from the census on the basis of a negative caller
search or this helper's fallback behavior.

Continue other raw/native consumers and confirmed-name consistency, four Online
screenshot bodies, remaining native/gameplay checks and the final combined
ROM/patch audit. No full-goal completion or candidate acceptance is implied.

Script: `scripts/research_slack_viewer_consumers_v209.py` (Ruff passing).
Evidence: `work/analysis/slack_consumers_v209/native_viewer_slot_proof.json`.
Full source review sheet: `work/analysis/slack_consumers_v209/loose_resource_sheet.png`.
