# V476 supplied Syracuse checkpoint with active Lookout

V474 is unchanged. Normal sailing from the repaired Genoa save reaches Tunis's
discovery event and then Syracuse. Manuel's actual Lookout voice reports Admiral,
city ahead! for both discoveries. Charles's normal docking voice says Dock at
Syracuse? All five complete discovery/docking message masks pass,including their
first/interior/final glyphs and blank cells.

Syracuse resupply completes. Ship Info shows Hull60/60,Water150,Food150 and the
native spaced crew field39/ 39/124. All digits and the deliberate field spacing
pass;an initial unspaced checker expectation was corrected,not the ROM. Hull60/60
is unchanged from the repaired Genoa checkpoint. Thirty-night Inn rest completes
and the town fatigue indicator is0.

Slot6 overwrite finishes after4200 additional frames,then the runner terminates
normally. Two fresh isolated cold loads verify the saved state. The entire Ship
Info screen matches its pre-save view,98304 pixels. The entire selected Lookout
screen matches V475's prepared setup,another98304 pixels. Full role/name/voice
caption masks pass. Cold-loaded Syracuse,(N37 E14),Wheat,Wine,Olive Oil,Sultana and
fatigue0 also pass. The original Genoa donor is unchanged.

Verifier: scripts/verify_syracuse_lookout_v476.py;Ruff passes.
Proof: work/analysis/weapon_voyage_v476/syracuse_proof.json.
Reports: work/emulation_v193/weapon_voyage_v476/capture_report.json,
work/emulation_v193/syracuse_lookout_reload_v476/capture_report.json and
work/emulation_v193/syracuse_ships_reload_v476/capture_report.json.

Normal reusable save on E:
Saves/hodram-syracuse-full-hull-lookout-v474.dsv.
Finalized native discovery screenshot is copied unchanged to E Screenshots.

These are targeted DeSmuME tests,not hardware or full-playthrough proof. This
verifies real Lookout discovery of Tunis/Syracuse;it does not yet establish the
effect on Istanbul. The supplied,undamaged Syracuse fleet is now a closer donor
for that approach and the actual Golden Cutlass purchase. Occupied Weapon and
all broader graphics requirements remain open. All22 historical requirements
and all18 incomplete plaques retained. No canonical promotion. Revisit older
record-based checks at actual full-goal completion.
