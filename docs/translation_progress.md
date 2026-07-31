# Translation progress

Generated: 2026-07-31 08:41 US Eastern Daylight Time

This is a rough, record-based estimate. A translated record can be one short label or several dialogue lines, so the percentage is a navigation aid rather than a word-count claim.

| File | Translated records | Detected records | Approx. complete |
|---|---:|---:|---:|
| `/COMMON/MESFILE.DK4` | 1404 | 2807 | 50.0% |
| `/COMMON/HELP.DK4` | 194 | 194 | 100.0% |
| `/data/SC0.DK4` | 258 | 6768 | 3.8% |
| `/data/SC1.DK4` | 0 | 5166 | 0.0% |
| `/data/SC2.DK4` | 0 | 6608 | 0.0% |
| `/data/SC3.DK4` | 0 | 5010 | 0.0% |
| **Tracked text total** | **1856** | **26553** | **7.0%** |

## Shared dialogue 50% target

`/COMMON/MESFILE.DK4` needs **0 more records** to reach 50% (1404 of 2807).

- Complete blocks B00-B14: 932 records (33.2%).
- Then complete B15-B18: 1359 cumulative records (48.4%).
- Translate 45 records from B19 to reach the exact 1404-record halfway mark.
- Each block still requires an internal-entry-point audit before insertion; record count alone cannot prevent missing first letters.

## Other tracked work

- ARM9/UI dictionary: 690 mapped slots have English replacements. This is not shown as a percentage because the full set of text-bearing ARM9 slots has not yet been exhaustively classified.
- The name/faction/place audit covers 89 world-city, town, port, and settlement slots, recurring commodity slots, twelve additional faction slots, 188 shared character-name slots, and 119 ship-model slots. Shared offsets propagate these names across city, palace, market, tavern, route-map, and shipyard screens.
- Redrawn graphics are tracked by the resource lists in `scripts/build_graphics_translation.py`; graphical text is not included in the table above.
- An in-game save can retain old names and labels. Coverage is measured against the clean ROM and translation sources, not save-state contents.

## How to refresh

Run `python scripts/build_translation_progress.py` after adding or revising translation batches.
