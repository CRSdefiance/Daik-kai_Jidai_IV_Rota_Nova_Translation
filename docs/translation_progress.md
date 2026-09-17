# Translation progress

Generated: 2026-09-11 10:45 US Eastern Daylight Time

This is a rough, record-based estimate. A translated record can be one short label or several dialogue lines, so the percentage is a navigation aid rather than a word-count claim.

| File | Translated records | Detected records | Approx. complete |
|---|---:|---:|---:|
| `/COMMON/MESFILE.DK4` | 2238 | 2807 | 79.7% |
| `/COMMON/HELP.DK4` | 194 | 194 | 100.0% |
| `/data/SC0.DK4` | 897 | 6768 | 13.3% |
| `/data/SC1.DK4` | 174 | 5166 | 3.4% |
| `/data/SC2.DK4` | 212 | 6608 | 3.2% |
| `/data/SC3.DK4` | 0 | 5010 | 0.0% |
| **Tracked text total** | **3715** | **26553** | **14.0%** |

## Shared dialogue milestone

`/COMMON/MESFILE.DK4` has passed the 50% milestone by **834 records** (2238 translated; the threshold is 1404 of 2807).

- Milestone reference—blocks B00-B14: 932 records (33.2%).
- Through B18: 1359 cumulative records (48.4%).
- The first 45 records from B19 reached the exact 1404-record halfway mark.
- Each block still requires an internal-entry-point audit before insertion; record count alone cannot prevent missing first letters.

## Lil route editorial progress

Lil's actual `/data/SC2.DK4` route has **240** source-reviewed natural-English draft records across B22 (49), B23 (35), B27 (49), B66 (72), B146 (35).
- B22 now has a complete 49-record fixed-allocation runtime layer with Lil/Kamil/Emilio/Fernando selectors and Lil-route name macros mapped. It was accepted in the cumulative 2026-09-17 baseline.
- The accepted B22 shared-data layer additionally covers Kamil's global `Overijssel` surname, all shared fleet-name formatter pointers, the crew-join first-letter guard, and the screenshot-reported Bruges region/hemp/location labels.
- B23 covers the immediate Deck-post tutorial and has a seven-record control probe; B27, B66, and B146 are retained under historical Hodram filenames after their route ownership was corrected.

## Accepted interface progress

- **Extras and Online:** complete accepted English pass for both Extras choices, all feature and tie-in pages, the Online banner, and all 13 baked text cards.
- **Options and Sound Setup:** the full `Options` label, prompts, all 38 BGM titles, and all 57 SFX titles are accepted.
- **Town Common menu:** all six radial labels and the Info, Functions, Options, Save/Load, Deck, Assign Sailors, and empty-Items paths covered by V6 are accepted.
- **Accepted Deck patch:** all compact room names, requirement and restriction strings, ability names, the Y-button `Crew` label, all 71 previously overlong activity responses, and the final inherited Deck placeholder are included in the accepted V10 baseline.
- **Lil, Guild, and port integration:** Lil's complete 49-record Amsterdam opening, shared names and fleet formats, Guild and Inn labels, all 218 item names, Amsterdam Guild descriptions, and the current Hodram/market/shipyard/cargo/sea repairs are accepted and baked.
- **Canonical accepted baseline:** `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.

## Other tracked work

- ARM9/UI dictionary: 851 mapped slots have English replacements. This is not shown as a percentage because the full set of text-bearing ARM9 slots has not yet been exhaustively classified.
- Redrawn graphics and fixed ARM9 labels are tracked by source-locked translation batches and the accepted-layer registry; they are not included in the table above.
- An in-game save can retain old names and labels. Coverage is measured against the clean ROM and translation sources, not save-state contents.

## How to refresh

Run `python scripts/build_translation_progress.py` after adding or revising translation batches.
