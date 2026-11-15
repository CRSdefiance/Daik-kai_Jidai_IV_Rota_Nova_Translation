"""Bind72 viewed panes and17 whole sheets; retain measured late differences and scoped names."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_actual_view_v7652')
ACTUAL=Path('work/analysis/papal_trade_actual_v7650/four_complete_scene_captures72_speech_occurrences_exact_body_headers_andnormal_returns.json')
LATER=Path('work/analysis/papal_trade_actual_comparison_v7651b/36_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGBl_limits.json')
OLD_NAMES=Path('translations/papal_trade_speaker_name_review_v1.json')
NAMES=Path('translations/papal_trade_speaker_name_review_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NAMES.exists();actual,later,names=map(read,[ACTUAL,LATER,OLD_NAMES]);assert later['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert actual['total_actual_speech_occurrences']==72 and actual['all_jobs_terminal_andreaped']
    sheets=[s for g in actual['groups'] for s in [*g['review_sheets'],g['transition_sheet']]]
    sheets.append(dict(path=later['review_sheet'],sha256=later['review_sheet_sha256']));assert len(sheets)==17
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert [len(g['later_RGB_differences']) for g in later['groups']]==[3,53] and [g['later_sample_count'] for g in later['groups']]==[133,133]
    assert all(g['all18_whole_upper_scene_portrait_andheader_RGB_equal'] and g['all_original_initializer_andexchange_results_andUI_words_equal'] for g in later['groups'])
    ROOT.mkdir(parents=True);panes=[]
    for g in actual['groups']:
        for i,panel in enumerate(g['speech_observations']):
            h=panel['selected_capture'];assert sha(Path(h['capture']).read_bytes())==h['sha256']
            crop=Image.open(h['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
            sheet=Image.open(g['review_sheets'][i//6]['path']).convert('RGB');x,y=i%3*520+4,(i%6)//3*416+24
            assert sheet.crop((x,y,x+512,y+384)).tobytes()==crop.tobytes()
            out=ROOT/f"route{g['route']}_{g['version']}_{panel['id']}_panel.png";crop.save(out)
            panes.append(dict(route=g['route'],version=g['version'],file_path=panel['file_path'],id=panel['id'],frame=h['frame'],whole_capture=h['capture'],whole_capture_sha256=h['sha256'],panel=str(out),panel_sha256=sha(out.read_bytes()),byte_equal_whole_frame_crop=True))
    successor=deepcopy(names);successor['historical_all_name_formatting_gates_false']=successor.pop('all_name_formatting_gates_false');successor['historical_actual_optional_headers_andfull_catalogue_UI_unvisited']=successor.pop('actual_optional_headers_andfull_catalogue_UI_unvisited')
    for r in successor['records']:
        g=next(g for g in actual['groups'] if g['route']==r['route'] and g['version']=='English')
        held=[h for p in g['speech_observations'] for h in p['complete_name_holds'] if h['actor_ID']==r['actor_ID']]
        assert held and all(h['text']==r['english'] and h['complete_name_first_internal_final_glyphs_andblank_guards_equal'] for h in held)
        r['historical_approval_scope']=r['approval_scope'];r['approval_scope']='This complete exchange, both exact native getter strings and observed original-route initialized-fixture progressive headers only. Full catalogue UI and natural optional activation unvisited.'
        r['review']['formatting']=True;r.update(actual_final_English_complete_header_holds=len(held),actual_final_English_fixture_header_observed=True,actual_header_proof=str(ACTUAL),actual_header_proof_sha256=sha(ACTUAL.read_bytes()),full_catalogue_UI_unvisited=True,natural_optional_event_activation_andoriginal_location_unvisited=True)
    successor.update(previous_review=str(OLD_NAMES),previous_review_sha256=sha(OLD_NAMES.read_bytes()),actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),all_four_contextual_name_formatting_gates_true=True,all_actual_first_internal_final_header_glyphs_andblank_guards_exact=True,actual_fixture_headers_observed_not_full_catalogue_UI_ororiginal_optional_activation=True,no_name_asset_change_ornew_dialogue_credit=True,all_broader207_name_role_alias_andearlier_consumers_open=True)
    save(NAMES,successor)
    save(ROOT/'all72_panes17_sheets_viewed_scoped_names_all_late_limits_preserved.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),comparison_proof=str(LATER),comparison_proof_sha256=sha(LATER.read_bytes()),viewed_sheets=sheets,all72_complete_source_English_speech_panes_individually_viewed=True,all12_six_speech_sheets_four_transition_sheets_one_unmasked_late_sheet_viewed=True,all72_panes_byte_equal_saved_whole_frame_crops=panes,all36_source_English_scene_portrait_complete_header_pairs_equal=True,source_English_body_header_complete_holds_by_route=[dict(route=r,source=next(g['complete_body_holds'] for g in actual['groups'] if g['route']==r and g['version']=='clean_Japanese'),English=next(g['complete_body_holds'] for g in actual['groups'] if g['route']==r and g['version']=='English')) for r in [0,1]],all_four_R5_complete18_black18_lightgray_source_English_holds_verified=True,all_fixtures_original_command_order_native_results_UI_words_andnormal_returns=True,source_English_exits_by_route=[g['source_English_exits'] for g in later['groups']],actual_return_samples_Lisbon_orStockholm8170_not_original_optional_location=True,Rafael_final_frame_Sea_View_Hodram_final_frame_Sailor_Water_has_run_out=True,incidental_Julio_sailing_tutorial_resource_messages_no_editorial_credit=True,later_RGB_differences_by_route=[3,53],later_samples_each_route=133,five_component_equality_by_route=[g['five_native_component_equality'] for g in later['groups']],whole_actor_equality_by_route=[g['whole_actors_equal'] for g in later['groups']],PRNG_seeds_by_route=[g['final_PRNG_seeds'] for g in later['groups']],all19_command_diff_rows_andseven_durations_each_route_preserved_in_comparison=True,no_full_RAM_every_frame_future_sequence_broad_simulation_orcausal_equivalence_claim=True,failed_7651_final_frame_assertion_preserved_source_locked7651b_includes16000_and16001_no_new_capture=True,all_measured_differences_preserved_for_later_older_record_technical_reaudit=True,disclosed_ROM_initialized_entry_fixtures_not_natural_optional_activation_location_earned_progress_full_effects_route_orhardware=True,speaker_name_review=str(NAMES),speaker_name_review_sha256=sha(NAMES.read_bytes()),registered_release_andintegration_credit_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,LATER,OLD_NAMES,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('72 exact panes and17 actual/comparison sheets viewed;four contextual name retentions have complete observed fixture headers. Late3/133 Rafael and53/133 Hodram RGB differences andall state/RNG limits retained. Registered integration still pending;zero credit.')
