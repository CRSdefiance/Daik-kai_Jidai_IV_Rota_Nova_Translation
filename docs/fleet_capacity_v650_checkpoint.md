# V650: ordinary five-ship fleet, dock transfers and captain prompt findings

The preceding user status turn polled live session73873, a verified wait. This
continuation resumes that same process and reaches a normal terminal56600-frame
report. It does not restart a live emulator. The full graphics goal stays active.

## Actual ordinary controls

Current V640 cold boots from an exact isolated copy of the Copenhagen donor.
154 ordinary input events produce156 unmodified two-screen captures. No gameplay
fixture, savestate, location, inventory, money, recovery or outcome write is used.
The fixture adapter is available but never invoked. Source donor bytes remain exact.

Normal Tavern recruitment offers1180 coins and announces29 recruits. The player
then accepts the warning about54 unassigned sailors; this does not retain those
unassigned sailors. Four normal Latina purchases use the default ship name.
The Yard subsequently displays its original five-ship limit notice. The ordinary
Swap Ships interface displays five fleet entries, stored ships and empty slots
during transfer previews. Captain selection reaches the ship and crew selectors.
The Port correctly refuses departure with unstaffed support ships.

Original native model queries independently establish one Vestaros initially and
five actual models in seven later states, including the final Save/Functions
state: Vestaros hull48/crew19 plus four Latina hull25/crew0. Original loop
0205A9E8 uses five8-byte descriptors; original02036C94 resolves their CShip models.
Temporary dock previews are not counted as persisted changes to those models.
Some exploratory button sequences returned to a previous selector instead of the
intended menu. Their actual captures and complete schedule remain preserved;
intent is not credited as execution of an unobserved Arrange/Cargo/battle screen.

Normal Functions > Save overwrites only slot6 in the isolated copied cartridge
battery. The resulting five-ship save is hash-bound for subsequent testing.
Its cold reload is not yet verified, and four support ships need crew before a
new battle attempt. No new combat, victory, loot or earned voyage is claimed.

## Graphics/control result and real defect

All156 captured frames were searched for the five complete miniature atlas masks
using the original palette-bank ink colors. None matches. This is a bounded
sampled-screen result, not global non-use, a Confirm parent, or a drawing trace.
The miniature/Confirm gameplay-parent investigation therefore remains open.

Two actually displayed system instructions expose missing word wrapping:

- COMMON269 at32600: `Choose the ship whose captain you wa` / `nt to change.`
- COMMON272 at35800: `Changing your flagship may cancel th` /
  `e crew's room assignments.`

Both source Japanese entries and complete unchanged English paragraphs are bound
to their native message IDs. Independent font masks verify both complete lines,
including all initial/final letters. The defects split words; they do not drop
characters. Repair is required before these instructions receive display clearance.
Follow-up V651 tests routing the full captain-instruction family269..272 through
the existing guarded modal word wrapper while preserving all English prose.

## Evidence and retained scope

Proof: `work/analysis/fleet_capacity_v650/fleet_capacity_proof.json`.
Run/report/RAM/native exports remain on E at the proof paths.
Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V650 Five ship capacity`.
These exploratory screenshots are test evidence, not final guide screenshots.
V650 does not change a ROM, patch, registry, canonical baseline or release pointer.
All18 original plaques remain incomplete and all22 historical scope objects retain
their full requirements. Online-body exceptions and brown-mark retention stand.
