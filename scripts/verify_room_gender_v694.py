"""Verify actual second-parent gender cells without hiding native replay gaps."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.probe_button_prompt_native import call, machine
from scripts.run_room_gender_v694 import CAP, ROM, ROOT
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_raw_portrait_tail_v689 import pictures
from scripts.verify_village_wrap_v608 import read, save

PAIRS = (('hodram', 'hodram_baseline'), ('maria', 'maria_baseline'),
         ('maria_selected', 'maria_selected_baseline'),
         ('hodram_ITCM', 'hodram_baseline'), ('maria_ITCM', 'maria_selected_baseline'))
PARENT, WIDGET, VIEW = 0x0218BD98, 0x0218DF2C, 0x0218A644
SEX = {1: 0, 3: 1, 10: 0, 12: 0}


def word(raw, address):
    return struct.unpack_from('<I', raw, address - 0x02000000)[0]


def text(raw, address):
    return raw[address - 0x02000000:address - 0x02000000 + 128].split(b'\0')[0].decode('ascii')


def class_name(raw, address):
    return text(raw, word(raw, word(raw, word(raw, address) - 4) + 4))


def marker_cell(pxl, bank, sex):
    palette_offset = struct.unpack_from('<I', pxl.source, 12)[0] + bank * 32
    palette = [native5(bgr555(v)) for (v,) in struct.iter_unpack('<H', pxl.source[palette_offset:palette_offset + 32])]
    x0, y0 = ((232, 96), (240, 112))[sex]
    return [palette[pxl.indices[(y0 + y) * pxl.width + x0 + x]] for y in range(16) for x in range(16)]


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for item in pre['donors'].values():
        assert sha(Path(item['path']).read_bytes()) == item['sha256']
    assert sha(CORE.read_bytes()) == CORE_SHA
    assert pre['producer_sha256'] == sha(Path('scripts/run_room_gender_v694.py').read_bytes())
    assert pre['observer_sha256'] == sha(Path('scripts/observe_room_gender_v694.py').read_bytes())
    assert pre['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    controls = read(ROOT / 'prefix_controls/native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 35 and len(controls['read_policy_cases']) == 8
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert arm[0x14BE8:0x14F60] == original[0x14BE8:0x14F60]
    assert arm[0x157D8:0x15948] == original[0x157D8:0x15948]
    # Original state-4 gender draw uses this two-word point, not image searching.
    assert struct.unpack_from('<I', arm, 0x14E24)[0] == 0xE59F3120
    point = struct.unpack_from('<I', arm, 0x14E24 + 8 + 0x120)[0]
    destination = struct.unpack_from('<2i', arm, point - 0x02000000)
    assert point == 0x021146A8 and destination == (80, 80)
    file = rom.read_file('/_pxl/__marker.pxl')
    pxl = PxlImage.from_bytes(file)
    assert (pxl.width, pxl.height, pxl.bits_per_pixel) == (256, 256, 4)
    frames = {1, 60, 180, 1600, *range(2000, 13201, 400)}
    shots, snapshots, pair_results, event_sets = {}, {}, [], {}
    for case, baseline in PAIRS:
        pair = []
        for name in (case, baseline):
            if name in shots:
                continue
            folder = CAP / ('room_gender_v694_' + name)
            report = read(folder / 'capture_report.json')
            assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
            assert report['frames'] == 13200 and report['cold_boot'] and not report['savestate_loaded']
            assert not report['callback_errors'] and not report['hardware_device_verification']
            assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
            schedule_folder = ROOT / 'selection' if name.startswith('maria_selected') else ROOT
            if name.endswith('_ITCM'):
                schedule_folder = ROOT / 'native_ITCM' / name.split('_')[0]
            assert report['scripted_input_schedule'] == read(schedule_folder / 'inputs.json')
            donor = pre['donors']['maria' if name.startswith('maria') else 'hodram']
            assert report['battery_save_preloaded']['source_sha256'] == donor['sha256']
            assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
            shots[name] = pictures(report)
            assert set(shots[name]) == frames
            snapshots[name] = {}
            for row in report['read_only_capture_RAM_snapshots']:
                raw = Path(row['path']).read_bytes()
                assert len(raw) == 0x400000 and sha(raw) == row['sha256']
                if row['frame'] in snapshots[name]:
                    assert snapshots[name][row['frame']] == raw
                snapshots[name][row['frame']] = raw
            assert set(snapshots[name]) == frames
            if not name.endswith('_baseline'):
                events = read(folder / 'observer/events.json')
                assert not events['errors'] and not events['mismatches'] and events['active_call_at_end'] is None
                assert events['CPU_WRAM_DTCM_configuration_unchanged']
                assert events['all_host_slots_restored_core_file_exact']
                assert events['producer_sha256'] == pre['observer_sha256']
                assert events['source_contract_sha256'] == pre['source_contract_sha256']
                if name.endswith('_ITCM'):
                    assert events['ITCM_extension_sha256'] == sha(Path('scripts/run_room_gender_ITCM_v694.py').read_bytes())
                    assert events['all_recorded_CPU_and_ITCM_state_preserved_by_extension']
                event_sets[name] = events
        for frame in sorted(frames):
            assert shots[case][frame].tobytes() == shots[baseline][frame].tobytes(), (case, frame)
            pair.append(frame)
        a, b = [CAP / ('room_gender_v694_' + n) / 'final_arm9_ram.bin' for n in (case, baseline)]
        assert a.read_bytes() == b.read_bytes()
        pair_results.append({'observed': case, 'unobserved': baseline, 'whole_two_screen_RGB_pairs': len(pair),
                             'complete_terminal_4MiB_RAM_equal': True})
    owner_cases, branch_cases = [], []
    for case in ('hodram_ITCM', 'maria_ITCM'):
        groups = {}
        for row in event_sets[case]['rows']:
            for field in ('RAM', 'DTCM', 'ITCM'):
                assert sha(Path(row[field]).read_bytes()) == row[field + '_sha256']
            groups.setdefault(row['call_number'], []).append(row)
        for rows in groups.values():
            start = rows[0]
            state = struct.unpack('<32I', bytes.fromhex(start['CPU128_hex']))
            raw = Path(start['RAM']).read_bytes()
            parent = state[11]
            assert parent == PARENT and class_name(raw, parent) == '18CDeckPersonnelView'
            room = word(raw, parent + 0x44)
            room_done = next(r for r in rows if r['kind'] == 'room_done')
            descriptor = struct.unpack('<32I', bytes.fromhex(room_done['CPU128_hex']))[4]
            if room == 32:
                assert descriptor == 0 and not rows[-1]['helper_entered']
                assert class_name(raw, state[10]) == '28CSelectPlayerForcePersonView'
            else:
                assert room == 5 and descriptor
                assert class_name(raw, state[10]) == '28CSelectPlayerForcePersonView'
                get = lambda kind, rows=rows: next(r for r in rows if r['kind'] == kind)
                values = lambda kind, get=get: struct.unpack('<32I', bytes.fromhex(get(kind)['CPU128_hex']))
                entered, raw_sex, identity, ready = [values(k) for k in ('gender_entry', 'raw_gender', 'identity', 'gender_ready')]
                actor, sex = entered[6], raw_sex[4]
                assert actor in SEX and sex == SEX[actor] and identity[4] == actor
                assert entered[4:6] == (WIDGET, 5) and word(raw, descriptor + 0x6C) == 5
                assert ready[12] == sex
                final_ram = Path(get('gender_ready')['RAM']).read_bytes()
                view = struct.unpack_from('<12I', final_ram, WIDGET + 0xA0 - 0x02000000)
                assert view[5] == 4 and view[7:9] == ((232, 96), (240, 112))[sex]
                assert view[9] & 255 == 48 and view[10:12] == (16, 16)
                owner = view[3]
                assert text(final_ram, word(final_ram, owner + 12)) == '_pxl/__marker.pxl'
                u = machine(arm)
                u.mem_write(0x02000000, final_ram)
                executed = call(u, 0xD6558, (owner,))
                header = u.reg_read(UC_ARM_REG_R0)
                assert bytes(u.mem_read(header, len(file))) == file
                original_machine = machine(original)
                assert all(bytes(u.mem_read(pc, 4)) == bytes(original_machine.mem_read(pc, 4)) for pc in executed)
                owner_cases.append({'case': case, 'actor': actor, 'raw_sex': sex, 'identity': identity[4],
                    'selector': ready[12], 'view': WIDGET + 0xA0, 'view_words': list(view),
                    'owner': owner, 'native_cached_header': header, 'complete_file_bytes': len(file),
                    'complete_file_sha256': sha(file), 'original_cache_getter_ABI_no_IO_bridge': True})
            branch_cases.append({'case': case, 'room': room, 'descriptor': descriptor,
                                 'original_null_bypass': room == 32, 'helper_entered': rows[-1]['helper_entered']})
    assert {r['actor'] for r in owner_cases} == set(SEX) and len(owner_cases) == 4
    cells = []
    for case in ('hodram', 'maria', 'maria_selected'):
        holds = range(8800, 10801 if case == 'maria_selected' else 12801, 400)
        for frame in holds:
            raw, image = snapshots[case][frame], shots[case][frame]
            index = word(raw, VIEW + 0xC88)
            assert index < word(raw, VIEW + 0x354)
            actor = word(raw, VIEW + 0x18 + index * 4)
            sex = SEX[actor]
            view = struct.unpack_from('<12I', raw, WIDGET + 0xA0 - 0x02000000)
            assert word(raw, PARENT + 0x44) == 5
            assert view[7:9] == ((232, 96), (240, 112))[sex] and view[9] & 255 == 48
            actual = [native5(image.getpixel((80 + x, 80 + y))) for y in range(16) for x in range(16)]
            expected = marker_cell(pxl, 48, sex)
            assert actual == expected, (case, frame, actor)
            assert actual != marker_cell(pxl, 48, 1 - sex)
            assert actual != marker_cell(pxl, 0, sex)
            shifted = [native5(image.getpixel((81 + x, 80 + y))) for y in range(16) for x in range(16)]
            assert shifted != expected
            cells.append({'case': case, 'frame': frame, 'actor': actor, 'sex': sex,
                          'source': list(view[7:9]), 'palette_bank': 48, 'destination_bounds': [80, 80, 96, 96],
                          'all256_cell_pixels_edges_and_background_exact': True,
                          'wrong_sex_palette_and_one_pixel_shift_controls_fail': True})
    assert len(cells) == 28 and sum(c['sex'] for c in cells) == 4
    replays = {case: read(ROOT / f'native_{case}_proof.json') for case in ('hodram', 'maria')}
    for proof in replays.values():
        assert proof['script_sha256'] == sha(Path('scripts/replay_room_gender_v694.py').read_bytes())
        assert proof['no_mismatch_removed_or_replaced_by_expected_state']
        for row in proof['cases']:
            assert row['all_recorded_intermediate_checkpoint_registers_CPSR_RAM_DTCM_ITCM_exact']
            assert row['return_registers_and_CPSR_exact'] and row['return_ITCM_exact']
    sheet = Image.new('RGB', (768, 820), '#263238')
    draw = ImageDraw.Draw(sheet)
    selected = [('hodram', 8800, 'Hodram'), ('maria_selected', 9200, 'Maria'),
                ('maria_selected', 9600, 'Yukihisa'), ('maria_selected', 10000, 'Maria return'),
                ('maria_selected', 10400, 'Xien Yan'), ('maria_selected', 10800, 'Maria return')]
    for n, (case, frame, label) in enumerate(selected):
        x, y = n % 3 * 256, n // 3 * 410
        draw.text((x + 5, y + 5), label + ' ' + str(frame), fill='white')
        sheet.paste(shots[case][frame], (x, y + 24))
    sp = ROOT / 'actual_room_selection_male_female_return_cycle.png'
    sheet.save(sp)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'actual_second_loose_marker_parent_and_both_gender_cells_verified': True,
        'parent_RTTI': '18CDeckPersonnelView', 'normal_room': 5, 'original_None_room32_null_bypass': True,
        'actual_branches': branch_cases, 'whole_file_original_native_owner_getters': owner_cases,
        'source_derived_original_draw_point': list(destination), 'draw_point_pointer': point,
        'complete_actual_cells': cells, 'complete_native5_pixels': len(cells) * 256,
        'whole_observed_unobserved_pairs': pair_results, 'total_whole_RGB_pairs': 165,
        'all5_whole_terminal_RAM_pairs_exact': True,
        'native_replays': {c: {'path': str(ROOT / f'native_{c}_proof.json'),
                              'sha256': sha((ROOT / f'native_{c}_proof.json').read_bytes()),
                              'complete_return_state_proven': p['complete_branch_return_state_proven']}
                           for c, p in replays.items()},
        'native_intermediate_gender_construction_states_exact_but_full_suffix_memory_mismatch_unresolved': True,
        'story_identity8_exception_not_live_exercised_original_code_preserved': True,
        'embedded_copy_consumer_not_verified': True,
        'normal_menu_changes_no_live_gameplay_fixture_and_Maria_historical_unlock_not_earned': True,
        'host_prefix_controls': 35, 'bounded_mirror_controls': 8,
        'all18_plaques_incomplete22_original_scopes_and_other_graphics_open': True,
        'ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
        'review_sheet': str(sp), 'review_sheet_sha256': sha(sp.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V694: second real room parent, 28 complete symbol cells/7168 pixels, four real owners, 165 full RGB pairs and five terminal RAM pairs verified; suffix replay memory gap retained.', flush=True)


if __name__ == '__main__':
    main()
