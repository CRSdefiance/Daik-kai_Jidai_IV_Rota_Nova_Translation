"""Seal observed prototype coverage andthe fresh one-page revision,without relabeling old English as new."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael330_actual_progress_20261105')
PROOFS=[Path('work/analysis')/p/'focused_actual_pixels.json' for p in [
    'Rafael_B81_complete_scene_pixels_v2_20261105','Rafael330_names_pages_FE_pixels_v1_20261105','Rafael330_menu_cursor_body_pixels_v3_20261105']]
MENUS=[Path('work/analysis')/p/'menu_actual_pixels.json' for p in ['Rafael330_menu_actual_pixels_v2_20261105','Rafael330_menu_cursor_actual_pixels_v2_20261105']]
SHEETS=[Path('work/analysis')/p/'receipt.json' for p in ['Rafael_B81_actual_compact_sheets_20261105','Rafael330_names_pages_actual_compact_sheets_20261105']]
FRESH=Path('work/analysis/Rafael_Emilio_food_acceptance_20261105/native_v2/compiled_native_pages.json')

if __name__=='__main__':
    assert not ROOT.exists();results=list(map(load,PROOFS));menus=list(map(load,MENUS));native=load(FRESH)
    full,focused,body=results
    assert (full['selected_utterances'],full['selected_pages'],focused['selected_utterances'],focused['selected_pages'],body['selected_utterances'])==(49,49,35,44,3)
    for d in results:
        assert d['all_selected_pages_observed_in_exact_fixture_order'] and d['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(d[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
    assert len(focused['observed_actor_IDs'])==16 and full['complete_scene_commands_retained']
    assert sum(d['complete_body_planes'] for d in results)==203 and sum(d['complete_header_planes'] for d in results)==187
    allmenus={}
    for d in menus:
        assert d['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        for menu in d['menus']:allmenus.setdefault(menu['source_command_offset'],set()).update(menu['observed_selected_options'])
    assert allmenus=={3114:{0,1},5298:{0,1,2}}
    doc=load(Path('work/analysis/Rafael330_stored_consumer_inputs_20261105/native_consumer_manuscript.json'))
    byid={r['id']:r.get('source_editorial_ID',r['id']) for r in doc['records']}
    sourceids={byid[r['id']] for d in results for r in d['body_pages']};pages={(r['id'],r['page']) for d in results for r in d['body_pages']}
    assert len(sourceids)==75 and len(pages)==86 and 'DK4_MES_B81_R0220' in sourceids
    assert {'DK4_MES_B81_R0037','DK4_MES_B81_R0070'}<={r['id'] for r in focused['body_pages']}
    assert len(native['records'])==native['pages']==1 and native['fresh_compiled_alignments']==4
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    for receiptpath in SHEETS:
        receipt=load(receiptpath)
        for sheet in receipt['bottom_screen_sheets']+receipt['full_scene_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert sum(len(load(p)['bottom_screen_sheets']) for p in SHEETS)==9 and len(load(SHEETS[0])['full_scene_sheets'])==1
    for d in menus:
        sheet=d['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    for s in [*body['review_sheets'],*native['review_sheets']]:assert sha(Path(s['path']).read_bytes())==s['sha256']
    ROOT.mkdir();save(ROOT/'actual_visual_andscope_approval_v1.json',dict(
        nine_compact_actual_sheets_andone_full_CG_sheet_directly_viewed=True,
        two_menu_cursor_sheets_andone_menu_response_sheet_directly_viewed=True,
        fresh_Emilio_native_page_directly_viewed=True,
        initialized_fixture_runs=4,total_frames=58004,prototype_actual_source_speeches=75,prototype_actual_native_body_pages=86,
        prototype_complete_body_holds=203,prototype_complete_header_holds=187,all16_scoped_names_actual_complete=True,
        all_five_native_menu_captions_all_two_andthree_cursor_indices_andA_to_following_speech_observed=True,
        all_four_FE_continuation_panels_andthree_FI_notice_texts_observed=True,
        all_nine_two_page_speeches_andseven_refined_page_turns_observed=True,
        original_B81_101_command_scene_retained_actual_branch49_of51_speeches=True,
        two_conditional_B81_asides_unvisited_in_whole_scene_but_observed_in_focused_fixture=True,
        actual_CG_is_static_Emilio_portrait_not_proof_of_who_threw_whom=True,
        faithful_agent_object_implicit_throw_wording_retained_no_invented_action=True,
        latest_manuscript='translations/rafael_B81_B84_contextual_editorial_manuscript_v2.json',latest_manuscript_source_records=330,
        latest_revision_count=174,latest_retention_count=156,current_wording_compatible_actual_source_speeches=74,current_wording_compatible_actual_body_pages=85,
        changed_Emilio_ID='DK4_MES_B81_R0220',changed_Emilio_fresh_native_page_pass=True,changed_Emilio_stored_andactual_pending=True,
        old_R220_actual_capture_not_relabelled_as_revised_English=True,
        actual_training_stat_effects_numeric_menu_return_registers_original_story_branch_outcomes_fullroute_andhardware_unvisited=True,
        ordinary_postfixture_opening_dialogue_seen_but_not_newly_reviewed_by_this_batch=True,
        all_original_full_captures_andprior_failed_analysis_receipts_preserved=True,
        registered_integration_andformal_batch_finalization_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [*PROOFS,*MENUS,*SHEETS,FRESH,Path(__file__)]}))
    print('Sealed four initialized runs/58004frames:75 prototype source speeches/86 bodypages,16 names,allmenu indices,FE continuations. One revisedEmilio page hasfresh native only;stored/actual andintegration remain.')
