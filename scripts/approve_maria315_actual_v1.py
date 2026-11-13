"""Bind viewed initialized captures to exact and explicitly limited Maria315 coverage."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B286_B302_clean_20261110')
NAMES = ['Maria315_Rafael_incense_armor', 'Maria315_fog_cave_exploration',
         'Maria315_monk_ghost_guardian', 'Maria315_sextant_Lil_alchemy']


def main():
    output = ROOT/'gameplay_review_v1.json'
    assert not output.exists()
    source = load(ROOT/'formatting_v1/formatting_input.json')
    native = load(ROOT/'final_native_v1.json')
    byid = {r['id']: r for r in native['records']}
    body_ids = set(byid)
    menus = load(ROOT/'menu_native_approved_v1.json')
    by_menu = {(r['block'], r['source_command_offset']): r for r in menus['menus']}
    tp = ROOT/'transition_review_v1/receipt.json'
    transitions = load(tp)
    assert transitions['initialized_QA_hosts_reach_resupply_departure_andfinal_sailing']
    evidence = {str(tp): digest(tp), str(Path(__file__)): digest(Path(__file__))}
    sheets, runs, pages, headers, turns, FE_returns = [], [], [], [], [], []
    observed, captions, seenmenus = set(), set(), set()
    states = {}
    for index, name in enumerate(NAMES):
        paths = [ROOT/f'display_fixtures_v1/{name}_fixture.json',
            ROOT/f'display_run_menu{index}_v1/terminal.json',
            ROOT/f'display_pixels_menu{index}_v1/focused_actual_pixels.json',
            ROOT/f'actual_sheets_menu{index}_v1/receipt.json']
        fixture, terminal, pixel, receipt = map(load, paths)
        assert terminal['terminal'] and terminal['frames'] == pixel['frames'] == fixture['frames']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order']
        assert pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert pixel['actual_gameplay'] and pixel['disclosed_initialized_fixture'] and pixel['existing_system_only_unlock_not_earned']
        assert not any(pixel[k] for k in ['natural_activation', 'original_location', 'earned_chronology', 'full_route', 'hardware', 'complete_scene_commands_retained'])
        for p, h in pixel['evidence'].items():
            assert digest(p) == h
        assert receipt['actual_pixel_proof_sha256'] == digest(paths[2])
        assert receipt['actual_dialogue_pages'] == pixel['selected_pages']
        assert len(receipt['bottom_screen_sheets']) == [4, 5, 7, 4][index]
        viewed = [*receipt['bottom_screen_sheets'], *receipt['full_scene_sheets'], transitions['runs'][index]['review_sheet']]
        if index == 1:
            mp = ROOT/'actual_menus1_v2/menu_actual_pixels.json'
            actualmenu = load(mp)
            paths.append(mp)
            assert actualmenu['frames'] == fixture['frames']
            assert actualmenu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
            assert actualmenu['complete_contiguous_cursor_band_and_remaining_paper_background_checked']
            assert actualmenu['ordinary_A_return_to_next_fixture_speech_observed']
            viewed.append(actualmenu['review_sheet'])
            for row in actualmenu['menus']:
                key = (row['block'], row['clean_source_command_offset'])
                assert key in by_menu
                seenmenus.add(key)
                captions.update(by_menu[key]['record_ids'])
                states.setdefault(key, set()).update(row['observed_selected_options'])
        else:
            assert fixture['menus'] == []
        for sheet in viewed:
            assert digest(sheet['path']) == sheet['sha256']
            sheets.append(dict(path=sheet['path'], sha256=sheet['sha256'], directly_viewed=True))
        calls = pixel['ordered_selected_source_calls']
        inputs = load(fixture['inputs'])
        assert digest(fixture['inputs']) == fixture['inputs_sha256']
        for at, call in enumerate(calls):
            ident = call['id']
            assert ident in body_ids
            observed.add(ident)
            pages.append(dict(run=index, **call))
            if at+1 == len(calls):
                continue
            follow = calls[at+1]
            presses = [r for r in inputs if r['buttons'] == ['A'] and call['frame'] < r['start'] <= follow['frame']]
            if follow['id'] == ident:
                assert follow['page'] == call['page']+1 and len(presses) == 1 and presses[0]['duration'] == 16
                turns.append(dict(run=index, id=ident, from_page=call['page'], to_page=follow['page']))
            if byid[ident]['kind'] == 'system-FE':
                assert len(presses) == 1 and presses[0]['duration'] == 16
                FE_returns.append(dict(run=index, id=ident, following_ID=follow['id'], ordinary_A_input=presses[0],
                    from_frame=call['frame'], to_frame=follow['frame']))
        headers.extend(pixel['headers'])
        runs.append(dict(index=index, frames=terminal['frames'], source_body_objects=pixel['selected_utterances'],
            observed_pages=pixel['selected_pages'], actual_proof=str(paths[2])))
        evidence.update({str(p): digest(p) for p in paths})
    unique = {(r['id'], r['page']) for r in pages}
    styles = {r['id'] for r in source['records'] if r.get('native_object_kind') == '4100-style-alternative'} & observed
    FE_ids = {ident for ident in observed if byid[ident]['kind'] == 'system-FE'}
    assert (len(observed), len(pages), len(unique), sum(r['frames'] for r in runs)) == (213, 213, 213, 91844)
    assert len(body_ids-observed) == 96 and len(styles) == 17 and len(sheets) == 28
    assert (len(seenmenus), len(captions), len(turns)) == (3, 6, 0)
    assert states == {(291, 674): {0, 1}, (291, 938): {0, 1}, (292, 770): {0, 1}}
    assert all(r['expected_native_pages'] == 1 for r in load(ROOT/'plan_v5/automatic_plans.json')['records'])
    required = {'DK4_MES_B286_R0029', 'DK4_MES_B286_R0042', 'DK4_MES_B302_R0038', 'DK4_MES_B302_R0057',
        'DK4_MES_B295_R0004', 'DK4_MES_B298_R0049', 'DK4_MES_B300_R0013'}
    assert required <= observed
    assert {0, 2, 3, 10, 18, 22, 135, 147, 156, 161, 179, 204, 206} == {h['expected_actor_ID'] for h in headers}
    source_byid = {r['id']: r for r in source['records']}
    assert sum(source_byid[i].get('native_literal_token_counts', {}).get('FI', 0) for i in observed) == 2
    assert sum(source_byid[i].get('native_literal_token_counts', {}).get('FA', 0) for i in observed) == 1
    assert len(FE_returns) == len(FE_ids) == 13
    raw = ROOT/'display_capture_menu2_v1/frame_018000_cold_boot.png'
    evidence[str(raw)] = digest(raw)
    save(output, dict(frames=91844, initialized_runs=4, runs=runs, distinct_source_body_objects=213,
        observed_pages_including_repeats=213, distinct_body_pages=213, offline_only_source_body_objects=96,
        observed_body_IDs=sorted(observed), observed_caption_IDs=sorted(captions), observed_style_IDs=sorted(styles),
        unvisited_source_IDs=sorted(body_ids-observed), actual_caption_strings=6, offline_only_caption_strings=0, actual_menus=3,
        menu_cursor_indices=[dict(block=k[0], source_command_offset=k[1], observed_indices=sorted(v)) for k, v in sorted(states.items())],
        observed_FE_IDs=sorted(FE_ids), native_FE_panels_observed=13, ordinary_A_FE_returns=FE_returns,
        two_page_transitions=turns, name_headers=headers, review_sheets=sheets, evidence=evidence,
        all_actual_body_menu_andtransition_sheets_directly_viewed=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,
        original_Rafael0_Lil2_headers_corrected_I_original_FA_andboth_FI_macros_observed=True,
        all17_effective_voice4_objects_andall_three_menu_returns_observed=True,
        all13_FE_panels_andfollowing_A_returns_observed=True,
        conqueror_warning_complete_on_one_page_andfollowing_call_observed=True,
        all_changed_text_single_page_no_new_multipage_behavior=True,
        complete_QA_host_nonspeech_setup_cleanup_andreturn_to_sailing_observed=True,
        original_unchanged_sailing_sharks_message_seen_without_new_editorial_credit=True,
        full_original_story_scene_control_flow_preserved=False,
        original_event_conditions_locations_rewards_andearned_progression_unvisited=True,
        numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        actual_gameplay=True, disclosed_initialized_fixture=True, existing_system_only_unlock_not_earned=True,
        direct_visual_review_pending=False, registered_integration_pending=True, new_credit=0, guide_photos=False,
        observer_reused_from='scripts/run_maria359_display_v1.py',
        inherited_unlock_scope_label_is_runner_version_not_source_batch=True,
        first_menu_analysis_wrong_summary_input_rejected_then_correct_approved_receipt_used=True))
    print('PASS213 actual bodies/pages,six captions,17 effective styles,13 FE returns,four sailing returns;96 bodies offline-only.')


if __name__ == '__main__':
    main()
