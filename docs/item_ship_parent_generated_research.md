# Item ship owners, parent positions and generated maps

This historical research was integrated into experimental V159. The canonical
baseline was not promoted. Fresh role-eligibility and inherited-release evidence,
candidate/patch identities and remaining checks are in the
[V159 checkpoint](all_routes_unified_v159_checkpoint.md). The full goal is incomplete.

## Actual ship owners

280 native raster cases pass on the cache-maintained ARM9 target
`edb1032dd92bfbe0c73f18ffdcae71f3b78108bab4ed7546f8b8d3fada739663`.
All 154 ship metadata initializers execute for each case. The figurehead mapping,
active-ship search, equipment getter, classification and native name virtual
execute without name/ownership callbacks. The observed kind3/index must match
the selected owner before rendering.

The cases cover all 104 fixed ship names in both pixel formats (208 cases), plus
editable slots0/49 at every name length1–18 in both formats (72 cases). Full
names fit their native nineteen-byte storage fields. All owner label/name
characters, independent pixels, bounds and nonoverlap pass; nine panels were
visually reviewed. Existing shorthand and name fidelity remain separate audits.
Outer table/vtable initialization, equipment and editable status/class/name
are controlled inputs. Artwork and physical display/input are not verified.

## Actual counter allocation

Native 02044F50 selects its header through literal020451DC, pointing to
**022BD7D8**, not the previously inferred nearby022BD7EC. Full shared-header
initialization020DD0C and actual bitmap construction020D4524, view020D3AFC and
overlay clear020D393C→01FFB2DC execute. The backing image is four-bit256×92;
the selected counter view is144×36. Clearing preserves every neighboring row,
column and guard byte. This connects the earlier counter glyph proof to its
real storage; upstream acquired-count state and full physical parent remain
unverified.

## Repair the actual parent, not only the local bitmap

The complete native0204D490 parent executes seven020CFC14→020D4170→01FF92D8
crop requests. The old category/effect and owner rows were240 pixels wide at
screen x56, ending at296. The new full English effect value at localx218
would therefore appear at screenx274, outside the256-pixel screen. The earlier
local raster proofs did not establish these final positions.

Four descriptor position fields now place those two rows atx8/y64 andx8/y80,
below the reserved icon area. Their widths, source crops, item name, title and
paragraph positions are unchanged. Restoring those four fields reproduces the
old source exactly; only four actual bytes differ.

The parent-repaired target is
`d5f49394f4bf6dad6647226b6bcf0f505e5a87bff75100ac486f398c857c92fc`.
All seven actual native crop vectors fit. Eight fresh panels cover maximum
category/role/effect/price, longest real crew/ship names, editable-name limits,
real paragraphs and a promotional default. Every complete glyph cell and pixel
survives independent composition at the native requested positions without
overlap, clipping or icon intrusion. All eight panels were reviewed. New-target
native startup/cache/ARM7 and counter-allocation checks pass;91 focused tests
and Ruff pass.

The zero ancestor origin/layer, artwork, border/background, parent state update
and physical GPU/controller remain explicit contracts. The independently
composed text preview is not a gameplay screenshot.

## Generated maps extend beyond the logical counter total

The complete native02102C24 initializer chooses five distinct items from ten
defaults and creates four map names for each selected item. Native RNG,
uniqueness checks, metadata copying, strcpy and sprintf execute without lookup
callbacks.37 seed cases check1110 complete names; maximum length23 fits the
31-byte content capacity. All ten source names and four templates are covered;
this is not all possible random sequences or downloaded-save states.

The displayed total198 excludes the twenty generated maps. Native item slots
still span0–217. The preceding private advice table covered only0–197; generated
maps fell back to a single ordinary COMMON string. Feeding that string into
the private multi-line helper read bytes after its terminator as additional
lines. This defect was reproduced at index198 on the parent research target.
No playable candidate contains this private helper yet.

The new source-locked repair extends the advice projection to all218 actual
slots. It appends one shared, double-terminated presentation of the existing
words, `Map fragment. Collect all four.`, and a218-pointer table. Only the range
comparison and table literal change in the prior payload. All198 existing
compiled paragraphs, full labels, helpers and repaired parent geometry remain
exact. COMMON is unchanged. The cache wrapper/copy extent and native main-arena
reservation are rebuilt for the appended data.

The new target is
`642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf`.
320 fresh generated-map raster cases cover every generated index in both item
screens and pixel formats, using four seeds that cover all ten base names and
all four templates. Every complete name and description glyph, independent
pixel, field bound and main-screen parent crop passes. Twenty additional static/
default raster regressions preserve the previous behavior. All 218 native item
metadata initializers and 257 lookup ABI cases pass.

The new payload reserves 20,576 bytes through the actual main-arena initializer.
Native startup preserves the complete payload, caller registers/stack and ARM7
ownership. The SDK selects every staged code line; 643 copied pool lines and
the final drain pass the explicit stale-cache model. The actual counter view/
clear and seven parent requests still pass. All ten generated-map panels were
reviewed, including the longest 23-character name on both screens. All 99 focused
tests and changed-file Ruff checks pass. The regressions reproduce the prior
extra-continuation defect and reject a missing first description character.

## Evidence and remaining gates

- `work/analysis/item_ship_owners_native_proof.json`
- `work/analysis/item_counter_canvas_native_proof.json`
- `work/analysis/item_parent_layout_native_proof.json`
- `work/analysis/promotional_item_full_initialization_proof.json`
- `work/analysis/generated_item_advice_plan.json`
- `work/analysis/generated_item_advice_native_proof.json`
- `work/qa/item_ship_owners_native/native_sheet.png`
- `work/qa/item_parent_layout_native/native_sheet.png`
- `work/qa/generated_item_advice_native/native_sheet.png`

Older2090/52/456/280 raster proofs retain their actual target hashes. Preservation
of relevant bytes is not represented as fresh execution on a later whole-image
hash. The34 local visible label formatting gates are inherited; Use remains
nonvisible and uncredited. All-label fidelity and broader global UI inventory
continue separately.

Finish role-dependent equipment eligibility, downloaded states, physical art/
parent/input checks, inherited release refresh and complete named-profile ROM/
manifest/patch integration. Explicit physical cold-boot acceptance is required
for canonical promotion under the repository build-continuity protocol. No
commit or push is claimed. Revisit older record-based checks after the full goal
is complete.
