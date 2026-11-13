# Contextual sailing footer correction V321/V322

## Source meaning and actual action

The verified V320 cartridge save was loaded into an isolated V318 cold boot.
Ordinary inputs entered Rafael's first sailing tutorial and then Sea View.
The footer caption Sea Map opened **Info Mode**, which instructs the player:
“View information about the cities and ships on screen. Select a target.”
This is target inspection, rather than opening a map.

The clean Japanese caption is **洋上**, meaning “at sea,” in the original
eight-byte ARM9 allocation at `0x11B514`. Both original footer owners,
`0x119140` and `0x119158`, still point to that allocation in the clean,
canonical and current ROMs. **Inspect** is a complete natural English
functional localization of this observed at-sea action. It is not an
abbreviation or a literal claim that 洋上 itself means inspection.

V322 replaces `Sea Map\0` with `Inspect\0` in the original eight bytes.
Every other ARM9 byte, instruction, pointer, font, helper, arena and label is
exact V318. All artwork and other ROM components remain exact V318.

## Native and actual verification

Both normal and automatic-sailing footer descriptors pass complete original
native raster/layout checks in both 4-bit and 16-bit modes: four cases.
Every letter, blank cell and placement fits without overlapping neighboring
captions. Automatic Stop's actual gameplay context remains unverified.

A fresh 31,200-frame V322 cold boot traverses the title menu, New Game captain
selection, Rafael's opening, Lisbon and sailing. No savestate, edited progress
flag or live memory injection is used. Captured title, character confirmation,
opening dialogue, recruitment and changed sailing screens were visually reviewed.

At frames 30,400 and 30,800 the full Inspect caption and both Sails captions
pass exact font masks: six complete labels. At frame 31,200 the ordinary command
opens Info Mode, and its heading and both instruction lines pass complete masks.
The whole upper Info Mode screen also matches the pre-change V318 action exactly.
Animated sea/map frames are not claimed identical between independent runs.

The earlier V321 voyage test ended normally at 16,800 frames after reporting
exhausted food. No port arrival, weapon/armor purchase or Auto Move unlock is
credited. It is retained as unsuccessful ordinary navigation with useful source
and action evidence. The original V320 docked save remains unmodified.

## Registered experimental candidate

| Item | Identity |
|---|---|
| ROM | `out/all_routes_combined_v322_candidate.nds` |
| ROM SHA256 | `9486a749d9ed15af618adee4f0818ce1e99a7bccd93a7daa4d639cf066db7e03` |
| Patch | `out/all_routes_combined_v322_candidate.xdelta` |
| Patch SHA256 | `1344e52193b560b6278e1562f6f4b0f8acc12dd09a58f06dffea14a1b3be5e59` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Profile | `all-routes-unified-v322` |
| Inheritance | All 470 V318 batches, accepted requirements and inherited native stages |
| New stage | `translations/sea_inspect_caption_release_v1.json` |
| New changed internal file versus V318 | `/__arm9__.bin`, original eight-byte caption only |
| Full manifest | `out/all_routes_combined_v322_candidate.manifest.json` |

The complete V318 profile reproduces its prior ROM byte for byte with the new
optional builder stage present. The clean-input patch reconstructs V322 exactly.
Manifest/registry hashes, all required batches, inherited changed records and
all 41 inherited changed paths are checked. The exact paths against the canonical
base are listed in the manifest; the new candidate adds no further changed path.
ARM7, overlays, banner, all route/COMMON/HELP data and artwork stay exact V318.

Source-lock, four native footer cases, full release/patch/inheritance checks,
the actual cold-boot masks/action and Ruff pass. The canonical base is unchanged;
user cold-boot acceptance is pending. On the user's emulator, check the title,
New Game or Continue, established opening/town and the sailing Inspect command.
It should display every letter and open target information.

## Evidence and remaining goal scope

Scripts: `prepare_sea_inspect_v322.py`, `verify_sea_inspect_v322.py` and
`record_sea_inspect_live_v322.py` under `scripts/`.

Proofs: `work/analysis/sea_inspect_v322/native_proof.json`, `release_proof.json`,
`cold_boot_inputs.json`, full V318 reproduction and exact patch reconstruction.
Actual capture: `work/emulation_v193/sea_inspect_v322/capture_report.json`.
Unsuccessful navigation: `work/emulation_v193/ordinary_voyage_v321/capture_report.json`.

Both graphics audits record the new evidence. All 18 plaque/hint entries and
Armor/Weapon variants remain incomplete. Occupied weapon/armor, alternate
conditions, other route/fleet contexts, legacy viewers and final FLS rendering
remain open. Low resolution Online screenshots remain exempt by user instruction.
The graphics goal stays active; revisit older record-based checks at its actual
completion. These are targeted automated emulator checks, not a complete
playthrough or physical-device verification.
