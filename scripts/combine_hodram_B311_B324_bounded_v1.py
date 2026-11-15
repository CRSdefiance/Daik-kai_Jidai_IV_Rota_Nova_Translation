"""Join the two qualified display runs, preserving run-local frames and complete source keys."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Hodram_B311_B324_clean_20261107')
OUT = ROOT/'bounded_combined_v1'
FIXTURE = OUT/'fixture_set.json'
LIVE = OUT/'focused_actual_pixels.json'
MENU = OUT/'menu_actual_pixels.json'
EXIT = ROOT/'bounded_QA_return_proof_v1.json'

def main():
    assert not OUT.exists() and not EXIT.exists()
    fixture_manifest = ROOT/'focused_fixtures_bounded_v1/fixtures.json'
    created = load(fixture_manifest)['fixtures']
    rebuilt_path = ROOT/'reconstruction_v1/reconstruction.json'
    rebuilt = load(rebuilt_path)
    native_path = Path(rebuilt['native'])
    native = load(native_path)
    byid = {r['id']: r for r in native['records']}
    assert len(created) == 2
    fixtures, actual, menus, transitions = [], [], [], []
    evidence = {}
    def bind(path):
        path = Path(path)
        value = digest(path)
        assert str(path) not in evidence or evidence[str(path)] == value
        evidence[str(path)] = value
    for index, entry in enumerate(created, 1):
        fpath = Path(entry['fixture'])
        f = load(fpath)
        assert digest(fpath) == entry['fixture_sha256']
        apath = ROOT/f'bounded_pixels_{index}_v1/focused_actual_pixels.json'
        mpath = ROOT/f'bounded_menus_{index}_v1/menu_actual_pixels.json'
        tpath = ROOT/f'bounded_run_{index}_v1/terminal.json'
        console = ROOT/f'bounded_run_{index}_console_v1.log'
        a, m, t = map(load, [apath, mpath, tpath])
        text = console.read_text(encoding='utf-8-sig')
        assert 'Undefined instruction' not in text and 'Saved cold-boot frame evidence:' in text
        assert (a['frames'], a['selected_utterances'], a['selected_pages']) == (f['frames'], len(f['selected_records']), f['expected_pages'])
        assert a['all_selected_pages_observed_in_exact_fixture_order']
        assert a['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert a['evidence'][str(fpath)] == digest(fpath) and a['evidence'][str(tpath)] == digest(tpath)
        assert m['fixture_sha256'] == digest(fpath) and m['terminal_sha256'] == digest(tpath)
        assert m['ordered_body_receipt_sha256'] == digest(apath)
        assert m['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert m['byte_identical_menu_occurrences_bound_by_exact_source_keys_andordered_surrounding_calls']
        assert f['QA_block_inside_original_stack_buffer'] and f['padded_QA_block_bytes'] <= f['source_bound_QA_block_limit'] == 9216
        assert f['clean_andregistered_host_exit_commands_identical'] and f['source_bound_QA_host_exit_hex'] == '00c200000000'
        assert a['following_nonfixture_modal_frame'] < a['frames']
        observer = Path(t['observer'])
        assert digest(observer) == t['observer_sha256']
        obs = load(observer)
        assert not obs['errors'] and not obs['mismatches'] and obs['all_host_slots_restored_and_core_file_exact']
        following = [r for r in obs['rows'] if r['kind'] == 'modal_paint' and r['frame'] >= a['following_nonfixture_modal_frame']]
        assert following and 'supplies' in following[-1]['text_CP932']
        assert ' '.join(following[-1]['text_CP932'].split()) == 'Ah, Admiral. I was just about to take on supplies. Tell us what you need.'
        report = load(t['report'])
        assert digest(t['report']) == t['report_sha256'] and report['frames'] == f['frames']
        final = report['frames_captured'][-1]
        assert final['frame'] == f['frames'] and digest(final['path']) == final['PNG_sha256']
        transitions.append(dict(fixture_index=index, fixture=str(fpath), frames=f['frames'],
            following_native_dialogue=following[-1], final_capture=final,
            console=str(console), console_sha256=digest(console), no_undefined_instruction_in_native_output=True))
        fixtures.append(f)
        actual.append(a)
        menus.append(m)
        for p in [fpath, apath, mpath, tpath, console, observer, Path(t['report'])]:
            bind(p)
        for p, h in a['evidence'].items():
            assert digest(p) == h
            bind(p)
    assert fixtures[0]['original_initializers'] == fixtures[1]['original_initializers']
    copied = [r for f in fixtures for r in f['copied_commands']]
    expected = [dict(block=g['block'], original_offset=c['offset'], whole_command_hex=c['whole_command_hex'], word=c['word'])
        for g in rebuilt['groups'] for c in g['all_target_commands'] if c['word'] in [0x4000,0x4100,0x2100,0x2200]]
    assert [{k:v for k,v in r.items() if k!='fixture_offset'} for r in copied] == expected
    assert len(copied) == 195
    selected = [{**r, 'fixture_index':i, 'fixture':created[i-1]['fixture']}
        for i, f in enumerate(fixtures,1) for r in f['selected_records']]
    assert len(selected) == len({r['id'] for r in selected}) == 189
    assert sum(r.get('native_object_kind') == '4100-style-alternative' for r in selected) == 38
    expected_pages = []
    for row in selected:
        body = byid[row['id']]
        count = 1 if body['kind'] == 'system-FE' else len(body['complete_native_English_display']['pages'])
        expected_pages.extend((row['id'], p) for p in range(1,count+1))
    ordered = [{**r, 'fixture_index':i, 'fixture':created[i-1]['fixture']}
        for i, a in enumerate(actual,1) for r in a['ordered_selected_source_calls']]
    assert [(r['id'],r['page']) for r in ordered] == expected_pages and len(expected_pages) == 191
    header_expectations = {}
    for f in fixtures:
        for key, value in f['expected_header_actor_ID_by_selector'].items():
            assert key not in header_expectations or header_expectations[key] == value
            header_expectations[key] = value
    assert len(header_expectations) == 17
    total_frames = sum(f['frames'] for f in fixtures)
    assert total_frames == 57202
    OUT.mkdir()
    save(FIXTURE, dict(format='dk4-disclosed-native-dialogue-fixture-set-v1', fixtures=created,
        frames=total_frames, initialized_runs=2, selected_records=selected, expected_pages=191,
        expected_header_actor_ID_by_selector=header_expectations, source_selectors_with_header=sorted(map(int,header_expectations)),
        frame_numbers_are_run_local=True, complete_original_scene_including_transitions_andbranches_retained=False,
        no_original_conditional_menu_outcome_orstat_claim=True, all195_source_command_copies_and189_bindings_exact=True,
        all_QA_blocks_inside_original_stack_buffer=True, new_credit=0))
    bind(FIXTURE)
    live = deepcopy(actual[0])
    live.pop('following_nonfixture_modal_frame')
    live.update(frames=total_frames, initialized_fixture_runs=2, selected_utterances=189, selected_pages=191,
        complete_body_planes=sum(a['complete_body_planes'] for a in actual),
        complete_header_planes=sum(a['complete_header_planes'] for a in actual),
        body_pages=[{**r, 'fixture_index':i, 'fixture':created[i-1]['fixture']} for i,a in enumerate(actual,1) for r in a['body_pages']],
        headers=[{**r, 'fixture_index':i} for i,a in enumerate(actual,1) for r in a['headers']],
        ordered_selected_source_calls=ordered, observed_source_selectors=sorted(map(int,header_expectations)),
        review_sheets=[s for a in actual for s in a['review_sheets']], unvisited_utterances=198,
        fixture_set=str(FIXTURE), fixture_set_sha256=digest(FIXTURE), frame_numbers_are_run_local=True,
        source_order_preserved_across_independent_initialized_fixtures=True, following_native_dialogue_per_run=transitions,
        direct_visual_review_pending=True, evidence=evidence)
    assert live['complete_body_planes'] == 398 and live['complete_header_planes'] == 370 and len(live['review_sheets']) == 32
    save(LIVE, live)
    images = []
    for m in menus:
        sheet = m['review_sheet']
        assert digest(sheet['path']) == sheet['sha256']
        images.append(Image.open(sheet['path']).convert('RGB'))
    sheet = Image.new('RGB',(max(im.width for im in images),sum(im.height for im in images)),'#eee')
    y = 0
    for im in images:
        sheet.paste(im,(0,y)); y += im.height
    png = OUT/'menus_QA.png'
    sheet.save(png)
    menu = deepcopy(menus[0])
    for key in ['fixture','fixture_sha256','terminal','terminal_sha256']:
        menu.pop(key)
    menu.update(fixture_set=str(FIXTURE), fixture_set_sha256=digest(FIXTURE), frames=total_frames, initialized_fixture_runs=2,
        menus=[{**r, 'fixture_index':i, 'fixture':created[i-1]['fixture']} for i,m in enumerate(menus,1) for r in m['menus']],
        menu_samples=[{**r, 'fixture_index':i} for i,m in enumerate(menus,1) for r in m['menu_samples']],
        complete_live_caption_samples=sum(m['complete_live_caption_samples'] for m in menus),
        ordered_body_receipt=str(LIVE), ordered_body_receipt_sha256=digest(LIVE),
        review_sheet=dict(path=str(png),sha256=digest(png)), per_fixture_review_sheets=[m['review_sheet'] for m in menus],
        frame_numbers_are_run_local=True, evidence=evidence)
    assert {(m['block'],m['source_command_offset'],tuple(m['observed_selected_options'])) for m in menu['menus']} == {
        (311,1086,(0,)),(311,1306,(0,)),(313,782,(0,)),(316,674,(0,)),(316,934,(0,)),(317,764,(0,))}
    save(MENU, menu)
    capacity = Path('work/Hodram_B301_B310_clean_20261107/native_QA_capacity_v1.json')
    for p in [fixture_manifest, rebuilt_path, native_path, capacity, ROOT/'bounded_selection_v1.json', LIVE, MENU]:
        bind(p)
    save(EXIT, dict(qualified_runs=2, qualified_frames=57202, utterances=189, pages=191, menus=6,
        complete_body_planes=398, complete_header_planes=370, all_copied_commands_andbindings_exact=True,
        all191_display_pages_qualified=True, following_native_dialogue_observed=True,
        following_native_dialogue_per_run=transitions, all_native_output_logs_free_of_undefined_instructions=True,
        capacity_proof=str(capacity), native_stack_buffer_overflow_proven_andguarded=True,
        reused_capacity_depends_on_exact_registered_consumer_not_new_CPU_trace=True,
        current_production_max_target_block_bytes=max(g['target_bytes'] for g in rebuilt['groups']),
        all14_production_blocks_inside_conservative_bound=True,
        no_production_scene_controls_changed=True, prior_failed_runs_preserved=True,
        bounded_QA_terminal_resolution_not_full_event_activation=True, actual_visual_review_pending=True,
        new_credit=0, evidence={**evidence,str(Path(__file__)):digest(__file__)}))
    print('Joined two bounded runs/57,202 frames:189 utterances191 pages6 menus;398 complete bodies370 headers and both returns pass. Visual review pending.')

if __name__ == '__main__':
    main()
