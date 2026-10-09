# Native Online captions and remaining COMMON consumers

## Proven caption path

Clean ARM9 `0x10434C–0x104358` selects a 12-byte descriptor at `0x12F88C`
using the menu index and calls `0x021045B4`. Descriptor fields are page-data
pointer, caption-pointer-table pointer, and page count. They are data, not code.
The earlier disassembly of data at `0x12F890` is not caller evidence.

| Descriptor offset | Caption table | Count | Caption string offsets |
| --- | --- | --- | --- |
| `0x12F88C` | `0x16D9A0` | 4 | `16DAC4`, `16DA70`, `16DA10`, `16DA8C` |
| `0x12F898` | `0x16D9B0` | 4 | `16DB44`, `16DAE4`, `16DB68`, `16DB8C` |
| `0x12F8A4` | `0x16D908` | 2 | `16DBB0`, `16DB04` |
| `0x12F8B0` | `0x16D974` | 3 | `16DBD4`, `16DB24`, `16DAA8` |

`0x104CD8–0x104D30` reads descriptor+4, selects the caption pointer, measures
byte length through `0x020CED28`, multiplies by six and centers at x=128.
It passes y=12 and style 15 to `0x02105694`. That helper constructs a local
context through `0x020D5160`, draws through `0x020D5404`, and destroys it.
No COMMON native ID is fetched in this caption path.

The source-locked preparer checks all four descriptor tables, all 13 clean
caption strings, the canonical and V132 English slots, the unchanged consumer
code and the exact native ASCII font. Its diagnostic panels use six-pixel
advance and the proven center; they are not gameplay screenshots.

## Three source-fidelity repairs in V133

| Source | Previous English | Revised English |
| --- | --- | --- |
| 様々な人々との人間ドラマ | People shape your story. | A drama of diverse lives |
| 勅命を受け、さらなる冒険へ | Orders lead to adventure! | Royal orders, new horizons |
| 多彩な交易品を売買してひと儲け！ | Trade goods and make a fortune! | Trade varied goods for a profit! |

“New horizons” localizes further adventures in promotional copy. Royal
authority, diversity and variety are retained; “a profit” avoids adding the
stronger claim of a fortune. The replacements occupy 25/25, 27/27 and 33/33
bytes including NUL, respectively. All 13 diagnostic captions were visually
reviewed, including first and last glyphs, and fit the 256-pixel panel.

The integrated builder reconstructs the V119 input stack plus this fixed-text
batch, then applies the inherited complete V132 COMMON transform with exact
updated ARM9 input/output hashes. The input reconstruction is an experimental
transform input, not a new baseline. `verify_online_caption_fidelity.py`
proves the saved V133 changes exactly the three slots over V132; all ROM files
and all 3,668 native COMMON selections otherwise remain byte-exact.

Evidence: `work/qa/online_caption_fidelity/report.json`, `sheet.png`,
`work/analysis/online_caption_v133_input_proof.json`,
`work/analysis/online_caption_v133_saved_proof.json`. Cold-boot caption rendering
and navigation remain pending. No accepted layer or baseline was promoted.

## Caller inventory coverage and remaining classification

Current extended coverage is documented in
`docs/native_common_extended_consumer_inventory.md`: 619 candidates, including
92 actor-variant table-wrapper calls, ARM register tails and potential Thumb
calls. Twenty-two focused tests pass. The following direct-call inventory is
the earlier checkpoint; absence of promotional IDs remains insufficient to
classify their consumers or prove them unused.

The first direct-call scan covered the loader/accessor only (49 calls). Five
source-hash-locked varargs wrappers now extend it to 523 direct ARM calls,
419 locally resolved native IDs and 104 unresolved values. Two actor-context
wrappers take the native ID in r1; three general presentation wrappers take
it in r0. The source disassembly proves their saved-register stack arguments
are passed to the native accessor before presentation.

Seven tests cover signed BL targets, rejection of B/BLX, constant propagation,
conditional invalidation, call clobbers, preserved registers, incoming-value
uncertainty and wrapper register declarations. The scan still does not cover
indirect/Thumb calls or recover unknown incoming registers, stack values and
tables. Data can look like ARM instructions. No resolved call currently names
promotional IDs 3289–3319 or scene/artwork/name IDs 3393–3606; **this does not
prove either group unused**.

Long COMMON promotional bodies, short raster Online50–62 cards, and these
native ARM9 captions are distinct source texts. The caption mapping does not
authorize shortening the long bodies, applying a four-line dialogue layout
to them, or claiming their consumer has been classified. Likewise, the 214
scene/artwork/name labels still require a consumer or resource-use mapping.

Additional research: `work/analysis/online_descriptor_full_consumer.txt`,
`online_caption_and_common_wrapper_types.txt`,
`native_common_arm_calls_wrappers_clean.json`, and
`remaining_common_base_arithmetic_candidates.txt`.

## V189 actual screenshot resource registration and page selection

The native static initializer at `0x02111A90` now executes fully with its original
filenames/global owners; all 13 actual page tables are mapped. Online24/27/31/33
are reachable selections, with the screenshot constructor receiving full 256x192
bounds at origin zero. See [V189 checkpoint](all_routes_unified_v189_checkpoint.md)
and `work/analysis/online_resource_pages_v189.json`. The earlier supplied-owner
crop proof was insufficient for these relationships. Filesystem loading, navigation,
GPU/layer/palette composition and live readability still require verification.

## V189 scoped native loader/cache with explicit SDK I/O bridge

[Native loader evidence](online_native_loader_v189.md) now covers individually
invoked real-owner image views across all 23 page screenshots: 27 native resolutions,
20 cache eviction cases and 168 byte-exact resident-image checks. Registration,
allocation/compaction/eviction/cache lookup execute native ARM code. Only SDK
filesystem open/read/close are bridged to exact candidate files. Hardware loading,
native pixel/GPU/layer/palette/alpha/input/live readability and gameplay are still
unverified; the bridge is not hidden or presented as physical gameplay evidence.
