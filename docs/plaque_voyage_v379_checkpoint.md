# Actual voyage plaque verification V379

V379 is an evidence checkpoint using the unchanged registered V378 ROM. No new ROM,
patch, artwork or gameplay state was created. The graphics goal remains active.

A fresh 15,600-frame DeSmuME cold boot loads the unchanged genuine cartridge save
from the V328 voyage and uses ordinary controller/stylus inputs. No savestate or
RAM injection is used. Its historical progress is unknown. After the sailing warning,
Info > Sailors > Select reaches four officer screens:

| Officer | Health | Mood |
| --- | --- | --- |
| Hodram Joakim Bergstrom | Healthy | Normal |
| Gerhard Ardelknatts | Healthy | Upset |
| Manuel Almeida | Healthy | Normal |
| Charles Jean Rochefort | Healthy | Normal |

Upset is now proven in an actual Sailor Info display. It preserves the source
不機嫌 meaning of irritability/bad mood. This run does not establish which prior
action caused that state, nor does the scurvy warning establish Sick for an officer.

`scripts/verify_plaque_voyage_v379.py` checks actual ROM and capture hashes, cold-boot
conditions, all four complete name masks, eight complete status masks, 40 complete
source-art plaque regions and 40 complete skill label/number lines. All pass,
including first and final letters and blank cells. Targeted Ruff passes.

Two verifier assumptions failed and were corrected: the name origin was supplied
incorrectly, then Gerhard's name was transcribed without its `l`. The unchanged RAM
export confirms `Gerhard Ardelknatts`, and independent complete font masks verify
its actual placement. Neither failure required a ROM or artwork edit.

Evidence: `work/analysis/plaque_voyage_v379/display_proof.json` and
`work/emulation_v193/plaque_voyage_v379/capture_report.json`.
ROM: `out/all_routes_combined_v378_candidate.nds`, SHA-256
`46a66cfbd079a53dbb155d6a531eae6ac5d956fea93e4f3d9a5a8c679900620f`.
Its profile is `all-routes-unified-v378`; its full handoff is documented in
`docs/unguarded_alignment_v378_checkpoint.md`.

The finalized Gerhard screenshot is archived unchanged as
`guide/screenshots/sailor-info-gerhard-upset-v378.png` and copied with verified hash
to `E:\Rota Nova translations\Screenshots`.

All 18 plaques/hints remain incomplete, per user instruction. Additional health/mood
states, occupied weapons/armor, Assign Sailors nonzero endurance and other fleet/route
contexts remain open. All 22 historical graphics requirements remain in the ledger.
This is a targeted emulator check, not a full route or hardware verification.
