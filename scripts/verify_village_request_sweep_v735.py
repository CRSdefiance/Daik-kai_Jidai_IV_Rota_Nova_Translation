"""Verify the new village request scope without reopening carried-forward work."""

import argparse
import struct
import textwrap
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_village_visits_v664 as coordinate
from scripts.native_village_town_v665 import replay
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.probe_worldmap_overlays_v638 import color5
from scripts.run_village_request_sweep_v735 import CARDS, ROM, ROOT
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_regional_ui_v616 import full_cells, glyphs
from scripts.verify_town_scene_v644 import rgb5
from scripts.verify_village_development_v665 import confirmation
from scripts.verify_village_images_v734 import blob
from scripts.verify_village_visits_v664 import dialog, menu, model
from scripts.verify_village_wrap_v608 import read, save


def text_field(image, font, paragraph, origin):
    # Independently calculate the current common 35-character line budget.
    lines = textwrap.wrap(paragraph, width=35, break_long_words=False,
                          break_on_hyphens=False)
    assert len(lines) <= 3
    masks = [full_cells(image, font, line, origin, 296 + n * 16, (0, 8, 0))
             for n, line in enumerate(lines)]
    expected = {(origin + x, 296 + n * 16 + y)
                for n, line in enumerate(lines) for x, y in glyphs(font, line)}
    actual = {(x, y) for y in range(296, 344) for x in range(16, 240)
              if image.getpixel((x, y)) == (0, 8, 0)}
    assert actual == expected
    return {'paragraph': paragraph, 'complete_lines': masks,
            'whole224x48_foreground_and_blank_cells_exact': True}


def requests(rom, case, contract, pre):
    path = Path(case['output']) / 'observer/requests.json'
    trace = read(path)
    assert not trace['errors'] and not trace['mismatches'] and not trace['unreturned_raw_requests']
    assert trace['callbacks'] == len(trace['rows'])
    assert trace['all_host_slots_restored_and_core_file_exact']
    assert trace['observer_sha256'] == pre['shared_observer_sha256']
    assert trace['source_contract_sha256'] == pre['shared_source_contract_sha256']
    names = contract['file_IDs']
    assert names == {str(i): p for p, i in rom.path_map().items()}
    cart = ROM.read_bytes()
    fnt, fs, fat, fats, ov, ovs = struct.unpack_from('<6I', cart, 0x40)
    table = [struct.unpack_from('<2I', cart, fat + n * 8) for n in range(fats // 8)]
    assert all(cart[lo:hi] == rom.rom.files[n] for n, (lo, hi) in enumerate(table))
    special = {(fnt, fnt + fs): 'FNT', (fat, fat + fats): 'FAT',
               (ov, ov + ovs): 'ARM9 overlay table'}
    card_ids = {rom.path_map()[f'/evstill/evstill{n:03d}.pxl'] for n in CARDS}
    pending, named, numeric, ranges = None, [], [], []
    for row in trace['rows']:
        cpu = struct.unpack('<32I', bytes.fromhex(row['CPU128_hex']))
        target = next(t for t in contract['targets'] if t['name'] == row['kind'])
        assert cpu[1:3] == (target['word'], target['PC'])
        assert row['args'] == list(cpu[4:8]) and row['LR'] == cpu[18]
        assert row['CPU128_WRAM_DTCM_ITCM_and_configuration_unchanged_by_observer']
        if row['kind'] == 'filename':
            assert pending is None
            assert bytes.fromhex(row['filename_with_NUL_hex']) == row['filename'].encode('ascii') + b'\0'
            pending = row
            named.append(row['filename'])
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
                assert (index, row['LR']) in ((0, 0x020DF9BC), (0, 0x020DF76C),
                                             (2, 0x020EA8B8), (2, 0x020EC9A0))
            numeric.append({'ID': index, 'path': names[str(index)], 'LR': row['LR']})
        elif row['kind'] == 'direct_range':
            span = tuple(row['byte_range'])
            assert span in special and row['file_ID'] == 0xFFFFFFFF
            assert struct.unpack_from('<I', bytes.fromhex(row['stack32_hex']))[0] == 0xFFFFFFFF
            assert span == tuple(cpu[6:8]) and bytes.fromhex(row['archive128_hex'])[:4] == b'rom\0'
            assert not any(span[0] < table[n][1] and table[n][0] < span[1] for n in card_ids)
            ranges.append({'range': list(span), 'source': special[span]})
        else:
            raise AssertionError('New original image-consumer request requires investigation: ' + str(row))
    assert pending is None
    assert not any('/evstill/' in name.replace('\\', '/').lower() for name in named)
    assert Counter(r['source'] for r in ranges) == {'FNT': 1, 'FAT': 1, 'ARM9 overlay table': 2}
    return {'path': str(Path(case['output']) / 'observer/requests.json'),
            'sha256': sha((Path(case['output']) / 'observer/requests.json').read_bytes()),
            'counts': dict(Counter(r['kind'] for r in trace['rows'])),
            'all_filenames': named, 'all_numeric_requests': numeric, 'all_direct_ranges': ranges,
            'no_eight_card_filename_ID_or_range_and_zero_raw_or_event_still_requests': True,
            'all_callback_guest_regions_preserved_and_host_slots_restored': True}


def verify_case(index):
    pre = read(ROOT / 'preflight.json')
    assert sha(Path('scripts/run_village_request_sweep_v735.py').read_bytes()) == pre['runner_sha256']
    assert sha(Path('scripts/observe_village_images_v734.py').read_bytes()) == pre['shared_observer_sha256']
    assert sha(Path(pre['shared_source_contract']).read_bytes()) == pre['shared_source_contract_sha256']
    assert sha((ROOT / 'cases.json').read_bytes()) == pre['cases_sha256']
    case = next(r for r in read(ROOT / 'cases.json') if r['index'] == index)
    folder = Path(case['output'])
    rc = read(folder / 'run_contract.json')
    assert rc['case'] == case and rc['runner_sha256'] == pre['runner_sha256']
    for key in ('original_donor', 'test_copy', 'inputs', 'commands', 'historical_report', 'historical_controller'):
        assert sha(Path(case[key]).read_bytes()) == case[key + '_sha256']
    contract = read(pre['shared_source_contract'])
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    report_path = folder / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == pre['candidate_sha256'] == sha(ROM.read_bytes())
    assert report['core_DLL_sha256'] == contract['core_sha256']
    assert report['frames'] == case['frames'] and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert not report['normal_travel_verified'] and not report['goal_complete']
    assert report['scripted_input_schedule'] == read(case['inputs'])
    assert report['battery_save_preloaded']['source'] == case['test_copy']
    assert report['battery_save_preloaded']['source_sha256'] == case['test_copy_sha256']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_location_fixtures')
    journal_path = folder / 'navigation_command_journal.json'
    journal = read(journal_path)
    assert journal['ROM_sha256'] == pre['candidate_sha256']
    assert all(r['validation_passed'] for r in journal['commands_received'])
    commands = read(case['commands'])
    assert [r['command'] for r in journal['commands_received']] == commands
    assert commands[-1] == {'stop': True}
    images, raw = {}, {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        image = Image.open(row['path']).convert('RGB')
        assert image.size == (256, 384)
        if row['frame'] in images:
            assert images[row['frame']].tobytes() == image.tobytes()
        images[row['frame']] = image
    for row in report['read_only_pause_RAM_snapshots']:
        assert row['read_only_export']
        data = blob(row)
        assert len(data) == 0x400000
        if row['frame'] in raw:
            assert raw[row['frame']] == data
        raw[row['frame']] = data
    assert blob(report['read_only_RAM_snapshot']) == raw[case['frames']]
    native = report['read_only_native_state']
    blob(native)
    regions = {name: blob(row) for name, row in native['regions'].items()}
    reference = NdsImage.open('out/all_routes_combined_v653_candidate.nds').read_file('/__arm9__.bin')
    assert sha(reference) == coordinate.ARM
    assert all(arm[a:b] == reference[a:b] for a, b in coordinate.SPANS)
    fixtures = report['synthetic_location_fixtures']
    assert len(fixtures) == sum('location_town' in c for c in commands)
    for fixture in fixtures:
        before = raw[fixture['frame']]
        after, receipt = coordinate.relocate(reference, before, index)
        receipt.update(actual_current_ARM9_sha256=sha(arm),
                       V735_current_guard='pinned-V712-coordinate-code-exact-V653',
                       village_request_sweep_case=index)
        assert fixture == dict(receipt, frame=fixture['frame'])
        at = receipt['active_ship'] - BASE + 16
        assert before[:at] == after[:at] and before[at + 8:] == after[at + 8:]
    old = next(r for r in read('work/analysis/village_development_v665/proof.json')['all24_development_cases'] if r['index'] == index)
    if index == 9:
        prior = read('work/analysis/Karibib_return_v667/proof.json')
        prefix_rows = read(case['historical_controller'])['entered_character_states']
        labels = [r['English'] for r in prior['complete_developed_menu']['complete_menu_labels']]
    else:
        prefix_rows = old['all_entered_character_prefixes_native_buffer_cursor_capacity_and_complete_display_verified']
        labels = [r['English'] for r in old['complete_developed_menu']['complete_menu_labels']]
    phases, states = case['phases'], []
    for phase in ('chief_request', 'complete_password_before_submission', 'answer_confirmation',
                  'accepted_clue', 'developed_village_menu', 'developed_town_return'):
        state = model(arm, raw[phases[phase]], index, case['name'], True)
        assert state['native_development'] == (0 if phase in ('chief_request', 'complete_password_before_submission', 'answer_confirmation') else 2)
        states.append({'phase': phase, **state})
    marker = read('work/analysis/village_promised_words_plan.json')['keyboard_wrapper']['provider_vtable']
    entries = []
    for n, row in enumerate(prefix_rows):
        snapshot = raw[row['frame']]
        needle = struct.pack('<I', marker)
        owners = [p - 4 for p in range(0x170000, len(snapshot) - 4, 4) if snapshot[p:p + 4] == needle]
        assert len(owners) == 1
        parent = owners[0]
        expected = case['answer'][:n]
        assert snapshot[parent + 0xB4:parent + 0xB4 + n + 1] == expected.encode('ascii') + b'\0'
        assert struct.unpack_from('<I', snapshot, parent + 0x78)[0] == n
        assert struct.unpack_from('<I', snapshot, parent + 0xD8)[0] == 18
        image = images[row['frame']]
        actual = {(x, y) for y in range(11) for x in range(108)
                  if image.getpixel((60 + x, 244 + y)) == (230, 230, 230)}
        assert actual == glyphs(font, expected)
        entries.append({'frame': row['frame'], 'entry': expected, 'native_and_whole108x11_input_exact': True})
    assert len(entries) == len(case['answer']) + 1
    old_clue = old['complete_dialogue_fields']['clue']
    # The two V666 reflows align their margins. Unchanged single-line fields
    # retain their original 16px origin; do not impose a new renderer rule.
    clue_origin = 22 if index in (4, 23) else old_clue['complete_lines'][0]['origin'][0]
    dialogues = {'confirmation': confirmation(images[phases['answer_confirmation']], rom, font, case['answer']),
                 'clue': text_field(images[phases['accepted_clue']], font, old_clue['paragraph'], clue_origin),
                 'facilities': dialog(images[phases['facilities_notice']], font, old['complete_dialogue_fields']['facilities']['paragraph'], 22)}
    developed_menu = menu(images[phases['developed_village_menu']], font, labels)
    final = images[case['frames']]
    header = find_mask(font, case['name'], final, (0, 10, 256, 40))
    u = machine(arm)
    u.mem_write(BASE, raw[case['frames']])
    call(u, 0xB5630, (states[-1]['town'],))
    assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 64)).split(b'\0')[0].decode('ascii') == case['name']
    call(u, 0xB7294, (90 + index, 0))
    background = f'/towngrp/towngrp{u.reg_read(UC_ARM_REG_R0):02d}.pxl'
    assert rom.read_file(background) == NdsImage.open('work/clean.nds').read_file(background)
    assert rom.read_file(background) in raw[case['frames']]
    upper, lower, drawing = replay(rom, raw[case['frames']], regions['9REG'], regions['LCDM'], regions['DTCM'], regions['ITCM'])
    expected = [[color5(final.getpixel((x, y + start))) for y in range(192) for x in range(256)] for start in (0, 192)]
    assert [rgb5(upper), rgb5(lower)] == expected
    assert upper == regions['LCDM'][0x40000:0x58000] and lower == regions['LCDM'][0x60000:0x78000]
    native_path = ROOT / f'case_{index:02d}/native_Town_replay.json'
    save(native_path, drawing)
    proof = {'index': index, 'name': case['name'], 'frames': case['frames'],
             'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
             'journal': str(journal_path), 'journal_sha256': sha(journal_path.read_bytes()),
             'unique_capture_frames': len(images), 'whole_pause_RAM_snapshots_checked': len(raw),
             'all7_exported_native_regions_hash_checked': len(regions) == 7,
             'all_coordinate_fixture_receipts_replayed_and_only8bytes_owned': len(fixtures),
             'normal_development_states': states, 'all_typed_prefixes': entries,
             'complete_dialogue_fields': dialogues, 'complete_developed_menu': developed_menu,
             'complete_current_Town_header': header, 'current_resident_source_exact_background': background,
             'native_Town_replay': str(native_path), 'native_Town_replay_sha256': sha(native_path.read_bytes()),
             'whole98304_native_scene_pixels_match_both_actual_displays_and_LCDC': True,
             'original_footer_resubmitted_through_original_API_in_isolated_native_replay': True,
             'requests': requests(rom, case, contract, pre),
             'not_normal_earned_voyage_or_all_story_contexts_or_hardware': True,
             'observed_only_not_a_new_unobserved_baseline_pair': True,
             'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(ROOT / f'case_{index:02d}/proof.json', proof)
    print(f"V735 verified {index:02d} {case['name']}: {len(images)} screens, {sum(proof['requests']['counts'].values())} classified requests, full native Town.", flush=True)
    return proof


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', type=int)
    args = parser.parse_args()
    if args.index is not None:
        verify_case(args.index)
        return
    sweep = read(ROOT / 'sweep_result.json')
    assert sweep['all23_workers_terminal'] and not sweep['signals'] and len(sweep['finished']) == 23
    pre = read(ROOT / 'preflight.json')
    assert sha(Path(pre['paired_Ezo_proof']).read_bytes()) == pre['paired_Ezo_proof_sha256']
    prior_pre = read('work/analysis/village_images_v734/preflight.json')
    contract = read(pre['shared_source_contract'])
    for path, digest in (
            ('scripts/headless_desmume_v193.py', prior_pre['shared_harness_sha256']),
            ('scripts/native_village_visits_v664.py', prior_pre['location_helper_sha256']),
            ('scripts/observe_file_requests_v681.py', contract['assembler_sha256']),
            ('scripts/trace_file_ids_v683.py', contract['mapped_read_helper_sha256'])):
        assert sha(Path(path).read_bytes()) == digest
    controls = read('work/analysis/village_images_v734/native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 30 and len(controls['read_policy_cases']) == 8
    prior_mapping = read('work/analysis/script_sources_v733/source_contract.json')
    assert prior_mapping['CPU_memory_read_helper_sha256'] == contract['mapped_read_helper_sha256']
    assert len(read('work/analysis/script_sources_v733/proof.json')['ten_DTCM_precedence_boundary_controls']) == 10
    results = []
    for case in read(ROOT / 'cases.json'):
        path = ROOT / f"case_{case['index']:02d}/proof.json"
        result = read(path) if path.exists() else None
        if result is None or result['verifier_sha256'] != sha(Path(__file__).read_bytes()):
            result = verify_case(case['index'])
        assert result['verifier_sha256'] == sha(Path(__file__).read_bytes())
        assert result['report_sha256'] == sha(Path(result['report']).read_bytes())
        results.append(result)
    assert {r['index'] for r in results} == set(range(24)) - {18}
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    # Actual current screenshots, including both reflowed clues and the five aliases.
    for page, chosen in enumerate((list(range(12)), list(range(12, 24)))):
        sheet = Image.new('RGB', (1024, 1320), '#263238')
        draw = ImageDraw.Draw(sheet)
        for cell, index in enumerate(chosen):
            if index == 18:
                ez = read(pre['paired_Ezo_proof'])
                report = read(ez['reports']['baseline']['path'])
                name, frame = 'Ezo (carried V734)', report['frames']
            else:
                result = next(r for r in results if r['index'] == index)
                report = read(result['report'])
                name, frame = result['name'], result['frames']
            image = Image.open(next(r['path'] for r in report['frames_captured'] if r['frame'] == frame)).convert('RGB')
            x, y = (cell % 4) * 256, (cell // 4) * 440
            draw.text((x + 6, y + 7), f'{index:02d} {name}', fill='white')
            draw.text((x + 6, y + 24), 'V712 / location fixture / final Town', fill='#b0bec5')
            sheet.paste(image, (x, y + 50))
        sheet.save(ROOT / f'current24_Town_review_{page + 1}.png')
    proof = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
             'all23_new_terminal_current_cases': results,
             'Ezo_paired_scope_carried_forward': {'path': pre['paired_Ezo_proof'], 'sha256': pre['paired_Ezo_proof_sha256']},
             'new_total_requests': dict(sum((Counter(r['requests']['counts']) for r in results), Counter())),
             'new_unique_capture_frames': sum(r['unique_capture_frames'] for r in results),
             'new_complete_native_Town_pixels': 23 * 98304,
             'all24_tested_arrival_password_development_return_sequences_covered_no8card_requests': True,
             'no_global_unused_or_other_story_debug_legacy_consumer_claim': True,
             'original_small_control_and_raw_comic_parent_requirements_still_open': True,
             'prototype_single_line_origin_assumption_corrected_using_retained_source_display_contract_no_ROM_change': True,
             'same_validated_V734_observer_controls_and_Ezo_baseline_carried_not23_new_baseline_pairs': True,
             'carried_observer_controls': {'grouped_host_cases': 30, 'main_RAM_mirror_cases': 8,
                                          'DTCM_precedence_cases': 10},
             'release_hashes_unchanged': pre['release_hashes'],
             'runner_sha256': pre['runner_sha256'], 'observer_sha256': pre['shared_observer_sha256'],
             'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(ROOT / 'proof.json', proof)
    print('V735 full23-case current scope verified; paired Ezo carried; original card triggers remain open.', flush=True)


if __name__ == '__main__':
    main()
