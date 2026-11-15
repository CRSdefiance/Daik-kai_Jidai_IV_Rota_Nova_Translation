"""Seal observed Maria pages and menu return; disclose the two focused host-exit probes."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

ROOT = Path('work/Maria_B0_B32_clean_20261109')
OUT = ROOT/'gameplay_review_v1.json'


def main():
    assert not OUT.exists()
    native_path = ROOT/'storage_inputs_v1/native_pages.json'
    native = load(native_path)
    byid = {r['id']: r for r in native['records']}
    evidence, runs, sheets, observed, pages, headers = {}, [], [], set(), set(), set()

    def bind(path):
        path = Path(path)
        value = digest(path)
        assert str(path) not in evidence or evidence[str(path)] == value
        evidence[str(path)] = value
        return value

    for run, actual, expected in [
        ('display_run_v1', 'display_pixels_v1', (28241, 92, 96)),
        ('display_exit_run_v1', 'display_exit_pixels_v1', (5441, 2, 2)),
        ('display_exit_run_v2', 'display_exit_pixels_v2', (9001, 2, 2)),
    ]:
        terminal_path = ROOT/run/'terminal.json'
        actual_path = ROOT/actual/'focused_actual_pixels.json'
        terminal, pixel = map(load, [terminal_path, actual_path])
        plan_path = ROOT/run/'run_plan.json'
        plan = load(plan_path)
        assert digest(plan['fixture']) == plan['fixture_sha256']
        fixture = load(plan['fixture'])
        assert terminal['terminal'] and (terminal['frames'], pixel['selected_utterances'], pixel['selected_pages']) == expected
        assert pixel['all_selected_pages_observed_in_exact_fixture_order']
        assert pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(pixel[k] for k in ['natural_activation', 'original_location', 'earned_chronology', 'full_route', 'hardware'])
        assert fixture['padded_QA_block_bytes'] <= fixture['source_bound_QA_block_limit'] == 9216
        assert fixture['QA_block_inside_original_stack_buffer']
        report, observer = map(load, [terminal['report'], terminal['observer']])
        assert digest(terminal['report']) == terminal['report_sha256']
        assert digest(terminal['observer']) == terminal['observer_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert verified_existing_unlock(report)
        assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
        assert digest(fixture['research_ROM']) == fixture['research_ROM_sha256'] == report['ROM_sha256']
        for sample in pixel['body_pages']:
            page = byid[sample['id']]['complete_native_English_display']['pages'][sample['page']-1]
            assert sample['native_plane_sha256'] == page['native_plane_sha256'] == digest(sample['native_plane'])
            observed.add(sample['id'])
            pages.add((sample['id'], sample['page']))
        headers.update((h['source_selector'], h['expected_actor_ID'], h['text']) for h in pixel['headers'])
        for path, expected_hash in pixel['evidence'].items():
            assert bind(path) == expected_hash
        if actual != 'display_pixels_v1':
            sheets += pixel['review_sheets']
        runs.append(dict(terminal=str(terminal_path), terminal_sha256=bind(terminal_path),
            actual=str(actual_path), actual_sha256=bind(actual_path),
            run_plan=str(plan_path), run_plan_sha256=bind(plan_path), fixture=plan['fixture'],
            fixture_sha256=bind(plan['fixture']), frames=expected[0], utterances=expected[1], pages=expected[2],
            complete_body_holds=pixel['complete_body_planes'], complete_header_holds=pixel['complete_header_planes']))
        for path in [terminal['report'], terminal['observer'], fixture['inputs']]:
            bind(path)
    assert (len(observed), len(pages), len(headers), sum(r['frames'] for r in runs)) == (92, 96, 14, 42683)
    contact_path = ROOT/'display_contacts_v1/receipt.json'
    contact = load(contact_path)
    assert contact['actual_pixel_proof_sha256'] == digest(ROOT/'display_pixels_v1/focused_actual_pixels.json')
    assert contact['actual_dialogue_pages'] == 96 and len(contact['bottom_screen_sheets']) == 8
    sheets += contact['bottom_screen_sheets'] + contact['full_scene_sheets']
    menu_path = ROOT/'display_menu_v1/menu_actual_pixels.json'
    menu = load(menu_path)
    assert menu['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert len(menu['menus']) == 1
    selected_menu = menu['menus'][0]
    assert (selected_menu['block'], selected_menu['source_command_offset'], selected_menu['count'], selected_menu['observed_selected_options']) == (29, 304, 2, [0])
    assert selected_menu['complete_live_samples'] == len(menu['menu_samples']) == 2
    broad_fixture = load(runs[0]['fixture'])
    broad = load(runs[0]['actual'])
    before = max(r['frame'] for r in broad['ordered_selected_source_calls'] if r['id'] == 'DK4_MES_B29_R0030')
    after = min(r['frame'] for r in broad['ordered_selected_source_calls'] if r['id'] == 'DK4_MES_B29_R0045')
    assert (before, after) == (17216, 17685)
    assert all(before < s['frame'] < after for s in menu['menu_samples'])
    visible = max(s['frame'] for s in menu['menu_samples'] if s['visible_selected_option'] == 0)
    controls = load(broad_fixture['inputs'])
    press = [r['start'] for r in controls if r['buttons'] == ['A'] and visible < r['start'] <= after]
    assert press == [17680]
    sheets.append(menu['review_sheet'])
    assert len(sheets) == 12
    for sheet in sheets:
        assert bind(sheet['path']) == sheet['sha256']
    exit_terminal = load(ROOT/'display_exit_run_v2/terminal.json')
    exit_report = load(exit_terminal['report'])
    exit_observer = load(exit_terminal['observer'])
    exit_fixture = load(runs[-1]['fixture'])
    assert exit_fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
    assert len(exit_fixture['original_initializers']) + len(exit_fixture['source_bound_QA_host_opening_exit']) == 47
    modal = [r for r in exit_observer['rows'] if r['kind'] == 'modal_paint']
    assert any(r['frame'] == 6409 and r['text_CP932'] == ' Want to resupply for ６００ gold?' for r in modal)
    assert any(r['frame'] == 7378 and 'Departed Hangzhou.' in r['text_CP932'] for r in modal)
    final = exit_report['frames_captured'][-1]
    assert final['frame'] == 9001 and bind(final['path']) == final['PNG_sha256']
    transition_captures = []
    for frame in [6480, 7440, 9001]:
        cap = next(r for r in exit_report['frames_captured'] if r['frame'] == frame)
        assert bind(cap['path']) == cap['PNG_sha256']
        transition_captures.append(cap)
    required = {'DK4_MES_B4_R0009', 'DK4_MES_B8_R0005', 'DK4_MES_B18_R0036', 'DK4_MES_B30_R0020'}
    assert all((key, 1) in pages and (key, 2) in pages for key in required)
    assert ('DK4_MES_B24_R0011', 1) in pages and ('DK4_MES_B24_R0011', 2) not in pages
    assert ('DK4_MES_B14_R0005', 1) in pages and ('SC3_B32_STYLE_8_94', 1) in pages
    for path in [native_path, contact_path, menu_path, ROOT/'representative_selection_v1.json',
        ROOT/'exit_selection_v1.json', ROOT/'exit_selection_v2.json', Path(__file__)]:
        bind(path)
    save(OUT, dict(runs=runs, frames=42683, initialized_runs=3,
        broad_display_runs=1, narrow_exit_probes=2, distinct_source_utterances=92, distinct_body_pages=96,
        ordinary_speeches_observed=91, physical_style_bodies_observed=1,
        offline_only_source_utterances=207, unvisited_source_IDs=sorted(set(byid)-observed),
        all_final_selected_body_planes_match_final_compiled_native_planes=True,
        all96_broad_pages_andboth_two_page_exit_sheets_directly_viewed=True,
        reviewed_body_sheets=sheets, all_four_two_page_transitions_observed=True,
        reclaimed_one_page_Havana_paragraph_observed=True, corrected_B14_I_glyph_observed=True,
        complete_eight_slot_style_command_default_voice4_andSailor_header_observed=True,
        other_six_physical_style_variants_andfuture_assignments_offline_only=True,
        name_headers=[dict(source_selector=s, expected_actor_ID=a, text=t) for s, a, t in sorted(headers)],
        full_catalogue_UI_unvisited=True, menu=selected_menu,
        menu_preceding_call_frame=before, menu_following_call_frame=after, ordinary_default_A_return_frame=17680,
        ordinary_default_menu_return_to_next_fixture_speech_observed=True,
        other_choice_cancel_numeric_VM_returns_andoriginal_story_branches_offline_only=True,
        original_prefix_tail_only_host_exit_not_qualified_as_town_return=True,
        complete_original_host_nonspeech_setup_variant_reaches_resupply_andordinary_sailing=True,
        qualified_exit_run=runs[-1], transition_captures=transition_captures,
        full_host_setup_andlonger_input_schedule_changed_together_no_single_cause_claim=True,
        research_fixture_adjustment_not_a_production_text_orengine_fix=True,
        no_dialogue_prose_orcompiled_body_change_from_gameplay_review=True,
        actual_gameplay=True, disclosed_initialized_native_display_QA=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        existing_system_unlock_not_earned=True, registered_integration_pending=True, new_credit=0,
        evidence=evidence))
    print('Sealed92 utterances/96 pages,14 headers,menu A return andsource-complete host exit to resupply/sailing;207 bodies offline-only.')


if __name__ == '__main__':
    main()
