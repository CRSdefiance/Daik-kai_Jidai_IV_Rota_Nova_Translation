"""Prepare complete unforced B173 content fixtures and focused 9001-frame boots."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_display_tools_v4436')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B172_display_fixture_v4389.py','scripts/research_lil_B173_display_fixture_v4436.py',{
        'B172':'B173','lil_B172':'lil_B173','display_fixture_v4389':'display_fixture_v4436','display_v4389':'display_v4436',
        'all_routes_combined_v4353':'all_routes_combined_v4404','relocation_v4381':'relocation_v4428',
        '[172]':'[173]','source_block=172':'source_block=173',
        "len(commands) == 38 and sum(command['word'] == 0xA000 for command in commands) == 1":"len(commands) == 23 and sum(command['word'] == 0xA000 for command in commands) == 2",
        'len(walk) == 47 and len(speeches) == 27':'len(walk) == 32 and len(speeches) == 11',
        "sum(command['word'] == 0x8000 for command in walk) == 0":"sum(command['word'] == 0x8000 for command in walk) == 1",
        "sum(command['word'] in [0x100, 0x200, 0x300, 0x400] for command in walk) == 0":"sum(command['word'] in [0x100, 0x200, 0x300, 0x400] for command in walk) == 4",
        "sum(command['word'] == 0xA000 for command in walk) == 5":"sum(command['word'] == 0xA000 for command in walk) == 6",
        'all47_stored_fixture_commands':'all32_stored_fixture_commands',
        'zero_relative_sites_zero_predicates_and_single_tail_end_preserved':'four_relative_sites_one_predicate_two_A000s_and_single_tail_end_preserved',
        'all27_progressive_source_texts_presentations_resources_C200_then_A000_retained_without_flattening':'all11_progressive_source_texts_presentations_resources_predicate_relative_suffix_and_two_A000s_retained_without_flattening',
        'source_event172_not_selected_or_eligibility_earned':'source_event173_not_selected_or_eligibility_earned',
        'source_B172_five_presentations_three_resources_C200_then_A0006240_and_tail_end_retained':'source_B173_two_presentations_two_resources_two_A000s_predicate_four_spans_and_tail_end_retained',
        'no_original_membership_queries_or_relative_sites':'one_original_predicate_and_four_relative_sites_retained_without_forcing',
        'stored_speech_objects=27':'stored_speech_objects=11',
        'actual_linear_path_departure_C200_A000_and_end_reachability_to_be_observed':'actual_unforced_suffix_path_effects_and_end_reachability_to_be_observed',
        'Paired B172 fixtures:27 progressive speeches,38 source commands plus9 original init commands;five presentations,three resources,C200 then A000/6240 and one end retained.':'Paired B173 fixtures:11 progressive speeches,23 source structural commands plus9 original init commands;two presentations,two resources,predicate,four relative sites,two A000s and one end retained.',
    })]
    tools.append(derive('scripts/run_lil_B172_display_fixture_v4390.py','scripts/run_lil_B173_display_fixture_v4437.py',{
        'B172':'B173','lil_B172':'lil_B173','display_fixture_v4389':'display_fixture_v4436',
        'display_run_v4390':'display_run_v4437','display_v4390':'display_v4437',
        'source_event172_not_selected':'source_event173_not_selected',"'displayed_original_source_block':172":"'displayed_original_source_block':173",
        'all_source_commands_presentations_resources_C200_then_A000_retained':'all_source_commands_presentations_resources_predicate_four_spans_and_two_A000s_retained',
        "'--frames','20001'":"'--frames','9001'",'range(2350,20001,60)':'range(2350,9001,60)',
        'range(2600,19501,240)':'range(2600,8501,240)',
        "'fixture_manifest':str(FIXTUREPATH)":"'focused_scene_and_normal_return_capture_not_extended_sailing_test':True,'requested_frames':9001,'fixture_manifest':str(FIXTUREPATH)",
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=173,speeches=11,source_structural_commands=23,stored_fixture_commands=32,
        original_B22_init_commands=9,original_B22_init_A000=4,source_A000=2,source_predicate=1,source_relative_sites=4,
        source_pause=0,source_declared_end_offsets=[762],source_presentations=[0x6000,0x6240],source_resources=[0x6329,0x6340],C200=0,
        no_source_command_omission_flattening_or_forced_predicate=True,no_natural_eligibility_recruitment_or_earned_flag_claim=True,
        frames=9001,scope='Complete11-speech exchange,unforced conditional suffix and normal return;do not extend into unrelated later sailing solely to repeat already documented scheduler research. Inspect actual retained paths and all captured frames;investigate concrete unresolved findings if any.',
        new_emulator_runs=0,full_goal_complete=False))
    print('Prepared complete B173 fixtures and9001-frame ordinary-input boots;all23 structural source commands retained,unforced paths to be observed.')
