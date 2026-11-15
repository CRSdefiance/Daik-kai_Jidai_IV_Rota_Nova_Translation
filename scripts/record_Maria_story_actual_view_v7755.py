"""Record all33 viewed sheets/131 actual panes, exact crops andall measured later limits."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_actual_view_v7755')
ACTUAL=Path('work/analysis/maria_story_actual_v7752c/six_scene_captures_actual_pages_headers_branches_returns_andunplayed_conditions.json')
LATER=Path('work/analysis/maria_story_actual_comparison_v7754/three_actual_pairs_measured_portraits_timing_RNG_states_RGB_limits.json')
OLD_NAMES=Path('translations/maria_B34_B108_B35_speaker_name_review_v1.json')
NAMES=Path('translations/maria_B34_B108_B35_speaker_name_review_v2.json')
RIGHTCELL=Path('work/analysis/maria_B35_source_rightcell_v7753/source_question_mark_actual_position_binding.json')
TRIAGE=Path('work/analysis/retainer_name_triage_v7744/nine_roles18_getters147_source_blocks484_uses_nine_context_samples.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NAMES.exists();actual,later,names=map(read,[ACTUAL,LATER,OLD_NAMES])
    assert not actual['unresolved'] and later['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert actual['total_actual_speech_occurrences']==130 and actual['complete_actual_page_panels']==131
    assert all(not g['actual_initializer_andexchange_result_differences'] and not g['actual_UI_request_differences'] for g in later['groups'])
    assert all(p['whole_upper_scene_portrait_header_RGB_equal'] for g in later['groups'] for p in g['scene_portrait_header_pairs'])
    assert sum(len(g['scene_portrait_header_pairs']) for g in later['groups'])==65
    assert [(g['block'],len(g['later_RGB_differences']),g['later_sample_count']) for g in later['groups']]==[(34,0,163),(108,75,75),(35,60,79)]
    sheets=[s for g in actual['groups'] for s in [*g['review_sheets'],g['transition_sheet']]]+later['review_sheets'];assert len(sheets)==33
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    ROOT.mkdir(parents=True);panes=[]
    for group in actual['groups']:
        assert not group['incomplete_sampled_holds'] and not group['unidentified_trace_rows']
        ordinal=0
        for speech in group['speech_observations']:
            for page in speech['pages']:
                assert page['complete_body_andname_holds'];h=page['complete_body_andname_holds'][-1]
                assert sha(Path(h['capture']).read_bytes())==h['sha256']
                crop=Image.open(h['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
                sheet=Image.open(group['review_sheets'][ordinal//6]['path']).convert('RGB');x,y=ordinal%3*520+4,(ordinal%6)//3*416+24
                assert sheet.crop((x,y,x+512,y+384)).tobytes()==crop.tobytes()
                path=ROOT/f'B{group["block"]}_{group["version"]}_{speech["id"]}_page{page["native_page"]}_panel.png';crop.save(path)
                panes.append(dict(block=group['block'],version=group['version'],file_path=speech['file_path'],id=speech['id'],native_page=page['native_page'],
                    frame=h['frame'],whole_capture=h['capture'],whole_capture_sha256=h['sha256'],panel=str(path),panel_sha256=sha(path.read_bytes()),
                    byte_equal_whole_frame_andreview_sheet_crop=True))
                ordinal+=1
        assert ordinal==group['actual_complete_page_panels']
    assert len(panes)==131
    successor=deepcopy(names)
    for row in successor['records']:
        observations=[dict(block=g['block'],version=g['version'],id=s['id'],page=p['native_page'],hold=h)
            for g in actual['groups'] for s in g['speech_observations'] if s['source_selector']==row['actor_ID']
            for p in s['pages'] for h in p['complete_body_andname_holds']]
        row.update(actual_source_English_complete_header_observations=observations,
            actual_initialized_fixture_header_seen=bool(observations),full_catalogue_UI_unvisited=True,
            actual_header_pixels_not_approval_of_shared_role_word_choice=True)
        if row['actor_ID']==26:assert not observations;row['unplayed_Julian_conditions_offline_only']=True
        if row['actor_ID']==155:row.update(broader_role_census_andtriage=str(TRIAGE),broader_role_census_andtriage_sha256=sha(TRIAGE.read_bytes()),
            shared_Sailor_Retainer_word_choice_still_unresolved=True,no_global_replacement_selected=True)
    successor.update(previous_name_review=str(OLD_NAMES),previous_name_review_sha256=sha(OLD_NAMES.read_bytes()),
        actual_source_English_pixel_proof=str(ACTUAL),actual_source_English_pixel_proof_sha256=sha(ACTUAL.read_bytes()),
        seven_actual_distinct_speaker_headers_seen_Julian26_offline_only=True,
        actual_pixels_not_full207_semantic_name_approval=True,all207_name_role_alias_review_active=True)
    save(NAMES,successor)
    findings=[
        dict(id='DK4_MES_B108_R0111',status='faithful-v2-two-page-render-works-but-refine-natural-reading-before-final-approval',
            reason="The complete v2 paragraph and both actual pages are verified. Its last short page continues after said she'd. A more direct reported-speech clause can preserve the young female leader, strong justice, hearsay, anger and categorical refusal while avoiding an unnecessary extra page. Preserve all successful two-page evidence."),
        dict(id='DK4_MES_B34_R0042',status='refine-possessive-precision-before-final-approval',
            reason="Clean 祖国 refers to Maria's homeland. My homeland leaves the companions' national origins unspecified. The v2 our homeland is not needed to convey the protective resolve; preserve its tentative assessment and collective intended action."),
    ]
    save(ROOT/'131_actual_panes33_sheets_viewed_named_limits_two_final_prose_refinements.json',dict(
        actual=str(ACTUAL),actual_sha256=sha(ACTUAL.read_bytes()),measured_later_limits=str(LATER),measured_later_limits_sha256=sha(LATER.read_bytes()),
        all33_actual_transition_andlate_comparison_sheets_individually_viewed=True,all131_actual_panes_exact_whole_frame_crops=panes,
        source_andEnglish_actual_speeches_per_language=65,unplayed_Julian_B108_R20_R125_offline_only=True,
        complete_body_andheader_holds=532,no_partial_orunknown_sampled_holds=True,all65_paired_upper_scene_portrait_header_RGB_regions_equal=True,
        all_actual_initializer_exchange_results_andUI_request_words_equal=True,
        full_timing_RNG_actor_component_calendar_andlate_RGB_measurements_preserved=True,
        late_RGB_differences_byblock=[dict(block=34,differences=0,samples=163),dict(block=108,differences=75,samples=75),dict(block=35,differences=60,samples=79)],
        no_everyframe_fullRAM_future_sequence_broad_simulation_orcausal_claim=True,
        original_normal_type0_value_carry_andR65_source_only_nineteenth_cell_findings_preserved=True,
        original_audit7752_and7752b_failures_preserved_not_ROM_failures_ornegative_control_rejections=True,
        final_prose_refinements=findings,name_review=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),
        all67_final_formatting_gates_remain_false_pending_refinements_policy_atomic_production_andregistered_integration=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        initialized_fixture_not_natural_optional_activation_original_location_earned_progress_full_effects_routes_orhardware=True,
        incidental_Chun_no_sailors_resupply_food_water_andnavigation_messages_no_editorial_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,LATER,OLD_NAMES,NAMES,RIGHTCELL,TRIAGE,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('131actual panes/33viewed sheets/65paired upperRGB matches;532complete body+header holds. Two finalprose refinements recorded;all old artifacts andlater limits preserved.No completion credit.')
