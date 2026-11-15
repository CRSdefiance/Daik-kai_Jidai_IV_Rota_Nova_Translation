# Saved-fleet crew plaque checkpoint V380

Evidence checkpoint using unchanged registered V378, not a new ROM release.
A fresh 8,000-frame DeSmuME cold boot loads the unchanged V328 cartridge save
through normal Continue/Load input, then opens Sea View > Crew Setup. No savestate,
RAM injection, fabricated inventory or forced display value is used. Older save
history is unknown. The first attempted sea-menu input occurred at Load confirmation;
ordinary A inputs completed loading before the menu was opened.

The saved Brigantine fleet shows complete `~60 days`, unlike the earlier fresh Lil
fleet's `~0 days`. Normal Lo (L) displays Fleet Crew 0, Unassigned 19 and `~999 days`.
Hi (R) restores Fleet Crew 19, Unassigned 0 and `~60 days`. These values are actual
game output; this audit does not infer a new meaning for the zero-crew value or
claim an independent verification of the Endurance calculation.

`scripts/verify_crew_voyage_v380.py` verifies the ROM/manifest, report and all PNG
hashes, unchanged donor save, three complete Endurance font masks, six complete
crew-count masks, and all 21 plaque composites (seven regions in each state).
All original plaque pixels, borders and lettering match the integrated source art.
First/final glyphs and blank cells are checked. Targeted Ruff passes.

Evidence: `work/analysis/crew_voyage_v380/display_proof.json` and
`work/emulation_v193/crew_voyage_v380/capture_report.json`.
ROM SHA-256: `46a66cfbd079a53dbb155d6a531eae6ac5d956fea93e4f3d9a5a8c679900620f`.
Profile: `all-routes-unified-v378`; complete ROM/patch handoff remains in
`docs/unguarded_alignment_v378_checkpoint.md`. No binary edit was needed.

The normal assigned-crew screen is archived unchanged for the guide in
`guide/screenshots/assign-sailors-brigantine-v378.png` and copied with verified hash
to `E:\Rota Nova translations\Screenshots`.

All 18 plaques/hints remain incomplete by user instruction. This resolves the
specific missing actual nonzero Endurance evidence, while other fleet/route contexts,
alternate health/mood states, occupied weapons/armor and historical graphics gates
remain open. All 22 original requirements remain in the ledger. The graphics goal
is active. This targeted emulator check is not a full playthrough or hardware test.
