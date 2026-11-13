# V685: four source-faithful percentage repairs and a final-build format guard

V684's complete Maria opening test found an actual formatting defect rather
than an artwork defect: `3% of sales` was interpreted by the native formatter
as a `% o` octal command. A full source-bound census identifies four affected
records across three routes. V685 repairs all four and prevents newly introduced
format commands from passing future playable builds merely because their C
syntax happens to be valid.

## Experimental combined release

| Item | Value |
| --- | --- |
|Candidate|`E:/Rota Nova translations/Generated/out/all_routes_combined_v685_candidate.nds`|
|Profile|`all-routes-unified-v685`|
|Candidate SHA256|`83e7bdc7c4926ad69eb04704e8327aba50d0fe29b00cce7f5f59d4be8c203150`|
|Manifest SHA256|`849e727a302970e90a55cf510571f69d7a68d2cfd8e244ddea6a7efedcfcee34`|
|Patch SHA256|`db9d1288f1ee1695d388ba2addc6841c5cdf3973b12403e6684b61011d66b181`|
|Canonical base|`out/raphael_natural_v2_accepted_base.nds`|
|Canonical SHA256|`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`|
|Inherited stack|All 470 existing batches and 114 accepted layers, with all V678 stages|
|New experimental stage|`story_literal_percent_safety`, using three canonical-source natural-dialogue-v2 manuscripts|
|Changed files relative to V678|`/data/SC0.DK4`, `/data/SC2.DK4`, `/data/SC3.DK4`|
|Canonical promotion|None; explicit user acceptance is still required|

All ARM9 bytes, every other ROM file/component and all 675 PXL/FLS files remain
byte-exact to V678. The previous 921-view/57-embedded-region graphics preservation
coverage is inherited through whole-file equality, not presented as a new
independent visual audit. A clean-ROM xdelta reconstruction reproduces V685
exactly. The ROM, patch and manifest remain together on E through `out`.

## Reviewed records

| File and record | Faithful repair |
| --- | --- |
|SC0 B177 R0180|The trade tutorial spells out a 1 percent share and retains the one-to-five-unit purchase limit.|
|SC2 B133 R0136|Lil confirms giving 2 percent of Nantes for 1 percent of Lisbon.|
|SC3 B33 R0137|Ian reports the 3 percent sales agreement and the condition that their ships pose as foreign vessels.|
|SC3 B135 R0325|The same original tutorial paragraph as SC0 receives identical English.|

Clean Japanese records and adjacent spoken context are retained in
`source_context_review.json`. All four canonical records are exact to clean
Japanese. The paragraphs preserve meaning, quantities, exchange direction,
speaker states 0D/02/15, original allocations and every neighboring record.
There are no authored line breaks, manual alignment bytes or new macros.
All four native-font previews were opened. Dialogue QA reports no unwaived
errors or warnings. Early tutorial drafts failed byte/phase or weak-wrap checks;
their reports are retained. The final opt-in balanced profiles use the existing
automatic planner with unchanged route metrics, guards and pair-phase rules.
Historical profile behavior is not silently altered.

## High-level prevention

The previous lexical regex accepted `% o` and `% s` because both are valid
format commands. The new final-file guard compares changed English story
records against clean Japanese command sequences after every registered stage.
It covers all four final SC0-SC3 archives. Source-leading 25 is exempt only at
byte zero when preserved from source. Binary/untranslated Japanese records are
not mislabeled as English printf templates. COMMON, HELP and ARM9 keep their
separate native contracts; this is not a claim that one generic scanner proves
all game text safe.

The old V678 files fail with precisely these four findings; V685 passes with
zero introduced or invalid commands. Ten focused regression tests include
lexically valid but unprovided argument reads, actual source placeholders,
argument order/types, leading-state exceptions and dangling percent signs.
All pass. AGENTS and workflow documentation now require literal story amounts
to use `percent`. Unsafe historical profiles will fail this final gate until
their repairs are selected; their output ROMs and evidence remain preserved.

Sixteen complete original-native sprintf calls reproduce each old corruption
and verify each repaired record under two supplied-argument controls. `% s`
reads the controlled BOGUS string; `% o` consumes the controlled octal value.
The repaired outputs are exact and argument-independent. Full native return,
saved registers/stack, destination canaries, source bytes and NULs pass. No
emulated renderer or formatter instruction is patched.

## Actual cold-boot verification

Three fresh terminal runs use the real V685 ROM and pinned DeSmuME core:

- Maria opening and its baseline each finish 31,000 frames, using only the
  authorized unchanged system-unlock save and ordinary New Game buttons.
  There is no savestate, story/chapter/location fixture or movie substitution.
- All 49 complete current Maria/baseline screenshots and terminal RAM match.
- All 48 unaffected Maria screenshots equal V678. Only frame 24400 changes,
  entirely inside the intended dialogue rectangle. Portrait, nameplate,
  background and borders are exact outside it.
- At 24400 every glyph of all three source-compiled lines—including `percent`—
  and all remaining empty rows match. Complete first/final-letter masks pass.
- All 45 inherited source-photo holds remain exact. Current RAM contains the
  complete repaired 2,528-byte chapter at those holds.
- The following dialogue, four crew notices and normal Hangzhou handoff remain
  intact. The actual before/after/following/Town sheet was opened.
- The separate 24,100-frame ordinary Rafael New Game run matches all 89 V678
  title, selection, story and Town screenshots, without a save or fixture.

The other three deep records receive complete source/QA/preview and original
native printf checks, not newly visited live-parent credit. These are targeted
automated emulator tests, not whole routes, earned Maria access or hardware
verification. User cold-boot acceptance should cover title/New Game, Maria's
corrected report and Hangzhou handoff; the other repaired tutorial/exchange
contexts remain useful later gameplay checks.

## Remaining work

All 18 plaque/hint audit entries remain incomplete; all 22 historical requirement
objects keep their exact scope. Three inherited blank scene holds retain their
unresolved original wait/padding classification. Six small controls, eight cards,
actual comic/legacy contexts and plaque/material acceptance remain open. No guide
approval is inferred from the isolated unlock save. Online exclusions and source
brown-mark preservation remain effective.

The requested older-record review is retained. One concrete follow-up is
SC3 B33 R0107, observed at frame 20200: the older sentence “Abroad exposed their
wrongdoing” needs naturalness/fidelity review against Yukihisa's source account
of learning his countrymen's misconduct abroad. Its glyph evidence is not an
editorial approval. This four-record format fix does not silently rewrite it.

## Reproduction and evidence

- `prepare_story_percent_v685`, three `audit_dialogue_batch` reports,
  `register_story_percent_v685`, registered integrated builder,
  `verify_story_percent_v685`, `run_story_percent_v685` and
  `finish_story_percent_v685`.
- New stage: `dk4tool/patch/story_literal_percent.py`; final guard:
  `dk4tool/script/format_safety.py`; focused tests:
  `tests/test_story_format_safety.py`.
- Full proofs, preserved draft failures, previews and test XML:
  `work/analysis/story_percent_v685/` on E.
- Captures: E Generated/work/emulation_v193 `story_percent_v685_*`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V685 Story percent repairs`.

The latest experimental compiled pointer advances to V685. The canonical and
V610 verified pointers remain unchanged. No acceptance, canonical promotion,
commit, push or graphics-goal completion is claimed.
