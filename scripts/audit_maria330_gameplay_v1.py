"""Seal the two directly viewed runs, preserving actual versus offline scope."""
from pathlib import Path
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

def main():
    target=ROOT/'gameplay_review_v1.json'; assert not target.exists()
    rebuiltpath=ROOT/'reconstruction_v2/reconstruction.json'; rebuilt=load(rebuiltpath)
    physical=load(rebuilt['manuscript']); byid={r['id']:r for r in physical['records']}
    original=load(rebuilt['source_manuscript'])
    bodyids={r['id'] for r in original['records'] if r['kind']!='typed-choice-label'}
    captions={r['id'] for r in original['records'] if r['kind']=='typed-choice-label'}
    nativepath=Path(rebuilt['native']); native={r['id']:r for r in load(nativepath)['records']}
    selectionpath=ROOT/'display_selection_v1.json'; selection=load(selectionpath)
    transitionpath=ROOT/'transition_review_v1/receipt.json'; transitions=load(transitionpath)
    assert transitions['source_complete_hosts_reach_resupply_departure_andfinal_sailing']
    evidence=[rebuiltpath,nativepath,selectionpath,transitionpath,Path(__file__)]
    observed=set(); bodyviews=set(); headers=set(); runs=[]; sheets=[]; FEchecks=[]; total_body=total_headers=total_menu=0
    for choice,frames,utterances,pages,headerplanes in [(0,22721,49,52,88),(1,11681,6,6,12)]:
        paths={k:ROOT/f'{directory}_menu{choice}_v1/{name}' for k,directory,name in [
            ('terminal','display_run','terminal.json'),('runplan','display_run','run_plan.json'),
            ('pixels','display_pixels','focused_actual_pixels.json'),('menus','menu_pixels','menu_actual_pixels.json')]}
        data={k:load(p) for k,p in paths.items()}; terminal,pixel,menus=[data[k] for k in ['terminal','pixels','menus']]
        assert terminal['terminal'] and terminal['frames']==pixel['frames']==frames
        report,observer=map(load,[terminal['report'],terminal['observer']])
        assert digest(terminal['report'])==terminal['report_sha256'] and digest(terminal['observer'])==terminal['observer_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and verified_existing_unlock(report)
        assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        assert (pixel['selected_utterances'],pixel['selected_pages'],pixel['complete_body_planes'],pixel['complete_header_planes'])==(utterances,pages,pages*2,headerplanes)
        fixturepath=Path(data['runplan']['fixture']); fixture=load(fixturepath)
        assert digest(fixturepath)==data['runplan']['fixture_sha256']
        assert digest(fixture['research_ROM'])==fixture['research_ROM_sha256']==report['ROM_sha256']
        assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
        assert len(fixture['original_initializers'])+len(fixture['source_bound_QA_host_opening_exit'])==47
        assert fixture['padded_QA_block_bytes']<=fixture['source_bound_QA_block_limit']==9216
        assert fixture['no_savestate_RAM_roster_money_RNG_eventflag_orcondition_result_override']
        for sample in pixel['body_pages']:
            display=native[sample['id']]['complete_native_English_display']
            plane=display if sample['selector']==254 else display['pages'][sample['page']-1]
            assert digest(sample['native_plane'])==sample['native_plane_sha256']==plane['native_plane_sha256']
            assert digest(sample['capture']['path'])==sample['capture']['PNG_sha256']
            observed.add(sample['id']); bodyviews.add((sample['id'],sample['page']))
        headers.update((h['source_selector'],h['expected_actor_ID'],h['text']) for h in pixel['headers'])
        assert menus['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert len(menus['menus'])==1
        m=menus['menus'][0]; assert (m['block'],m['source_command_offset'],m['count'])==(102,210,2)
        assert m['observed_selected_options']==([0] if choice==0 else [0,1])
        assert len(menus['menu_samples'])==menus['complete_live_caption_samples']==(2 if choice==0 else 4)
        if choice==0:
            controls=load(fixture['inputs']); assert digest(fixture['inputs'])==fixture['inputs_sha256']
            for owner in physical['pagination_owners']:
                ids=owner['child_IDs']; calls=[c for c in pixel['ordered_selected_source_calls'] if c['id'] in ids]
                assert [c['id'] for c in calls]==ids and all(c['page']==1 for c in calls)
                after=next(c for c in pixel['ordered_selected_source_calls'] if c['frame']>calls[-1]['frame'])
                assert after['id']==('DK4_MES_B116_R0044' if owner['source_ID'].endswith('0041') else 'DK4_MES_B116_R0054')
                inputs=[]
                for left,right in [(calls[0],calls[1]),(calls[1],after)]:
                    pushes=[c for c in controls if left['frame']<c['start']<right['frame'] and c['buttons']==['A']]
                    assert len(pushes)==1 and pushes[0]['duration']==16; inputs.append(pushes[0])
                paints=[r for r in observer['rows'] if r['kind']=='modal_paint' and calls[0]['frame']<=r['frame']<after['frame']]
                expected={r['expected_expanded_body_hex'] for r in fixture['selected_records'] if r['id'] in ids}
                assert {r['text_hex'] for r in paints}==expected
                FEchecks.append(dict(source_ID=owner['source_ID'],calls=calls,following=after,ordinary_A_inputs=inputs,no_extra_blank_panel=True))
            assert fixture['source_personality_tables_copied_complete']==5
        else:
            controls=load(fixture['inputs'])
            assert dict(start=4140,duration=4,buttons=['DOWN']) in controls
        transition=next(t for t in transitions['runs'] if t['choice']==choice)
        assert transition['frames']==frames
        for sample in transition['samples']:assert digest(sample['capture']['path'])==sample['capture']['PNG_sha256']
        sheets.extend(pixel['review_sheets']); sheets.append(transition['review_sheet'])
        # The default menu montage displayed poorly in the image viewer. The exact full frame was viewed instead.
        if choice==0:
            direct=next(s['capture'] for s in menus['menu_samples'] if s['frame']==13920)
            sheets.append(dict(path=direct['path'],sha256=direct['PNG_sha256']))
        else:sheets.append(menus['review_sheet'])
        total_body+=pixel['complete_body_planes']; total_headers+=pixel['complete_header_planes']; total_menu+=menus['complete_live_caption_samples']
        runs.append(dict(choice=choice,frames=frames,physical_body_candidates=utterances,pages=pages,
            source_personality_tables_copied_complete=fixture['source_personality_tables_copied_complete']))
        evidence.extend([*paths.values(),fixturepath,Path(terminal['report']),Path(terminal['observer']),Path(fixture['inputs'])])
    assert observed==set(selection['selected_speech_ids']) and (len(observed),len(bodyviews))==(55,58)
    sourceids={byid[i].get('source_editorial_ID',i) for i in observed}
    assert (len(bodyids),len(sourceids),len(bodyids-sourceids),len(captions))==(328,53,275,2)
    assert (total_body,total_headers,total_menu)==(116,100,6) and len(FEchecks)==2
    assert {'DK4_MES_B105_R0023','DK4_MES_B110_R0011','DK4_MES_B121_R0019','DK4_MES_B118_R0008'}<=observed
    for sheet in sheets:assert digest(sheet['path'])==sheet['sha256']
    save(target,dict(frames=sum(r['frames'] for r in runs),initialized_runs=2,runs=runs,
        distinct_native_body_candidates=55,distinct_source_body_objects=53,distinct_body_pages=58,
        complete_body_planes=total_body,complete_header_planes=total_headers,complete_live_menu_samples=total_menu,
        offline_only_source_body_objects=275,observed_body_IDs=sorted(observed),observed_source_body_IDs=sorted(sourceids),
        unvisited_source_IDs=sorted(bodyids-sourceids),observed_caption_IDs=sorted(captions),unvisited_caption_IDs=[],
        actual_menus=1,actual_caption_strings=2,both_menu_options_andordinary_returns_observed=True,
        numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited=True,FE_continuations=FEchecks,
        both_source_owned_FE_continuation_A_andfollowing_returns_observed=True,no_extra_blank_FE_panel_observed=True,
        all_three_mixed_font_Latin_repairs_andformer_Japanese_grant_observed=True,complete_dynamic_style_objects_observed=5,
        name_headers=[dict(source_selector=s,expected_actor_ID=a,text=t) for s,a,t in sorted(headers)],
        all58_selected_pages_two_captions_andboth_host_transitions_directly_viewed=True,
        all_selected_complete_body_header_andmenu_pixel_bounds_blank_andcentering_checks_pass=True,
        complete_source_QA_hosts_return_to_resupply_andordinary_sailing=True,
        review_sheets=[dict(s,directly_viewed=True) for s in sheets],actual_gameplay=True,disclosed_initialized_fixture=True,
        existing_system_only_unlock_not_earned=True,natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        source_event_conditions_rewards_cutscene_art_andstat_effects_not_simulated=True,full_catalogue_UI_unvisited=True,
        source_role_IDs_qualified_offline_not_inferred_from_pixels=True,guide_photos=False,new_credit=0,
        registered_integration_pending=True,evidence={str(p):digest(p) for p in evidence}))
    print('PASS actual QA:53 source bodies/55 physical bodies/58 viewed pages, both options, two FE continuations, both ordinary sailing returns.')

if __name__=='__main__':main()
