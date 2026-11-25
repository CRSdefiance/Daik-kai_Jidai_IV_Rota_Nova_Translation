"""Seal directly viewed initialized gameplay with exact offline exclusions and menu timing."""
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')
NAMES = ['Lil269_expedition_figurehead', 'Lil269_ruins_riddle', 'Lil269_spy_capture_rewards']


def main():
    output = ROOT / 'gameplay_review_v1.json'
    assert not output.exists()
    nativepath = ROOT / 'final_native_v1.json'
    sourcepath = ROOT / 'formatting_v2/formatting_input.json'
    native, source = map(load, [nativepath, sourcepath])
    byid = {r['id']: r for r in native['records']}
    transitionspath = ROOT / 'transition_review_v1/receipt.json'
    transitions = load(transitionspath)
    assert transitions['initialized_QA_hosts_reach_resupply_andfollowing_native_tutorial']
    assert transitions['free_sailing_not_claimed']
    menus, evidence = [], {str(p): digest(p) for p in [nativepath, sourcepath, transitionspath, Path(__file__)]}
    for i in range(2):
        path = ROOT / f'actual_menus{i}_v1/menu_actual_pixels.json'
        menu = load(path)
        assert menu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert menu['ordinary_A_return_to_next_fixture_speech_observed']
        assert menu['complete_contiguous_cursor_band_and_remaining_paper_background_checked']
        assert menu['observed_each_menu_between_its_own_exact_preceding_and_following_speech']
        assert digest(menu['body_proof']) == menu['body_proof_sha256']
        menus.extend(menu['menus'])
        evidence[str(path)] = digest(path)
    menu_keys = {(m['block'], m['clean_source_command_offset']): m for m in menus}
    expected = {(250, 470): [0], (251, 270): [1, 2], (251, 1752): [1]}
    assert set(menu_keys) == set(expected)
    for key, states in expected.items():
        assert menu_keys[key]['observed_selected_options'] == states
    runs, sheets, observed, calls_all, headers, turns, FE_returns = [], [], set(), [], [], [], []
    for i, name in enumerate(NAMES):
        paths = [ROOT / f'display_fixtures_v1/{name}_fixture.json',
            ROOT / f'display_run{i}_v1/terminal.json', ROOT / f'display_pixels{i}_v1/focused_actual_pixels.json',
            ROOT / f'actual_sheets{i}_v1/receipt.json', ROOT / f'display_run{i}_v1/run_plan.json']
        fixture, terminal, pixel, receipt, plan = map(load, paths)
        assert terminal['terminal'] and terminal['frames'] == fixture['frames'] == pixel['frames']
        assert pixel['all_selected_pages_observed_in_exact_fixture_order']
        assert pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert pixel['actual_gameplay'] and pixel['disclosed_initialized_fixture']
        assert not any(pixel[k] for k in ['natural_activation', 'original_location', 'earned_chronology', 'full_route', 'hardware', 'complete_scene_commands_retained'])
        assert digest(plan['fixture']) == plan['fixture_sha256'] and not plan['existing_system_only_unlock_not_earned']
        assert fixture['QA_block_inside_original_stack_buffer'] and fixture['padded_QA_block_bytes'] <= 9216
        assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
        assert len(fixture['original_initializers']) + len(fixture['source_bound_QA_host_opening_exit']) == 41
        assert receipt['actual_pixel_proof_sha256'] == digest(paths[2])
        assert receipt['actual_dialogue_pages'] == pixel['selected_pages'] and not receipt['full_scene_sheets']
        assert len(receipt['bottom_screen_sheets']) == [5, 3, 5][i]
        ordered = [(r['id'], r['page']) for r in pixel['ordered_selected_source_calls']]
        selected = [next(s for s in pixel['body_pages'] if (s['id'], s['page']) == k) for k in ordered]
        for offset, sheet in enumerate(receipt['bottom_screen_sheets']):
            assert digest(sheet['path']) == sheet['sha256']
            part = selected[offset * 12:(offset + 1) * 12]
            assert sheet['full_original_capture_refs'] == [s['capture'] for s in part]
            with Image.open(sheet['path']) as im:
                canvas = im.convert('RGB')
                for n, sample in enumerate(part):
                    capture = sample['capture']
                    assert digest(capture['path']) == capture['PNG_sha256']
                    with Image.open(capture['path']) as raw:
                        tile = raw.convert('RGB').crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST)
                    x, y = n % 3 * 512, n // 3 * 410 + 25
                    assert canvas.crop((x, y, x + 512, y + 384)).tobytes() == tile.tobytes()
            sheets.append({**sheet, 'directly_viewed': True, 'exact_original_capture_tiles_bound': True})
        for sheet in [transitions['runs'][i]['review_sheet']]:
            assert digest(sheet['path']) == sheet['sha256']
            sheets.append({**sheet, 'directly_viewed': True})
        if i < 2:
            menu = load(ROOT / f'actual_menus{i}_v1/menu_actual_pixels.json')
            sheet = menu['review_sheet']
            assert digest(sheet['path']) == sheet['sha256']
            sheets.append({**sheet, 'directly_viewed': True})
        inputs = load(fixture['inputs'])
        assert digest(fixture['inputs']) == fixture['inputs_sha256']
        fixture_offsets = {r['id']: r['fixture_offset'] for r in fixture['selected_records']}
        calls = pixel['ordered_selected_source_calls']
        for at, call in enumerate(calls):
            ident = call['id']
            assert ident in byid
            observed.add(ident)
            calls_all.append(dict(run=i, **call))
            if at + 1 == len(calls):
                continue
            follow = calls[at + 1]
            presses = [r for r in inputs if r['buttons'] == ['A'] and call['frame'] < r['start'] <= follow['frame']]
            if ident == follow['id']:
                assert follow['page'] == call['page'] + 1 and len(presses) == 1 and presses[0]['duration'] == 16
                turns.append(dict(run=i, id=ident, from_page=call['page'], to_page=follow['page'], ordinary_A_input=presses[0]))
            elif byid[ident]['kind'] == 'system-FE':
                between = [m for m in fixture['menus'] if fixture_offsets[ident] < m['fixture_offset'] < fixture_offsets[follow['id']]]
                assert len(presses) == 1 + len(between) and all(p['duration'] == 16 for p in presses)
                FE_returns.append(dict(run=i, id=ident, following_ID=follow['id'], intervening_menus=between, ordinary_A_inputs=presses))
        for p, h in pixel['evidence'].items():
            assert digest(p) == h
        headers.extend(pixel['headers'])
        runs.append(dict(index=i, frames=terminal['frames'], source_body_objects=pixel['selected_utterances'],
            observed_pages=pixel['selected_pages'], actual_proof=str(paths[2]), run_plan=str(paths[4])))
        evidence.update({str(p): digest(p) for p in paths})
    unique = {(c['id'], c['page']) for c in calls_all}
    styles = {r['id'] for r in source['records'] if r.get('native_object_kind') == '4100-style-alternative'} & observed
    captions = {r['id'] for r in source['records'] if r['kind'] == 'typed-choice-label'}
    assert (len(observed), len(unique), len(calls_all), sum(r['frames'] for r in runs)) == (139, 141, 141, 64563)
    assert len(set(byid) - observed) == 123 and len(styles) == 2 and len(captions) == 7
    assert len(turns) == 2 and len(FE_returns) == 21 and len(sheets) == 18
    assert 'DK4_MES_B251_R0009' in {r['id'] for r in FE_returns}
    save(output, dict(frames=64563, initialized_runs=3, runs=runs, distinct_source_body_objects=139,
        observed_pages_including_repeats=141, distinct_body_pages=141, offline_only_source_body_objects=123,
        observed_body_IDs=sorted(observed), observed_caption_IDs=sorted(captions), observed_style_IDs=sorted(styles),
        unvisited_source_IDs=sorted(set(byid) - observed), actual_caption_strings=7, offline_only_caption_strings=0,
        actual_menus=3, menu_cursor_indices=[dict(block=m['block'], source_command_offset=m['clean_source_command_offset'], observed_indices=m['observed_selected_options']) for m in menus],
        ordinary_A_FE_returns=FE_returns, two_page_transitions=turns, name_headers=headers, review_sheets=sheets,
        evidence=evidence, all_actual_body_menu_andtransition_sheets_directly_viewed=True,
        all_selected_current_pages_match_current_compiled_native_planes=True,
        all_selected_two_page_turns_FE_andmenu_A_returns_observed=True,
        repaired_riddle_complete_with_normal_A_return_observed=True,
        three_choice_Right_andtwo_choice_No_cursor_andfollowing_A_return_observed=True,
        complete_QA_host_nonspeech_setup_cleanup_andfollowing_tutorial_observed=True,
        free_sailing_not_claimed=True, full_original_story_scene_control_flow_preserved=False,
        original_event_conditions_locations_rewards_andearned_progression_unvisited=True,
        numeric_modal_returns_cancellation_andoriginal_branch_outcomes_unvisited=True,
        observed_menu_inputs_follow_opening_A_pulse=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        actual_gameplay=True, disclosed_initialized_fixture=True, existing_system_only_unlock_not_earned=False,
        direct_visual_review_pending=False, registered_integration_pending=True, new_credit=0, guide_photos=False))
    print('PASS139 bodies/141 pages,2 turns,21 FE returns,3 menus and18 directly viewed sheets;123 bodies offline-only.')


if __name__ == '__main__':
    main()
