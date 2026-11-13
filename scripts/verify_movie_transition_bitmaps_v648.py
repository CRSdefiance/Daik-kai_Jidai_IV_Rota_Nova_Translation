"""Source-native dissolve phases and ordinary clean/current transition evidence."""
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.compression_probe import decompress_lz10
from scripts.native_movie_transition_v648 import paint
from scripts.probe_button_prompt_native import BASE, machine
from scripts.research_committed_composition_v646 import render_order, vram_bindings
from scripts.research_ending_transitions_v642 import compose
from scripts.verify_opening_composition_v646 import checked_export
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/movie_transition_bitmaps_v648')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SOURCES = {'rafael': '/evstill/evstill001.pxl', 'lil': '/towngrp/towngrp03.pxl', 'hodram': '/evstill/evstill033.pxl'}
BAYER = bytes([0, 10, 2, 12, 8, 4, 14, 6, 3, 13, 1, 11, 15, 7, 9, 5])
BOUNDARIES = {'rafael': 3140, 'lil': 2860, 'hodram': 3120}


def rgb(words):
    result = []
    for w in words:
        r, g, b = w & 31, w >> 5 & 31, w >> 10 & 31
        g6 = 2 * g + (g >> 4)
        result.append((r * 255 // 31, g6 * 255 // 63, b * 255 // 31))
    return result


def shot_pixels(shot):
    assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    image = Image.open(shot['path']).convert('RGB')
    assert image.size == (256, 384)
    return list(image.get_flattened_data())


def report(label, suffix, digest, config):
    path = CAP / ('movie_transition_bitmaps_v648_' + label + suffix) / 'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == digest and data['frames'] == config['frames']
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not data.get('battery_save_preloaded') and not any(k.startswith('synthetic_') for k in data)
    assert data['scripted_input_schedule'] == read(config['inputs'])
    return data, {'path': str(path), 'sha256': sha(path.read_bytes())}


def main():
    pre, configs = read(ROOT / 'preflight.json'), read(ROOT / 'run_configs.json')
    for p, h in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == h
    assert sha(Path(pre['prior_proof']).read_bytes()) == pre['prior_proof_sha256']
    rom, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    clean_sha = sha(Path('work/clean.nds').read_bytes())
    original_code = machine(clean.read_file('/__arm9__.bin'))
    overlay = loadOverlayTable(clean.rom.arm9OverlayTable, lambda i, f: clean.files[f])[0]
    original_code.mem_write(overlay.ramAddress, bytes(overlay.data))
    exporter = sha((ROOT / 'executed_committed_exporter_source.py').read_bytes())
    results, baseline_frames, exact_clean, remaining_delta, native_count = {}, 0, 0, [], 0
    for label, config in configs.items():
        data, info = report(label, '', pre['candidate_sha256'], config)
        baseline, bi = report(label, '_baseline', pre['candidate_sha256'], config)
        control, ci = report(label, '_clean_control', clean_sha, config)
        assert not baseline.get('read_only_capture_GPU_states') and not control.get('read_only_capture_GPU_states')
        shots = {s['frame']: s for s in data['frames_captured']}
        bs, cs = ({s['frame']: s for s in r['frames_captured']} for r in (baseline, control))
        assert shots.keys() == bs.keys() == cs.keys()
        clean_differences = []
        for f, shot in shots.items():
            actual, base, old = shot_pixels(shot), shot_pixels(bs[f]), shot_pixels(cs[f])
            assert actual == base
            diff = [i for i, (a, b) in enumerate(zip(actual, old, strict=True)) if a != b]
            baseline_frames += 1
            exact_clean += not diff
            if diff:
                clean_differences.append({'frame': f, 'RGB_differences': len(diff), 'positions': diff})
                assert label == 'lil' and f == 2865 and len(diff) == 63
            if f == BOUNDARIES[label]:
                assert not diff
        packed = rom.read_file(SOURCES[label])
        assert packed == clean.read_file(SOURCES[label])
        decoded = decompress_lz10(packed) if packed[0] == 0x10 else packed
        picture = PxlImage.from_bytes(decoded)
        assert (picture.bits_per_pixel, picture.width, picture.height) == (8, 256, 192)
        po = struct.unpack_from('<I', decoded, 12)[0]
        palette_bytes = decoded[po:po + 512]
        palette = struct.unpack('<256H', palette_bytes)
        photo_words = [palette[i] for i in picture.indices]
        assert all(w & 32768 for w in photo_words)
        expected_phases = {p: struct.pack('<49152H', *[w if BAYER[(i // 256 % 4) * 4 + i % 4] <= p else 0
            for i, w in enumerate(photo_words)]) for p in range(16)}
        states = data['read_only_capture_GPU_states']
        native_states = {s['frame']: s for s in data['read_only_capture_native_states']}
        assert {s['frame'] for s in states} == native_states.keys() == set(config['GPU_and_native_frames'])
        rows, family, current_targets, raw_VRAM = [], {}, {}, {}
        movie = FlsArchive(rom.read_file(config['movie']))
        for state in states:
            f, native = state['frame'], native_states[state['frame']]
            committed = checked_export(state, exporter)
            assert sha(Path(native['path']).read_bytes()) == native['sha256']
            assert native['read_only_export'] and not native['state_loaded'] and native['main_RAM_unchanged_by_export']
            assert native['DTCM_region'] == 0x027E0000 and native['serialized_RAM_matches_same_frame_direct_export']
            for item in native['regions'].values():
                assert sha(Path(item['path']).read_bytes()) == item['sha256']
            raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
            io, vram, dtcm, itcm = [Path(native['regions'][k]['path']).read_bytes() for k in ['9REG', 'LCDM', 'DTCM', 'ITCM']]
            assert io == Path(committed['files']['source_arm9_io.bin']['path']).read_bytes()
            assert vram == Path(committed['files']['source_lcdc_vram.bin']['path']).read_bytes()
            header = 0x02276D74
            flags, width, height, paloff, pixoff = struct.unpack_from('<5I', raw, header - BASE)
            assert (flags, width, height) == struct.unpack_from('<3I', decoded)
            assert raw[header - BASE + paloff:header - BASE + paloff + 512] == palette_bytes
            assert raw[header - BASE + pixoff:header - BASE + pixoff + 49152] == picture.indices
            assert raw[0x12792C:0x12793C] == BAYER
            scene_nodes, node = [], struct.unpack_from('<I', raw, 0x3117C4 + 16)[0]
            while node:
                assert node not in {n['node'] for n in scene_nodes} and len(scene_nodes) < 50
                vt = struct.unpack_from('<I', raw, node - BASE)[0]
                scene_nodes.append({'node': node, 'draw': struct.unpack_from('<I', raw, vt - BASE + 12)[0]})
                node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
            transition_present = label != 'hodram' or any(n['draw'] == 0x02029150 for n in scene_nodes)
            if transition_present:
                upper, _, execution = paint(rom, original_code, raw, io, vram, dtcm, itcm)
                native_count += 1
                current_targets[f] = upper
            else:
                assert label == 'hodram' and f in (3122, 3123)
                upper, execution = None, None
            raw_VRAM[f] = vram[0x60000:0x78000]
            if label != 'hodram':
                effect = next(n['node'] for n in execution['original_scene_lists'][0x023117C4] if n['draw'] == 0x020283F4)
                progress, duration = struct.unpack_from('<2I', raw, effect - BASE + 0x38)
                assert duration == 32 and progress % 2 == 0
                pending_phase = progress * 16 // duration
                assert upper == expected_phases[pending_phase]
                # The capture is inside/awaiting the next painter. Validate the
                # preceding completed phase from its counter, never from PNGs.
                completed_phase = pending_phase - 1
                assert raw_VRAM[f] == expected_phases[completed_phase]
                if not family:
                    for phase in range(16):
                        controlled, _, ep = paint(rom, original_code, raw, io, vram, dtcm, itcm, phase)
                        assert controlled == expected_phases[phase]
                        family[phase] = {'complete98304_source_bitmap_bytes_exact': True, 'execution': ep}
                    assert len({sha(p) for p in expected_phases.values()}) == 16
                wrong = expected_phases[(completed_phase + 1) % 16]
                wrong_differences = sum(a != b for a, b in zip(wrong, raw_VRAM[f], strict=True))
                assert wrong_differences > 0
            else:
                progress = duration = pending_phase = completed_phase = None
                assert raw_VRAM[f] == struct.pack('<49152H', *photo_words)
                if upper is not None:
                    assert upper == raw_VRAM[f]
                wrong_differences = None
            bindings, resources = vram_bindings(committed, movie)
            ordered, _ = render_order(committed)
            backdrop, _ = compose(ordered, movie, bindings)
            renderer = Path(state['files']['gpu_framebuffer_RGBA8888.bin']['path']).read_bytes()
            observed_3D = rgb([((renderer[i] >> 3) | ((renderer[i+1] >> 3) << 5) | ((renderer[i+2] >> 3) << 10))
                for i in range(0, len(renderer), 4)])
            assert observed_3D == backdrop
            rows.append({'frame': f, 'current_progress': progress, 'duration': duration,
                'pending_source_phase': pending_phase, 'completed_VRAM_source_phase': completed_phase,
                'all49152_native_bitmap_words_including_bit15_exact': True,
                'wrong_completed_phase_byte_differences': wrong_differences,
                'whole3D_backdrop_matches_independent_ROM_composition': True,
                'source_VRAM_3D_resources': resources, 'execution': execution,
                'actual_upper_scene_nodes': scene_nodes,
                'post_transition_source_bitmap_retained_no_next_scene_replay_claim': not transition_present,
                'captured_CPU_PC': native['ARM9_instruction_address']})
        future_targets = {str(f): [g for g, buf in raw_VRAM.items() if target == buf]
                          for f, target in current_targets.items()}
        if label == 'lil':
            delta = clean_differences[0]
            assert {i // 256 for i in delta['positions']} == {79}
            assert all(i % 256 % 4 == 3 for i in delta['positions'])
            current, old = shot_pixels(shots[2865]), shot_pixels(cs[2865])
            photo_rgb = rgb(photo_words)
            assert all(current[i] == backdrop[i] and old[i] == photo_rgb[i] for i in delta['positions'])
            remaining_delta = [{'frame': 2865, 'pixels': 63, 'row': 79, 'Bayer_cell': [3, 3],
                'threshold': BAYER[15], 'current_all_old_original_3D_colors': True,
                'clean_all_new_original_photo_colors': True,
                'exact_intraframe_scanline_timing_not_independently_reconstructed': True}]
        results[label] = {'reports': {'export': info, 'baseline': bi, 'clean_control': ci},
            'source_picture': SOURCES[label], 'source_file_sha256': sha(packed),
            'source_original_palette_and_all49152_indices_exact_in_actual_header': True,
            'native_current_paint_targets_seen_in_captured_VRAM': future_targets,
            'controlled_original_dissolve_phase_family': family, 'cases': rows,
            'complete_same_frame_clean_control_differences': clean_differences,
            'original_reported_boundary_complete_two_screen_pixels_exact_clean': True}
        save(ROOT / 'verification_progress.json', {'routes': results, 'not_final': True})
        print(label, '6 source bitmap/3D states pass; actual transition scene replays',
              sum(r['execution'] is not None for r in rows), 'phase family', len(family), flush=True)
    assert baseline_frames == 36 and exact_clean == 35 and len(remaining_delta) == 1 and native_count == 16
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'previous_goal_turn_classification': 'progress', 'current_goal_turn_classification': 'progress',
        'routes': results, '18_complete_bitmap_states_884736_words_match_source_native_output': True,
        '16_actual_upper_transition_scene_replays_exact_clean_code_ABI': True,
        '2_post_transition_Hodram_states_retain_complete_previously_native_verified_photo': True,
        '32_controlled_original_phase_calls_all98304_bitmap_bytes_exact': True,
        'all16_replayed_upper_scene_instructions_exact_original_clean_ARM9_and_overlay0': True,
        '36_whole_two_screen_no_export_baselines_exact': True,
        '35_whole_two_screen_clean_controls_exact': True,
        'all3_original_reported_boundary_screens_exact_untouched_Japanese': True,
        'one_later_Lil63_pixel_difference_both_colors_original_sources': remaining_delta,
        'no_per_frame_delay_fitting_no_PNG_selection_of_source_phase': True,
        'exact_independent_intraframe_2D_display_timing_still_open': True,
        'not_claimed_as18_complete_same_frame_ROM_RGB_compositions': True,
        'all18_plaques_incomplete_all22_historical_requirements_exact': True,
        'ROM_patch_registry_canonical_release_pointers_unchanged': True,
        'scripts': {str(p): sha(p.read_bytes()) for p in Path('scripts').glob('*v648.py')},
        'full_goal_complete': False}
    save(ROOT / 'transition_bitmap_proof.json', proof)
    print('V648 source/native proof passes;3 reported boundaries exact clean;one later63-pixel phase edge explained;intraframe timing remains open.')


if __name__ == '__main__':
    main()
