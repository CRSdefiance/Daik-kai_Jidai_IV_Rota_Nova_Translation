"""Prepare representative display fixtures using the exact rebuilt commands."""
import json
from pathlib import Path
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.prepare_rafael_B221_B240_actual_v1 import source as previous
from scripts.qualify_rafael_plett_relocation_v1 import REFERENCE, plan_surnames
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B261_B280_contextual_v1 import ROOT, sha


SELECTION = ROOT / 'focused_selection_v1.json'
PROPOSAL = REFERENCE / 'proposal.json'
NAME_PROOF = REFERENCE / 'native_v1/native_name_fields_verification.json'


def select():
    assert not SELECTION.exists()
    def speech(block, *indices):
        return [dict(speech=f'DK4_MES_B{block}_R{index:04d}') for index in indices]

    def menu(offset):
        return dict(menu=dict(block=261, source_command_offset=offset))

    def style(offset):
        return dict(style=dict(block=261, source_command_offset=offset, expected_style=4))

    sequence = [
        *speech(261, 6, 9, 12), menu(270), *speech(261, 31), style(342), *speech(261, 54, 72), style(852),
        *speech(261, 95, 114, 121, 125, 129, 140, 144, 148, 155), menu(1664), *speech(261, 170, 174, 178, 195, 206, 218),
        *speech(262, 7, 13), *speech(263, 6, 9), *speech(264, 6, 10),
        *speech(270, 5, 8, 12, 15, 19, 26, 31, 47),
        *speech(277, 6, 9), *speech(276, 16, 47), *speech(278, 47),
    ]
    save(SELECTION, dict(format='dk4-disclosed-native-dialogue-fixture-selection-v2',
         fixtures=[dict(name='rafael_puzzles_town_and_bounties', sequence=sequence,
                        purpose='Observe the two menus, both crew voice tables, FE instructions, the town FI greetings, Jacob’s nameplate, and the bounty page turn.')],
         chosen_fixture_path_is_a_display_sequence_not_original_branch_routing=True, guide_photos=False, new_credit=0))


source = checked_text(previous, {
    "    inventory, _, _ = scoped_inventory()":
        """    surname_proof=load(NAME_PROOF)
    assert surname_proof['proposal_sha256']==sha(PROPOSAL.read_bytes())
    corrected, name_plan=plan_surnames(arm,load(PROPOSAL),NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    assert json.loads(json.dumps(name_plan))==surname_proof['name_data_plan']
    assert sha(corrected)==surname_proof['versions'][1]['ARM9_sha256']
    inventory, _, _ = scoped_inventory()""",
    "        assert all(fixture.read_file(p) == v for p, v in image.iter_components())":
        """        assert all(fixture.read_file(p) == v for p, v in image.iter_components())
        fixture.replace_file('/__arm9__.bin',corrected)
        assert [p for p,v in image.iter_components() if fixture.read_file(p)!=v]==['/__arm9__.bin']""",
    "        inverse.replace_file(path, archive)":
        """        inverse.replace_file(path, archive)
        assert inverse.read_file('/__arm9__.bin')==corrected
        inverse.replace_file('/__arm9__.bin',arm)""",
    "            not_registered_candidate_or_natural_activation=True":
        """            proposed_surname_fields_applied=True,surname_proof_sha256=sha(NAME_PROOF.read_bytes()),
            not_registered_candidate_or_natural_activation=True""",
    "ORDINARY,args.roles,Path('scripts/prepare_reviewed_dialogue_fixtures_v2.py'),Path(__file__)":
        "ORDINARY,args.roles,PROPOSAL,NAME_PROOF,Path('scripts/prepare_reviewed_dialogue_fixtures_v2.py'),Path(__file__)",
})


if __name__ == '__main__':
    if sys.argv[1:] == ['--select']:
        select()
    else:
        exec(compile(source, __file__ + '::exact-initialized-fixture-with-both-surnames', 'exec'), globals())
