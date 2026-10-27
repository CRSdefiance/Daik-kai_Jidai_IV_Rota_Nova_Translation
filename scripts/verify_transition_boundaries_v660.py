"""Complete all18 retained boundary states at their actual source scanlines."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.compression_probe import decompress_lz10
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.native_movie_transition_v648 import paint
from scripts.observe_transition_scanlines_v659 import ENTRIES, PROLOGUES, jump
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_committed_composition_v646 import render_order, vram_bindings
from scripts.research_ending_transitions_v642 import compose
from scripts.verify_movie_transition_bitmaps_v648 import BAYER, rgb
from scripts.verify_opening_composition_v646 import checked_export
from scripts.verify_transition_scanlines_v659 import core_entries, pixels
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/transition_boundaries_v660')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def hodram_stripe_control(rom, original, raw, native, photo):
    node = struct.unpack_from('<I', raw, 0x3117D4)[0]
    while node:
        vt = struct.unpack_from('<I', raw, node - BASE)[0]
        if struct.unpack_from('<I', raw, vt - BASE + 12)[0] == 0x02029150:
            break
        node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
    assert node
    adjustment = struct.unpack('<i', original.mem_read(0x0202915C, 4))[0]
    assert adjustment == -40
    parent = node + adjustment
    progress, duration, direction = struct.unpack_from('<3I', raw, parent - BASE + 8)
    assert duration == 32 and direction == 1
    controlled = bytearray(raw)
    struct.pack_into('<I', controlled, parent - BASE + 8, duration * 3 // 4)
    changed = [i for i, (a, b) in enumerate(zip(raw, controlled, strict=True)) if a != b]
    assert changed and all(parent - BASE + 8 <= i < parent - BASE + 12 for i in changed)
    io, vram, dtcm, itcm = [Path(native['regions'][k]['path']).read_bytes() for k in ('9REG', 'LCDM', 'DTCM', 'ITCM')]
    upper, _, execution = paint(rom, original, bytes(controlled), io, vram, dtcm, itcm)
    expected = struct.pack('<49152H', *[w if i % 8 < 6 else 0 for i, w in enumerate(photo)])
    assert upper == expected
    path = ROOT / 'Hodram_original_six_of_eight_stripe_control.bin'
    path.write_bytes(upper)
    return {'actual_source_frame': 3118, 'actual_node': node, 'original_thunk_adjustment': adjustment,
        'actual_parent': parent, 'actual_pending_progress': progress, 'duration': duration,
        'isolated_owned_progress': duration * 3 // 4, 'changed_RAM_bytes': [BASE + i for i in changed],
        'only_isolated_progress_field_changed_no_emulator_game_RAM_or_ROM_write': True,
        'controlled_argument_not_claimed_as_observed3117_callback_argument': True,
        'all98304_bytes_match_independent_six_of_eight_original_photo_pattern': True,
        'path': str(path), 'sha256': sha(upper), 'execution': execution}


def main():
    pre, configs = read(ROOT / 'preflight.json'), read(ROOT / 'run_configs.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['inherited_observer']).read_bytes()) == pre['inherited_observer_sha256']
    assert sha(Path(pre['prior_transition_proof']).read_bytes()) == pre['prior_transition_proof_sha256']
    assert sha(Path(pre['prior_scanline_proof']).read_bytes()) == pre['prior_scanline_proof_sha256']
    prior, scanline = read(pre['prior_transition_proof']), read(pre['prior_scanline_proof'])
    for path, digest in scanline['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert scanline['this_resolves_the_specific_V648_Lil63_pixel_scanline_timing_comparison']
    assert len(scanline['twelve_relocated_host_prefix_GPR_flags_and_full_stack_controls']) == 12
    assert sha(CORE.read_bytes()) == CORE_SHA
    roms = {'current': NdsImage.open(pre['candidate']), 'clean': NdsImage.open('work/clean.nds')}
    code = {}
    for label, rom in roms.items():
        cpu = machine(rom.read_file('/__arm9__.bin'))
        for overlay in loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, fid, rom=rom: rom.files[fid]).values():
            cpu.mem_write(overlay.ramAddress, bytes(overlay.data))
        code[label] = cpu
    exporter = sha(Path('scripts/inspect_committed_gpu_v646.py').read_bytes())
    routes, pairs, states, total_rows, total_words, matching_clean_frames = {}, [], [], 0, 0, 0
    stripe_control = None
    for route, config in configs.items():
        assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
        assert config['GPU_and_native_frames'] == [r['frame'] for r in prior['routes'][route]['cases']]
        image_file = roms['current'].read_file(config['picture'])
        assert image_file == roms['clean'].read_file(config['picture'])
        decoded = decompress_lz10(image_file) if image_file[0] == 16 else image_file
        picture = PxlImage.from_bytes(decoded)
        assert (picture.width, picture.height, picture.bits_per_pixel) == (256, 192, 8)
        po = struct.unpack_from('<I', decoded, 12)[0]
        palette_bytes = decoded[po:po + 512]
        palette = struct.unpack('<256H', palette_bytes)
        photo = [palette[i] for i in picture.indices]
        assert all(w & 32768 for w in photo)
        photo_rgb = rgb(photo)
        instructions = set()
        for row in prior['routes'][route]['cases']:
            if row['execution']:
                instructions.update(row['execution']['all_executed_instruction_words_exact_registered_ROM'])
        for row in prior['routes'][route]['controlled_original_dissolve_phase_family'].values():
            instructions.update(row['execution']['all_executed_instruction_words_exact_registered_ROM'])
        assert instructions
        for address in instructions:
            assert code['current'].mem_read(address, 4) == code['clean'].mem_read(address, 4)
        reports, images, sources, source_models = {}, {}, {}, {}
        for label, rom in roms.items():
            folder = CAP / ('transition_boundaries_v660_' + route + '_' + label + '_observed')
            rp, bp = folder / 'capture_report.json', Path(str(folder).replace('_observed', '_baseline')) / 'capture_report.json'
            report, baseline = read(rp), read(bp)
            digest = sha(rom.source.read_bytes())
            for data in (report, baseline):
                assert data['ROM_sha256'] == digest and data['core_DLL_sha256'] == CORE_SHA
                assert data['frames'] == config['frames'] and data['cold_boot'] and not data['savestate_loaded']
                assert not data['callback_errors'] and not data.get('battery_save_preloaded')
                assert not any(k.startswith('synthetic_') for k in data)
                assert data['scripted_input_schedule'] == read(config['inputs'])
                seen = {}
                for shot in data['frames_captured']:
                    values = pixels(shot)
                    if shot['frame'] in seen:
                        assert values == seen[shot['frame']]
                    seen[shot['frame']] = values
            assert report['core_options'] == baseline['core_options']
            shots, base = ({r['frame']: r for r in d['frames_captured']} for d in (report, baseline))
            assert shots.keys() == base.keys() and len(shots) == 12
            for frame in shots:
                assert pixels(shots[frame]) == pixels(base[frame])
                pairs.append({'route': route, 'build': label, 'frame': frame,
                              'observed': shots[frame], 'unmodified_core_baseline': base[frame],
                              'all98304_two_screen_RGB_pixels_exact': True})
            op = folder / 'scanlines/scanline_observer.json'
            observer = read(op)
            assert observer['script_sha256'] == pre['inherited_observer_sha256']
            assert not observer['errors'] and observer['every_original_RenderLine_called_once']
            assert observer['all_entry_bytes_restored_and_DLL_file_unchanged']
            assert observer['no_game_ROM_RAM_VRAM_register_or_input_writes']
            assert set(map(int, observer['frames'])) == set(config['scanline_frames'])
            binding = core_entries(observer)
            for row, (rva, n, fmt), prefix in zip(observer['host_core_entry_detours_only_in_diagnostic_process'], ENTRIES, PROLOGUES, strict=True):
                assert (row['RVA'], row['stolen_bytes'], row['format'], row['original_hex']) == (rva, n, fmt, prefix)
                assert bytes.fromhex(row['trampoline_hex']) == bytes.fromhex(prefix) + jump(row['address'] + n)
                assert bytes.fromhex(row['detour_hex'])[:6] == b'\xff\x25\0\0\0\0'
            words_by_frame = {}
            for frame, value in observer['frames'].items():
                frame = int(frame)
                for item in value['files'].values():
                    assert sha(Path(item['path']).read_bytes()) == item['sha256']
                words = struct.unpack('<49152H', Path(value['files']['bitmap_row']['path']).read_bytes())
                io = Path(value['files']['IO']['path']).read_bytes()
                assert len(value['rows']) == 192
                for line, row in enumerate(value['rows']):
                    assert (row['line'], row['VCount'], row['frame'], row['format']) == (line, line, frame, '555')
                    assert row['original_render_called_once_and_returned']
                    actual_io = io[line * 8192:(line + 1) * 8192]
                    assert struct.unpack_from('<I', actual_io)[0] == 0x1191B
                    assert struct.unpack_from('<H', actual_io, 14)[0] == 0x4084
                    assert struct.unpack_from('<H', actual_io, 8)[0] & 3 == 1
                    assert actual_io[0x243] == 0x81
                    assert struct.unpack_from('<4h2I', actual_io, 0x30) == (256, 0, 0, 256, 0, line * 256)
                    assert struct.unpack_from('<3H', actual_io, 0x50) == (0, 0, 0)
                    assert struct.unpack_from('<H', actual_io, 0x6C)[0] == 0
                    actual = words[line * 256:(line + 1) * 256]
                    original = photo[line * 256:(line + 1) * 256]
                    assert all(w == 0 or w == source for w, source in zip(actual, original, strict=True))
                    if route == 'hodram':
                        if frame == 3117:
                            assert list(actual) == [w if x % 8 < 6 else 0 for x, w in enumerate(original)]
                        else:
                            assert list(actual) == original
                    else:
                        assert any(all(bool(w & 32768) == (BAYER[line % 4 * 4 + x % 4] <= phase)
                            for x, w in enumerate(actual)) for phase in range(-1, 16))
                total_rows += 192
                total_words += len(words)
                words_by_frame[frame] = words
            images[label], sources[label] = shots, words_by_frame
            movie = FlsArchive(rom.read_file(config['movie']))
            assert {s['frame'] for s in report['read_only_capture_GPU_states']} == set(config['GPU_and_native_frames'])
            for state in report['read_only_capture_GPU_states']:
                frame = state['frame']
                committed = checked_export(state, exporter)
                raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
                assert sha(raw) == state['main_RAM_sha256']
                cpu = machine(rom.read_file('/__arm9__.bin'))
                cpu.mem_write(BASE, raw)
                call(cpu, 0x7F244, ())
                assert cpu.reg_read(UC_ARM_REG_R0) == config['captain']
                header = 0x02276D74 - BASE
                flags, width, height, paloff, pixoff = struct.unpack_from('<5I', raw, header)
                assert (flags, width, height) == struct.unpack_from('<3I', decoded)
                assert raw[header + paloff:header + paloff + 512] == palette_bytes
                assert raw[header + pixoff:header + pixoff + 49152] == picture.indices
                if route == 'hodram' and label == 'current' and frame == 3118:
                    native = next(n for n in report['read_only_capture_native_states'] if n['frame'] == frame)
                    assert native['read_only_export'] and not native['state_loaded'] and native['main_RAM_unchanged_by_export']
                    for field in native['regions'].values():
                        assert sha(Path(field['path']).read_bytes()) == field['sha256']
                    stripe_control = hodram_stripe_control(rom, code['clean'], raw, native, photo)
                bindings, textures = vram_bindings(committed, movie)
                ordered, order = render_order(committed)
                backdrop, draws = compose(ordered, movie, bindings)
                renderer = Path(state['files']['gpu_framebuffer_RGBA8888.bin']['path']).read_bytes()
                diagnostic = rgb([renderer[i] >> 3 | (renderer[i + 1] >> 3) << 5 | (renderer[i + 2] >> 3) << 10
                                  for i in range(0, len(renderer), 4)])
                assert diagnostic == backdrop
                expected = [photo_rgb[i] if w & 32768 else backdrop[i] for i, w in enumerate(words_by_frame[frame])]
                assert expected == pixels(shots[frame])[:49152]
                source_models[label, frame] = expected
                states.append({'route': route, 'build': label, 'frame': frame,
                    'whole49152_upper_RGB_pixels_exact': True,
                    'source_photo_all512_palette_bytes_and49152_indices_exact_in_actual_header': True,
                    'source_bound_actual_captain_getter': config['captain'],
                    'original_ROM_texture_bindings': textures, 'render_order': order, 'native_draws': draws,
                    'opacity_observed_before_original_RenderLine_not_PNG_or_finished_framebuffer': True,
                    '3D_framebuffer_checked_only_as_diagnostic_not_used_as_expected_art': True,
                    'no_delay_fitting_screenshot_phase_selection_or_waived_pixels': True})
            reports[label] = {'observed': str(rp), 'observed_sha256': sha(rp.read_bytes()),
                'baseline': str(bp), 'baseline_sha256': sha(bp.read_bytes()),
                'observer': str(op), 'observer_sha256': sha(op.read_bytes()), 'bound_host_entry_calls': binding}
        differences = []
        for frame in images['current']:
            now, old = pixels(images['current'][frame]), pixels(images['clean'][frame])
            delta = [i for i, (a, b) in enumerate(zip(now, old, strict=True)) if a != b]
            matching_clean_frames += not delta
            if delta:
                assert route == 'lil' and frame == 2865 and len(delta) == 63
                assert {i // 256 for i in delta} == {79} and all(i % 4 == 3 for i in delta)
            differences.append({'frame': frame, 'positions': delta, 'RGB_differences': len(delta)})
        for frame in config['GPU_and_native_frames']:
            assert source_models['current', frame] == source_models['clean', frame]
        if route == 'lil':
            for label in roms:
                older = read(scanline['reports'][label]['scanline_observer'])
                old_shots = {s['frame']: s for s in read(scanline['reports'][label]['observed'])['frames_captured']}
                for frame in config['scanline_frames']:
                    source = older['frames'][str(frame)]['files']['bitmap_row']
                    assert struct.pack('<49152H', *sources[label][frame]) == Path(source['path']).read_bytes()
                    assert pixels(images[label][frame]) == pixels(old_shots[frame])
        routes[route] = {'reports': reports, 'source_picture': config['picture'],
            'source_file_sha256': sha(image_file), 'source_indices_sha256': sha(picture.indices),
            'all_inherited_native_painter_instruction_words_current_clean_exact': sorted(instructions),
            'original_six_state_frame_set': config['GPU_and_native_frames'],
            'current_clean_whole_two_screen_comparisons': differences,
            'all_six_actual_states_exact_source_RGB_in_both_builds': True}
        save(ROOT / 'verification_progress.json', {'routes': routes, 'source_case_count': len(states), 'not_final': True})
        print(route, 'six complete source states in both builds pass; native rows/baselines pass.', flush=True)
    assert len(states) == 36 and len(pairs) == 72
    assert total_rows == 10368 and total_words == 2654208 and matching_clean_frames == 35
    assert stripe_control is not None
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'twelve_terminal_ordinary_New_Game_cold_boots_no_savestate_or_gameplay_fixtures': True,
        'routes': routes, 'all72_whole_two_screen_observer_vs_unmodified_core_pairs': pairs,
        'all10368_original_before_read_scanline_IO_CPU_and_source_row_records': True,
        'all2654208_bitmap_source_words_exact_original_photo_or_original_transparency_pattern': True,
        'all18_original_boundary_state_frames_exact_source_RGB_in_current_and_clean': states,
        'complete_independent_upper_RGB_comparisons': len(states) * 49152,
        'pre_boundary_Hodram3117_six_of_eight_stripes_match_complete_original_native_control': stripe_control,
        'all_sixteen_phase_family_and_actual_painter_code_preserved_from_V648': True,
        'Lil2865_same63_pixel_edge_and_all_source_scanline_rows_reproduce_V659': True,
        'all_three_named_V647_V648_boundary_comparisons_now_have_same_frame_source_evidence': True,
        'no_universal_delay_fit_no_screenshot_selected_expected_source_no_pixel_waiver': True,
        'host_diagnostic_entry_detours_disclosed_bounded_restored_and_Dll_file_unchanged': True,
        'no_entire_movie_every_DMA_cycle_physical_hardware_or_full_campaign_claim': True,
        'remaining_legacy_control_card_material_equipment_and_acceptance_gates_open': True,
        'all18_original_plaques_incomplete22_historical_scopes_retained': True,
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'full_goal_complete': False,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__),
            Path('scripts/run_transition_boundaries_v660.py'), Path('scripts/run_lil_transition_states_v660.py'),
            Path('scripts/observe_transition_scanlines_v659.py'), Path('scripts/verify_transition_scanlines_v659.py'))},
        'prior_transition_proof_sha256': pre['prior_transition_proof_sha256'],
        'prior_scanline_proof_sha256': pre['prior_scanline_proof_sha256']}
    save(ROOT / 'proof.json', proof)
    print('V660: all18 retained boundary states/36 complete source RGB compositions;72 full baselines;10368 actual source scanlines pass.')


if __name__ == '__main__':
    main()
