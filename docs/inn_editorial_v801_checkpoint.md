# V801: Inn source, context and English review

The next 23 COMMON entries, 1177–1199, have a clean-source/context/prose pass:
19 proposed revisions and four retained wordings. These are drafts, not completed
production translations. The current registered combined ROM remains V799.
The ledger now records 553 source/prose reviewed and 527 editorially complete;
the three older context drafts 750–752 and these 23 Inn drafts remain open.

## Proven context

- Original Innkeeper provider B2CD8 resolves facility role 8 to actor 142 in
  Istanbul. The actual portrait/name and active message cache are captured.
- Ten original stay-caller fragments cover the one-night fee, goodnight,
  multi-night question, all 3/10/30-night confirmations, hospitality,
  both insufficient-funds callers and early departure inside the rest loop.
- Role 2 is Japanese 参謀, Strategist. Original 53F4C selects 1186–1193 from
  table 021180E0; 208 native actor/voice cases and three original company-name
  caller fragments pass. The donor has no assigned Strategist, so the ordinary
  baseline does not prove actual report activation.
- Original market consumer 5CC70 selects 1182/1183 for a price crash and
  1184/1185 for a buyout. Arguments are town, goods and affected company.
  1185 describes the company's disappointment at missing the purchase.
  Its old faction-opposition question is unrelated and is replaced in the draft.
- Original battle/raid callers supply relative month first, not the player name.
  Six selected-event fragments bind the three event types and two outcomes.
  1195/1196 can have a town or a company as their subject. 1197/1198 concern
  a company attacking a town. Selected-event fixtures do not prove eligibility.
- All 144 pairs of source calendar month values verify the relative-month
  provider, including the year boundary.

Proofs: `work/analysis/inn_context_v801/native_context.json` and
`work/analysis/inn_context_v801/baseline_and_time_ownership.json`.

## Completed baseline emulator run

The DeSmuME run cold-boots V799 with an isolated copy of the protected Istanbul
donor, without a savestate or new fixture. Session 30596 exited successfully at
8,600 frames, and its terminal report has no callback errors. Five active message
IDs, 1177–1181, match exact current templates in the native cache. The one-night
stay changes cash 8371→8370 and advances 48 calendar ticks. The three-night stay
changes cash 8370→8367 and advances 144 ticks. The original menus return normally
and B returns to town. These are baseline scenes, not revised-English verification.
The original donor hash remains unchanged.

Captures/report:
`E:/Rota Nova translations/Generated/work/emulation_v193/inn_v801_context/`.

## Manuscripts and next work

`translations/inn_editorial_manuscript_v1.json` preserves the initial reviewed
draft. V2 changes only the optional `for` in 1180: “You're staying %s nights,
then?” All three original durations now fit one line. The remaining 22 paragraphs
are exact. `translations/inn_time_phrases_manuscript_v1.json` reviews complete
relative-month phrases instead of abbreviations.

Production formatting gates remain false until COMMON repacking, native copies,
registered release reconstruction and revised actual scenes are verified. Continue
with the V802 research described below; do not re-inventory this family or count
its drafts as complete. The full editorial goal and separate graphics audit remain
unfinished.
