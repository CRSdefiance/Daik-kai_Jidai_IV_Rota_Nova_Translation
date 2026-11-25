# Native captain portrait binding, V202 research

## V203 follow-up

The fourth captain portrait now matches all 14,144 native pixels through an explicit
one-instruction-byte selection fixture. All four static portrait crops total
56,576 exact pixels. Maria's complete fields and actual-player default names also
pass. This does not establish a legitimate unlock or classify the legacy palettes.
See [V203 scope and proof](maria_native_widgets_v203.md); pending statements below
describe the V202 checkpoint.

2026-10-07. The previous goal turn made progress on full-name capacity handling,
preview review and faithful English corrections. This turn investigates the
embedded portrait buffers and verifies the actual displayed portrait resources.
**No ROM, patch, runtime code or artwork changed. V190 remains the latest registered
candidate, and the full graphics goal is active.**

## Actual constructor and display owner

The unchanged native parent segment `0209EDD8–0209EE80` reads SLACKIMG block
`14 + character index` into its literal buffer `02233040`, constructs a native
image view and copies its data fields into a 44-byte persistent span. The upper
halfword of the 16-bit flags slot remains untouched; the test deliberately seeds
both sides and checks that preservation. All four complete field copies,
declared 104×136 extents, raw-buffer/source bytes, object
canaries and unowned object bytes pass. The actual resource initializer supplies
the owner registry; the owner list is not substituted.

| SLACKIMG block | Actual initialized owner | Selected resource | Native extent | Different embedded/loose indices |
|---|---|---|---|---:|
| 14 | `0231395C` | `/_pxl/personbustup00.pxl` | 104×136 | 11,759 |
| 15 | `02313948` | `/_pxl/personbustup01.pxl` | 104×136 | 10,712 |
| 16 | `02313934` | `/_pxl/personbustup02.pxl` | 104×136 | 11,313 |
| 17 | `02313920` | `/_pxl/personbustup03.pxl` | 104×136 | 9,254 |

A separately constructed native view on each proven owner resolves through the
actual game cache/loader. All four complete PXL files, including their 512-byte
palettes, headers and 14,144 index bytes, match the ROM exactly. Their cache pointers
remain inside the real native pool, and all SDK handles close. Only SDK filesystem
open/read/absolute seek/close operations are bridged to the exact ROM resources;
the parent, view construction, owner selection, cache and loader code execute
unchanged ARM instructions.

A native memory-read hook observes **zero reads** from the 14,144-byte legacy
buffer during these tested constructor/field-copy/cache paths. The buffer is read
from the archive but does not supply the palette or pixels to this tested display
path. The actual displayed resource is the loose PXL. Its index stream is not an
exact copy of the embedded buffer. A visually plausible palette for that buffer
must not be treated as the game's displayed palette.

This does not prove that blocks 14–17 are unused everywhere. The preceding parent
register/stack/object context is supplied, the entire UI constructor is not run,
and other consumers of the shared scratch buffer remain outside this test. Retain
both archive and loose resources. The eleven-unresolved-block storage census is
unchanged; the legacy buffers' own palette/other-consumer interpretation remains
open even though this particular display relationship is now established.

## Complete displayed pixels and source review

Three actual cold-boot captain-selection/confirmation captures match their entire
104×136 PXL images at native bounds **[76, 28, 180, 164]**:

| Portrait | Captured run | Complete exact five-bit pixels |
|---|---|---:|
| Rafael | V201 research smoke, frame 1500 | 14,144 |
| Hodram | V198 research widgets, frame 2100 | 14,144 |
| Lil | Registered V190 Lil cold boot, frame 2100 | 14,144 |
| Total | | 42,432 |

Each saved capture hash, capture ROM hash and exact portrait resource equality
against V190 is checked. Every edge and background pixel is included. These are
static native display crops; all temporal/alpha states and physical devices are
not inferred. The fourth portrait passes native owner/loading proof and full
source review, but its live display remains pending.

All four complete PXL portraits were reviewed on a native integer-scale sheet.
They are character paintings without written UI captions, names or instructions.
**Retain the original artwork.** Costume embroidery and painted ornament are part
of the depiction; do not invent readings or replace decorative details. Written
captain names and biographies sit outside these images and retain their separate
localization/formatting gates. All four source images, palettes and dimensions
remain exact to the immutable canonical baseline.

## Reproducible evidence and remaining scope

- `scripts/research_portrait_resource_binding_v202.py`
- `scripts/verify_portrait_native_pixels_v202.py`
- `work/analysis/portrait_binding_v202/native_resource_binding.json`
- `work/analysis/portrait_binding_v202/native_portrait_pixels.json`
- `work/qa/portrait_binding_v202/actual_PXL_owners_review.png` and four full images.

Both scripts pass focused Ruff. No new playable build or promotion is implied.
Continue the fourth live portrait, legacy palette/other-consumer questions, four
unfinished Online bodies, all other archive/contextual/native/gameplay work,
confirmed-name/artwork consistency and registered combined ROM/patch integration.
At eventual goal completion, revisit the older record-based checks as requested.
