# V600: correct score owner and original result-parent rendering

The previous goal turn completed V599's experimental keyboard controls and
source-bound native tests. This turn changes testing and audit evidence. The
production V599 ROM, patch, graphic assets and release registry are unchanged.

## Material review and a wrong historical binding

Expanded source/current review did not establish another coarse-fill defect in
the treasure-header or fleet-wallpaper families. Their earlier restoration and
preservation evidence remains scoped. No unsupported texture replacement is made.

The Won/Lost score atlas still lacked a mapped actual parent. Investigating its
old V164 owner exposed an error: the test read adjacent literal words at
0210F3A8/0210F3AC as an owner/filename pair. The initializer had loaded the
filename from the preceding word, not the following one.

Executing the complete original initializer **0210E190** proves the mapping:

| Owner | Actual initialized owner+12 filename |
| --- | --- |
|023139FC|`_pxl/deckchip15.pxl`|
|02313A38|`_pxl/deck04.pxl`|

The old type33 selector therefore selects Ironclad deck artwork. It does not
prove score selection. An isolated one-byte ship-layout diagnostic confirms
this: the real initialized Deck view selects owner023139FC and resolves the
complete native36532-byte deckchip15 file, not the7572-byte score atlas.
The ship master record identifies type33 as Ironclad. This diagnostic changes
only the named Vestaros test ship's type byte11→33; it does not create a fully
configured or normally acquired Ironclad. The clean-ROM replay did not reach
the same Deck state and receives no paired visual credit.

Historical V164 generation/font checks remain reproducible. Its source-selector
interpretation is superseded here. There is no evidence that this test error
changed the shipped atlas: the actual English deck04 asset remains unchanged.
Future ownership proofs must inspect executed initializer fields and whole
resident files, rather than presumed adjacent pool entries.

## Actual original parent

The correct owner has real source callers0200C210/0200C26C/0200C2A4 for the numeric
digits and Won/Lost labels, and0200C3F0 for the separate Perfect artwork.
Original setup0200C14C selects source[160,0,24,24] for 勝 and[184,0,24,24] for 敗.
Its painter0200C054 places the label after two16-pixel numeric positions.
Won/Lost remain faithful compact result headings; no terminology change is needed.

The original result selector0200A964 calls tally animation0200A6BC when wins differ
from its total, and the original Perfect path otherwise. Source caller tracing
leads back through0200A994/0200A5A8/0200A54C to02073DE0. This is a real call-chain
lead, not a newly earned battle outcome or a visited ordinary result context.

## Explicit native research fixtures

Three RESEARCH_ONLY ROMs inherit exact V599. A separate32-bit research helper
section at01FFD000..01FFDB00 wraps the original frame-pump entry020CF7A4.
It waits for the initialized named Deck view, runs the original result selector
once with explicit10 Won/2 Lost/12 total counters, then executes the displaced
original push and resumes020CF7A8. Recursive frame-pump calls see the cleared guard.
The wrapper preserves all13 general registers, LR and CPSR flags; three controlled
ABI cases additionally verify the displaced stack push. Only the result boundary
is bridged in those ABI cases; the actual emulator runs execute the original body.

Original result selection, constructors, source crops, palette, cache getters,
painters and rendering remain unchanged. No source owner, filename, crop or
loaded-header substitution is used. Current preserves the exact production atlas;
the original-art control restores clean deck04; the blank-label control clears
only its two24-by24 label cells. Digits, Perfect artwork and all other files retain
V599 content. The new autoload section is research instrumentation, not a release
allocation decision. No research ROM is an integrated handoff candidate.

All three fresh cold boots complete7100 frames using the same source save and
controller schedule. They do not load a savestate. The first two capture every
frame4200–7100; the blank control captures4200–4650 and selected later frames.
Read-only final native ITCM proves each one-shot guard reached zero and all three
explicit counters remain10/2/12. The source/copy save hash is unchanged.

Actual final resource getters execute from each captured real cache without SDK
or resource bridges. Every complete7572-byte resident score file matches its
named current/original/blank ROM entry. The resource's initialized filename is
checked independently in the live state as well as in the original initializer.

## Exact pixels and retained failures

Independent source-font masks include all94 English ink pixels: leading, inner
and final letters. Original selector/constructor execution produces93 animation
updates, with only the frame-pump boundary bridged for this geometry replay.
Every original score object's real member descriptors still selects the correct
owner and complete24-by24 label cells. These are source geometry updates, not93
new gameplay scenes.

For the451-frame three-way window, original unchanged digit sprites locate the
pose independently of either Japanese or English lettering. The full source
label is composed over the same-frame blank control, retaining transparency.

- **323 frames pass both entire98,304-pixel composites**:646 full composites,
  or63,504,384 native5 pixel positions.
- **99 frames are wholly identical** in all three runs.
- **12 frames have no complete matching digit pose**. No position is invented.
- **17 frames fail the whole-composite comparison**. Their exact difference
  bounds and digit-anchored rectangles remain in the proof.
- There are no ambiguous multi-pose matches. No frame is silently shifted to
  obtain a pass. The phase/clipping causes of failed comparisons remain unproven.

At frame4500, a separately captured live blank-run controller independently
confirms the two complete centered rectangles[56,84,128,108] and[128,84,200,108].
Both source and English whole composites pass. All original872 opaque Japanese
label points and94 English points are included; transparent source pixels retain
the underlying actual Deck scene.

Across all2905 shared captured frame pairs,2552 entire original/current frames
are identical and353 differ. That is not an assertion that every difference is
text: remaining failed whole-frame cases include differences outside label cells.
They are retained as an unresolved verification gap, not erased or attributed to
an established renderer defect. Complete centered text is verified; every
animation boundary, ordinary result activation and earned battle outcome are not.

## Artifacts and continued scope

- `scripts/prepare_score_parent_v600.py` and `native_score_fixture_manifest.json`.
- `scripts/verify_score_parent_v600.py` and `native_score_parent_proof.json`.
- `original_result_animation_states.json`, original caller disassembly and
  material/source diagnostic images under `work/analysis/material_review_v600`.
- Native captures/reports/state exports on E under
  `Generated/work/emulation_v193/native_score_v600_*`.
- Selected full unmodified research screenshots and hashed provenance under
  `Screenshots/Test fixtures/V600 Score parent`; no ordinary guide credit.
- The one-byte ship-layout diagnostics are retained separately under
  `score_parent_v600_current` and `score_parent_v600_original`.

Production remains experimental V599, SHA256
`1c72049ca2eba551825d67de2429b4ac9751179183afc2ddb5749666d398eba5`.
Its patch and canonical base remain unchanged. No new production build is needed
for corrected evidence. All18 original plaque entries remain incomplete and all22
historical objects retain exact scope. Other materials, miniatures, Confirm,
legacy/village/movie gates remain open. Goal classification: progress through a
corrected resource identity, mapped real parent and native source/blank/current
pixel evidence, with failed cases retained. The full goal remains active; older
record-based checks still need revisiting at actual completion.
