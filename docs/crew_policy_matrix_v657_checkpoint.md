# V657: all three Assign Sailors policies on an ordinary five-ship fleet

The status turn preceding this continuation polled the existing emulator session
64928 and confirmed it live at frame7500. It was a verified wait, not a reason to
restart the run. This checkpoint continues that same session through frame17500
and stops it normally, producing its terminal capture report.

## Actual gameplay and source wording

The current V653 ROM cold-boots and loads an isolated copy of the ordinary V652
slot6 save. That save contains the normally recruited125 sailors and repaired
five-ship fleet: Vestaros and four Latinas. No savestate, modified ROM, RAM write,
location, inventory, money, health or outcome fixture is used in this run.

Original Town controls enter Crew Setup. Y opens the original allocation menu.
The unchanged menu table02114EF8 orders these existing English labels:

| Japanese source | English | Assigned by ship | Fleet Crew | Unassigned |
| --- | --- | --- | --- | --- |
| 旗艦重視 | Flagship | 89 / 9 / 9 / 9 / 9 | 125 | 0 |
| 平均化 | Even | 49 / 19 / 19 / 19 / 19 | 125 | 0 |
| 必要最小 | Minimum | 39 / 9 / 9 / 9 / 9 | 75 | 50 |

These labels and all three existing notifications faithfully describe the source.
The original minimum requirements are39/9/9/9/9, and maximums124/24/24/24/24.
Even distributes spare sailors after the individual requirements; its label does
not require identical final counts on differently sized ships. Minimum correctly
shows75 assigned in Fleet Crew and50 Unassigned, with46 days Endurance rather
than28. The available sailor pool remains125 in every policy.

The three original notices are “Assigned to flagship first.”, “Sailors assigned
evenly.” and “Minimum sailors assigned.” Their original ARM9 pointers and Japanese
strings are recorded. The confirmation is the original COMMON message11,
これで、よろしいですか？, localized as “Does this work?”. No wording is changed here.

## Original models, actual confirmation and preservation

Captured controller0218A0D8 owns the48-byte allocation model at0218A0E8. Its five
model pointers independently match the original fleet getters. The complete
original allocators020206EC/02020674/0202062C reproduce each observed48-byte result,
including all pointers, counts and total. Only temporary count bytes change in
the replay; full main RAM outside those fields remains exact. Original summation,
minimum and maximum getters agree. All calls preserve their original stack and
saved-register ABI; tested handler/allocation/getter instruction spans match the
clean Japanese ROM.

Preview changes leave the canonical ship models at49/19/19/19/19 until confirmation.
B cancels the Even confirmation and returns to the assignment screen with the
same counts. Because that preview already equaled the persisted counts, this
case does not prove rollback of a different allocation. A separate Flagship X/A
confirmation changes the actual canonical crew to89/9/9/9/9; reopening Crew Setup
shows those counts. A final Even X/A confirmation restores49/19/19/19/19. All
five hull values remain60/25/25/25/25. Eleven captured original-getter states bind
these observations. No ordinary Save command or subsequent saved-game cold reload
is claimed for the new policy changes.

## Complete display checks

- 40 distinct unmodified two-screen captures and37 read-only main-RAM frames.
- Seven whole plaque regions in13 actual contexts:91 regions,95836 native pixel
  comparisons covering lettering, material and borders. All five selected rows
  are exercised; the small/large ship information fields remain readable.
- 273 complete numeric/header field masks plus all three popup labels, including
  first/final letters, spaces and blank font cells. Counts conserve the125 pool.
- Three notices and three confirmation appearances: six complete228x80 display
  ink/shadow/blank-cell comparisons against original rendering. All visible
  characters are in order; first/final glyph erasure controls are rejected.
- Six actual cached228x48 bitmap views independently reproduce10944 declared
  indices each through the complete original native painter with actual captured
  context and source VRAM, guards and ABI checks.

The previous plaque packet still represents the current artwork: both plaque
resources and the1408-byte equipment material tile match V627 exactly. The two
V632 enlarged Japanese/English comparison sheets were inspected; no new coarse
light blocks or vertical streaks were identified in those crops. No redundant
replacement packet is generated, and user visual approval is not inferred.

## Evidence and remaining scope

- Proof: `work/analysis/crew_policy_matrix_v657/proof.json`.
- Verify: `python scripts/verify_crew_policy_matrix_v657.py`; targeted Ruff passes.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V657 Crew policies`.
- Three unmodified policy screenshots are also saved under
  `E:/Rota Nova translations/Screenshots/Guide candidates/V653 Crew policies`,
  with provenance and pending publication/user review explicitly recorded.
- Current ROM remains `out/all_routes_combined_v653_candidate.nds`, SHA256
  `c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade`.

This closes the three-policy display/model comparison for this five-ship setup.
It does not establish every capacity, other fleet arrangement, legacy miniature
control use or device behavior. No ROM, patch, manifest, registry, canonical or
release pointer changes. All18 original plaque/hint entries stay incomplete;
all22 historical scope objects remain exact. Broader equipment, actual small
controls/cards/legacy art, transition, material/user review and acceptance remain
open. The four low-resolution Online exceptions and preserved brown comic marks
remain in force. Older record-based checks are still due at full-goal completion.
