"""Verify captured Sailor Info symbols and plaques, retaining native replay gaps."""

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
from scripts.run_gender_exception_v697 import ACTOR, BASE, FLAG_MASK, FLAG_OBJECT, FLAG_WORD
from scripts.run_person_gender_v698 import CAP, FRAMES, ROM, ROOT, VIEW_OFFSET, word
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_raw_portrait_tail_v689 import pictures
from scripts.verify_room_gender_v694 import class_name, marker_cell
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, field in ((Path('scripts/run_person_gender_v698.py'), 'producer_sha256'),
                        (Path(pre['fixture_methods_source']), 'fixture_methods_sha256'),
                        (ROOT / 'inputs.json', 'inputs_sha256'),
                        (ROOT / 'source_contract.json', 'source_contract_sha256'),
                        (Path(pre['donor']), 'donor_sha256')):
        assert sha(path.read_bytes()) == pre[field], path
    assert sha(CORE.read_bytes()) == CORE_SHA
    source = read(ROOT / 'source_contract.json')
    assert sha(Path(source['native_input_controls_inherited']).read_bytes()) == source['native_input_controls_sha256']
    controls = read(ROOT / 'prefix_controls/native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 45 and len(controls['read_policy_cases']) == 8
    failure = read(ROOT / 'native_flag0_call1_failure.json')
    assert failure == {'error': 'UcError()', 'PC': 0x020E31E4, 'reached': ['update_entry', 'actor_ready']}
    assert not (ROOT / 'native_prefix_proof.json').exists()
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean_machine = machine(NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    assert arm[0x80440:0x804E4] == NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')[0x80440:0x804E4]
    marker_bytes = rom.read_file('/_pxl/__marker.pxl')
    marker = PxlImage.from_bytes(marker_bytes)
    plaque_contract = Path('translations/source_plaque_grain_v1.json')
    plaque_record = next(r for r in read(plaque_contract)['files'] if r['file_path'] == '/_pxl/personinfo.pxl')
    plaque_bytes = rom.read_file(plaque_record['file_path'])
    # The V542 grain target predates the registered bevel/frame repairs.
    # V671 reviewed this complete V666 asset against original/current native crops.
    reviewed_rom = Path('out/all_routes_combined_v666_candidate.nds')
    assert sha(reviewed_rom.read_bytes()) == '706350a55a058b7a87b67d396333ed397dac664ba36ea378161d18fd085ba121'
    assert plaque_bytes == NdsImage.open(reviewed_rom).read_file(plaque_record['file_path'])
    plaque = PxlImage.from_bytes(plaque_bytes)
    assert len(plaque_record['records']) == 10
    shots, memories, events, reports, pairs, sources, cells, plaques = {}, {}, {}, [], [], [], [], []
    for flag in (0, 1):
        for suffix in ('observed', 'baseline'):
            case = f'flag{flag}_{suffix}'
            folder = CAP / ('person_gender_v698_screen1_' + case)
            rp, ep = folder / 'capture_report.json', folder / 'observer/events.json'
            report, event, contract = read(rp), read(ep), read(folder / 'run_contract.json')
            assert report['frames'] == 7800 and report['cold_boot'] and not report['savestate_loaded']
            assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
            assert not report['callback_errors'] and not report['hardware_device_verification']
            assert report['scripted_input_schedule'] == read(ROOT / 'inputs.json')
            assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
            assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
            fixture = report['synthetic_Arcadius_Sailor_Info_flag_fixture']
            assert fixture['flag9'] == flag and fixture['selected_lookup_and_flag_inputs_restored_before_exit']
            assert not fixture['earned_actor_recruitment_or_story_reveal']
            assert {k for k, v in report.items() if k.startswith('synthetic_') and v} == {'synthetic_Arcadius_Sailor_Info_flag_fixture'}
            assert fixture['events_sha256'] == sha(ep.read_bytes())
            assert event['producer_sha256'] == contract['producer_sha256'] == pre['producer_sha256']
            assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
            assert event['source_contract_sha256'] == pre['source_contract_sha256']
            assert event['all_host_slots_restored_core_file_exact'] and not event['errors'] and not event['mismatches']
            assert event['flag_value'] == flag and event['extra_observer_enabled'] == (suffix == 'observed')
            assert event['recorded_state_read_only_except_declared_install_and_restore']
            orig = event['original_inputs']
            assert orig['parent'] == 0x02189E24 and orig['array'] == orig['actor_cell'] == 0x02190A58
            assert orig['count'] == 5 and orig['actor'] == 1 and orig['flag_word'] == 1
            writes = event['fixture_writes']
            assert [(r['kind'], r['frame']) for r in writes] == [('install', 5913), ('restore', 7401)]
            for row in writes:
                before, after = [Path(row[n]).read_bytes() for n in ('before', 'after')]
                assert sha(before) == row['before_sha256'] and sha(after) == row['after_sha256']
                expected = bytearray(before)
                desired = {int(k): v for k, v in row['declared_word_values'].items()}
                assert set(desired) == {orig['actor_cell'], FLAG_WORD}
                for address, value in desired.items():
                    struct.pack_into('<I', expected, address - BASE, value)
                assert after == expected and row['CPU_DTCM_ITCM_unchanged_and_all_other_RAM_bytes_exact']
                target = {orig['actor_cell']: ACTOR, FLAG_WORD: orig['flag_word'] | (FLAG_MASK if flag else 0)}
                if row['kind'] == 'restore':
                    target = {orig['actor_cell']: 1, FLAG_WORD: orig['flag_word']}
                assert desired == target
            shots[case] = pictures(report)
            assert set(shots[case]) == set(FRAMES)
            memories[case] = {}
            for row in report['read_only_capture_RAM_snapshots']:
                raw = Path(row['path']).read_bytes()
                assert len(raw) == 0x400000 and sha(raw) == row['sha256']
                if row['frame'] in memories[case]:
                    assert memories[case][row['frame']] == raw
                memories[case][row['frame']] = raw
            assert set(memories[case]) == set(FRAMES)
            assert word(memories[case][7800], FLAG_WORD) == orig['flag_word']
            assert word(memories[case][7800], orig['actor_cell']) == 1
            events[case] = event
            reports.append({'case': case, 'path': str(rp), 'sha256': sha(rp.read_bytes()), 'frames': 7800,
                            'capture_frames': len(FRAMES), 'declared_fixture_writes': 2})
        observed, baseline = f'flag{flag}_observed', f'flag{flag}_baseline'
        assert all(shots[observed][f].tobytes() == shots[baseline][f].tobytes() for f in FRAMES)
        assert all(memories[observed][f] == memories[baseline][f] for f in FRAMES)
        final = [CAP / ('person_gender_v698_screen1_' + name) / 'final_arm9_ram.bin' for name in (observed, baseline)]
        assert final[0].read_bytes() == final[1].read_bytes()
        for a, b in zip(events[observed]['fixture_writes'], events[baseline]['fixture_writes'], strict=True):
            assert all(Path(a[n]).read_bytes() == Path(b[n]).read_bytes() for n in ('before', 'after'))
        pairs.append({'flag9': flag, 'whole_RGB_pairs': 21, 'whole_capture_RAM_pairs': 21,
                      'terminal_RAM_and_install_restore_full_memory_pairs_exact': True})
        row_list = events[observed]['rows']
        assert events[observed]['calls'] == 2 and len(row_list) == 18
        for number in (1, 2):
            rows = {r['kind']: r for r in row_list if r['call'] == number}
            assert list(rows) == ['update_entry', 'actor_ready', 'raw_gender', 'identity',
                'flag_entry', 'flag_return', 'processed', 'view_ready', 'gender_draw']
            for row in rows.values():
                for field in ('RAM', 'DTCM', 'ITCM'):
                    assert sha(Path(row[field]).read_bytes()) == row[field + '_sha256']
            assert cpu(rows['raw_gender'])[4] == 1 and cpu(rows['identity'])[4] == ACTOR
            assert cpu(rows['flag_entry'])[4:6] == (FLAG_OBJECT, 9)
            assert cpu(rows['flag_entry'])[18] == 0x02080468
            assert cpu(rows['flag_return'])[4] == (FLAG_MASK if flag else 0)
            assert cpu(rows['processed'])[8] == flag
            ready = rows['view_ready']
            raw = Path(ready['RAM']).read_bytes()
            parent = events[observed]['original_inputs']['parent']
            assert cpu(ready)[14] == parent and class_name(raw, parent) == '22CPersonInformationView'
            view_address = parent + VIEW_OFFSET
            view = struct.unpack_from('<12I', raw, view_address - BASE)
            assert view[3] == 0x02313F74 and view[5] == 4
            assert view[7:9] == ((232, 96), (240, 112))[flag]
            assert view[9] & 255 == 48 and view[10:12] == (16, 16)
            u = machine(arm)
            u.mem_write(BASE, raw)
            executed = call(u, 0xD6558, (view[3],))
            header = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(header, len(marker_bytes))) == marker_bytes
            assert all(bytes(u.mem_read(pc, 4)) == bytes(clean_machine.mem_read(pc, 4)) for pc in executed)
            draw = rows['gender_draw']['actual_original_copy_arguments']
            # Cached storage can move between construction and the later draw.
            # Resolve again from the draw's own RAM rather than equate pointers across frames.
            draw_machine = machine(arm)
            draw_raw = Path(rows['gender_draw']['RAM']).read_bytes()
            draw_machine.mem_write(BASE, draw_raw)
            draw_executed = call(draw_machine, 0xD6558, (view[3],))
            draw_header = draw_machine.reg_read(UC_ARM_REG_R0)
            assert bytes(draw_machine.mem_read(draw_header, len(marker_bytes))) == marker_bytes
            assert draw_raw[draw_header - BASE:draw_header - BASE + len(marker_bytes)] == marker_bytes
            assert all(bytes(draw_machine.mem_read(pc, 4)) == bytes(clean_machine.mem_read(pc, 4)) for pc in draw_executed)
            assert draw == {'screen': 1, 'whole_Marker_header': draw_header, 'source': list(view[7:9]),
                            'size': [16, 16], 'destination': [84, 76]}
            sources.append({'flag9': flag, 'call': number, 'actual_class': class_name(raw, parent),
                'view_address': view_address, 'view_words': list(view), 'original_copy': draw,
                'construction_cached_header': header, 'draw_cached_header': draw_header,
                'whole_cached_Marker_bytes': len(marker_bytes), 'cached_Marker_sha256': sha(marker_bytes),
                'complete_original_cache_getter_ABI_no_bridge': True, 'getter_instructions': len(executed)})
        for frame in (6200, 6600, 7000, 7400):
            image, raw = shots[observed][frame], memories[observed][frame]
            parent = events[observed]['original_inputs']['parent']
            assert class_name(raw, parent) == '22CPersonInformationView'
            array, count, index = [word(raw, parent + n) for n in (4, 8, 12)]
            assert array == 0x02190A58 and count == 5 and index == int(frame == 6600)
            actor = word(raw, array + index * 4)
            assert (actor != ACTOR) if frame == 6600 else (actor == ACTOR)
            selected = struct.unpack_from('<12I', raw, parent + VIEW_OFFSET - BASE)
            sex = 0 if frame == 6600 else flag
            assert selected[7:9] == ((232, 96), (240, 112))[sex]
            assert selected[9] & 255 == 48 and selected[10:12] == (16, 16)
            pixels = [native5(image.getpixel((84 + x, 76 + y))) for y in range(16) for x in range(16)]
            expected = marker_cell(marker, 48, sex)
            assert pixels == expected
            assert pixels != marker_cell(marker, 48, 1 - sex) and pixels != marker_cell(marker, 0, sex)
            assert [native5(image.getpixel((85 + x, 76 + y))) for y in range(16) for x in range(16)] != expected
            cells.append({'flag9': flag, 'frame': frame, 'selected_actor': actor, 'selector': sex,
                          'complete256_native5_pixels_exact': True, 'three_negative_controls_fail': True})
            for record in plaque_record['records']:
                x0, y0, x1, y1 = record['plaque_box']
                for y in range(y0, y1):
                    for x in range(x0, x1):
                        assert native5(image.getpixel((x, y))) == native5(plaque.palette[plaque.indices[y * plaque.width + x]]), (flag, frame, record['english'], x, y)
                plaques.append({'flag9': flag, 'frame': frame, 'id': record['id'], 'english': record['english'],
                                'complete_box': record['plaque_box'], 'native5_pixels': (x1 - x0) * (y1 - y0)})
    a, b = shots['flag0_observed'], shots['flag1_observed']
    same_frames = [f for f in FRAMES if f <= 5900] + [6600, 7600, 7800]
    assert len(same_frames) == 18 and all(a[f].tobytes() == b[f].tobytes() for f in same_frames)
    male, female = marker_cell(marker, 48, 0), marker_cell(marker, 48, 1)
    expected_diff = {(84 + i % 16, 76 + i // 16) for i, (x, y) in enumerate(zip(male, female, strict=True)) if x != y}
    assert len(expected_diff) == 25
    for frame in (6200, 7000, 7400):
        actual_diff = {(i % 256, i // 256) for i, (x, y) in enumerate(zip(a[frame].get_flattened_data(), b[frame].get_flattened_data(), strict=True)) if x != y}
        assert actual_diff == expected_diff
    sheet = Image.new('RGB', (768, 960), '#263238')
    draw = ImageDraw.Draw(sheet)
    for row, flag in enumerate((0, 1)):
        for col, frame in enumerate((6200, 6600, 7600)):
            x, y = col * 256, row * 480
            label = 'Arcadius fixture' if frame == 6200 else 'next officer' if frame == 6600 else 'restored roster'
            draw.text((x + 5, y + 5), f'Flag9={flag}, {frame}: {label}', fill='white')
            image = shots[f'flag{flag}_observed'][frame]
            sheet.paste(image, (x, y + 24))
            if frame != 7600:
                sheet.paste(image.crop((84, 76, 100, 92)).resize((48, 48), Image.Resampling.NEAREST), (x + 5, y + 416))
                draw.text((x + 61, y + 430), 'Symbol at 3x', fill='white')
    sp = ROOT / 'Sailor_Info_both_flag_states_plaques_and_restored_return.png'
    sheet.save(sp)
    assert len(cells) == 8 and len(plaques) == 80 and sum(r['native5_pixels'] for r in plaques) == 55200
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'actual_original_Sailor_Info_Arcadius_flag9_exception_both_symbols_verified': True,
        'four_fixture_cold_boot_runs': reports, 'matched_observer_and_minimal_fixture_pairs': pairs,
        'total_whole_RGB_and_capture_RAM_pairs': 42, 'original_source_getters_and_draw_arguments': sources,
        'complete_symbol_cells': cells, 'complete_native5_symbol_pixels': 2048,
        'whole_plaque_crops': plaques, 'whole_plaque_native5_pixels': 55200,
        'plaque_contract_sha256': sha(plaque_contract.read_bytes()), 'current_personinfo_PXL_sha256': sha(plaque_bytes),
        'all3_Arcadius_holds_only25_source_predicted_symbol_pixels_change': True,
        'all15_pre_fixture_next_officer_and2_restored_whole_RGB_cross_flag_pairs_exact': True,
        'all4_runs_only_lookup_word_and_flag9_bit_changed_and_restored': True,
        'original_donor_ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
        'full_original_update_prefix_replay_NOT_verified': {'failure': failure,
            'evidence': str(ROOT / 'native_flag0_call1_failure.json'),
            'failure_sha256': sha((ROOT / 'native_flag0_call1_failure.json').read_bytes()),
            'replayer_sha256': sha(Path('scripts/replay_person_gender_v698.py').read_bytes())},
        'restored_roster_retains_fixture_portrait_cache_not_normal_profile_display_credit': True,
        'V694_full_suffix_memory_gap_embedded_consumers_and_all18_plaques_remain_open': True,
        'not_earned_recruitment_story_reveal_or_guide_evidence': True,
        'review_sheet': str(sp), 'review_sheet_sha256': sha(sp.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V698:42 whole RGB/RAM pairs,eight complete symbols,80 whole plaque crops55200 pixels; native prefix replay remains unverified.', flush=True)


if __name__ == '__main__':
    main()
