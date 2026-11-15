"""Record directly viewed initialized captures and exact limited gameplay coverage."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B176_B195_clean_20261110')


def main():
    output = ROOT/'gameplay_review_v1.json'
    assert not output.exists()
    source = load(ROOT/'formatting_v1/formatting_input.json')
    native = load(ROOT/'final_native_v1.json')
    native_by_id = {r['id']:r for r in native['records']}
    body_ids = set(native_by_id)
    menus = load(ROOT/'menu_native_approved_v1.json')
    by_menu = {(r['block'], r['source_command_offset']):r for r in menus['menus']}
    transition_path = ROOT/'transition_review_v1/receipt.json'
    transitions = load(transition_path)
    assert transitions['initialized_QA_hosts_reach_resupply_departure_andfinal_sailing']
    evidence = {str(transition_path):digest(transition_path), str(Path(__file__)):digest(Path(__file__))}
    sheets, runs, pages, headers, page_turns, FE_returns = [], [], [], [], [], []
    observed_menus, observed_captions, observed_bodies = set(), set(), set()
    states = {}
    names = ['Maria305_random_trade_menu0', 'Maria305_letters_refusal_menu1', 'Maria305_armor_glyphs_menu2']
    for index, name in enumerate(names):
        fixture_path = ROOT/f'display_fixtures_v1/{name}_fixture.json'
        terminal_path = ROOT/f'display_run_menu{index}_v1/terminal.json'
        pixel_path = ROOT/f'display_pixels_menu{index}_v1/focused_actual_pixels.json'
        menu_path = ROOT/f'actual_menus{index}_v1/menu_actual_pixels.json'
        sheet_path = ROOT/f'actual_sheets_menu{index}_v1/receipt.json'
        fixture, terminal, pixel, actual_menu, receipt = map(load, [fixture_path, terminal_path, pixel_path, menu_path, sheet_path])
        assert terminal['terminal'] and terminal['frames'] == pixel['frames'] == actual_menu['frames'] == fixture['frames']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order']
        assert pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert pixel['actual_gameplay'] and pixel['disclosed_initialized_fixture'] and pixel['existing_system_only_unlock_not_earned']
        assert not any(pixel[k] for k in ['natural_activation', 'original_location', 'earned_chronology', 'full_route', 'hardware', 'complete_scene_commands_retained'])
        for p, h in pixel['evidence'].items():
            assert digest(p) == h
        assert actual_menu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert actual_menu['complete_contiguous_cursor_band_and_remaining_paper_background_checked']
        assert actual_menu['ordinary_A_return_to_next_fixture_speech_observed']
        assert receipt['actual_pixel_proof_sha256'] == digest(pixel_path)
        assert receipt['actual_dialogue_pages'] == pixel['selected_pages']
        assert len(receipt['bottom_screen_sheets']) == [7, 3, 3][index]
        # These exact sheets were opened and read through view_image in this goal turn.
        for sheet in [*receipt['bottom_screen_sheets'], actual_menu['review_sheet'], transitions['runs'][index]['review_sheet']]:
            assert digest(sheet['path']) == sheet['sha256']
            sheets.append(dict(path=sheet['path'], sha256=sheet['sha256'], directly_viewed=True))
        calls = pixel['ordered_selected_source_calls']
        inputs = load(fixture['inputs'])
        assert digest(fixture['inputs']) == fixture['inputs_sha256']
        for at, call in enumerate(calls):
            ident = call['id']
            assert ident in body_ids
            observed_bodies.add(ident)
            pages.append(dict(run=index, **call))
            if at+1 == len(calls):
                continue
            follow = calls[at+1]
            selected = [r for r in inputs if r['buttons'] == ['A'] and call['frame'] < r['start'] <= follow['frame']]
            if follow['id'] == ident:
                assert follow['page'] == call['page']+1 and len(selected) == 1 and selected[0]['duration'] == 16
                page_turns.append(dict(run=index, id=ident, from_page=call['page'], to_page=follow['page'],
                    ordinary_A_input=selected[0], from_frame=call['frame'], to_frame=follow['frame']))
            if native_by_id[ident]['kind'] == 'system-FE':
                assert len(selected) == 1 and selected[0]['duration'] == 16
                FE_returns.append(dict(run=index, id=ident, following_ID=follow['id'], ordinary_A_input=selected[0],
                    from_frame=call['frame'], to_frame=follow['frame']))
        for row in actual_menu['menus']:
            key = (row['block'], row['clean_source_command_offset'])
            assert key in by_menu
            observed_menus.add(key)
            observed_captions.update(by_menu[key]['record_ids'])
            states.setdefault(key, set()).update(row['observed_selected_options'])
        headers.extend(pixel['headers'])
        runs.append(dict(index=index, frames=terminal['frames'], source_body_objects=pixel['selected_utterances'],
            observed_pages=pixel['selected_pages'], actual_proof=str(pixel_path), menu_proof=str(menu_path)))
        for p in [fixture_path, terminal_path, pixel_path, menu_path, sheet_path]:
            evidence[str(p)] = digest(p)
    unique_pages = {(r['id'], r['page']) for r in pages}
    observed_style_ids = {r['id'] for r in source['records'] if r.get('native_object_kind') == '4100-style-alternative'} & observed_bodies
    FE_ids = {ident for ident in observed_bodies if native_by_id[ident]['kind'] == 'system-FE'}
    assert (len(observed_bodies), len(pages), len(unique_pages), sum(r['frames'] for r in runs)) == (127, 135, 132, 63843)
    assert len(body_ids-observed_bodies) == 167 and len(observed_style_ids) == 3
    assert (len(observed_menus), len(observed_captions), len(page_turns)) == (3, 7, 5)
    assert states[(185, 242)] == {0, 1, 2} and states[(179, 990)] == {0, 1} and states[(179, 818)] == {0}
    assert {'DK4_MES_B177_R0066', 'DK4_MES_B188_R0047', 'DK4_MES_B185_R0071', 'DK4_MES_B195_R0004'} <= observed_bodies
    assert len(FE_returns) == len(FE_ids)
    save(output, dict(frames=63843, initialized_runs=3, runs=runs,
        distinct_source_body_objects=127, observed_pages_including_repeats=135, distinct_body_pages=132,
        offline_only_source_body_objects=167, observed_body_IDs=sorted(observed_bodies),
        observed_caption_IDs=sorted(observed_captions), observed_style_IDs=sorted(observed_style_ids),
        unvisited_source_IDs=sorted(body_ids-observed_bodies), actual_caption_strings=7, offline_only_caption_strings=4,
        actual_menus=3, menu_cursor_indices=[dict(block=k[0], source_command_offset=k[1], observed_indices=sorted(v)) for k,v in sorted(states.items())],
        observed_FE_IDs=sorted(FE_ids), native_FE_panels_observed=len(FE_ids), ordinary_A_FE_returns=FE_returns,
        two_page_transitions=page_turns, name_headers=headers, review_sheets=sheets, evidence=evidence,
        all135_actual_pages_seven_captions_andthree_host_transitions_directly_viewed=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,
        all_five_two_page_turns_andfollowing_calls_observed=True,
        all_three_style_objects_current_voice4_observed_other19_physical_alternatives_offline_only=True,
        repaired_B177_FE_panel_complete_andnormal_A_return_observed=True,
        both_fullwidth_I_replacements_original_FA_andGuan_Yu_translation_observed=True,
        parrot_complete_echo_exchange_andEmilio_first_person_replies_observed=True,
        both_letter_page_turns_signatures_andSailor_headers_observed=True,
        complete_QA_host_nonspeech_setup_cleanup_andreturn_to_sailing_observed=True,
        full_original_story_scene_control_flow_preserved=False,
        original_event_conditions_locations_rewards_andearned_progression_unvisited=True,
        numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        actual_gameplay=True, disclosed_initialized_fixture=True, existing_system_only_unlock_not_earned=True,
        contextual_layout_retentions=[dict(id='DK4_MES_B182_R0026',
            reason='Retain the automatic short formal opening: the next complete opening phrase is36 ASCII cells, exceeding this indented35-cell row. Full prose, bane of Tokugawa and leader of Japan remain intact within two pages; forcing joins worsens the boundary. This is not an authored dramatic break.')],
        direct_visual_review_pending=False, registered_integration_pending=True, new_credit=0, guide_photos=False))
    print('Approved127 actual bodies/132 unique pages/135 observed pages,7 captions,5 page turns and3 sailing returns;167 bodies offline-only.')


if __name__ == '__main__':
    main()
