# V511 normal Tunis voyage and Sick-state plaque audit

Previous goal turn: progress, normal recovered Athens and Tripoli checkpoints.
V508 remains unchanged. This turn advances the normal voyage to Tunis and verifies
an actual disease/recovery context; no state, inventory, unlock or savestate fixture.

## Normal voyage and recovery

A cold boot loads the genuine resupplied Tripoli save. Original city-coordinate
getters and coastline queries are read-only guidance for ordinary steering.
The fleet reaches Tunis, docks, resupplies and saves after a normal 30-day Inn stay.
Observed date advances November10→December10 and fatigue indicator44→0.
These are observed game results, not independent recovery/calendar arithmetic.

The sea warning reports scurvy. Direct Sailor Info inspection establishes the
actual conditions rather than inferring them from that warning:

| Officer | Before the Inn | After the Inn |
| --- | --- | --- |
| Hodram Joakim Bergstrom | Healthy / Relaxed | Healthy / Relaxed |
| Manuel Almeida | Healthy / Upset | Healthy / Relaxed |
| Charles Jean Rochefort | **Sick / Upset** | **Healthy / Relaxed** |

Original Health state5 is疾病, rendered **Sick**. Mood state2 isリラックス,
**Relaxed**; state4 is不機嫌, **Upset**. These existing translations match the
source meaning and are natural concise status labels. The first assumed health
offset was corrected from state1疲労/Tired to the actual state5; no ROM text changed.

## Complete current-ROM display checks

Six actual Sailor Info captures pass:

- All60 plaque regions (ten per screen), including full lettering, bevels, borders
  and backgrounds, match the current source PXL at native color precision.
- All12 health/mood word masks include first, internal and final letters and blank
  cells. Every complete officer name mask passes.
- All60 skill label/number lines match the complete native font masks.
- Tunis Iron, Hemp and Rhino Horn specialty masks pass in three gameplay captures
  and again after cold reload. No newly untranslated or clipped label is found.

The recovered Tunis save is written through normal Save slot6, copied with an
exact hash after clean shutdown, then cold-loaded without a savestate. Its whole
256×192 upper town panel is pixel-identical to the saved-state capture. This proves
the displayed Tunis checkpoint persisted; officer conditions are not separately
re-inspected in that reload.

Checkpoint: `E:\Rota Nova translations\Saves\hodram-tunis-rested-v508.dsv`.
Exact save/ROM/report/PNG hashes are in
`work/analysis/environment_voyage_v511/sick_recovery_proof.json`.

## Scope and remaining work

All18 plaques remain in the continued audit and are not marked fully complete.
Other injury/exhaustion/mood states, other owners/contexts and the original22
graphics requirements remain. The next voyage leg continues west toward Gibraltar,
then Africa/East Asia. Seoul, Osaka/Nagasaki/Naha are not credited by this run.
No new ROM/patch or canonical promotion; experimental V508 remains current:
`c7b86f93ad034bf5c19aa82a51cecb4194ace6dcdce23e481e67c24074bbfbcb`.

Verifier: `scripts/verify_sick_recovery_v511.py` (Ruff passes).
Reports: `work/emulation_v193/environment_voyage_v511/capture_report.json`
(20940 frames), and `environment_voyage_v511_tunis_reload/capture_report.json`
(4200 frames). Full ordinary input schedules are retained. Original donor is exact.
The goal remains active; revisit older record-based checks at actual completion.
