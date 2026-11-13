# Actual Survey assignment and navigation V327

V326 remains unchanged, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.
No ROM, artwork or patch changes were made.

## Successful ordinary assignment

A current-ROM cold boot loads a byte-exact isolated copy of the older Stockholm
desktop cartridge save described in V326. The original save remains unchanged;
its historical progression is unknown. No savestate, save editing, unlock patch
or live RAM injection is used. The run ends normally at 33,100 frames.

Hodram's first port visit starts a departure tutorial before normal commands.
After the tutorial, Port > Depart > Deck View is available. All officers are
already assigned; selecting the None bucket reports No unassigned crew.

The actual current room coordinates are now established:

- `(150,59)` selects Helm, occupied by Manuel Almeida.
- `(150,114)` selects Captain, occupied by Hodram.
- `(194,114)` selects Mate, occupied by Gerhard.
- `(108,59)` selects Survey, requiring Survey skill 120.

Selecting Gerhard's Mate room and pressing A picks him up for reassignment.
Selecting Survey shows Gerhard 124, Charles 123 and Manuel 120 as eligible.
A places Gerhard; X opens Confirm crew assignment; A commits it and returns
to the departure menu. This is an actual assignment, not a supplied fixture.

The complete Survey heading and Gerhard Ardelknatts name pass native font masks
at `(80,24)` and `(80,40)`. The full confirmation sentence also passes.

## Auto Move's separate route gate

Port > Auto Move opens the actual destination map after assignment. Touching
`(123,106)` selects Hamburg, with the game's displayed coordinates N53 E8.
These are game coordinates; no external geographic correction is inferred.
A opens the complete Auto Move confirmation; confirming reports:

> There is no route to that city.

Both complete lines pass the independent font masks: 164 and 119 ink pixels.
They begin at the same x22 margin, at y296 and y312. This adds actual evidence
that the existing left-alignment repair applies to this modal context too.
No leading or trailing character is missing.

The qualified Survey officer and a usable route connection are separate gates.
This save still lacks the requested route. No automatic sailing or actual
Stop Auto Move display is achieved or credited.

## Manual sailing and retained unsuccessful attempts

The sailing tutorial confirms stylus steering trims sails and tapping the
flagship stops it. The actual voyage displays numeric coordinates because a
Survey officer is aboard. Short steering pulses and stylus touches did not
reliably establish the intended course. Sustained LEFT input produced westward
movement at latitude 55: longitude 18, then 16, then 14 in recorded checkpoints.
Coordinate readings are visually observed, not independently font-masked.

The fleet stalled near an island at 55,14. UP input subsequently reached 56,14;
the following southwest attempt returned near 55,14 without port arrival.
Cold-weather dialogue interrupted inputs twice. Fatigue rose while supplies
remained. The run was stopped before further unverified navigation attempts.

Later Menu button/touch attempts did not open a crew screen. They provide no
alternate health/mood or new in-game save evidence. The cause of those failed
inputs is not established and is not attributed to the translation. The ROM's
existing logic remains unchanged. No Copenhagen/Hamburg port arrival, new route
connection, equipment acquisition or occupied weapon/armor is claimed.

All six complete Rotate/Inspect/Sails caption masks pass in two actual sea frames.
The recorded route request, assignment, controls, weather interruptions and
coordinate checkpoints remain available for choosing the next useful test.

## Goal and evidence

Both graphics audits and progress documents record the results. All 18 plaque/
hint entries and Armor/Weapon variants remain incomplete. Automatic Stop,
occupied equipment, alternate conditions, legacy viewers and final FLS GPU
contexts remain open. Low resolution Online images remain exempt. The full
graphics goal stays active; revisit older record-based checks at actual completion.

These are targeted automated emulator checks, not a complete route or hardware test.

Evidence: `work/analysis/navigation_v327/proof.json` and
`work/emulation_v193/auto_move_v327/capture_report.json`, including all scheduled
inputs, PNG hashes and read-only final RAM/native exports.
Verifier: `scripts/record_navigation_v327.py`; focused Ruff passes.
