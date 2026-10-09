# Additional publisher source search V231

V231 is research, not a new ROM. The previous turn completed29 source-resolution
art decisions. This turn checks previously unexamined publisher URLs and a linked
trailer for the four unresolved Online screenshot transcripts. V218 is unchanged;
the full graphics goal remains active and incomplete.

## Images and actual page links

The recovered2003–2005 archive index contains72 image URLs. Earlier work checked
eight selected sources. All **64 remaining URLs** now resolve to current images
on the original publisher host and have been downloaded, hashed and visually
reviewed, including the small navigation/border/button images. The one animated
GIF has two frames, and both are inspected. No candidate is excluded merely by
file size. Every indexed URL is accounted for by the original eight or this64.

The current files' SHA-1/base32 digests match **35** historical index digests.
The other current bytes are not asserted to be historical captures. Archive
timestamps identify discovery provenance; current URLs/SHA-256 identify actual
downloaded evidence.

The publisher's [introduction page](https://www.gamecity.ne.jp/dol/game/index.htm)
is accessible. Its actual links add **eight329x269 PNGs**. These show ships, naval
combat, ruins, NPCs and a bazaar. The bazaar picture reproduces the already
source-backed composition/bubbles, but crops the required chat area. The NPC
picture shows the same pair in another scene/sentence; it is not Online31's
dialogue source. No new transcript is derived from those similarities.

The previously investigated`screen.htm`/`screenshot.htm` URLs return404 today.
One bounded12-second lookup for the early archived index timed out. This is
unavailable archive evidence, not a negative source result; the process is terminal.

## Linked trailer

The introduction page links the still-accessible
[TGS2004 trailer](https://download1.gamecity.ne.jp/movie/tgs2004-dol.mpg).
Its25,462,788 bytes are pinned by SHA-256
`9087252e3a85a9273d25f7641c31bbc4ea894c49fdf060d437acbf945d512346`.
PyAV19.0.1 was installed only in the ignored local`.deps/media` directory for
reference decoding; no system installation or ROM dependency was added.

All **3,422** decoded MPEG-1 frames (320x240,30fps, about114 seconds) were compared
with the four immutable native screenshot originals. Two-second timeline samples
on five sheets and four ranked comparison sheets were visually reviewed. The
trailer shows battles, towns, player conversations and introductory scenes, but
the reviewed output supplies no exact profile/quest/two-portrait/dialogue/chat
counterpart for the missing text.

Global RGB ranking often favored unrelated backgrounds. It is a candidate locator,
not an absence proof across every possible crop, overlay transformation or transient
frame. Not every video frame was manually transcribed. No similar character, ruin,
town or chat conversation is substituted for the original screenshot's text.

## Outcome and limits

No faithful new body/chat transcript was recovered for Online24/27/31/33.
All four remain partially translated, and a clearer exact source is still needed.
The inspected collections do not establish that larger originals are absent
elsewhere. Their existing source-backed headers/bubbles/Julien label remain intact.

No translation, graphics batch, release registry, ROM or patch changed. Other
implementation/native/display work remains available, so this is not a blocked-
goal declaration. Preserve the full objective and the after-completion follow-up
on older record-based checks.

## Evidence

- `scripts/research_publisher_archive_images_v231.py` and
  `scripts/inspect_publisher_trailer_v231.py` (Ruff passes).
- `work/research/publisher_archive_images_v231/source_inventory.json`:
  64 actual fetches, GIF frames and nine reviewed sheets.
- `current_page_links.json`, `current_index_image_sources.json` and its reviewed sheet.
- `tgs2004_movie_source.json`, `trailer_review_inventory.json`, timeline/candidate PNGs.
- `review_proof.json`: complete72-URL coverage and35 historical-digest comparisons.
- `early_index_lookup.json`: bounded unavailable archive request.

All source file/sheet hashes are checked before review approval. Separate archive
and current-index sheet filenames prevent one collection overwriting another.
