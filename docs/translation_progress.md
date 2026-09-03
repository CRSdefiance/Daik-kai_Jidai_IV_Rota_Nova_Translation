# Translation progress

Generated: 2026-09-03 13:31 US Eastern Daylight Time

This is a rough, record-based estimate. A translated record can be one short label or several dialogue lines, so the percentage is a navigation aid rather than a word-count claim.

| File | Translated records | Detected records | Approx. complete |
|---|---:|---:|---:|
| `/COMMON/MESFILE.DK4` | 2238 | 2807 | 79.7% |
| `/COMMON/HELP.DK4` | 194 | 194 | 100.0% |
| `/data/SC0.DK4` | 331 | 6768 | 4.9% |
| `/data/SC1.DK4` | 174 | 5166 | 3.4% |
| `/data/SC2.DK4` | 205 | 6608 | 3.1% |
| `/data/SC3.DK4` | 0 | 5010 | 0.0% |
| **Tracked text total** | **3142** | **26553** | **11.8%** |

## Shared dialogue milestone

`/COMMON/MESFILE.DK4` has passed the 50% milestone by **834 records** (2238 translated; the threshold is 1404 of 2807).

- Milestone reference—blocks B00-B14: 932 records (33.2%).
- Through B18: 1359 cumulative records (48.4%).
- The first 45 records from B19 reached the exact 1404-record halfway mark.
- Each block still requires an internal-entry-point audit before insertion; record count alone cannot prevent missing first letters.

## Accepted interface progress

- **Extras and Online:** complete accepted English pass for both Extras choices, all feature and tie-in pages, the Online banner, and all 13 baked text cards.
- **Options and Sound Setup:** the full `Options` label, prompts, all 38 BGM titles, and all 57 SFX titles are accepted.
- **Town Common menu:** all six radial labels and the Info, Functions, Options, Save/Load, Deck, Assign Sailors, and empty-Items paths covered by V6 are accepted.
- **Canonical accepted baseline:** `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf`.

## Other tracked work

- ARM9/UI dictionary: 810 mapped slots have English replacements. This is not shown as a percentage because the full set of text-bearing ARM9 slots has not yet been exhaustively classified.
- Redrawn graphics and fixed ARM9 labels are tracked by source-locked translation batches and the accepted-layer registry; they are not included in the table above.
- An in-game save can retain old names and labels. Coverage is measured against the clean ROM and translation sources, not save-state contents.

## How to refresh

Run `python scripts/build_translation_progress.py` after adding or revising translation batches.
