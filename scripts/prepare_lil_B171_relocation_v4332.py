"""Derive B171 relocation and final stored-byte proofs from reviewed producers."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B171_relocation_tools_v4332')

if __name__ == '__main__':
    assert not ROOT.exists()
    tools = [derive('scripts/research_lil_B170_relocation_v4281.py', 'scripts/research_lil_B171_relocation_v4332.py', {
        'Relocate all33 B170 speeches;preserve twelve leaves,one pause,C200 and both consecutive ends.': 'Relocate all37 B171 speeches;preserve eight leaves,C200 and both consecutive ends.',
        'lil_B170_relocation_v4281': 'lil_B171_relocation_v4332',
        'lil_B170_editorial_manuscript_v5': 'lil_B171_editorial_manuscript_v4',
        'all_routes_combined_v4251': 'all_routes_combined_v4303',
        'assert number==170 and len(end_maps)==2': 'assert number==171 and len(end_maps)==2',
        '[1852,1856]': '[2112,2116]',
        'for r in results)==33': 'for r in results)==37',
        "sum(len(r['original2000_pause_and_resume_maps']) for r in results)==1": "sum(len(r['original2000_pause_and_resume_maps']) for r in results)==0",
        '[170]': '[171]',
        'all33speech_and12_nonrelative_leaves_preserved': 'all37speech_and8_nonrelative_leaves_preserved',
        'one_original2000_pause_and_resume_preserved': 'no_source2000_pause_commands',
        'no_source00_or_dynamic_objects': 'no_source_dynamic_speaker_objects',
        '45commands/33speech/noFE/no_relative_sites,one pause andtwo consecutive ends': '45commands/37speech/noFE/no_relative_sites,no pause andtwo consecutive ends',
    })]
    tools.append(derive('scripts/prove_lil_B170_stored_v4282.py', 'scripts/prove_lil_B171_stored_v4333.py', {
        'all33': 'all37', 'lil_B170_stored_v4282': 'lil_B171_stored_v4333',
        'lil_B170_editorial_manuscript_v5': 'lil_B171_editorial_manuscript_v4',
        'lil_B170_relocation_v4281': 'lil_B171_relocation_v4332',
        'lil_B170_voices_v4262': 'lil_B171_voices_v4312',
        '[2,25]': '[2,25,81]', 'len(cases)==33': 'len(cases)==37',
        'fresh+reused==132': 'fresh+reused==148', 'stored_targets132': 'stored_targets148',
        'current_final_stored_macro_alignment_cases=132': 'current_final_stored_macro_alignment_cases=148',
        'stored_targets=33,progressive=33,FE=0': 'stored_targets=37,progressive=37,FE=0',
        'macro_cases=132': 'macro_cases=148',
        'actual_selected_scenes_and_later_A000_body_unexecuted': 'actual_selected_scenes_and_presentation_resource_bodies_unexecuted',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=tools, source_scope=dict(block=171,
        speeches=37, commands=45, nonrelative_leaves=8, relative_sites=0, predicates=0,
        pause=0, A000=0, C200=1, resources=[0x6325], source_end_offsets=[2112,2116],
        presentations=[0x6000,0x4500,0x4621,0x61FF], final_stored_alignment_cases=148),
        no_ROM_registry_ledger_orcredit_change=True, full_goal_complete=False))
    print('Prepared B171 relocation and148 stored alignment-case producers; all eight leaves and both ends retained.')
