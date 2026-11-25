"""Record directly viewed, pixel-bound Lil gameplay with exact offline exclusions."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Lil382_residual_A_clean_20261110')
NAMES=['Lil382_Aziza','Lil382_cross_story_letters','Lil382_rose_scam_figurehead']


def main():
    out=ROOT/'gameplay_review_v1.json';assert not out.exists()
    native=load(ROOT/'final_native_v1.json');byid={r['id']:r for r in native['records']}
    menus=load(ROOT/'menu_native_approved_v1.json');live=load(ROOT/'actual_menus2_bound_v1.json')
    transition=load(ROOT/'transition_review_v1/receipt.json')
    assert transition['initialized_QA_hosts_reach_resupply_andfollowing_native_tutorial']
    assert live['ordinary_A_return_to_next_fixture_speech_observed']
    assert live['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert {(m['block'],m['source_command_offset']) for m in live['menus']}=={(239,470),(242,680)}
    assert all(m['observed_selected_options']==[0] for m in live['menus'])
    evidence={str(p):digest(p) for p in [ROOT/'final_native_v1.json',ROOT/'menu_native_approved_v1.json',ROOT/'actual_menus2_bound_v1.json',ROOT/'transition_review_v1/receipt.json',Path(__file__)]}
    runs=[];sheets=[];observed=set();pages=[];headers=[];turns=[];FE_returns=[]
    for index,name in enumerate(NAMES):
        paths=[ROOT/f'display_fixtures_v1/{name}_fixture.json',ROOT/f'display_run{index}_v1/terminal.json',
               ROOT/f'display_pixels{index}_v1/focused_actual_pixels.json',ROOT/f'actual_sheets{index}_v1/receipt.json',
               ROOT/f'display_run{index}_v1/run_plan.json']
        fixture,terminal,pixel,receipt,plan=map(load,paths)
        assert terminal['terminal'] and terminal['frames']==fixture['frames']==pixel['frames']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order'] and pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert pixel['actual_gameplay'] and pixel['disclosed_initialized_fixture']
        assert not any(pixel[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware','complete_scene_commands_retained'])
        assert receipt['actual_pixel_proof_sha256']==digest(paths[2]) and receipt['actual_dialogue_pages']==pixel['selected_pages']
        assert digest(plan['fixture'])==plan['fixture_sha256'] and not plan['existing_system_only_unlock_not_earned']
        for p,h in pixel['evidence'].items():assert digest(p)==h
        viewed=[*receipt['bottom_screen_sheets'],transition['runs'][index]['review_sheet']]
        assert not receipt['full_scene_sheets'] and len(receipt['bottom_screen_sheets'])==[7,5,8][index]
        if index==2:viewed.append(live['review_sheet'])
        for sheet in viewed:
            assert digest(sheet['path'])==sheet['sha256'];sheets.append({**sheet,'directly_viewed':True})
        calls=pixel['ordered_selected_source_calls'];inputs=load(fixture['inputs'])
        assert digest(fixture['inputs'])==fixture['inputs_sha256']
        for at,call in enumerate(calls):
            ident=call['id'];assert ident in byid;observed.add(ident);pages.append(dict(run=index,**call))
            if at+1==len(calls):continue
            follow=calls[at+1];presses=[r for r in inputs if r['buttons']==['A'] and call['frame']<r['start']<=follow['frame']]
            if follow['id']==ident:
                assert follow['page']==call['page']+1 and len(presses)==1 and presses[0]['duration']==16
                turns.append(dict(run=index,id=ident,from_page=call['page'],to_page=follow['page'],ordinary_A_input=presses[0]))
            if byid[ident]['kind']=='system-FE':
                assert len(presses)==1 and presses[0]['duration']==16
                FE_returns.append(dict(run=index,id=ident,following_ID=follow['id'],ordinary_A_input=presses[0]))
        headers.extend(pixel['headers'])
        runs.append(dict(index=index,frames=terminal['frames'],source_body_objects=pixel['selected_utterances'],observed_pages=pixel['selected_pages'],actual_proof=str(paths[2]),run_plan=str(paths[4])))
        evidence.update({str(p):digest(p) for p in paths})
    unique={(p['id'],p['page']) for p in pages}
    styleids={i for i in observed if byid[i].get('native_object_kind')=='4100-style-alternative'}
    # The native record schema identifies styles in the source manuscript.
    source=load(ROOT/'formatting_v1/formatting_input.json')
    styleids={r['id'] for r in source['records'] if r.get('native_object_kind')=='4100-style-alternative'}&observed
    captions={i for m in menus['menus'] for i in m['record_ids']}
    assert (len(observed),len(pages),len(unique),sum(r['frames'] for r in runs))==(211,217,217,82563)
    assert len(set(byid)-observed)==167 and len(styleids)==2 and len(captions)==4
    assert len(turns)==6 and len(FE_returns)==2 and len(sheets)==24
    assert {m['block'] for m in live['menus']}=={239,242}
    save(out,dict(frames=82563,initialized_runs=3,runs=runs,distinct_source_body_objects=211,
        observed_pages_including_repeats=217,distinct_body_pages=217,offline_only_source_body_objects=167,
        observed_body_IDs=sorted(observed),observed_caption_IDs=sorted(captions),observed_style_IDs=sorted(styleids),
        unvisited_source_IDs=sorted(set(byid)-observed),actual_caption_strings=4,offline_only_caption_strings=0,
        actual_menus=2,menu_cursor_indices=[dict(block=m['block'],source_command_offset=m['source_command_offset'],observed_indices=m['observed_selected_options']) for m in live['menus']],
        observed_FE_IDs=[r['id'] for r in FE_returns],ordinary_A_FE_returns=FE_returns,two_page_transitions=turns,
        name_headers=headers,review_sheets=sheets,evidence=evidence,
        all_actual_body_menu_andtransition_sheets_directly_viewed=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,
        all_selected_two_page_turns_FE_andmenu_A_returns_observed=True,
        complete_QA_host_nonspeech_setup_cleanup_andfollowing_tutorial_observed=True,
        free_sailing_not_claimed=True,full_original_story_scene_control_flow_preserved=False,
        original_event_conditions_locations_rewards_andearned_progression_unvisited=True,
        numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited=True,
        requested_DOWN_inputs_preceded_menu_open_actual_cursor_index0_only=True,
        selection_purpose_Frozen_Rose_notice_not_copied_B241_is_offline_only=True,
        Frozen_Rose_handover_andthird_FE_not_claimed_gameplay=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        actual_gameplay=True,disclosed_initialized_fixture=True,existing_system_only_unlock_not_earned=False,
        direct_visual_review_pending=False,registered_integration_pending=True,new_credit=0,guide_photos=False))
    print('PASS211 bodies/217 pages,6 turns,2 FE and2 default menu returns;24 viewed sheets;167 bodies offline-only.')


if __name__=='__main__':main()
