"""Bind36 viewed panes/nine sheets andretain measured later limits with scoped names."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_actual_view_v7708')
ACTUAL=Path('work/analysis/maria_B207_actual_v7706/Maria_two_complete_scene_captures36_occurrences_exact_body_headers_andnormal_returns.json')
LATER=Path('work/analysis/maria_B207_actual_comparison_v7707/Maria18_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
OLD_NAMES=Path('translations/maria_B207_speaker_name_review_v1.json')
NAMES=Path('translations/maria_B207_speaker_name_review_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NAMES.exists();actual,later,names=map(read,[ACTUAL,LATER,OLD_NAMES]);assert later['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert actual['total_actual_speech_occurrences']==36 and actual['all_jobs_terminal_andreaped'] and len(later['groups'])==1
    measured=later['groups'][0];assert measured['route']==3 and len(measured['later_RGB_differences'])==104 and measured['later_sample_count']==123
    assert measured['all18_whole_upper_scene_portrait_andheader_RGB_equal'] and measured['all_original_initializer_andexchange_results_andUI_words_equal']
    assert measured['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=False)
    assert not measured['whole_actors_equal'] and measured['final_PRNG_seeds']==[1942423083,327589790]
    assert measured['source_English_exits']==[8696,8694] and len(measured['command_comparison_differences'])==19 and len(measured['duration_differences'])==8
    sheets=[s for g in actual['groups'] for s in [*g['review_sheets'],g['transition_sheet']]]
    sheets.append(dict(path=later['review_sheet'],sha256=later['review_sheet_sha256']));assert len(sheets)==9
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    ROOT.mkdir(parents=True);panes=[]
    for g in actual['groups']:
        assert g['actual_unique_speeches']==18 and g['complete_body_holds']==g['complete_name_holds']==74 and not g['incomplete_sampled_holds'] and not g['unidentified_trace_rows']
        assert g['normal_return_sample_frame']==8780
        for i,panel in enumerate(g['speech_observations']):
            h=panel['selected_capture'];assert sha(Path(h['capture']).read_bytes())==h['sha256']
            crop=Image.open(h['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
            sheet=Image.open(g['review_sheets'][i//6]['path']).convert('RGB');x,y=i%3*520+4,(i%6)//3*416+24
            assert sheet.crop((x,y,x+512,y+384)).tobytes()==crop.tobytes()
            out=ROOT/f"route3_{g['version']}_{panel['id']}_panel.png";crop.save(out)
            panes.append(dict(route=3,version=g['version'],file_path=panel['file_path'],id=panel['id'],frame=h['frame'],whole_capture=h['capture'],whole_capture_sha256=h['sha256'],panel=str(out),panel_sha256=sha(out.read_bytes()),byte_equal_whole_frame_andreview_sheet_crop=True))
    successor=deepcopy(names);successor['historical_actual_optional_headers_andfull_catalogue_UI_unvisited']=successor.pop('actual_optional_headers_andfull_catalogue_UI_unvisited')
    english=next(g for g in actual['groups'] if g['version']=='English')
    for r in successor['records']:
        held=[h for p in english['speech_observations'] for h in p['complete_name_holds'] if h['actor_ID']==r['actor_ID']]
        assert held and all(h['text']==r['english'] and h['complete_name_first_internal_final_glyphs_andblank_guards_equal'] for h in held)
        r['historical_formatting_scope']=r['formatting_scope'];r['formatting_scope']='This complete exchange, both exact native getter strings and observed Maria initialized-fixture progressive headers. Full catalogue UI and natural optional activation/location unvisited.'
        r['review']['formatting']=True;r.update(actual_final_English_complete_header_holds=len(held),actual_final_English_fixture_header_observed=True,actual_header_proof=str(ACTUAL),actual_header_proof_sha256=sha(ACTUAL.read_bytes()),full_catalogue_UI_unvisited=True,natural_optional_event_activation_andoriginal_location_unvisited=True)
    successor.update(previous_review=str(OLD_NAMES),previous_review_sha256=sha(OLD_NAMES.read_bytes()),actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),both_contextual_name_formatting_gates_true=True,all_actual_first_internal_final_header_glyphs_andblank_guards_exact=True,actual_fixture_headers_observed_not_full_catalogue_UI_ororiginal_optional_activation=True,no_name_asset_change_ornew_dialogue_credit=True,all_broader207_name_role_alias_andearlier_consumers_open=True)
    save(NAMES,successor)
    save(ROOT/'Maria36_panes9_sheets_viewed_scoped_names_all_late_limits_preserved.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),comparison_proof=str(LATER),comparison_proof_sha256=sha(LATER.read_bytes()),viewed_sheets=sheets,all36_complete_source_English_speech_panes_individually_viewed=True,all_six_speech_sheets_two_transition_sheets_one_unmasked_late_sheet_viewed=True,all36_panes_byte_equal_whole_frame_andreview_sheet_crops=panes,all18_source_English_scene_portrait_complete_header_pairs_equal=True,complete_body_andheader_holds_each_language=74,both_R4_complete18_black18_lightgray_source_English_holds_verified=True,all_original_command_order_native_results_UI_words_andnormal_returns=True,source_English_exits=[8696,8694],actual_return_sample_Hangzhou8780_not_original_optional_location=True,source_final_Sailor_rats_food_safety_English_final_Sailor_dizzy_starving_cannot_go_on_incidental_no_credit=True,later_RGB_differences=104,later_samples=123,five_component_equality=measured['five_native_component_equality'],whole_actor_equality=False,PRNG_seeds=[1942423083,327589790],all19_command_diff_rows_and8_durations_preserved_in_comparison=True,raw_calendars_differ_no_invented_date_interpretation=True,no_full_RAM_every_frame_future_sequence_broad_simulation_orcausal_equivalence_claim=True,all_measured_differences_preserved_for_later_older_record_technical_reaudit=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,disclosed_ROM_initialized_entry_fixtures_not_natural_optional_activation_location_earned_progress_full_effects_route_orhardware=True,speaker_name_review=str(NAMES),speaker_name_review_sha256=sha(NAMES.read_bytes()),registered_release_andintegration_credit_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,LATER,OLD_NAMES,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('36 exact panes/nine sheets viewed;two contextual name retentions have complete actual headers.19 command/8 duration rows,104/123 late RGB differences andall state/calendar/RNG limits retained;zero integration credit.')
