# V510 normal recovery and Tripoli voyage

Previous goal turn: progress on complete registered PXL cache loading. Current
V508 ROM remains unchanged; this turn advances normal gameplay toward the East
Asian environment checks. No savestate, inventory fixture, teleport or unlock
injection is used.

## Recovered Athens checkpoint

The genuine Athens cartridge checkpoint cold-loads in V508. Ordinary Inn input
selects Stay More → 30 Days and confirms the stay. The displayed date advances
from August23 to September22 and the observed fatigue indicator falls55→0.
These are observed UI results, not an independent implementation of recovery or
calendar arithmetic. Normal Save slot6 completes, followed by clean shutdown.

The Brigantine needs39 sailors and already has39; Max124. No crew reduction is
performed. The complete `~38 days`, Fleet Crew39, Unassigned0 and39/39/124 masks
pass. All seven current Assign Sailors plaque regions match their source assets
pixel-for-pixel, including lettering, borders and backgrounds.

The recovered save is copied byte-exactly to:
`E:\Rota Nova translations\Saves\hodram-athens-rested-v508.dsv`.
Its SHA-256 is
`83fe3317eee3bca21b70be69bf34febd12d3aea09a83e75003b1f848d5fea937`.
The initial hash attempt encountered the emulator's open file handle; verification
was completed after normal shutdown. The original donor remains unchanged.

## Normal Tripoli arrival and persistence

A fresh cold boot loads the recovered save. Read-only original city-coordinate
getters and coastline queries inform ordinary D-pad steering. The fleet crosses
the Mediterranean, discovers Tripoli, confirms docking and completes resupply.
The original port event also plays through normal input. No movement or flags
are inserted into the game state.

The actual Tripoli town panel shows Port/Normal, coordinatesN32 E13, Hayreddin
Clan and Cotton/Hemp/Gold. Every specialty letter and blank cell matches the
current compact font mask on arrival and after cold reload.

Original town getter26/facility0 selects harbor painting44. A wholly visible
160×16 source patch matches2,560 native-color pixels in each capture. The earlier
larger region overlapped the date HUD; the final cold-reload frame was also
occluded by the Port menu. Neither is an artwork defect. The verifier uses the
existing unobscured reload frame3400 and bounds above the date panel. It does not
claim the occluded pixels, full-image alpha or every scene composition.

Ordinary Save slot6, shutdown and another cold boot confirm the Tripoli checkpoint
persists. Its verified E-drive copy is:
`E:\Rota Nova translations\Saves\hodram-tripoli-resupplied-v508.dsv`.
The exact hash is in `work/analysis/environment_voyage_v510/voyage_proof.json`.

## Evidence and remaining work

- `scripts/verify_environment_voyage_v510.py` verifies ROM/report/PNG/donor hashes,
  all seven plaque composites, full crew/Endurance masks, specialty masks,
  unobscured background pixels, copied save bytes and cold-reload provenance.
- Reports: `environment_voyage_v510` (11700 frames),
  `environment_voyage_v510_leg` (10770),
  `environment_voyage_v510_tripoli_reload` (4200), under`work/emulation_v193`.
- Original read-only water-route evidence:
  `work/analysis/environment_voyage_v510/athens_tripoli_route/water_route_proof.json`.

This is a normal additional port/recovery/fleet context and persistent voyage
progress. Seoul, Osaka/Nagasaki/Naha and other East Asian visits are still pending.
All22 historical requirements and all18 incomplete plaques remain in the audit.
No new ROM or patch is necessary; experimental V508 remains current, SHA-256
`c7b86f93ad034bf5c19aa82a51cecb4194ace6dcdce23e481e67c24074bbfbcb`.
The graphics goal remains active. Revisit older record-based checks at actual
full-goal completion.
