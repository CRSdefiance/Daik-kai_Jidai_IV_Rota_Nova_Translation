# Translation progress

Generated: 2026-08-18 US Eastern Daylight Time

This is a rough, record-based estimate. A translated record can be one short label or several dialogue lines, so the percentage is a navigation aid rather than a word-count claim.

The detailed SC0 block inventory is in [`sc0_block_map.md`](sc0_block_map.md); it lists every internal block, record count, current coverage, and known route ownership.

## 2026-08-20 accepted Raphael baseline

- Raphael: all 331 currently identified records have source-first
  `natural-dialogue-v2` coverage. Of these, 304 build-safe records, including the five
  parity-preserving expanded opening records, are baked into
  `out/raphael_natural_v2_accepted_base.nds`. The accepted baseline now also contains
  the parity-preserving 106-record Lisbon expansion, fixed-offset centered tutorial
  choices, and repaired shared crew-join template. The remaining 27 translated records
  are explicitly quarantined for unmapped controls or allocation limits.
- Lil: all 162 currently identified records now have source-first English drafts
  (113 in SC1 and the 49-record SC2 block-22 opening). They remain non-buildable
  pending Lil-specific leading-state, macro parity, portrait/name-preamble, and
  relocation work. Draft coverage must not be confused with playable coverage.

| File / container | What it contains | Translated records | Total records | Approx. complete |
|---|---|---:|---:|---:|
| `/COMMON/MESFILE.DK4` | Shared menus, town dialogue, common prompts | 1404 | 2807 | 50.0% |
| `/COMMON/HELP.DK4` | Help/tutorial records (194 unique records; raw table has duplicate/pointer rows) | 194 | 194 | 100.0% |
| `/data/SC0.DK4` | Raphael route/story and related scene text (all 331 identified Raphael records covered) | 331 | 6768 | 4.9% |
| `/data/SC1.DK4` | Lil/Argot route and scene text | 113 | 5166 | 2.2% |
| `/data/SC2.DK4` | Hodram/Bergstrom route and scene text | 156 | 6608 | 2.4% |
| `/data/SC3.DK4` | Other route/event scene text | 0 | 5010 | 0.0% |
| `/data/DECKCHIP.DK4` | Deck/ship-chip binary asset; generic scanner produced 29 false positives | 0 | 0 confirmed text records | Not a text table |
| `/data/WORLDMAP.DK4` | Mixed world-map binary data; the generic scanner's 1,279 apparent Japanese records are false positives | 0 | 0 confirmed text records | Not a text table |
| `/__arm9__.bin` | ARM9 UI, names, city/faction/commodity tables (audited slots) | 685 | 685 | 100.0% |
| **Indexed text total** | **All extractable text containers above** | **2882** | **27267** | **10.6%** |

### Containers requiring a separate binary extractor

| File | What it likely contains | Translation status |
|---|---|---|
| `/data/EV0.DK4` | Event/cutscene resources | Not yet indexed; total cannot be reported reliably |
| `/data/EV1.DK4` | Event/cutscene resources | Not yet indexed; total cannot be reported reliably |
| `/data/EV2.DK4` | Event/cutscene resources | Not yet indexed; total cannot be reported reliably |
| `/data/EV3.DK4` | Event/cutscene resources | Not yet indexed; total cannot be reported reliably |
| `/data/WORLDMAP.DK4` | World-map binary data | Not a generic text table; requires a format-specific map-data extractor before any text can be identified safely |

## Shared dialogue 50% target

`/COMMON/MESFILE.DK4` needs **0 more records** to reach 50% (1404 of 2807).

- Complete blocks B00-B14: 932 records (33.2%).
- Then complete B15-B18: 1359 cumulative records (48.4%).
- Translate 45 records from B19 to reach the exact 1404-record halfway mark.
- Each block still requires an internal-entry-point audit before insertion; record count alone cannot prevent missing first letters.

## Other tracked work

- ARM9/UI dictionary: 685 audited text-bearing slots currently have English replacements. This covers the extracted ARM9 audit table, not every arbitrary byte sequence in the binary.
- Route-specific coverage currently includes 162 identified Lil drafts and 156
  Hodram/Bergstrom records. Neither figure proves a complete route because event
  containers and many scene blocks remain unmapped.
- The percentages count records, not words. A long dialogue record has the same weight as a one-word label.
- Redrawn graphics are tracked by the resource lists in `scripts/build_graphics_translation.py`; graphical text is not included in the table above.
- An in-game save can retain old names and labels. Coverage is measured against the clean ROM and translation sources, not save-state contents.

## How to refresh

Run `python scripts/build_translation_progress.py` after adding or revising translation batches.
