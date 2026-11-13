"""Finalize539 research reviews after complete storage and representative scene checks."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B61_B80_checked_20261104')
FORMAT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
REBUILT=Path('work/analysis/Rafael_B61_B80_rebuilt_v12_20261104/reconstruction.json')
STORED=Path('work/analysis/Rafael_B61_B80_stored_native_v12_20261104/stored_native_verification.json')
LOOKUP=Path('work/analysis/Rafael_B61_B80_stored_catalogue_v12_20261104/all539_stored_effective_body_bindings.json')
LOADERS=Path('work/analysis/Rafael_B61_B80_loaders_v12_20261104/verification.json')
NAMES=Path('translations/rafael_B61_B80_scoped_progressive_names_research_final_v1.json')
NAME_PIXELS=Path('work/analysis/Rafael_B61_B80_names_pagination_pixels_v12_20261104/focused_actual_pixels.json')
CG_PIXELS=Path('work/analysis/Rafael_B69_complete_scene_pixels_v12_20261104/focused_actual_pixels.json')
FINAL=Path('translations/rafael_B61_B80_contextual_final_review_v1.json')
NAMES_FINAL=Path('translations/rafael_B61_B80_scoped_names_actual_final_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists() and not NAMES_FINAL.exists()
    manuscript=FORMAT/'formatting_input_v5.json';plan_path=FORMAT/'automatic_v12/automatic_plans.json'
    native_path=FORMAT/'combined_native_v12.json';visual_path=FORMAT/'body_display_approval_v12.json'
    doc,plan,native,visual,rebuilt,stored,lookup,loaders,names,np,cg=map(load,[
        manuscript,plan_path,native_path,visual_path,REBUILT,STORED,LOOKUP,LOADERS,NAMES,NAME_PIXELS,CG_PIXELS])
    assert len(doc['records'])==len(native['records'])==len(plan['records'])==len(stored['records'])==len(lookup['records'])==539
    assert not plan['failures'] and visual['all_final_pages_directly_viewed']
    assert stored['complete_stored_pages']==visual['body_pages']==native['pages']==545
    assert stored['reconstruction_sha256']==sha(REBUILT.read_bytes()) and stored['native_sha256']==sha(native_path.read_bytes())
    assert native['runtime']==stored['runtime'] and native['runtime']['captain']==0
    assert stored['exact_previous_stored_records_reused']==538 and stored['fresh_parity_dependent_pages']==1
    assert stored['fresh_relocated_native_relative_cases']==485
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,2,684)
    assert all(not load(FORMAT/file)[key] for file,key in [('no_menu_objects_v12.json','menus'),('no_style_objects_v12.json','objects')])
    assert sum(r['decision']=='revision' for r in doc['records'])==210
    assert sum(r['decision']=='retention' for r in doc['records'])==329
    for result in [np,cg]:
        assert result['all_selected_pages_observed_in_exact_fixture_order']
        assert result['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(result[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
    assert (np['selected_utterances'],np['selected_pages'])==(29,35)
    assert (cg['selected_utterances'],cg['selected_pages'])==(66,66) and cg['complete_scene_commands_retained']
    assert len(np['observed_actor_IDs'])==22 and set(np['observed_actor_IDs'])=={r['actor_ID'] for r in names['records']}
    sheets=np['review_sheets']+cg['review_sheets'];assert len(sheets)==17
    for sheet in sheets:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    old_names=load('work/analysis/Rafael_B61_B80_names_pagination_pixels_20261104/focused_actual_pixels.json')
    assert [s['sha256'] for s in np['review_sheets']]==[s['sha256'] for s in old_names['review_sheets']]
    observed={r['id'] for result in [np,cg] for r in result['body_pages']}
    observed_pages={(r['id'],r['page']) for result in [np,cg] for r in result['body_pages']}
    assert len(observed)==95 and len(observed_pages)==101
    question=next(r for r in doc['records'] if r['id']=='DK4_MES_B69_R0069')
    assert question['english']=='Does it look bad on me?' and question['id'] in observed
    ROOT.mkdir()
    visual_actual=ROOT/'actual_visual_approval.json'
    save(visual_actual,dict(reviewed_sheets=sheets,all17_final_sheets_directly_viewed_or_exact_sheet_pixel_reuse=True,
        six_name_sheets_exact_to_six_directly_viewed_predecessor_sheets=True,eleven_final_CG_sheets_directly_viewed=True,
        revised_negative_question_andretained_reassurance_read_as_one_exchange=True,
        all22_scoped_names_all_six_pagination_cases_andall_six_FE_speeches_complete=True,
        complete_original_CG_kiss_sequence_andreturn_observed=True,
        guide_photos=False,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    actual_path=ROOT/'actual_review.json'
    actual=dict(total_frames=102005,initialized_fixture_runs=5,qualifying_final_revision_frames=39002,
        qualifying_final_revision_runs=2,prior_capture_gap_andpre_reassurance_runs_preserved=True,
        actual_utterances=95,actual_body_pages=101,offline_only_utterances=444,
        complete_body_planes=np['complete_body_planes']+cg['complete_body_planes'],
        complete_header_planes=np['complete_header_planes']+cg['complete_header_planes'],
        observed_actor_IDs=np['observed_actor_IDs'],sampled_ids=sorted(observed),
        all17_final_sheets_directly_viewed_or_exact_sheet_pixel_reuse=True,
        complete_original_B69_66_speeches_92_commands_CG_actions_andreturn_observed=True,
        all_six_FE_speeches_all_six_two_page_cases_andall22_headers_observed=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        final_name_pixels=str(NAME_PIXELS),final_name_pixels_sha256=sha(NAME_PIXELS.read_bytes()),
        final_CG_pixels=str(CG_PIXELS),final_CG_pixels_sha256=sha(CG_PIXELS.read_bytes()),
        numeric_branch_conditions_andfull_catalogue_UI_unvisited=True,new_credit=0,guide_photos=False)
    save(actual_path,actual)
    final_names=deepcopy(names)
    for row in final_names['records']:
        assert row['actor_ID'] in np['observed_actor_IDs'] and all(row['review'].values())
        row.update(actual_target_headers_unvisited=False,actual_header_evidence=dict(
            path=str(NAME_PIXELS),sha256=sha(NAME_PIXELS.read_bytes()),actor_ID=row['actor_ID']))
        row['formatting_scope']='Complete native style11 planes andpixel-bound actual headers in the final disclosed initialized fixture; full catalogue UI remains unvisited.'
    final_names.update(actual_scene_headers_unvisited=False,no_new_dialogue_credit=True,
        actual_header_evidence=str(NAME_PIXELS),actual_header_evidence_sha256=sha(NAME_PIXELS.read_bytes()),
        previous_scoped_research=str(NAMES),previous_scoped_research_sha256=sha(NAMES.read_bytes()),new_credit=0)
    validate_natural_dialogue_batch(final_names);save(NAMES_FINAL,final_names)
    final=deepcopy(doc);by_stored={r['id']:r for r in stored['records']};by_plan={r['id']:r for r in plan['records']}
    for row in final['records']:
        assert all(row['review'][g] for g in ['source','context','localization','naturalness'])
        entry=by_stored[row['id']];row['review']['formatting']=True
        row.update(planned_integrated_reference=dict(file_path=doc['file_path'],block=row['block'],
            offset=entry['new_offset'],header_offset=entry['new_offset']-5,record_index=entry['new_record_index'],
            exact_stored_hex=entry['stored_hex'],target_archive_sha256=rebuilt['target_archive_sha256']),
            planned_English_markup=by_plan[row['id']]['formatted_markup'],
            registered_release_andcompletion_credit_pending=True,all_fifth_formatting_gates_still_pending=False,
            complete_native_preamble_andfresh_formatting_pending=False,
            fresh_formatting_native_visual_stored_andrepresentative_gameplay_pending=False,
            actual_utterance_observed_in_disclosed_fixture=row['id'] in observed,
            formatting_evidence=dict(native=str(native_path),stored=str(STORED),loaders=str(LOADERS),
                actual=str(actual_path),visual=str(visual_actual),scope='All545 pages offline;95 utterances/101 pages observed,444 offline-only. Complete original B69 behind initialized opening; focused name/pagination sequence. No natural event activation.'))
    evidence=[manuscript,plan_path,native_path,visual_path,REBUILT,STORED,LOOKUP,LOADERS,NAMES_FINAL,
        NAME_PIXELS,CG_PIXELS,actual_path,visual_actual,FORMAT/'no_menu_objects_v12.json',FORMAT/'no_style_objects_v12.json',Path(__file__)]
    final.update(format='dk4-editorial-final-review-v1',all_five_individual_review_gates_passed=True,
        all_formatting_gates_false=False,registered_release_andcompletion_credit_pending=True,new_credit=0,
        scoped_name_review=str(NAMES_FINAL),scoped_name_review_sha256=sha(NAMES_FINAL.read_bytes()),
        formatting_evidence={str(p):sha(p.read_bytes()) for p in evidence})
    validate_natural_dialogue_batch(final);save(FINAL,final);save(ROOT/'release_plans.json',plan)
    save(ROOT/'formatting_checkpoint.json',dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        scoped_names=str(NAMES_FINAL),scoped_names_sha256=sha(NAMES_FINAL.read_bytes()),prose_reviews=539,
        revised=210,retained=329,body_pages=545,layout_refinements=14,ASCII_I_fixes=16,ellipsis_fixes=14,
        scoped_names_retained=22,actual_utterances=95,actual_body_pages=101,offline_only_utterances=444,
        all_individual_five_gates_pass_in_research=True,registered_release_andcompletion_credit_pending=True,
        new_credit=0,guide_photos=False,full_goal_complete=False))
    print('539 five-gate research reviews;95 observed utterances/101 pages/22 headers,444 offline-only. Registered integration pending;zero new credit.')
