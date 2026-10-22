"""Check paired actual frames/RAM and independent recorded script-source bounds."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.observe_script_sources_v733 import ROM, ROOT
from scripts.run_script_sources_v733 import CAP, FRAMES
from scripts.trace_file_ids_v683 import mapped_read
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    assert pre['candidate_sha256'] == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    for name in ('runner', 'observer'):
        path = Path('scripts') / ('run_script_sources_v733.py' if name == 'runner' else 'observe_script_sources_v733.py')
        assert pre[name + '_sha256'] == sha(path.read_bytes())
    assert pre['shared_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    contract = read(ROOT / 'source_contract.json')
    for key, hashkey in (('original_filter_assembler', 'original_filter_assembler_sha256'),
                        ('CPU_memory_read_helper', 'CPU_memory_read_helper_sha256')):
        assert sha(Path(contract[key]).read_bytes()) == contract[hashkey]
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 10 and len(controls['read_policy_cases']) == 8
    assert controls['observer_sha256'] == contract['original_filter_assembler_sha256']
    # Current direct helper controls plus its pinned original emulator read policy.
    policy = read('work/analysis/file_ids_v683/source_contract.json')['ARM9_CPU_read_policy']
    for key in ('MMU_header', 'SFORMAT_source'):
        assert sha(Path(policy[key]).read_bytes()) == policy[key + '_sha256']
    raw, dtcm, base = b'\x35' * 0x400000, bytes(range(256)) * 64, 0x027E0000
    mapping = []
    for address, length, valid, use_dtcm in ((base, 16, True, True), (base + 16352, 32, True, True),
        (base + 16383, 1, True, True), (base + 16383, 2, False, True),
        (base - 1, 2, False, False), (base - 16, 16, True, False),
        (base + 16384, 16, True, False), (0x02001000, 128, True, False),
        (0x02401000, 128, True, False), (0x03000000, 1, False, False)):
        try:
            result = mapped_read(raw, dtcm, base, address, length)
        except ValueError:
            assert not valid
        else:
            assert valid and result == (dtcm[address - base:address - base + length] if use_dtcm else b'\x35' * length)
        mapping.append({'address': address, 'length': length, 'accepted': valid, 'DTCM_selected': valid and use_dtcm})
    reports, pictures = {}, {}
    for mode in ('baseline', 'observed'):
        folder = CAP / ('script_sources_v733_' + mode)
        report = read(folder / 'capture_report.json')
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['frames'] == 4000
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert 'battery_save_preloaded' not in report and 'synthetic_inventory_fixtures' not in report
        assert report['core_DLL_sha256'] == contract['core_sha256']
        assert report['scripted_input_schedule'] == read(ROOT / 'inputs.json')
        pictures[mode] = {}
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            pictures[mode].setdefault(row['frame'], Image.open(row['path']).convert('RGB'))
        assert set(pictures[mode]) == set(FRAMES)
        reports[mode] = {'path': str(folder / 'capture_report.json'),
            'sha256': sha((folder / 'capture_report.json').read_bytes())}
        final = report['read_only_RAM_snapshot']
        assert len(Path(final['path']).read_bytes()) == 0x400000
        assert sha(Path(final['path']).read_bytes()) == final['sha256']
    a, b = [read(reports[m]['path']) for m in ('baseline', 'observed')]
    assert a['core_options'] == b['core_options']
    assert Path(a['read_only_RAM_snapshot']['path']).read_bytes() == Path(b['read_only_RAM_snapshot']['path']).read_bytes()
    for frame in FRAMES:
        assert pictures['baseline'][frame].tobytes() == pictures['observed'][frame].tobytes()
    trace_path = CAP / 'script_sources_v733_observed/observer/commands.json'
    trace = read(trace_path)
    assert not trace['errors'] and not trace['mismatches']
    assert trace['callbacks'] == len(trace['rows']) == 41
    assert trace['all_host_slots_restored_and_core_file_exact']
    assert trace['observer_sha256'] == pre['observer_sha256']
    assert trace['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    rom = NdsImage.open(ROM)
    blocks = [IlnkContainer.parse(rom.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)]
    pairs, starts = [], []
    for n, row in enumerate(trace['rows']):
        cpu = struct.unpack('<32I', bytes.fromhex(row['CPU128_hex']))
        target = next(t for t in contract['targets'] if t['name'] == row['kind'])
        assert cpu[1:3] == (target['word'], target['PC'])
        assert cpu[17] == row['player']
        descriptor = struct.unpack('<4I', bytes.fromhex(row['player_descriptor16_hex']))
        source = row['source']
        assert source['classification'] == 'original_SC_cache'
        assert source['route'] == 0 and source['block'] == 44
        expected = blocks[source['route']][source['block']]
        actual = Path(source['actual_payload_file']).read_bytes()
        assert actual == expected and source['payload_bytes'] == len(actual) == 6768
        assert source['actual_sha256'] == source['registered_sha256'] == sha(actual)
        assert source['whole_resident_payload_exact_ROM']
        assert source['cache_address'] == row['player'] + 0x58 and source['payload_address'] == row['player'] + 0x60
        assert source['cache_vtable'] == 0x02134578 and descriptor[:2] == (0x021345B0, source['instruction_pointer'])
        offset = source['instruction_offset']
        assert offset == source['instruction_pointer'] - source['payload_address'] and 8 <= offset < len(actual) - 1
        assert source['first_word'] == struct.unpack_from('<H', actual, offset)[0]
        assert source['packet_prefix_hex'] == actual[offset:offset + 16].hex()
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        if row['kind'] == 'before_command':
            assert cpu[5] == row['player'] and row['mode'] == cpu[7]
            starts.append(n)
        else:
            original = trace['rows'][row['entry_row']]
            assert original['kind'] == 'before_command' and original['player'] == row['player']
            assert original['source'] == source and original['frame'] <= row['frame']
            assert row['decoded_length'] == descriptor[2] and row['result_words'][0] == descriptor[3]
            pairs.append({'entry_row': row['entry_row'], 'return_row': n,
                'frames': [original['frame'], row['frame']], 'word': source['first_word'],
                'offset': offset, 'decoded_length': row['decoded_length'],
                'whole6768_byte_active_source_exact_before_and_after': True})
    assert len(starts) == 21 and len(pairs) == 20
    assert trace['unreturned_at_capture_end'] == [{'player': trace['rows'][40]['player'], 'entry_row': 40}]
    sheet = Image.new('RGB', (1024, 816), '#263238')
    draw = ImageDraw.Draw(sheet)
    for x, mode in ((0, 'baseline'), (512, 'observed')):
        draw.text((x + 12, 12), f'V712 ordinary Rafael New Game / {mode} / frame4000', fill='white')
        sheet.paste(pictures[mode][4000].resize((512, 768), Image.Resampling.NEAREST), (x, 40))
    sheet.save(ROOT / 'baseline_observed_review.png')
    proof = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'two_terminal4000_frame_ordinary_New_Game_cold_boots_no_save_or_gameplay_fixture': True,
        'reports': reports, 'all16_complete_RGB_frame_pairs_exact': True,
        'final_whole4MiB_RAM_pair_exact': a['read_only_RAM_snapshot']['sha256'],
        'trace': str(trace_path), 'trace_sha256': sha(trace_path.read_bytes()),
        'actual_native_callback_count': 41, 'complete_command_entry_return_pairs': pairs,
        'all21_pre_command_sources_and20_return_sources_match_entire_registered_SC0_block44': True,
        'whole_resident_script_bytes': 6768,
        'observed_pre_command_word_counts': dict(Counter(hex(trace['rows'][n]['source']['first_word']) for n in starts)),
        'one_command_still_awaiting_in_game_input_at_capture_end_not_a_live_process': trace['unreturned_at_capture_end'],
        'temporary_write_restore_unobserved_contexts_other_SC_blocks_and_village_triggers_not_excluded': True,
        'ten_current_native_host_prefix_controls_eight_mirror_controls': True,
        'ten_DTCM_precedence_boundary_controls': mapping, 'pinned_original_emulator_read_policy': policy,
        'runner_sha256': pre['runner_sha256'], 'observer_sha256': pre['observer_sha256'],
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'release_hashes_unchanged': pre['release_hashes'], 'full_goal_complete': False}
    save(ROOT / 'proof.json', proof)
    print('V733:41 real command observations/20 full entry-return pairs retain entire SC0 block44;16 whole screen pairs/final4MiB match baseline.')


if __name__ == '__main__':
    main()
