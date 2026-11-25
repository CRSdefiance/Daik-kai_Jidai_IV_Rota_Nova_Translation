# Ordinary equipment and save verification V320

No ROM or artwork changes were needed. V318 remains the latest registered
candidate, SHA256
`45b549eafee6a9cf3ff2d8a4e637f8722ebd52fb61dfa9b1dc5adab2fe6d1007`.

## Actual gameplay and display evidence

A targeted automated DeSmuME test cold boots V318 with a byte-exact copy of the
genuine earlier Rafael cartridge save. Ordinary controller and stylus inputs
purchase a Sextant at Lisbon's Guild for 2,500 coins, equip it on Julio Erneco,
and inspect four crew members through Info > Sailors. No savestate, live memory
edit or synthetic unlock is used. The first run ends normally at 32,000 frames.

The current ROM's native font and source-preserved graphics verify:

- 40 complete plaque instances across Julio, Janus, Claudio and Rafael.
- 40 complete skill/value lines, including blank cells and first/final letters.
- The four complete character names.
- All 90 lettering pixels and blank cells of the occupied Sextant tooltip,
  at `(114,210)` with the actual orange native text color.
- The complete Equipped Items hint in Julio's default slot selection.
- All 1,024 unobscured Sextant icon pixels, source item index 125. The current
  entire item atlas remains byte-identical to the clean ROM.

The occupied icon contains a visible red overlay. Exactly 864 of its pixels
match the source icon at native color precision; the other 160 are retained
as a separate native-composition obligation. The failed first whole-icon
assertion was an incorrect assumption that this equipped icon lacked an
overlay, not an established asset defect. No pixels were altered to pass it.

## Genuine saved progress

Functions > Save writes only the runner's isolated cartridge-save copy.
The original input save remains byte-identical. A second fresh cold boot
loads a copy of this new save through Continue and uses ordinary inputs to
select Julio and his occupied Sextant. That run ends normally at 6,400 frames.

The resulting complete 256x384 Sailor Info screen matches the first run's
occupied-slot capture exactly: all 98,304 framebuffer pixels. The purchase,
equipped item, name, values, plaques and tooltip survive a genuine save/reload.
This is a verified starting point for subsequent gameplay tests.

Save: `work/emulation_v193/ordinary_equipment_v320/saves/all_routes_combined_v318_candidate.dsv`.
Its exact hash and both capture-report hashes are recorded in
`work/analysis/ordinary_equipment_v320/live_proof.json`.

## Navigation and remaining work

Lisbon's Guild icon is at bottom-screen `(20,145)`. Current observed stock is
Travels of Marco Polo, Sextant and Twisted Horn Map 2; no weapon or armor is
available there in this context. A radial-menu touch rotates the touched
command into selection; A opens it. Merely touching a command does not open
its submenu. Use the observed labels rather than assuming fixed wheel positions.

The actual displayed Survey values are Julio 110 with the equipped Sextant,
Janus 100, Claudio 63 and Rafael 80. No before/after stat arithmetic or all-crew
eligibility conclusion is inferred. The prior deck context requires 120;
this test does not reach Auto Move, an actual voyage or its Stop footer.

All 18 plaque/hint audit entries and their Armor/Weapon variants remain
`fully_completed:false`. Actual occupied weapon/armor, alternate conditions,
additional route/fleet contexts, legacy viewers, FLS final rendering and other
remaining requirements are still open. Low resolution Online images remain
excluded by the user. These checks are not a whole-game playthrough or physical
device verification. The graphics goal remains active; revisit older
record-based checks when the entire goal is complete.

Evidence is reproducibly checked by `scripts/record_ordinary_equipment_v320.py`.
Both graphics audits record the current proof; the script passes Ruff.
