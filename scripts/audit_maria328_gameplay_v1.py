"""Seal the directly viewed representative run without claiming natural event activation."""
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

def main():
    target=ROOT/'gameplay_review_v1.json';assert not target.exists()
    paths=dict(terminal=ROOT/'display_run_v1/terminal.json',pixels=ROOT/'display_pixels_v1/focused_actual_pixels.json',
        menus=ROOT/'display_menu_pixels_v1/menu_actual_pixels.json',runplan=ROOT/'display_run_v1/run_plan.json',
        selection=ROOT/'display_selection_v1.json',transition=ROOT/'transition_review_v1/receipt.json',
        rebuilt=ROOT/'reconstruction_v1/reconstruction.json',stored=ROOT/'stored_v1/stored_native_verification.json')
    data={k:load(p) for k,p in paths.items()};terminal=data['terminal'];pixel=data['pixels'];menus=data['menus']
    assert terminal['terminal'] and terminal['frames']==pixel['frames']==22001
    report,observer=map(load,[terminal['report'],terminal['observer']])
    assert digest(terminal['report'])==terminal['report_sha256'] and digest(terminal['observer'])==terminal['observer_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and verified_existing_unlock(report)
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
    assert (pixel['selected_utterances'],pixel['selected_pages'],pixel['complete_body_planes'],pixel['complete_header_planes'])==(44,48,96,72)
    fixturepath=Path(data['runplan']['fixture']);assert digest(fixturepath)==data['runplan']['fixture_sha256']
    fixture=load(fixturepath);assert digest(fixture['research_ROM'])==fixture['research_ROM_sha256']==report['ROM_sha256']
    assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
    assert len(fixture['original_initializers'])+len(fixture['source_bound_QA_host_opening_exit'])==47
    assert fixture['padded_QA_block_bytes']<=fixture['source_bound_QA_block_limit']==9216
    nativepath=Path(data['rebuilt']['native']);native={r['id']:r for r in load(nativepath)['records']}
    bodyviews=set();observed=set()
    for sample in pixel['body_pages']:
        display=native[sample['id']]['complete_native_English_display']
        plane=display if sample['selector']==254 else display['pages'][sample['page']-1]
        assert digest(sample['native_plane'])==sample['native_plane_sha256']==plane['native_plane_sha256']
        assert digest(sample['capture']['path'])==sample['capture']['PNG_sha256']
        observed.add(sample['id']);bodyviews.add((sample['id'],sample['page']))
    assert observed==set(data['selection']['selected_speech_ids']) and (len(observed),len(bodyviews))==(44,48)
    physical=load(data['rebuilt']['manuscript']);byid={r['id']:r for r in physical['records']}
    sourceids={byid[i].get('source_editorial_ID',i) for i in observed};assert len(sourceids)==43
    original=load(data['rebuilt']['source_manuscript'])
    allbodyids={r['id'] for r in original['records'] if r['kind']!='typed-choice-label'}
    assert len(allbodyids)==313 and len(allbodyids-sourceids)==270
    first='DK4_MES_B87_R0139_FE_PAGE_1';second='DK4_MES_B87_R0139_FE_PAGE_2';following='DK4_MES_B87_R0194'
    calls=[c for c in pixel['ordered_selected_source_calls'] if c['id'] in [first,second,following]]
    assert calls==[dict(frame=5465,id=first,page=1),dict(frame=5706,id=second,page=1),dict(frame=6177,id=following,page=1)]
    controls=load(fixture['inputs']);assert digest(fixture['inputs'])==fixture['inputs_sha256']
    for frame in [5680,5920,6160]:assert next(c for c in controls if c['start']==frame)==dict(start=frame,duration=16,buttons=['A'])
    expectedFE={r['expected_expanded_body_hex'] for r in fixture['selected_records'] if r['id'] in [first,second]}
    middle=[r for r in observer['rows'] if r['kind']=='modal_paint' and 5465<=r['frame']<6177]
    assert {r['text_hex'] for r in middle}==expectedFE
    assert menus['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert {(m['block'],m['source_command_offset']) for m in menus['menus']}=={(87,816),(92,372)}
    assert len(menus['menu_samples'])==menus['complete_live_caption_samples']==4
    assert all(m['count']==3 and m['observed_selected_options']==[0] for m in menus['menus'])
    assert [s['frame'] for s in menus['menu_samples'] if s['source_command_offset']==next(m['stored_command_offset'] for m in menus['menus'] if m['block']==87)]==[6000,6120]
    captionids={r['id'] for o in data['stored']['typed_objects'] if (o['block'],o['offset']) in {(m['block'],m['stored_command_offset']) for m in menus['menus']} for r in o['label_references']}
    assert len(captionids)==6
    allcaptions={r['id'] for r in original['records'] if r['kind']=='typed-choice-label'}
    headers={(h['source_selector'],h['expected_actor_ID'],h['text']) for h in pixel['headers']}
    assert {h[0] for h in headers}=={3,4,10,22,137,163,170,207,208,214,215}
    assert len({h[1] for h in headers})==8
    assert 'SC3_B95_STYLE_400_42' in observed and 'SC3_B95_STYLE_400_18' not in observed
    assert fixture['source_personality_tables_copied_complete']==3
    sheets=pixel['review_sheets']+[menus['review_sheet'],data['transition']['review_sheet']]
    assert len(pixel['review_sheets'])==8
    for sheet in sheets:assert digest(sheet['path'])==sheet['sha256']
    for sample in data['transition']['samples']:assert digest(sample['capture']['path'])==sample['capture']['PNG_sha256']
    assert data['transition']['source_complete_host_reaches_resupply_departure_andfinal_sailing_capture']
    post=[r for r in observer['rows'] if r['kind']=='modal_paint' and r['frame']>pixel['ordered_selected_source_calls'][-1]['frame']]
    assert any(r['frame']==17938 and r['text_CP932']==' Want to resupply for ６００ gold?' for r in post)
    assert any(r['frame']==18911 and 'Departed Hangzhou.' in r['text_CP932'] for r in post)
    evidencepaths=[*paths.values(),fixturepath,nativepath,Path(terminal['report']),Path(terminal['observer']),Path(fixture['inputs']),Path(__file__)]
    save(target,dict(frames=22001,initialized_runs=1,distinct_native_body_candidates=44,distinct_source_body_objects=43,
        distinct_body_pages=48,complete_body_planes=96,complete_header_planes=72,offline_only_source_body_objects=270,
        observed_body_IDs=sorted(observed),observed_source_body_IDs=sorted(sourceids),unvisited_source_IDs=sorted(allbodyids-sourceids),
        observed_caption_IDs=sorted(captionids),unvisited_caption_IDs=sorted(allcaptions-captionids),actual_menus=2,actual_caption_strings=6,
        complete_live_menu_samples=4,other_selections_cancellation_andoriginal_branch_outcomes_unvisited=True,
        source_owned_FE_continuation_A_then_menu_then_named_return_observed=True,FE_first_frame=5465,FE_continuation_frame=5706,
        following_named_frame=6177,ordinary_A_frames=[5680,5920,6160],no_extra_blank_FE_panel_observed=True,
        repaired_bean_FE_rows_andfour_progressive_two_page_layouts_observed=True,complete_dynamic_style_objects_observed=3,
        corrected_corrupt_style_observed='SC3_B95_STYLE_400_42',other_corrupt_style_offline_only='SC3_B95_STYLE_400_18',
        name_headers=[dict(source_selector=s,expected_actor_ID=a,text=t) for s,a,t in sorted(headers)],
        source_role_IDs_qualified_offline_not_inferred_from_header_pixels=True,
        all48_selected_pages_six_captions_andhost_transitions_directly_viewed=True,
        all_selected_complete_body_header_andmenu_pixel_bounds_blank_andcentering_checks_pass=True,
        host_resupply_frame=17938,host_departure_frame=18911,host_final_sailing_frame=22001,
        complete_source_QA_host_returns_to_resupply_andordinary_sailing=True,
        review_sheets=[dict(s,directly_viewed=True) for s in sheets],
        actual_gameplay=True,disclosed_initialized_fixture=True,existing_system_only_unlock_not_earned=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        source_event_conditions_rewards_cutscene_art_andstat_effects_not_simulated=True,
        guide_photos=False,new_credit=0,registered_integration_pending=True,evidence={str(p):digest(p) for p in evidencepaths}))
    print('PASS actual QA:43 source bodies/44 native candidates/48 viewed pages,six captions,eight actor headers;FE/menu/style/pagination/host transitions pass.')

if __name__=='__main__':main()
