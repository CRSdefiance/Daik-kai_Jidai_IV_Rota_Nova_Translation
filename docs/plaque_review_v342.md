# Plaque review and Endurance fidelity V342

## Review sheets

These sheets show native source/current asset crops at 3x nearest-neighbor scale. No smoothing or pixel repainting is applied. All 18 entries remain in the ongoing audit. Original runtime stat text is omitted from the source artwork crops; its exact Japanese wording is printed above each card. The Equipped Items header uses an actual V341 capture, and Armor/Weapon variants retain their historical V299 capture labels. These are not relabeled as new V342 gameplay.

![assign_sailors_review.png](<C:/Projects/Personal Projects/g-p-6a676ab5787c819181af4a29d5cebfbc/dk4-translation-tool/work/analysis/plaque_review_v342/review_packet/assign_sailors_review.png>)

![sailor_info_review.png](<C:/Projects/Personal Projects/g-p-6a676ab5787c819181af4a29d5cebfbc/dk4-translation-tool/work/analysis/plaque_review_v342/review_packet/sailor_info_review.png>)

## Translation review

| Entry | Screen | Japanese | Current English | Meaning |
| --- | --- | --- | --- | --- |
| 1 | Assign Sailors | 艦隊水夫数 | Fleet Crew | Total sailors in the fleet, rather than an assignment command. |
| 2 | Assign Sailors | 未編成水夫数 | Unassigned | Sailors who have not been allocated to ships. |
| 3 | Assign Sailors | 航行可能日数 | Endurance | How many days the fleet can remain at sea; the value explicitly says days. |
| 4 | Assign Sailors | 海兵詰所 | Quarters | Marine quarters count; compact label denotes the rooms, not the number of marines. |
| 5 | Assign Sailors | 砲種 | Cannon | Cannon type, with its gun name displayed immediately to the right. |
| 6 | Assign Sailors | 縦帆性能 | Fore/Aft | Fore-and-aft sail performance, including more than lateen sails. |
| 7 | Assign Sailors | 横帆性能 | Square | Square-sail performance, paired with Fore/Aft. |
| 8 | Sailor Info | 身体 | Health | Physical condition, followed by Healthy, Sick, Injured or another condition. |
| 9 | Sailor Info | 精神 | Mood | Current mental condition; distinct from the permanent Spirit stat. |
| 10 | Sailor Info | レベル | Level | Character level. |
| 11 | Sailor Info | HP | HP | Current hit points. |
| 12 | Sailor Info | 体力 | Stamina | Physical stamina attribute. |
| 13 | Sailor Info | 敏捷 | Agility | Agility attribute. |
| 14 | Sailor Info | 魅力 | Charm | Personal charm attribute. |
| 15 | Sailor Info | 知力 | Wits | Intellectual ability; concise natural English stat label. |
| 16 | Sailor Info | 精神 | Spirit | Mental fortitude attribute, separate from the current Mood condition. |
| 17 | Sailor Info | 運勢 | Luck | Luck attribute; exact native source is 運勢. |
| 18 | Sailor Info | 装備アイテム | Equipped Items | Items currently equipped; Weapon and Armor are variants of this same entry. |

All 17 sprite regions remain byte-exact to V341; their lettering/style is preserved. The review confirms the contextual distinction between Mood and Spirit, marine quarters rather than a marine-person count, and fore-and-aft performance rather than only lateen sails.

## Source approximation restored

The original Endurance caption is約%d日: approximately %d days. Earlier English %d days omitted that qualification. V342 reads ~%d days, using the original native tilde glyph and unchanged numeric argument/calculation. The new nine-byte format needs a terminator beyond the old eight-byte slot, so its one pointer redirects to a source-locked appended string in the owned pool. Existing source strings, backing sprite assets, renderer code and prior payload bytes remain exact. Startup/cache/ARM7/arena checks cover the extension.

Twenty complete native rasters cover 0/1/9/10/99/100/999/65535 and both signed 32-bit limits in 4-bit and 16-bit formats. These use supplied text geometry; actual parent proof is separate. A matched pair of fresh 11,200-frame cold boots reaches title, Lil selection/opening, town and Assign Sailors. Normal Lo/Hi inputs exercise three crew states without a savestate or RAM injection. Actual ~0 days has complete independent native font masks in all three captures; 21 entire plaque instances match the integrated assets. All changed framebuffer pixels lie only in the duration row. Other 36 comparable captured frames are exact to V341. Both emulator processes terminate normally. Actual nonzero durations and other routes remain unclaimed.

V341 reproduces byte-exact. All 470 inherited accepted/experimental batches, required layers and prior stages/records remain. Only ARM9 changes versusV341. The clean-input patch reconstructs V342 exactly. Focused Ruff passes.

## Integrated experimental candidate

| Artifact | Identity |
| --- | --- |
| ROM | `out\all_routes_combined_v342_candidate.nds` |
| ROM SHA256 | `1f6bda701f2bf95393037f8e4d9a94ffb7190ec418d8a6e77f42f217a8736305` |
| Patch | `out\all_routes_combined_v342_candidate.xdelta` |
| Patch SHA256 | `03e656fafb9f3c0fa3804bfbdf661147a7e83696c2827187e3fa4d8892104ff2` |
| Profile | `all-routes-unified-v342` |
| Canonical base | `out\raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |

The canonical baseline stays unchanged. V342 is experimental pending user cold-boot acceptance. Review title/New Game, town, Assign Sailors duration/plaque layout and existing Sailor Info. These are targeted automated emulator checks, not a full route or hardware-device verification.

## Remaining audit

All 18 plaques/hints and variants retain completion false, per the user instruction. Actual occupied weapons/armor, alternative conditions and broader route/fleet contexts stay open. Source-retained/legacy artwork callers, regional map palettes, unavailable diplomacy displays, ending/Gallery contexts and other ledger requirements also remain open. Low-resolution Online images remain user-exempt. Revisit older record-based checks at actual full-goal completion.

Evidence: work/analysis/plaque_review_v342/native_proof.json, release_proof.json, review_packet/review_inventory.json and the two Endurance capture reports. Scripts: prepare_endurance_v342.py, verify_endurance_v342.py --live and build_plaque_review_v342.py.
