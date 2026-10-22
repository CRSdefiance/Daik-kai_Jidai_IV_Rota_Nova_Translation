# V582: ordinary New Game name editor and Latin keyboard

V581 remains the current experimental ROM. This is new native UI evidence;
no ROM, translation, runtime helper, release profile or patch changes.

## Ordinary controls and source-linked behavior

A fresh cold boot with no existing battery save reaches Rafael's selection and
name confirmation. B returns to his biography, where the actual footer says
Y Edit. Y opens **Name: Edit** with the first-name field selected; A opens its
keyboard. Earlier taps while normal confirmation was active did not enter this
state. They must not be cited as inability to edit names.

The keyboard initially offers Japanese characters. Selecting its functional
**英** key and pressing A opens the original Latin page. A touch positions the
selection; activation uses A in this observed sequence. The full page contains
lowercase a-z followed by uppercase A-Z. These are character-entry choices,
not Japanese instructions requiring translation. The functional 英/記 resource
identifiers remain intact.

A inserts lowercase full-width a; Y Delete removes that whole character. X Finish
returns the intact name Rafael to confirmation. B returns to the prior name-edit
screen. It does not leave editing for the biography. No gameplay Save action is
performed and no existing user save is loaded or edited.

## Complete glyph and buffer evidence

All52 Latin cells match the original `/GRP/KANJI.FNT` and original ARM9 Shift-JIS
map. There are888 ink points and6,864 complete twelve-by-eleven cell positions.
The entire140x84 table foreground mask (11,760 positions), including inter-cell
gaps and unused slots, contains exactly the expected letters. Native cells have
14-pixel column/row pitch. The plain dialogue ASCII font was an incorrect first
comparison model; these are full-width Shift-JIS glyphs. No font or ROM correction
was needed.

The actual editor parent is0218EEC8, its string buffer is parent+B4 and its native
name limit is16. The captured outer/provider/child vtables are021558CC/0215591C/
02155D44. Before insertion the buffer is `Rafael\0`; at5700 it is
`52 61 66 61 65 6C 82 81 00`; after deletion it is `Rafael\0` again. The live provider
executes original D1E3C/D1BBC and resolves 英 to index50 with the complete52-entry
two-byte Latin table. These bounded replays use the captured real object and do
not modify the running game. This does not establish maximum-length boundaries,
password normalization or every other keyboard page.

Complete native masks verify Name: Edit, Name, the initial editor Rafael, the
post-deletion Rafael and both confirmation names. Name uses the measured gray
(213,214,213); the other checked strings use(230,230,230). First/final letters
and all blank cells pass. The full98,304-pixel name-edit frame at4400 returns
exactly at6500. Initial confirmation and post-edit confirmation differ at182
pixels, all inside the state header[16,198,100,209]: Choose Captain versus
Name: Edit. Every other pixel is exact. The latter title itself has a complete
passing native font mask; the state difference is not treated as a defect.

## Confirm consumer investigation remains open

The separate48x20 `kakutei.pxl` Confirm graphic is not found at any native position
in eight selected confirmation/editor/Latin/return frames. This compares all881
opaque source pixels and respects the original79 transparent pixels, using the
original palette0 colors. It does not exclude clipping, scaling, other banks,
arbitrary modulation, unsampled transitions or other screens.

An aligned ARM PC-relative-load scan across every current main section and the
declared overlay finds two direct loads of owner023139C0, at0210EBDC/0210EBE8.
Both are in the original startup initializer, consistent with the already proven
registered filename. The first exploratory linear disassembly stopped at embedded
data; its zero-reference result was discarded. The corrected scan is recorded
by the permanent verifier. This is not proof of global non-use: arithmetic,
indirect pointers, aliases and other display layouts remain possible.

The Name editor is now a verified native context, but it does not resolve the
separate Confirm graphic or the five miniature bitmap callers.

## Evidence and reproduction

- Verifier: `scripts/verify_name_editor_native_v582.py`; targeted Ruff passes.
- Proof: `work/analysis/confirm_consumers_v582/native_name_editor_proof.json`.
- Exact replay: `final_recorded_inputs.json` in that directory.
- Original initialization/disassembly diagnostics are retained alongside the proof.
- Native report, screenshots and read-only pause RAM: E:/Rota Nova translations/
  Generated/work/emulation_v193/name_editor_v582.
- Nine unmodified full screenshots, report, replay and hashed provenance:
  E:/Rota Nova translations/Screenshots/Guide candidates/V581 Name editor.
  These are guide candidates only; publication is not approved.

For unattended reproduction, use a fresh output directory, the V581 ROM,
`--frames 6500 --inputs-json` with the final recorded schedule,
`--capture-every 6500 --capture-at 1600 2000 2400 2800 3200 3600 4000 4400 4800 5200
5500 5700 5900 6100 6300 6500 --dump-capture-ram --touchscreen`, without a battery
save or any synthetic-fixture option. The recorded run instead pauses interactively
at the documented states; that original report remains authoritative. Inspect
new provenance before changing the verifier's named evidence directory.

Candidate SHA256 remains542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68;
patch SHA256 remainse411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415.
All18 original plaque inventory entries remain incomplete; all22 historical
requirement objects retain their exact scope. Remaining material, legacy/event/
movie and actual consumer gates stay open. The graphics goal remains active;
revisit older record-based checks at actual full completion.
