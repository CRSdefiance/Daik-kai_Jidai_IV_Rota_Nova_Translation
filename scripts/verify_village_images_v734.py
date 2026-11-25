"""Verify Ezo progression, complete paired captures and all recorded request kinds."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.observe_village_images_v734 import ROM, ROOT
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_village_images_v734 import CAP, relocate
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_regional_ui_v616 import glyphs
from scripts.verify_village_development_v665 import confirmation
from scripts.verify_village_visits_v664 import dialog, menu, model
from scripts.verify_village_wrap_v608 import read, save

CARDS = (168, 169, 170, 171, 206, 207, 208, 209)


def blob(row):
    data = Path(row['path']).read_bytes()
    assert sha(data) == row['sha256']
    if 'bytes' in row:
        assert len(data) == row['bytes']
    return data


def main():
    pre, contract = read(ROOT / 'preflight.json'), read(ROOT / 'source_contract.json')
    for key, filename in (('runner', 'run_village_images_v734.py'), ('observer', 'observe_village_images_v734.py')):
        assert pre[key + '_sha256'] == sha((Path('scripts') / filename).read_bytes())
    for key in ('original_donor', 'test_copy', 'historical_proof', 'historical_report', 'historical_controller'):
        assert sha(Path(pre[key]).read_bytes()) == pre[key + '_sha256']
    assert pre['shared_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert pre['location_helper_sha256'] == sha(Path('scripts/native_village_visits_v664.py').read_bytes())
    assert contract['assembler_sha256'] == sha(Path('scripts/observe_file_requests_v681.py').read_bytes())
    assert contract['mapped_read_helper_sha256'] == sha(Path('scripts/trace_file_ids_v683.py').read_bytes())
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 30 and len(controls['read_policy_cases']) == 8
    prior_mapping = read('work/analysis/script_sources_v733/source_contract.json')
    assert prior_mapping['CPU_memory_read_helper_sha256'] == contract['mapped_read_helper_sha256']
    assert len(read('work/analysis/script_sources_v733/proof.json')['ten_DTCM_precedence_boundary_controls']) == 10
    reports, images, memories = {}, {}, {}
    for mode in ('baseline', 'observed'):
        folder = CAP / ('village_images_v734_Ezo_' + mode)
        report = read(folder / 'capture_report.json')
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == 16700
        assert report['core_DLL_sha256'] == contract['core_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule'] == read(ROOT / 'inputs.json')
        assert report['battery_save_preloaded']['source'] == pre['test_copy']
        assert report['battery_save_preloaded']['source_sha256'] == pre['test_copy_sha256']
        assert not report['normal_travel_verified']
        assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_location_fixtures')
        pictures, snapshots = {}, {}
        for row in report['frames_captured']:
            path = Path(row['path'])
            assert sha(path.read_bytes()) == row['PNG_sha256']
            image = Image.open(path).convert('RGB')
            if row['frame'] in pictures:
                assert pictures[row['frame']].tobytes() == image.tobytes()
            pictures[row['frame']] = image
        for row in report['read_only_pause_RAM_snapshots']:
            snapshots[row['frame']] = blob(row)
        assert len(pictures) == 48 and len(snapshots) == 45
        assert blob(report['read_only_RAM_snapshot']) == snapshots[16700]
        assert len(report['synthetic_location_fixtures']) == 2
        for fixture in report['synthetic_location_fixtures']:
            before = snapshots[fixture['frame']]
            arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
            after, receipt = relocate(arm, before, 18)
            assert fixture == dict(receipt, frame=fixture['frame'])
            at = receipt['active_ship'] - BASE + 16
            assert before[:at] == after[:at] and before[at + 8:] == after[at + 8:]
        reports[mode] = {'path': str(folder / 'capture_report.json'),
            'sha256': sha((folder / 'capture_report.json').read_bytes())}
        images[mode], memories[mode] = pictures, snapshots
    a, b = [read(reports[s]['path']) for s in ('baseline', 'observed')]
    assert a['core_options'] == b['core_options']
    assert set(images['baseline']) == set(images['observed'])
    for frame in images['baseline']:
        assert images['baseline'][frame].tobytes() == images['observed'][frame].tobytes(), frame
    for frame in memories['baseline']:
        assert memories['baseline'][frame] == memories['observed'][frame], frame
    native_pairs = []
    for state in (a['read_only_native_state'], b['read_only_native_state']):
        blob(state)
        for region in state['regions'].values():
            blob(region)
    na, nb = a['read_only_native_state'], b['read_only_native_state']
    assert na['ARM9_registers'] == nb['ARM9_registers'] and na['ARM9_instruction_address'] == nb['ARM9_instruction_address']
    assert na['regions'].keys() == nb['regions'].keys()
    for name in na['regions']:
        assert blob(na['regions'][name]) == blob(nb['regions'][name])
        native_pairs.append({'region': name, 'sha256': na['regions'][name]['sha256']})
    rom, cart = NdsImage.open(ROM), ROM.read_bytes()
    arm, font = rom.read_file('/__arm9__.bin'), GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    old = next(r for r in read(pre['historical_proof'])['all24_development_cases'] if r['index'] == 18)
    phases = pre['historical_successful_phases']
    states = []
    for phase in ('chief_request', 'complete_password_before_submission', 'answer_confirmation',
                  'accepted_clue', 'developed_village_menu', 'developed_town_return'):
        state = model(arm, memories['observed'][phases[phase]], 18, 'Ezo', True)
        assert state['native_development'] == (0 if phase in ('chief_request', 'complete_password_before_submission', 'answer_confirmation') else 2)
        states.append({'phase': phase, 'frame': phases[phase], **state})
    entries = []
    marker = read('work/analysis/village_promised_words_plan.json')['keyboard_wrapper']['provider_vtable']
    for n, old_entry in enumerate(old['all_entered_character_prefixes_native_buffer_cursor_capacity_and_complete_display_verified']):
        raw = memories['observed'][old_entry['frame']]
        needle = struct.pack('<I', marker)
        owners = [p - 4 for p in range(0x170000, len(raw) - 4, 4) if raw[p:p + 4] == needle]
        assert len(owners) == 1
        parent = owners[0]
        expected = 'Kamui'[:n]
        assert raw[parent + 0xB4:parent + 0xB4 + n + 1] == expected.encode('ascii') + b'\0'
        assert struct.unpack_from('<I', raw, parent + 0x78)[0] == n
        assert struct.unpack_from('<I', raw, parent + 0xD8)[0] == 18
        image = images['observed'][old_entry['frame']]
        actual = {(x, y) for y in range(11) for x in range(108)
            if image.getpixel((60 + x, 244 + y)) == (230, 230, 230)}
        assert actual == glyphs(font, expected)
        entries.append({'frame': old_entry['frame'], 'entry': expected,
            'native_buffer_cursor_capacity_and_complete108x11_foreground_exact': True})
    assert len(entries) == 6
    dialogues = {'confirmation': confirmation(images['observed'][phases['answer_confirmation']], rom, font, 'Kamui'),
        'clue': dialog(images['observed'][phases['accepted_clue']], font, old['complete_dialogue_fields']['clue']['paragraph'], 22),
        'facilities': dialog(images['observed'][phases['facilities_notice']], font, old['complete_dialogue_fields']['facilities']['paragraph'], 22)}
    labels = [r['English'] for r in old['complete_developed_menu']['complete_menu_labels']]
    current_menu = menu(images['observed'][phases['developed_village_menu']], font, labels)
    header = find_mask(font, 'Ezo', images['observed'][16700], (0, 10, 256, 40))
    u = machine(arm)
    u.mem_write(BASE, memories['observed'][16700])
    call(u, 0xB5630, (states[-1]['town'],))
    assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 64)).split(b'\0')[0] == b'Ezo'
    call(u, 0xB7294, (108, 0))
    background = f'/towngrp/towngrp{u.reg_read(UC_ARM_REG_R0):02d}.pxl'
    assert background == '/towngrp/towngrp48.pxl'
    assert rom.read_file(background) == NdsImage.open('work/clean.nds').read_file(background)
    assert rom.read_file(background) in memories['observed'][16700]
    trace_path = CAP / 'village_images_v734_Ezo_observed/observer/requests.json'
    trace = read(trace_path)
    assert not trace['errors'] and not trace['mismatches'] and not trace['unreturned_raw_requests']
    assert trace['callbacks'] == len(trace['rows']) == 108
    assert trace['observer_sha256'] == pre['observer_sha256']
    assert trace['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    names = contract['file_IDs']
    assert names == {str(i): p for p, i in rom.path_map().items()}
    fnt, fnt_size, fat, fat_size, overlay, overlay_size = struct.unpack_from('<6I', cart, 0x40)
    table = [struct.unpack_from('<2I', cart, fat + n * 8) for n in range(fat_size // 8)]
    assert fat_size == len(rom.rom.files) * 8
    assert all(cart[lo:hi] == rom.rom.files[n] for n, (lo, hi) in enumerate(table))
    special = {(fnt, fnt + fnt_size): 'FNT', (fat, fat + fat_size): 'FAT',
        (overlay, overlay + overlay_size): 'ARM9 overlay table'}
    card_ids = {rom.path_map()[f'/evstill/evstill{n:03d}.pxl'] for n in CARDS}
    pending, named, numeric, ranges = None, [], [], []
    for row in trace['rows']:
        cpu = struct.unpack('<32I', bytes.fromhex(row['CPU128_hex']))
        target = next(t for t in contract['targets'] if t['name'] == row['kind'])
        assert cpu[1:3] == (target['word'], target['PC']) and row['args'] == list(cpu[4:8]) and row['LR'] == cpu[18]
        assert row['CPU128_WRAM_DTCM_ITCM_and_configuration_unchanged_by_observer']
        if row['kind'] == 'filename':
            assert pending is None
            assert bytes.fromhex(row['filename_with_NUL_hex']) == row['filename'].encode('ascii') + b'\0'
            pending = row
            named.append({'frame': row['frame'], 'filename': row['filename'], 'caller_return': row['LR']})
        elif row['kind'] == 'numeric_ID':
            index = row['file_ID']
            assert index == cpu[6] and str(index) in names and index not in card_ids
            assert bytes.fromhex(row['archive128_hex'])[:4] == b'rom\0'
            if row['LR'] == 0x020DED7C:
                assert pending is not None and pending['args'][0] == row['args'][0]
                path = '/' + pending['filename'].replace('\\', '/').lstrip('/')
                assert path.casefold() == names[str(index)].casefold()
                pending = None
            else:
                assert pending is None
                assert (index, row['LR']) in ((0, 0x020DF9BC), (0, 0x020DF76C), (2, 0x020EA8B8), (2, 0x020EC9A0))
            numeric.append({'frame': row['frame'], 'ID': index, 'path': names[str(index)], 'caller_return': row['LR']})
        elif row['kind'] == 'direct_range':
            span = tuple(row['byte_range'])
            assert span in special and row['file_ID'] == struct.unpack_from('<I', bytes.fromhex(row['stack32_hex']))[0] == 0xFFFFFFFF
            assert span == tuple(cpu[6:8]) and bytes.fromhex(row['archive128_hex'])[:4] == b'rom\0'
            assert not any(span[0] < table[n][1] and table[n][0] < span[1] for n in card_ids)
            ranges.append({'frame': row['frame'], 'range': list(span), 'source': special[span]})
        else:
            raise AssertionError('Unexpected actual raw or event-still request must be investigated,not silently excluded: ' + str(row))
    assert pending is None and len(named) == 49 and len(numeric) == 55 and len(ranges) == 4
    assert Counter(r['source'] for r in ranges) == {'FNT': 1, 'FAT': 1, 'ARM9 overlay table': 2}
    assert not any('/evstill/' in r['filename'].replace('\\', '/').lower() for r in named)
    sheet = Image.new('RGB', (1024, 1648), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (label, frame) in enumerate((('Initial chief request', 12200), ('Password accepted', 14400),
                                      ('Facilities notice', 14800), ('Developed Ezo port', 16700))):
        x, y = (i % 2) * 512, (i // 2) * 824
        draw.text((x + 10, y + 10), f'V712 / coordinate fixture / {label} / {frame}', fill='white')
        sheet.paste(images['baseline'][frame].resize((512, 768), Image.Resampling.NEAREST), (x, y + 40))
    sheet.save(ROOT / 'Ezo_progression_review.png')
    proof = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'], 'reports': reports,
        'two_terminal16700_frame_current_Ezo_replays': True,
        'all48_whole_RGB_pairs_and45_whole4MiB_pause_RAM_pairs_exact': True,
        'all_seven_exported_final_guest_region_pairs': native_pairs,
        'final_exported_ARM9_registers_and_PC_exact': True,
        'native_development_states': states, 'all_six_complete_typed_prefixes': entries,
        'complete_confirmation_clue_and_facility_fields': dialogues, 'complete_developed_menu': current_menu,
        'complete_current_Ezo_title': header, 'source_exact_resident_selected_background': background,
        'trace': str(trace_path), 'trace_sha256': sha(trace_path.read_bytes()),
        'actual_request_counts': dict(Counter(r['kind'] for r in trace['rows'])),
        'all_named_requests': named, 'all_numeric_requests': numeric, 'all_direct_ranges': ranges,
        'zero_event_still_formatter_or_raw_SLACK_entries_in_this_complete_sequence': True,
        'no_eight_card_path_or_file_ID_or_direct_range_requests_in_this_sequence': True,
        'entry_requests_not_successful_load_or_every_filesystem_route': True,
        'other_villages_story_states_global_unused_and_original_card_triggers_not_proven': True,
        'protected_source_copy_coordinate_only_fixtures_replayed_no_password_or_development_injection': True,
        'prototype_unrelated_name_getter_corrected_to_original_TownModel_B5630': True,
        'runner_sha256': pre['runner_sha256'], 'observer_sha256': pre['observer_sha256'],
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'release_hashes_unchanged': pre['release_hashes'],
        'full_goal_complete': False}
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', proof)
    print('V734:full Ezo progression/typed Kamui/development2 passes;108 requests classified,zero card/raw/event-still requests;48 RGB/45 RAM/7 guest region pairs exact.')


if __name__ == '__main__':
    main()
