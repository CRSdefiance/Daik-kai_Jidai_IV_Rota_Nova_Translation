"""Seal primary display coverage and one representative unchanged-host extended return."""
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil361_B283_B298_clean_20261110')


def main():
    output = ROOT / 'gameplay_review_v1.json'
    assert not output.exists()
    pages_path = ROOT / 'gameplay_pages_review_v1.json'
    pages = load(pages_path)
    assert pages['all_actual_body_andmenu_sheets_directly_viewed']
    assert pages['all_selected_current_pages_match_current_compiled_native_planes']
    assert pages['all_selected_two_page_turns_FE_andmenu_A_returns_observed']
    assert pages['repaired_R50_FE_no_blank_row_andnormal_A_return_observed']
    assert pages['three_choice_Other_andtwo_choice_Run_andWait_cursors_andfollowing_A_returns_observed']
    assert (pages['distinct_source_body_objects'], pages['distinct_body_pages'], pages['frames'], pages['initialized_runs']) == (199, 200, 64563, 3)
    assert len(pages['review_sheets']) == 21
    for p, h in pages['evidence'].items():
        assert digest(p) == h
    extension_path = ROOT / 'extended_tail_v1/extension.json'
    extension = load(extension_path)
    assert extension['original_input_prefix_exact'] and extension['ROM_all_commands_controls_setup_andexit_unchanged']
    assert extension['no_memory_save_orstate_override']
    fixture_path = ROOT / 'extended_tail_v1/fixture.json'
    terminal_path = ROOT / 'extended_run0_v1/terminal.json'
    pixel_path = ROOT / 'extended_pixels0_v1/focused_actual_pixels.json'
    plan_path = ROOT / 'extended_run0_v1/run_plan.json'
    transition_path = ROOT / 'extended_transition_review_v1/receipt.json'
    fixture, terminal, pixel, plan, transition = map(load, [fixture_path, terminal_path, pixel_path, plan_path, transition_path])
    assert terminal['terminal'] and terminal['frames'] == fixture['frames'] == pixel['frames'] == 21761
    assert pixel['all_selected_pages_observed_in_exact_fixture_order']
    assert pixel['all_complete_native_body_andheader_planes_andblank_guards_match']
    assert digest(plan['fixture']) == plan['fixture_sha256']
    assert not plan['existing_system_only_unlock_not_earned']
    original_fixture = load(extension['original_fixture'])
    assert digest(extension['original_fixture']) == extension['original_fixture_sha256']
    assert all(fixture[k] == v for k, v in original_fixture.items() if k not in ['inputs', 'inputs_sha256', 'frames'])
    original_inputs, extended_inputs = map(load, [original_fixture['inputs'], fixture['inputs']])
    assert extended_inputs[:len(original_inputs)] == original_inputs
    assert all(r['buttons'] == ['A'] and r['duration'] == 16 for r in extended_inputs[len(original_inputs):])
    original_pixels = load(ROOT / 'display_pixels0_v1/focused_actual_pixels.json')
    assert pixel['ordered_selected_source_calls'] == original_pixels['ordered_selected_source_calls']
    reused = []
    for call in pixel['ordered_selected_source_calls']:
        key = call['id'], call['page']
        old = next(r for r in original_pixels['body_pages'] if (r['id'], r['page']) == key)
        fresh = next(r for r in pixel['body_pages'] if (r['id'], r['page']) == key)
        assert digest(old['capture']['path']) == old['capture']['PNG_sha256']
        assert digest(fresh['capture']['path']) == fresh['capture']['PNG_sha256']
        assert fresh['capture']['PNG_sha256'] == old['capture']['PNG_sha256']
        reused.append(dict(id=key[0], page=key[1], original=old['capture'], extended=fresh['capture'],
            exact_previous_direct_visual_capture_reused=True))
    assert len(reused) == 42
    assert transition['initialized_QA_hosts_reach_resupply_andfollowing_native_tutorial']
    assert transition['free_sailing_not_claimed'] and len(transition['runs']) == 1
    run = transition['runs'][0]
    sheet = run['review_sheet']
    assert digest(sheet['path']) == sheet['sha256']
    with Image.open(sheet['path']) as image:
        canvas = image.convert('RGB')
        for i, sample in enumerate(run['samples']):
            capture = sample['capture']
            assert digest(capture['path']) == capture['PNG_sha256']
            with Image.open(capture['path']) as raw:
                expected = raw.convert('RGB').resize((512, 768), Image.Resampling.NEAREST)
            assert canvas.crop((i * 512, 25, i * 512 + 512, 793)).tobytes() == expected.tobytes()
    assert len(run['samples']) == 3
    for p, h in {**pixel['evidence'], **transition['evidence']}.items():
        assert digest(p) == h
    evidence = {**pages['evidence'], **pixel['evidence'], **transition['evidence']}
    evidence.update({str(p): digest(p) for p in [pages_path, extension_path, fixture_path, terminal_path,
        pixel_path, plan_path, transition_path, Path(__file__)]})
    extra_run = dict(index=3, role='Focused longer-tail host-exit check;42 exact repeated body pages, no new source-body credit.',
        frames=21761, source_body_objects=42, observed_pages=42, actual_proof=str(pixel_path), run_plan=str(plan_path))
    save(output, {**pages, 'frames': 86324, 'initialized_runs': 4, 'primary_initialized_runs': 3,
        'focused_host_exit_runs': 1, 'runs': pages['runs'] + [extra_run],
        'observed_pages_including_repeats': 242, 'distinct_body_pages': 200,
        'review_sheets': pages['review_sheets'] + [{**sheet, 'directly_viewed': True, 'exact_original_capture_tiles_bound': True}],
        'exact_repeated_extended_pages_reused': reused, 'evidence': evidence,
        'host_exit_transition_approval_pending': False,
        'all_actual_body_menu_andtransition_sheets_directly_viewed': True,
        'representative_complete_QA_host_cleanup_resupply_andfollowing_tutorial_observed': True,
        'complete_QA_host_nonspeech_setup_cleanup_andfollowing_tutorial_observed': True,
        'host_exit_scope': 'One representative unchanged-ROM longer-tail run; the three original runs ended earlier. No claim that all three original captures observed resupply or tutorial.',
        'extended_tail_resolves_capture_schedule_shortfall_without_ROM_changes': True,
        'direct_visual_review_pending': False, 'registered_integration_pending': True, 'new_credit': 0})
    print('PASS199 bodies/200 unique pages,242 occurrences,4 menus,15 FE returns,1 page turn; representative host exit observed.22 sheets viewed.')


if __name__ == '__main__':
    main()
