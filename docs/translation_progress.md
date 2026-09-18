# Translation progress

Generated: 2026-09-18 09:19 US Eastern Daylight Time

This is a rough, record-based estimate. A translated record can be one short label or several dialogue lines, so the percentage is a navigation aid rather than a word-count claim.

| File | Translated records | Detected records | Approx. complete |
|---|---:|---:|---:|
| `/COMMON/MESFILE.DK4` | 2313 | 2807 | 82.4% |
| `/COMMON/HELP.DK4` | 194 | 194 | 100.0% |
| `/data/SC0.DK4` | 6689 | 6768 | 98.8% |
| `/data/SC1.DK4` | 5108 | 5166 | 98.9% |
| `/data/SC2.DK4` | 1834 | 6608 | 27.8% |
| `/data/SC3.DK4` | 0 | 5010 | 0.0% |
| **Tracked text total** | **16138** | **26553** | **60.8%** |

## Shared dialogue milestone

`/COMMON/MESFILE.DK4` has passed the 50% milestone by **909 records** (2313 translated; the threshold is 1404 of 2807).

- Milestone reference—blocks B00-B14: 932 records (33.2%).
- Through B18: 1359 cumulative records (48.4%).
- The first 45 records from B19 reached the exact 1404-record halfway mark.
- Each block still requires an internal-entry-point audit before insertion; record count alone cannot prevent missing first letters.

## Route translation progress

- **Raphael (`/data/SC0.DK4`):** the V93 route profile translates every remaining visible Japanese record. Residual unmatched records in the table include controls, nontext payloads, and records whose translated layers do not use the ordinary one-record/one-ID accounting model.
- **Hodram (`/data/SC1.DK4`):** the V32 route profile covers the complete story and all Japanese-bearing records identified by the route audit, while preserving the one verified nontext event payload.
- **Lil (`/data/SC2.DK4`):** V21 is integrated with **240** source-reviewed natural-English draft records across B22 (49), B23 (35), B27 (49), B66 (72), B146 (35).
- Lil B22 has a complete 49-record source-locked runtime layer with the Lil/Kamil/Emilio/Fernando selectors and route name macros mapped; it is included in the unified route candidate.
- B23 covers the immediate Deck-post tutorial and has a seven-record control probe; B27, B66, and B146 are retained under historical Hodram filenames after their route ownership was corrected.
- The unified profile combines Raphael V93, Hodram V32, Lil V21, the Amsterdam opening, shared interface layers, and the global COMMON spacing repair.

## Integrated interface progress

- **Extras and Online:** complete accepted English pass for both Extras choices, all feature and tie-in pages, the Online banner, and all 13 baked text cards.
- **Options and Sound Setup:** the full `Options` label, prompts, all 38 BGM titles, and all 57 SFX titles are accepted.
- **Town Common menu:** all six radial labels and the Info, Functions, Options, Save/Load, Deck, Assign Sailors, and empty-Items paths covered by V6 are accepted.
- **Accepted Deck patch:** all compact room names, requirement and restriction strings, ability names, the Y-button `Crew` label, all 71 previously overlong activity responses, and the final inherited Deck placeholder are included in the accepted V10 baseline.
- **Runtime text safety:** the unified candidate validates packed-entry boundaries, renderer guards, literal-percent safety, dynamic F-initial crew names, full-name separators, and COMMON automatic wrapping.
- **Canonical accepted baseline:** `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.

## Other tracked work

- ARM9/UI dictionary: 852 mapped slots have English replacements. This is not shown as a percentage because the full set of text-bearing ARM9 slots has not yet been exhaustively classified.
- Redrawn graphics and fixed ARM9 labels are tracked by source-locked translation batches and the accepted-layer registry; they are not included in the table above.
- An in-game save can retain old names and labels. Coverage is measured against the clean ROM and translation sources, not save-state contents.

## How to refresh

Run `python scripts/build_translation_progress.py` after adding or revising translation batches.
