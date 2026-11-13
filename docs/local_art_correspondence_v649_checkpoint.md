# V649: local transformed-art correspondence investigation

Evidence only on the unchanged V640 combined candidate, SHA256
`93868a0b250a3b52897225dac48ab29e0b14d1f097208ca9a418208dd29d0b9e`.
No ROM, artwork, dialogue, patch, registry, canonical or release-pointer changes.

## New search boundary

V506 ranked whole padded-storage images by32x24 average RGB. That method can
miss a cropped, resized or palette-converted picture inside a larger texture.
V649 instead decodes every clean-ROM660 PXL and261 FLS texture. FLS images use
their record-declared source extents rather than power-of-two padding. All921
source-file hashes and declared dimensions are verified independently of the
search. All21 legacy SLACKIMG block19 planes are decoded from exact source words.

Six informative48x48 source patches per plane give126 queries. Target proxies
preserve aspect ratio up to128x128. Local windows range8..64 pixels at4-pixel
grid steps,with nearby positions/sizes refined.904 original views have eligible
windows;17 thin/flat views are explicitly listed without eligible windows.
Full grayscale patch correlation supplements perceptual hashes,followed by
local RGB/shape refinement. Candidate scores are not proof of picture identity.

## Controls and failure retained

Six clearly marked,isolated search controls use original frames4,7,8,16,20 with
known half/eighty-percent/full scales,13/11-pixel placement and selected16-level
color quantization. They are generated search inputs,not game-ROM replacements.
The initial hash-only method missed control4;its exact source,log and partial
results are retained. Full patch correlation was added;the originalNCC>0.90 gate
was retained. An independent verifier requires at least two distinct source boxes
per control at their actual known transformed positions,within3 proxy pixels.
All six pass. A uniform negative image contributes zero eligible windows.

## Reviewed result and limits

All21 strongest actual-art leads were inspected on three explicitly labeled
sheets. They mostly match simple boundaries,garment highlights,sky gradients
or unrelated picture details. No complete picture or Japanese-caption copy is
established by these reviewed leads. No actual candidate meets the declared
two-distinct-patch geometric model atNCC>=0.93/RGB error<=24. Shared cast imagery
alone,including the Deck Master poster versus the GUI atlas,is not treated as
evidence of a whole poster/caption copy or a legacy viewer.

This is a bounded lead search. Unselected source patches,thin images,other scales,
rotations,flips,alpha composition,differently encoded assets and other embedded
formats remain outside its coverage. It is not global duplicate exclusion or
proof that legacy assets are unused. No native loading,crop/composition,ordinary
scene,emulator screenshot or guide/playthrough credit is added. The unresolved
legacy-reader investigation should follow a different source-consumer lead.

The numerical stage uses bundled Python3.12.14,numpy2.3.5 and Pillow12.3.0.
The generated337MB feature cache and all original decoded views remain on E in
the analysis directory;the cache is hash-bound without duplicating it into the
review archive. Runtime/source metadata and all search scripts are retained.

## Audit and review

Proof: `work/analysis/local_art_correspondence_v649/correspondence_proof.json`.
Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V649 Local artwork correspondence`.
Analysis/source previews: `work/analysis/local_art_correspondence_v649`,physically
on E through the existing analysis junction. These previews are source decodes
and analysis sheets,not screenshots of gameplay.

The current repaired V632 plaque comparison packet was presented for user
material review. No response or approval is inferred. All18 plaque/hint objects
remain incomplete;all22 historical requirement objects retain their exact scope.
Online screenshot-body exceptions and brown-mark retention remain effective.
The full graphics goal,legacy/native/material/map/acceptance gates and final
older-record follow-up remain open.
