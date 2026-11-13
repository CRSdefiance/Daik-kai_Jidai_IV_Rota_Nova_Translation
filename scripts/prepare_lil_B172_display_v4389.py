"""Prepare paired full B172 content fixtures retaining all38 source commands."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_display_tools_v4389')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B171_display_fixture_v4340.py','scripts/research_lil_B172_display_fixture_v4389.py',{
        'B171':'B172','lil_B171':'lil_B172','display_fixture_v4340':'display_fixture_v4389','display_v4340':'display_v4389',
        'all_routes_combined_v4303':'all_routes_combined_v4353','relocation_v4332':'relocation_v4381','editorial_manuscript_v4':'editorial_manuscript_v3',
        '[171]':'[172]','source_block=171':'source_block=172',
        "len(commands) == 45 and sum(command['word'] == 0xA000 for command in commands) == 0":"len(commands) == 38 and sum(command['word'] == 0xA000 for command in commands) == 1",
        'len(walk) == 54 and len(speeches) == 37':'len(walk) == 47 and len(speeches) == 27',
        "sum(command['word'] == 0 for command in walk) == 2":"sum(command['word'] == 0 for command in walk) == 1",
        "sum(command['word'] == 0xA000 for command in walk) == 4":"sum(command['word'] == 0xA000 for command in walk) == 5",
        'all54_stored_fixture_commands':'all47_stored_fixture_commands',
        'zero_relative_sites_zero_predicates_and_both_declared_ends_preserved':'zero_relative_sites_zero_predicates_and_single_tail_end_preserved',
        'all37_progressive_source_texts_presentations_resource_and_C200_retained_without_flattening':'all27_progressive_source_texts_presentations_resources_C200_then_A000_retained_without_flattening',
        'source_event171_not_selected_or_eligibility_earned':'source_event172_not_selected_or_eligibility_earned',
        'source_B171_4500_4621_61FF_6325_C200_and_both_ends_retained_without_invented_A000_or_pause':'source_B172_five_presentations_three_resources_C200_then_A0006240_and_tail_end_retained',
        'stored_speech_objects=37':'stored_speech_objects=27',
        'actual_linear_path_dream_morning_C200_and_end_reachability_to_be_observed':'actual_linear_path_departure_C200_A000_and_end_reachability_to_be_observed',
        'Paired B171 fixtures:37 progressive speeches,45 source commands plus9 original init commands;presentations,resource,C200 and both ends retained.':'Paired B172 fixtures:27 progressive speeches,38 source commands plus9 original init commands;five presentations,three resources,C200 then A000/6240 and one end retained.',
    })]
    tools.append(derive('scripts/run_lil_B171_display_fixture_v4341.py','scripts/run_lil_B172_display_fixture_v4390.py',{
        'B171':'B172','lil_B171':'lil_B172','display_fixture_v4340':'display_fixture_v4389',
        'display_run_v4341':'display_run_v4390','display_v4341':'display_v4390',
        'source_event171_not_selected':'source_event172_not_selected',"'displayed_original_source_block':171":"'displayed_original_source_block':172",
        'all_source_commands_presentations_resource_and_C200_retained':'all_source_commands_presentations_resources_C200_then_A000_retained',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=172,speeches=27,source_commands=38,stored_fixture_commands=47,
        original_B22_init_commands=9,original_B22_init_A000=4,source_A000=1,source_A000_hex='00a0ffff010cc960',source_C200_before_A000=True,
        source_pause=0,source_declared_end_offsets=[1880],source_presentations=[0x6000,0x45FF,0x4651,0x4620,0x6240],
        source_resources=[0x6329,0x6340,0x632A],C200=1,no_source_command_omission_flattening_or_forced_predicate=True,
        no_natural_eligibility_recruitment_or_earned_flag_claim=True,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared paired complete B172 fixtures and20001-frame ordinary-input cold boots;all38 source commands retained.')
