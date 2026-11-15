"""Seal actual evidence for unchanged content and retain the reopened wine reply explicitly."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'initial_gameplay_review_v1.json';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v2/reconstruction.json';rebuilt=load(rebuiltpath)
    native={r['id']:r for r in load(rebuilt['native'])['records']}
    selectionpath=ROOT/'display_selection_v1.json';selection=load(selectionpath)
    transitionpath=ROOT/'transition_review_v1/receipt.json';transitions=load(transitionpath)
    menupath=ROOT/'actual_menu_inputs_v1/native_menus.json';menutable=load(menupath)
    menus_by_key={(m['block'],m['source_command_offset']):m for m in menutable['menus']}
    assert transitions['source_complete_hosts_reach_resupply_departure_andfinal_sailing'] and len(transitions['runs'])==3
    evidence=[rebuiltpath,Path(rebuilt['native']),selectionpath,transitionpath,menupath,Path(__file__)]
    observed=set();pages_seen=set();captions=set();headers=set();sheets=[];runs=[];totals=[0,0,0];allmenus=[];FEchecks=[]
    for choice,frames,bodies,headerplanes in [(0,29681,80,106),(1,11681,5,10),(2,11201,4,6)]:
        paths={k:ROOT/f'{directory}_menu{choice}_v1/{name}' for k,directory,name in [
            ('terminal','display_run','terminal.json'),('runplan','display_run','run_plan.json'),
            ('pixels','display_pixels','focused_actual_pixels.json'),('menus','menu_pixels','menu_actual_pixels.json')]}
        d={k:load(p) for k,p in paths.items()};terminal,pixel,menus=d['terminal'],d['pixels'],d['menus']
        assert terminal['terminal'] and terminal['frames']==pixel['frames']==frames
        report,observer=map(load,[terminal['report'],terminal['observer']])
        assert digest(terminal['report'])==terminal['report_sha256'] and digest(terminal['observer'])==terminal['observer_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and verified_existing_unlock(report)
        assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert (pixel['selected_utterances'],pixel['selected_pages'],pixel['complete_body_planes'],pixel['complete_header_planes'])==(bodies,bodies,2*bodies,headerplanes)
        assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        fixturepath=Path(d['runplan']['fixture']);fixture=load(fixturepath)
        assert digest(fixturepath)==d['runplan']['fixture_sha256']
        assert digest(fixture['research_ROM'])==fixture['research_ROM_sha256']==report['ROM_sha256']
        assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
        assert len(fixture['original_initializers'])==7 and len(fixture['source_bound_QA_host_opening_exit'])==40
        assert fixture['padded_QA_block_bytes']<=fixture['source_bound_QA_block_limit']==9216
        assert fixture['no_savestate_RAM_roster_money_RNG_eventflag_orcondition_result_override']
        controls=load(fixture['inputs']);assert digest(fixture['inputs'])==fixture['inputs_sha256']
        assert all(c['duration']==16 for c in controls if c['buttons']==['A'] and c['start']>=4000)
        for sample in pixel['body_pages']:
            display=native[sample['id']]['complete_native_English_display']
            plane=display if sample['selector']==254 else display['pages'][sample['page']-1]
            assert digest(sample['native_plane'])==sample['native_plane_sha256']==plane['native_plane_sha256']
            assert digest(sample['capture']['path'])==sample['capture']['PNG_sha256']
            observed.add(sample['id']);pages_seen.add((sample['id'],sample['page']))
        headers.update((h['source_selector'],h['expected_actor_ID'],h['text']) for h in pixel['headers'])
        assert menus['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert menus['ordinary_A_return_to_next_fixture_speech_observed']
        assert len(menus['menus'])==len(fixture['menus'])==(2 if choice<2 else 1)
        calls=pixel['ordered_selected_source_calls']
        for m in menus['menus']:
            key=m['block'],m['clean_source_command_offset'];proven=menus_by_key[key]
            assert digest(m['proof'])==m['proof_sha256']==proven['native_receipt_sha256']
            expected=list(range(choice+1)) if m['count']==3 else [0] if choice==0 else [0,1]
            assert m['observed_selected_options']==expected
            assert m['observed_default_return_A_input'] in [c['start'] for c in controls if c['buttons']==['A'] and c['duration']==16]
            assert m['following_speech_frame']==next(c['frame'] for c in calls if c['id']==m['following_speech'])
            captions.update(proven['record_ids']);allmenus.append(dict(run=choice,**m))
        if choice==0:
            FEids={r['id'] for r in fixture['selected_records'] if r['selector']==254};assert len(FEids)==27
            for ident in sorted(FEids):
                call=next(c for c in calls if c['id']==ident)
                following=next(c for c in calls if c['frame']>call['frame'])
                pushes=[c for c in controls if call['frame']<c['start']<following['frame'] and c['buttons']==['A']]
                assert len(pushes)==1 and pushes[0]['duration']==16
                FEchecks.append(dict(id=ident,call=call,following=following,ordinary_A=pushes[0]))
            call=next(c for c in calls if c['id']=='DK4_MES_B169_R0073')
            following=next(c for c in calls if c['frame']>call['frame'])
            assert following['id']=='DK4_MES_B169_R0106' and call['page']==1
            assert len([c for c in controls if call['frame']<c['start']<following['frame'] and c['buttons']==['A']])==1
        transition=next(t for t in transitions['runs'] if t['choice']==choice);assert transition['frames']==frames
        sheets.extend(pixel['review_sheets']);sheets.extend([menus['review_sheet'],transition['review_sheet']])
        totals=[a+b for a,b in zip(totals,[pixel['complete_body_planes'],pixel['complete_header_planes'],menus['complete_live_caption_samples']],strict=True)]
        runs.append(dict(choice=choice,frames=frames,physical_body_candidates=bodies,pages=bodies,run_plan=str(paths['runplan'])))
        evidence.extend([*paths.values(),fixturepath,Path(terminal['report']),Path(terminal['observer']),Path(fixture['inputs'])])
    assert observed==set(selection['selected_speech_ids']) and len(observed)==len(pages_seen)==83
    assert len(captions)==5 and len(allmenus)==5 and totals==[178,122,19] and len(sheets)==22
    forecasts={r['block'] for r in native.values() if r['id'] in observed and 'may soon be popular' in r['logical_English']}
    assert forecasts==set(range(152,169))
    for sheet in sheets:assert digest(sheet['path'])==sheet['sha256']
    reopened='DK4_MES_B152_R0008'
    assert reopened in observed
    save(out,dict(frames=52563,initialized_runs=3,runs=runs,distinct_source_body_objects=83,distinct_body_pages=83,
        complete_body_planes=178,complete_header_planes=122,complete_live_menu_samples=19,
        observed_body_IDs=sorted(observed),observed_source_body_IDs=sorted(observed),observed_caption_IDs=sorted(captions),
        unvisited_source_IDs=sorted(set(native)-observed),offline_only_source_body_objects=290,
        actual_menus=2,actual_menu_occurrences=5,actual_caption_strings=5,offline_only_caption_strings=12,
        both_two_choice_options_all_three_indices_andordinary_A_returns_observed=True,ordinary_menu_returns=allmenus,
        numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited=True,FE_panels=FEchecks,
        all17_town_forecasts_and27_FE_panels_observed=True,reclaimed_bargaining_aside_single_page_andfollowing_A_observed=True,
        Calicut_padding_repair_complete_single_row_andnormal_A_return_observed=True,
        Wits_fullwidth50000_Namahage_andGlassmakingGuide_repairs_observed=True,
        name_headers=[dict(source_selector=s,expected_actor_ID=a,text=t) for s,a,t in sorted(headers)],
        all83_initial_pages_five_captions_andthree_host_transitions_directly_viewed=True,
        all_selected_complete_body_header_andmenu_pixel_bounds_blank_andcentering_checks_pass=True,
        complete_source_QA_hosts_return_to_resupply_andordinary_sailing=True,
        review_sheets=[dict(s,directly_viewed=True) for s in sheets],actual_gameplay=True,disclosed_initialized_fixture=True,
        existing_system_only_unlock_not_earned=True,natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        initial_prose_reopened_after_actual_whole_exchange_review=True,contextual_retention_reopened_IDs=[reopened],
        changed_current_reply_not_approved_by_old_actual_page=True,unchanged_actual_body_IDs_available_for_exact_dependency_reuse=sorted(observed-{reopened}),
        current_prose_orall_fifth_gates_not_approved_here=True,full_current_batch_gameplay_approval=False,
        source_event_conditions_rewards_andstat_effects_not_simulated=True,full_catalogue_UI_unvisited=True,
        guide_photos=False,new_credit=0,registered_integration_pending=True,evidence={str(p):digest(p) for p in evidence}))
    print('Verified three actual runs:83 original bodies,5 captions,27 FE returns andthree sailing exits;one reopened reply requires fresh target evidence.')


if __name__=='__main__':main()
