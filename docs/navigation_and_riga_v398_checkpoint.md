# Calibrated ordinary controls and Riga arrival V395–V398

The registered experimental candidate remains unchanged V388, SHA-256
`1629f2823aa953507c0ec3029556701509fd28d364824aefb6ce2aa61109abcc`.
No ROM or artwork was modified. The graphics goal is active and incomplete.

## Original steering and actual matched controls

Original input selection at `02076A4C..02076B28` reads the held-direction word
from sailing controller+50B4. Eight original selector-fragment executions produce
angles0,32,64,96,128,160,192,224. The fragment is entered after its upstream
eligibility checks; supplied owner/input bits are explicit native test contracts.
The subsequent original rudder routine `0207AF64` turns toward the selected angle,
with a rate derived from ship/crew data. A long button press is not a free rotation.

Four normal cold boots load the same unchanged genuine V328 save and differ only
in a128-frame direction input after frame6000. All18 earlier whole screenshots
match. Read-only final ship getters give Up0, Right64, Down128, Left192. Right
changes native x positively and Down increases y. Up/Left have no displacement
in this coastal starting context; open-water movement is not inferred from them.
Coast collision and later sailing can change heading after an input ends.

`scripts/verify_navigation_controls_v395.py` verifies reports, ROM, input schedules,
all screenshot/snapshot hashes, original selector bytes and final ship fields.
Proof: `work/analysis/navigation_controls_v395/proof.json`. Targeted Ruff passes.

## Normal voyage, landing and resupply

V396 normally loads the genuine saved voyage, holds Right for2000 frames, then
Down+Right for250 and Down for90. The game displays Dock at Riga? atframe8340;
ordinary A confirms docking. Frame8800 is the actual Riga town, Type Port,
coordinatesN57 E23, with Bergstrom Fleet20% and Wheat/Furs/Wax specialties.
The Port interaction offers resupply for a visually observed148 coins; A accepts
and opens Depart/Dock/Cargo Setup. Observed funds change44700 to44552.

Native complete masks pass for Dock at Riga?, Resupply?, coins. punctuation,
Depart, Riga, (N57 E23), Bergstrom Fleet and all three specialty names. First/final
letters and blank cells are included. Price digits do not match the ordinary
word-font mask and are not credited as numerically verified glyphs; source numeric
format/rendering and independent economy arithmetic remain unproven. The values
above are observed screen values, not an independent calculation of the transaction.

## Persisted progress through the game

The normal Save menu creates slot3 in the isolated copied battery. V397's first
reload test mistakenly moved away from the remembered slot and loaded the old
sea save; that failed selection is retained and receives no Riga reload credit.
V398 uses the remembered third slot through normal Continue/Load confirmation.
Its cold boot reloads Riga Docked with the resupplied checkpoint, and the town,
coordinates, fleet and specialty masks pass again. The original V328 battery
still has its exact original hash; only the isolated test battery was saved.

Verifier: `scripts/verify_riga_arrival_v398.py`.
Proof: `work/analysis/port_navigation_v396/arrival_reload_proof.json`.
New save: `work/emulation_v193/port_navigation_v396/saves/all_routes_combined_v388_candidate.dsv`.
SHA-verified convenience copy: `E:\Rota Nova translations\Saves\hodram-riga-v388.dsv`.
Copy receipt: `work/analysis/port_navigation_v396/save_external_copy_receipt.json`.
Finalized screenshot: `E:\Rota Nova translations\Screenshots\riga-town-resupplied-v388.png`.

## Remaining work

This is a genuine additional port/fleet context and persistent navigation progress.
It is not a weapon/armor acquisition, unlocked Gallery/ending or full playthrough.
Next, inspect ordinary Auto Move eligibility between the visited owned ports and
continue supplied travel toward source-backed equipment acquisition. Original
requirements for a captain, surveyor, connected route and shares still apply.

All18 plaque/hint entries remain fully_completed:false and all22 historical
requirements remain in the ledger. Original raw-comic/other consumers, deep
contexts and other health/mood/equipment variants remain open. Online low-resolution
translation remains user-exempt. Revisit older record-based checks at full completion.
