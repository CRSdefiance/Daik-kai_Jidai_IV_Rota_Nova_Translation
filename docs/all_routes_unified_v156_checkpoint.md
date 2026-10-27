# Combined V156: movement notices and sailing statuses

The full translation goal remains active. V156 integrates nine clean-source,
natural-dialogue-v2, en-US movement strings: five supply/action/status/failure
labels and four crew-variant shortage paragraphs. Prose retains both runtime
substitutions and the source intent of stopping automatic travel after supplies
run out. Paragraphs are wrapped after complete substitution. The two status
cells read **Auto Sail** and **Fast Sail**, with a visible gap between them.

## Native callers and formatting

Actual movement branches 02078260 and 02078278 execute captain selection,
the actor table at 02118580, COMMON selection, native sprintf and text
preparation for all eight source variants. The complete copied portrait frame
places the actor table at SP+27C, not the monthly caller's SP+274. Twenty-four
cases cover the combined-supply branch and both actual single-supply getter
branches. Single-supply runtime string initialization is a fixture, supplying
Water and Food; this does not establish every resource-name producer.

The native macro pass reproduced a capital-I collision in "I'll stop...".
A scoped portrait wrapper checks the actual parent return, actor-table pointer
and complete NUL-ended selected template against the four compiled paragraphs.
Only these exact movement paragraphs use literal copying and the inherited
guarded word wrapper. This also preserves capital F in substituted Food.
Wrong parent/table, an unknown template and a near-match with an added suffix
retain the original macro path. Nine monthly/unrelated cases and all 54 actual
village callers preserve their V155 outputs and buffer guards.

The actual 256×32 sailing bitmap constructor and both native formatter/render
calls execute. A caller-specific tracking wrapper keeps complete status labels
inside their original 60-pixel cells at (60,12) and (120,12). Preview review caught
touching labels in an earlier "Auto Sailing/Fast Sailing" research draft; the
final nine-character labels leave a clear gap. The failure modal's actual caller
also preserves its complete text: "Automatic travel is unavailable."

Twenty-eight paired 4/16-bit pixel cases cover all twelve substituted shortage
paragraphs, the failure modal and both status labels together. Complete glyph
order, first/final letters, bounds, whole words and independently decoded native
pixels pass. All fourteen unique panels were visually inspected. Full parent
bitmap/frame composition, physical input and physical cold boot remain pending.

## COMMON packing and preservation

Messages 610–613 replace four mapped B7 owners without changing any block size,
NUL count or directory byte. Message 609 shares the first owner and remains
byte-exact, including its existing line breaks and trailing space. Spare allocation
is placed before the last owner's first mapped entry and skipped by its native
offset; it cannot become trailing message padding or an extra selected line.
All 3,668 selections are independently compared; only four authored texts differ.
All 104 block-7 selections pass warm and cold native copies with explicit ARM946
alignment behavior: 208 cases. The 704 shared-copy phase/length cases also pass.
This work does not approve the separate older message 609's display semantics.

Five label owners are exhaustively checked at every byte position in all actual
loaded ARM9 sections and the decompressed overlay. Original Japanese storage is
preserved. All 207 ordinary getters and 239 shared name/item owners remain exact.
The inherited 3,008-byte staged pool prefix is preserved, expanding to 3,264 bytes
at 023A7200 and copied late to 02387A20. Main heap low is 023886E0. ITCM grows
from 7,900 to 8,160 bytes and ends at 01FF9FE0, with its arena low also 01FF9FE0.
Only 32 bytes remain before overlay destination 01FFA000; future helpers require
an explicit allocation review. DTCM and every inherited helper remain exact.

Native SDK autoload, BSS clearing, ARM7 source and loaded sections, complete late
copy, registers, stack and arena reservations pass. Cross-CPU scheduling and
physical cache behavior are outside this bounded execution.

## Saved integration and identities

The canonical builder rebuilds all 435 inherited batches and terminal stages.
Accepted layers remain baked into the immutable base. Hash locks bind complete
source/prose review, native evidence and the inspected sheet. Fifty focused tests
pass: nine movement/repacking/release rejection tests and forty-one inherited
packing/renderer/monthly/input/village tests. Changed tools pass ruff.

Saved components, full manifest lineage, canonical English menus/graphics and
exact clean patch reconstruction pass. Relative to V155, only ARM9 and COMMON
change; all other ROM files/components and all four route files are byte-exact.
The inherited 1,061-panel FE proof is preserved through unchanged route, font and
modal consumer bytes; those raster cases were not rerun. No canonical promotion.

- Candidate: `out/all_routes_combined_v156_candidate.nds`
- ROM SHA-256: `c9c9cf24cc3ae5d530c3924487493054c15af0f392ff2fc49539bd2fa8c6b7ea`
- ARM9 SHA-256: `9ea488296bf96f47522c90eb09cdea75bd5bc33e86854a25619805767a949a2c`
- COMMON SHA-256: `ea978f466496f8593f13fb97f17b9bac174beea5665c57f1f5e358b2808776c9`
- Patch: `out/all_routes_combined_v156_candidate.xdelta`, 751,537 bytes
- Patch SHA-256: `cf364c60b0105dfbe3bb6f27d9eb4b7932deb93e677b900cdbfbd4ddb3d0f141`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Patch base: `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`
- Profile: `all-routes-unified-v156`, experimental.
- Canonical changed paths: `/__arm9__.bin`, `/COMMON/HELP.DK4`,
  `/COMMON/MESFILE.DK4`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`,
  `/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`.
- Physical cold-boot checks remain: title, New Game, established story/town/
  recruitment, Ceuta/tutorials, village editor and automatic-travel shortage,
  status and unavailable screens. Do not use a savestate.

Evidence: `work/analysis/movement_notices_native_proof.json`,
`movement_notice_callers_proof.json`, `movement_v156_saved_proof.json`,
`work/qa/movement_notices_native/native_sheet.png`; manifest beside the ROM.

## Remaining full goal

The current loaded ARM9/overlay inventory is refreshed at
`work/analysis/arm9_text_loaded_inventory_v156.json`: 81,318 byte/font candidates,
including binary coincidences, and 1,460 aligned address-word leads. Neither is
an untranslated-string count. The five former movement-label owners now point
to English, while their original source strings remain in storage. The rough
record coverage report is `work/analysis/translation_coverage_v156.md`; it is
historical-source navigation, not gameplay or full translation assurance.

245 COMMON selections/133 owners still need consumer/layout integration; further
ARM9/UI and older-name semantics, BGM/Reports/Sailing Help physical presentation
and Japanese graphics/native composition remain open. Graphics include 26
PXL/FLS assets, three embedded copies and the CMMNIMG external-palette UI atlas;
two decorative MAPPOINT atlases and 21 embedded blocks remain to classify.
After the full goal, revisit older record-based checks as requested.
