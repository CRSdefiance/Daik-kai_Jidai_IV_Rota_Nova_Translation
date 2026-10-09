# Combined V163: eight village caption images

V163 is the latest **experimental** combined candidate. It translates eight
handwritten Japanese captions in the original white village/development images.
All earlier translations and repairs remain exact. The full goal is incomplete;
canonical promotion and final commit/push remain pending.

## Source and natural English

| Image | Japanese source | English |
| --- | --- | --- |
| evstill168 | アラブの村 1 | Arab Village 1 |
| evstill169 | 新大陸の村 | New World Village |
| evstill170 | 中国 村 | Chinese Village |
| evstill171 | 北海の村 | North Sea Village |
| evstill206 | 村 アラブ 発展後 | Arab Village (Developed) |
| evstill207 | 新大陸 発展後 | New World Village (Developed) |
| evstill208 | 中国の島 発展後 | Chinese Island (Developed) |
| evstill209 | 北海の村 発展後 | North Sea Village (Developed) |

The captions preserve the number in image 168 and the completed development
state in images 206–209. Image208 explicitly says **island**; that meaning is
retained. Image207's village context is inferred from its paired New World
village image 169, and this inference is recorded in the localization note.
Spaces in the transcription represent the source's handwritten arrangement.
Each English caption is one complete heading without manually broken words.

Image 207 also has an isolated stroke clipped by the top edge. It cannot be
confidently transcribed as a complete character. Its English heading uses the
readable Japanese lines and the paired village context; the clipped mark remains
a source interpretation question to revisit when its actual scene use is mapped.

Every resource matches the original clean Japanese ROM, immutable canonical
base and V162. The entire image is a white caption canvas, including the old
handwritten ink/antialias pixels. Replacing that caption canvas uses original
white palette index 255 and the source palette's closest dark blue to the original
ink. No new village illustration is invented. The eight captions use the game's
complete six-pixel-advance English font, with all eleven rows in each glyph cell
and no visible row trimming. All words fit inside the original 256×192 canvas.
Headers, complete palettes, dimensions and pixel extents remain exact. The
handwritten caption's pixels are replaced; no original handwriting style match
is claimed.

All eight full original and English panels were visually reviewed side by side.
Preview: `work/qa/village_graphics_v163/review.png`.
Source/localization/artwork: `work/analysis/village_graphics_v163_artwork.json`.
The placeholder appearance does not prove these images are unused; no exclusion
or live event reachability is asserted.

## Verification and limits

**50 focused graphics tests pass**: nineteen new village tests and all 31 earlier
button/name/treasure/fleet tests. They verify eight complete native font rasters,
negative missing-first-character cases in native output and packed eight-bit
images, complete visible bounds, eight native full-image size/adoption cases,
source-lock rejection, exact source headers/palettes/extents, complete caption
canvases and profile/stage inheritance. New script and test files pass Ruff.

The original native font lookup/paletted primitive executes complete glyph cells
with saved-register/stack checks and image canaries. Shape proofs use a four-bit
scratch image at index 15; each actual eight-bit target independently verifies
every caption glyph pixel at its original blue palette index. This does not
claim that the four-bit primitive draws eight-bit textures directly.

Native full-image sizing/view adoption verifies256×192 for each target with the
existing PXL getter. The loaded resource/header and selector table binding are
**controlled inputs**. This is format/geometry evidence, not actual event loading
or live crop proof. Complete widget/GPU palette/alpha presentation, hardware
input, all display contexts, event reachability and physical gameplay remain
pending. Native evidence: `work/analysis/village_graphics_v163_native.json`.

Saved-ROM checks prove every other V162 resource/component, inherited terminal
stage, relocation and changed record exact. ARM9, shared text, HELP, all four
routes and all previous translated graphics remain byte-identical to V162.
Canonical menu/graphics invariants and exact clean-ROM xdelta reconstruction
pass. Saved proof: `work/analysis/village_v163_saved_proof.json`.

## Candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V162 comparison | `0ece3348fd68b3c3ef9fb8e4104360806bd4cc007aef21d3780e28f9352b1f9c` |
| V163: `out/all_routes_combined_v163_candidate.nds` | `e37d81b0ba5f12c21d5a586966944f087b9ec348ce85e5fdc03c8d02d4721cd9` |
| ARM9, exact V162 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V163 build | `f2b5713d670d992590d899387931bddef830869fa07a4b31c0e8387205acdf6d` |
| V163 patch: `out/all_routes_combined_v163_candidate.xdelta`, 768393 bytes | `3a3f21b43a25f300fad60ff7c34a8f3043bb5502ec3b8de603fa811b6e819565` |

Profile: `all-routes-unified-v163`, experimental. The registered builder starts
from the canonical base and reproduces every one of the 441 V162 batches and
terminal stages. Eight additional source-locked experimental batches bring
the total to **449**: `translations/village_caption_evstill168_graphics_v1.json`
through the corresponding 169, 170, 171, 206, 207, 208 and 209 files.
All accepted layers are baked into the canonical baseline; zero additional
accepted batches are required. The adjacent `.manifest.json` contains the full
batch list, paths/records, inherited stages and build checks.

Compared with V162, only these eight internal files differ:
`/evstill/evstill168.pxl`, `/evstill/evstill169.pxl`,
`/evstill/evstill170.pxl`, `/evstill/evstill171.pxl`,
`/evstill/evstill206.pxl`, `/evstill/evstill207.pxl`,
`/evstill/evstill208.pxl` and `/evstill/evstill209.pxl`.

Compared with the canonical baseline, 22 internal paths differ: those eight plus
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/SLACKIMG.DK4`,
`/Iseki/dock.pxl`, `/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`,
`/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`, `/data/SC0.DK4`,
`/data/SC1.DK4`, `/data/SC2.DK4` and `/data/SC3.DK4`.

Before acceptance, cold-boot without a savestate and test the title, New Game
captain selection/name entry, an established story, town UI and inherited
changed item/Advice/Gallery/treasure/fleet/button screens. Find the actual
village and developed-village image contexts and check all eight complete
captions, visible bounds, blue/white palette, alpha and input behavior.
Explicit user acceptance is required before canonical promotion.

## Full goal remaining

245 COMMON selections / 133 physical owners still need actual consumer/layout
integration. Other ARM9/UI, names/source fidelity, Reports/Sailing Help
persistence, BGM physical audio/input, downloaded items and full gameplay
checks remain. The historical graphics inventory now has **14** other confirmed
Japanese loose/FLS resources, one matching embedded title copy, the separate
CMMNIMG atlas and unclassified artwork. The count describes inventory after
these caption edits; it does not clear every in-game screen. Final packaging,
progress and GitHub commit/push remain campaign tasks. On full goal completion,
retain the requested note to revisit older record-based checks.
