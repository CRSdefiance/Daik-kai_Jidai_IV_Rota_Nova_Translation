"""Bind 37 newly viewed panes/11 sheets and93 exact prior panes to final-v3 prose."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_final_view_v7768')
ACTUAL=Path('work/analysis/maria_story_final_actual_binding_v7766/six_final_v3_actual_groups_two_fresh_four_exact_reused.json')
FRESH=Path('work/analysis/maria_story_final_actual_v7765/two_final_English_captures_actual_pages_headers_branches_returns.json')
OLD_VIEW=Path('work/analysis/maria_story_actual_view_v7755/131_actual_panes33_sheets_viewed_named_limits_two_final_prose_refinements.json')
OLD_LATER=Path('work/analysis/maria_story_actual_comparison_v7754/three_actual_pairs_measured_portraits_timing_RNG_states_RGB_limits.json')
NEW_LATER=Path('work/analysis/maria_story_final_comparison_v7767/two_final_pairs_measured_portraits_timing_RNG_states_RGB_limits.json')
LATER=ROOT/'three_final_pairs_two_fresh_one_exact_reused.json'
OLD_NAMES=Path('translations/maria_B34_B108_B35_speaker_name_review_v2.json')
NAMES=Path('translations/maria_B34_B108_B35_speaker_name_review_v3.json')
NATIVE=Path('work/analysis/maria_story_final_native_v7757b/67_final_v3_native_pages_andfully_bound_logical_lineage.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NAMES.exists()
    actual,fresh,oldview,oldlater,newlater,names,native=map(read,[ACTUAL,FRESH,OLD_VIEW,OLD_LATER,NEW_LATER,OLD_NAMES,NATIVE])
    assert not actual['unresolved'] and actual['total_actual_speech_occurrences']==actual['complete_actual_page_panels']==130
    assert newlater['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert oldview['all33_actual_transition_andlate_comparison_sheets_individually_viewed']
    oldB35=next(g for g in oldlater['groups'] if g['block']==35)
    oldactual=read(oldlater['actual_proof'])
    assert oldlater['actual_proof_sha256']==sha(Path(oldlater['actual_proof']).read_bytes())
    for version in ['clean_Japanese','English']:
        assert next(g for g in actual['groups'] if (g['block'],g['version'])==(35,version))==next(g for g in oldactual['groups'] if (g['block'],g['version'])==(35,version))
    groups=[*deepcopy(newlater['groups']),deepcopy(oldB35)]
    assert sum(len(g['scene_portrait_header_pairs']) for g in groups)==65
    assert all(not g['actual_initializer_andexchange_result_differences'] and not g['actual_UI_request_differences'] for g in groups)
    assert all(p['whole_upper_scene_portrait_header_RGB_equal'] for g in groups for p in g['scene_portrait_header_pairs'])
    sheets=[s for g in fresh['groups'] for s in [*g['review_sheets'],g['transition_sheet']]]+newlater['review_sheets']
    assert len(sheets)==11
    for sheet in sheets:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    for preview in native['review_previews']:assert sha(Path(preview['path']).read_bytes())==preview['sha256']
    ROOT.mkdir(parents=True);panes=[]
    for group in fresh['groups']:
        ordinal=0
        for speech in group['speech_observations']:
            for page in speech['pages']:
                hold=page['complete_body_andname_holds'][-1];assert sha(Path(hold['capture']).read_bytes())==hold['sha256']
                crop=Image.open(hold['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
                sheet=Image.open(group['review_sheets'][ordinal//6]['path']).convert('RGB');x,y=ordinal%3*520+4,(ordinal%6)//3*416+24
                assert sheet.crop((x,y,x+512,y+384)).tobytes()==crop.tobytes()
                path=ROOT/f'B{group["block"]}_{speech["id"]}_page{page["native_page"]}.png';crop.save(path)
                panes.append(dict(block=group['block'],version=group['version'],file_path=speech['file_path'],id=speech['id'],native_page=page['native_page'],
                    frame=hold['frame'],whole_capture=hold['capture'],whole_capture_sha256=hold['sha256'],panel=str(path),panel_sha256=sha(path.read_bytes()),
                    byte_equal_whole_frame_andreview_sheet_crop=True,final_v3_new_actual_view=True));ordinal+=1
        assert ordinal==group['actual_complete_page_panels']
    assert len(panes)==37
    reused=[deepcopy(p) for p in oldview['all131_actual_panes_exact_whole_frame_crops'] if (p['block'],p['version']) not in [(34,'English'),(108,'English')]]
    assert len(reused)==93
    for pane in reused:
        assert sha(Path(pane['whole_capture']).read_bytes())==pane['whole_capture_sha256']
        assert sha(Path(pane['panel']).read_bytes())==pane['panel_sha256']
    later=deepcopy(newlater);later.update(groups=groups,review_sheets=newlater['review_sheets']+[next(s for s in oldlater['review_sheets'] if 'B35_' in s['path'])],
        B35_exact_prior_measurements_reused=True,B35_prior_proof=str(OLD_LATER),B35_prior_proof_sha256=sha(OLD_LATER.read_bytes()),review_sheets_visual_pending=False)
    save(LATER,later)
    successor=deepcopy(names)
    for row in successor['records']:
        row['previous_v2_actual_header_observations_preserved_in']=str(OLD_NAMES)
        observations=[dict(block=g['block'],version=g['version'],id=s['id'],page=p['native_page'],hold=h)
            for g in actual['groups'] for s in g['speech_observations'] if s['source_selector']==row['actor_ID']
            for p in s['pages'] for h in p['complete_body_andname_holds']]
        row.update(actual_source_English_complete_header_observations=observations,actual_initialized_fixture_header_seen=bool(observations))
        if row['actor_ID']==26:assert not observations
    successor.update(previous_name_review=str(OLD_NAMES),previous_name_review_sha256=sha(OLD_NAMES.read_bytes()),
        actual_source_English_pixel_proof=str(ACTUAL),actual_source_English_pixel_proof_sha256=sha(ACTUAL.read_bytes()),
        final_v3_two_English_scenes_observed=True,shared155_label_semantic_review_still_unresolved_no_asset_edit=True)
    save(NAMES,successor)
    holds=sum(g['complete_body_andheader_holds'] for g in actual['groups']);assert holds==528
    save(ROOT/'130_final_actual_panes11_new_sheets93_prior_panes_exact.json',dict(
        actual=str(ACTUAL),actual_sha256=sha(ACTUAL.read_bytes()),measured_later_limits=str(LATER),measured_later_limits_sha256=sha(LATER.read_bytes()),
        all11_new_actual_transition_late_sheets_individually_viewed=True,all37_new_actual_panes_exact_whole_frame_crops=panes,
        all93_unchanged_prior_actual_panes_exact=reused,all130_final_actual_panes_viewed_with_exact_reuse=True,
        two_final_native_previews_viewed=native['review_previews'],complete_body_andheader_holds=holds,
        all65_final_paired_upper_scene_portrait_header_RGB_regions_equal=True,all_actual_initializer_exchange_results_andUI_request_words_equal=True,
        final_late_limits=[dict(block=g['block'],exits=g['source_English_exits'],command_differences=len(g['command_comparison_differences']),
            duration_differences=len(g['duration_differences']),late_RGB_differences=len(g['later_RGB_differences']),late_samples=g['later_sample_count'],
            component_equality=g['five_native_component_equality'],actors_equal=g['whole_actors_equal'],final_seeds=g['final_PRNG_seeds']) for g in groups],
        full_timing_RNG_actor_component_calendar_andlate_RGB_measurements_preserved=True,
        no_everyframe_fullRAM_future_sequence_broad_simulation_orcausal_claim=True,
        source_R65_rightcell_andnormal_type0_valuecarry_findings_preserved=True,
        names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),seven_actual_distinct_headers_Julian26_offline_only=True,
        shared155_Sailor_Retainer_review_open_no_global_name_asset_change=True,
        two_unplayed_Julian_B108_R20_R125_offline_only=True,all67_formatting_gates_false_policy_production_release_pending=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        initialized_fixture_not_natural_optional_activation_original_location_earned_progress_full_effects_routes_orhardware=True,
        incidental_later_prose_no_credit=True,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,FRESH,OLD_VIEW,OLD_LATER,NEW_LATER,LATER,OLD_NAMES,NAMES,NATIVE,Path(__file__)]},
        new_credit=0,new_emulator_runs=2,full_goal_complete=False))
    print('Final-v3 visual review130panes:37fresh/93exact reuse;11new sheets;528complete body+header holds;65upperRGBpairs equal.Shared155 label remains open.')
