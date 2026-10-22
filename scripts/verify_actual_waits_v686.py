"""Prove each blank capture lies inside the original zero-argument modal call."""

import struct
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.run_opening_holds_v686 import CAP, FRAMES, ROOT
from scripts.verify_opening_holds_v686 import HOLDS
from scripts.verify_village_wrap_v608 import read, save


def pictures(report):
    result = {}
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        im = Image.open(path).convert('RGB')
        if row['frame'] in result:
            assert result[row['frame']].tobytes() == im.tobytes()
        result[row['frame']] = im
    return result


def main():
    pre = read(ROOT / 'preflight.json')
    source = read(ROOT / 'wait_source_contract.json')
    controls = read(ROOT / 'wait_native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 10 and len(controls['read_policy_cases']) == 8
    observer_sha = sha(Path('scripts/observe_wait_entries_v686.py').read_bytes())
    assert observer_sha == controls['current_observer_sha256']
    assert sha(Path('scripts/observe_file_requests_v681.py').read_bytes()) == source['original_assembler_sha256']
    assert sha(CORE.read_bytes()) == CORE_SHA
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    results = {}
    for version in ('source', 'current'):
        folder = CAP / ('opening_wait_entries_v686_' + version)
        rp = folder / 'capture_report.json'
        report, contract = read(rp), read(folder / 'run_contract.json')
        expected_sha = pre['clean_sha256'] if version == 'source' else pre['candidate_sha256']
        assert report['ROM_sha256'] == expected_sha and report['core_DLL_sha256'] == CORE_SHA
        assert report['frames'] == 31000 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule'] == read(pre['inputs'])
        assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
        assert {k for k, v in report.items() if k.startswith('synthetic_') and v} == {'synthetic_gallery_fixtures'}
        assert contract['runner_sha256'] == sha(Path('scripts/run_wait_entries_v686.py').read_bytes())
        assert contract['observer_sha256'] == observer_sha
        assert contract['inputs_sha256'] == pre['inputs_sha256']
        assert sha(Path(contract['unlock_manifest']).read_bytes()) == contract['unlock_manifest_sha256']
        baseline_path = (CAP / 'opening_holds_v686_source/capture_report.json' if version == 'source'
                         else CAP / 'story_percent_v685_baseline/capture_report.json')
        baseline = read(baseline_path)
        assert baseline['ROM_sha256'] == expected_sha and baseline['scripted_input_schedule'] == report['scripted_input_schedule']
        actual, previous = pictures(report), pictures(baseline)
        assert set(actual) == {1, 60, 180, *FRAMES} and len(actual) == 12
        assert actual.keys() <= previous.keys()
        assert all(im.tobytes() == previous[f].tobytes() for f, im in actual.items())
        assert (folder / 'final_arm9_ram.bin').read_bytes() == (baseline_path.parent / 'final_arm9_ram.bin').read_bytes()
        mp = folder / 'observer/actual_modal_intervals.json'
        meta = read(mp)
        assert not meta['errors'] and not meta['mismatches'] and meta['pending_entry'] is None
        assert meta['observer_sha256'] == observer_sha
        assert meta['source_contract_sha256'] == sha((ROOT / 'wait_source_contract.json').read_bytes())
        assert meta['each_callback_CPU_WRAM_DTCM_and_configuration_unchanged']
        assert meta['all_slots_restored_before_free_core_file_exact']
        assert meta['callbacks'] == len(meta['rows']) + meta['ignored_other_modal_callers']
        targets = {t['PC']: t for t in source['targets']}
        for row in meta['rows']:
            cpu = struct.unpack('<32I', bytes.fromhex(row['CPU128_hex']))
            assert cpu[1] == targets[cpu[2]]['word'] and cpu[19] == cpu[2] + 8
            raw = Path(row['actual_RAM']).read_bytes()
            assert len(raw) == 0x400000 and sha(raw) == row['actual_RAM_sha256']
            assert raw[0x18F250:0x18F2B0].hex() == row['owner96_hex']
            assert struct.unpack_from('<I', raw, 0x18F254)[0] == row['actual_VM_cursor']
            assert row['actual_VM_cursor'] == 0x0218F2B0 + row['chapter_offset']
            assert struct.unpack_from('<H', raw, row['actual_VM_cursor'] - 0x02000000)[0] == row['original_command']
            assert struct.unpack_from('<I', raw, 0x18F2AC)[0] == row['chapter_cache_index'] == 33
            assert sha(raw[0x18F2B0:0x18F2B0 + 2528]) == source['chapter_sha256'][version]
            if row['kind'] == 'modal_entry':
                assert cpu[4:6] == (0, 0) and cpu[18] == 0x0202A218
                assert row['actual_original_arguments'] == [0, 0]
            else:
                assert cpu[2] == 0x0202A218
                assert row['native_modal_return_value_recorded_without_boolean_assumption'] == cpu[4]
        assert len(meta['rows']) % 2 == 0
        intervals = []
        for n in range(0, len(meta['rows']), 2):
            entered, returned = meta['rows'][n:n + 2]
            assert entered['kind'] == 'modal_entry' and returned['kind'] == 'script_wait_return'
            assert returned['matching_actual_entry_index'] == n
            assert entered['chapter_offset'] == returned['chapter_offset']
            assert entered['original_command'] == returned['original_command']
            assert entered['frame'] <= returned['frame']
            intervals.append({'entry_frame': entered['frame'], 'return_frame': returned['frame'],
                              'chapter_offset': entered['chapter_offset'], 'command': entered['original_command']})
        proven = []
        for sf, cf, offset in HOLDS:
            frame = sf if version == 'source' else cf
            selected = [i for i in intervals if i['chapter_offset'] == offset and i['command'] == 0x2000
                        and i['entry_frame'] <= frame < i['return_frame']]
            interval, = selected
            a = next(p for p in report['scripted_input_schedule'] if 'A' in p['buttons'] and p['start'] > frame)
            following = next(p for p in report['scripted_input_schedule'] if p['start'] > a['start'])
            assert a['start'] <= interval['return_frame'] < following['start']
            proven.append({**interval, 'blank_capture_frame_inside_actual_modal_call': frame,
                'first_following_A_press': a,
                'actual_return_follows_first_A_and_precedes_every_subsequent_scheduled_action': True,
                'return_frames_after_first_A_start': interval['return_frame'] - a['start'],
                'modal_return_not_assumed_to_precede_button_release_or_invented_cleanup_latency': True})
        results[version] = {'report': str(rp), 'report_sha256': sha(rp.read_bytes()),
            'baseline_report': str(baseline_path), 'baseline_sha256': sha(baseline_path.read_bytes()),
            'trace': str(mp), 'trace_sha256': sha(mp.read_bytes()), 'all_wait_intervals': intervals,
            'three_actual_blank_capture_intervals': proven,
            'twelve_complete_two_screen_baseline_pairs_and_terminal_RAM_exact': True,
            'callbacks': meta['callbacks'], 'ignored_other_modal_callers': meta['ignored_other_modal_callers']}
    save(ROOT / 'actual_wait_proof.json', {'candidate_sha256': pre['candidate_sha256'], 'versions': results,
        'all_three_source_and_current_blank_captures_inside_actual_original_zero_argument_modal_calls': True,
        'not_inferred_from_cached_VM_cursor_alone_or_arbitrary_screenshot_lag': True,
        '24_whole_screen_baseline_pairs_two_terminal_RAM_pairs_and_ten_native_prefix_controls_pass': True,
        'each_wait_returns_after_first_following_A_before_any_subsequent_scheduled_action': True,
        'GUI_actual_entry_and_return_observed_without_bridging_or_game_state_writes': True,
        'scope_is_three_explicit_script_waits_not_global_blank_page_A_phase_or_full_route_acceptance': True,
        'component_and_photo_proof': str(ROOT / 'proof.json'),
        'component_and_photo_proof_sha256': sha((ROOT / 'proof.json').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V686 actual source/current modal calls bracket all six blank captures; returns follow A;24 whole baseline pairs exact.', flush=True)


if __name__ == '__main__':
    main()
