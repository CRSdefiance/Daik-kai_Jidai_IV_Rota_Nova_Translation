"""Prepare complete unforced B174 fixtures and focused16001-frame cold boots."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_display_tools_v4487')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B173_display_fixture_v4436.py','scripts/research_lil_B174_display_fixture_v4487.py',{
        'B173':'B174','lil_B173':'lil_B174','display_fixture_v4436':'display_fixture_v4487','display_v4436':'display_v4487',
        'all_routes_combined_v4404':'all_routes_combined_v4445','relocation_v4428':'relocation_v4477',
        'editorial_manuscript_v3':'editorial_manuscript_v5','[173]':'[174]','source_block=173':'source_block=174',
        'len(commands) == 23':'len(commands) == 45','len(walk) == 32 and len(speeches) == 11':'len(walk) == 54 and len(speeches) == 33',
        'all32_stored_fixture_commands':'all54_stored_fixture_commands','all11_progressive_source_texts':'all33_progressive_source_texts',
        'source_event173_not_selected_or_eligibility_earned':'source_event174_not_selected_or_eligibility_earned',
        'source_B173_two_presentations_two_resources_two_A000s_predicate_four_spans_and_tail_end_retained':
            'source_B174_two_presentations_one_resource_two_A000s_predicate_four_spans_C200_and_tail_end_retained',
        'expected_conditional_speech_IDs=[]':"expected_conditional_speech_IDs=['DK4_MES_B174_R0069']",
        'stored_speech_objects=11':'stored_speech_objects=33',
        "        assert sum(command['word'] == 0 for command in walk) == 1":
            "        assert sum(command['word'] == 0 for command in walk) == 1\n        assert sum(command['word'] == 0xC200 for command in walk) == 1",
        'four_relative_sites_one_predicate_two_A000s_and_single_tail_end_preserved':
            'four_relative_sites_one_predicate_two_A000s_C200_and_single_tail_end_preserved',
        'all11_progressive_source_texts_presentations_resources_predicate_relative_suffix_and_two_A000s_retained_without_flattening':
            'all33_progressive_source_texts_presentations_resource_predicate_optional_Emilio_two_A000s_and_C200_retained_without_flattening',
        'Paired B173 fixtures:11 progressive speeches,23 source structural commands plus9 original init commands;two presentations,two resources,predicate,four relative sites,two A000s and one end retained.':
            'Paired B174 fixtures:33 progressive speeches,45 source commands plus9 original init commands;two presentations,one resource,predicate,four relative sites,two A000s,C200 and one end retained.',
    })]
    tools.append(derive('scripts/run_lil_B173_display_fixture_v4437.py','scripts/run_lil_B174_display_fixture_v4488.py',{
        'B173':'B174','lil_B173':'lil_B174','display_fixture_v4436':'display_fixture_v4487',
        'display_run_v4437':'display_run_v4488','display_v4437':'display_v4488',
        'source_event173_not_selected':'source_event174_not_selected',"'displayed_original_source_block':173":"'displayed_original_source_block':174",
        'all_source_commands_presentations_resources_predicate_four_spans_and_two_A000s_retained':
            'all_source_commands_presentations_resource_predicate_optional_Emilio_four_spans_two_A000s_and_C200_retained',
        "'--frames','9001'":"'--frames','16001'",'range(2350,9001,60)':'range(2350,16001,60)',
        'range(2600,8501,240)':'range(2600,15501,240)',"'requested_frames':9001":"'requested_frames':16001",
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=174,speeches=33,
        source_structural_commands=45,stored_fixture_commands=54,original_B22_init_commands=9,
        original_B22_init_A000=4,source_A000=2,source_predicate=1,source_relative_sites=4,
        optional_speech='DK4_MES_B174_R0069',source_C200=1,source_declared_end_offsets=[2086],
        source_presentations=[0x6000,0x6240],source_resources=[0x6340],frames=16001,
        no_source_command_omission_flattening_or_forced_predicate=True,
        no_natural_eligibility_recruitment_or_earned_flag_claim=True,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared paired B174 fixtures and16001-frame ordinary-input boots, preserving all45 commands and unforced Emilio condition.')
