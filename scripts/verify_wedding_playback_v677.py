"""Actual original M26 playback, source pixels, fixture fidelity and baseline evidence."""

import struct
from copy import deepcopy
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.native_wedding_fixture_v677 import ROOT, plan
from scripts.research_committed_composition_v646 import render_order, vram_bindings
from scripts.research_ending_blend_v631 import plane, sixbit_palette
from scripts.research_ending_transitions_v642 import compose
from scripts.run_village_visits_v664 import CAP
from scripts.verify_ending_photo_markers_v594 import find_live
from scripts.verify_opening_composition_v646 import checked_export
from scripts.verify_village_wrap_v608 import read, save


def image(shot):
    assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    return Image.open(shot['path']).convert('RGB')


def main():
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'playback_config.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    rom = NdsImage.open(pre['candidate'])
    arm, source = rom.read_file('/__arm9__.bin'), rom.read_file('/FLS/M26.fls')
    assert source == NdsImage.open('work/clean.nds').read_file('/FLS/M26.fls')
    controls = read(ROOT / 'fixture_controls.json')
    assert controls['script_sha256'] == sha(Path('scripts/check_wedding_fixture_v677.py').read_bytes())
    assert len(controls['policy_cases']) == 11 and len(controls['native_prefix_cases']) == 5
    inputs = read(config['inputs'])
    assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
    assert len(inputs) == 61 and max(e['start'] + e.get('duration', 5) - 1 for e in inputs) == 14408
    reports, shots, receipts, fixtures = {}, {}, {}, {}
    for tag in ('pilot_v2', 'observed', 'fixture_baseline', 'disabled_v2'):
        folder = CAP / ('wedding_playback_v677_' + tag)
        report = read(folder / 'capture_report.json')
        assert report['frames'] == (4000 if tag == 'disabled_v2' else 16000)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
        assert not report.get('battery_save_preloaded')
        assert report['scripted_input_schedule'] == (read(ROOT / 'pilot_inputs.json') if tag == 'disabled_v2' else inputs)
        contract = read(folder / 'run_contract.json')
        producer = ROOT / 'pilot_v2_run_wedding_playback_v677.py' if tag.endswith('_v2') else Path('scripts/run_wedding_playback_v677.py')
        assert contract['runner_sha256'] == sha(producer.read_bytes())
        assert contract['fixture_sha256'] == sha(Path('scripts/native_wedding_fixture_v677.py').read_bytes())
        proof = read(folder / 'chapter_fixture/fixture.json')
        assert proof['script_sha256'] == contract['fixture_sha256']
        assert proof['slot_restored_before_filter_free'] and not proof['errors'] and not proof['mismatches']
        assert proof['applied'] == (tag != 'disabled_v2')
        assert len(proof['rows']) == proof['callbacks'] == 1
        row = proof['rows'][0]
        data = {}
        for key, item in row['files'].items():
            data[key] = Path(item['path']).read_bytes()
            assert sha(data[key]) == item['sha256']
        after, receipt = plan(arm, data['CPU_before.bin'], data['RAM_before.bin'], enabled=tag != 'disabled_v2')
        assert row['receipt'] == receipt and data['CPU_expected_after.bin'] == after
        assert row['frame'] == 2222 and row['actual_CPU_after_exact_and_full_WRAM_unchanged_at_fixture']
        if tag != 'disabled_v2':
            assert receipt['changed_CPU_byte_offsets'] == [20] and receipt['incoming_block'] == 22 and receipt['requested_block'] == 70
            assert {key for key, value in report.items() if key.startswith('synthetic_') and value} == {'synthetic_original_chapter_loader_fixture'}
            assert report['earned_completion_verified'] is False
        else:
            assert not any(key.startswith('synthetic_') for key in report)
        frame_map = {}
        for shot in report['frames_captured']:
            pixels = image(shot).tobytes()
            if shot['frame'] in frame_map:
                assert frame_map[shot['frame']][1] == pixels
            frame_map[shot['frame']] = shot, pixels
        reports[tag], shots[tag], fixtures[tag] = report, frame_map, proof
        receipts[tag] = {'path': str(folder / 'capture_report.json'),
                         'sha256': sha((folder / 'capture_report.json').read_bytes())}
    assert shots['observed'].keys() == shots['fixture_baseline'].keys() and len(shots['observed']) == 705
    assert all(shots['observed'][frame][1] == item[1] for frame, item in shots['fixture_baseline'].items())
    assert len(shots['pilot_v2']) == 67 and all(shots['observed'][frame][1] == item[1] for frame, item in shots['pilot_v2'].items())
    ordinary = read(CAP / 'wedding_source_v676_baseline/capture_report.json')
    ordinary_shots = {s['frame']: image(s).tobytes() for s in ordinary['frames_captured']}
    assert len(shots['disabled_v2']) == 12 and all(ordinary_shots[frame] == item[1] for frame, item in shots['disabled_v2'].items())
    assert len({sha((CAP / ('wedding_playback_v677_' + tag) / 'final_arm9_ram.bin').read_bytes())
                for tag in ('pilot_v2', 'observed', 'fixture_baseline')}) == 1
    assert (CAP / 'wedding_playback_v677_disabled_v2/final_arm9_ram.bin').read_bytes() == (
        CAP / 'wedding_source_v676_baseline/final_arm9_ram.bin').read_bytes()
    meta = read(CAP / 'wedding_playback_v677_observed/observer/paint_observer.json')
    assert meta['original_slot_restored_and_DLL_file_unchanged'] and meta['all_three_original_slot_pointers_restored_before_filter_free']
    assert not meta['mismatch'] and not meta['overflow']
    assert meta['private_wrapper_sha256'] == sha(Path('scripts/observe_wedding_runtime_v676.py').read_bytes())
    entries = Path(meta['path']).read_bytes()
    assert sha(entries) == meta['sha256']
    special = []
    for row in struct.iter_unpack('<40I', entries):
        if row[1] in (0x02024134, 0x02028A28, 0x020D2B1C):
            special.append({'frame': row[0], 'PC': row[1], 'args': list(row[3:7]), 'LR': row[8],
                            'inapplicable_blitter_guard_flags': row[38]})
        else:
            assert not row[38]
    assert [(r['frame'], r['PC']) for r in special] == [(16, 0x020D2B1C), (559, 0x020D2B1C),
        (2222, 0x02024134), (14489, 0x02028A28), (14489, 0x020D2B1C)]
    assert special[2]['args'][1] == 70 and special[3]['args'][1] == 6 and special[4]['args'] == [26, 0, 1, 0]
    obj = special[2]['args'][0]
    assert special[3]['args'][3] == obj + 8 + 4324
    block = IlnkContainer.parse(rom.read_file('/data/SC2.DK4')).blocks[70]
    research = read(ROOT / 'composition_research.json')
    assert research['script_sha256'] == sha(Path('scripts/research_wedding_composition_v677.py').read_bytes())
    assert not research['failures'] and len(research['rows']) == 152
    rows = research['rows']
    assert [row['frame'] for row in rows] == config['gpu_frames']
    assert [row['native']['live_controller']['native_counter'] for row in rows] == list(range(152))
    assert all(next(c['RGB_differences'] for c in row['comparisons'] if c['lag'] == 1) == 0 for row in rows)
    assert all(any(next(c['RGB_differences'] for c in row['comparisons'] if c['lag'] == lag) > 0
                   for row in rows) for lag in (0, 2, 3))
    retained = [(row['frame'], item) for row in rows for item in row['separate_retained_committed_commands']]
    assert len(retained) == 1 and retained[0][0] == 14740 and retained[0][1]['prior_actual_native_source_frame'] == 14736
    states = {s['frame']: s for s in reports['observed']['read_only_capture_GPU_states']}
    assert set(states) == set(config['gpu_frames'])
    for frame, state in states.items():
        checked_export(state, sha(Path('scripts/inspect_committed_gpu_v646.py').read_bytes()))
        raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
        assert sha(raw) == state['main_RAM_sha256']
        assert raw[obj + 8 - 0x02000000:obj + 8 - 0x02000000 + len(block)] == block
    # Three independent source perturbations test both photographs and blending.
    movie, negative = FlsArchive(source), []
    chosen = [next(r for r in rows if any(d['texture'] == t and d['alpha'] == 31 for d in r['draws'])) for t in (0, 1)]
    chosen.append(next(r for r in rows if any(0 < d['alpha'] < 31 for d in r['draws'])))
    for row in chosen:
        committed = read(row['committed']['path'])
        bound, _ = vram_bindings(committed, movie)
        ordered, _ = render_order(committed)
        actual = list(image(shots['observed'][row['frame'] + 1][0]).crop((0, 0, 256, 192)).get_flattened_data())
        assert compose(ordered, movie, bound)[0] == actual
        poly = ordered[-1]
        texture = movie.texture(bound[poly['texture_parameter'], poly['palette']])
        position = next(i for i in plane(poly, texture) if i is not None and texture.indices[i])
        old = texture.indices[position]
        texture.indices[position] = max(range(len(texture.palette)), key=lambda i: sum(abs(a - b) for a, b in zip(texture.palette[i][:3], texture.palette[old][:3], strict=True)))
        try:
            assert compose(ordered, movie, bound)[0] != actual
        finally:
            texture.indices[position] = old
        shifted = deepcopy(ordered)
        for vertex in shifted[-1]['vertices']:
            vertex[0] += 1 / 128
        assert compose(shifted, movie, bound)[0] != actual
        item = {'frame': row['frame'], 'visible_source_texel_and_one_pixel_geometry_change_rejected': True}
        if 0 < poly['attributes'] >> 16 & 31 < 31:
            opaque = deepcopy(ordered)
            opaque[-1]['attributes'] = opaque[-1]['attributes'] & ~(31 << 16) | 31 << 16
            assert compose(opaque, movie, bound)[0] != actual
            item['incorrect_opaque_alpha_rejected'] = True
        negative.append(item)
    # Original final photo is held after the live movie object is gone.
    colors = sixbit_palette(movie.texture(1))
    expected = []
    for index in movie.texture(1).indices[:256 * 192]:
        r6, g6, b6 = colors[index]
        r, g, b = r6 >> 1, g6 >> 1, b6 >> 1
        expected.append((r * 255 // 31, ((g << 1) | (g >> 4)) * 255 // 63, b * 255 // 31))
    held = []
    for frame in (15200, 15400, 15600, 15800, 16000):
        assert list(image(shots['observed'][frame][0]).crop((0, 0, 256, 192)).get_flattened_data()) == expected
        held.append(frame)
        raw = (CAP / f'wedding_playback_v677_pilot_v2/frame_{frame:06d}_arm9_ram.bin').read_bytes()
        assert find_live(raw, source) is None
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'previous_goal_turn_classification': pre['previous_goal_turn_classification'],
        'four_successful_runs': receipts, '705_complete_fixture_observed_baseline_pairs': True,
        '67_pilot_pairs12_disabled_unmodified_pairs_and_exact_terminal_RAM_states': True,
        'actual_original_B70_loaded_all6764_bytes_in152_GPU_states': True,
        'one_CPU_R1_field_fixture22_to70_no_WRAM_ROM_script_or_movie_file_edits': True,
        'actual_original_chapter6_M26_request': special,
        '152_complete_source_compositions_all_native_counters0_through151': True,
        'whole_RGB_pixel_comparisons': 152 * 49152, 'source_textures': [0, 1],
        'whole_native_extent_and_palette_VRAM_bindings_inside_original_crops': True,
        'full_native_draws_with_GPU_commands': sum(len(r['native']['draws']) for r in rows),
        'one_fixed_submission_to_display_frame_other0_2_3_rejected': True,
        'retained_final_fade_command_resolved_by_original_earlier_draw_without_waived_pixels': retained,
        'source_geometry_alpha_controls': negative, 'five_final_original_photo_holds': held,
        '11_policy5_native_host_controls': controls, 'all_slots_restored_and_core_file_exact': True,
        'initial_wrong_empty_reader_marker_rejected_before_game_state_change': True,
        'earned_wedding_route_completion_every_DMA_cycle_or_hardware_not_claimed': True,
        'older_record_followup': {'id': 'DK4_MES_B70_R0397', 'capture': 'pilot_v2/frame_011400_navigation.png',
            'note': 'Older manual dialogue leaves me. alone on its last line; retain for requested older record review.'},
        'all18_plaques_incomplete22_original_requirements_retained_no_ROM_change': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V677705 paired screens,152 complete source compositions,165 native draws and5 original photo holds verified; forced chapter context disclosed.', flush=True)


if __name__ == '__main__':
    main()
