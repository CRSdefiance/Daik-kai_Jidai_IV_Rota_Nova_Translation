"""Full source/native RGB checks for all textures in Rafael and Lil endings."""

from copy import deepcopy
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ending_fixture_v537 import request_ending
from scripts.research_ending_blend_v631 import plane
from scripts.research_ending_transitions_v642 import CAP, ROM, ROOT, compose, native_bindings
from scripts.research_photo_sampler_v630 import geometry, rgb_palette
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_village_wrap_v608 import read, save


def negatives(polys, movie, bindings, actual):
    assert compose(polys, movie, bindings)[0] == actual
    if actual == [(0, 0, 0)] * 49152:
        return {'complete_black_transition_verified_no_visible_picture_negative_claim': True}
    selected = None
    for index in reversed(range(len(polys))):
        poly = polys[index]
        texture = bindings[poly['texture_parameter'], poly['palette']]
        if not texture:
            continue
        tex = movie.texture(texture)
        positions = plane(poly, tex)
        transparent = bool(poly['texture_parameter'] & (1 << 29))
        source = next((s for s in positions if s is not None and (not transparent or tex.indices[s])), None)
        if source is not None:
            selected = index, tex, source
            break
    assert selected is not None
    index, tex, source = selected
    old = tex.indices[source]
    alternate = max(range(len(tex.palette)), key=lambda i: sum(abs(a - b) for a, b in
                    zip(tex.palette[i][:3], tex.palette[old][:3], strict=True)))
    tex.indices[source] = alternate
    try:
        assert compose(polys, movie, bindings)[0] != actual
    finally:
        tex.indices[source] = old
    shifted = deepcopy(polys)
    for vertex in shifted[index]['vertices']:
        vertex[0] += 1 / 128
    assert compose(shifted, movie, bindings)[0] != actual
    result = {'visible_source_texel_blank_and_one_pixel_geometry_shift_rejected': True}
    translucent = [i for i, p in enumerate(polys) if 0 < p['attributes'] >> 16 & 31 < 31
                   and bindings[p['texture_parameter'], p['palette']]]
    if translucent:
        changed = deepcopy(polys)
        i = translucent[-1]
        changed[i]['attributes'] = changed[i]['attributes'] & ~(31 << 16) | 31 << 16
        assert compose(changed, movie, bindings)[0] != actual
        result['wrong_opaque_alpha_rejected'] = True
    return result


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, clean_arm = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == pre['candidate_sha256'] and sha(arm) == pre['ARM9_sha256']
    for row in pre['original_code_ranges']:
        lo, hi = row['offset']
        assert arm[lo:hi] == clean_arm[lo:hi]
    for path, digest in pre['original_ending_movies'].items():
        assert rom.read_file(path) == clean.read_file(path) and sha(rom.read_file(path)) == digest
    configs = read(ROOT / 'run_configs.json')
    assert len(configs) == 4
    results, bindings_seen, reports, all_shots, prompts, terminal, lag_rejections = [], {0: set(), 2: set()}, [], [], [], [], []
    native_calls, black_cases, alpha_cases = 0, 0, 0
    for config in configs:
        label, captain = config['label'], config['captain']
        folder = CAP / f'ending_transitions_v642_{label}'
        report_path = folder / 'capture_report.json'
        report = read(report_path)
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == config['frames']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report['earned_completion_verified'] and len(report['synthetic_ending_fixtures']) == 1
        assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_ending_fixtures')
        assert report['scripted_input_schedule'] == read(config['inputs'])
        raw = (folder / f"frame_{config['pause_at']:06d}_arm9_ram.bin").read_bytes()
        after, fixture = request_ending(arm, raw, captain)
        assert fixture['changes'] == [{'address': 0x022796BC, 'before': 1, 'after': 4}]
        assert report['synthetic_ending_fixtures'] == [{'frame': config['pause_at'], **fixture}]
        for bad_arm, bad_ram, bad_captain in ((arm + b'\0', raw, captain), (arm, raw[:-1], captain),
                (arm, raw, (captain + 1) % 4), (arm, raw, True), (arm, after, captain)):
            try:
                request_ending(bad_arm, bad_ram, bad_captain)
            except ValueError:
                pass
            else:
                raise AssertionError('Invalid ending fixture accepted')
        donor = report.get('battery_save_preloaded')
        if captain == 0:
            assert donor['source_sha256'] == config['source_save_sha256']
            assert sha(Path(donor['source']).read_bytes()) == config['source_save_sha256']
            assert donor['copied_byte_exact_before_cold_boot']
        else:
            assert donor is None
        shots = {s['frame']: s for s in report['frames_captured']}
        for shot in report['frames_captured']:
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        states = {s['frame']: s for s in report['read_only_capture_GPU_states']}
        assert sorted(states) == config['gpu_export_frames']
        polys, images = {}, {}
        for frame, state in states.items():
            assert state['read_only_export'] and not state['state_loaded'] and state['main_RAM_unchanged_by_export']
            assert sha(Path(state['path']).read_bytes()) == state['sha256']
            for item in state['files'].values():
                assert Path(item['path']).stat().st_size == item['bytes']
                assert sha(Path(item['path']).read_bytes()) == item['sha256']
            raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
            assert sha(raw) == state['main_RAM_sha256']
            polys[frame] = geometry(Path(state['files']['gpu_geometry_chunk91.bin']['path']).read_bytes())
            images[frame] = Image.open(shots[frame]['path']).convert('RGB').crop((0, 0, 256, 192))
        source = rom.read_file(f'/FLS/M{29 + captain}.fls')
        movie = FlsArchive(source)
        source_bindings, native_records = {}, {}
        for anchor in config['anchors']:
            for frame in range(anchor, anchor + 3):
                sf = frame - 2
                state = states[sf]
                raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
                bindings, native = native_bindings(arm, clean_arm, raw, source)
                source_bindings[sf], native_records[sf] = bindings, native
                actual = list(images[frame].get_flattened_data())
                if label == 'rafael' and anchor == 12080:
                    assert not polys[sf] and native.get('no_live_FLS_controller')
                    texture = movie.texture(7)
                    palette = rgb_palette(texture)
                    expected = [palette[n] for n in texture.indices[:49152]]
                    assert expected == actual
                    assert expected != [(0, 0, 0)] * 49152
                    terminal.append({'label': label, 'frame': frame, 'explicit_original_terminal_texture': 7,
                        'entire49152_source_RGB_pixels_exact': True,
                        'no_new_FLS_geometry_not_misinterpreted_as_black_frame': True,
                        'PNG': shots[frame]})
                    continue
                expected, draws = compose(polys[sf], movie, bindings)
                assert expected == actual, (label, sf, frame)
                controls = negatives(polys[sf], movie, bindings, actual)
                native_calls += len(native.get('draws', []))
                black_cases += bool(controls.get('complete_black_transition_verified_no_visible_picture_negative_claim'))
                alpha_cases += bool(controls.get('wrong_opaque_alpha_rejected'))
                bindings_seen[captain].update(d['texture'] for d in draws)
                im = Image.new('RGB', (256, 192))
                im.putdata(expected)
                path = ROOT / f'{label}_{frame:06d}_SOURCE_COMPOSITION.png'
                im.save(path)
                results.append({'label': label, 'captain': captain, 'source_geometry_frame': sf,
                    'display_frame': frame, 'whole49152_RGB_pixels_exact_no_exclusions': True,
                    'native_binding': native, 'original_source_draws': draws, 'PNG': shots[frame],
                    'GPU_state': {'path': state['path'], 'sha256': state['sha256']},
                    'source_reconstruction': str(path), 'source_reconstruction_sha256': sha(path.read_bytes()), **controls})
        # One fixed shared delay must work for every active composition. For each
        # alternative, retain a counterexample rather than choosing per-frame lags.
        if label in ('rafael', 'lil'):
            for lag in (0, 1, 3):
                rejected = None
                for frame in sorted(states):
                    sf = frame - lag
                    if sf not in source_bindings or not polys[sf]:
                        continue
                    predicted, _ = compose(polys[sf], movie, source_bindings[sf])
                    different = sum(a != b for a, b in zip(predicted, images[frame].get_flattened_data(), strict=True))
                    if different:
                        rejected = {'label': label, 'alternative_lag': lag, 'source_geometry_frame': sf,
                                    'display_frame': frame, 'whole_RGB_differences': different}
                        break
                assert rejected is not None
                lag_rejections.append(rejected)
        save(ROOT / f'{label}_verified_native_bindings.json', native_records)
        last = Image.open(shots[config['frames']]['path']).convert('RGB')
        ink, bounds = complete_mask(GameAsciiFont.from_arm9(arm), 'Save the ending data?', last, 16, 296, (0, 8, 0))
        assert ink == 238
        prompts.append({'label': label, 'frame': config['frames'], 'whole_text_and_blank_cells_exact': True,
                        'ink': ink, 'bounds': bounds, 'PNG': shots[config['frames']]})
        reports.append({'label': label, 'path': str(report_path), 'sha256': sha(report_path.read_bytes()),
                        'GPU_checkpoints': len(states), 'fixture': fixture})
        all_shots.extend({'label': label, **shots[f]} for f in sorted(states))
    assert len(results) == 78 and len(terminal) == 3
    assert bindings_seen == {0: set(range(8)), 2: set(range(10))}
    scripts = [Path(__file__), Path('scripts/research_ending_transitions_v642.py'),
        Path('scripts/native_ending_fixture_v537.py'), Path('scripts/headless_desmume_v193.py'),
        Path('scripts/research_ending_blend_v631.py'), Path('scripts/research_photo_sampler_v630.py'),
        Path('scripts/inspect_desmume_gpu_v630.py')]
    proof = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'], 'reports': reports,
        'read_only_GPU_checkpoints': sum(r['GPU_checkpoints'] for r in reports),
        'actual_all18_source_texture_bindings': {str(k): sorted(v) for k, v in bindings_seen.items()},
        'full_source_compositions': results, 'separate_terminal_hold_compositions': terminal,
        'whole_comparison_pixels': (len(results) + len(terminal)) * 49152,
        'complete_black_transitions': black_cases, 'visible_wrong_alpha_controls': alpha_cases,
        'complete_original_native_draw_calls': native_calls, 'fixed_delay_frames': 2,
        'alternative_delay_counterexamples': lag_rejections, 'complete_ending_save_prompts': prompts,
        'all_screenshots': all_shots, 'all_source_code_movies_palettes_dimensions_and_release_artifacts_unchanged': True,
        'only_declared_one_byte_ending_state_per_run_no_savestate_or_movie_substitution': True,
        'earned_endings_hardware_and_every_intermediate_frame_not_claimed': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'full_goal_complete': False, 'scripts': {str(p): sha(p.read_bytes()) for p in scripts}}
    save(ROOT / 'native_ending_transitions_proof.json', proof)
    print(f'{len(results)} full source compositions +{len(terminal)} terminal holds;{proof["whole_comparison_pixels"]} exact RGB pixels;all18 texture bindings;{alpha_cases} wrong-alpha controls;4 complete ending prompts.')


if __name__ == '__main__':
    main()
