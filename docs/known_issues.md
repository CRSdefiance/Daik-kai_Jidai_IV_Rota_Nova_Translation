# Known issues

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
