"""Record direct review of every B50 page, item transition and later nonidentical RGB pair."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_actual_review_v8510b')
ACTUAL=Path('work/analysis/Hodram_B50_actual_v8507/B50/paired_actual_dialogue_headers_flow_returns.json')
COMPARE=Path('work/analysis/Hodram_B50_comparison_v8509/paired_selected_path_comparison.json')
DIFFERENCES=Path('work/analysis/Hodram_B50_difference_view_v8510/sheet.json')
FE=Path('work/analysis/Hodram_B50_FE_binding_v8508/two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json')
if __name__=='__main__':
    assert not ROOT.exists();actual,comparison,diff,fe=map(read,[ACTUAL,COMPARE,DIFFERENCES,FE]);g=comparison['groups'][0]
    assert not actual['unresolved'] and actual['all_observed_complete_body_name_holds_andnative_flow_pass']
    assert len(actual['groups'])==2 and len(actual['review_sheets'])==1
    sheets=actual['review_sheets']+comparison['review_sheets']+[diff['sheet']]
    assert len(sheets)==3
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    groups=actual['groups'];assert [len(x['speeches']) for x in groups]==[3,3]
    assert [sum(len(s['complete_holds']) for s in x['speeches']) for x in groups]==[25,25]
    assert [x['normal_return']['frame'] for x in groups]==[4739,4737]
    assert [x['normal_return']['native_result'] for x in groups]==[[0,0],[0,0]]
    assert all(not x['unvisited_conditional_text_IDs'] and len(x['command_pairs'])==20 for x in groups)
    assert comparison['total_actual_frames']==20002 and len(g['later_RGB_comparisons'])==89 and g['later_RGB_difference_count']==4
    assert all(g['five_native_component_equality'].values()) and g['whole_actors_equal']
    assert g['final_PRNG_seeds']==list(map(int,['3867090476','3028864251']))
    rng=[c for c in g['command_comparison_differences'] if any('RNG' in k for k in c['different_fields'])];assert not rng
    assert [x['frame'] for x in g['later_RGB_comparisons'] if not x['whole_RGB_equal']]==[5110,5650,5830,7270]
    assert len(g['duration_differences'])==2 and not g['UI_request_differences']
    assert all(x['upper_scene_portrait_RGB_equal'] and x['complete_header_region_RGB_equal'] for x in g['scene_pairs'])
    assert fe['all_actual_FE_typed_descriptors_palette_complete_bitmap_andphysical_RGB_match_independent_model']
    assert [len(x['complete_actual_holds']) for x in fe['groups']]==[3,3]
    observed=[s['id'] for s in groups[0]['speeches']];assert observed==['DK4_MES_B50_R0007','DK4_MES_B50_R0010','DK4_MES_B50_R0013']
    ROOT.mkdir(parents=True);save(ROOT/'whole_exchange_review.json',dict(actual=str(ACTUAL),actual_sha256=sha(ACTUAL.read_bytes()),comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),directly_viewed_sheets=sheets,all_three_sheets_directly_viewed=True,
        actual_frames=20002,actual_emulator_runs=2,actual_source_speech_IDs=observed,actual_complete_source_andEnglish_body_name_orabsent_FE_header_holds=50,
        all_three_source_andEnglish_singlepages_andcomplete_name_orabsent_FE_header_viewed=True,actual_progressive_actors=[2],actual_full_nameplates=['Lil Argot'],
        complete_body_first_internal_final_characters_bounds_singlepages_andnames_pass=True,
        FE_before6302_original_order_andabsent_header_portrait_preserved_inboth_languages=True,
        actual_original_item148_layout0_show_andhide_directly_viewed=True,original_source_item_card_name_andProof_label_unchanged=True,
        normal_returns=g['normal_returns'],unvisited_conditional_text_IDs=[],timing_differences=g['duration_differences'],different_script_boundary_RNG_values=rng,
        later_RGB_direct_view_findings=['5110:original A-button prompt visibility differs.','5650:later original All right. menu first-row highlight differs.','5830:original A-button prompt visibility differs.','7270:later original Depart menu first-row highlight differs.'],
        later_RGB_equal_pairs=85,later_RGB_total_pairs=89,final_PRNG_seeds=g['final_PRNG_seeds'],five_checked_native_components_equal=g['five_native_component_equality'],whole_actor_equal=True,
        raw_calendar_values_uninterpreted=g['raw_calendars_uninterpreted'],following_original_commands_with_frames_not_identical=not g['following_commands_equal'],
        no_every_frame_causality_future_rng_outcome_broad_simulation_fullroute_hardware_natural_event_location_orinventory_eligibility_claim=True,
        no_ROM_registration_orcompletion_credit=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,COMPARE,DIFFERENCES,FE,Path(__file__)]}))
    print('Viewed all six B50 pages/50 complete holds,original FE header/portrait,layout0 item show-hide andall four later RGB differences;limits retained,zero credit.')
