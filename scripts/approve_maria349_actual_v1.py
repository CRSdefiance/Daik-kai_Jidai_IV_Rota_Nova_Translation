"""Bind directly viewed initialized captures to exact, limited Maria349 gameplay coverage."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B275_B285_clean_20261110')
NAMES=['Maria349_smuggler_informant','Maria349_impostor_reveal','Maria349_forest_desert']

def main():
    output=ROOT/'gameplay_review_v1.json';assert not output.exists()
    source=load(ROOT/'formatting_v1/formatting_input.json');native=load(ROOT/'final_native_v1.json')
    byid={r['id']:r for r in native['records']};body_ids=set(byid)
    menus=load(ROOT/'menu_native_approved_v1.json');by_menu={(r['block'],r['source_command_offset']):r for r in menus['menus']}
    tp=ROOT/'transition_review_v1/receipt.json';transitions=load(tp)
    assert transitions['initialized_QA_hosts_reach_resupply_departure_andfinal_sailing']
    evidence={str(tp):digest(tp),str(Path(__file__)):digest(Path(__file__))}
    sheets=[];runs=[];pages=[];headers=[];turns=[];FE_returns=[];states={};observed=set();captions=set();seenmenus=set()
    for index,name in enumerate(NAMES):
        paths=[ROOT/f'display_fixtures_v1/{name}_fixture.json',ROOT/f'display_run_menu{index}_v1/terminal.json',
            ROOT/f'display_pixels_menu{index}_v1/focused_actual_pixels.json',ROOT/f'actual_sheets_menu{index}_v1/receipt.json']
        fixture,terminal,pixel,receipt=map(load,paths)
        assert terminal['terminal'] and terminal['frames']==pixel['frames']==fixture['frames']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert pixel['actual_gameplay'] and pixel['disclosed_initialized_fixture'] and pixel['existing_system_only_unlock_not_earned']
        assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware','complete_scene_commands_retained'])
        for p,h in pixel['evidence'].items():assert digest(p)==h
        assert receipt['actual_pixel_proof_sha256']==digest(paths[2]) and receipt['actual_dialogue_pages']==pixel['selected_pages']
        assert len(receipt['bottom_screen_sheets'])==[5,7,5][index]
        viewed=[*receipt['bottom_screen_sheets'],transitions['runs'][index]['review_sheet']]
        if index==2:
            mp=ROOT/'actual_menus2_v1/menu_actual_pixels.json';actualmenu=load(mp);paths.append(mp)
            assert actualmenu['frames']==fixture['frames']
            assert actualmenu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
            assert actualmenu['complete_contiguous_cursor_band_and_remaining_paper_background_checked']
            assert actualmenu['ordinary_A_return_to_next_fixture_speech_observed']
            viewed.append(actualmenu['review_sheet'])
            for row in actualmenu['menus']:
                key=(row['block'],row['clean_source_command_offset']);assert key in by_menu
                seenmenus.add(key);captions.update(by_menu[key]['record_ids']);states.setdefault(key,set()).update(row['observed_selected_options'])
        else:assert fixture['menus']==[]
        # Each exact listed sheet was opened and read directly before approval.
        for sheet in viewed:
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
        headers.extend(pixel['headers']);runs.append(dict(index=index,frames=terminal['frames'],source_body_objects=pixel['selected_utterances'],observed_pages=pixel['selected_pages'],actual_proof=str(paths[2])))
        evidence.update({str(p):digest(p) for p in paths})
    unique={(r['id'],r['page']) for r in pages};styles={r['id'] for r in source['records'] if r.get('native_object_kind')=='4100-style-alternative'}&observed
    FE_ids={ident for ident in observed if byid[ident]['kind']=='system-FE'}
    assert (len(observed),len(pages),len(unique),sum(r['frames'] for r in runs))==(191,193,193,77043)
    assert len(body_ids-observed)==150 and len(styles)==12 and len(sheets)==21
    assert (len(seenmenus),len(captions),len(turns))==(3,8,2)
    assert states=={(281,758):{0,1},(283,682):{0,1},(285,814):{0,1}}
    assert {r['id'] for r in turns}=={'DK4_MES_B275_R0128','DK4_MES_B277_R0109'}
    assert {'DK4_MES_B275_R0151','DK4_MES_B278_R0004','DK4_MES_B278_R0178','DK4_MES_B285_R0227','DK4_MES_B285_R0333'}<=observed
    assert {129,131,139,156}<={h['expected_actor_ID'] for h in headers}
    role_source={r['id']:r for r in source['records']}
    assert {215,218}<={role_source[i]['source_selector'] for i in observed}
    assert sum(role_source[i].get('native_literal_token_counts',{}).get('FI',0) for i in observed)==7
    assert len(FE_returns)==len(FE_ids)==7
    save(output,dict(frames=77043,initialized_runs=3,runs=runs,distinct_source_body_objects=191,observed_pages_including_repeats=193,distinct_body_pages=193,
        offline_only_source_body_objects=150,observed_body_IDs=sorted(observed),observed_caption_IDs=sorted(captions),observed_style_IDs=sorted(styles),
        unvisited_source_IDs=sorted(body_ids-observed),actual_caption_strings=8,offline_only_caption_strings=0,actual_menus=3,
        menu_cursor_indices=[dict(block=k[0],source_command_offset=k[1],observed_indices=sorted(v)) for k,v in sorted(states.items())],
        observed_FE_IDs=sorted(FE_ids),native_FE_panels_observed=7,ordinary_A_FE_returns=FE_returns,two_page_transitions=turns,name_headers=headers,
        review_sheets=sheets,evidence=evidence,all_actual_body_menu_andtransition_sheets_directly_viewed=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,both_two_page_turns_andfollowing_calls_observed=True,
        former_actor_governor_priest_headers_andFI_macros_observed=True,wolf_andscorpion_roles215_218_andall_three_menu_returns_observed=True,
        all_seven_FE_panels_andfollowing_A_returns_observed=True,complete_QA_host_nonspeech_setup_cleanup_andreturn_to_sailing_observed=True,
        full_original_story_scene_control_flow_preserved=False,original_event_conditions_locations_rewards_andearned_progression_unvisited=True,
        numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited=True,natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        actual_gameplay=True,disclosed_initialized_fixture=True,existing_system_only_unlock_not_earned=True,direct_visual_review_pending=False,
        registered_integration_pending=True,new_credit=0,guide_photos=False,
        observer_reused_from='scripts/run_maria359_display_v1.py',inherited_unlock_scope_label_is_runner_version_not_source_batch=True))
    print('Approved191 actual bodies/193 pages,eight captions,twelve voice4 alternatives,two page turns,seven FE returns andthree sailing returns;150 bodies offline-only.')

if __name__=='__main__':main()
