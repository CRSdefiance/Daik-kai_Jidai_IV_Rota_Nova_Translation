# V655: complete native cargo tooltip and banner composition

The previous goal turn made progress with V654's completed five-ship victory,
original rewards, nine text displays,21 headings and12 complete Spoils banners.
One hovered banner was explicitly withheld because a tooltip covered part of it.
This checkpoint resolves that comparison and four other captured hover states.
The full graphics goal remains active; no ROM or artwork changes are needed.

## Actual source scene and geometry

V654's terminal replay supplies the unchanged actual RAM, ITCM, DTCM, VRAM, bank
registers and unmodified PNGs at16400,16800,20000,20400 and23200. No new emulator
run, savestate, gameplay fixture or saved-game result is introduced here.

The modal cargo controller is the original `COrganizeLoadView`. Its original
multiple-inheritance metadata selects base offset31F8; the actual owner-list
pointer at base+14 identifies context023117C4. The earlier generic lower context
023117AC belongs to the sea scene underneath this modal. It was the wrong source
for the cargo composition and receives no display credit.

The original context list places the cached Spoils `CSurfaceSprite` before an
active original `CBalloon`. Both are executed with their actual node/context
arguments, in that order, using complete native routines0200CAF8 and020068AC.
The actual banner view's original resource getter resolves the whole current
`_pxl/senrihin.pxl` exactly.

The balloon rectangle is lower-screen[16,74,56,90]:40x16. Its source text crop is
[0,0,36,12] within a208x36 cached bitmap. Original unchanged padding at02112594 is
2x2. Text therefore starts at native display[18,268], after the lower screen's
192-row offset. The earlier [16,266] model omitted this original inset. The final
position comes from original object fields and code, not fitting English letters
to a screenshot.

## Faithful name and complete leading/trailing letters

Original commodity95 is `木材`; **Timber** is its existing faithful English name.
The original item-table lookup and virtual name getter020589FC return that full
current string. No name/string getter or painter is replaced in the replay.

All432 declared source-view indices match an independent original-font model,
including77 complete letter pixels and every blank cell. The actual source palette
matches current ARM9; foreground15 is BGR5558020, displayed RGB(0,8,0).

Both actual first T and final r survive. In each of the five cases, native
analysis-only erasure of the source T changes exactly its13 destination pixels;
erasure of r changes exactly8. Every control fails the complete captured result,
with no other output pixel changes. Captured source/header/palette/backing bytes,
destination guards and original saved-register/stack ABI pass.

## Every pixel of the covered banner and complete tooltip

Both destination planes start poisoned. Original native writes assign every
pixel in the tested union, without reading output before it is written. Captured
visible framebuffers are excluded as VRAM inputs. The existing cached source
name bitmap and source artwork are inputs; a finished screenshot is not.

For each captured hover state, all4096 banner pixels and all640 tooltip pixels
match the actual unmodified capture. Their overlap is440 positions, so4296 unique
positions are checked per case:21480 across five cases. Frame23200's formerly
unexplained369 changed banner pixels are exactly the original tooltip composition.
No pixels are waived. This adds five complete composed-banner results to V654's
12 unobstructed banner results. It does not change historical V654 proof files.

## Retained diagnostic limits

An attempted entire-scene replay also identified the correct cargo context, but
selected-cell animation reads the original hardware timer04000100. It was not
bridged or fitted. The full cargo scene is not claimed reconstructed; only the
complete source-bound banner/balloon callbacks and their tested regions pass.

An exploratory constructor call used a supplied style/anchor contract and produced
a different rectangle. It is retained as a research lead, not the actual name
producer, an additional gameplay screen or verification of all possible tooltips.
The final proof uses the actual captured source bitmap, native name getter and
original source geometry. No text, font, palette, renderer or material repair is
required by the earlier model mismatches.

## Evidence and unchanged full goal

- Proof: `work/analysis/cargo_tooltip_v655/proof.json`.
- Verify: `python scripts/verify_cargo_balloon_v655.py`.
- Archive:
  `E:/Rota Nova translations/Screenshots/Test fixtures/V655 Cargo tooltip composition`.
- The five original V654 PNGs are explicitly labeled reused; native cropped
  reconstructions are derived diagnostics. No new guide/publication credit.
- ROM remains `out/all_routes_combined_v653_candidate.nds`, SHA256
  `c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade`.

The ROM, exact patch, manifest, registry, canonical baseline and release pointers
remain hash-exact. No V655 ROM, commit, push or canonical promotion is made.
All18 original plaque/hint entries remain incomplete and all22 historical scope
objects remain exact. This closes the specific hovered-banner comparison from
V654; wider material/user review, six small-control parents, card/legacy/art,
transition, gameplay and final-acceptance requirements remain open. The four
low-resolution Online exceptions and preserved brown marks remain in force.
Older record-based checks remain due at actual full-goal completion.
