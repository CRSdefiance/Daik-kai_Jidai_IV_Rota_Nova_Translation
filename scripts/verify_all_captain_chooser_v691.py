"""Verify all chooser names, complete source portraits and persistent input control."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.probe_button_prompt_native import call, machine
from scripts.run_all_captain_chooser_v691 import CAP, FRAMES, ROM, ROOT, STATES
from scripts.trace_chooser_raw_independence_v690 import PATTERN
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_raw_portrait_tail_v689 import pictures
from scripts.verify_village_wrap_v608 import read, save

NAMES = (('Rafael', '', 'Castor', 'Castor Co.'),
         ('Hodram', 'Joakim', 'Bergstrom', 'Bergstrom Fleet'),
         ('Lil', '', 'Argot', 'Argot Co.'),
         ('Maria', 'Huamei', 'Li', 'Li Clan'))


def main():
    pre = read(ROOT / 'preflight.json')
    assert pre['runner_sha256'] == sha(Path('scripts/run_all_captain_chooser_v691.py').read_bytes())
    assert pre['observer_source_sha256'] == sha(Path(pre['observer_source']).read_bytes())
    assert sha(CORE.read_bytes()) == CORE_SHA
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, key in ((ROOT / 'inputs.json', 'inputs_sha256'), (ROOT / 'unlock_manifest.json', 'unlock_manifest_sha256'),
                      (ROOT / 'isolated_raw_buffer_fixture.json', 'fixture_manifest_sha256')):
        assert sha(path.read_bytes()) == pre[key]
    assert sha(Path(pre['inherited_identical_host_controls']).read_bytes()) == pre['host_controls_sha256']
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    assert sha(Path(pre['original_donor']).read_bytes()) == pre['original_donor_sha256']
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    assert arm[0x46F00:0x46F50] == clean.read_file('/__arm9__.bin')[0x46F00:0x46F50]
    font = GameAsciiFont.from_arm9(arm)
    reports, shots, snapshots, event_sets = {}, {}, {}, {}
    all_cases = []
    for name in ('control', 'poison'):
        folder = CAP / ('all_captain_chooser_v691_' + name)
        rp = folder / 'capture_report.json'
        report, contract = read(rp), read(folder / 'run_contract.json')
        assert report['frames'] == 5200 and report['ROM_sha256'] == pre['candidate_sha256']
        assert report['core_DLL_sha256'] == CORE_SHA and report['cold_boot']
        assert not report['savestate_loaded'] and not report['callback_errors']
        assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
        assert report['scripted_input_schedule'] == read(ROOT / 'inputs.json')
        expected_flags = {'synthetic_gallery_fixtures'} | ({'synthetic_raw_portrait_buffer_fixture'} if name == 'poison' else set())
        assert {k for k, v in report.items() if k.startswith('synthetic_') and v} == expected_flags
        assert contract['runner_sha256'] == pre['runner_sha256']
        assert contract['observer_source_sha256'] == pre['observer_source_sha256']
        assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
        events = read(folder / 'observer/events.json')
        assert len(events['rows']) == events['callbacks'] == 10
        assert not events['ignored'] and not events['errors'] and not events['mismatches']
        assert events['producer_sha256'] == pre['observer_source_sha256']
        assert events['source_contract_sha256'] == pre['source_contract_sha256']
        assert events['all_host_slots_restored_core_file_exact']
        assert events['CPU_DTCM_configuration_unchanged_WRAM_only_declared_single_fixture_write']
        assert len(events['fixture_writes']) == int(name == 'poison')
        if name == 'poison':
            fixture, = events['fixture_writes']
            before, after = (Path(fixture[k]).read_bytes() for k in ('source_before_RAM', 'after_RAM'))
            assert sha(before) == fixture['source_before_RAM_sha256'] and sha(after) == fixture['after_RAM_sha256']
            expected_after = bytearray(before)
            expected_after[0x233040:0x233040 + 14144] = PATTERN
            assert after == expected_after and fixture['pattern_sha256'] == sha(PATTERN)
            manifest = read(ROOT / 'isolated_raw_buffer_fixture.json')
            assert sha(before[0x233040:0x233040 + 14144]) == manifest['source_block17_sha256']
        shots[name] = pictures(report)
        assert set(shots[name]) == set(FRAMES) and len(shots[name]) == 14
        snapshot_rows = {r['frame']: r for r in report['read_only_capture_RAM_snapshots']}
        assert set(snapshot_rows) == set(FRAMES)
        snapshots[name] = {}
        for frame, row in snapshot_rows.items():
            raw = Path(row['path']).read_bytes()
            assert len(raw) == 0x400000 and sha(raw) == row['sha256']
            snapshots[name][frame] = raw
        for frame, index in STATES:
            raw, image = snapshots[name][frame], shots[name][frame]
            parent = 0x02192500
            record = struct.unpack_from('<I', raw, parent + 0x54 - 0x02000000)[0]
            assert struct.unpack_from('<I', raw, record + 4 - 0x02000000)[0] == index
            field_cases = []
            for field, offset in enumerate((8, 0x19, 0x2A, 0x3B)):
                text = raw[record + offset - 0x02000000:record + offset - 0x02000000 + (21 if field == 3 else 17)].split(b'\0')[0].decode('ascii')
                assert text == NAMES[index][field]
                y0 = 220 + 22 * field
                expected = {(89 + n * 6 + x, y0 + y) for n, ch in enumerate(text)
                            for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
                actual = {(x, y) for y in range(y0, y0 + 11) for x in range(89, 202)
                          if image.getpixel((x, y)) == (230, 230, 230)}
                assert actual == expected
                field_cases.append({'field': field, 'text': text, 'whole113x11_field_positions': 1243,
                    'complete_ink_pixels': len(expected), 'all_first_final_letters_and_trailing_blank_cells_exact': True})
            vp = parent + 0x5AC + index * 0x30
            view = struct.unpack_from('<12I', raw, vp - 0x02000000)
            assert view[5] == 4 and view[7:9] == (0, 0) and view[10:12] == (104, 136)
            owner = view[3]
            fp = struct.unpack_from('<I', raw, owner + 12 - 0x02000000)[0]
            filename = raw[fp - 0x02000000:fp - 0x02000000 + 128].split(b'\0')[0].decode('ascii')
            assert filename == f'_pxl/personbustup{index:02d}.pxl'
            path = '/' + filename
            data = rom.read_file(path)
            assert data == clean.read_file(path)
            source = PxlImage.from_bytes(data).render()
            assert source.size == (104, 136)
            assert all(native5(image.getpixel((76 + x, 28 + y))) == native5(source.getpixel((x, y)))
                       for y in range(136) for x in range(104))
            # Captured real owner, complete original cached-file getter; no I/O bridge.
            u = machine(arm)
            u.mem_write(0x02000000, raw)
            executed = call(u, 0xD6558, (owner,))
            header = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(header, len(data))) == data
            original = machine(clean.read_file('/__arm9__.bin'))
            assert all(bytes(u.mem_read(pc, 4)) == bytes(original.mem_read(pc, 4)) for pc in executed)
            all_cases.append({'case': name, 'frame': frame, 'captain_index': index,
                'selected_record': record, 'fields': field_cases, 'view': vp, 'owner': owner,
                'filename': filename, 'original_full_file_sha256': sha(data),
                'native_cached_file_header': header, 'complete_cached_file_bytes': len(data),
                'native_cache_hit_instructions': len(executed), 'complete_original_getter_ABI_no_IO_bridges': True,
                'native_portrait_bounds': [76, 28, 180, 164], 'complete_source_native5_pixels': 14144,
                'all_edges_and_background_pixels_included': True})
        reports[name] = {'report': str(rp), 'report_sha256': sha(rp.read_bytes()),
            'events_sha256': sha((folder / 'observer/events.json').read_bytes())}
        event_sets[name] = events
    assert all(shots['control'][f].tobytes() == shots['poison'][f].tobytes() for f in FRAMES)
    assert [r['CPU128_hex'] for r in event_sets['control']['rows']] == [r['CPU128_hex'] for r in event_sets['poison']['rows']]
    persistent = []
    for frame in FRAMES:
        a, b = snapshots['control'][frame], snapshots['poison'][frame]
        expected = bytearray(a)
        if frame >= 2700:
            expected[0x233040:0x233040 + 14144] = PATTERN
            assert a[0x233040:0x233040 + 14144] != PATTERN
            persistent.append(frame)
        assert b == expected
    a = (CAP / 'all_captain_chooser_v691_control/final_arm9_ram.bin').read_bytes()
    b = (CAP / 'all_captain_chooser_v691_poison/final_arm9_ram.bin').read_bytes()
    expected = bytearray(a)
    expected[0x233040:0x233040 + 14144] = PATTERN
    assert b == expected
    sheet = Image.new('RGB', (1024, 820), '#263238')
    draw = ImageDraw.Draw(sheet)
    for row, name in enumerate(('control', 'poison')):
        for col, (frame, index) in enumerate(STATES[:4]):
            draw.text((col * 256 + 5, row * 410 + 5), f'{name}: {NAMES[index][0]} {frame}', fill='white')
            sheet.paste(shots[name][frame], (col * 256, row * 410 + 24))
    sp = ROOT / 'all_four_captains_control_and_declared_fixture.png'
    sheet.save(sp)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'runs': reports, 'all14_full_RGB_case_pairs_equal': True,
        'seven_actual_selections_per_case_including_reverse_return_cycle': all_cases,
        'all56_whole_name_middle_surname_company_fields_complete': True,
        'all14_complete_portrait_planes198016_native5_pixels_match_original': True,
        'all14_complete_real_owner_cache_hits_equal_original_ROM_files': True,
        'raw_input_pattern_persists_through_all_captain_states': persistent,
        'all_other_captured_and_terminal_main_RAM_equal_no_tolerance_mask': True,
        'existing_system_unlock_donor_not_earned_and_second_case_declared_raw_fixture': True,
        'no_story_progression_all_console_frame_other_consumer_or_global_nonuse_claim': True,
        'all18_plaques_incomplete22_original_requirements_other_graphics_open': True,
        'ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
        'review_sheet': str(sp), 'review_sheet_sha256': sha(sp.read_bytes()),
        'runner_sha256': pre['runner_sha256'], 'observer_source_sha256': pre['observer_source_sha256'],
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V691:all four captains and return cycle;56 complete fields198016 original portrait pixels14 cache hits and14 full pairs pass.', flush=True)


if __name__ == '__main__':
    main()
