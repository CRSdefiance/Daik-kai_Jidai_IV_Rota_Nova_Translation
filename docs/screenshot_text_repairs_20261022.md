# Screenshot text corrections - experimental

The user reported V1954. That artifact/profile is not available in this checkout.
All three visible text/encoding defects are independently present in the local
V1594 candidate. Do not silently identify those two version numbers as equivalent.

## Confirmed causes and corrections

- **SC0 B177 R140:** clean `8E51` is the complete Japanese glyph `参` in
  `参ったなぁ`. Its native object already stores actor zero immediately before
  the body (`00 40 FF FF 00 00 [text]`). The historical batch incorrectly authors
  `{SPEAKER:8E}`. `8E` then combines with English `4F` (O) to make `三`, exactly
  explaining the screenshot's `三h dear.`. Remove only that false text prefix;
  preserve the actual actor-zero metadata. Fresh source-reviewed prose is
  “Oh dear. He's decided for himself. Does that mean he's joining us?”
- **COMMON message 3667:** the stored paragraph starts with full-width `Ｉ`
  (`82 68`). This uses the 12-pixel Japanese cell instead of the ordinary
  six-pixel Latin font, explaining the raised glyph and wider spacing. Replace
  it with ordinary ASCII I; preserve the wording and the original copy span.
- **Faticia:** the persistent name starts with full-width `Ｆ` (`82 65`).
  Replace it with ASCII F in the same nine-byte allocation, leaving every pointer
  unchanged. The ordinary name at ARM9 offset `15D5E4` was already ASCII; the
  displayed persistent name at file offset `172F60` was the mixed-font copy.

Those full-width I/F spellings were historical macro-safety workarounds. The
current inherited native literal-command guard preserves `Faticia` and `I hear`
as ASCII. The original `I` followed by LF still expands as a command: this repair
neither disables that behavior nor globally rewrites other records. Expansion
must still precede wrapping for the mapped COMMON consumer.

## Photo 2: corrected diagnosis - No label centering

The original Yes/No branches are `聞く` / `聞かない` (listen / do not listen).
They answer Cesare's ship-selection advice offer in **B177 R144**, not Rafael's
rhetorical question in R140. R144 now reads “Ah, Admiral. Would you like some
advice on choosing a ship?”, retaining its complete source actor `0D` and native
allocation. No choice or command bytes change.

The user subsequently clarified that Photo2 reports the **No label being off
center**, not a missing prompt. The earlier missing-prompt interpretation was
incorrect and is withdrawn. Historical proof fields saying that a missing-prompt
transition was unverified describe that mistaken interpretation, not an additional
user-reported defect. See `ship_advice_choice_centering_20261022.md` for the native
padding diagnosis, unpadded-string repair and Yes/No/cancel branch verification.

## Integrated research candidate

- Candidate: `out/screenshot_text_repairs_20261022_candidate.nds`
- SHA-256: `ba0c910644725ef54a3d817b1754a861244c11fe7c95a06974f32440773bbf54`
- Canonical construction base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Profile: `screenshot-text-repairs-20261022`, inheriting the complete V1594 profile
- Stack SHA-256: `69fcaf4bc1d12f63b987418104e48d913b7e3ede7be957186f8314fd7e1fd787`
- All 114 accepted layers remain baked into the unchanged canonical base. All
  471 inherited batches plus the new four-record manuscript are in the manifest.
- Exact additional changed internal files versus V1594: `/data/SC0.DK4`,
  `/COMMON/MESFILE.DK4`, `/__arm9__.bin`. All other files/components match V1594.
  The ARM9 change is name data only; fonts, native code, selectors, staged payload
  size, metadata, command addresses and name pointers remain unchanged.
- Status: experimental research candidate; not promoted or ready for normal
  release handoff. V1492 remains the promoted checkpoint. No clean-source or
  canonical ROM is modified, and no release patch is published.

## Verification and limits

- Both story records pass exhaustive source/context/formatting QA with zero
  blocking issues. All generated previews were viewed.
- Original native initialization and all 207 ordinary name getters pass; only
  Faticia's text changes, and all 207 returned pointers remain exact.
- All 3,668 COMMON directory/copy boundaries and 3,667 unselected text strings
  are preserved. This checks stored ownership; it is not a claim of re-executing
  every native COMMON copy.
- Five original native macro-expansion cases pass, including preserved literal
  I/F and the preserved executable `I` plus LF case. Input/output guards pass.
- Seven complete controlled native bitmap cases match independently decoded
  font pixels, semantic glyph order and bounds. The before/after sheet was viewed.
- Integrated builder, saved-file round trip, baseline verifier, manifest ancestry,
  targeted Ruff and 52 existing dialogue/pair-phase/raw-source tests pass.
- A fixture-free automated DeSmuME cold boot runs 4,000 frames using the existing
  `cliff_editorial_v829/ordinary_newgame_inputs.json` schedule, without a savestate
  or callback errors. All seven captured whole-screen frames at
  1/60/180/1600/2000/3200/4000 match the V1594 reference exactly: startup, New Game,
  character selection and the opening scene. The startup sheet was viewed.
- The changed Alexandria, guild-rumor and tavern nameplate scenes, their original
  progressive timing, both Yes/No branches, and physical hardware remain
  unverified. These checks do not establish a full playthrough.
- ROM retention was previewed only; no ROMs were deleted.

## Reproducible sources and evidence

- `translations/screenshot_text_repairs_20261022_manuscript_v1.json`
- `translations/screenshot_text_repairs_20261022_release_v1.json`
- `dk4tool/patch/screenshot_text_repairs.py`
- `scripts/verify_screenshot_text_repairs_20261022.py`
- `work/screenshot_text_repairs_20261022/integration_receipt.json`
- `work/screenshot_text_repairs_20261022/native_text_proof.json`
- `work/screenshot_text_repairs_20261022/native_before_after.png`
- `work/screenshot_text_repairs_20261022/story_audit/`
- `work/screenshot_text_repairs_20261022/startup_verification.json`
- `work/screenshot_text_repairs_20261022/cold_boot/capture_report.json`
- `out/screenshot_text_repairs_20261022_candidate.manifest.json`

Historical batches and earlier evidence remain unchanged. The new optional
builder stage runs after the complete inherited stack, checks full source and
target hashes and only writes reviewed, equal-length owned spans.
