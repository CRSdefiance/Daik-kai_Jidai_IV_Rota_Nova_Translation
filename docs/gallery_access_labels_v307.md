# Ordinary Gallery access and missing labels V306/V307

V306 establishes Gallery access through a legitimate ordinary in-game save and
finds three untranslated submenu labels. V307 corrects those labels in their
existing string allocations, preserving every native unlock condition.

## Actual ordinary save and menu access

A fresh production V305 cold boot reaches Rafael in Lisbon. Ordinary controls
open Functions/Save, show six unused slots, choose the first empty slot and confirm
new save creation. The game returns to its Functions menu. Ordinary Quit Game
confirmation returns to title. Continue, Grand Race and Gallery are now enabled.
No source-ROM changes, progress-flag patches, loaded states or live RAM injection.

The original native predicate at020ED708 checks six slot tags against `DK4R` and
reads their headers. Its result supplies all three title enable fields. After the
actual save, all three runtime fields equal1. This is not evidence that route
completion is required merely to open the Gallery menu.

The Gallery submenu shows Items and `史跡`. Both open normally and report no items
acquired/no ruins discovered in this fresh game. That is empty-collection evidence,
not item/artwork display verification. Extras is a separate About Extras/Online
Version menu. The successful run stops at31200 frames, exports read-only state and
exits. Every screenshot/report hash and empty callback-error check passes.

## Three missing source labels and fixed translations

The original four-entry Gallery table at02115708 contains Items plus three labels
still Japanese in V305. They are distinct from previously translated headings.

| Source | English | Slot offset/capacity | Sole pointer owner |
|---|---|---|---|
| 史跡 | Ruins |13894C /8 bytes|115718|
| 登場人物 | Characters |1389EC /12 bytes|115728|
| イベントシーン | Event Scenes |138EFC /16 bytes|115738|

Ruins follows established game terminology and the actual no-ruins message for
historic sites. Characters includes game people beyond crew members. Event Scenes
matches the existing heading/descriptions. Clean, canonical and current Japanese
slots/pointers are checked independently; complete English and NUL fit without
relocation. There are no other static pointer aliases. Full code/table allocation
and every unrelated ARM9 byte remain exact after restoring the three owned spans.

Characters is enabled by bit3 in the system halfword at0227985C. Event Scenes is
enabled by any low-four bit via original02046DFC. All16 combinations execute the
original submenu flag setup before/after: results, system memory and stack are
unchanged. The meaning of those bits is not inferred from the mask alone. The
fresh save's low-four bits remain0, so those two views are still genuinely locked.
No hidden entry is made available by this translation.

All three complete English labels execute the original native font raster inside
84x16 and pass every first/interior/final letter, blank cell, ink pixel and guard.
This is controlled native text evidence, not a full hidden-popup unlock/GPU test.

## Fresh corrected ROM

V307 repeats the31200-frame ordinary start/save/title/Gallery sequence with exactly
the successful V306 inputs. It shows the complete Items/Ruins popup in its original
bounds. Every native foreground/blank text cell matches independently decoded game
font pixels:126 ink pixels total. Actual color is8,8,8; the first check's assumed
0,8,0 color was corrected from the capture rather than weakening the glyph mask.
Save, title, popup and empty-collection images were inspected. No state is loaded,
RAM injected or progress flag altered; callback errors are empty and the process
exits successfully.

## Registered artifacts and preservation

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v307` |
| Candidate | `out/all_routes_combined_v307_candidate.nds` |
| ROM SHA256 | `61c64dba659daf74d6418842ef982f1517ddca8e4879deffda6da5b6c7980ff5` |
| Patch | `out/all_routes_combined_v307_candidate.xdelta` |
| Patch SHA256 | `87a9c79d257cd3163403327ac1e07a28dfb9bf01b1da4b3733347f3c3519e7c6` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Inherited comparison | `out/all_routes_combined_v305_candidate.nds` |
| Comparison SHA256 | `f9cba4b0b48a57f9afc51d7ef1d56f48fde6888202d65c237096f2d3407563d4` |
| Clean patch input | `work/clean.nds` |
| Clean SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Status | Experimental; user acceptance pending; canonical unchanged |

All470 inherited batches and every accepted requirement/stage remain. The named
profile adds a source/target-locked terminal label stage. The manifest records the
registry/config/evidence hashes, complete batch/profile stack and changed records.
Only ARM9's three string slots change versus V305. All native code/gates/tables,
fonts, graphics, route/COMMON/HELP text, ARM7, overlays, banner and entry addresses
remain byte-identical. Full V305 reproduces exactly before and after the shared
builder edit. The clean patch reconstructs the candidate exactly. Ruff passes.

## Remaining evidence and user checks

Test a new ordinary save and title Gallery access on the user's emulator. With a
legitimate suitable existing game save, check Characters/Event Scenes labels and
their full original layouts. Collection pages are empty in this test. Original
hidden-view access/artwork/GPU, legacy raw-comic/native composition and all18
plaque/hint entries with Armor/Weapon variants remain open. The earlier generic
unlocked-Gallery-save request is refined by this evidence: ordinary saves suffice
for Items/Ruins access; a save carrying the appropriate original system bits is
still needed for the two hidden views. No new user acceptance is inferred.

The low-resolution Online image translation exception remains. The full graphics
goal is active/incomplete. Revisit older record-based checks at actual completion,
including hidden variants and the difference between translated headings and menu
labels. V306/V307 evidence is under their `work/analysis` and `work/emulation_v193`
folders, with access/native/release proofs, exact reconstructed ROM and captures.
