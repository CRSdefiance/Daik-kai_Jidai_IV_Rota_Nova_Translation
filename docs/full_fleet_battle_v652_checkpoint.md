# V652: staffed five-ship encounter, loss/recovery and queued portrait findings

The preceding goal turn made progress through V651's integrated captain-modal
formatter repair, complete actual screen checks and exact patch reconstruction.
This continuation tests another real fleet context. The full graphics goal stays
active. V652 is an evidence checkpoint; the experimental ROM remains V651.

## Ordinary preparation and reusable save

A fresh V651 cold boot loads an isolated exact copy of V650's five-ship Copenhagen
save. Original Tavern recruitment and Auto > Even assignment are used. Original
model getters independently distinguish the preview from the committed result:
the models still contain19/0/0/0/0 crew at10200/11200; the normal confirmation at
14000 commits49/19/19/19/19, a total125. No recruitment result, money, crew,
condition, ability, inventory or ship model is injected.

Normal Yard repair then changes Vestaros hull48 to60. Its crew49 remains exact;
the four Latina hull25/crew19 models remain intact. Normal Functions > Save writes
only slot6 in the isolated battery. This19600-frame run terminates normally. Its
staffed/repaired five-ship save is preserved separately from all later outcomes.
Source donor, ROM, patch and release registry hashes stay unchanged.

## Visibility lead and coordinate-only fixture

A second6000-frame cold boot departs normally. The older test fixture is evaluated
offline and rejects the state because Speyer's mobile ship is not instantiated.
Nothing from that rejected attempt is applied to the running emulator. Original
fleet/name/position/model getters establish a moving offscreen Speyer fleet with
an intact Hanse Cog named model, hull30/crew13. The player is in a different part
of the map. Ordinary sailing and this initial diagnostic run are preserved.

After that run terminates, a new adapter is prepared and frozen before the next
emulator starts. It retains the original source-code, identity, ship and terrain
checks. An offscreen target permits only `approach`, requires that observed30/13
Hanse Cog, and changes only the player's lead-ship coordinate field. Original
terrain code must identify water near the target's actual recorded position.
Five invalid-code/size/action/offscreen-recovery controls are rejected offline.

The final encounter run applies two `approach` fixtures, at4800 and5200. Each owns
one8-byte coordinate field; four bytes actually differ each time. Complete4MiB
before/after replay matches the recorded fixture hashes. Ship model, hull, crew,
other player ships, enemy data, war flags, result flags, rewards and inventory are
unchanged by both fixtures. No recovery fixture is used.

The original visibility update constructs Speyer's real mobile ship after the
first approach. Its live values are initialized by original game code; the saved
model's13 crew is not asserted to equal the subsequently initialized mobile crew.
The second approach uses the now-live enemy position and original terrain checks.
Both are disclosed location fixtures, not proof of an earned voyage.

## Actual duel, loss and recovery

Original encounter dialogue, combat and the boarding duel run. At13200 original
getters identify all five live player ships: Vestaros60/43 plus four Latina25/19.
They also identify three live enemy ships. At14400 the player lead ship is60/0;
the four support ships still have19 crew each. The game announces the loss,
switches to a surviving Latina and returns the fleet to Oslo. Four intact Latina
models remain at16000 and23600. No victory or full-fleet reward screen is reached.
The reason for the loss is not inferred to be a script, a particular duel input
or a general game defect from these observations alone.

The23600-frame run terminates normally after an ordinary isolated slot6 Save.
A separate3200-frame cold boot reloads that post-loss battery and original getters
confirm all four surviving Latina models. Both the pre-battle five-ship save and
the post-loss four-ship Oslo save are retained, with distinct hashes/provenance.
No complete route, hardware-device or battle-victory clearance is claimed.

## Graphics result and newly visible formatting debt

All143 unmodified capture records across the four terminal runs are hash-bound
and searched for the five complete miniature atlas masks using the original83
palette banks. No complete match is found in these sampled states. This is not
global non-use, a Confirm parent, or victory-reward coverage. All six small-control
parent requirements remain open.

Three actual word splits need repair:

| Context | Source identity | Actual example |
|---|---|---|
| Recruitment cost | Native890; original voice table02118380 | `c` / `oins` at5200 in the staffing run |
| Unassigned crew | Native71; original voice table02117460 | `th` / `at` at12800 in the staffing run |
| Retreat | Native2684; original voice table02117080 | `Retrea` / `t` at15200 in the encounter run |

The related complete families are890..896,71..75 and2683..2689:19 voice entries.
Current English/source Japanese for those families is retained in analysis.
Two retreat entries share identical English. A preliminary supplied-role probe
therefore did not uniquely establish the actual call. The later connected replay
executes original020351C4..020351E8, including the real ship-name virtual getter,
role1 and original table argument, through the original role/voice selector.
It selects2684. The original nonquestion role caller returns02053DB8; the cost
and unassigned confirmations use original question-role return02053D24.

These are the same two typed queued portrait paths already handled selectively
by the existing shared wrapper. Their factory/geometry and complete source-entry
contracts should guide the next shared formatter repair. V651's distinct
captain-modal parent020546E8 fix remains preserved and is not a repair for these
newly observed portrait paths. No new English, manual line break or production
formatter change is applied in V652. Full foreground/blank-cell repair clearance
is still pending for these findings.

The crew-capacity lead at original020AB18C returns124 for Vestaros and24 for a
Latina, matching observed Max values. This remains a source-consumer lead until
bound to the actual Max-column producer; it is not used as a new cheat limit.

## Evidence, integration and retained goal scope

- Proof: `work/analysis/full_fleet_battle_v652/battle_proof.json`.
- Preparation proof: `work/analysis/full_fleet_battle_v652/staffing_proof.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V652 Full fleet encounter`.
- RAM/native exports remain at the original E paths, with report hashes.
- Current ROM remains `all_routes_combined_v651_candidate.nds`, SHA256
  `a11e57dfb6e021244122e002cd4804051db2298ae387b753eb16dc22ef6a573f`.
- Its profile, patch, manifest, all470 batches/114 accepted layers, graphics,
  canonical baseline and release pointers remain unchanged.

All18 original plaque/hint entries remain incomplete; all22 historical requirement
objects retain their exact scope. No new final-guide screenshots, canonical
promotion or Git commit/push is claimed. The shared portrait wrapping repair,
full-fleet victory/reward controls and all wider graphics gates remain open.
