"""Verify both actual Arcadius flag states, bounded fixtures and complete cells."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.probe_button_prompt_native import call, machine
from scripts.replay_room_gender_v694 import cpu
from scripts.run_gender_exception_v697 import (
    ACTOR,
    BASE,
    CAP,
    FLAG_MASK,
    FLAG_OBJECT,
    FLAG_WORD,
    ROM,
    ROOT,
    VIEW,
)
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_raw_portrait_tail_v689 import pictures
from scripts.verify_room_gender_v694 import marker_cell
from scripts.verify_village_wrap_v608 import read, save


def word(raw, address):
    return struct.unpack_from('<I', raw, address - BASE)[0]


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    assert sha(CORE.read_bytes()) == CORE_SHA
    assert pre['producer_sha256'] == sha(Path('scripts/run_gender_exception_v697.py').read_bytes())
    assert pre['inputs_sha256'] == sha((ROOT / 'inputs.json').read_bytes())
    assert pre['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    controls = read(ROOT / 'prefix_controls/native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 45 and len(controls['read_policy_cases']) == 8
    native = read(ROOT / 'native_prefix_proof.json')
    assert native['replayer_sha256'] == sha(Path('scripts/replay_gender_exception_v697.py').read_bytes())
    assert len(native['cases']) == 2 and all(r['all7_actual_R0_R14_CPSR_RAM_DTCM_ITCM_checkpoints_exact'] for r in native['cases'])
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    original_machine = machine(NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    marker_bytes = rom.read_file('/_pxl/__marker.pxl')
    marker = PxlImage.from_bytes(marker_bytes)
    frames = {1, 60, 180, 1600, *range(2000, 10801, 400)}
    shots, memories, events, reports = {}, {}, {}, []
    source_cases, cells, pairs = [], [], []
    for flag in (0, 1):
        for suffix in ('observed', 'baseline'):
            case = f'flag{flag}_{suffix}'
            folder = CAP / ('gender_exception_v697_' + case)
            rp = folder / 'capture_report.json'
            report, contract = read(rp), read(folder / 'run_contract.json')
            assert report['frames'] == 10800 and report['cold_boot'] and not report['savestate_loaded']
            assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
            assert not report['callback_errors'] and not report['hardware_device_verification']
            assert report['scripted_input_schedule'] == read(ROOT / 'inputs.json')
            assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
            assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
            fixture = report['synthetic_actor8_gender_story_flag_fixture']
            assert fixture['flag9'] == flag and fixture['actor_and_flag_inputs_restored_before_exit']
            assert not fixture['earned_recruitment_or_story_progress']
            assert {k for k, v in report.items() if k.startswith('synthetic_') and v} == {'synthetic_actor8_gender_story_flag_fixture'}
            ep = folder / 'observer/events.json'
            assert sha(ep.read_bytes()) == fixture['events_sha256']
            event = read(ep)
            assert event['producer_sha256'] == contract['producer_sha256'] == pre['producer_sha256']
            assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
            assert event['source_contract_sha256'] == pre['source_contract_sha256']
            assert event['all_host_slots_restored_core_file_exact'] and not event['errors'] and not event['mismatches']
            assert event['flag_value'] == flag and event['extra_observer_enabled'] == (suffix == 'observed')
            assert event['recorded_state_read_only_except_declared_install_and_restore']
            orig = event['original_inputs']
            assert orig['actor_cell'] == VIEW + 0x18 and orig['actor'] == 1
            assert not orig['flag_word'] & FLAG_MASK
            writes = event['fixture_writes']
            assert [r['kind'] for r in writes] == ['install', 'restore'] and writes[1]['frame'] == 10001
            for row in writes:
                before, after = [Path(row[n]).read_bytes() for n in ('before', 'after')]
                assert sha(before) == row['before_sha256'] and sha(after) == row['after_sha256']
                desired = {int(k): v for k, v in row['declared_word_values'].items()}
                expected = bytearray(before)
                assert set(desired) == {orig['actor_cell'], FLAG_WORD}
                for address, value in desired.items():
                    struct.pack_into('<I', expected, address - BASE, value)
                assert after == expected and row['CPU_DTCM_ITCM_unchanged_and_all_other_RAM_bytes_exact']
                if row['kind'] == 'install':
                    assert desired[orig['actor_cell']] == ACTOR
                    assert desired[FLAG_WORD] == (orig['flag_word'] | (FLAG_MASK if flag else 0))
                else:
                    assert desired == {orig['actor_cell']: 1, FLAG_WORD: orig['flag_word']}
            shots[case] = pictures(report)
            assert set(shots[case]) == frames
            memories[case] = {}
            for row in report['read_only_capture_RAM_snapshots']:
                raw = Path(row['path']).read_bytes()
                assert len(raw) == 0x400000 and sha(raw) == row['sha256']
                if row['frame'] in memories[case]:
                    assert memories[case][row['frame']] == raw
                memories[case][row['frame']] = raw
            assert set(memories[case]) == frames
            assert word(memories[case][10800], FLAG_WORD) == orig['flag_word']
            events[case] = event
            reports.append({'case': case, 'path': str(rp), 'sha256': sha(rp.read_bytes()),
                            'declared_fixture_writes': 2, 'complete_captured_images': 27})
        observed, baseline = f'flag{flag}_observed', f'flag{flag}_baseline'
        assert all(shots[observed][f].tobytes() == shots[baseline][f].tobytes() for f in frames)
        assert all(memories[observed][f] == memories[baseline][f] for f in frames)
        final = [CAP / ('gender_exception_v697_' + name) / 'final_arm9_ram.bin' for name in (observed, baseline)]
        assert final[0].read_bytes() == final[1].read_bytes()
        for a, b in zip(events[observed]['fixture_writes'], events[baseline]['fixture_writes'], strict=True):
            for field in ('before', 'after'):
                assert Path(a[field]).read_bytes() == Path(b[field]).read_bytes()
        pairs.append({'flag9': flag, 'whole_RGB_pairs': 27, 'whole_capture_RAM_pairs': 27,
                      'complete_terminal_RAM_and_both_install_restore_full_memory_pairs_exact': True})
        row_list = events[observed]['rows']
        assert [r['kind'] for r in row_list] == ['selection_entry', 'helper_entry', 'raw_gender', 'identity',
            'flag_entry', 'flag_return', 'view_ready', 'helper_return', 'gender_draw']
        rows = {r['kind']: r for r in row_list}
        for row in row_list:
            for field in ('RAM', 'DTCM', 'ITCM'):
                assert sha(Path(row[field]).read_bytes()) == row[field + '_sha256']
        assert cpu(rows['helper_entry'])[6] == ACTOR
        assert cpu(rows['raw_gender'])[4] == 1 and cpu(rows['identity'])[4] == ACTOR
        assert cpu(rows['flag_entry'])[4:6] == (FLAG_OBJECT, 9)
        assert cpu(rows['flag_entry'])[18] == 0x02015868
        assert cpu(rows['flag_return'])[4] == (FLAG_MASK if flag else 0)
        assert cpu(rows['view_ready'])[12] == flag
        draw = rows['gender_draw']
        raw = Path(draw['RAM']).read_bytes()
        registers = cpu(draw)
        assert registers[5] == 0x0218DFCC
        assert struct.unpack_from('<2i', raw, registers[7] - BASE) == (80, 80)
        view = struct.unpack_from('<12I', raw, registers[5] - BASE)
        assert view[5] == 4 and view[7:9] == ((232, 96), (240, 112))[flag]
        assert view[9] & 255 == 48 and view[10:12] == (16, 16)
        u = machine(arm)
        u.mem_write(BASE, raw)
        executed = call(u, 0xD6558, (view[3],))
        header = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(header, len(marker_bytes))) == marker_bytes
        assert all(bytes(u.mem_read(pc, 4)) == bytes(original_machine.mem_read(pc, 4)) for pc in executed)
        source_cases.append({'flag9': flag, 'raw_gender': 1, 'identity': ACTOR,
            'original_getter_return': FLAG_MASK if flag else 0, 'actual_selector': flag,
            'actual_draw_view': registers[5], 'actual_draw_point': [80, 80], 'view_words': list(view),
            'whole_actual_cached_Marker_bytes': len(marker_bytes), 'whole_cached_Marker_sha256': sha(marker_bytes),
            'original_cache_getter_complete_ABI_no_bridge': True, 'getter_instructions': len(executed)})
        for frame in (8800, 9200, 9600, 10000):
            image, raw = shots[observed][frame], memories[observed][frame]
            assert word(raw, VIEW + 0x18) == ACTOR
            assert bool(word(raw, FLAG_WORD) & FLAG_MASK) == bool(flag)
            selected = struct.unpack_from('<12I', raw, 0x0218DFCC - BASE)
            assert selected[7:9] == view[7:9] and selected[9] & 255 == 48
            pixels = [native5(image.getpixel((80 + x, 80 + y))) for y in range(16) for x in range(16)]
            expected = marker_cell(marker, 48, flag)
            assert pixels == expected
            assert pixels != marker_cell(marker, 48, 1 - flag) and pixels != marker_cell(marker, 0, flag)
            shifted = [native5(image.getpixel((81 + x, 80 + y))) for y in range(16) for x in range(16)]
            assert shifted != expected
            cells.append({'flag9': flag, 'frame': frame, 'complete256_native5_pixels_exact': True,
                          'wrong_sex_palette_and_shift_controls_fail': True})
    a, b = shots['flag0_observed'], shots['flag1_observed']
    before = sorted(f for f in frames if f <= 8400)
    assert len(before) == 21 and all(a[f].tobytes() == b[f].tobytes() for f in before)
    assert all(a[f].tobytes() == b[f].tobytes() for f in (10400, 10800))
    male, female = marker_cell(marker, 48, 0), marker_cell(marker, 48, 1)
    expected_diff = {(80 + i % 16, 80 + i // 16) for i, (x, y) in enumerate(zip(male, female, strict=True)) if x != y}
    assert len(expected_diff) == 25
    for frame in (8800, 9200, 9600, 10000):
        actual_diff = {(i % 256, i // 256) for i, (x, y) in enumerate(zip(a[frame].get_flattened_data(), b[frame].get_flattened_data(), strict=True)) if x != y}
        assert actual_diff == expected_diff
    sheet = Image.new('RGB', (768, 960), '#263238')
    draw = ImageDraw.Draw(sheet)
    for row, flag in enumerate((0, 1)):
        for col, frame in enumerate((8800, 10000, 10400)):
            x, y = col * 256, row * 480
            draw.text((x + 5, y + 5), f'Flag9={flag}, {frame}' + (' restored' if frame == 10400 else ' fixture'), fill='white')
            image = shots[f'flag{flag}_observed'][frame]
            sheet.paste(image, (x, y + 24))
            if frame != 10400:
                sheet.paste(image.crop((80, 80, 96, 96)).resize((48, 48), Image.Resampling.NEAREST), (x + 5, y + 416))
                draw.text((x + 61, y + 430), 'Symbol at 3x', fill='white')
    sp = ROOT / 'Arcadius_both_original_flag_states_and_restored_return.png'
    sheet.save(sp)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'actual_Arcadius_identity8_story_flag9_exception_in_second_room_parent_verified': True,
        'original_raw_gender1_both_states_processed_male0_then_female1': source_cases,
        'four_declared_fixture_cold_boot_runs': reports, 'matched_observer_and_minimal_fixture_pairs': pairs,
        'total_whole_RGB_and_capture_RAM_pairs': 54, 'complete_actual_symbol_cells': cells,
        'complete_actual_native5_symbol_pixels': 2048,
        'all4_hold_full_RGB_differences_exact25_source_predicted_gender_pixels_only': True,
        'all21_pre_fixture_and2_post_restore_whole_RGB_cross_state_pairs_exact': True,
        'all4_runs_install_and_restore_only_selected_lookup_word_and_story_flag9_bit': True,
        'original_donor_ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
        'both_original_selection_to_gender_construction_prefixes14_complete_state_checkpoints_exact': True,
        'native_prefix_proof': str(ROOT / 'native_prefix_proof.json'),
        'native_prefix_proof_sha256': sha((ROOT / 'native_prefix_proof.json').read_bytes()),
        'not_earned_recruitment_or_story_progress_not_full_info_suffix_equivalence': True,
        'embedded_copy_other_parent_states_and_all18_plaques_remain_open': True,
        'review_sheet': str(sp), 'review_sheet_sha256': sha(sp.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V697 Arcadius original flag9 exception: both actual selectors, eight complete symbol cells,54 whole RGB/RAM pairs,25 source-predicted changed pixels and restored inputs verified.', flush=True)


if __name__ == '__main__':
    main()
