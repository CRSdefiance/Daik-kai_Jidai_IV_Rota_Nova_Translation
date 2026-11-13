"""Verify ordinary route movie samples; retain post-movie limits explicitly."""

from collections import Counter
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_committed_composition_v646 import render_order, vram_bindings
from scripts.research_ending_blend_v631 import plane
from scripts.research_ending_transitions_v642 import compose
from scripts.verify_ending_photo_markers_v594 import find_live
from scripts.verify_opening_composition_v646 import checked_export
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/route_opening_movies_v647')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ENGLISH = {'rafael': [27], 'lil': [1, 2], 'hodram': [3, 4]}
BOUNDARIES = {'rafael': 3140, 'lil': 2860, 'hodram': 3120}


def pixels(shot):
    assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    image = Image.open(shot['path']).convert('RGB')
    assert image.size == (256, 384)
    return list(image.crop((0, 0, 256, 192)).get_flattened_data())


def caption(polys, movie, binding, tid, actual):
    tex = movie.texture(tid)
    selected = [p for p in polys if binding[p['texture_parameter'], p['palette']] == tid
                and p['attributes'] >> 16 & 31 == 31]
    if len(selected) != 1:
        return None
    sampled = {i for i in plane(selected[0], tex) if i is not None}
    ink = {i for i, value in enumerate(tex.indices) if value}
    if not ink <= sampled:
        return None
    width, height = movie.records[tid][0] >> 16, movie.records[tid][1] & 65535
    assert all(i % tex.width < width and i // tex.width < height for i in ink)
    original = bytes(tex.indices)
    # Remove actual white-fill boundary columns, avoiding invisible outer black
    # shadow texels. These controls must visibly fail the complete RGB check.
    fill = {i for i, value in enumerate(original) if value == 1}
    assert fill and set(original) == {0, 1, 2}
    controls = []
    for label, col in [('leading white letter column', min(i % tex.width for i in fill)),
                       ('trailing white letter column', max(i % tex.width for i in fill))]:
        altered = bytearray(original)
        changed = [i for i in fill if i % tex.width == col]
        for i in changed:
            altered[i] = 0
        tex.indices[:] = altered
        try:
            negative, _ = compose(polys, movie, binding)
        finally:
            tex.indices[:] = original
        diff = sum(a != b for a, b in zip(negative, actual, strict=True))
        assert diff > 0
        controls.append({'control': label, 'source_fill_texels_removed': len(changed),
                         'whole_upper_RGB_differences': diff})
    return {'native_width_height': [width, height], 'complete_ink_and_shadow_source_texels': len(ink),
            'every_ink_shadow_texel_sampled_inside_original_native_bounds': True,
            'both_visible_boundary_controls_rejected': controls}


def main():
    pre, configs = read(ROOT / 'preflight.json'), read(ROOT / 'run_configs.json')
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    rom = NdsImage.open(pre['candidate'])
    assert sha(Path(pre['candidate']).read_bytes()) == pre['candidate_sha256']
    clean, v303, v299 = (NdsImage.open(p) for p in ('work/clean.nds',
        'out/all_routes_combined_v303_candidate.nds', 'out/all_routes_combined_v299_candidate.nds'))
    arm = rom.read_file('/__arm9__.bin')
    assert sha(arm) == pre['ARM9_sha256']
    exporter_sha = sha((ROOT / 'executed_committed_exporter_source.py').read_bytes())
    results, baseline_count, total_ink, reports = {}, 0, 0, {}
    old_clip = None
    for label, config in configs.items():
        folder = CAP / ('route_opening_movies_v647_' + label)
        report_path = folder / 'capture_report.json'
        report = read(report_path)
        baseline_path = Path(str(folder) + '_baseline') / 'capture_report.json'
        baseline = read(baseline_path)
        for data in (report, baseline):
            assert data['ROM_sha256'] == pre['candidate_sha256'] and data['frames'] == config['frames']
            assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
            assert data['scripted_input_schedule'] == read(config['inputs'])
            assert not data.get('battery_save_preloaded') and not any(k.startswith('synthetic_') for k in data)
        assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
        assert not baseline.get('read_only_capture_GPU_states')
        shots = {s['frame']: s for s in report['frames_captured']}
        base_shots = {s['frame']: s for s in baseline['frames_captured']}
        assert shots.keys() == base_shots.keys()
        for f, shot in shots.items():
            pixels(shot)
            pixels(base_shots[f])
            assert Image.open(shot['path']).convert('RGB').tobytes() == Image.open(base_shots[f]['path']).convert('RGB').tobytes()
        baseline_count += len(shots)
        source = rom.read_file(config['movie'])
        assert sha(source) == pre['movies'][config['movie']]
        assert source == v303.read_file(config['movie'])
        movie, original = FlsArchive(source), FlsArchive(clean.read_file(config['movie']))
        assert movie.records == original.records and movie.count == original.count
        changed = []
        for i in range(movie.count):
            now, before = movie.texture(i), original.texture(i)
            assert (now.flags, now.width, now.height, now.palette) == (before.flags, before.width, before.height, before.palette)
            if now.indices != before.indices:
                changed.append(i)
        assert changed == ENGLISH[label]
        assert {r['frame'] for r in report['read_only_capture_GPU_states']} == set(config['gpu_export_frames'])
        cases, boundaries, seen, captions, wrong_lag = [], [], set(), {}, []
        for state in report['read_only_capture_GPU_states']:
            f = state['frame']
            committed = checked_export(state, exporter_sha)
            raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
            assert sha(raw) == state['main_RAM_sha256']
            u = machine(arm)
            u.mem_write(BASE, raw)
            call(u, 0x7F244, ())
            assert u.reg_read(UC_ARM_REG_R0) == config['captain']
            live = find_live(raw, source)
            if live is None:
                assert f == BOUNDARIES[label]
                boundaries.append({'frame': f, 'expected_movie_controller_absent': True,
                    'not_counted_as_independent_movie_source_composition': True,
                    'reason': 'Post-movie software bitmap overlays require separate timing/paint verification.'})
                continue
            binding, resources = vram_bindings(committed, movie)
            ordered, order = render_order(committed)
            expected, draws = compose(ordered, movie, binding)
            actual = pixels(shots[f + 1])
            assert expected == actual, (label, f, sum(a != b for a, b in zip(expected, actual, strict=True)))
            for resource in resources:
                seen.update(resource['source_equivalence_candidates'])
            for tid in ENGLISH[label]:
                if tid in captions:
                    continue
                check = caption(ordered, movie, binding, tid, actual)
                if check is not None:
                    captions[tid] = {'source_frame': f, 'display_frame': f + 1, **check}
                    total_ink += check['complete_ink_and_shadow_source_texels']
                    if label == 'lil' and tid == 1:
                        bad = FlsArchive(v299.read_file('/FLS/M22.fls')).texture(1)
                        poly = next(p for p in ordered if binding[p['texture_parameter'], p['palette']] == tid)
                        sampled = {s for s in plane(poly, movie.texture(tid)) if s is not None}
                        missing = [i for i, v in enumerate(bad.indices) if v and i not in sampled]
                        values = Counter(bad.indices[i] for i in missing)
                        assert len(missing) == 42 and values == {1: 12, 2: 30}
                        old_clip = {'source': 'V299 /FLS/M22.fls texture1', 'current_original_geometry_source_frame': f,
                            'source_ink_outside_actual_sampled_native_view': len(missing),
                            'white_fill_pixels_lost': values[1], 'black_outline_pixels_lost': values[2],
                            'no_ROM_or_actual_display_mutation': True}
            wrong = sum(a != b for a, b in zip(expected, pixels(shots[f]), strict=True))
            if wrong:
                wrong_lag.append({'frame': f, 'whole_upper_RGB_differences': wrong})
            cases.append({'source_frame': f, 'display_frame': f + 1, 'movie_controller': live,
                'all49152_RGB_pixels_exact_without_exclusions': True, 'source_VRAM_resources': resources,
                'draws': draws, 'render_order': order, 'committed_export': state['read_only_committed_geometry']['path'],
                'committed_export_sha256': state['read_only_committed_geometry']['sha256']})
        assert seen == set(range(movie.count)) and set(captions) == set(ENGLISH[label])
        assert len(boundaries) == 1 and wrong_lag
        reports[label] = {kind: {'path': str(p), 'sha256': sha(p.read_bytes())}
                          for kind, p in [('export', report_path), ('baseline', baseline_path)]}
        results[label] = {'movie': config['movie'], 'all_source_views_represented': sorted(seen),
            'source_views': movie.count, 'cases': cases, 'complete_caption_checks': captions,
            'lag0_counterexamples': wrong_lag, 'separate_post_movie_boundaries_not_cleared': boundaries,
            'independent_no_export_whole_two_screen_comparisons': len(shots)}
        print(label, len(cases), 'complete source frames;', len(captions), 'complete captions;', len(shots), 'baseline frames', flush=True)
    assert sum(len(r['cases']) for r in results.values()) == 94
    assert total_ink == 8559 and old_clip is not None
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'previous_goal_turn_classification': 'no progress: status reply; revalidated existing captures and executed verification now',
        'current_goal_turn_classification': 'progress', 'routes': results, 'reports': reports,
        'all94_active_movie_compositions_exact': True, 'complete_upper_RGB_pixels': 94 * 49152,
        'all36_native_source_views_represented': True,
        'all5_English_captions_complete8559_ink_shadow_texels_and10_visible_boundary_controls': True,
        'prior_real_clipping_defect_reproduced_against_native_sampled_view': old_clip,
        'independent_no_export_whole_two_screen_frames_exact': baseline_count,
        'independent_no_export_whole_two_screen_pixels_exact': baseline_count * 98304,
        'source_storage_native_geometry_palettes_all_other_texture_pixels_exact_clean': True,
        'all_three_movie_files_byte_exact_previously_reviewed_V303': True,
        'post_movie_boundary_timing_and_independent_bitmap_paint_proof_remain_open': True,
        'original97_planned_checkpoints_accounted94_active_plus3_post_movie_not_silently_waived': True,
        'no_ROM_patch_registry_or_release_pointer_change': True,
        'all18_plaques_incomplete_all22_historical_requirements_retained': True,
        'unsampled_movie_frames_legacy_consumers_entire_routes_and_hardware_not_inferred': True,
        'scripts': {str(p): sha(p.read_bytes()) for p in Path('scripts').glob('*v647.py')},
        'actual_exporter_source_sha256': exporter_sha, 'full_goal_complete': False}
    save(ROOT / 'route_opening_movie_proof.json', proof)
    print('V647 complete sampled verification:', 94, 'source frames;', total_ink, 'caption ink/shadow texels;', baseline_count, 'baseline frames. Post-movie composition remains open.')


if __name__ == '__main__':
    main()
