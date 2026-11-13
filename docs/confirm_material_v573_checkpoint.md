# V572-V573: original Confirm shading and complete English font

## Source, translation and material

The separate `/_pxl/kakutei.pxl` button reads 確定. **Confirm** remains the
appropriate English action label. The source is a 48x20 four-bit PXL, with a
52-byte header/palette prefix. Its material is blue diagonal shading, not wood.
The inherited white-only erasure retained Japanese-shaped black shadows.

The source-locked correction reconstructs 190 old white/shadow points (109 white,
81 shadow) along the original x+y shading diagonals. Every inferred point has
original visible samples on both sides. No new palette or generic wood donor is
used. All 674 visible material points outside the old strokes and new English
are exact original pixels. The geometric frame, gray bevel, full palette and
metadata remain exact. The complete original game-font Confirm uses 86 ink
points and 76 deliberate one-pixel English shadow points, with full first and
last letters. Only 217 indices change from V571.

Concealed shading is inferred, not an exact recovery. The held-out visible-point
check reproduces 234 of 254 original controls exactly; the largest RGB channel
error is 25. Full point/control details are in `prototype_proof.json`. The bounded
palette search did not identify an unlettered donor. A raw original-payload scan
found one exact occurrence; differently encoded/compressed copies are not ruled
out. The comparison sheet was visually reviewed.

## Integration and exact patch

- Experimental profile: `all-routes-unified-v573`.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Candidate: `out/all_routes_combined_v573_candidate.nds`, SHA256
  `f987f1c56ba5641544e5c84698c59351e39465b15001601adddf697698d89a77`.
- Patch: `out/all_routes_combined_v573_candidate.xdelta`, SHA256
  `f8fb10ac58bb4625facde62db5865bd4d1aaec2acd36e1040a41f253a273dbd3`.
- Patch input: clean ROM SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The complete registered builder retains all 470 inherited batches, 114 accepted
layers and every V571 stage. Only `/_pxl/kakutei.pxl` changes from V571; all code,
other artwork and translations are byte-identical. The neighboring manifest
identifies the complete stack. The clean-ROM patch reconstructs the candidate
byte for byte. Files resolve to the requested E-drive Generated directory.
Canonical promotion has not occurred.

## Native rendering and regression evidence

Four targeted automated emulator cases use isolated Cargo Setup fixtures at
frames 4300/4600. Ten setup/literal words select the original Confirm owner
023139C0, crop [0,0,48,20], palette0 and flags0; artwork is not substituted. The
captured view and original getter020D4170 resolve a resident Confirm PXL exactly
matching the named ROM file. Only documented ARM9 fixture words differ from each
fixture's parent. The default marker fixture remains reproducible unchanged.

All 3,524 opaque native button pixels pass across four cases. The original
palette entry14 is transparent (packed value0000, high bit clear); the other
entries are opaque. Its 79 outer-edge points per crop remain exact original
indices, and all 158 corrected-capture background points match the controls.
The first verifier incorrectly treated those points as opaque black. That test
expectation was corrected using the original palette flag; no ROM repair was
needed. Two paired full-screen comparisons pass all 196,608 points, respecting
this original transparency. Full letters and the source frame are visible.

A separate ordinary cold boot runs the established 21,200-frame title/New Game/
opening/town input schedule. All 56 unique startup captures match V571 exactly.
The source battery save remains unchanged. Ruff and the complete feature verifier
pass. This is targeted emulator evidence; it does not establish every ordinary
Confirm-parent context, a complete playthrough, or hardware-device behavior.

## Evidence and open scope

- Research: `scripts/review_confirm_material_v572.py` and
  `work/analysis/confirm_material_v572/prototype_proof.json`.
- Source locks: `translations/confirm_material_v1.json`.
- Integration: `dk4tool/patch/confirm_material.py`.
- Verification: `scripts/verify_confirm_material_v573.py` and
  `work/analysis/confirm_material_v572/v573_release_proof.json`.
- Raw captures: E:/Rota Nova translations/Generated/work/emulation_v193/
  confirm_material_v573_control, confirm_material_v573_actual, confirm_material_v573_fresh.
- Labeled captures/comparison and provenance: E:/Rota Nova translations/Screenshots/
  Test fixtures/V573 Confirm material. Manual crop placement is not a guide image.

Ordinary button-parent context remains open. The global plaque defect includes
all translated materials, enlarged pale blocks, vertical streaks and Japanese
shadow remnants. All 18 original plaque/hint entries remain `fully_completed:false`,
unchanged from the pre-build snapshot. All 22 historical requirements retain their
exact scope. The graphics goal remains active; the older record-based checks
remain a later follow-up, not silently closed by this material repair.
