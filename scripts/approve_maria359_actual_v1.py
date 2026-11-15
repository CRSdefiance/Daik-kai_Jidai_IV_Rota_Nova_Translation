"""Bind directly viewed initialized captures to exact limited Maria359 gameplay coverage."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B253_B274_clean_20261110')

def main():
    output=ROOT/'gameplay_review_v1.json';assert not output.exists()
    source=load(ROOT/'formatting_v1/formatting_input_v2.json');native=load(ROOT/'final_native_v2.json')
    byid={r['id']:r for r in native['records']};body_ids=set(byid)
    menus=load(ROOT/'menu_native_approved_v1.json');by_menu={(r['block'],r['source_command_offset']):r for r in menus['menus']}
    tp=ROOT/'transition_review_v1/receipt.json';transitions=load(tp)
    assert transitions['initialized_QA_hosts_reach_resupply_departure_andfinal_sailing']
    evidence={str(tp):digest(tp),str(Path(__file__)):digest(Path(__file__))}
    sheets=[];runs=[];pages=[];headers=[];turns=[];FE_returns=[];states={};observed=set();captions=set();seenmenus=set()
    names=['Maria359_towns_London_snake_menu0','Maria359_jungle_coin_forest_menu1','Maria359_carronade_desert_compass_menu0']
    for index,name in enumerate(names):
        paths=[ROOT/f'display_fixtures_v1/{name}_fixture.json',ROOT/f'display_run_menu{index}_v1/terminal.json',
            ROOT/f'display_pixels_menu{index}_v1/focused_actual_pixels.json',ROOT/f'actual_menus{index}_v1/menu_actual_pixels.json',
            ROOT/f'actual_sheets_menu{index}_v1/receipt.json']
        fixture,terminal,pixel,actualmenu,receipt=map(load,paths)
        assert terminal['terminal'] and terminal['frames']==pixel['frames']==actualmenu['frames']==fixture['frames']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert pixel['actual_gameplay'] and pixel['disclosed_initialized_fixture'] and pixel['existing_system_only_unlock_not_earned']
        assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware','complete_scene_commands_retained'])
        for p,h in pixel['evidence'].items():assert digest(p)==h
        assert actualmenu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert actualmenu['complete_contiguous_cursor_band_and_remaining_paper_background_checked']
        assert actualmenu['ordinary_A_return_to_next_fixture_speech_observed']
        assert receipt['actual_pixel_proof_sha256']==digest(paths[2]) and receipt['actual_dialogue_pages']==pixel['selected_pages']
        assert len(receipt['bottom_screen_sheets'])==[5,4,7][index]
        # Every listed sheet was opened and read directly before this approval.
        for sheet in [*receipt['bottom_screen_sheets'],actualmenu['review_sheet'],transitions['runs'][index]['review_sheet']]:
            assert digest(sheet['path'])==sheet['sha256'];sheets.append(dict(path=sheet['path'],sha256=sheet['sha256'],directly_viewed=True))
        calls=pixel['ordered_selected_source_calls'];inputs=load(fixture['inputs']);assert digest(fixture['inputs'])==fixture['inputs_sha256']
        for at,call in enumerate(calls):
            ident=call['id'];assert ident in body_ids;observed.add(ident);pages.append(dict(run=index,**call))
            if at+1==len(calls):continue
            follow=calls[at+1];presses=[r for r in inputs if r['buttons']==['A'] and call['frame']<r['start']<=follow['frame']]
            if follow['id']==ident:
                assert follow['page']==call['page']+1 and len(presses)==1 and presses[0]['duration']==16
                turns.append(dict(run=index,id=ident,from_page=call['page'],to_page=follow['page'],ordinary_A_input=presses[0],from_frame=call['frame'],to_frame=follow['frame']))
            if byid[ident]['kind']=='system-FE':
                assert len(presses)==1 and presses[0]['duration']==16
                FE_returns.append(dict(run=index,id=ident,following_ID=follow['id'],ordinary_A_input=presses[0],from_frame=call['frame'],to_frame=follow['frame']))
        for row in actualmenu['menus']:
            key=(row['block'],row['clean_source_command_offset']);assert key in by_menu
            seenmenus.add(key);captions.update(by_menu[key]['record_ids']);states.setdefault(key,set()).update(row['observed_selected_options'])
        headers.extend(pixel['headers']);runs.append(dict(index=index,frames=terminal['frames'],source_body_objects=pixel['selected_utterances'],observed_pages=pixel['selected_pages'],actual_proof=str(paths[2]),menu_proof=str(paths[3])))
        evidence.update({str(p):digest(p) for p in paths})
    unique={(r['id'],r['page']) for r in pages};styles={r['id'] for r in source['records'] if r.get('native_object_kind')=='4100-style-alternative'}&observed
    FE_ids={ident for ident in observed if byid[ident]['kind']=='system-FE'}
    assert (len(observed),len(pages),len(unique),sum(r['frames'] for r in runs))==(164,165,165,70803)
    assert len(body_ids-observed)==185 and len(styles)==12 and len(sheets)==22
    assert (len(seenmenus),len(captions),len(turns))==(5,10,1)
    assert states=={(267,486):{0},(259,1090):{0,1},(264,716):{0,1},(269,640):{0},(274,864):{0}}
    assert turns[0]['id']=='DK4_MES_B258_R0051' and turns[0]['to_page']==2
    cure=[r for r in pages if r['id']=='DK4_MES_B254_R0012'];assert len(cure)==1 and cure[0]['page']==1
    assert {'DK4_MES_B271_R0223','DK4_MES_B269_R0074','DK4_MES_B273_R0014','DK4_MES_B272_R0118'}<=observed
    actor18=[h for h in headers if h['expected_actor_ID']==18 and h['text']=='Charles Rochefort'];assert actor18
    pixel2=load(ROOT/'display_pixels_menu2_v1/focused_actual_pixels.json')
    actor18_capture_frames={p['frame'] for p in pixel2['body_pages'] if p['id']=='DK4_MES_B271_R0223'}
    assert actor18_capture_frames and actor18_capture_frames<={h['frame'] for h in actor18}
    assert len(FE_returns)==len(FE_ids)
    raw=ROOT/'display_capture_menu2_v1/frame_015840_cold_boot.png'
    save(output,dict(frames=70803,initialized_runs=3,runs=runs,distinct_source_body_objects=164,observed_pages_including_repeats=165,distinct_body_pages=165,
        offline_only_source_body_objects=185,observed_body_IDs=sorted(observed),observed_caption_IDs=sorted(captions),observed_style_IDs=sorted(styles),
        unvisited_source_IDs=sorted(body_ids-observed),actual_caption_strings=10,offline_only_caption_strings=0,actual_menus=5,
        menu_cursor_indices=[dict(block=k[0],source_command_offset=k[1],observed_indices=sorted(v)) for k,v in sorted(states.items())],
        observed_FE_IDs=sorted(FE_ids),native_FE_panels_observed=len(FE_ids),ordinary_A_FE_returns=FE_returns,two_page_transitions=turns,name_headers=headers,
        review_sheets=sheets,individual_raw_capture_directly_viewed=dict(path=str(raw),sha256=digest(raw)),evidence=evidence,
        all_actual_body_menu_andtransition_sheets_directly_viewed=True,all_selected_current_pages_match_current_compiled_native_planes=True,
        London_two_page_turn_andfollowing_call_observed=True,cure_complete_on_one_page_observed=True,
        actor18_B271R223_header_andall_five_menu_returns_observed=True,complete_QA_host_nonspeech_setup_cleanup_andreturn_to_sailing_observed=True,
        full_original_story_scene_control_flow_preserved=False,original_event_conditions_locations_rewards_andearned_progression_unvisited=True,
        numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited=True,natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        actual_gameplay=True,disclosed_initialized_fixture=True,existing_system_only_unlock_not_earned=True,direct_visual_review_pending=False,
        registered_integration_pending=True,new_credit=0,guide_photos=False))
    print('Approved164 actual bodies/165 pages,10 captions,12 voice4 alternatives,one page turn andthree sailing returns;',len(FE_ids),'FE returns;185 bodies offline-only.')

if __name__=='__main__':main()
