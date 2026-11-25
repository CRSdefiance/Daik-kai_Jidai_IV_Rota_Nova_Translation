# V467 London checkpoint and V468 shared crew-header correction

Experimental. The full graphics goal remains active; all22 historical requirements
and all18 incomplete plaque entries remain in the audit.

## Genuine voyage checkpoint

The Port Worker warns that the flagship is short of sailors. The assignment
screen shows19 current against39 needed. Ordinary Tavern recruitment and
Auto→Minimum assign39. Complete native number masks verify Need39, Now39 and
Max124. The33 unassigned shown during setup are not a carried reserve: the later
London view and cold-loaded view show zero unassigned.

Normal steering reaches London after a Speyer patrol and observed withdrawal,
not victory. The game discovers London and confirms docking. Port resupply and
an ordinary10-night Inn stay complete. The London town indicator is already0
on arrival and remains0 after the Inn/reload; no17→0 reduction is credited.
Numbers/months seen only visually are not economy/calendar arithmetic proofs.
The normal slot6 overwrite completes with4100 more frames before termination.

Normal save and cold load retain London, the39 assigned sailors and Blue Oak
clue1. The original Copenhagen donor remains exact. Save on E:

`Saves\hodram-london-rested-minimum-crew-v464.dsv`

SHA-256: `05fa512b078fd01a8f6bee605254e9f72bfe3453c0ea098d977c87d86b6b693e`

Checkpoint proof: `work/analysis/shield_voyage_v467/london_proof.json`.
Verifier: `scripts/verify_london_checkpoint_v467.py`.
Armor/Weapon acquisition and occupied displays remain open.

## Layout defect and shared correction

Matched native glyphs locate the old Need/Now/Max headers at116/158/194, while
their number columns end at160/196/232. The header line ends20 pixels too far
left. Original draw0201E4B8 uses point02114E90 through its unique direct pointer
at0201E634. Moving that point's x from116 to136 shifts the whole inherited
heading line20 pixels. Its y, all strings, fonts, numbers, artwork, palettes,
dimensions, borders and other ARM9 data/code remain unchanged. Only one byte in
the four-byte coordinate word differs.

Complete corrected glyph bounds:

| Header | Bounds | Number-column right edge |
| --- | --- | --- |
| Need | 136,192–160,203 | 160 |
| Now | 178,192–196,203 | 196 |
| Max | 214,192–232,203 | 232 |

Source 必要数／現在数／最大数 means required/current/maximum sailor counts.
The inherited short English labels remain faithful. The seven plaque meanings
are retained: Fleet Crew=艦隊水夫数; Unassigned=未編成水夫数;
Endurance=航行可能日数; Quarters=海兵詰所, a room count; Cannon=砲種,
the cannon type; Fore/Aft=縦帆性能; Square=横帆性能. Cannon is not a gun-deck
room-count label. Existing native textured paper/borders remain pixel exact.

## Evidence and release

Matched genuine-save cold boots cover Vestaros's39/39/124 and Carteria's9/16/24.
All14 complete plaque instances match the current ROM. Every pixel outside the
header region matches V464; every first/interior/final header glyph and blank
cell matches the original font. The London save cold-loads in V468 with39 assigned.
All56 earlier title/New Game/character/story/town/Help-entry frames match V464.
These are targeted DeSmuME tests, not hardware or full-game verification.

Release proof: `work/analysis/crew_columns_v468/release_proof.json`.
Verifier: `scripts/verify_crew_columns_v468.py`; changed files pass Ruff.

ROM: `all_routes_combined_v468_candidate.nds`

SHA-256: `1d9b297779847af1a9515070bc139e6d08c842628559e029a13515347c47d59a`

Patch SHA-256: `e2a77e6ca6c559d4d5dd4be73b1ed055082fd0143af6c508edcf01dbd6390a88`

Profile: `all-routes-unified-v468`. All470 V464 batches and every inherited stage
are preserved, along with the canonical base's114 accepted-layer declarations.
Only `/__arm9__.bin` differs from V464. The clean-ROM patch reconstructs the
entire candidate exactly. No file, section, pool, arena or4096-byte ITCM growth.

Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
No canonical promotion. ROM/patch/manifest and three finalized guide captures are
copied byte exactly to `E:\Rota Nova translations` and its `Screenshots` folder.
User cold-boot areas: title/New Game and established story/town screens, then
Assign Sailors on small/large ships, including minimum assignment and headers.

Next: continue the earned shield search from London, with normal supply stops;
retain all other legacy/environment/ending/alternate-state requirements. Revisit
older record-based checks when the full goal is actually complete.
