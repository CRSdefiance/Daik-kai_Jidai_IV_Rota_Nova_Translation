"""Prepare complete B173 relocation with all four original relative handlers."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_relocation_tools_v4428')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B172_relocation_v4381.py','scripts/research_lil_B173_relocation_v4428.py',{
        'Relocate all27 B172 speeches;preserve eleven leaves,C200 then later A000 and one tail end.':'Relocate all11 B173 speeches;preserve four relative sites,predicate,two A000s,eight leaves and one tail end.',
        'lil_B172_relocation_v4381':'lil_B173_relocation_v4428','lil_B172_editorial':'lil_B173_editorial',
        'all_routes_combined_v4353':'all_routes_combined_v4404','number==172':'number==173',
        '[1880] # one complete source tail end preserved':'[762] # one complete source tail end preserved',
        'for r in results)==27':'for r in results)==11',
        "sum(len(r['relative_skip_fixups']) for r in results)==0":"sum(len(r['relative_skip_fixups']) for r in results)==4",
        "sum(len(r['target_native_skip_cases']) for r in results)==0 and sum(len(r['command_map']) for r in results)==38":"sum(len(r['target_native_skip_cases']) for r in results)==20 and sum(len(r['command_map']) for r in results)==23",
        '[172]':'[173]','all27speech_and11_nonrelative_leaves_preserved':'all11speech_and8_nonrelative_leaves_preserved',
        'no_source_relative_sites_or_native_skip_cases':'all4_source_relative_sites_and20_native_skip_cases_preserved',
        '38commands/27speech/noFE/no_relative_sites,no pause,C200 then later A000 andone tail end':'23structural commands/11speech/noFE/four relative sites/20 target cases,no pause,two A000s/one predicate/one tail end',
    })]
    tools.append(derive('scripts/prove_lil_B172_stored_v4382.py','scripts/prove_lil_B173_stored_v4429.py',{
        'all27':'all11','lil_B172_stored_v4382':'lil_B173_stored_v4429','lil_B172_editorial':'lil_B173_editorial',
        'lil_B172_relocation_v4381':'lil_B173_relocation_v4428','lil_B172_voices_v4365':'lil_B173_voices_v4412',
        '[2,26,201]':'[2,202]','len(cases)==27':'len(cases)==11','fresh+reused==108':'fresh+reused==44',
        'stored_targets108':'stored_targets44','current_final_stored_macro_alignment_cases=108':'current_final_stored_macro_alignment_cases=44',
        'stored_targets=27,progressive=27,FE=0':'stored_targets=11,progressive=11,FE=0','macro_cases=108':'macro_cases=44',
        'actual_selected_scenes_and_presentation_resource_later_A000_bodies_unexecuted':'actual_selected_scenes_and_presentations_resources_two_A000_bodies_unexecuted',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_scope=dict(block=173,speeches=11,structural_commands=23,
        nonrelative_leaves=8,relative_sites=4,target_operand_cases=20,predicates=1,pause=0,A000=2,C200=0,
        resources=[0x6329,0x6340],source_end_offsets=[762],presentations=[0x6000,0x6240],source_macros=0,final_stored_alignment_cases=44),
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared B173 relocation and44 stored alignment-case producers;all four relative sites and complete effects retained.')
