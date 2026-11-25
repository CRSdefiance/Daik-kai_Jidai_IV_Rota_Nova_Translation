# V648: original movie-to-scene bitmap phases

Evidence only for the existing V640 combined candidate, SHA256
`93868a0b250a3b52897225dac48ab29e0b14d1f097208ca9a418208dd29d0b9e`.
No ROM, artwork, patch, registry, canonical or release-pointer change.

## Ordinary captures and source identity

Three normal New Game runs capture six adjacent CPU/GPU states around each V647
boundary. Three independent no-export runs and three untouched-Japanese controls
use exactly the same inputs. No save, savestate, cheat, movie substitution or live
RAM write is used. All nine processes terminate normally. All 36 distinct complete
two-screen export/baseline captures match. The three originally reported boundary
screens match the untouched Japanese ROM in every pixel on both screens.

The actual decoded headers, complete 512-byte palettes and all 49,152 indices
identify these byte-identical clean/current sources:

| Route | Original software-overlay image |
|---|---|
| Rafael | `/evstill/evstill001.pxl` |
| Lil | `/towngrp/towngrp03.pxl` |
| Hodram | `/evstill/evstill033.pxl` |

The matching 3D movie backdrops independently reconstruct from ROM textures,
native VRAM bindings and committed geometry at all 18 states. Their complete
49,152 pixels also match the core's serialized 3D framebuffer diagnostically.
The framebuffer is not used as expected source art.

## Original painter and completed video-memory phase

The ordinary lower scene list at023117AC is separate from the actual upper list
at023117C4. The latter includes stack-owned transition nodes. Replaying only the
relevant upper list invokes the original iterator, image getters and painters.
All 98,304 destination bytes are assigned over poison; guards, fragment ABI,
captured ITCM/DTCM, and every executed instruction word match clean-original
ARM9/overlay0. No file-getter, renderer bridge or VRAM write is substituted.
This source proof does not claim lower-scene execution or a whole SDK frame.

Rafael/Lil use the original4x4 ordered-dissolve table at0212792C and original
caller020283F4 / ITCM painter01FF85C8. Sixteen isolated progress-counter controls
per route execute the entire native upper painter and reproduce all source words
for every phase. These are disclosed source-phase controls, not ordinary played
callback arguments. The captured pending counters progress/32 give the current
phase; the preceding completed phase matches the entire actual video-memory
bitmap in all12 states, without selecting a phase from screenshots. Unmodified
native pending paints also predict later completed VRAM states. Four Hodram
transition paints match the entire photo/VRAM directly. At3122 that transition
owner has been removed;at3123 new dialogue nodes are present. These two snapshots
retain the same complete previously native-verified photograph in VRAM. They
are not counted as upper transition callback replays. The initial attempt to
replay all six Hodram states failed:the next scene changes its output,and the
dialogue scene produces writes outside the isolated upper-picture contract.
That diagnostic is retained without a live-game defect
claim or a waiver. In total16 actual transition scene replays and32 controlled
phase replays pass;all18 displayed bitmaps884736 words,including bit15,match
source/native output. Subsequent dialogue composition is outside this proof.

## Display timing and retained limits

The current CPU can be halfway through building the next RAM surface while
video memory contains the preceding completed phase. Intra-frame copying means
an end-of-frame VRAM snapshot does not supply one universal screenshot delay.
V647's fitted-delay alternatives are therefore not promoted to timing proof.

35 of36 whole two-screen clean/current captures match. The later Lil frame2865
differs at63 pixels on row79,x congruent3 modulo4:exactly the original threshold5
cell. Every current pixel is the old original 3D-backdrop color; every Japanese
control pixel is the new original town-photo color at the same position. The
initial assumption about which build updated first was rejected and retained
in diagnostics. No translated letters, palette corruption or invented colors
explain this edge. Exact independent scanline timing is still unproved; this
is not claimed as18 complete same-frame RGB source compositions or as full movie
coverage. The three original unexplained boundary comparisons now have source,
native-phase and actual clean-control evidence, rather than a ROM repair.

## Saved evidence and remaining goal

Proof: `work/analysis/movie_transition_bitmaps_v648/transition_bitmap_proof.json`.
Native exports and nine run reports remain on E under `movie_transition_bitmaps_v648_*`.
Review archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V648 Movie transition bitmaps`.
Transition captures remain test fixtures; no new guide candidates are selected.
All18 plaques remain incomplete,all22 historical requirements remain exact,Online
body exceptions/brown-mark retention remain effective,and full goal remains active.
Legacy consumers,small controls,material review,map contexts,broader timing and
final acceptance remain open. Older record-based checks remain due at completion.
