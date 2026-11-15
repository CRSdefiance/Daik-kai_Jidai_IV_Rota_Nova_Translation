"""Refine the seven source-reviewed retreat reports without authored layout."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.battle_reaction_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.retreat_transfer_native_plan_v1511 import compiled
from scripts.verify_village_wrap_v608 import read, save

SOURCE = Path('translations/retreat_transfer_editorial_manuscript_v1.json')
OUT = Path('translations/retreat_transfer_editorial_manuscript_v2.json')

if __name__ == '__main__':
    assert not OUT.exists()
    old = read(SOURCE)
    context = read(old['source_context'])
    assert sha(Path(old['source_context']).read_bytes()) == old['source_context_sha256']
    clean = NdsImage.open('work/clean.nds')
    current = NdsImage.open(old['current_ROM'])
    assert sha(Path(old['current_ROM']).read_bytes()) == old['current_ROM_sha256']
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    before = current_entries(current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin'))
    doc = deepcopy(old)
    for row in doc['records']:
        n = row['message_id']
        assert jp[n].text.hex() == row['source_hex']
        assert before[n].text.hex() == row['current_text_hex']
        assert row['english'].startswith("Our flagship's out of action!")
        row['english'] = row['english'].replace("Our flagship's out of action!", "Our flagship's been knocked out!", 1)
        row['localization_note'] = (
            "Render the source flagship's incapacitation as the natural combat report 'been knocked out', "
            "without asserting sinking, death or the loss of the whole fleet. Preserve the voice-specific "
            "report, command or suggestion and the single replacement-ship name. The original ship swap "
            "and surviving hull establish that 'knocked out' means out of action here. Read aloud with "
            "the original evacuation/defeat and following sailing transition. The earlier 'out of action' "
            "wording was faithful but its native preview stranded command heads such as Get/Fall; this "
            "equally faithful complete report also permits a clean command boundary without authored "
            "breaks, alignment spaces, omitted facts or a weaker meaning. All generated variants still "
            "require native font and visual review."
        )
        row['editorial_decision'] = 'revise'
        row['status'] = 'source-context-prose-refined;native-font-visual-release-and-original-transfer-pending'
        assert not row['review']['formatting']
        compiled(row)
    assert len(doc['records']) == 7
    doc.update(revised=7, retained=0, supersedes=str(SOURCE), supersedes_sha256=sha(SOURCE.read_bytes()),
               refinement_reason='Faithful incapacitation wording and complete urgent commands; no authored layout.',
               status='seven-source-context-prose-refined;native-font-visual-release-original-transfer-pending',
               producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUT, doc)
    print('Retreat7: seven source-faithful prose refinements; native formatting and gameplay gates remain pending.')
