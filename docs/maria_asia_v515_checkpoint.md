# Maria Asia testing V515

The user suggested using the previously discovered Action Replay code to begin
Maria's route near the Asian artwork. The isolated research ROM is an exact V508
copy except for ARM9 byte 0x9F068: instruction 03A00003 becomes 03A00004 at
0209F068. This keeps Maria available on Choose Captain. It does not write any
completion flag. The production ROM remains unchanged. This is an authorized
selection bypass, not evidence that Maria's unlock was earned through a completed
route. The code and its original disassembly are in `maria_unlock_action_replay.md`.

## Verified current Hangzhou screen

`work/analysis/maria_asia_v515/hangzhou_proof.json` verifies the single-byte
fixture, actual cold boot, normal opening/facility inputs and every captured PNG
hash. Current China, Silk Cloth and Jade labels match complete native font masks,
including all blank cells and their first/final letters. A 170×96 visible portion
of retained town background33 matches exactly at native color precision. Source
columns84–85 at rows80–95 are covered by the Inn nameplate/frame and excluded.
The backgrounds are also unchanged in the newly registered V514 candidate.

These captures belong in the explicitly labeled test-fixture archive, with their
manifest and proof. They do not establish a normal unlock or a complete route.

## Voyage status

The first normal manual voyage departed Hangzhou and drifted east toward Nagasaki.
It encountered a Kurushima warning at frame24560 with low supplies. Neither Seoul
nor Nagasaki was docked in that run. Its capture report is retained; no teleport,
inventory, supply, character-condition or completion flag was injected.

The next test uses the game's Auto Move from Hangzhou. An invalid touchscreen
input used stacked-image y259 instead of lower-screen-local y67; input validation
terminated that emulator process. This was a harness input error, not a ROM crash.
The replacement cold run has the corrected coordinate and its own output folder.
Only terminal reports count as complete runs; a paused process is not completion.

Seoul background35, Osaka background37 and the alternate Tavern/Inn icon-caption
composition in Nagasaki, Osaka and Naha remain to verify through actual visits.
All 22 original graphics requirements and all 18 incomplete plaques remain open
where their remaining gates are unproven. The graphics goal stays active.

## Terminal Auto Move evidence

The corrected cold run ended normally at frame27800. Seoul and Nagasaki both
return the complete two-row message "There is no route to that city." All eight
actual specialty labels in their map previews match complete font masks. The map
uses six-pixel glyphs at x136, y84+20n; this differs from town stock rows.
Neither preview is a town visit or a display of backgrounds35/37. The read-only
original terrain route reaches Seoul through a western channel, turning east
after travelling north; it has not yet established boat passage or docking.
Proof: `work/analysis/maria_asia_v515/map_and_route_proof.json`.
