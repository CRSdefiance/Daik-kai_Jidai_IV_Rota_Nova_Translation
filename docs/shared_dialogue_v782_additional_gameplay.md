# V782: required-crew and warning scenes verified

Two more actual families now pass: required-crew shortfall **1035** and the
low-success warning **1022**. Together with capacity prompt 1042, there are six
complete holds across three original consumer families. The same registered V782
ROM and exact clean-input patch are unchanged. V782 remains experimental; V780
remains the last candidate whose entire editorial batch has finished its checks.

The batch still needs actual missing-information1020, village coordinates1028/1029,
anchorage/destination fleet rumors1030–1034, and private barmaid topics1049–1069.
No new entries receive completion credit yet. Totals remain 367 complete
(259 revised/108 retained), 420 source/prose reviewed, and 53 drafts. The whole
editorial goal, all route work, other prose, and the separate graphics audit
remain unfinished.

## Required crew: five short

Paired V780/V782 cold boots use copies of the protected Istanbul donor. The
authorized fixture invokes the original ship crew setter181B4 and copies only
Vestaros's crew halfword back to the emulator. One byte actually changes, 39 to 0.
Required crew 39, capacity 124, cash, health, cargo, location and other RAM are
unchanged at insertion. The normal game recruits 34 and computes a shortage of 5.
This is an isolated test state, not an earned crew loss or a normal journey.

The source-faithful prompt reads: "You're still 5 short of the crew you need.
Shall I recruit more?" The original full-width digit and every English letter are
verified in both complete holds6800/7200. Sixteen strict screen controls and16
state/model/object/task pairs match. Cancellation goes through Assign Sailors and
the unassigned-sailors confirmation, then returns normally to town at8800.

One cyan row blink differs at8000. A separate original-build cold boot reproduces
the identical fixture and input schedule and captures7900–8000. The entire V782
screen matches complete original frames; no rectangle is excluded to hide the
highlight. Its full-frame matches and provenance are recorded in the verifier.

## Low-success warning: original Bribe flow

The final V3 fixture changes three room/assignment bytes, Gerhard's XP word, and
one calendar word(+768 native ticks,16 source calendar days). Original Speech209
beats the original Tavern threshold15. Opponents, cash, menu flags, code and
source saves are unchanged. At9400, while target selection is being reached,
one Gerhard condition byte changes from0 to3. Original Speech becomes104; Pasha's
unchanged leader Speech is152. The original success calculation gives28, below
the Bribe warning threshold50. This is a disclosed prerequisite test, not earned
qualification, elapsed story time, illness, or a successful scheme.

The player normally opens Schemes, chooses Bribe, chooses Pasha, and chooses a
town's broker. The original routine selects voice-table warning1022:
"The chances of success seem very low... Do you want to proceed?"
Two complete holds 12200/12600 pass exact native glyphs, leading/trailing letters,
line breaks, margins, blank paper and outside-dialogue pixels. Thirty-four strict
whole-screen controls and33 state/model/object/task pairs match the baseline.
No additional animation exception is needed. Selecting No returns through the
normal Tavern menu to town at 13400. Cash stays 8371; no 1000-coin scheme charge is
committed and the complete original job records remain unchanged.

Both final fixture receipts reproduce byte for byte from the read-only RAM
snapshots saved before each fixture. The original harness and each active adapter
remain unchanged throughout their captures. All captures are targeted automated
emulator tests, without savestates, physical hardware or full-route claims.

## Earlier probes and the next lead

Earlier warning probes kept Schemes hidden; they receive no warning credit. The
original date-dependent availability threshold was380 against Speech209. A native
trace shows the16-day state yields threshold15. An initial visual reading of8371
as837 was wrong; the original8371 already satisfies the1000-coin requirement.
A funds-only test is preserved as an unused probe. The final V3 fixture leaves
cash unchanged. An earlier opponent-XP attempt failed its native assertion and
was never applied to an emulator. Its rejected source is preserved.

The next missing-information investigation executes the original57068 helper
against all five selectable local factions. Each currently has2–4 eligible known
towns, so ordinary selection will not reach1020 in this save. The helper's second
argument is an output array, not a region number. Its exact returned town lists
are recorded in missing_information_native_lead.json. A further bounded source
state will be needed; no actual1020 activation is claimed.

## Preservation and archive

Across all three actual families there are61 strict whole-screen controls, two
complete original blink-phase controls and60 state/model/object/task pairs. The
earlier seven ordinary startup/New Game comparisons remain valid. The frozen
production manuscript/configuration dependencies, combined ROM, patch, canonical
base, clean ROM and original donor saves retain their exact hashes. The user's
COMMON676/677 formatting repair remains covered by the existing V782 proof.

Verified screenshots are saved under E:/Rota Nova translations/Screenshots/Test
fixtures/V782 Shared dialogue. Supplemental evidence is archived beside the V782
integration archive. Test states are not promoted to finished guide screenshots.
The18 plaques, excluded Online bodies, preserved brown marks and older-record
follow-up remain open and unchanged. No new ROM, commit or GitHub push is made.
