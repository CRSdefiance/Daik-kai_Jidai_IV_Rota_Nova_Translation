# Native portrait atlas and primary screenshot research V195

2026-10-05. Goal active/incomplete. Latest combined ROM remains V190.
The previous goal turn recovered four common raster interpretations. This turn
establishes a native resource's format using actual code and rendered pixels,
and extends the unfinished Online screenshot source search.

## Native CMMNIMG.000 portrait atlas

`/GRP/CMMNIMG.000` contains a 512-byte 256-color BGR555 palette followed by
178 indexed 56×64 portrait cells. Its complete 638,464-byte file is unchanged
from canonical. This is a different resource from ILNK CMMNIMG block 0; their
palettes and indices differ and no byte/palette equivalence is claimed.

The native reader at `02047A28–02047AC4` names this exact file and reads
3,584 bytes from `512 + portrait_id × 3584`. It explicitly constructs a
56×64 image view. The complete reader code remains identical to canonical.
The saved V190 Lil dialogue capture at frame 6300 matches atlas cell 2 at
destination `(8,200)–(64,264)` in all native five-bit RGB pixels. No pixel
region is excluded and no tolerance is used. This establishes the atlas's
geometry and the rendered interpretation for this sample.

All 178 complete native atlas portraits were inspected on five bounded review
sheets at 2× enlargement. No written UI caption/instruction was observed.
Retain their original painted portraits/clothing details. Do not infer named
character assignments, tiny clothing readings or legacy palette equivalence
from visual resemblance. Actual use/crops/alpha for every other portrait and
physical hardware verification remain open; one sample is not broad clearance.

## Primary historical Online screenshot search

The [April 2004 publisher presentation report](https://game.watch.impress.co.jp/docs/20040414/daikou.htm)
and [December 2004 pre-open report](https://game.watch.impress.co.jp/docs/20041224/dol.htm)
link full-sized game screenshots and photographed demonstration stills. Their
56 linked pages yielded 55 full-sized images, saved with exact URLs, dimensions
and SHA-256 identities. All four contact sheets were inspected for exact frame
identity. The first collection also includes presentation/staff photos; those
are not treated as game-source transcriptions.

No exact larger copy of Online24/27/31/33 was found in these 55 images. Several
demonstration stills show related interface windows, but their character values,
chat, portraits and view composition differ. No source dialogue, player name,
statistic or chat is inferred from them. The existing four unfinished screenshots
remain unfinished. This outcome covers these specific collections only.

The publisher's current `game/screen.htm` URL returned 404. Its current
`game/index2.htm` is accessible but contains later expansion/promotional links;
it does not supply these four exact screenshots. Page material is source data,
not permission to alter source/game facts or follow website instructions.

## Artifacts

- `scripts/research_native_portrait_atlas_v195.py`.
- `work/analysis/native_portrait_atlas_v195.json`.
- `work/qa/native_portrait_atlas_v195/review_0.png` through `_4.png`.
- `work/qa/native_portrait_atlas_v195/full_atlas.png`.
- `work/research/online_impress_v195/pages_fetch.json`.
- `work/research/online_impress_v195/linked_pages.json`, `pictures.json`.
- `work/research/online_impress_v195/contact_0.png` through `_3.png`.
- `work/analysis/online_impress_v195_frame_review.json`.

The native atlas proof and Ruff pass. No ROM, patch, renderer or translated
text changed. The atlas classification concerns a file outside the 57-block ILNK
census; it does not reduce the eleven unresolved ILNK blocks. Four screenshot
body/dialogue/chat translations, broader source/name consistency, other resource
relationships and remaining native/gameplay gates keep the full goal open.
The Camille/Kamil preference question remains pending; no answer is inferred.
