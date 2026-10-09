# Additional exact-source search: November 2004 beta gallery

V244 is source research, not a ROM candidate. V241 remains unchanged. The previous
goal turn made progress on eight actual live captions; this turn inspects an
additional linked screenshot collection for the four unfinished Online bodies.

## Sources actually recovered

The previously saved historical game index links a
[November 2004 beta announcement](https://www.4gamer.net/news/history/2004.11/20041112210231detail.html).
Its actual link leads to the [beta screenshot collection](https://www.4gamer.net/shots/daikoukaionline/index.html).
Four linked gallery indexes supply54 individual image pages. Every page is fetched,
and all54 original screenshots download successfully:47 at1024×768 and7 at800×600.
This collection is distinct from the59 screenshots compared in the earlier source
review. No filename pattern is guessed to generate extra screenshot URLs.

Six images from the linked announcement and16 images from the publisher's
[April 2004 presentation report](https://www.gamecity.ne.jp/dol/report/index.htm)
are also fetched. The latter include presentation photographs, slides and projected
game screens. In total76 image resources download with zero image errors. Their
URLs, resolved URLs, dimensions, file hashes and page-discovery provenance are saved.

The historical index also documents a higher-resolution TGS trailer ZIP hosted at
`download.bbgames.jp`. One bounded availability request fails with host-resolution
error. That request is terminal; it is not a live download or proof that no mirror
exists. The lower-resolution publisher trailer already reviewed in V231 is not
downloaded or reviewed again.

## Review result

All76 images are visually inspected on seven bounded collection sheets, and four
ranked comparison sheets are reviewed against the original clean-ROM Online24,
Online27, Online31 and Online33 pixels. Ranking uses whole-image RGB comparison
as a locator, not as an identity or transcription test. Full original images remain
saved at their downloaded resolution.

The beta set provides readable examples of related character, ship, tavern, skill,
quest and dialogue interfaces. They are different characters/scenes/screenshots
from the four required originals. A profile indoors does not replace Online24's
profile at sea; other portrait pairs do not supply Online31's dialogue. Similarly,
the other quest/tavern scenes do not establish Online33's exact quest or chat.
No source sentence, player name or chat line is inferred from a similar interface.

**Zero new faithful body/chat transcripts are recovered.** The existing reviewed
headers, bubbles and Julien label remain intact. Online24/27/31/33 are still
partially translated and require a clearer exact source. This bounded collection
review does not establish absence elsewhere or transcribe every unrelated image.

## Evidence and next work

- `scripts/research_online_beta_v244.py`: fetches actual linked index/page images,
  preserves downloaded bytes and builds source/ranking sheets; Ruff passes.
- `work/research/online_beta_sources_v244/page_discovery.json` and
  `beta_gallery_discovery.json`: actual initial page and trailer-request outcomes.
- `source_inventory.json`: four indexes,54 image pages,76 downloads and reviews.
- `review_proof.json`: verified file/sheet hashes, source dimensions and explicit
  four-target transcript result.
- `all_source_review_0.png` through`_6.png`; four`Online*_ranked_review.png` sheets.

No translation asset, ROM, patch, release profile or runtime changes. Other native,
embedded/environmental and confirmed-name consistency work remains available, so
the goal remains active rather than blocked. Preserve the full objective, including
the exact remaining screenshot source dependency and final gameplay/integration.
Revisit older record-based checks at eventual completion as requested.
