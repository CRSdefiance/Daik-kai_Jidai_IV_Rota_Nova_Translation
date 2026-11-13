# V810-V815: actual ceremony scenes and original outcomes

This checkpoint advances the existing V809 experimental ROM's gameplay evidence.
No ROM, registered dependency, manuscript, palette, graphics layer or patch was
changed. V809 remains SHA-256
`4b85eae04e1f1654022433c2a9a2aafd8b719daf10cc5f2120a32f9781728ae2`,
profile `all-routes-unified-v809`. Its exact clean-input patch and registered
stack remain the integration reference. V803 remains the last *whole batch*
gameplay-verified reference; continuation must retain the complete V809 stack.

## Access and fixture provenance

Original source paths establish the Istanbul gate, site-discovery bit, facility
mask and date selection. The ninth town button's touch rectangle is
`(212,113)-(256,163)`; entering also requires A. Initial Hodram story events
intercept the gate before the recurring ceremony. The normal sequence was played
through the brass-lamp conversation, rockfall, ingredient requests and map check.

Isolated fixtures supply the calendar word, discovered-site bit, facility mask,
existing cargo-product bytes and map 164. Original setters/getters bind each
field. Sulfur, Timber and Saltpeter occupy five existing cargo slots per request;
the actual quest code consumes them and determines when each stage advances.
Observed successful supplies are not a proof of minimum required quantities.
Item 164's clean Japanese is 岩窟集落への地図, currently Cave Village Map.
Original inventory transfer 02049F30 changes only its item record and acquisition
history: three bytes in each paired map preflight. All unrelated RAM is exact.
Fixtures do not replace dialogue, speaker selection, ceremony eligibility,
outcome handlers or time functions. They do not establish earned inventory,
natural campaign availability or elapsed daily-update simulation.

Normal in-game saves create reusable **new** isolated donors. The original V751
donor, SHA-256
`d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132`,
remains unchanged. Saved setup manifests accompany the V811, V813, V814 and V815
DSVs under `E:/Rota Nova translations/Saves/Test fixtures`. No savestates are used.

The initial V815 `ceremony_v809_temple_work` folder has a misleading name:
the already-open menu retained its original Gate button, so this run is the
**site chant**, not a Temple preparation test. Its original return rebuilt the
menu. A normal save and reload then created the correct Temple/Church menu for
subsequent tests. Do not infer the selected consumer from the folder name or a
modified facility mask alone.

## Verified actual display and outcomes

Each revised run has an independently replayed V803 control with the same
initial donor, controller/touch inputs and explicit fixture requests. All runs
are targeted automated emulator tests using the actual ROM, not full route
playthroughs or hardware verification. Every run exited normally.

| Scene family | Complete revised holds | Whole-screen controls | State pairs |
| --- | ---: | ---: | ---: |
| Site prayer, result and off-day refusal | 5 | 35 | 37 |
| Site chant, protagonist reactions and result | 8 | 13 | 18 |
| Temple preparation, result and repeated offer | 7 | 26 | 30 |
| Church prayer, result, off-day response and cancellation | 6 | 9 | 12 |
| Total | 26 | 83 | 97 |

These are 21 distinct revised COMMON IDs, not 26 completed editorial entries.
All 26 holds match the complete native and independently rendered font planes,
stored templates, real-parent formatting and captured wrapped buffers. Full
leading/trailing letters, visible margins, bounds, substituted Cappadocia/Hodram
names and blank paper pass. Pixels outside the dialogue body match the paired
original screens, preserving portraits, speaker labels and UI. All 83 control
frames match both complete screens, including the unchanged original level-up
notices and retained shared refusal 64. No unexpected continuation page appears.

All 97 paired state snapshots match the original actors, towns, items, goods,
ship models, courier/task state, financial state and calendar. The actual site
prayer and chant advance four days / 192 ticks. Temple preparation and Church
prayer advance one day / 48 ticks. Tested Temple and Church cancellations advance
zero ticks. Cash remains unchanged in the measured action intervals, and normal
town returns and next-day refusals are observed. Original crew/level-up outcomes
agree with V803; no synthetic result callback is substituted.

Proofs under `work/analysis/ceremony_access_v810`:

- `prayer_gameplay_verification_v814.json`
- `site_chant_gameplay_verification_v815.json`
- `temple_preparations_gameplay_verification_v815.json`
- `church_prayer_gameplay_verification_v815.json`

Verified full-resolution captures with provenance are copied to the future-guide
folder `E:/Rota Nova translations/Guide screenshots/Editorial V809`.

## Editorial finding and remaining work

`route_editorial_finding_sulfur_v815.json` pins clean/current SC1 file hashes,
record `DK4_MES_B296_R0063`, offsets and complete bytes. The older English
"Bring sulfur; we can make it" drops 大量 (a large quantity/plenty) and the
source's anytime nuance. Actual insufficient-supply refusals make the amount
qualifier relevant. This is a confirmed **open** route finding, not a completed
natural-dialogue-v2 revision. Other compressed story lines seen in the prelude
have not yet received full source/context review.

Still required: the alternate Temple chant, site dance/fast/climb, other
protagonist-specific reactions and remaining declines/normal returns. Original
town getters map Athens to Town 19, site 7, ceremony start day 21. Its date
conditions provide the missing Temple chant and site dance/fast/climb branches;
use normal docking with an isolated location fixture, then source-bound access
inputs as needed. Do not repurpose Istanbul's off-day as an eligible ceremony.

Coverage remains **550 completed COMMON / 605 source-and-prose reviewed / 55
pending**. The whole 52-entry ceremony family gets no completion credit yet.
The whole editorial goal remains active, and the graphics/18-plaque audit remains
separate and unfinished. No canonical promotion or user acceptance is inferred.
