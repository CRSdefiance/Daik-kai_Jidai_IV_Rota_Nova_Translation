"""Seal directly viewed actual pages, normal controller returns and honest unvisited scope."""
from pathlib import Path
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock


def main():
    target=ROOT/'gameplay_review_v1.json';assert not target.exists()
    rebuiltpath=ROOT/'reconstruction_v1/reconstruction.json';rebuilt=load(rebuiltpath);doc=load(rebuilt['manuscript'])
    bodyids={r['id'] for r in doc['records'] if r['kind']!='typed-choice-label'}
    captions={r['id'] for r in doc['records'] if r['kind']=='typed-choice-label'}
    native={r['id']:r for r in load(rebuilt['native'])['records']}
    selectionpath=ROOT/'display_selection_v1.json';selection=load(selectionpath)
    transitionpath=ROOT/'transition_review_v1/receipt.json';transitions=load(transitionpath)
    assert transitions['source_complete_hosts_reach_resupply_departure_andfinal_sailing']
    evidence=[rebuiltpath,Path(rebuilt['native']),selectionpath,transitionpath,Path(__file__)]
    observed=set();pages_seen=set();headers=set();sheets=[];runs=[];tutorial=[];FEchecks=[];returns=[]
    totals=[0,0,0]
    for choice,frames,utterances,pages,headerplanes in [(0,22241,46,50,88),(1,10961,3,3,6)]:
        paths={k:ROOT/f'{directory}_menu{choice}_v1/{name}' for k,directory,name in [
            ('terminal','display_run','terminal.json'),('runplan','display_run','run_plan.json'),
            ('pixels','display_pixels','focused_actual_pixels.json'),('menus','menu_pixels','menu_actual_pixels.json')]}
        d={k:load(p) for k,p in paths.items()};terminal,pixel,menus=[d[k] for k in ['terminal','pixels','menus']]
        assert terminal['terminal'] and terminal['frames']==pixel['frames']==frames
        report,observer=map(load,[terminal['report'],terminal['observer']])
        assert digest(terminal['report'])==terminal['report_sha256'] and digest(terminal['observer'])==terminal['observer_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and verified_existing_unlock(report)
        assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert (pixel['selected_utterances'],pixel['selected_pages'],pixel['complete_body_planes'],pixel['complete_header_planes'])==(utterances,pages,pages*2,headerplanes)
        assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        fixturepath=Path(d['runplan']['fixture']);fixture=load(fixturepath)
        assert digest(fixturepath)==d['runplan']['fixture_sha256']
        assert digest(fixture['research_ROM'])==fixture['research_ROM_sha256']==report['ROM_sha256']
        assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
        assert len(fixture['original_initializers'])+len(fixture['source_bound_QA_host_opening_exit'])==47
        assert fixture['padded_QA_block_bytes']<=fixture['source_bound_QA_block_limit']==9216
        assert fixture['no_savestate_RAM_roster_money_RNG_eventflag_orcondition_result_override']
        controls=load(fixture['inputs']);assert digest(fixture['inputs'])==fixture['inputs_sha256']
        for sample in pixel['body_pages']:
            display=native[sample['id']]['complete_native_English_display']
            plane=display if sample['selector']==254 else display['pages'][sample['page']-1]
            assert digest(sample['native_plane'])==sample['native_plane_sha256']==plane['native_plane_sha256']
            assert digest(sample['capture']['path'])==sample['capture']['PNG_sha256']
            observed.add(sample['id']);pages_seen.add((sample['id'],sample['page']))
        headers.update((h['source_selector'],h['expected_actor_ID'],h['text']) for h in pixel['headers'])
        assert menus['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches'] and len(menus['menus'])==1
        m=menus['menus'][0];assert (m['block'],m['source_command_offset'],m['count'])==(136,356,2)
        assert m['observed_selected_options']==([0] if choice==0 else [0,1])
        assert len(menus['menu_samples'])==menus['complete_live_caption_samples']==(2 if choice==0 else 4)
        lastmenu=max(s['frame'] for s in menus['menu_samples'])
        following=next(c for c in pixel['ordered_selected_source_calls'] if c['frame']>lastmenu)
        pushes=[c for c in controls if lastmenu<c['start']<=following['frame'] and c['buttons']==['A']]
        assert len(pushes)==1 and pushes[0]['duration']==16
        returns.append(dict(choice=choice,last_complete_menu_frame=lastmenu,following=following,ordinary_A=pushes[0],numeric_return_register_not_observed=True))
        if choice==0:
            calls=pixel['ordered_selected_source_calls']
            for n,nextn in [(325,328),(335,338),(351,354),(366,369)]:
                ident=f'DK4_MES_B135_R{n:04d}';pair=[c for c in calls if c['id']==ident]
                assert [c['page'] for c in pair]==[1,2]
                following=next(c for c in calls if c['frame']>pair[-1]['frame'])
                assert following['id']==f'DK4_MES_B135_R{nextn:04d}'
                inputs=[]
                for left,right in [(pair[0],pair[1]),(pair[1],following)]:
                    pushes=[c for c in controls if left['frame']<c['start']<right['frame'] and c['buttons']==['A']]
                    assert len(pushes)==1 and pushes[0]['duration']==16;inputs.append(pushes[0])
                tutorial.append(dict(id=ident,pages=pair,following=following,ordinary_A_inputs=inputs))
            FEids={r['id'] for r in fixture['selected_records'] if r['selector']==254};assert len(FEids)==6
            for ident in sorted(FEids):
                call=next(c for c in calls if c['id']==ident)
                following=next(c for c in calls if c['frame']>call['frame'])
                FEchecks.append(dict(id=ident,call=call,following=following))
            assert next(c for c in calls if c['id']=='DK4_MES_B130_R0225')['frame']>next(c for c in calls if c['id']=='DK4_MES_B130_R0221')['frame']
            assert next(c for c in calls if c['id']=='DK4_MES_B131_R0043')['frame']>next(c for c in calls if c['id']=='DK4_MES_B131_R0039')['frame']
        else:assert dict(start=4140,duration=4,buttons=['DOWN']) in controls
        transition=next(t for t in transitions['runs'] if t['choice']==choice);assert transition['frames']==frames
        sheets.extend(pixel['review_sheets']);sheets.extend([menus['review_sheet'],transition['review_sheet']])
        totals=[a+b for a,b in zip(totals,[pixel['complete_body_planes'],pixel['complete_header_planes'],menus['complete_live_caption_samples']],strict=True)]
        runs.append(dict(choice=choice,frames=frames,physical_body_candidates=utterances,pages=pages,run_plan=str(paths['runplan'])))
        evidence.extend([*paths.values(),fixturepath,Path(terminal['report']),Path(terminal['observer']),Path(fixture['inputs'])])
    assert observed==set(selection['selected_speech_ids']) and (len(bodyids),len(observed),len(pages_seen),len(captions))==(335,48,52,2)
    assert totals==[106,94,6] and len(tutorial)==4 and len(FEchecks)==6 and len(sheets)==14
    assert {'DK4_MES_B127_R0029','DK4_MES_B128_R0080','DK4_MES_B130_R0271','DK4_MES_B135_R0294','DK4_MES_B136_R0211'}<=observed
    for sheet in sheets:assert digest(sheet['path'])==sheet['sha256']
    save(target,dict(frames=sum(r['frames'] for r in runs),initialized_runs=2,runs=runs,
        distinct_native_body_candidates=48,distinct_source_body_objects=48,distinct_body_pages=52,
        complete_body_planes=106,complete_header_planes=94,complete_live_menu_samples=6,
        offline_only_source_body_objects=287,observed_body_IDs=sorted(observed),observed_source_body_IDs=sorted(observed),
        unvisited_source_IDs=sorted(bodyids-observed),observed_caption_IDs=sorted(captions),unvisited_caption_IDs=[],
        actual_menus=1,actual_caption_strings=2,both_menu_options_andordinary_returns_observed=True,ordinary_menu_returns=returns,
        numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited=True,tutorial_transitions=tutorial,FE_panels=FEchecks,
        all_four_two_page_tutorial_A_andfollowing_returns_observed=True,all_six_FE_panels_andnamed_returns_observed=True,
        both_mixed_font_Latin_I_repairs_observed=True,Carlo_Cesare_Fernando_name_introductions_observed=True,
        name_headers=[dict(source_selector=s,expected_actor_ID=a,text=t) for s,a,t in sorted(headers)],
        all52_selected_pages_two_captions_andboth_host_transitions_directly_viewed=True,
        all_selected_complete_body_header_andmenu_pixel_bounds_blank_andcentering_checks_pass=True,
        complete_source_QA_hosts_return_to_resupply_andordinary_sailing=True,
        review_sheets=[dict(s,directly_viewed=True) for s in sheets],actual_gameplay=True,disclosed_initialized_fixture=True,
        existing_system_only_unlock_not_earned=True,natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        source_event_conditions_minigame_rewards_cutscene_art_andstat_effects_not_simulated=True,full_catalogue_UI_unvisited=True,
        guide_photos=False,new_credit=0,registered_integration_pending=True,evidence={str(p):digest(p) for p in evidence}))
    print('PASS actual QA:48 source bodies/52 viewed pages,both captions/options,four tutorial page turns,six FE panels,both sailing returns.')


if __name__=='__main__':main()
