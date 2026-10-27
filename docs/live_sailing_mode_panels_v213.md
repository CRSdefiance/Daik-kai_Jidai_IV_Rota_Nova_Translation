# Three confirmed Japanese sailing panels V213

2026-10-07. Previous turn verified RACE records and identified generated help
paths. This turn confirms three additional on-screen Japanese panels and prepares
complete English. **No ROM change; V211 remains current and full goal active.**

## Actual normal-gameplay evidence

A fresh V211 cold boot reaches ordinary sailing. Three successive Y presses
select Info, Search and Declare War. Captures 17400, 17900 and 18400 show Japanese
instructions on the upper screen; source/PNG/ROM hashes and the input schedule are
saved. No savestate or memory injection is used. These are real remaining screens,
not a prediction from preserved strings or a fixture forcing an unused reader.

| Panel | Source start | Pointer site | Original bytes including NUL |
|---|---|---|---:|
| Info | `02147778` | `0206F424` | 141 |
| Search | `02147540` | `0206F418` | 305 |
| Declare War | `02147674` | `0206F420` | 257 |

The active parent calls the real overlay renderer at `01FFB4BC`, then transfers
the produced bitmap. It parses CP932 character pairs; ASCII replacement cannot
be assumed compatible. Original fullwidth spaces encode layout and must not be
copied into natural English prose as unexplained padding.

The earlier raw-mode queue is a different path. Its setter takes destination,
type and index; inspected direct callers pass types 0,3–8. The new live evidence
therefore does not claim that the old queued help types 10/11 are selected. The
actual on-screen source allocations above are authoritative for this work.

## Reviewed complete English

**Info Mode:** View information about the cities and ships on screen. Select a target.

**Search Mode:** Press A to search. You may find water, food, items, or other supplies.
If you find nothing, sailor fatigue rises by 3. Sailors may desert or be attacked
by wild animals while searching.

**Declare War Mode:** Select a fleet or city on screen to begin a battle. Declaring
war puts you at war with that faction and greatly lowers goodwill. You cannot
declare war on an allied faction's fleets.

The manuscript records clean Japanese, observed control/context, meaning and
localization reasons. Search preserves the exact fatigue increase and does not
wrongly tie every desertion/animal attack exclusively to failure. War preserves
the explicit fleet-specific alliance restriction. All three bodies are logical
paragraphs; the eventual formatter owns line breaks.

Source, context, localization and naturalness are reviewed. Formatting and native
English display remain explicitly false. This is not a registered layer or a
claim that the screens are fixed. Do not truncate complete prose or force plain
ASCII into the CP932-pair renderer to satisfy old byte capacities. Next work is
native buffer/layout calibration and safe English production, then full integration
and direct first/last-letter/display checks on these same mode screens.

## Artifacts and full scope

- `translations/sailing_mode_panels_manuscript_v1.json`.
- `work/analysis/generated_modes_v213/live_source_proof.json`.
- `work/emulation_v193/generated_modes_v213/` captures, read-only final RAM export
  and capture report.

These three live panels are additional remaining work; the historical PXL/FLS
inventory of four unfinished Online files is not used to hide them. Naming,
other raw/embedded/contextual/native/gameplay gates and the final combined
ROM/patch remain in the goal. No completion or user acceptance is implied.
