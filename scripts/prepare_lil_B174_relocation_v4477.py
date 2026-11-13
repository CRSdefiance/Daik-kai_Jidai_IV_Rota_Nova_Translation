"""Prepare reversible B174 relocation, retaining its optional speech and effect tail."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_relocation_tools_v4477')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B173_relocation_v4428.py','scripts/research_lil_B174_relocation_v4477.py',{
        'Relocate all11 B173 speeches;preserve four relative sites,predicate,two A000s,eight leaves and one tail end.':
            'Relocate all33 B174 speeches;preserve conditional Emilio,four relative sites,predicate,two A000s,C200,eight leaves and single end.',
        'lil_B173_relocation_v4428':'lil_B174_relocation_v4477',
        'lil_B173_editorial_manuscript_v3':'lil_B174_editorial_manuscript_v5',
        'all_routes_combined_v4404':'all_routes_combined_v4445','number==173':'number==174',
        '[762] # one complete source tail end preserved':'[2086] # one complete source tail end preserved',
        'for r in results)==11':'for r in results)==33',
        "sum(len(r['command_map']) for r in results)==23":"sum(len(r['command_map']) for r in results)==45",
        '[173]':'[174]','all11speech_and8_nonrelative_leaves_preserved':'all33speech_and8_nonrelative_leaves_preserved',
        '23structural commands/11speech/noFE/four relative sites/20 target cases,no pause,two A000s/one predicate/one tail end':
            '45structural commands/33speech/noFE/four relative sites/20 target cases,no pause,two A000s/one predicate/C200/one tail end',
    }),derive('scripts/prove_lil_B173_stored_v4429.py','scripts/prove_lil_B174_stored_v4478.py',{
        'all11':'all33','lil_B173_stored_v4429':'lil_B174_stored_v4478',
        'lil_B173_editorial_manuscript_v3':'lil_B174_editorial_manuscript_v5',
        'lil_B173_relocation_v4428':'lil_B174_relocation_v4477','lil_B173_voices_v4412':'lil_B174_voices_v4454',
        '[2,202]':'[2,14,26,201]','len(cases)==11':'len(cases)==33','fresh+reused==44':'fresh+reused==132',
        'stored_targets44':'stored_targets132','current_final_stored_macro_alignment_cases=44':'current_final_stored_macro_alignment_cases=132',
        'stored_targets=11,progressive=11,FE=0':'stored_targets=33,progressive=33,FE=0','macro_cases=44':'macro_cases=132',
        'actual_selected_scenes_and_presentations_resources_two_A000_bodies_unexecuted':
            'actual_selected_scene_presentations_resource_two_A000_and_C200_bodies_unexecuted',
    })]
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_scope=dict(block=174,speeches=33,
        structural_commands=45,nonrelative_leaves=8,relative_sites=4,target_operand_cases=20,
        predicates=1,pause=0,A000=2,C200=1,resources=[0x6340],source_end_offsets=[2086],
        presentations=[0x6000,0x6240],source_macros=0,final_stored_alignment_cases=132),
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared B174 reversible relocation and132 stored native alignment cases, preserving all45 commands.')
