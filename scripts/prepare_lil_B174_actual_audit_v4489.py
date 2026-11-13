"""Prepare actual B174 audit with conditional speech and complete effect/C200 order."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_actual_tools_v4489')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/audit_lil_B173_actual_v4438b.py','scripts/audit_lil_B174_actual_v4489.py',{
        'lil_B173_actual_v4438b':'lil_B174_actual_v4489',
        'lil_B173_display_fixture_v4436':'lil_B174_display_fixture_v4487',
        'lil_B173_native_approval_v4425/all11':'lil_B174_native_approval_v4474/all33',
        'lil_B173_display_run_v4437':'lil_B174_display_run_v4488','lil_B173_display_v4437':'lil_B174_display_v4488',
        'lil_B173_controls_v4417/two_resources_one_predicate_four_spans_two_A000s_and_single_end':
            'lil_B174_controls_v4459/one_resource_conditional_Emilio_four_spans_two_A000s_C200_and_single_end',
        'lil_B173_branches_v4414':'lil_B174_branches_v4456',
        "report['frames'] == 9001":"report['frames'] == 16001",
        "rp['source_event173_not_selected']":"rp['source_event174_not_selected']",
        "rp['all_source_commands_presentations_resources_predicate_four_spans_and_two_A000s_retained']":
            "rp['all_source_commands_presentations_resource_predicate_optional_Emilio_four_spans_two_A000s_and_C200_retained']",
        "source['block'] != 173":"source['block'] != 174",'original_source_block=173':'original_source_block=174',
        "len(intervals)==len({row['id'] for row in intervals})==11":"32<=len(intervals)==len({row['id'] for row in intervals})<=33",
        '[0x2100,0x4100,0x2000,0xC200]':'[0x2100,0x4100,0x2000]',
        "predicates[0]['original_source_offset']==728":"predicates[0]['original_source_offset']==874",
        "        source_objects={r['source_offset']:r for r in fixture['selected_original_objects']}":
            """        assert [by_at[r['offset']]['source_record_index'] for r in intervals]==source_path['spoken_source_record_indices']
        source_objects={r['source_offset']:r for r in fixture['selected_original_objects']}""",
        "selected[-1]['original_source_offset']==762":"selected[-1]['original_source_offset']==2086",
        "r.get('original_source_block')==173":"r.get('original_source_block')==174",
        "effect['result_words']==[3,0 if effect['original_source_offset']==720 else result]":"effect['result_words']==[3,result]",
        "[r['word'] for r in resources]==[0x6329,0x6340]":"[r['word'] for r in resources]==[0x6340]",
        "[r['original_source_offset'] for r in presentations]==[8,760]":"[r['original_source_offset'] for r in presentations]==[8,2066]",
        "'DK4_MES_B173_R0044'":"'DK4_MES_B174_R0135'",
        "        assert final_speech['returned']<=effects[0]['start']<=effects[0]['returned']<=predicate['start']<=predicate['returned']\n        assert predicate['returned']<=presentations[1]['start']<=presentations[1]['returned']<=selected[-1]['start']":
            """        ui=[r for r in selected if r['word']==0xC200]
        assert len(ui)==1 and ui[0]['original_source_offset']==2084 and ui[0]['result_words']==[3,result]
        assert len(effects)==2 and [r['original_source_offset'] for r in effects]==[2068,2076]
        assert predicate['returned']<=final_speech['start']<=final_speech['returned']<=presentations[1]['start']
        assert presentations[1]['returned']<=effects[0]['start']<=effects[0]['returned']<=effects[1]['start']<=effects[1]['returned']<=ui[0]['start']<=ui[0]['returned']<=selected[-1]['start']""",
        "fixture['all32_stored_fixture_commands'])==32":"fixture['all54_stored_fixture_commands'])==54",
        'case=case,source_block=173':'case=case,source_block=174','frames=9001':'frames=16001',
        'actual_source_relative_commands=relative':'actual_source_relative_commands=relative,actual_source_C200=ui',
        'final_effect_predicate_and_return_interval=[final_speech,effects[0],predicate,presentations[1],selected[-1]]':
            'predicate_final_speech_presentation_effects_C200_return_interval=[predicate,final_speech,presentations[1],*effects,ui[0],selected[-1]]',
        'single_source_end_offset=762':'single_source_end_offset=2086',
        'exact_observed_boolean_path_and_all11_speeches_match_original_source_commands':'exact_observed_boolean_path_and_all_actually_selected_speeches_match_original_source_commands',
        'len(actual) + len(offline) == 11':'len(actual) + len(offline) == 33',
        'all23_structural_source_commands':'all45_structural_source_commands',
        'all11_progressive_speeches_observed':'all32_unconditional_speeches_observed_and_optional_Emilio_coverage_explicit',
        'failed_initial_zero_descriptor_assumption_preserved=True':'actual_last_result_model_reused_from_source_bound_VM_contract=True',
        'single_source_end762_actually_reached':'single_source_end2086_actually_reached',
        'all11_unforced_predicate_paths_effects_and_end':'all33_unforced_predicate_paths_effects_C200_and_end',
        'frames_per_boot=9001':'frames_per_boot=16001','B173':'B174',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,source_block=174,source_speeches=33,
        unconditional_speeches=32,conditional_source_ID='DK4_MES_B174_R0069',
        stored_fixture_commands=54,source_structural_commands=45,source_predicate_offset=874,
        source_tail=[2066,2068,2076,2084,2086],actual_result_words_are_VM_descriptor_type_and_persistent_last_result=True,
        no_assumed_predicate_branch_or_actual_panels_before_terminal_audit=True,new_credit=0,full_goal_complete=False))
    print('Prepared actual B174 audit: source32+optional Emilio, unforced predicate, two effects/C200 and single end; no results assumed.')
