# V568–V569: correct marker prices and restore original artwork

## Confirmed source-ownership and translation defect

The historical marker batch assumed 16-pixel rows throughout the goods column.
Original source writing contradicts that assumption:

| Original | Meaning | Correct source cell | Previous English/region |
| --- | --- | --- | --- |
| 売り値 | Selling price | [112,48,144,60] | Disc., [112,48,145,64] |
| 買い値 | Buying price | [112,60,144,72] | Buy, [112,64,145,80] |
| Bag illustration | Artwork, no caption | [112,72,152,112] | Sell over part of the illustration |

The new compact headings are **Sell** and **Buy**, faithful price-column labels.
“Disc.” incorrectly implied a discount. The other Sell caption had no Japanese
writing beneath it and must not be retained as a translation. Historical records
`DK4_MARKER_DISCOUNT`, `DK4_MARKER_BUY_PRICE`, and `DK4_MARKER_SELL_PRICE` are
superseded by the registered correction, not rewritten in old reproduction inputs.
The historical major-caption catalog of 24 becomes 23 after removing the invented
artwork caption and retaining the two actual price headings.

The correction first restores original [112,48,145,96], then reconstructs the two
actual price text cells from their own unlettered source material using visible
2D context. Both original words conceal much of the same material, so 58 inferred
points use other source rows. Hidden texture is inferred, not recovered exactly.
All 380 visible material points outside source strokes/shadows and new English
remain original. The complete original game font supplies 90 English ink points;
the trimmed top two rows and sixth column are checked blank for every used glyph.
Both captions fit fully within their 32x12 source-writing spans.

All 1,600 original bag pixels are now exact, restoring 369 pixels changed by the
incorrect Buy/Sell regions. Only the owned 33x48 region changes from V566: 703
indices in the loose marker and the corresponding embedded marker. Every other
caption, gender symbol, ornament and image pixel remains unchanged. Source headers,
all 83 palettes and dimensions remain exact. The full 65,536 embedded marker indices
match the loose marker; the embedded frame half and all other archive blocks stay
unchanged. The texture workflow now requires checking source writing and artwork
ownership independently of regular row spacing.

## Registered combined candidate

- Profile: `all-routes-unified-v569`, experimental, retaining all 470 batches,
  114 accepted layers and every V566 stage. Canonical parent unchanged.
- Base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- ROM: `out/all_routes_combined_v569_candidate.nds`, SHA256
  `27126e0bc04ab0d97a95dc0494f4cad5882abe8af4c4952e933b18b80df99cf4`.
- Patch: `out/all_routes_combined_v569_candidate.xdelta`, SHA256
  `3dc118787197cbbd56148f6411f65306a6a9e9c312eb832025c6f5ab018697a2`.
- Patch source: clean ROM SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

Only `/_pxl/__marker.pxl` and `/GRP/CMMNIMG.DK4` change from V566. Every code
component, other artwork and other translation remains byte-identical. The adjacent
manifest records source/config/target hashes and all inherited layers. The patch
reconstructs the exact candidate from the exact clean ROM.

## Native checks and their limits

Two disposable test ROMs alter ten argument-setup/literal words to select the
original marker resource and manually request [112,48,152,112] through the existing
header renderer. No artwork file is substituted; resource loading and drawing code
remain original. Actual core RAM shows owner02313F74, source112/48, size40x64,
palette0 and flags0. Original getter020D4170 resolves a resident PXL byte-identical
to the named marker file. Four control/corrected cases at4300/4600 pass all 10,240
crop pixels. Two paired whole-screen comparisons pass 196,608 pixels, including
both complete English words and the entire restored bag.

These are manually supplied crop fixtures, not proof of the original price-panel
parent or ordinary UI placement. The ordinary copied-save Market > Trade attempt
was refused because a trading contract was absent; Market Info opened a fee dialog.
No purchase/contract was completed, and neither attempt earns price-display credit.
The original source save remains unchanged. Their report and scope are retained.

The initial crop fixture is explicitly rejected and retained. It reused source-X
register112 for palette/flags, producing invalid colors. The corrected fixture
stores width/height/zero palette/zero flags before setting X/Y; captured arguments
are asserted before pixel verification. This was a test-code error and never changed
the production ROM. See `rejected_fixture_diagnostic.json` and the retained rejected
metadata/captures. No successful claim uses those failed captures.

A separate ordinary V569 cold boot passes all 56 unique title/New Game/opening/town
captures against V566. Ruff passes. This is targeted emulator verification, not a
complete playthrough or physical-device test.

## Evidence and remaining scope

- `scripts/review_marker_ownership_v568.py`; source/prototype reconstruction.
- `dk4tool/patch/marker_price_ownership.py`; exact payload/metadata/font/artwork guards.
- `translations/marker_price_ownership_v1.json`; source/target locks and payload.
- `scripts/verify_marker_ownership_v569.py`; fixture preparation and release verifier.
- `work/analysis/marker_materials_v568/v569_release_proof.json` and
  `price_ownership_review.png` (uniform four-times pixel scale).
- Native captures on E under `Generated/work/emulation_v193/marker_ownership_v569_zero_*`;
  ordinary startup under `marker_ownership_v569_fresh`.
- Labeled screenshots and provenance on E under
  `Screenshots/Test fixtures/V569 Marker ownership`; not guide-publication candidates.

The other marker material families, the separate blue Confirm button, original
price-parent contexts and the broader graphics audit remain open. In particular,
the smaller Temp Store/Issued/Spoils marker headers still require their own source
shadow/material review; standalone banner repairs do not prove those smaller copies.
All 18 original plaque/hint entries remain incomplete. All 22 historical requirements
retain their original scope. The graphics goal stays active.
