# Original Online screenshot source search (research V190)

2026-10-05. The graphics goal remains active and incomplete. The latest combined
ROM is V189; **V190 here names research, not a compiled candidate**.

## Sources recovered

- The [April/May 2004 gallery](https://www.4gamer.net/store/shots/daikoukai_ol/index.html)
  and its second page contain 29 original game screenshots.
- The [June 2004 customization gallery](https://www.4gamer.net/store/shots/daikoukai_ol_2/index.html)
  and its second page contain 30 original game screenshots.
- A public archive index recovered 72 publisher image URLs captured in 2003–2005.
  Eight selected publisher images remain directly accessible: six character scenes
  and two promotional/price banners. None supplies the four required frames.

All 59 gallery images and the eight selected publisher images were saved with
their actual URL, SHA-256 and dimensions. Gallery page links were followed rather
than assigning guessed screenshot filenames. The publisher paths were obtained
from the archive index. Current publisher downloads are **not asserted to be
byte-identical to their historical capture**; the archive timestamp identifies
discovery provenance, and the fetched URL/hash identify the downloaded evidence.

## Matching and visual review

All 23 real Online screenshot selections were extracted from the immutable
canonical ROM. Each was compared against all 59 gallery images (1,357 comparisons).
Mean RGB error at 64x48 ranks possible matches; it does not identify dialogue,
establish source authority, or prove absence of Japanese. Four comparison sheets
show each canonical frame beside its four highest-ranked candidates. The two
gallery contact sheets per collection and these four comparison sheets were reviewed.
The eight publisher images were reviewed on their separate contact sheet.

| Pending resource | Result in these collections |
| --- | --- |
| Online24 | No matching character information modal, values and chat frame. Similar ships do not supply the missing labels or transcript. |
| Online27 | No matching bazaar/tree/bubble/chat composition. Existing exact official bubble evidence is retained; chat from another market scene is not substituted. |
| Online31 | No matching two-portrait ruins/dialogue/chat composition. Images of the same characters or ruins do not establish the displayed sentence. |
| Online33 | No matching two-tab status modal and chat frame. Similar tavern backgrounds do not establish the modal's text or values. |

No larger exact copy of these four frames was found in the reviewed collections.
This is a result about these specific collections, **not an assertion that no
larger originals exist elsewhere**. Uncertain source text remains pending; no
guessed dialogue, player names, statistics or chat was inserted.

## Saved evidence and next work

- `scripts/research_online_4gamer_v190.py`: linked public gallery downloader.
- `scripts/compare_online_4gamer_v190.py`: canonical-source matching matrix.
- `work/research/online_4gamer_sources/research_fetch.json`, `images_fetch.json`.
- Corresponding files in `customization/` for the second collection.
- `matching_report.json`, `matching_review_0.png` through `matching_review_3.png`.
- `archive_index.json`, `archive_fetch.json`, `publisher_archive/fetch.json`.
- `remaining_frame_review.json`: explicit manual review outcomes and manifest hashes.

The broader 2004 publisher archive query timed out without returning an index.
Its shell process returned normally after reporting that timeout; no process is
left running and no result is inferred. The next source search should use narrower
archive URL/date ranges or inspect archived publisher screenshot-page links.
Other safe work remains in embedded art classification and full-resolution review.

Ruff passes for both research scripts. No translated asset, registry, ROM or patch
changed. Four unfinished screenshot resources remain; localization counts, native
display/input/gameplay gates and the full graphics objective are unchanged.
