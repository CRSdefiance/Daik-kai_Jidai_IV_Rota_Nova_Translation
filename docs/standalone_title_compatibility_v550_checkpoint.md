# V550 standalone resource and title engine compatibility

The previous turn verified all8 native village-card fixture displays. This turn
adds engine compatibility evidence for the4 remaining standalone resources and
native compositing tests for2 title images. V546 remains unchanged. No production
ROM, patch, translation, registry/profile or source artwork is changed.

## Four complete original-engine file/view tests

| File | Source extent | Complete bytes |
|---|---|---:|
|`/_pxl/copyright.pxl`|256x16|4628|
|`/_pxl/logo.pxl`|256x192|49684|
|`/_pxl/ship_eurL.pxl`|312x246|77284|
|`/_pxl/startmenu0.pxl`|256x192|49684|

All181280 bytes load exactly through the source-original resource cache routines
and virtual whole-view copy. Original startup/cache initialization and the base
resource constructor execute. The derived class tag is obtained from a genuine
originally constructed registered window resource; the4 diagnostic filename fields
and resource owners are explicitly supplied contracts. File contents, native
cache results, PXL headers, palettes and indices are not preloaded or invented.
Only SDK filesystem operations are bridged to exact current ROM files.

Full calls retain their stack/saved-register ABI, source/destination view guards,
owner guards and supplied filename pointers. Zero optional crop dimensions are
lazy full-image contracts, not proof of original scene bounds. These tests do not
replace V509's656/660 original loading-consumer census with a660/660 claim: the
4 original consumers still have not been identified.

## Two native GPU compatibility tests

Two research-only copies replace the25-byte original filename-format data span
at02134BC8 with an explicit standalone title path. Every ARM instruction, section
extent, other byte and original route instruction/operand/prose/file remains
exact to V546. Original event-still file loading and drawing then display the
unaltered title asset in Rafael's opening scene as a diagnostic input. This is a
borrowed original widget, not proof that the normal title scene uses either file.
Each fixture has a provenance manifest and is never a production release.

Both captures cold-boot the real DeSmuME core without preloaded saves, savestates,
RAM injections or cheats. All49152 upper-screen pixels match at3600,4000 and4200:

- Rota Nova:8378 coloured source pixels and40774 transparent background pixels.
- Porto Estado:48994 coloured source pixels and158 transparent background pixels.

Transparent points are checked against matched native blank-key control frames,
not excluded. The complete lower screens also remain exact to the controls.
Complete existing title words/edges are included in these whole-plane comparisons.
Porto's independent full-word masks/source protection from V329 bind to the exact
current file SHA. The whole Rota logo file remains exact to reviewed V188 artwork.
Original header flags, palettes and extents remain exact to clean. No new wording
or artwork defect was established and no restoration is changed.

## Correct palette-key control

An initial Rota control incorrectly filled entry0. That entry is coloured; the
Rota logo's sole black palette entry is255. The control was invalid for exposing
background and is retained/excluded in `rejected_index0_logo_control.json`.
The corrected control fills255. Porto's key is0. Both correct controls preserve
original headers/palettes/extents and every other fixture byte. The preparation
script now derives the key from each source palette and verifies existing correct
control files without overwriting provenance. Do not assume every PXL uses index0
as its transparent colour. These observations apply to the tested source palettes,
flags and parent; other renderers/alpha states are not inferred.

## Scope and saved evidence

The filename search/pointer trace rediscovered earlier limitations: standalone
names lack an identified caller, and winframe00's exact owner literal only exposes
startup registration in this search. This absence is not global unused proof or
credited as a new resolved consumer. Generated/indirect paths, original parent/
scene selection, embedded WINFRAME display and approximate concealed scenery
remain open. Copyright and the312x246 ship receive loader/view tests only; they
are not forced into an incompatible256x192 scene display.

Screenshots are saved under
`E:/Rota Nova translations/Screenshots/Test fixtures/standalone_title_v550`.
They were visually inspected and are labeled synthetic scenes, not guide-approved
or normal title-screen captures. Hash copy receipts are in the native proof.
All5 emulator sessions terminate with exit0, including the excluded diagnostic.

- `scripts/verify_standalone_resource_compatibility_v550.py`.
- `scripts/prepare_standalone_title_gpu_v550.py`.
- `scripts/prepare_standalone_alpha_controls_v550.py`.
- `scripts/verify_standalone_title_gpu_v550.py`.
- `work/analysis/standalone_resource_compatibility_v550/compatibility_proof.json`.
- `work/analysis/standalone_resource_compatibility_v550/native_compositing_proof.json`.

Focused Ruff passes. All22 original requirement records remain exact. All18
plaque/hint entries and the global texture issue remain incomplete. The full
objective stays active; no canonical promotion. V546 SHA256 remains
499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3.
