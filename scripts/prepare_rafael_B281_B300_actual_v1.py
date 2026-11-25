"""Build a focused native command sequence with the qualified Zaganos name."""
import sys

from scripts.audit_story_glyph_consistency import save
from scripts.prepare_rafael_B261_B280_actual_v1 import source as previous
from scripts.qualify_rafael_zaganos_name_v1 import OUT, ROOT
from scripts.source_locked_derivation_v5118 import checked_text


SELECTION = ROOT / 'focused_selection_v1.json'
PROPOSAL = OUT / 'proposal.json'
NAME_PROOF = OUT / 'native_v1/native_name_fields_verification.json'


def select():
    assert not SELECTION.exists()

    def speech(block, *indices):
        return [dict(speech=f'DK4_MES_B{block}_R{index:04d}') for index in indices]

    def style(offset):
        return dict(style=dict(block=293, source_command_offset=offset, expected_style=4))

    def menu(offset):
        return dict(menu=dict(block=293, source_command_offset=offset))

    sequence = [
        *speech(281, 5, 8, 23, 54), *speech(284, 54), *speech(290, 5, 8),
        *speech(292, 6), style(24), style(328), style(678), *speech(293, 98), menu(884), style(980),
        style(1176), menu(1906), style(1954), style(2428), style(3074), style(3334),
        *speech(293, 396, 409, 412), *speech(294, 6), *speech(296, 13, 17),
        *speech(298, 46), *speech(300, 5, 9),
    ]
    save(SELECTION, dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',
         fixtures=[dict(name='rafael_bear_ruins_and_bounties', sequence=sequence,
                        purpose='Check both bear menus, alternate voices, chant page turns, bounty names, substitutions and gold notices.')],
         chosen_fixture_path_is_a_display_sequence_not_original_branch_routing=True, guide_photos=False, new_credit=0))


source = checked_text(previous, {
    "    corrected, name_plan=plan_surnames(arm,load(PROPOSAL),NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))":
        "    corrected, name_plan=plan_arm9_name_fields(arm,load(PROPOSAL),NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))",
    "    assert json.loads(json.dumps(name_plan))==surname_proof['name_data_plan']":
        "    assert name_plan==surname_proof['name_data_plan'] and name_plan['changed_bytes']==1",
})


if __name__ == '__main__':
    if sys.argv[1:] == ['--select']:
        select()
    else:
        from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
        exec(compile(source, __file__ + '::exact-initialized-fixture-with-Zaganos-surname', 'exec'), globals())
