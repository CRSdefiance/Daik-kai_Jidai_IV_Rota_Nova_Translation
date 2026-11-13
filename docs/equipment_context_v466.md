# V466 actual inventory and rested post-Speyer checkpoint

V464 is unchanged. The previous turn produced a normal supplied at-sea save.
This turn checks actual equipment eligibility and recovers the fleet in port.

## Inventory and original search gates

Normal Items displays “You don't have any items.” Its entire native glyph mask
passes, including the leading Y, final period and blank cells. Laocoon Sword25
and Crescent Shotel27 have a nonzero found/exclusion flag; this is not proof of
player ownership or an occupied equipment slot. Neither is credited as owned.

All218 original category queries identify54 Weapon/Armor records. The unchanged
original search fragment02079C68..02079C88 executes for every one using genuine
captured records. It skips unknown-clue items and nonzero exclusion flags. Only
Blue Oak Shield49 passes these initial gates. Entry/register storage and stop
addresses are explicit isolated test contracts; full search/acquisition is not
claimed. No flags, live RAM or battery progress are synthesized.

Original item-point virtual020499FC returns map coordinates19464,5192. The
original fleet-point virtual0202C1C4 matches the actual ship world coordinates
divided by128. The shield's derived world target is2491392,664576. Original
search-radius getter020655B8 returns32 map units, equivalent to4096 world units.
Both point buffers preserve outer guards; the complete captured RAM is unchanged.
These unit checks prevent confusing the small map coordinates with world values.

## Normal recovery, save and reload

Normal steering reaches the Copenhagen docking prompt. Inn→Stay More→30 nights
lowers displayed fatigue38→0. Two ordinary Treat Everyone rounds give fleet
rumors; no new equipment clue is credited. Functions→Save→slot6 confirms the
overwrite and completes after4100 more frames. The isolated saved battery then
cold-loads normally. Zero-fatigue glyphs, complete Copenhagen/coordinate/goods
masks and Blue Oak clue1 survive. The original post-Speyer donor is unchanged.

The final guide capture is an actual256x384 DeSmuME framebuffer and copied
unchanged to E Screenshots. Every PNG and both terminal reports are hash checked.
This is targeted emulator verification, not hardware or full-game completion.

Verifier: `scripts/verify_equipment_context_v466.py`.
Proof: `work/analysis/equipment_context_v466/context_proof.json`.
Reports: `work/emulation_v193/equipment_context_v466/capture_report.json` and
`work/emulation_v193/rested_equipment_reload_v466/capture_report.json`.

Normal save:
`E:\Rota Nova translations\Saves\hodram-copenhagen-rested-post-speyer-v464.dsv`

SHA-256: `dd6fbb734ef6f9fd3819a5c40cb4f0d38c304194027042469d1bee4dc729d822`

Next: depart from this recovered post-encounter checkpoint and pursue the earned
shield, using a water route and regular port stops. Weapon/Armor occupancy,
alternate states and other graphics consumers remain open. All22 historical
requirements and all18 incomplete plaques remain. No new ROM, artwork edits or
canonical promotion. Revisit older record-based checks at actual full completion.
