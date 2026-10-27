# V608: village portrait wrapping corrected across all clues/messages

V607 made progress by reaching the original village UI and exposing a real split
of `hear`. V608 fixes that formatting contract without changing the English
wording, accepted answers, fonts, native text renderers, graphics or keyboard.
The goal remains active; village menu/name translation and all other graphics
gates remain open.

## Source and integration

- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Experimental profile: `all-routes-unified-v608`, inheriting all 470 V604
  batches and all 114 accepted layers. The registry and adjacent manifest name
  the complete stack. Nothing is promoted to accepted or made canonical.
- Candidate: `out/all_routes_combined_v608_candidate.nds`, physically on E under
  `Rota Nova translations/Generated/out`, SHA256
  `1bf4f00b6117d6a9a16daca8a8d3a4a8e1dc5e9f24aeac984023db8d1c73ab7f`.
- ARM9 SHA256:
  `c99b2a5ab97ef4a973c648d4b5a3f0faf8109d041e03e2ed81c813d0d4c09605`.
- Exact clean-ROM `.xdelta` SHA256:
  `ef97e56eedd0370bf48d6bd83072791451d7082ca13c97baaa80be55719e8e91`.
- Only `/__arm9__.bin` differs from V604. Every route, COMMON archive, artwork,
  embedded container and other component remains byte-identical to V604.

The terminal transform is `dk4tool/patch/village_portrait_wrap.py`, configured by
`translations/village_portrait_wrap_v1.json`. It validates the existing reviewed
natural-dialogue-v2 manuscript and every original clean/canonical Japanese span.
It compiles all 24 expanded clues and four independently rendered messages using
36 first-row cells, 35 continuation content cells and the existing two-space
machine guards. Manuscript prose stays one paragraph; no hand-authored breaks or
translation shortening are introduced. Eleven stored strings actually change.

Ten fit their existing aligned slots. Kamui's clue needs two additional bytes;
its original slot and every neighboring string are preserved. A new aligned copy
adds 32 bytes to staged storage. An exhaustive byte-position reference search
finds exactly one owner of its former address, at 02119230. That field, the startup
copy branch and arena bound are updated. The existing cache wrapper and native
copy size are rebuilt; inherited payload bytes outside the owned text spans are
exact. No rendering, glyph, input or other runtime helper is added.

## Actual scene and correct canvas identification

The isolated Syracuse donor and authorized location fixture from V607 are reused.
The runner verifies that V608 is the exact registered transform of V604 before
using its unchanged source getter/terrain contract. Only eight ship-coordinate
bytes are owned; no discovery, scene, resource or dialogue flags are supplied.
Normal travel and successful password entry are not claimed.

The 8,600-frame cold boot finalizes normally, without a savestate or callback
errors. At frame 7800, the original village request displays:

```text
Captain, the village chief asks to
hear the promised words.
```

Both complete line masks start at native x22, at y296/y312. Every foreground
position in the entire old 224x48 text region passes, including inter-word spaces,
blank tails and the now-empty third row. The old V604/V607 split is independently
reproduced from its actual screenshot before crediting this repair. Everything
above the dialogue remains exact. Six complete discovery, docking, menu, prompt
and editor frames also remain pixel-identical to V607.

The real parent is 0218D798, vtable 021438A0 (`21CMessageSurfaceSprite`), client
228x48, backed by a 288x48 four-bit canvas at 0601A000. Captured VRAM bank D
control 81 maps its physical bytes to main BG. All 6,912 bytes of the captured
request plane exactly match an independent replay of the original 020548A8
renderer against this actual parent and independently decoded font pixels.

An intermediate working assumption called this a three-row canvas. The completed
binding corrects that: it stores four 12-pixel rows, and the original compositor
spaces those rows 16 pixels apart on screen. All current paragraphs need at most
three stored rows. The final compiler allows four; its maximum-row metadata was
corrected and the integrated manifest regenerated. The ROM bytes and SHA256 are
unchanged between those two builds, so the captured tests cover the final ROM.

## All paragraph layouts and regressions

All 28 contexts execute the original renderer against the captured parent,
palette, header and VRAM mapping. Current live pointer fields select every stored
string, including the newly loaded Kamui clue. Clue prefix/suffix expansion is an
explicit replay input; this does not claim 24 ordinary clue events were visited.

Every nonblank glyph appears in order, every complete word remains on one row,
and all leading/final letters fit. Each complete 6,912-byte canvas matches
independent font decoding: 193,536 bytes total. Header, palette and neighboring
guards remain exact, with no page overflow. Transparent canvas resets are
explicit replay contracts. The full 28-panel native-raster analysis sheet was
visually reviewed; its plain analysis backing is not replacement game artwork
or an ordinary guide screenshot.

A separate 24,100-frame ordinary New Game/Market run uses no existing save or
synthetic fixture. All 19 sampled whole screens match V604 exactly, including
startup and established Market navigation. The complete registered builder,
manifest and clean patch roundtrip pass. Fresh preservation checks cover all
660 PXL headers/palette banks/extents, 261 FLS textures and 57 embedded extents.
Those checks preserve scope; they do not prove all artwork contexts complete.

## Evidence and remaining work

`work/analysis/village_wrap_v608` holds the transform, actual-canvas, preservation
and release proofs, source schedules, build log and native-raster sheet.
Reproduction scripts are `prepare_village_wrap_v608.py`,
`run_village_wrap_v608.py`, `probe_village_canvas_v608.py`,
`verify_village_wrap_v608.py` and `record_village_wrap_v608.py`.
Build only through `build_integrated_release.py --profile all-routes-unified-v608`.

Raw reports and exports are under E's `Generated/work/emulation_v193` directories
`village_wrap_v608_inuvik` and `village_wrap_v608_market`. Selected fixture images,
native previews and provenance are under `Screenshots/Test fixtures/V608 Village
wrapping`; ordinary regression guide candidates are saved separately. Publication
and physical-device/user acceptance remain unapproved.

V607's request wrapping defect is resolved for this actual scene and all 28
bounded paragraph layouts. Its six Japanese menu strings and village name remain
open. All eight ordinary village-card contexts, successful password/development,
other graphic/legacy/material/movie contexts and broader gameplay acceptance
remain open. All 18 plaque/hint objects stay incomplete, and all 22 historical
requirement objects retain their exact scope. Revisit older record-based checks
at actual full goal completion.
