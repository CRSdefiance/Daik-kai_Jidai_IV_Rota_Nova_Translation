# Confirmed names: COMMON and HELP editorial review

## What changed

The settled names remain Rafael, Hodram, Joakim, Camille and Maria Huamei Li.
This review completes the source/context/natural-English review of the five
nonroute draft owners left by the V198 name-migration preparation. The one packed
owner contains four independently selected messages, so the work covers **six
native COMMON entries and two HELP articles**. V218 remains the registered ROM;
these manuscripts are not a playable release.

The previous turn verified existing naming documents without changing their
decisions or implementation: it was **no progress toward the graphics goal**.
This turn supplies corrected authoritative manuscripts, complete native entry
identities, an allocation proposal, rendered previews and execution evidence.

## English and source fidelity

| Native message | Reviewed English | Reason |
|---|---|---|
| 1360 | ... (I don't understand the words.) | Does not invent partial foreign-language proficiency. |
| 1361 | Yes, that's a lovely sound. | Preserves the warm response to the sound/timbre. |
| 1362 | ...That's quite well done... | Keeps the restrained approval and hesitation. |
| 1363 | Zzz... Honestly, Camille... Zzz... | Preserves the sleepy, mildly exasperated address and snores. |
| 1683 | I can't keep relying on Camille forever... | Restores natural self-reflection and continuing reliance. |
| 1830 | Am I going to die...? Camille... | Restores the source's uncertainty; “Dying” wrongly made it definite. |

The six native entries have individual source, context, localization and
naturalness review. Ambient/battle/health entries are response variants; neighboring
entries are not assumed to be consecutive speech by one fixed actor. No family
relationship, rank or death outcome is invented. Reserved uppercase I/F retain
the existing safe full-width glyph encoding; editable prose contains no alignment
spaces or authored line breaks.

Rafael's HELP article now preserves Lisbon's Mediterranean region, the accessible
start with many companions, the military investment discount and **doubled
Influence gain** for discovering ruins/items. The older “double power” draft lost
the stat's meaning. Its heading and advantages remain distinct semantic sections.

Military Investment now includes **Palace and Governor's Office**, 1–20 units,
gold costs of 50 percent of the city's Arms rating (40 percent for Rafael), raised
Arms, both market-share conditions, reduced likelihood of surrender under attack,
and access to better ships/cannons. The older explanation omitted conditions and
weakened the result to “may rise.” Literal percentages remain spelled out for
printf safety. No shortened text is substituted merely to fit old allocations.

## Correct native identity and allocation

Clean B16 R0051 contains global IDs **1360–1363**. In V218 their physical owner is
B16 R0055. Clean B19 R0008/message1683 is now B18 R0104; clean B20 R0030/message1830
is now B19 R0113. The V198 draft's physical canonical R0051 source actually selects
an unrelated spotted-city/fleet report. It must **not** be used as the native lock
for the four ambient responses, nor can its pipe-joined English be shipped as one
message. Use the clean global IDs and current native locks recorded in the new
manuscript.

The proposed whole-owner allocation preserves all four packed responses, their
separate entry starts and all native global IDs. It compares every one of the
**3,668** selected messages: the six authored messages are exact, and the other
**3,662** are byte-exact, including padding. No unrelated English padding is
compacted. All 41 cache blocks remain within 4,096 bytes. The largest native copy
remains **444 bytes**, within the 512-byte output buffer. Only the COMMON payload
and native directory/offset tables change in the proposal; executable loader code
and all unrelated ARM9 bytes are preserved.

The two complete HELP articles exceed their old allocations even before layout:
317 prose bytes versus283, and493 versus392. Their allocation and native article
consumer remain open. The structured manuscript preserves heading/paragraph/
advantage roles and does not pretend that flattened prose or a passing COMMON
loader proves HELP presentation.

## Verification and limits

- Six exact-font previews reviewed on `work/qa/confirmed_name_common_v228/sheet_0.png`.
  Zero formatting blockers; complete initial/final letters and punctuation fit.
- Eighteen actual ARM9 selector/loader/copy cases: six warm, six cold-cache and six
  unchanged neighboring messages. Cold cases execute the native header/block read
  path with explicit host file-read bridges. Text, terminal NUL, output guards and
  stack survive.
- These are allocation/copy and offline layout checks. Final macro expansion,
  physical text pixels, actor/portrait binding, scene transitions and gameplay are
  separate. No candidate promotion or whole-game correctness is claimed.

## Authoritative artifacts

- `translations/confirmed_name_common_manuscript_v1.json`: six source-locked entries.
- `translations/confirmed_name_help_manuscript_v1.json`: two complete structured articles.
- `work/analysis/confirmed_name_common_v228/editorial_review.json`.
- `work/analysis/confirmed_name_common_v228/native_proof.json` and `allocation_plan.json`.
- `work/qa/confirmed_name_common_v228/report.json` and all six previews.
- `scripts/prepare_confirmed_name_common_v228.py` and `verify_confirmed_name_common_v228.py`.

The other route-name drafts still need individual editorial/layout review and
registered integration. Four Online screenshot bodies, unresolved raw/embedded
consumers, native crop/alpha checks and final combined ROM/patch/gameplay remain
within the original graphics goal. The goal stays active. At completion, revisit
the older record-based checks as requested.
