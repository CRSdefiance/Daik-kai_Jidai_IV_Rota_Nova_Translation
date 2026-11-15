# V512 normal Ceuta voyage and recovered checkpoint

Previous goal turn: progress on the genuine Sick-state/recovery audit in Tunis.
V508 remains unchanged. This turn advances the normal voyage to Gibraltar/Ceuta
for the subsequent Atlantic/Africa/East Asia legs.

## Normal gameplay progress

A cold boot loads the genuine recovered Tunis save. Ordinary controller input
selects Sail, navigates west, discovers Ceuta and confirms docking. Original
terrain and ship-position queries are read-only guidance. Fog, scurvy messages,
wind/turning effects and coastal collisions interrupt the approach; the actual
inputs and captures remain in the report. No movement, condition, inventory or
unlock is injected, and no savestate is used.

Ceuta resupply completes normally. A 30-night Inn stay visibly advances the date
January19→February18 and the observed fatigue indicator62→0. Save slot6 completes;
after clean shutdown the cartridge is copied byte-exactly to:
`E:\Rota Nova translations\Saves\hodram-ceuta-rested-v508.dsv`.
A fresh cold boot confirms the displayed recovered Ceuta state persists. These
are observed game results, not independent calendar/recovery arithmetic.

## Display and source checks

- Complete native font masks for **P. Oil, Ambergris and Leather** match on
  arrival, after recovery and after cold reload, including first/final letters
  and blank cells.
- Original town getter12/facility0 selects harbor painting42. A wholly visible
  160×16 patch above the date HUD matches2,560 native-color source pixels in each
  of the three captures. Occluded areas/full-image alpha are not credited.
- The whole256×192 upper town panel after cold reload is pixel-identical to the
  normally saved capture. All ROM/report/PNG/donor/save-copy hashes pass.

The small oil label was initially misread from the screenshot. The current native
commodity getter confirms index15 is **P. Oil**; the clean source is **ヤシ油**.
V343 had already retained this legacy abbreviation with its older fidelity review
open. That follow-up is reaffirmed here; no full-word replacement is authored or
claimed reviewed. Revisit it alongside the older record-based checks at actual
goal completion.

The earlier unreadable Rafael company-share announcement did **not** occur in
this Hodram visit. This run supplies no new display clearance for that announcement.

## Evidence and remaining work

- `scripts/verify_ceuta_checkpoint_v512.py`.
- `work/analysis/environment_voyage_v512/ceuta_proof.json`.
- `work/emulation_v193/environment_voyage_v512/capture_report.json` (16950 frames).
- `work/emulation_v193/environment_voyage_v512_ceuta_reload/capture_report.json`
  (4200 frames).
- Original read-only terrain route:
  `work/analysis/environment_voyage_v512/tunis_ceuta_route/water_route_proof.json`.

The next voyage continues into the Atlantic, then toward the remaining East Asian
artwork checks. Seoul/Osaka/Nagasaki/Naha and other original gates remain pending.
All22 historical requirements and all18 incomplete plaques remain in the audit.
No new ROM/patch or canonical promotion; experimental V508 stays current:
`c7b86f93ad034bf5c19aa82a51cecb4194ace6dcdce23e481e67c24074bbfbcb`.
The full graphics goal remains active.
