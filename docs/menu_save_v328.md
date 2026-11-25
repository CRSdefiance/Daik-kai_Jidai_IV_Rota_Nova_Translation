# Actual Surveyor consumers and persistent sailing save V328

V326 remains unchanged, SHA256
`fc40562bca01ccdcb2678d470c143c8d6baacbb65e23e0bde4d42b5d7a95f5c1`.
No ROM, artwork or patch change was needed.

## Input mapping and usable Menu sequence

The pinned DeSmuME source passes libretro Y and X into the corresponding Y and X
arguments of NDS_setPad. Both source Git blob hashes are verified against the
commit tree; the runner uses the same libretro IDs. No button swap is introduced.
Primary header: [NDSSystem.h at the pinned commit](https://github.com/libretro/desmume/blob/95b4d798731caa809125b6c3c11d17cc332ff6ef/desmume/src/NDSSystem.h#L433).

The original V327 schedule is replayed through the actual Survey assignment to
early sailing. A one-frame X press does not open Menu. Y opens the expected Info
Mode. B returns, A toggles Sails and an eight-frame X press opens the radial Menu.
The A-then-X sequence opens Menu twice in the original run and again after load.

This supplies a usable observed sequence. It does not prove a universal
sails/anchor restriction, establish why a one-frame input was missed, or explain
V327's later weather/fatigue/terrain Menu failures. No production control code
or input mapping is changed based on an unsupported cause.

## Two actual consumers of the shared role correction

Info > Sailors selects Gerhard from the current roster. **Surveyor** is displayed
in both the roster and Sailor Info, with complete names and full font masks.
This follows the committed ordinary reassignment, rather than an injected role.

The V326 shared-table fix now has actual First Mate evidence from V326 and actual
Surveyor evidence here. Other valid roles retain their separate exhaustive native
lookup/raster coverage, without claiming every role was visited in gameplay.

Both Sailor Info captures verify all 20 complete plaque instances and all 20
skill/value lines. The full Equipped Items hint also passes. All 18 ongoing
plaque/hint entries and their Armor/Weapon variants remain incomplete.

## Normal second-slot save and load

Functions > Save creates a new second slot in the runner's isolated cartridge
copy. The first imported Stockholm slot remains available. The original desktop
donor file stays byte-identical; its older gameplay provenance is unknown.

A separate fresh cold boot imports a copy of the new DSV. The initial scheduled
reload selected the old Stockholm slot, so that attempt receives no sailing-save
credit. Ordinary Functions > Load then explicitly selects the second slot, whose
selection and loaded at-sea screen are captured. Gerhard remains Surveyor.

The complete 256x384 Sailor Info screen after loading the second slot matches
the pre-save capture exactly: all 98,304 pixels. The assignment and complete
English role/name/values/plaques persist through native save/load. No savestate,
save editing, unlock patch or live RAM injection is used. Both processes end
normally: 30,000 frames for creation, 6,600 for the reload check.

Reusable save: `work/emulation_v193/early_menu_v328/saves/all_routes_combined_v326_candidate.dsv`.
Its exact SHA256, source hashes, source commit and both report paths are in
`work/analysis/input_mapping_v328/proof.json`.

## Remaining scope and observed wording

The save-selection list shows the compact joined wording **N. SeaAt Sea**. The
abbreviation and missing separator need source/formatter review; this checkpoint
does not correct or certify that caption. The new save provides a repeatable
ordinary route to that view as well as assigned Surveyor and early sailing.

No new port, route connection, automatic Stop display, weapon/armor acquisition
or alternate Health/Mood state is credited. Current observed conditions remain
Healthy/Normal. Legacy viewers, final FLS GPU composition and broader gameplay
gates remain open. Low resolution Online screenshots remain exempt by the user.
The full graphics goal stays active; revisit older record-based checks at actual
completion. These are targeted emulator checks, not a complete playthrough or
physical-device test.

## Evidence

- `scripts/record_menu_save_v328.py`, focused Ruff passing.
- `work/analysis/input_mapping_v328/proof.json`, pinned `NDSSystem.h` and input schedules.
- `work/emulation_v193/early_menu_v328/capture_report.json`.
- `work/emulation_v193/early_menu_v328_reload/capture_report.json`.

Both authoritative graphics audits and the progress documents record the scoped
results, keeping every outstanding completion gate open.
