# Known issues

## Options report and sailing-help prompt encoding

The Options confirmation prompts live in `__arm9__.bin`, but they are rendered by a
fixed-width Shift-JIS dialog path rather than the normal ASCII-capable menu renderer.
The original `options_menu_en.nds` inserted ASCII into those slots and is revoked: the
resulting text was visibly mangled (`Income reports` and `Sailing help`).

`out/options_menu_v2.nds` is the corrected research candidate. Its two prompts use
CP932 full-width Latin characters, retain the original `%s` substitutions, and are
built directly from `out/all_goods_roundtrip.nds`. Do not replace text in either
prompt with ASCII. Any future revision must retain the exact source-byte lock and be
cold-boot tested before promotion.

The scrolling BGM/SFX labels are not the same ARM9 caption table. They are now
mapped and translated in the corrected research candidate `out/sound_selector_en_v3.nds`:
38 BGM titles are packed across `/COMMON/MESFILE.DK4` block 36 records 46-63,
while 57 SFX titles occupy fixed or standalone ARM9 slots. The BGM panel uses a
double-byte glyph renderer: narrow ASCII produces fragmented/reordered glyph tiles
even when the packed offsets are correct. V1 and V2 are therefore superseded.
V3 uses centered full-width Latin labels within the original Japanese cell counts;
some titles are necessarily abbreviated until this panel is routed through the
normal narrow-Latin renderer. The candidate passes byte-level and baseline checks but
still requires a cold-boot test of every selector entry before promotion.

## Lil opening scene control preamble

Lil's actual opening is `/data/SC2.DK4`, block 22. Its dialogue records begin
with control sequences that affect the active portrait and name plate. Replacing
the visible Japanese text while retaining only a guessed byte prefix produces an
incorrect speaker and corrupts the first visible English glyph.

`lil_sc2_opening_repair.nds` and `lil_sc2_opening_repair_v2.nds` are revoked
research candidates and must not be distributed. The safe integration baseline
is `out/all_goods_roundtrip.nds`. Map the full control preamble in
a disposable live-tested probe before another SC2 block-22 translation build.

## Naming keyboard page selection

The naming popup still opens on the Japanese kana page. The visible `英` and `記`
entries are not ordinary captions: the keyboard manager also uses their exact encoded
values to identify the Latin and symbol pages. Replacing either value makes the
corresponding page render as a blank black panel.

For stability, the current build keeps those two functional identifiers unchanged.
The editor headings use direct translations such as `Name: Edit`; they no longer
contain instructions to press `英`.

Making Latin input the default remains a code-level task. It requires locating and
changing the keyboard manager's initial page index without modifying its page
identifiers. Until then, select `英` to reach the built-in Latin keyboard.

## Town-screen date suffixes

The compact date panel on town screens still renders Japanese `月` and `日` suffixes,
for example `1月 2日`. This is distinct from the translated birthday, inn-duration,
arrival-month, and shared calendar strings. It is also absent from the town graphics
atlas, indicating that the town HUD builds the date through a separate low-level
renderer.

Do not replace the shared Japanese font glyphs as a workaround: those glyphs remain
necessary for untranslated material and a global replacement would corrupt unrelated
screens. The safe follow-up is to locate the town HUD's formatter or glyph-emission
routine and change only that call site.
# Release baseline warning

- `out/all_goods_roundtrip.nds` is the user-designated safe integration baseline as of 2026-08-04.
- Its SHA-256 is `8e61fd4e8c444b25566cc273dd676b3e5bea5d683ad167db2f92444c10df9764`.
- All later integration, route, repair, and probe ROMs—including `lil_route_roundtrip.nds`, `raphael_complete_en.nds`, `raphael_complete_fixed.nds`, and the Lil repair probes—are deprecated historical artifacts. Do not distribute them or use them as a base.
- Run `scripts/verify_release_baseline.py out/all_goods_roundtrip.nds <candidate.nds>` before handing off any subsequent candidate.
