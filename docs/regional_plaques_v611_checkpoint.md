# V611: further plaque defects, repaired asset, native context still open

The previous continuation made progress through V610 village UI and password
testing. This batch returns to the user's global plaque material complaint. A
new source/current sweep finds an additional affected regional-fleet atlas and
records further Golden Route and Save/Load leads. The graphics goal is active.

## Confirmed regional material defect and repair

The original `/_pxl/chihofleetinfo.pxl` has five gold plaques: レベル, 収入額,
支出額, 投資額 and 任務. The current English atlas retains conspicuous upper
Japanese strokes above four historical text rectangles, horizontal row-fill
bands and incomplete right/bottom rims. Complete English words alone had not
verified these source materials. The atlas comparison includes surrounding
wallpaper, the original full faces, native-size images and a five-times enlarged
source/current/prototype sheet.

V611 repairs all five faces with contiguous fine grain from original Japanese
towninfo `[3,62,43,74]`, the source sample reviewed for the V581 join correction.
The period remains 40 columns. Concealed Japanese texture and resized interior
regions are reconstructed; their exact original hidden pixels are unknown.
Each plaque takes its two-pixel rim from its own original regional source face,
with the corners and final two columns retained under the declared width mapping.
The financial plaques retain the existing expanded English width. This is a
source-framed redesign, not a claim that all visible interior grain or source
geometry is identical to the original Japanese plaque.

The entire historical edit and original glyph area is owned and restored before
the final face/English pass. All pixels outside the five declared rectangles stay
exact V610. Outside each new face, the selected source wallpaper is exact; the
count of newly restored wallpaper points is zero for these chosen bounds. Do not
describe this as recovery of previously missing wallpaper pixels.

Five independently checked native-font masks retain 424 complete ink points,
all first/final letters and blank cells. Ten explicit first/final-letter erasure
controls fail. The repair changes 3,333 indices and verifies 1,144 own-source rim
samples. Every header byte, palette bank, dimension, unrelated pixel and other
ROM component remains unchanged from V610.

## Translation review

| Japanese | English | Meaning and decision |
| --- | --- | --- |
| レベル | Level | The admiral's level, beside the original level value. |
| 収入額 | Income | Financial income amount. |
| 支出額 | Expenses | Financial expenditures; plural is natural for the aggregate field. |
| 投資額 | Invested | The amount invested, rather than the previous command-like Invest. |
| 任務 | Mission | The fleet's assigned task or policy. |

Original code `0208DFC8..0208E03C` obtains the financial record through
`020367FC` and places its three values at x52, y104/124/144. Mission starts at
x52/y164; Level's value is at x132/y80. The new plaques end at x49 and x125,
respectively. These source positions establish a layout contract, not actual
screen verification. No dialogue, name, numerical formatter, policy or model
data is changed. No new prose translation is claimed.

## Native experiment: no plaque display credit

Executing the original filename initializer `0210FAB0..0210FAD4` identifies
owner `02313380` and filename `_pxl/chihofleetinfo.pxl`. The original full-screen
backdrop branch at `0208E1EC` constructs a 256x192 view. Those source facts do
not prove that a particular Fleet Info session executes this branch.

Two explicitly labeled research ROMs change only instruction `0208E140` to
branch to that existing regional-background path. Earlier fleet checks, financial
data, models, input, flags and all other code remain unchanged. This is a test
instrument, not an approved release change or proof of regional-fleet formation.

The first control schedule stopped at 12,000 frames, before the Info selection
at 16,001. It receives no Fleet Info or regional-display credit. The corrected
paired 17,200-frame cold boots use the complete established schedule and the
same unchanged isolated save. They reach the known Fleet Info screen normally.
However, all three paired complete images at 16,900/17,000/17,200 remain exact.
The whole regional PXL is absent from the captured RAM, and no live full backdrop
view matches its declared owner/descriptor contract. The branch patch is present
in live RAM. None of these captures verifies the five repaired plaques.

Do not relabel an inactive source branch as an actual display consumer. Follow
the real regional-fleet/model path or a suitable legacy consumer next. Repeating
this same background-selector schedule or merely substituting the atlas into an
unrelated viewer would not establish normal regional-fleet usage. No global
unused-asset conclusion follows from this bounded negative result.

## Integration and ordinary regression

- Experimental candidate: `out/all_routes_combined_v611_candidate.nds`, physically
  `E:/Rota Nova translations/Generated/out/all_routes_combined_v611_candidate.nds`.
- Candidate SHA256: `25641cade46936dea0fb73f5e444f9b31aea77d0cb1633b14f7503e1979f81d1`.
- Profile: `all-routes-unified-v611`; all 470 V610 batches and 114 accepted layers
  retained, with the five-plaques terminal stage added.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Changed internal file from V610: `/_pxl/chihofleetinfo.pxl` only. All ARM9/ARM7,
  startup, cache, pool, heap, layout, scripts and other translations are exact.
- Exact clean-ROM patch SHA256:
  `7aa3ab897ff2606dc5358f12427919023b4d04803587c2572efc763dcc705bbd`.
- Patch input: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- All 19 unique ordinary New Game/Market regression screens in a separate
  24,100-frame run match V610 exactly; no existing save or synthetic fixture.
- Fresh preservation checks retain all 660 PXL headers/indexed palettes/extents,
  all 261 FLS textures and all 57 embedded block extents.
- The registered builder, manifest, independent asset checks, exact clean patch
  reconstruction and targeted Ruff pass.

The first build correctly rejected use of the translated integration baseline
as a Japanese texture reference, before output. The source binding was corrected
to `work/clean.nds`. A subsequent build ended with a MemoryError; it produced no
candidate. After both processes were terminal and system memory was checked,
the complete build was retried successfully without skipping any inherited layer.
Both diagnostics are retained alongside the successful build log.

**V610 remains the latest verified candidate.** V611 is compiled and statically
verified, with ordinary regression evidence, but its changed plaques still need
actual native loading, palette, crops, readability and contextual review. No
canonical promotion, human/device acceptance or ordinary regional-fleet progress
is claimed. The inactive research selector ROMs are never release parents.

## Additional material findings retained

The sweep generated comparisons for 24 changed top-level UI atlases, not 24 new
complete visual clearances. Five families were inspected visually. Besides the
regional atlas, Golden Route discovery/log and Save/Load plaques still show
overwritten source rims/grain or broad row-filled material. A far-right dark
remainder beside the Golden Route log's Prize needs source-ownership review.
Its Gain/Prize wording also needs contextual review against 利益率/報奨金.
These findings are not fixed by V611. Other generated atlases are not silently
marked visually reviewed. The Porto Estado comparison remains a legacy-art
reference, not a newly cleared native context.

## Evidence and reproduction

1. `scripts/review_regional_plaques_v611.py` generates the prototype/config/sheet.
2. `scripts/register_regional_plaques_v611.py` registers the complete profile.
3. `scripts/build_integrated_release.py --profile all-routes-unified-v611`.
4. `scripts/verify_regional_plaques_v611.py --static-only`.
5. `scripts/prepare_regional_view_v611.py` creates explicitly named research ROMs.
6. Run the captured 17,200-frame schedules, ordinary 24,100-frame regression and
   `scripts/audit_graphics_preservation_v574.py` with the report arguments.
7. `scripts/verify_regional_plaques_v611.py` records both successful asset/regression
   evidence and the unsuccessful display experiment in `pending_native_proof.json`.
8. `scripts/record_regional_plaques_v611.py` archives the proofs and keeps the
   latest verified release pointers at V610.

New source comparisons, test captures, diagnostics and scripts are saved on E.
Research captures are not guide candidates. All 18 original plaque/hint entries
remain incomplete; all 22 historical requirement objects retain exact scope.
Village cards, other graphics/material/legacy/movie gates and broader gameplay
verification remain open. Older record-based checks remain due at full completion.
