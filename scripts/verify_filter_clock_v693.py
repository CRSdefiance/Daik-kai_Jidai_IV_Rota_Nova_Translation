"""Predict complete same-frame bitmap/RGB output from clocks and DMA commands."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE_SHA, SOURCE
from scripts.probe_button_prompt_native import call, machine
from scripts.run_filter_predecessors_v693 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_transition_scanlines_v659 import core_entries, prologue_controls
from scripts.verify_village_wrap_v608 import read, save


def checked_bytes(item):
    data = Path(item['path']).read_bytes()
    assert sha(data) == item['sha256']
    return data


def images(report):
    result = {}
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        im = Image.open(path).convert('RGB')
        if row['frame'] in result:
            assert result[row['frame']].tobytes() == im.tobytes()
        result[row['frame']] = im
    return result


def clock_cases(events, arm):
    period, threshold = struct.unpack_from('<2I', arm, 0xFEC)
    assert (period, threshold) == (0x88FA4, 0x77DAF)
    result = []
    for index, paint in enumerate(events['paints']):
        phases = []
        for item in paint['clocks']:
            u = machine(arm)
            u.mem_write(0x02170374, struct.pack('<Q', item['origin']))
            calls = []

            def clock(uc, pc, size, unused, item=item, calls=calls):
                if pc == 0x020E4F98:
                    assert uc.reg_read(UC_ARM_REG_LR) == 0x02000FA8
                    uc.reg_write(UC_ARM_REG_R0, item['tick'] & 0xFFFFFFFF)
                    uc.reg_write(UC_ARM_REG_R1, item['tick'] >> 32)
                    uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
                    calls.append(item['tick'])
            u.hook_add(UC_HOOK_CODE, clock)
            call(u, 0xF9C, ())
            assert calls == [item['tick']]
            delta = (item['tick'] - item['origin']) & 0xFFFFFFFFFFFFFFFF
            expected = int(delta % period < threshold)
            assert u.reg_read(UC_ARM_REG_R0) == expected
            phases.append({'tick': item['tick'], 'origin': item['origin'], 'delta': delta,
                'period': period, 'threshold': threshold, 'original_native_visible_result': expected,
                'complete_original_helper_return_ABI_pass': True})
        result.append({'paint': index, 'entry_frame': paint['entry_frame'], 'phases': phases})
    return result


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    controls = read(pre['inherited_prefix_controls'])
    assert sha(Path(pre['inherited_prefix_controls']).read_bytes()) == pre['inherited_prefix_controls_sha256']
    assert len(controls['native_host_cases']) == 15 and len(controls['read_policy_cases']) == 8
    host_controls = prologue_controls()
    assert len(host_controls) == 12
    save(ROOT / 'scanline_prefix_controls.json', host_controls)
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    clean_machine = machine(clean_arm)
    current_machine = machine(NdsImage.open(pre['cases']['current_full']['ROM']).read_file('/__arm9__.bin'))
    dma_code = bytes(clean_machine.mem_read(0x01FF9894, 0x70))
    assert dma_code == bytes(current_machine.mem_read(0x01FF9894, 0x70))
    assert bytes(clean_machine.mem_read(0x01FF98D0, 8)) == bytes.fromhex('084083e5001092e5')
    # The source copies every immediate-DMA word before scheduling the bus stall.
    mmu = (SOURCE / 'MMU.cpp').read_text(encoding='utf-8')
    block = mmu[mmu.index('void DmaController::doCopy()'):mmu.index('void triggerDma(')]
    assert block.index('_MMU_write16(procnum,MMU_AT_DMA,dst, temp);') < block.index('nds.freezeBus |=')
    source_binding = {'original_DMA_command_after_control_write_PC': 0x01FF98D4,
        'original_clean_current_complete_DMA_setup_code_sha256': sha(dma_code),
        'core_MMU_source': str(SOURCE / 'MMU.cpp'), 'core_MMU_source_sha256': sha((SOURCE / 'MMU.cpp').read_bytes()),
        'complete_immediate_copy_precedes_scheduled_bus_stall_in_pinned_core': True}
    save(ROOT / 'DMA_source_binding.json', source_binding)
    # Every observed run is checked against its own ROM's existing unobserved
    # schedule. No current/source frame is delayed or substituted.
    baseline_checks = []
    for case, old in (('source', 'source_full'), ('current', 'hodram_full'),
                      ('source_full', 'source_full'), ('current_full', 'hodram_full')):
        folder = CAP / ('filter_clock_v693_' + case)
        report_path = folder / 'capture_report.json'
        observed, baseline = read(report_path), read(CAP / ('navigator_filter_v692_' + old) / 'capture_report.json')
        assert observed['frames'] == 15200 and observed['cold_boot'] and not observed['savestate_loaded']
        assert not observed['callback_errors'] and observed['core_DLL_sha256'] == CORE_SHA
        assert observed['ROM_sha256'] == baseline['ROM_sha256']
        assert observed['scripted_input_schedule'] == baseline['scripted_input_schedule']
        assert not any(v for k, v in observed.items() if k.startswith('synthetic_'))
        a, b = images(observed), images(baseline)
        assert b.keys() <= a.keys()
        assert all(a[f].tobytes() == im.tobytes() for f, im in b.items())
        assert (folder / 'final_arm9_ram.bin').read_bytes() == (CAP / ('navigator_filter_v692_' + old) / 'final_arm9_ram.bin').read_bytes()
        baseline_checks.append({'case': case, 'whole_RGB_pairs': len(b),
            'complete_terminal_RAM_exact_to_same_ROM_unobserved_baseline': True,
            'report': str(report_path), 'report_sha256': sha(report_path.read_bytes())})
    cases, clocks, native_count, panels = [], {}, 0, []
    for case in ('source_full', 'current_full'):
        folder = CAP / ('filter_clock_v693_' + case)
        event_path = folder / 'clock_observer/events.json'
        events = read(event_path)
        assert not events['errors'] and not events['mismatches'] and not events['active_call_at_end']
        assert events['no_game_CPU_RAM_VRAM_IO_ITCM_DTCM_writes'] and events['all_host_slots_restored_core_file_exact']
        assert events['producer_sha256'] == pre['observer_sha256']
        native = read(ROOT / (case + '_native_proof.json'))
        assert len(native['cases']) == len(events['paints']) == 8
        native_count += 8
        clocks[case] = clock_cases(events, clean_arm)
        outputs = []
        for row, paint in zip(native['cases'], events['paints'], strict=True):
            assert row['entry_frame'] == paint['entry_frame'] and row['actual_clock_inputs'] == paint['clocks']
            assert row['complete_output_bytes_different_from_actual_return'] == 0
            assert row['bytes_written'] == 98304 and row['output_bytes_read_before_written'] == 0
            assert row['actual_return_registers_match'] and row['actual_return_CPSR_match']
            assert row['all_executed_ARM_ITCM_overlay_and_copied_pool_words_exact_registered_ROM']
            output = Path(row['output']).read_bytes()
            assert sha(output) == row['output_sha256']
            outputs.append(output)
        scan_path = folder / 'scanlines/scanline_observer.json'
        scan = read(scan_path)
        assert scan['all_entry_bytes_restored_and_DLL_file_unchanged'] and not scan['errors']
        assert scan['every_original_RenderLine_called_once'] and scan['no_game_ROM_RAM_VRAM_register_or_input_writes']
        assert scan['script_sha256'] == pre['scanline_observer_sha256']
        for path, digest in scan['source_files'].items():
            assert sha(Path(path).read_bytes()) == digest
        bindings = core_entries(scan)
        assert len(bindings) == 3
        pictures = images(read(folder / 'capture_report.json'))
        for frame in (9600, 10800):
            item = scan['frames'][str(frame)]
            actual = checked_bytes(item['files']['bitmap_row'])
            cpu, io = checked_bytes(item['files']['CPU_registers']), checked_bytes(item['files']['IO'])
            issued = []
            for line, row in enumerate(item['rows']):
                assert (row['frame'], row['line'], row['VCount'], row['format']) == (frame, line, line, '555')
                assert row['original_render_called_once_and_returned']
                registers = struct.unpack_from('<16I', cpu, line * 64)
                if row['ARM9_PC'] == 0x01FF98D4 and registers[5] == 0x06000000:
                    assert registers[4:8] == (0x8000C000, 0x06000000, 0x022E1794, 3)
                    issued.append(line)
                r = io[line * 8192:(line + 1) * 8192]
                assert struct.unpack_from('<I', r)[0] == 0x1191B
                assert struct.unpack_from('<H', r, 14)[0] == 0x4084 and r[0x243] == 0x81
                assert struct.unpack_from('<4h2I', r, 0x30) == (256, 0, 0, 256, 0, line * 256)
                assert struct.unpack_from('<3H', r, 0x50) == (0, 0, 0) and struct.unpack_from('<H', r, 0x6C)[0] == 0
            old_index = max(i for i, p in enumerate(events['paints']) if p['return_frame'] < frame)
            completed_now = [i for i, p in enumerate(events['paints']) if p['return_frame'] == frame]
            if issued:
                assert len(completed_now) == 1
                new_index, switch = completed_now[0], min(issued)
            else:
                assert not completed_now
                new_index, switch = old_index, 192
            # Switch comes only from the original DMA PC/arguments above. Never
            # derive it from pixel disagreement or a shifted screenshot.
            expected = outputs[old_index][:switch * 512] + outputs[new_index][switch * 512:]
            assert expected == actual
            expected_image = Image.new('RGB', (256, 192))
            expected_image.putdata(rgb(struct.unpack('<49152H', expected)))
            observed_image = pictures[frame].crop((0, 192, 256, 384))
            assert expected_image.tobytes() == observed_image.tobytes()
            image_path = ROOT / f'{case}_{frame}_predicted.png'
            expected_image.save(image_path)
            wrong_index = new_index if issued else old_index - 1
            wrong = outputs[wrong_index]
            negative = sum(a != b for a, b in zip(wrong, actual, strict=True))
            assert negative > 0
            cases.append({'case': case, 'frame': frame, 'previous_complete_paint': old_index,
                'same_frame_completed_paint': new_index if issued else None,
                'switch_row_from_original_DMA_PC_and_full_arguments': switch if issued else None,
                'all192_actual_rows_and49152_same_frame_RGB_pixels_exact': True,
                'complete98304_bitmap_bytes_exact': True, 'independent_wrong_phase_control_different_bytes': negative,
                'no_pixel_mask_delay_frame_substitution_or_fitted_switch': True,
                'scanline_evidence': str(scan_path), 'scanline_evidence_sha256': sha(scan_path.read_bytes())})
            panels.append((case, frame, observed_image, expected_image))
    assert [c['switch_row_from_original_DMA_PC_and_full_arguments'] for c in cases] == [55, 97, None, None]
    sheet = Image.new('RGB', (1024, 448), '#263238')
    draw = ImageDraw.Draw(sheet)
    for case, frame, actual, predicted in panels:
        y, col = (0 if frame == 9600 else 224), (0 if case == 'source_full' else 2)
        for offset, im, label in ((0, actual, 'actual'), (1, predicted, 'original native prediction')):
            x = (col + offset) * 256
            draw.text((x + 3, y + 4), f'{case} {frame} {label}', fill='white')
            sheet.paste(im, (x, y + 32))
    review = ROOT / 'same_frame_original_cursor_review.png'
    sheet.save(review)
    save(ROOT / 'clock_decisions.json', clocks)
    save(ROOT / 'proof.json', {'candidate': pre['cases']['current_full']['ROM'],
        'candidate_sha256': pre['cases']['current_full']['ROM_sha256'],
        'all16_complete_original_paints1572864_bytes_and_ABI_registered_code_exact': native_count == 16,
        'all40_actual_SDK_clock_inputs_original_modulo_decisions_verified': sum(len(p['phases']) for r in clocks.values() for p in r) == 40,
        'all4_complete_same_frame_native_bitmap_and_RGB_predictions': cases,
        'whole_baseline_pairs': baseline_checks, 'total_whole_same_ROM_unobserved_pairs': sum(r['whole_RGB_pairs'] for r in baseline_checks),
        'all_four_complete_terminal_RAM_pairs_exact': True,
        'native_host_prefix_controls': 15, 'mirror_controls': 8, 'scanline_host_prefix_controls': 12,
        'source_DMA_binding': source_binding, 'original_V692_87_and1446_highlight_differences_explained': True,
        'specific_V692_cursor_timing_gap_closed_without_ROM_or_artwork_change': True,
        'second_gender_other_graphics_all18_plaques_and_full_goal_still_open': True,
        'review_sheet': str(review), 'review_sheet_sha256': sha(review.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V693:16 complete native paints,40 actual clock inputs,DMA rows55/97,four full RGB planes and152 baseline pairs verified.', flush=True)


if __name__ == '__main__':
    main()
