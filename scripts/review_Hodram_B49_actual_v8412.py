"""Record direct review of the selected B49 path and preserve every measured limitation."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_actual_review_v8412')
ACTUAL=Path('work/analysis/Hodram_B49_actual_v8409/B49/paired_actual_dialogue_headers_flow_returns.json')
COMPARE=Path('work/analysis/Hodram_B49_comparison_v8410/paired_selected_path_comparison.json')
DIFFERENCES=Path('work/analysis/Hodram_B49_difference_view_v8411/sheet.json')

if __name__=='__main__':
    assert not ROOT.exists();actual,comparison,diff=map(read,[ACTUAL,COMPARE,DIFFERENCES]);g=comparison['groups'][0]
    assert not actual['unresolved'] and actual['all_observed_complete_body_name_holds_andnative_flow_pass']
    assert len(actual['groups'])==2 and len(actual['review_sheets'])==2
    sheets=actual['review_sheets']+comparison['review_sheets']+[diff['sheet']]
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    groups=actual['groups'];assert [len(x['speeches']) for x in groups]==[6,6]
    assert [sum(len(s['complete_holds']) for s in x['speeches']) for x in groups]==[33,33]
    assert [x['normal_return']['frame'] for x in groups]==[5213,5216]
    assert [x['normal_return']['native_result'] for x in groups]==[[0,0],[0,0]]
    assert groups[0]['unvisited_conditional_text_IDs']==groups[1]['unvisited_conditional_text_IDs'] and len(groups[0]['unvisited_conditional_text_IDs'])==8
    assert comparison['total_actual_frames']==20002 and len(g['later_RGB_comparisons'])==81 and g['later_RGB_difference_count']==2
    assert all(g['five_native_component_equality'].values()) and g['whole_actors_equal'] and g['final_PRNG_seeds']==[1633251573,1633251573]
    rng=[c for c in g['command_comparison_differences'] if any('RNG' in k for k in c['different_fields'])]
    assert [c['canonical_source_offset'] for c in rng]==[324,416,424,980]
    assert [x['frame'] for x in g['later_RGB_comparisons'] if not x['whole_RGB_equal']]==[5350,6130]
    assert len(g['duration_differences'])==2 and not g['UI_request_differences']
    assert all(x['upper_scene_portrait_RGB_equal'] and x['complete_header_region_RGB_equal'] for x in g['scene_pairs'])
    observed=[s['id'] for s in groups[0]['speeches']]
    assert observed==['DK4_MES_B49_R0006','DK4_MES_B49_R0010','DK4_MES_B49_R0015','DK4_MES_B49_R0019','DK4_MES_B49_R0022','DK4_MES_B49_R0033']
    ROOT.mkdir(parents=True);save(ROOT/'selected_path_review.json',dict(actual=str(ACTUAL),actual_sha256=sha(ACTUAL.read_bytes()),comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),directly_viewed_sheets=sheets,all_four_sheets_directly_viewed=True,actual_frames=20002,actual_selected_source_speech_IDs=observed,actual_complete_source_andEnglish_body_name_holds=66,actual_progressive_actors=[1,2],actual_full_nameplates=['Hodram Bergstrom','Lil Argot'],complete_body_first_internal_final_characters_bounds_singlepages_andnames_pass=True,New_World_directions_three_balanced_rows_directly_viewed=True,source_standalone_ellipsis_andHodram_header_complete=True,actual_original_item148_layout2_show_andhide_directly_viewed=True,original_source_item_card_name_andProof_label_unchanged=True,normal_returns=g['normal_returns'],unvisited_conditional_text_IDs=groups[0]['unvisited_conditional_text_IDs'],typed_B49_menu_mixed_ellipsis_reply_FE_andlayout0_not_observed_by_whole_script_run=True,timing_differences=g['duration_differences'],different_script_boundary_RNG_values=rng,later_RGB_difference_frames=[5350,6130],later_RGB_direct_view_findings=['5350:small Port tooltip edge/highlight difference in town UI.','6130:later original sailing menu first-row highlight differs.'],later_RGB_equal_pairs=79,later_RGB_total_pairs=81,final_PRNG_seeds=g['final_PRNG_seeds'],five_checked_native_components_equal=g['five_native_component_equality'],whole_actor_equal=True,raw_calendar_values_uninterpreted=g['raw_calendars_uninterpreted'],following_original_commands_with_frames_not_identical=True,no_every_frame_causality_future_rng_outcome_broad_simulation_fullroute_hardware_oroptional_event_eligibility_claim=True,focused_B49_menu_backing_controller_normal_dismissal_mixed_ellipsis_FE_transition_andlayout0_risks_still_pending=True,all16_formatting_gates_remain_false_until_remaining_required_checks=True,no_ROM_registration_orcompletion_credit=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,COMPARE,DIFFERENCES,Path(__file__)]}))
    print('Viewed12actual body/namepages/66completeholds plusitem show-hide and2laterRGBdifferences. Normalreturns5213/5216;boundaryRNGdifferences retained despiteequal finalseed. Eight speeches/twochoices remainunvisited;focusedUI/FE tests pending.No credit.')
