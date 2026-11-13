# V577: complete small-caption search in existing candidate captures

The previous goal turn made progress: nine actual Grand Race help pages, six
menu labels, measured native geometry and preserved test provenance were added.
This turn searches existing native evidence for the five unresolved miniature
graphics. No artwork, ROM, patch, release profile or canonical baseline changes.
The current experimental candidate remains V573, SHA256
`f987f1c56ba5641544e5c84698c59351e39465b15001601adddf697698d89a77`.

## Corpus and source bindings

There are 134 capture reports naming 22 registered candidates, representing
8,778 saved capture occurrences and 2,417 distinct PNG byte streams. Every
searched image is hash checked against its report. Every source ROM's full hash,
neighboring integrated-release manifest, registered profile and canonical-parent
hash are checked. All seven miniature cells and all 83 palette banks are exact
to V573 in these 22 source ROMs. This includes the two already verified M/D cells
as calibration; it does not imply every other graphic is the same across versions.

The PXL parser's ordinary `palette` property exposes only the first bank. The
search explicitly reads all 83 original banks from the complete palette prefix.
Their index9 foreground entries yield 68 distinct five-bit RGB colors. All are
included, including black. No single bank or assumed white-only text is substituted.

## Exact-mask search and result

The detector uses each current full source cell, including every foreground and
blank pixel, rather than OCR or a matching English word in a different font:

| Caption | Source cell size | Complete ink pixels |
| --- | --- | --- |
| Done | 16x8 | 43 |
| Rank | 23x8 | 49 |
| Cancel | 41x8 | 55 |
| Pick Cargo | 48x8 | 84 |
| Pick Ship | 32x8 | 76 |

All native x/y positions in each stored 256-pixel-wide framebuffer are searched.
Both 256x192 and stacked 256x384 captures are supported. Actual M/D appearances
at the proven V562 town, Port and Sail frames calibrate bit order, native color,
cell margins and exact native positions; all six complete cells are detected.

**None of the five complete miniature masks occurs in the 2,417 searched PNGs.**
This changes the next action: the existing saved menu captures do not provide a
positive consumer lead, so repeatedly inspecting the same screenshots or treating
runtime Done/Cancel text as these bitmap cells is not useful. Trace an original
source-coordinate/bitmap-copy path or reach another relevant parent.

This is a bounded negative, not global non-use or proof that no display is missing.
It excludes neither unsampled frames, unvisited states, scaled/partially clipped
copies, nor arbitrary fade/modulation colors outside the original bank colors.
Some reports use labeled synthetic gameplay or unlock fixtures; these are search
inputs, not newly earned progress or ordinary guide screenshots. Even a positive
pixel match would need original resource/crop/parent provenance before credit.

## Static follow-up

An additional inclusive-rectangle search finds no exact complete four-field
miniature rectangle constants in the mapped main code or declared ARM9 overlays.
Sixteen nearby immediate-coordinate pairs are retained as leads. The apparently
promising208/32 pair at02012F00 and related constructor/reset code stores widget
selection-state fields and participates in sentinel comparisons; its numeric
resemblance alone does not establish a frame-atlas crop. No consumer is credited
from these disassembly candidates. Indirect, computed and embedded-copy paths
remain open.

## Remaining testing, in practical terms

| Area | Current evidence | Still required |
| --- | --- | --- |
| Five miniature captions | Complete stored English and source-copy/palette checks; no matching saved native frames | Identify actual consumers and verify their native crop/composition |
| Separate Confirm graphic | Repaired source material and controlled native crops | Verify its actual parent display; one-player Grand Race waiting did not expose it |
| Plaques and equipment hints | All 18 original entries have paired actual source/current evidence | Continue the requested global texture/style review; keep all 18 incomplete |
| Embedded/environmental/event artwork | Reviewed source retain/localization decisions and many bounded native displays | Remaining legacy archive ownership, clipped source-fragment identity and deeper movie/event composition contexts |

This is mostly remaining display verification; this batch discovers no new
Japanese text to translate. It does not justify a percentage or completion date:
the unresolved consumer paths have not been reduced to a known number of simple
playable scenes. The full goal and all historical requirements retain scope.

## Artifacts

- `scripts/search_miniature_captures_v577.py` (Ruff passes).
- `work/analysis/miniature_consumers_v577/capture_corpus_search_proof.json` contains
  every report/input schedule, ROM/manifest binding, searched PNG hash, template,
  bank color, calibration and result.
- `immediate_pair_leads.json` retains the sixteen disassembly windows.
- Existing screenshots remain on E; the search proof is on E through the existing
  work/analysis junction. No screenshots are reclassified as guide evidence.

All 18 plaque entries remain `fully_completed:false`; all 22 historical objects
are retained exactly. No playable V577 is created. Revisit older record-based
checks at actual full goal completion.
