# Combined V157: complete English duel statistics

V157 is the latest **experimental** combined candidate. It rebuilds the complete
435-batch registered stack from the immutable canonical baseline, including all
V156 stages, then adds one source-reviewed duel statistics template. The logical
English is **Fencing %d HP %d %s**. Both numbers and the entire health-state word
are retained. The formatter supplies bitmap columns; prose contains no authored
alignment spaces. Physical cold boot and gameplay remain pending.

## Native crop defect and correction

The original Japanese bitmap is 144×12. The parent crops source x0–60, x60–120
and x120–144 into three regions. That final 24-pixel crop cuts complete English
health words. Local bitmap previews alone would miss this defect.

The new view is 156×12, with generated twelve-character columns for Fencing
and HP, followed by the complete state. Three/five-digit numeric fields retain
the native 0–500 effective skill range and unsigned 0–65535 HP range. Only the
third crop expands to 36 pixels and moves from parent x72 to x66. Its right edge
is x102, leaving space inside the unchanged 104×40 parent rectangle. The first
two crops, row heights, parent geometry and original Japanese storage stay exact.

The actual source image initializer 0210DD0C establishes 464×96 pixels, 4-bit
storage, pixel base 022BFDD0. Native indexed slot construction at 0200D79C–D840,
0200E368, 020D3AFC and 020D4A7C creates both source views at (0,24)/(0,36), inside
that canvas. Slot rectangles are [152,95,256,135]/[0,95,104,135]. Actual primary
draw dispatch executes 0200E1B0 → 020D470C → 0200CB6C → 020CFC14 → 020D4170,
capturing all three requests at native GPU boundary 01FF92D8. All bounds pass.
Last destinations are [218,119,254,131]/[66,119,102,131]. Source allocation and
neighboring actor rows are intact. All-byte loaded-section/overlay scans prove
sole template owner E310 and sole descriptor owner E28C; other tables stay exact.

64 native owner/getter/formatter/raster cases cover both actors, 4/16-bit modes,
minimum/maximum numbers, seven health states and the unknown empty fallback.
Complete first/interior/final glyphs match independent font decoding. Each
non-space glyph lies wholly within one native crop. All sixteen local and
sixteen paired parent panels were inspected; complete values, words and borders
are readable. Parent previews compose captured native requests on the CPU.

The full effective-skill provider/equipment are fixtures; nine signed values
execute the native final clamp separately. HP and health getters execute
natively. Whole bitmap clearing, widget registration, border/frame/secondary
picture and final GPU submission are explicit contracts. This is not a hardware
GPU or physical gameplay claim.

## Variadic ABI and safe storage

A push/BL/pop wrapper corrupts the third variadic stack argument. The twelve-byte
tail helper at 01FF9FE0 sets tracking to -1 and branches to D5200 with SP, LR and
R0–R3 intact. A regression reproduces the bad suffix pointer when the wrong
wrapper is substituted; it was never shipped.

The inherited 3264-byte staged pool prefix remains exact. The pool grows to
3296 bytes at 023A7200, late-copied to 02387A20, reserving main arena low
02388700. ITCM is 8172 bytes and ends at 01FF9FEC; aligned native arena low is
01FFA000, exactly the overlay boundary. Further resident helpers require
separate proven allocation. Native SDK autoload/BSS, ARM7 source/loaded sections,
late-copy bytes, arena bounds, stack and registers pass. Original DTCM and
all inherited helpers stay exact.

## Integration and verification

24 movement callers, 54 village callers, nine monthly/unrelated portrait paths,
both inherited status rasters, 207 names, 239 shared owners, 3668 COMMON selections
and 704 ARM946 alignment cases pass. COMMON is byte-exact to V156. Forty-eight
focused tests and changed-tool lint pass. Negative checks reject shortened
state crops, corrupted variadic wrappers, missing actor cases/reviews and stale
evidence. Preview generation preserves captured native coordinate records.

Saved components, inherited terminal manifest entries, full 435-batch lineage,
canonical menu/graphics checks and exact clean-ROM patch reconstruction pass.
Only ARM9 differs from V156. All route files, fonts, FE modal consumers, COMMON,
graphics and other components are exact. The inherited 1061 FE panel proof is
preserved through unchanged relevant bytes; those cases were not rerun.
No canonical promotion, commit or push is claimed at this checkpoint.

- Candidate: `out/all_routes_combined_v157_candidate.nds`
- ROM SHA-256: `23822596bd2fe8b486ef61f944a8077693dd1bd07c445761cc51388c985924fe`
- ARM9 SHA-256: `ab08d6e267e512e5f1dc3998930f8a3699809be784d712395ced60dc23ea91ad`
- COMMON SHA-256: `ea978f466496f8593f13fb97f17b9bac174beea5665c57f1f5e358b2808776c9`
- Patch: `out/all_routes_combined_v157_candidate.xdelta`, 751606 bytes
- Patch SHA-256: `8846e007042e6e07e7ad75348a8b5bf854b980c53a7adf04fb69eea6fa9aa359`
- Profile: `all-routes-unified-v157`, experimental
- Registry SHA-256: `67da9c7858ef74eb636eaeb2550623c1fcdea8f4168aa2c757edfff2e9cae347`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Patch base: `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`
- Manifest: adjacent `all_routes_combined_v157_candidate.manifest.json`.

Relative to the canonical baseline, changed paths remain `/__arm9__.bin`,
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/personinfo.pxl`, and `/data/SC0.DK4` through `/data/SC3.DK4`.
Cold-boot acceptance must use this exact full candidate without a savestate,
covering title/New Game, story/town/recruitment, Ceuta/tutorials, village editor,
travel messages and both duel panels.

Evidence: `work/analysis/swordsmanship_status_native_proof.json`,
`swordsmanship_status_plan.json`, `duel_v157_saved_proof.json`,
`work/qa/swordsmanship_status_native/{native_sheet,parent_sheet}.png`.

## Remaining full goal

Loaded inventory `work/analysis/arm9_text_loaded_inventory_v157.json` contains
81318 byte/font candidates and 1459 aligned address-word leads. These are not
untranslated counts. The stored Japanese duel template remains, but its sole
owner now points to reviewed English. Rough record navigation is refreshed at
`work/analysis/translation_coverage_v157.md`.

245 COMMON selections/133 owners need actual consumer/layout integration;
further ARM9/UI, older-name semantics, BGM/Reports/Sailing Help physical
presentation, Japanese graphics and native composition remain open. Graphics
include 26 confirmed PXL/FLS assets, three embedded copies and the CMMNIMG
external-palette atlas; two decorative MAPPOINT atlases and 21 embedded blocks
remain to classify. Full goal stays active. After completion, revisit older
record-based checks as requested.
