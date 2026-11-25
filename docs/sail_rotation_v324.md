# Source-faithful Rotate caption V324

## Meaning and clarity

Original **帆回転** means sail rotation. The source caption and sailing tutorial
identify L/R as the sail-angle control, while A opens/closes sails. The accepted
canonical baseline already uses the complete action verb **Rotate**.

V267 changed this to the object label Sails, with a padded sixth cell. That
decision made both distinct controls read Sails. V324 restores Rotate, which
states the rotation action and distinguishes it from the retained A-button
Sails caption. The tutorial's L/R meaning remains authoritative; no new
camera-control interpretation is introduced.

## Exact change and preservation

Only the original eight-byte ARM9 span at `0x147928` changes from
`Sails \0\0` to `Rotate\0\0`. Its sole original owner at `0x119138` is unchanged.
The clean Japanese span, canonical English and current inherited bytes are
source-locked. All other code, pointers, fonts, helpers, arenas, labels,
route/COMMON/HELP data, artwork, ARM7, overlays and banner stay exact V322.

The old padded object label and new verb both occupy six stored cells. Original
footer positions and widths remain exact. The inherited complete-ASCII footer
measurement fix and Inspect caption remain present. Historical profiles and
their source-locked batches are retained unchanged.

## Verification

Four native cases pass: normal/automatic footers in both 4-bit and 16-bit formats.
The normal footer's complete Rotate, Sails, Inspect and Menu rasters pass; all
placements match the parent. The automatic footer remains entirely unchanged.
Actual automatic Stop gameplay remains a separate open check.

A fresh 31,200-frame DeSmuME cold boot traverses title/New Game, captain selection,
Rafael's opening, Lisbon and sailing. No savestate, progress edits or live RAM
injection is used. At frames 30,400 and 30,800 all six complete Rotate/Sails/Inspect
font masks pass, including every ink and blank cell. The retained Info Mode
heading and both instruction lines also pass after the normal Inspect command.

The title at frame 1,200, character confirmation at 2,000, opening dialogue at
10,800 and recruitment confirmation at 14,400 match the V322 captures byte for
byte. Changed sailing screens were visually reviewed. Independent animated
sea/map frames are not claimed identical. Control behavior is preserved by
the exact data-only delta; this run does not prove port arrival or equipment
acquisition.

The complete V322 stack reproduces byte for byte through the updated builder.
V324 retains all 470 inherited batches, all required layers and inherited
changed records. Its clean-input patch reconstructs the ROM exactly. Source-lock,
native raster/layout, manifest/inheritance, patch, actual font/frame checks
and focused Ruff pass.

## Registered experimental candidate

| Item | Identity |
|---|---|
| Candidate | `out/all_routes_combined_v324_candidate.nds` |
| ROM SHA256 | `14a285ca3605c243593f64d3de43dd6c4e2caf0a44acb0a6be085f6cd69968b9` |
| Patch | `out/all_routes_combined_v324_candidate.xdelta` |
| Patch SHA256 | `a7e513b59877ff23240ffd236d2659259ef213b77e4fcd5539829c270b4eedb0` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Profile | `all-routes-unified-v324` |
| New stage | `translations/sail_rotation_caption_release_v1.json` |
| New changed component versus V322 | `/__arm9__.bin`, original eight-byte caption only |
| Complete manifest | `out/all_routes_combined_v324_candidate.manifest.json` |

The manifest enumerates all 41 inherited changed paths against the canonical
base; this candidate adds no changed path. The canonical baseline is unchanged.
Experimental; user cold-boot acceptance is pending. On the user's emulator check
title/New Game or Continue, established opening/town, complete sailing captions
and the retained Inspect action. Rotate should identify the L/R angle control,
while Sails identifies A open/close.

## Audit and evidence

Both graphics audits and progress documents record V324. All 18 plaque/hint
entries and Armor/Weapon variants remain incomplete. Final FLS GPU rendering,
legacy viewers, occupied weapon/armor, alternate conditions and wider gameplay
contexts remain open. Low resolution Online images remain excluded by the user.
The graphics goal stays active; revisit older record-based checks at actual
completion. These are targeted automated emulator checks, not a full playthrough
or physical-device verification.

Evidence: `work/analysis/sail_rotation_v324/native_proof.json`, `release_proof.json`,
full V322 reproduction, exact patch reconstruction, and
`work/emulation_v193/sail_rotation_v324/capture_report.json`.
Scripts: `prepare_sail_rotation_v324.py` and `verify_sail_rotation_v324.py --live`
under `scripts/`.
