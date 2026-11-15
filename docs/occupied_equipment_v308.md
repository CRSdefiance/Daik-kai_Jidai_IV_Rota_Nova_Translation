# Occupied equipment audit checkpoint V308

This checkpoint tests the existing V307 ROM. No new ROM or patch was needed.
Candidate: `out/all_routes_combined_v307_candidate.nds`, SHA256
`61c64dba659daf74d6418842ef982f1517ddca8e4879deffda6da5b6c7980ff5`.

## Actual acquisition and display

A fresh DeSmuME cold boot ran 34,400 frames using ordinary controller/touch
inputs. No savestate was loaded. Rafael entered Lisbon's Guild, purchased
Travels of Marco Polo for 10,000 coins, and equipped it through Items, Y, and
the ordinary character selection. Frame30000 shows the equip confirmation;
frame30400 shows Equipped By Rafael. Info > Sailors reaches Sailor Info.
Frame34400 selects the occupied third equipment slot and shows the book title.

`scripts/record_occupied_equipment_v308.py` verifies every captured PNG hash
against the capture report and the current ROM identity. Results:

- All223 book tooltip letter pixels and blank cells match the native font.
- All2,080 pixels of the 130x16 paper, lettering and corners match at native
  color precision; the complete title fits the original box.
- All1,024 original book icon pixels match source item88.
- Rafael Castor's complete name and all10 skill/value lines match the font.
- All17 graphics plaques match their inherited source-locked English assets
  in the actual Assign Sailors and Sailor Info views.

The historical Japanese item title is 東方見聞録; Travels of Marco Polo remains
the established English title. This checkpoint retains the prior translation
review and adds current display evidence, rather than treating pixels as
independent proof of meaning. Speech is122 in this capture; no stat-effect
arithmetic is inferred from that value.

Evidence: `work/analysis/occupied_equipment_v308/live_proof.json` and
`work/emulation_v193/occupied_equipment_v308_corrected/capture_report.json`.

## Navigation and limitations

The earlier replay followed an old input schedule and reached Sea View.
Its captures remain in `work/emulation_v193/occupied_equipment_v308`; they
receive no purchase or occupied-equipment credit. The corrected run identified
each town facility and menu before proceeding. The Guild stock contained the
book, a Sextant, and a map. No weapon or armor was acquired in this run.

The equip confirmation wraps Marco between lines as Ma / rco. Every letter
is visible, but that word break remains a formatting issue to audit. This
checkpoint does not certify all confirmation paragraphs or word wrapping.

All18 ongoing plaque/hint entries, including the Armor and Weapon variants,
remain `fully_completed:false`. Actual occupied weapon/armor, alternate
health/mood and further route/fleet contexts remain open. These are targeted
automated emulator checks, not a complete playthrough or hardware test.

## User scope and dialogue margins

The user exempts low resolution Online game images from translation. Both
authoritative audits retain that exception for Online24/27/31/33; existing edits
and historical evidence remain intact. These images do not block the goal.

The submitted shopkeeper indentation was corrected in V258, which aligns both
lines at x22 without dropping letters. See `common_dialogue_left_alignment_v258.md`.
That renderer change remains inherited by the current profile.

The graphics goal remains incomplete. Revisit older record-based checks when
the entire goal is actually complete.
