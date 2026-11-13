# V654: five-ship victory, rewards and complete Spoils contexts

The previous completed goal turn made progress through V653's shared queued
portrait repair, integrated candidate, complete native/emulator comparisons and
updated audits. This checkpoint advances actual five-ship battle/reward coverage.
It does not change the ROM or complete the full graphics goal.

## Same encounter, original automatic control

Current V653 cold-boots from the same isolated, normally staffed/repaired
Copenhagen donor used by V652/V653. Original ship models are Vestaros60/49 and
four Latina25/19. The original sailing simulation reduces the live flagship's
crew to43; the four supports remain19 each. All five ships survive this run.

Exactly the existing two coordinate-only approach fixtures are applied at4800
and5200. Each owns8 coordinate bytes; four bytes actually change. Original
identity/model and water-terrain checks remain required. Entire4MiB replay
reproduces every write. No recovery, character health, crew, enemy, inventory,
outcome or reward injection is applied. The source battery is unchanged.

All41 paired pre-Y whole screens match V653's previous loss path. At13200,
the original Y automatic duel input replaces that path's A input. Original
simulation produces the enemy-ship capture, crew-defeat notice and victory.
This establishes a successful tested control sequence, not a guarantee of
victory in every duel or a general diagnosis of every earlier loss.

## Interrupted exploratory run and completed replay

The first interactive process captured through28400 but ended without a final
capture report. Its handle returned Unknown process id, a fresh process inventory
found no matching Python process, and no terminal report existed. The input
journal alone is not treated as a completion receipt. All original PNGs/RAM/native
exports remain as interrupted evidence.

Only after those absence checks, a fresh isolated cold boot replays the complete
recorded commands and appends a normal stop at28400. The process exits0 and its
terminal report records28400 frames, no savestate and no callback errors. All84
unmodified capture records/82 distinct sampled frames are hash-bound. Repeated
same-name screenshots match the interrupted run exactly. No observation timeout
is used as a reason to restart a live emulator.

## Original rewards and surviving fleet

Original per-ship model/live getters verify all five ship identities and hull/crew
in nine actual states through28400. Live values remain Vestaros60/43 and four
Latina25/19. Original nation/funds getters independently establish:

- 25,975 before the reward notices close.
- 30,175 after the 4,200-coin capture reward.
- 30,250 after the 75-coin national reward, retained through frame 28,400.

The Power+28 notice is also displayed normally. No normal post-victory Save action
is performed; a new reusable saved-game checkpoint is not claimed. This test ends
in the original post-victory story sequence, not a whole route or hardware test.

## Complete text and actual five-ship cargo views

Nine captured reward/warning fields pass complete228x80 native foreground,
CP932 shadow, exact palette-color and blank-cell comparisons. Original native
raster execution consumes the actual same-frame prepared strings, including
full-width reward digits. All visible glyphs match in order; first/final glyph
erasure controls fail. These include ship capture, victory, supplies, coin rewards,
the Power notice and both Finish-warning states.

Normal R cycles through all five original ship positions and wraps to Vestaros.
Twenty-one whole title masks pass, including Vestaros/Latina Cargo Setup. Source
parent mode3 and its actual cached view bind owner02313A4C to the complete resident
`_pxl/senrihin.pxl`; original view getters return the whole current file exactly.

Twelve complete4096-pixel Spoils banners match every current source pixel,
including letters, wood, borders and palette:49152 pixels total. One initially
included frame23200 has a hover tooltip over369 banner pixels within source
x16..55,y5..15. That full-banner expectation is rejected and retained as a
diagnostic. The frame receives no complete-banner credit. Simple tooltip font
models also did not establish its complete native geometry/palette; no new
tooltip clearance or artwork defect is inferred from those model failures.

Original A selection previews, R navigation, Finish/X, cancel/B and final accept/A
reach the normal post-victory story. This is not comprehensive permanent cargo
acquisition clearance. Early analysis of parent+18 treated it as a possible loot
list; it is retained only as an unproven lead, not proof of which items were
committed. All five source model records before/after remain available for later
typed cargo-consumer work. An exploratory34FC0 result220 is not asserted to be
current crew; the independently observed current live total is119.

The five complete miniature masks are searched only in these82 sampled states
using the original83 source palette banks. This bounded search does not establish
global non-use. The six small-control parent requirements remain open. Faithful
material reconstruction/user review is also not closed by current-art matches.

## Evidence and unchanged integration

- ROM remains `out/all_routes_combined_v653_candidate.nds`, SHA256
  `c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade`.
- Proof: `work/analysis/full_fleet_victory_v654/proof.json`.
- Completed replay:
  `E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_victory_v654_replay`.
- Interrupted evidence remains in the separate `full_fleet_victory_v654_actual`
  directory; it is not counted as a terminal run.
- Archive:
  `E:/Rota Nova translations/Screenshots/Test fixtures/V654 Five ship victory`.
- Reproduce with `python scripts/run_full_fleet_victory_v654.py --replay` in a
  fresh output folder using the pinned preflight/command files, then run
  `python scripts/verify_full_fleet_victory_v654.py` against that declared folder.

The existing V653 ROM, patch, manifest, registry and canonical baseline remain
hash-exact. No V654 ROM, canonical promotion, commit or push is created. All18
original plaque/hint entries stay incomplete, and all22 historical requirement
objects remain exact. Wider control/card/legacy/art/material/transition and final
acceptance gates remain open. Low-resolution Online screenshot exclusions and
preserved brown comic marks remain in force. Older record-based checks remain
due at actual full-goal completion. The full graphics goal stays active.
