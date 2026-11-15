"""Seal reviewed native-pixel QA, keeping conditional activation explicitly unvisited."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.analyze_maria301_display_v1 import verified_existing_unlock

ROOT = Path('work/Maria_B58_B70_clean_20261109')


def main():
    out = ROOT/'gameplay_review_v1.json'
    assert not out.exists()
    native_path = ROOT/'storage_inputs_v1/native_pages.json'
    byid = {r['id']: r for r in load(native_path)['records']}
    selection_path = ROOT/'display_selection_v1.json'
    selection = load(selection_path)
    evidence, runs, sheets, full_sheets = {}, [], [], []
    observed, pages, headers = set(), set(), set()
    body_holds = header_holds = 0

    def bind(path):
        path = Path(path)
        value = digest(path)
        assert str(path) not in evidence or evidence[str(path)] == value
        evidence[str(path)] = value
        return value

    for name, expected in [('rescue', (23681, 57, 57)), ('town', (24641, 59, 59))]:
        terminal_path = ROOT/f'display_runs_v1/{name}/terminal.json'
        plan_path = terminal_path.with_name('run_plan.json')
        actual_path = ROOT/f'display_pixels_v1/{name}/focused_actual_pixels.json'
        terminal, plan, pixel = map(load, [terminal_path, plan_path, actual_path])
        fixture = load(plan['fixture'])
        assert terminal['terminal'] and (terminal['frames'], pixel['selected_utterances'], pixel['selected_pages']) == expected
        assert pixel['all_selected_pages_observed_in_exact_fixture_order']
        assert pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(pixel[k] for k in ['natural_activation', 'original_location', 'earned_chronology', 'full_route', 'hardware'])
        assert bind(plan['fixture']) == plan['fixture_sha256']
        assert fixture['padded_QA_block_bytes'] <= fixture['source_bound_QA_block_limit'] == 9216
        assert fixture['QA_block_inside_original_stack_buffer']
        assert fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
        assert len(fixture['original_initializers']) + len(fixture['source_bound_QA_host_opening_exit']) == 47
        report, observer = map(load, [terminal['report'], terminal['observer']])
        assert bind(terminal['report']) == terminal['report_sha256']
        assert bind(terminal['observer']) == terminal['observer_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert verified_existing_unlock(report)
        assert not observer['errors'] and not observer['mismatches']
        assert observer['all_host_slots_restored_and_core_file_exact']
        assert bind(fixture['research_ROM']) == fixture['research_ROM_sha256'] == report['ROM_sha256']
        for sample in pixel['body_pages']:
            display = byid[sample['id']]['complete_native_English_display']
            page = display if sample['selector'] == 254 else display['pages'][sample['page']-1]
            assert sample['native_plane_sha256'] == page['native_plane_sha256'] == bind(sample['native_plane'])
            assert bind(sample['capture']['path']) == sample['capture']['PNG_sha256']
            observed.add(sample['id'])
            pages.add((sample['id'], sample['page']))
        headers.update((h['source_selector'], h['expected_actor_ID'], h['text']) for h in pixel['headers'])
        body_holds += pixel['complete_body_planes']
        header_holds += pixel['complete_header_planes']
        compact_path = ROOT/f'display_{name}_sheets_v1/receipt.json'
        compact = load(compact_path)
        assert compact['actual_pixel_proof_sha256'] == digest(actual_path)
        assert compact['actual_dialogue_pages'] == expected[2]
        assert len(compact['bottom_screen_sheets']) == 5 and len(compact['full_scene_sheets']) == 1
        for sheet in compact['bottom_screen_sheets'] + compact['full_scene_sheets']:
            assert bind(sheet['path']) == sheet['sha256']
        sheets.extend(compact['bottom_screen_sheets'])
        full_sheets.extend(compact['full_scene_sheets'])
        for p, h in pixel['evidence'].items():
            assert bind(p) == h
        for sheet in pixel['review_sheets']:
            assert bind(sheet['path']) == sheet['sha256']
        modal = [r for r in observer['rows'] if r['kind'] == 'modal_paint']
        resupply = next(r for r in modal if r['text_CP932'] == ' Want to resupply for ６００ gold?')
        departure = next(r for r in modal if 'Departed Hangzhou.' in r['text_CP932'])
        assert pixel['ordered_selected_source_calls'][-1]['frame'] < resupply['frame'] < departure['frame'] < report['frames']
        for p in [terminal_path, plan_path, actual_path, compact_path, fixture['inputs']]:
            bind(p)
        runs.append(dict(name=name, run_plan=str(plan_path), terminal=str(terminal_path), actual=str(actual_path),
                         fixture=plan['fixture'], frames=expected[0], utterances=expected[1], pages=expected[2]))
    selected = set(selection['selected_speech_ids'])
    assert observed == selected and (len(observed), len(pages), len(sheets), body_holds, header_holds) == (116, 116, 10, 232, 214)
    required = ['DK4_MES_B59_R0056', 'DK4_MES_B61_R0105', 'DK4_MES_B61_R0023', 'DK4_MES_B70_R0034']
    assert set(required) <= observed
    menu_path = ROOT/'display_menu_pixels_v1/menu_actual_pixels.json'
    menus = load(menu_path)
    assert menus['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
    assert menus['complete_live_caption_samples'] == 4 and len(menus['menu_samples']) == 4
    assert {(m['block'], m['source_command_offset']) for m in menus['menus']} == {(60, 428), (64, 104)}
    for menu in menus['menus']:
        assert menu['observed_selected_options'] == [0] and menu['count'] == 2
        assert bind(menu['proof']) == menu['proof_sha256']
    labels = set()
    for sample in menus['menu_samples']:
        assert sample['all_complete_captions_centering_first_internal_final_glyphs_blank_guards_andbackgrounds_exact']
        assert bind(sample['capture']['path']) == sample['capture']['PNG_sha256']
        for label in sample['labels']:
            assert bind(label['native_plane']) == label['native_plane_sha256']
            labels.add((sample['source_command_offset'], label['index'], label['text']))
    assert len(labels) == 4
    assert bind(menus['review_sheet']['path']) == menus['review_sheet']['sha256']
    for key in ['fixture', 'terminal']:
        assert bind(menus[key]) == menus[key+'_sha256']
    transition_path = ROOT/'transition_review_v1/receipt.json'
    transitions = load(transition_path)
    assert transitions['both_original_host_sequences_reach_resupply_departure_andfinal_capture']
    assert len(transitions['samples']) == 6
    for sample in transitions['samples']:
        assert bind(sample['capture']['path']) == sample['capture']['PNG_sha256']
    assert bind(transitions['review_sheet']['path']) == transitions['review_sheet']['sha256']
    for p in [native_path, selection_path, menu_path, transition_path, Path(__file__)]:
        bind(p)
    save(out, dict(runs=runs, frames=48322, initialized_runs=2, distinct_source_utterances=116,
        distinct_body_pages=116, offline_only_source_utterances=183,
        unvisited_source_IDs=sorted(set(byid)-observed), reviewed_body_sheets=sheets, reviewed_full_scene_sheets=full_sheets,
        all116_selected_pages_directly_viewed=True, complete_body_timing_holds=232, complete_header_timing_holds=214,
        all_final_selected_body_planes_match_final_compiled_native_planes=True,
        both_reclaimed_single_page_paragraphs_andnext_source_returns_observed=True,
        corrected_B59_ASCII_I_andB61_normal_F_glyphs_observed=True,
        inline_FE_boy_andnamed_portrait_return_observed=True,
        ordinary_default_menu_return_to_next_fixture_speech_observed=True,
        ordinary_16frame_A_return_observed=True, observed_menu_instances=2, observed_choice_captions=4,
        menus=menus['menus'], menu_pixel_receipt=str(menu_path), reviewed_menu_sheet=menus['review_sheet'],
        numeric_modal_return_register_other_menu_indices_andcancellation_unvisited=True,
        other_returns_andall_relative_sites_proved_separately_offline=True,
        complete_original_host_nonspeech_setup_reaches_resupply_andordinary_sailing=True,
        qualified_exit_run=runs[0], transition_captures=transitions['samples'],
        reviewed_transition_sheet=transitions['review_sheet'], all_six_transition_captures_directly_viewed=True,
        name_headers=[dict(source_selector=s, expected_actor_ID=a, text=t) for s,a,t in sorted(headers)],
        no_prose_compiled_buffer_font_viewport_orengine_changes=True,
        actual_gameplay=True, disclosed_initialized_native_display_QA=True,
        natural_activation=False, original_location=False, earned_chronology=False, full_route=False, hardware=False,
        existing_system_unlock_not_earned=True, conditional_town_alternatives_not_naturally_consecutive=True,
        original_source_scene_conditions_effects_outcomes_not_simulated=True, full_catalogue_UI_unvisited=True,
        registered_integration_pending=True, new_credit=0, guide_photos=False, evidence=evidence))
    print('Sealed116 viewed pages,232 body/214 header holds,two menus andboth ordinary host exits;183 bodies offline-only.')


if __name__ == '__main__':
    main()
