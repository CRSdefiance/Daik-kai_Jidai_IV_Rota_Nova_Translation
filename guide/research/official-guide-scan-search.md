# Official guide scan search

Checked 2026-10-11 for the guide project. Target: **大航海時代IV ROTA NOVA ガイドブック**, KINGS, Koei, March 2006, 207 pages, ISBN **9784775804032 / 4775804030**, covering DS and PSP.

## Result

No accessible full scan of the exact book was verified or downloaded. The strongest lead is an existing forum re-upload announcement; its actual files are hidden behind login/reply requirements. Neither the ISBN nor completeness of the advertised file has been checked.

## Leads and checks

| Resource | Result | Limits |
|---|---|---|
| [Endless Fight re-upload thread](https://endlessfight.org/discuz/forum.php?mod=viewthread&tid=409) | Posted 2021-10-25, edited 2022-11-26; lists a Rota Nova strategy-book upload among six resources. | Login and reply required to view hidden material; no attachment accessed. PSP label alone does not identify the ISBN. |
| [Original Rota Nova thread](https://endlessfight.org/forum/viewthread.php?tid=7024) | Exact original link recovered from the re-upload thread. | Normal retrieval returned HTTP 500; content not inspected. |
| [Re-upload replies, page 2](https://endlessfight.org/discuz/forum.php?mod=viewthread&tid=409&page=2) and [page 3](https://endlessfight.org/discuz/forum.php?mod=viewthread&tid=409&page=3) | Public replies retrieved. | No publicly accessible exact-book file identified in those replies. |
| [Google Books](https://books.google.com/books?id=7CMqNwAACAAJ) | Correct ISBN and 207-page bibliographic entry; retrieved page says “No eBook available.” | No full text or preview located. Books API request returned 429; HTML entry was checked instead. |
| [National Diet Library record](https://ndlsearch.ndl.go.jp/books/R100000002-I000008154358) | Exact book identified through the ISBN OpenSearch API; record lists paper format and call number **Y78-H6393**. | No book-specific online scan link found in the retrieved record. Generic site links about access/copies do not prove this book can be downloaded. |
| Internet Archive text catalog | Query for exact phrase “rota nova” or either ISBN, restricted to texts, returned **0** records. | A catalog query is not proof that no differently titled or unindexed scan exists. |
| Open Library ISBN endpoint | `https://openlibrary.org/isbn/9784775804032.json` returned 404. | Only that ISBN endpoint was established absent; no conclusion about every possible catalog record. |
| Wayback CDX index for the original forum URL | Query `endlessfight.org/forum/viewthread.php?tid=7024*`, successful captures only, returned an empty array. | That URL pattern only; not an exhaustive Wayback search of all aliases. |

## Search scope

Searched English, Japanese, and Chinese title variants using the ISBNs, PDF, scan / スキャン / 扫描, guidebook / ガイドブック / 攻略本, and archive/library terms. Search results were mostly physical-book listings, gameplay guides, unrelated PDFs, or game-file listings. None established an accessible full scan of this exact book.

A broader Internet Archive keyword query produced substantial unrelated material and was inconclusive. It is not counted as a negative scan result.

## Next useful steps

1. Inspect the forum lead through an ordinarily authorized account if available. Do not treat the announcement as evidence that a working file is still present. No account was created and no reply or message was posted during this search.
2. If a file becomes accessible, first inspect the cover, title/copyright page, ISBN, DS/PSP coverage, pagination, and missing/blurred pages. Record file hash and provenance before citing its contents.
3. Investigate the National Diet Library's available access/copy services for this specific paper holding, or obtain a physical copy for reference photography/scanning. Availability and applicable service limits remain unverified.

This search does not change S5's status: **book text not accessed**. Any eventual guidebook findings still require DS/PSP separation and original English explanation.

## Expanded Archive.org follow-up

On 2026-10-11, searched title fields for Rota Nova, Daikoukai/Daikokai, Japanese 大航海時代 / 大航海, and Uncharted Waters, plus both ISBNs and the Strategy Guides collection. Also inspected file inventories for relevant bundled uploads.

- `ps-iv`: earlier Chinese PlayStation IV strategy guide, not the official 2006 Rota Nova book.
- `uncharted-waters-4-manual-chs`: earlier Chinese PC IV manual, not the Rota Nova guidebook.
- `daikoukai-jidai-iv-rota-nova` and `uncharted-waters-ch`: software listings; no guide PDF in inspected file inventories. Game archives were not downloaded or unpacked.
- `oldgamesebooks`: published inventory mentions an IV PK electronic guide; its contents were not downloaded. Does not establish a Rota Nova scan.
- `ddsc-game-manuals`: matching file names concern other sailing titles and Uncharted Waters II; no Rota Nova guide identified.
- `20260115_20260115_1647`, titled Japanese Guides: unrelated police/regulatory documents.

At the user's request, the two IV PDFs were downloaded as [other-version layout references](../references/other-versions/README.md), with verified Archive SHA-1 checksums. Sample pages were rendered and visually inspected. No exact Rota Nova guide scan was verified in this expanded search; unindexed or differently named uploads remain possible.
