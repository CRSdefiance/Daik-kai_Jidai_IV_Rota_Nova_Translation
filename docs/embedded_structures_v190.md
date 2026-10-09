# Embedded portrait and section research V190

## V192 correction to the record origin

The native selector proves that stored table offsets are relative to each entry's
own address. The earlier section-relative payload boundaries below are superseded
by the corrected parser and all 406 native selections. Word 8 is a table offset,
not a type tag. The original report is preserved as
`work/analysis/embedded_structures_v190_before_self_relative_fix.json`.
See [V192 native classification](native_character_containers_v192.md).

2026-10-05. Goal active/incomplete; latest combined ROM remains V189.
The previous goal turn made progress by saving the original screenshot source
search. This turn adds source-locked embedded storage evidence. No ROM, translation
batch or release profile changed. V190 names research, not a new candidate.

## Four raw portrait interpretations

SLACKIMG blocks 14–17 each contain exactly 14,144 bytes. Displaying one byte per
pixel as grayscale at 104×136 produces four coherent head-and-shoulders portraits.
All four complete source images were reviewed on the enlarged review sheet;
no Japanese caption or instruction was observed. The four original blocks are
unchanged in V189. Source bytes, saved PNG bytes and complete decode/encode
roundtrips are pinned in `work/analysis/embedded_structures_v190.json`.

This is a grayscale **display interpretation**. It does not establish native
grayscale encoding, palette ownership, actual geometry, color-key/alpha or usage.
The alternate 136×104 interpretation produces broken horizontal strips. Native
loose portrait files do use 104×136 dimensions, but their index payloads do not
match these raw blocks. No exact character/resource association is inferred.
The visual outcome is “no caption observed in the reviewed interpretation”, not
archive-wide or runtime clearance. Historical unclassified counts are unchanged.

## Eight paired section structures

CHARA blocks 6–13 share an initial word 8, an extent word, and two bounded relative
offset tables. The second table begins at `4 + extent`. The first table begins at
byte 8. The first relative offset in each table equals four times its derived entry
count; both tables have the same count. Their offsets are strictly increasing and
each payload fits its section.

| Block | Paired records |
| --- | ---: |
| 6 | 8 |
| 7 | 7 |
| 8 | 8 |
| 9 | 12 |
| 10 | 7 |
| 11 | 8 |
| 12 | 7 |
| 13 | 7 |
| Total | 64 |

Every table and all 128 bounded payloads reconstruct the complete original blocks
byte for byte. All eight blocks are unchanged in V189. This establishes the observed
storage partition; it does **not** establish animation, sprite, mask, geometry,
palette or command semantics. Naive zero-run decoding and interpreting the first
two payload bytes as width/height did not produce a consistent image extent and
are not adopted. Native consumers and payload encoding remain to map.

## Exact loose-image search

`scripts/research_raw_embedded_matches_v190.py` searches all 27 historically unresolved
blocks against 701 complete loose PXL payloads, including packed bytes, expanded
4-bit indices and direct-color source bytes. The minimum is 1,024 bytes and four
distinct values, excluding short/constant background coincidences. No exact
contiguous match was found. The 660 loose PXL resources comprise 66 four-bit,
552 eight-bit and 42 sixteen-bit files.

This search checks a gap in the earlier raw BGR555/loose matching method. It does
not clear resampled, remapped, tiled or compressed copies. Later external-palette
pair classifications are preserved; searching the historical 27 is not a reversal
of those classifications. No missing translated copy was proved by this search.

## Source search availability

A narrower publisher HTML archive-index query timed out and returned no index.
The lighter archive availability API returned HTTP 429 for three exact-page
lookups. These are unavailable source evidence, not negative screenshot results.
All processes are terminal; no job is left running. Avoid repeating the broad
archive search while it is rate limited. Embedded decoding and native resource
mapping remain useful work independent of that service.

## Artifacts and remaining work

- `scripts/research_embedded_structures_v190.py`
- `scripts/research_raw_embedded_matches_v190.py`
- `work/analysis/embedded_structures_v190.json`
- `work/analysis/raw_embedded_matches_v190.json`
- `work/qa/embedded_masks_v190/portrait_review.png`
- `work/research/online_4gamer_sources/publisher_game_pages_fetch.json`
- `work/research/online_4gamer_sources/publisher_page_availability.json`

Both scripts pass Ruff. Complete saved grayscale roundtrips, all section boundaries
and all eight reconstruction checks pass. Native encoding/use, other unclassified
raw content, four Online screenshot transcripts, source fidelity and all live
graphics/input/gameplay gates remain open. No full-goal completion is claimed.
