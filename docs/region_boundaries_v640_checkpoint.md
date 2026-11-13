# V640: complete shared region-name boundaries and ordinary Area tooltips

## Defect and high-level repair

Tracing the remaining map pages exposed a real inherited string defect: original
region6's current label reads `AmericasMed.`. The legacy fixed-text batch writes
all eight bytes of `Americas` into its eight-byte source slot, consuming its NUL.
The following independent `Med.` label is then read as part of the same C string.
The defect is present in V546,V610,V627,V633 and V636; it is not introduced by the
recent commodity or map-verification work. The ordinary V636 Area tooltip now
reproduces the whole joined label in the paired source run.

The correction handles the complete shared family of eight name owners. Every
name receives independently owned character and NUL bytes; every real pointer
is rebuilt and validated against its expected complete name. Original wording,
including existing UI abbreviations and SE Asia's renderer pad, is retained.
Americas is not shortened to make its old slot fit.

The original80-byte name span is ARM9 offsets14C79C..14C7EC. Complete aligned names
use72 bytes, leaving eight spare bytes without pool, section, startup, arena or
file growth. Four name pointers move. The geometry/metadata of all eight native
records remain byte-exact to clean. Every-byte ARM9 pointer census finds exactly
the eight expected owners; the overlay census finds no alias into the span.

The word at14C7EC is an adjacent integer array's first zero, referenced by original
instruction literal02094588. It is not spare text padding. The repair excludes
that word and preserves the array and its pointer. This distinction prevents a
terminator repair from damaging the original area-selection geometry/order.

`region_name_boundaries` is a registered terminal stage after the complete V636
stack. Its validator rejects a missing terminator, joined name, overlapping owner,
unknown interior reference, wrong source, altered wording or changed geometry.
It validates all eight final pointers, rather than checking only the replacement
bytes. The original historical batch remains unchanged for reproduction.

A bounded audit of85 `dk4-arm9-fixed-text-batch-v1` batches checks7018 records for
the same pattern: an English payload exactly fills a source slot containing NUL,
still matches those bytes in final V636, and has nonzero following data. Americas
is the sole matching lead. This is a specific current exact-capacity census, not
a claim to classify all project strings, aliases, C-string consumers or runtime
text. NUL ownership is separate from the existing paired-glyph guards.

## Registered combined candidate and exact patch

| Item | Identity |
|---|---|
|Profile|`all-routes-unified-v640`|
|Status|Experimental; user cold-boot acceptance pending|
|Canonical base|`out/raphael_natural_v2_accepted_base.nds`|
|Base SHA256|`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`|
|Candidate|`out/all_routes_combined_v640_candidate.nds`|
|Candidate SHA256|`93868a0b250a3b52897225dac48ab29e0b14d1f097208ca9a418208dd29d0b9e`|
|ARM9 SHA256|`54e35ccaf340a40506a98b0bc3fb7b14091eacac3548fe305d8e553922aa8da1`|
|Patch|`out/all_routes_combined_v640_candidate.xdelta`|
|Patch SHA256|`dc9f02f610f6f4156e39b4609175a7e7facbc2bad659c5d391315fd112225738`|
|Patch input|`work/clean.nds`, SHA256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`|

Built with `scripts/build_integrated_release.py`. All470 inherited batches and114
accepted layers remain. Only `/__arm9__.bin` changes from V636, solely within the
owned name span and four reference words. Every other file/component and staged
section remains exact. The manifest retains the same53 changed canonical paths,
all required batches and every existing check. Fresh921 PXL/FLS metadata/palette/
extent checks and57 embedded extent checks pass. The saved clean-ROM patch
reconstructs every candidate byte exactly.

ROM, manifest and patch physically reside under
`E:/Rota Nova translations/Generated/out/`. No canonical promotion or Git push.

## Native and actual gameplay verification

All eight original record getters execute with the corrected real pointers and
read complete independently terminated names. All eight96x16 original-renderer
bitmaps match independent full font masks, including leading/final letters and
unused cells. A corrupt-NUL control is rejected. The actual captured current RAM
also yields every complete name without code/data restaging or substitute objects.

Three terminal DeSmuME runs use cold boot, ordinary inputs, no preloaded battery
save, no savestate and no RAM/ROM display fixture:

1. `region_boundaries_v640_market`,24100 frames:32 unique startup, New Game,
 captain, opening-story, town and Market frames match the established V636
 controls. Inputs are the unchanged V633 Market schedule.
2. `region_boundaries_v640_map`,39200 frames: the established ordinary map path,
 then X selects Area, Right and ordinary touches visit all seven region tooltips.
3. `region_boundaries_v640_map_source`,39200 frames: unchanged V636 receives the
 exact same complete input schedule to reproduce the joined Americas tooltip.

| Frame | Actual tooltip |
|---:|---|
|36400|N. Sea|
|36800|Indian|
|37200|Americas|
|37600|Med.|
|38000|Africa|
|38400|SE Asia|
|38800|E Asia|
|39200|N. Sea repeated|

All eight appearances pass complete actual font masks and whole white backing/
margin checks. Origins are independently derived from original region geometry
on the world map, not selected to fit tested letters. The original blue selected-
area border overlaps blank popup rows in some states; its exact pixels are bound
to the paired unmodified source control and retained. No text glyph is excluded.

For the Americas case, V636 independently passes the complete `AmericasMed.`
font mask, and V640 passes the complete `Americas` mask. Every screen pixel outside
the old tooltip rectangle is unchanged. The shortened backing's former tail is
checked against the actual native map bitmap and retained original blue border,
so the removed suffix leaves no stale glyphs or white backing. Every other region
tooltip's complete two-screen image is exact to V636. The four map-prefix full
screens are also exact to V638.

These are all seven region labels selected on global source page7. They do not
claim actual display coverage for the seven separate regional source pages0–6.
`Global` has a complete native bitmap/provider test; it is not invented as an
eighth selectable Area tooltip.

The native preview sheet and actual old/current Americas pair, plus N. Sea,
Indian and SE Asia full screens, were visually inspected. The complete text is
readable; no missing first/final letters or new clipping was identified in those
views. The other region views receive full automated glyph/backing comparisons;
individual visual review of all full screens is not claimed. Tests do not replace
the user's cold-boot acceptance or full-route/device verification.

## Files, archive and user review

- `dk4tool/patch/region_name_boundaries.py`.
- `translations/region_name_boundaries_v1.json`.
- `scripts/prepare_region_boundaries_v640.py`.
- `scripts/verify_region_boundaries_v640.py`.
- `scripts/record_region_boundaries_v640.py`.
- `work/analysis/region_boundaries_v640/release_proof.json`, native previews,
 bounded legacy census, preservation/patch proofs, source/current input schedules.
- `E:/Rota Nova translations/Screenshots/Test fixtures/V640 Region name boundaries`:
 unmodified captures, reports, tools, proofs and clearly labeled derived sheets.
- Separate ordinary current guide candidates are saved on E; broken V636 control
 screenshots are excluded. No publication approval is inferred.

For user cold-boot review: title/New Game and an established story scene, town/
Market, then World Map→X Area selection and its Americas tooltip. Confirm complete
names and ordinary selection behavior. The candidate remains experimental.

## Preserved remaining scope

All18 original plaque/hint entries remain `fully_completed:false`; all22
historical requirement objects/scopes remain exact. Only the latest compiled
experimental pointer advances to V640. Canonical, V610 verified and other release
pointers remain unchanged. Actual regional source pages, sepia/legacy/raw comic/
title consumers, village cards, miniature/Confirm ordinary contexts, other movie/
material variants, plaque texture approval and final user acceptance remain open.
The preceding V639 turn made progress on the source/native mask lifecycle. The
full graphics goal remains active; older record checks remain due at completion.
