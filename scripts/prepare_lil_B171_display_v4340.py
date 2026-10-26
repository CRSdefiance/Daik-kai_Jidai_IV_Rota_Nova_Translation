"""Prepare paired complete B171 content fixtures and ordinary read-only cold boots."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B171_display_tools_v4340')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B170_display_fixture_v4291.py','scripts/research_lil_B171_display_fixture_v4340.py',{
        'B170':'B171','lil_B170':'lil_B171',
        'display_fixture_v4291':'display_fixture_v4340','display_v4291':'display_v4340',
        'all_routes_combined_v4251':'all_routes_combined_v4303',
        'relocation_v4281':'relocation_v4332','editorial_manuscript_v5':'editorial_manuscript_v4',
        '[170]':'[171]','source_block=170':'source_block=171',
        "sum(command['word'] == 0xA000 for command in commands) == 1":"sum(command['word'] == 0xA000 for command in commands) == 0",
        'len(walk) == 54 and len(speeches) == 33':'len(walk) == 54 and len(speeches) == 37',
        "sum(command['word'] == 0xA000 for command in walk) == 5":"sum(command['word'] == 0xA000 for command in walk) == 4",
        'all33_progressive_source_texts_pause_resources_later_A000_and_C200_retained_without_flattening':'all37_progressive_source_texts_presentations_resource_and_C200_retained_without_flattening',
        'source_event170_not_selected_or_eligibility_earned':'source_event171_not_selected_or_eligibility_earned',
        'source_B170_later_A000_hex1019_2001_resources_presentations_pause_C200_and_both_ends_retained':'source_B171_4500_4621_61FF_6325_C200_and_both_ends_retained_without_invented_A000_or_pause',
        'stored_speech_objects=33':'stored_speech_objects=37',
        'actual_linear_path_pause_effect_C200_and_end_reachability_to_be_observed':'actual_linear_path_dream_morning_C200_and_end_reachability_to_be_observed',
        'Paired B170 fixtures:33 progressive speeches,45 source commands plus9 original init commands;pause,resources,later A000,C200 and both ends retained.':'Paired B171 fixtures:37 progressive speeches,45 source commands plus9 original init commands;presentations,resource,C200 and both ends retained.',
    })]
    tools.append(derive('scripts/run_lil_B170_display_fixture_v4292.py','scripts/run_lil_B171_display_fixture_v4341.py',{
        'B170':'B171','lil_B170':'lil_B171',
        'display_fixture_v4291':'display_fixture_v4340',
        'display_run_v4292':'display_run_v4341','display_v4292':'display_v4341',
        'source_event170_not_selected':'source_event171_not_selected',
        "'displayed_original_source_block':170":"'displayed_original_source_block':171",
        'all_source_commands_and_later_A000_retained':'all_source_commands_presentations_resource_and_C200_retained',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=171,speeches=37,source_commands=45,
        stored_fixture_commands=54,original_B22_init_commands=9,original_B22_init_A000=4,
        source_A000=0,source_pause=0,source_declared_end_offsets=[2112,2116],
        source_presentations=[0x6000,0x4500,0x4621,0x61FF],source_resource=0x6325,C200=1,
        no_source_command_omission_flattening_or_forced_predicate=True,
        no_natural_eligibility_recruitment_or_earned_flag_claim=True,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared paired complete B171 fixtures and20001-frame cold boots;all45 source commands retained.')
