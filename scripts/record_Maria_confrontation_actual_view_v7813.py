"""Record32 complete source/English panes,nine viewed sheets andall measured later limits."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_actual_view_v7813')
ACTUAL=Path('work/analysis/maria_confrontation_actual_v7811/two_scene_captures_actual_pages_headers_branches_returns.json')
LATER=Path('work/analysis/maria_confrontation_actual_comparison_v7812/one_actual_pair_measured_portraits_timing_RNG_states_RGB_limits.json')
OLD_NAMES=Path('translations/maria_B36_speaker_name_review_v1.json')
NAMES=Path('translations/maria_B36_speaker_name_review_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NAMES.exists();actual,later,names=map(read,[ACTUAL,LATER,OLD_NAMES])
    assert not actual['unresolved'] and actual['total_actual_speech_occurrences']==actual['complete_actual_page_panels']==32
    assert later['actual_proof_sha256']==sha(ACTUAL.read_bytes()) and len(later['groups'])==1
    g=later['groups'][0]
    assert g['block']==36 and len(g['scene_portrait_header_pairs'])==16
    assert not g['actual_initializer_andexchange_result_differences'] and not g['actual_UI_request_differences']
    assert all(p['whole_upper_scene_portrait_header_RGB_equal'] for p in g['scene_portrait_header_pairs'])
    assert g['source_English_exits']==[8213,8216] and len(g['command_comparison_differences'])==18 and len(g['duration_differences'])==6
    assert len(g['later_RGB_differences'])==108 and g['later_sample_count']==131
    assert g['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True)
    assert not g['whole_actors_equal'] and g['final_PRNG_seeds']==[164302531,4157282706]
    assert actual['source_andEnglish_black_andperglyph_ASCII_CP932_gray_masks_required']
    sheets=[s for group in actual['groups'] for s in [*group['review_sheets'],group['transition_sheet']]]+later['review_sheets']
    assert len(sheets)==9
    for sheet in sheets:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True);panes=[]
    for group in actual['groups']:
        assert group['actual_unique_speeches']==group['actual_complete_page_panels']==16
        assert group['complete_body_andheader_holds']==66 and not group['incomplete_sampled_holds'] and not group['unidentified_trace_rows'] and not group['unplayed_conditional_speech_IDs']
        ordinal=0
        for speech in group['speech_observations']:
            for page in speech['pages']:
                hold=page['complete_body_andname_holds'][-1];assert sha(Path(hold['capture']).read_bytes())==hold['sha256']
                crop=Image.open(hold['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
                sheet=Image.open(group['review_sheets'][ordinal//6]['path']).convert('RGB');x,y=ordinal%3*520+4,(ordinal%6)//3*416+24
                assert sheet.crop((x,y,x+512,y+384)).tobytes()==crop.tobytes()
                path=ROOT/f'{group["version"]}_{speech["id"]}_page{page["native_page"]}.png';crop.save(path)
                panes.append(dict(file_path=speech['file_path'],block=36,version=group['version'],id=speech['id'],native_page=page['native_page'],
                    frame=hold['frame'],whole_capture=hold['capture'],whole_capture_sha256=hold['sha256'],panel=str(path),panel_sha256=sha(path.read_bytes()),
                    byte_equal_whole_frame_andreview_sheet_crop=True));ordinal+=1
        assert ordinal==16
    assert len(panes)==32
    updated=deepcopy(names)
    for row in updated['records']:
        observations=[dict(block=36,version=group['version'],id=s['id'],page=p['native_page'],hold=h)
            for group in actual['groups'] for s in group['speech_observations'] if s['source_selector']==row['actor_ID']
            for p in s['pages'] for h in p['complete_body_andname_holds']]
        assert observations
        row.update(actual_source_English_complete_header_observations=observations,actual_initialized_fixture_header_seen=True,
            full_catalogue_UI_unvisited=True,actual_scene_headers_andfull_catalogue_UI_pending=False)
    updated.update(previous_name_review=str(OLD_NAMES),previous_name_review_sha256=sha(OLD_NAMES.read_bytes()),
        actual_source_English_proof=str(ACTUAL),actual_source_English_proof_sha256=sha(ACTUAL.read_bytes()),
        all_three_selected_progressive_headers_actually_observed=True,full_catalogue_UI_unvisited=True,
        no_name_asset_edit_orfull207_shared_role_semantic_approval=True)
    save(NAMES,updated)
    save(ROOT/'32_actual_panes9_sheets_viewed_names_andall_late_limits.json',dict(
        actual=str(ACTUAL),actual_sha256=sha(ACTUAL.read_bytes()),measured_later_limits=str(LATER),measured_later_limits_sha256=sha(LATER.read_bytes()),
        all32_actual_panes_exact_whole_frame_crops=panes,all9_actual_transition_late_sheets_individually_viewed=True,
        actual_speeches_each_language=16,total_actual_complete_pages=32,complete_body_andheader_holds=132,
        source_andEnglish_complete_black_ASCII_gray_CP932_gray_andname_masks_required=True,
        no_partial_unknown_orunplayed_speech_records=True,all16_upper_scene_portrait_header_RGB_pairs_equal=True,
        all_initializer_exchange_results_andUI_request_words_equal=True,
        source_English_exits=[8213,8216],command_difference_rows=18,duration_difference_rows=6,
        later_RGB_differences=108,later_samples=131,five_component_equality=g['five_native_component_equality'],
        whole_actor_equality=False,final_PRNG_seeds=g['final_PRNG_seeds'],
        all_raw_timing_RNG_actor_component_calendar_following_commands_andlate_RGB_preserved=True,
        no_everyframe_fullRAM_future_sequence_broad_simulation_orcausal_equivalence_claim=True,
        initialized_Hangzhou_return_frame8300_not_original_optional_scene_location_oractivation=True,
        no_inferred_Camille_attendance_from_inherited_initialization_graphics=True,
        names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),all207_name_role_alias_and151_159_review_remain_open=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        all16_formatting_gates_false_policy_reference_seal_atomic_production_andregistered_release_pending=True,
        incidental_Maria_levelup_navigation_andlater_sailing_messages_no_editorial_credit=True,
        all_prior_ROMs_manuscripts_failed_producers_andproofs_preserved=True,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,LATER,OLD_NAMES,NAMES,Path(__file__)]},
        new_credit=0,new_emulator_runs=2,new_actual_frames=32002,full_goal_complete=False))
    print('32actual panes/9viewed sheets;132complete body+header holds;all16upperRGB pairs/results/UI match.18command/6duration rows,108/131lateRGBdifferences preserved.No credit yet.')
