# V1653 Search report editorial review

The coverage ledger now records **1,519 source/prose reviews**, including **1,350
completed entries** (1,009 revised and 341 retained). There are **169 reviewed but
incomplete COMMON entries**: the earlier 144, hot-spring13 and notice310, and these
11 Search reports. Broader shared, route and other player-facing prose remains.

## New source review

Clean Japanese and original callers were reviewed for COMMON312,2217–2221 and
2229–2233. The old failure reports omitted the expedition's return; some also
collapsed tentative findings and hearsay. The five foraging reports all used the
same terse quantity labels. New natural English drafts restore the source facts,
tone and report structure. The crew-loss status removes its old authored newline
and trailing padding.

The original empty-search consumer uses role1/table02116EC0. The foraging consumer
uses role7/table02116E80 and two original formatted quantities, water then food,
before adding those same supplies. COMMON312 is a distinct numeric modal. These
contracts must remain separate in native formatting and release verification.

- Manuscript: `translations/search_reports_editorial_manuscript_v1.json`.
- Exact Japanese/current references, tables, unchanged caller code and surrounding
  entries: `work/analysis/search_reports_source_v1653/clean_source_and_original_consumers.json`.
- Coverage receipt: `work/analysis/search_reports_source_v1653/source_prose_review_receipt.json`.

These are **source/prose drafts**, with the formatting review gate explicitly
false. They are not integrated in a ROM and receive no completion credit. Full
native argument expansion, fonts, line boundaries, copies, release/patch and
revised gameplay verification remain pending.

## Continuing hot-spring verification

V1637 remains the experimental cumulative candidate; V1492 remains promoted.
The optional relaxation/Experience branch is still pending. The earlier run
`hot_spring_notice_resilient_v1645_1637` is terminal at53178 on Assign Sailors,
with a complete input/fixture/4MiB RAM/capture/source-save audit at
`work/analysis/hot_spring_resilient_terminal_v1650a/terminal53178_preservation.json`.
This is not a normal Sea View return or an editorial completion.

The first navigator could mistake stale loaded dialogue for a live message after
a zero-crew warning opened Assign Sailors. It sent repeated A inputs there. This
was a test-navigation error, not a ROM text defect; every input remains in the
journal. The successor requires a visible dialogue panel and stops at other UI.
Its paper/control feature tests are navigation checks, not glyph verification.

A new source-save cold boot replays the original prefix through42673. A separately
preflighted fixture restores only10 live crew bytes to the original persisted
counts49/19/19/19/19; it preserves hull, all persisted models, actors, skills,
fatigue, RNG, code and every other RAM byte. This uses the user's permission for
test-support cheats and is not earned recruitment. Existing48-byte locations and
20-byte original-method supply refills are also explicitly recorded and audited.
The original event selection and optional branch remain unmodified.

At57475/57505 the original discovery2276 appeared, followed by recovery309 at
57725/57755. Both final captures were viewed. A normal A acknowledgement returned
to the viewed Sea View57975 without optional relaxation or310. These observations
do not close the pending batch. The active runner/journal and next action belong
in `docs/editorial_handoff_current.md` after the current run is checkpointed.

Separate graphics/all18 plaques and the later older-record re-audit remain open.
No full route or hardware verification is claimed.
