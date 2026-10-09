# Native archive reader and raw thumbnail research V191

## V202 follow-up: actual captain display owner established

The extended native parent now proves all four persistent field copies. A complete
native cache load on each actual owner supplies the loose PXL header/palette/pixels,
with zero reads from the legacy buffer in the tested path. Three real cold-boot
portraits match all 42,432 pixels; all four complete source paintings were reviewed.
The legacy buffers' own palette/other consumers and the fourth live crop remain
pending; they are not declared unused globally. See
[current evidence and limits](native_captain_portrait_binding_v202.md).

2026-10-05. Graphics goal active/incomplete. V191 names research; the latest
combined candidate is V189. No ROM, patch, translated artwork or profile changed.

## Native archive read evidence

The exact V189 candidate passes unchanged native archive constructors, filename
selection, block-count/directory-offset reads, seek/read/copy and close logic.
All 57 blocks in the six GRP ILNK archives were reconstructed through 223 native
read chunks: **11,814,968 bytes**, including every translated embedded region.
All complete block hashes, buffer guards, complete routine returns and saved
register/stack ABI checks pass. All SDK bridge handles are closed.

Only SDK file operations are bridged to the exact candidate filesystem:

| SDK operation | Address |
| --- | --- |
| Open | `020DED50` |
| Read | `020DEBDC` |
| Absolute seek | `020DEB70` |
| Close | `020DED08` |

Archive offset parsing and native stream state are not substituted. Generic block
tests use controlled chunk buffers and valid indices/ranges; this does not claim
invalid-input protection or native allocation safety. This is software integration
evidence with an explicit SDK I/O bridge, not physical NitroFS/OS or GPU proof.

## Actual raw portrait parent segment

The unchanged parent segment `0209EDD8–0209EE18` executes the real block selection
and `0204704C` archive helper, then constructs image views through `020D3D30`.
The complete native resource initializer executes first (2,864 distinct instructions),
so the owner table is initialized by game code instead of a supplied owner list.

The parent selects SLACKIMG blocks 14–17 and writes each exact 14,144-byte block
to its actual buffer literal, `02233040`. It constructs views on these registered
owners with extent 104×136:

| Raw block | Actual owner | Original registered filename |
| --- | --- | --- |
| 14 | `0231395C` | `_pxl/personbustup00.pxl` |
| 15 | `02313948` | `_pxl/personbustup01.pxl` |
| 16 | `02313934` | `_pxl/personbustup02.pxl` |
| 17 | `02313920` | `_pxl/personbustup03.pxl` |

The segment reaches its real continuation with stack/register context preserved;
raw-buffer and view canaries pass. Its preceding register/stack context is supplied
from the preceding MOV/STR instructions. The full parent UI constructor is not
executed. This proves the observed segment's block selection, complete byte reads,
registered owner binding and view extents. It does **not** prove that the raw buffer
provides the displayed pixels or palette: the views bind loose PXL owners, and the
raw-to-display relationship still needs tracing. No palette candidate is adopted
from visual resemblance alone.

## Nineteen complete landmark thumbnail interpretations

SLACKIMG block18 begins with 512 bytes whose 256 BGR555 words have clear high bits.
The remaining 58,368 bytes partition into 19 coherent 64×48 landmark/building images.
The palette prefix, every index byte, all 19 saved PNGs and the complete source
block roundtrip are pinned. The block is unchanged in V189.

All 19 complete images were inspected enlarged on the review sheet. No caption or
instruction was observed. Retain the original landmark/architectural art; do not
invent tiny plaque readings, exact landmark names or city assignments. Original
small architectural details remain indistinct. The 19-image partition and palette
interpretation are coherent storage observations, not declared native metadata;
native geometry, bank/alpha selection and actual use remain unproved. Historical
unclassified counts and localization counts are unchanged.

## Artifacts and remaining gates

- `scripts/research_native_archive_io_v191.py`
- `scripts/research_raw_thumbnails_v191.py`
- `work/analysis/native_archive_io_v191.json`
- `work/analysis/raw_thumbnails_v191.json`
- `work/qa/raw_palette_prefix_v191/thumbnail_review.png`
- `work/qa/embedded_masks_v190/palette_candidates.png` (unadopted comparisons)

Both scripts pass Ruff. Native archive read/offset evidence is stronger than the
earlier storage-only checks, but pixel decoding, palette/alpha, actual rendered
crops, whole UI construction, input/gameplay and cold-boot review remain open.
Four Online screenshot transcripts and other raw encoding/source-fidelity work
also remain. The full graphics goal is not complete.
