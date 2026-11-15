"""Independent source-band model, original native paints and actual pre-render rows."""

import struct
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_graphic_paints_v669 import units
from scripts.research_still_reveal_v675 import BASE, ROOT, SIZE
from scripts.run_village_visits_v664 import CAP
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_transition_scanlines_v659 import core_entries, prologue_controls
from scripts.verify_village_wrap_v608 import read, save

ENTRY = CAP / 'still_reveal_v675_before_iterator_v3'
SCAN = CAP / 'still_reveal_v675_scanlines_both'
OLD_SCAN = CAP / 'still_reveal_v675_scanlines'


def checked(path, digest):
    data = Path(path).read_bytes()
    assert sha(data) == digest, path
    return data


def shots(report):
    result = {}
    for shot in report['frames_captured']:
        checked(shot['path'], shot['PNG_sha256'])
        pixels = list(Image.open(shot['path']).convert('RGB').get_flattened_data())
        if shot['frame'] in result:
            assert result[shot['frame']][1] == pixels
        result[shot['frame']] = (shot, pixels)
    return result


def original_span(image, address, size):
    return next(data[address - base:address - base + size] for base, data in units(image)
                if base <= address and address + size <= base + len(data))


def band_words(source, phase):
    assert 0 <= phase <= 8 and len(source) == 49152
    return [value if (index // 256) % 8 < phase else 32768
            for index, value in enumerate(source)]


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        checked(path, digest)
    checked(CORE, CORE_SHA)
    rom, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    source = rom.read_file('/evstill/evstill084.pxl')
    assert source == clean.read_file('/evstill/evstill084.pxl')
    flags, stride, height, paloff, pixoff = struct.unpack_from('<5I', source)
    assert (flags & 255, stride, height) == (8, 128, 192)
    palette = struct.unpack_from('<256H', source, paloff)
    source_words = [palette[index] | 32768 for index in source[pixoff:]]
    family = [band_words(source_words, phase) for phase in range(9)]
    original_code = []
    for address, size in ((0x020280CC, 0x1C0), (0x0202828C, 0x15C),
                          (0x02029150, 16), (0x020D32B8, 0x5C), (0x01FFAF98, 4),
                          (0x01FF9898, 0x74)):
        data = original_span(rom, address, size)
        assert data == original_span(clean, address, size)
        original_code.append({'address': address, 'bytes': size, 'sha256': sha(data)})
    observer = read(ENTRY / 'before_paint/observer.json')
    assert observer['slot_restored_DLL_unchanged'] and not observer['errors'] and not observer['mismatches']
    assert observer['callbacks'] == len(observer['rows']) == 20 and observer['frame'] == 4000
    assert observer['script_sha256'] == sha(Path('scripts/observe_scene_entry_v675.py').read_bytes())
    controls = read(ROOT / 'host_snapshot_controls.json')['cases']
    assert len(controls) == 9
    assert all(c['all_host_registers_flags_stack_exact_original_handler_once_and_emulated_bytes_unchanged']
               for c in controls)
    replay = read(ROOT / 'before_entry_replay_research.json')
    assert [r['event'] for r in replay] == observer['rows']
    native, phases = [], set()
    for case in replay:
        event = case['event']
        regions = {key: checked(value['path'], value['sha256']) for key, value in event['files'].items()}
        raw = regions['WRAM']
        assert event['CPU_and_all_copied_source_regions_unchanged_by_snapshot']
        checked(event['CPU_prefix'], event['CPU_prefix_sha256'])
        header = 0x02276D74
        words = struct.unpack_from('<5I', raw, header - BASE)
        assert words == (0x108, 128, 192, 20, 0x46ADC)
        assert raw[header + words[3] - BASE:header + words[3] - BASE + 512] == source[paloff:paloff + 512]
        assert raw[header + words[4] - BASE:header + words[4] - BASE + 49152] == source[pixoff:]
        effect = [node for node in case['nodes'] if node['draw'] == 0x02029150]
        assert len(effect) <= 1
        if effect:
            root = effect[0]['node'] - 40
            vt, owner, progress, duration, orientation = struct.unpack_from('<5I', raw, root - BASE)
            geometry_offset = struct.unpack_from('<i', raw, vt - BASE - 12)[0]
            rect = struct.unpack_from('<4i', raw, root + geometry_offset - BASE + 4)
            assert rect == (0, 0, 256, 192) and duration == 64 and orientation == 0
            phase = progress * 8 // duration
            detail = {'root': root, 'vtable': vt, 'owner': owner, 'progress': progress,
                      'duration': duration, 'orientation': orientation, 'source_rectangle': rect}
        else:
            phase, detail = 8, {'effect_node_absent_and_original_complete_source_background': True}
        phases.add(phase)
        output = checked(case['output'], case['output_sha256'])
        actual = list(struct.unpack('<49152H', output))
        assert actual == family[phase], case['frame']
        assert case['error'] is None and case['assigned_bytes'] == SIZE
        assert not case['nonregistered_instruction_words']
        assert case['upper_guard_after'] == 'a5' * 16
        # The adjacent preceding16 bytes are owned by the lower canvas, which
        # the original traversal paints too. They cannot be an unowned guard.
        # Bind all eight writes to the original tiled painter and source state.
        edge = [w for w in case['global_writes'] if 0x022F9784 <= w['address'] < 0x022F9794]
        assert len(edge) == 8
        assert [w['address'] for w in edge] == list(range(0x022F9784, 0x022F9794, 2))
        assert all(w['bytes'] == 2 and w['PC'] == 0x01FFAF98 for w in edge)
        expected_edge = struct.pack('<8H', *[w['value'] for w in edge])
        assert expected_edge == raw[0x022F9784 - BASE:0x022F9794 - BASE]
        assert case['upper_guard_before'] == expected_edge.hex()
        assert case['source_RAM_sha256'] == sha(raw)
        native.append({'frame': case['frame'], 'actual_before_paint_inputs': detail,
            'independent_source_band_phase': phase, 'all49152_native_output_words_exact': True,
            'all98304_output_bytes_assigned_no_prior_output_read_and_trailing_guard_exact': True,
            'preceding_edge_owned_by_lower_canvas_all8_original_tiled_writes_bound': True,
            'current_registered_code_and_overlay_exact_every_executed_word': True,
            'effect_body_and_iterator_original_clean_words_exact': True,
            'after_frame_software_difference_bytes_retained': case['differences_from_after_frame_software_bytes']})
    assert phases == set(range(9))
    # A complete-phase comparison must detect a wrong thickness even where the
    # original court itself contains black pixels. Compare every source word.
    negative_controls = []
    for phase in range(8):
        count = sum(a != b for a, b in zip(family[phase], family[phase + 1], strict=True))
        assert count > 5000
        negative_controls.append({'phase': phase, 'wrong_next_phase_detected_pixels': count})
    reports, maps, contracts = {}, {}, {}
    for tag, folder in (('entry', ENTRY), ('both', SCAN), ('main_only', OLD_SCAN),
                        ('unmodified_baseline', CAP / 'maria_dispatch_v674_baseline')):
        report = read(folder / 'capture_report.json')
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
        assert report['frames'] == 4000 and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors']
        assert report['scripted_input_schedule'] == read('work/analysis/maria_opening_v674/dispatch_inputs.json')
        assert report['battery_save_preloaded']['source_sha256'] == read('work/analysis/maria_opening_v674/preflight.json')['donor_sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        assert {k for k, value in report.items() if k.startswith('synthetic_') and value} == {'synthetic_gallery_fixtures'}
        if tag != 'unmodified_baseline':
            contract = read(folder / 'run_contract.json')
            runner = {'entry': Path('scripts/run_still_reveal_v675.py'),
                      'both': Path('scripts/run_still_scanlines_v675.py'),
                      'main_only': ROOT / 'initial_main_only_scanline_runner.py'}[tag]
            parent = {'entry': Path('scripts/observe_scene_entry_v675.py'),
                      'both': Path('scripts/observe_still_scanlines_v675.py'),
                      'main_only': Path('scripts/observe_transition_scanlines_v659.py')}[tag]
            assert sha(runner.read_bytes()) == contract['runner_sha256']
            assert sha(parent.read_bytes()) == contract['observer_sha256']
            assert contract['inputs_sha256'] == sha(Path('work/analysis/maria_opening_v674/dispatch_inputs.json').read_bytes())
        reports[tag], maps[tag] = report, shots(report)
        contracts[tag] = {'path': str(folder / 'capture_report.json'),
                          'sha256': sha((folder / 'capture_report.json').read_bytes())}
    pairs = []
    for tag in ('both', 'main_only', 'unmodified_baseline'):
        for frame, (shot, pixels) in maps[tag].items():
            assert maps['entry'][frame][1] == pixels, (tag, frame)
            pairs.append({'compared_to': tag, 'frame': frame, 'all98304_two_screen_RGB_pixels_exact': True})
    assert len({sha((folder / 'final_arm9_ram.bin').read_bytes()) for folder in
                (ENTRY, SCAN, OLD_SCAN, CAP / 'maria_dispatch_v674_baseline')}) == 1
    scan = read(SCAN / 'scanlines/scanline_observer.json')
    assert scan['all_entry_bytes_restored_and_DLL_file_unchanged'] and not scan['errors']
    assert scan['script_sha256'] == sha(Path('scripts/observe_still_scanlines_v675.py').read_bytes())
    assert scan['parent_observer_sha256'] == sha(Path('scripts/observe_transition_scanlines_v659.py').read_bytes())
    assert scan['no_game_ROM_RAM_VRAM_register_or_input_writes'] and scan['every_original_RenderLine_called_once']
    native_entries, prefix_cases = core_entries(scan), prologue_controls()
    display_cases = []
    for key, value in scan['frames'].items():
        frame = int(key)
        data = {name: checked(item['path'], item['sha256']) for name, item in value['files'].items()}
        upper = list(struct.unpack('<49152H', data['sub_bitmap_row']))
        lower = list(struct.unpack('<49152H', data['bitmap_row']))
        io = data['IO']
        assert len(value['rows']) == 192
        for line, row in enumerate(value['rows']):
            assert (row['line'], row['VCount'], row['frame'], row['format']) == (line, line, frame, '555')
            assert row['original_render_called_once_and_returned']
            registers = io[line * 8192:(line + 1) * 8192]
            assert registers[0x242] == 0x84 and registers[0x243] == 0x81
            assert struct.unpack_from('<I', registers, 0x1000)[0] == 0x11813
            assert struct.unpack_from('<H', registers, 0x100E)[0] == 0x4084
            assert struct.unpack_from('<4h2I', registers, 0x1030) == (256, 0, 0, 256, 0, line * 256)
            assert struct.unpack_from('<3H', registers, 0x1050) == (0, 0, 0)
            assert struct.unpack_from('<H', registers, 0x106C)[0] == 0
        # Whole-frame phase is selected from the source bitmap before rendering,
        # never from a screenshot or a later software buffer. Mixed frames are
        # independently predicted from the actual original DMA transfer inputs.
        selected = [phase for phase, model in enumerate(family) if upper == model]
        assert len(selected) <= 1
        mixed = None
        if selected:
            phase = selected[0]
            expected_words = family[phase]
        else:
            current = next(item for item in native if item['frame'] == frame)['independent_source_band_phase']
            assert (frame, current) in ((3762, 1), (3786, 4))
            # The first observed upper channel3 transfer determines the change
            # from the preceding complete phase to this native paint's phase.
            # Before it the CPU is painting or transferring lower/OBJ memory;
            # after completion it may return to the kernel. No PNG/bitmap pixel
            # or hard-coded scanline chooses this boundary.
            upper_dma_lines = []
            for line, row in enumerate(value['rows']):
                regs = struct.unpack_from('<16I', data['CPU_registers'], line * 64)
                if row['ARM9_PC'] == 0x01FF98D4 and (regs[5], regs[6]) == (0x06200000, 0x022F9794):
                    upper_dma_lines.append(line)
            assert upper_dma_lines
            boundary = min(upper_dma_lines)
            assert upper_dma_lines == list(range(boundary, max(upper_dma_lines) + 1))
            expected_words, row_phases, transfer_inputs = [], [], []
            for line, row in enumerate(value['rows']):
                regs = struct.unpack_from('<16I', data['CPU_registers'], line * 64)
                pc = row['ARM9_PC']
                assert original_span(rom, pc, 4) == original_span(clean, pc, 4)
                if line in upper_dma_lines:
                    assert (regs[3], regs[4], regs[7]) == (0x040000D4, 0x8000C000, 3)
                phase = current if line >= boundary else current - 1
                row_phases.append(phase)
                expected_words.extend(family[phase][line * 256:(line + 1) * 256])
                transfer_inputs.append({'line': line, 'original_PC': pc, 'R6': regs[6], 'R5': regs[5],
                                        'channel': regs[7], 'count_and_control': regs[4]})
            assert upper == expected_words, frame
            mixed = {'current_before_paint_phase': current, 'previous_phase': current - 1,
                     'first_observed_upper_DMA_line': boundary,
                     'last_observed_upper_DMA_line': max(upper_dma_lines),
                     'all192_original_CPU_positions_and_register_inputs': transfer_inputs,
                     'all49152_source_words_predicted_from_original_DMA_and_native_paint_inputs': True}
            phase = None
        expected = rgb(expected_words)
        assert expected == maps['both'][frame][1][:49152], frame
        assert rgb(lower) == maps['both'][frame][1][49152:], frame
        display_cases.append({'frame': frame, 'observed_source_whole_bitmap_phase': phase,
            'all49152_source_words_exact_original_court_and_band_geometry': True,
            'all49152_independent_source_RGB_pixels_exact_actual_upper_display': True,
            'all49152_lower_pixels_match_separate_main_engine_diagnostic': True,
            'mixed_source_frame_original_DMA_prediction': mixed,
            'phase_from_actual_pre_render_source_no_PNG_fitting_or_frame_delay': True,
            'not_an_independent_prediction_of_all_CPU_DMA_clock_cycles': True})
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['release_hashes'][pre['candidate']],
        'previous_goal_turn_classification': 'no progress: status answer only; revalidated terminal capture and continued source/display verification',
        'original_source': '/evstill/evstill084.pxl', 'original_source_sha256': sha(source),
        'original_painter_thunk_iterator_and_blocking_loop': original_code,
        'all20_actual_before_paint_native_replays': native, 'all9_band_phases_covered': True,
        'whole_native_output_words_compared': len(native) * 49152,
        'wrong_thickness_negative_controls': negative_controls, 'nine_native_host_selection_ABI_controls': controls,
        'report_contracts': contracts, 'full_two_screen_pairs': pairs, 'four_terminal_RAM_states_exact': True,
        'pre_RenderLine_host_source_bindings': native_entries, 'twelve_host_prefix_relocation_controls': prefix_cases,
        'actual_upper_source_and_display_cases': display_cases,
        'all_source_scanlines': len(display_cases) * 192,
        'whole_upper_source_RGB_comparisons': len(display_cases) * 49152,
        'specific_V674_blank_and_reveal_comparisons_resolved_without_ROM_change': True,
        'initial_main_engine_only_observer_proved_lower_screen_not_used_for_upper_claim': True,
        'initial_whole_frame_phase_and_preceding_guard_assumptions_rejected_with_original_ownership': True,
        'mixed_frames_predicted_from_native_inputs_and_first_original_upper_DMA_at_lines68_and143': True,
        'missing_overlay_and_wrong_instruction_and_duplicate_tag_failures_retained': True,
        'no_global_transition_hardware_full_Maria_opening_or_M26_ownership_claim': True,
        'all18_plaques_incomplete22_original_requirements_retained': True, 'full_goal_complete': False,
        'verifier_sha256': sha(Path(__file__).read_bytes())})
    print('V675 independent native band paints and actual source scanline RGB verification passed.', flush=True)


if __name__ == '__main__':
    main()
