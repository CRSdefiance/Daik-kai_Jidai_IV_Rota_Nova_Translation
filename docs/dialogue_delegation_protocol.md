# Delegated dialogue translation protocol

This protocol makes large dialogue batches safe to delegate to Terra or another
translator without asking that translator to understand ROM layout. It does not make
unreviewed prose correct by itself. The tools prove structure and presentation; a
localization review proves meaning and voice.

## Responsibility boundary

The translator owns only:

- the faithful meaning of the clean Japanese source;
- idiomatic American English;
- character voice and scene continuity;
- a short source gloss and localization note.

The formatter/build system owns:

- line breaks, effective line width, and maximum lines;
- speaker and runtime macros;
- fixed record allocation and padding;
- detection of blank-page risk, dropped-glyph risk, and placeholders;
- deterministic previews and release ancestry.
- protected-break ASCII pair phase, including any invisible pre-LF repair byte.

The translator must never add spaces for visual alignment, preserve Japanese line
breaks, copy an older English draft, shorten a line merely to fit, or edit encoded
bytes. Ordinary prose is one paragraph ending in `{PAD}`.

## Required `natural-dialogue-v2` record

Every new record supplies `id`, `english`, `speaker`, `context`, `source_meaning`,
`localization_note`, and a per-record `review` object whose five required gates are
`source`, `context`, `localization`, `naturalness`, and `formatting`. Batch-level
review declarations are not enough in v2.

An explicit `{LB}` is exceptional. It requires `manual_break_reason`, appears only at
a true dramatic pause or paragraph boundary, and will still appear as a warning in
the QA report. `{LB@...}`, `{ALIGN@...}`, leading breaks, consecutive breaks, and
authored alignment spaces are forbidden.

## Mandatory batch loop

1. Extract records and immediate neighbors from the clean Japanese ROM. Never use a
   translated candidate as source.
2. Write a faithful source gloss before writing localized English.
3. Localize for `en-US`, preserving facts and intent rather than Japanese syntax.
4. Read the English aloud with the previous and next records. Record any deliberate
   adaptation in `localization_note`.
5. Run the exhaustive audit:

   ```text
   python scripts/audit_dialogue_batch.py --rom out/raphael_natural_v2_accepted_base.nds --japanese-rom work/clean.nds --batch <batch.json> --out work/qa/<batch-name>
   ```

6. Open `summary.md` and every generated PNG. The preview deliberately displays the
   current 6-pixel native continuation indent. Do not add spaces to cancel it.
7. Resolve every error and warning. A warning may be waived only with a narrow
   `qa_waivers` entry on that record and a written `qa_waiver_reason` (or v2
   `localization_note`). The normal audit and the integrated release builder both
   fail on unwaived warnings; an undocumented waiver also fails the build.
8. Build only through the batch's registered release profile and run the baseline,
   manifest, and feature verifiers in `build_continuity_protocol.md`.
9. Cold-boot a representative scene sample. Deep-game batches no longer require a
   human to visit every text box, because every record receives offline structural
   QA and a rendered preview; however, scene transitions, portraits, control flow,
   and a statistical sample still require live testing.

## What the audit guarantees

For every record, the report records the clean Japanese source, localized text,
formatted markup, visible lines, line widths, automatic/manual break counts, fixed
padding, engine guard indent, diagnostics, and an exact-font PNG preview. It blocks
bad controls, unsafe macro bytes, overflow, padding-created blank pages, manual-wrap
debt, weak line endings, orphaned final lines, authored leading spaces, and known
diagnostic placeholders.

The release builder repeats these checks from the canonical source bytes. A report
generated earlier cannot become a stale permission slip after the text is edited.

It cannot prove that an English sentence is faithful, funny, or in character. Those
remain explicit per-record editorial gates and should be reviewed by a second person
or model for large delegated batches.

## Renderer limitation

Cold-boot testing is authoritative over static inference. The 2026-08-10 bare-`0A`
candidate visibly moved the first character after a break to the preceding line
(`man o/f`, `n/ow`, `B/ehold`, `when w/e`). The traced routine was a layout/parser
layer, not sufficient proof of the progressive story renderer's display timing.

Raphael work must use `raphael-story-live`. It emits protected `0A 20` breaks and uses
the default route's measured `FI`/`FA`/`FO` widths. The `story-clean-revoked` profile
exists only to reproduce the failed experiment and is forbidden in release profiles.
No translator may insert manual leading spaces. Removing the remaining one-cell guard
indent requires a separately isolated renderer patch or a proven zero-width guard.

The accepted zero-cursor experiment additionally requires pair-phase-safe protected
breaks. The encoder tracks printable ASCII phase across the entire record, ignores
speaker/control and multibyte CP932 units, applies declared runtime-macro expansion
parity, and inserts a pre-LF space only at the unsafe phase. That repair is deliberately
absent from translator markup. Unknown macro parity and fixed-allocation overflow are
hard errors, never requests for a translator to add spacing by hand.

## Promotion rule

A QA-clean translation batch is still experimental. It becomes accepted only after
the user cold-boots the integrated candidate and explicitly approves it. Automated
success never authorizes replacing the canonical baseline or promoting a layer.
