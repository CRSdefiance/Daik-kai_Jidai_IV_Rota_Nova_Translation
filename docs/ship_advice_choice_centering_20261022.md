# Photo 2: Yes/No choice centering

The user clarified that the defect in Photo2 is the position of **No**, not a
missing dialogue prompt. The earlier missing-prompt interpretation is withdrawn.

## Confirmed cause

SC0 block177's native two-choice object occupies `[0x8E6,0x8FC)`. The English
strings were `Yes ` and `No      `, retaining their four- and eight-byte source
allocations. Original native width function `020CF348` counts every trailing
space: four and eight units rather than three and two. The native renderer
centers the padded string, leaving No's two visible letters against the left of
its48-pixel label bitmap. Yes also sits three pixels left of its correct origin.

The original menu minimum is eight units, so removing these spaces need not
change the frame geometry. Original virtual geometry `02052E40` returns the
same rectangle `[88,64,168,128]` for both old and corrected labels.

## Bounded data repair

Original opcode `2100` contains two relative label offsets. Its original getter
`0202A30C` selects `object+6+offset[index]`. It does not find the second label by
scanning past the first. Original VM handler `0202A1D8` advances past the last
string and rounds up to the next two-byte command boundary.

The typed choice compiler stores unpadded terminated Yes/No strings:

- Yes retains its original start and terminates one byte earlier. The reclaimed
  separator becomes unused gap storage; the next alignment NUL remains intact.
- No moves six bytes forward inside its existing owned allocation. Its table
  offset changes from6 to12, and its original final terminator is retained.
- The complete object remains22 bytes. Its opcode, first offset, final NUL and
  alignment byte, following command address, ILNK directory and every other
  script byte remain exact. The NUL count also remains unchanged, preserving
  subsequent diagnostic record numbering.
- Neither label contains authored alignment spaces. Translators retain plain
  `Yes{PAD}` / `No{PAD}`; the menu compiler owns storage and termination.
- No native code, font, geometry, choice meaning or branch result changes.

Source-reviewed meanings remain accept/decline Cesare's ship-selection advice;
the clean Japanese is `聞く` / `聞かない`. No recruitment decision is introduced.

## Native verification

`scripts/verify_ship_advice_choice_centering_20261022.py` executes the original
provider constructor, label getter, count getter, width function, geometry
method and complete VM dispatcher. Yes, No and cancel preserve their original
result states and the22-byte next-command delta. Only modal input completion is
bridged in that isolated dispatch test; no original-scene gameplay is claimed.

Complete native `D5340 -> CF0A8 -> D5404` centered-label planes match independent
ASCII-font pixels at two foreground styles for all four old/new label cases.
Original label origins are12 for padded Yes and0 for padded No. Corrected
origins are15 and18; both visible text-cell centers are exactly24. Full source,
bitmap, stack/register and buffer-boundary checks pass. Three negative compiler
cases reject changed opcodes, changed wording and incomplete review gates.

The comparison sheet was visually inspected. Its letter pixels are generated
by the native renderer; selection-colored backgrounds are illustrative. It is
not a full screenshot of the original Alexandria scene.

## Integration

The experimental `screenshot-text-repairs-centered-20261022` profile inherits
the entire preceding screenshot-text profile and V1594 stack, then applies this
one choice-object repair. It retains the corrected Oh dear paragraph, ordinary
I in message3667 and ordinary F in Faticia. The new stage changes only
`/data/SC0.DK4` relative to its immediate parent. The canonical construction
baseline and promoted V1492 checkpoint remain unchanged.

The reported user version was V1954; that ROM/profile is not available here.
The available V1594 independently contains the exact padded labels seen in the
screenshot. Do not silently equate those version numbers.

Candidate identity, final manifest, baseline verification and cold-boot results
are recorded in `work/choice_centering_20261022/integration_receipt.json` after
the registered build completes. Original Alexandria scene/input activation
and physical hardware remain separate checks; the build stays experimental.

## Sources and evidence

- `dk4tool/patch/ship_advice_choice_centering.py`
- `translations/ship_advice_choice_centering_20261022_manuscript_v1.json`
- `translations/ship_advice_choice_centering_20261022_release_v1.json`
- `scripts/verify_ship_advice_choice_centering_20261022.py`
- `work/choice_centering_20261022/native_choice_proof.json`
- `work/choice_centering_20261022/native_choice_before_after.png`

The earlier screenshot repair's historical missing-prompt proof flags are not
evidence of a separate defect. They remain historical records of the earlier
misinterpretation and are superseded by this clarification.

## Completed build identity and startup regression

- Candidate: `out/screenshot_text_repairs_20261022_centered_candidate.nds`
- SHA-256: `6b77a37d4f2113102e0cce5d2b0d1018d26899c45eed90ffd2a60b4ee340a6a8`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `screenshot-text-repairs-centered-20261022`;473 batches including
  both screenshot manuscripts, with all114 accepted layers baked into the base.
- Stack snapshot SHA-256:
  `69c46e5bfb2446e79a3146a993df691f3384612963c4a77875d418f08a7967f3`.
- Manifest ancestry/source/config checks, native verifier, baseline verifier,
  Ruff and syntax checks pass. Every file/component except SC0 matches the
  preceding screenshot-repair parent; only the owned22-byte object changes.
- A fixture-free4000-frame automated DeSmuME cold boot with the existing input
  schedule and no savestate/callback errors matches all seven parent startup,
  character-selection and opening frames exactly. The contact sheet was viewed.
- Original Alexandria scene input and physical hardware are not claimed.
  Candidate remains experimental; no promotion or normal release handoff.
- ROM retention preview completed; no ROMs were deleted.
