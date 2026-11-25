"""Prove complete initialization return and the scoped live payload counterfactual."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.replay_raw_portrait_tail_v689 import execute
from scripts.trace_chooser_raw_independence_v690 import CAP, PATTERN, ROOT
from scripts.verify_raw_portrait_tail_v689 import pictures
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    producer = Path('scripts/trace_chooser_raw_independence_v690.py')
    assert pre['producer_sha256'] == sha(producer.read_bytes())
    assert pre['fixture_manifest_sha256'] == sha(Path(pre['fixture_manifest']).read_bytes())
    assert pre['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    assert sha(CORE.read_bytes()) == CORE_SHA
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    controls = read(ROOT / 'prefix_controls/native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 20 and len(controls['read_policy_cases']) == 8
    assert sha(Path(pre['baseline_report']).read_bytes()) == pre['baseline_report_sha256']
    old = pictures(read(pre['baseline_report']))
    runs, shots, event_sets = {}, {}, {}
    for name in ('control', 'poison'):
        folder = CAP / ('chooser_raw_independence_v690_' + name)
        rp = folder / 'capture_report.json'
        report, contract = read(rp), read(folder / 'run_contract.json')
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
        assert report['frames'] == 4000 and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report.get('battery_save_preloaded')
        assert report['scripted_input_schedule'] == read(pre['inputs'])
        assert report['synthetic_raw_portrait_buffer_fixture'] == (name == 'poison')
        assert {k for k, v in report.items() if k.startswith('synthetic_') and v} == (
            {'synthetic_raw_portrait_buffer_fixture'} if name == 'poison' else set())
        assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
        assert contract['producer_sha256'] == pre['producer_sha256']
        assert contract['fixture_manifest_sha256'] == pre['fixture_manifest_sha256']
        events = read(folder / 'observer/events.json')
        assert events['producer_sha256'] == pre['producer_sha256']
        assert events['source_contract_sha256'] == pre['source_contract_sha256']
        assert len(events['rows']) == events['callbacks'] == 10 and events['ignored'] == 0
        assert not events['errors'] and not events['mismatches']
        assert events['all_host_slots_restored_core_file_exact']
        assert events['CPU_DTCM_configuration_unchanged_WRAM_only_declared_single_fixture_write']
        assert len(events['fixture_writes']) == int(name == 'poison')
        assert [r['kind'] for r in events['rows']] == ['raw_entry', 'raw_return'] * 4 + ['loop_complete', 'initialization_return']
        for row in events['rows']:
            assert sha(Path(row['RAM']).read_bytes()) == row['RAM_sha256']
            assert sha(Path(row['DTCM']).read_bytes()) == row['DTCM_sha256']
        start, actual = events['rows'][-2:]
        a = struct.unpack('<32I', bytes.fromhex(start['CPU128_hex']))
        b = struct.unpack('<32I', bytes.fromhex(actual['CPU128_hex']))
        ram = Path(start['RAM']).read_bytes()
        saved = struct.unpack_from('<9I', ram, a[17] + 0x174 - 0x02000000)
        assert saved[-1] == b[2] == 0x0209DC90
        native, replay = execute(start, b[2])
        assert replay['stop_PC'] == b[2] and replay['registers'] == list(b[4:19])
        assert replay['CPSR'] == b[20]
        assert replay['registers'][4:12] == list(saved[:8])
        assert replay['registers'][13] == a[17] + 0x174 + 36
        assert not replay['raw_payload_reads'] and not replay['raw_payload_writes']
        assert not replay['executed_instruction_words_different_from_original']
        assert replay['unique_executed_instructions'] == 873
        assert bytes(native.mem_read(0x02000000, 0x400000)) == Path(actual['RAM']).read_bytes()
        assert bytes(native.mem_read(0x027E0000, 0x4000)) == Path(actual['DTCM']).read_bytes()
        shots[name] = pictures(report)
        assert shots[name].keys() == old.keys() and len(shots[name]) == 21
        if name == 'control':
            assert all(im.tobytes() == old[f].tobytes() for f, im in shots[name].items())
            assert (folder / 'final_arm9_ram.bin').read_bytes() == (Path(pre['baseline_report']).parent / 'final_arm9_ram.bin').read_bytes()
        runs[name] = {'report': str(rp), 'report_sha256': sha(rp.read_bytes()),
            'events': str(folder / 'observer/events.json'),
            'events_sha256': sha((folder / 'observer/events.json').read_bytes()),
            'complete_initialization_remainder': replay,
            'actual_return_CPU_CPSR_saved_registers_stack_RAM_DTCM_exact': True}
        event_sets[name] = events
    assert all(im.tobytes() == shots['poison'][f].tobytes() for f, im in shots['control'].items())
    control_folder, poison_folder = (CAP / ('chooser_raw_independence_v690_' + n) for n in ('control', 'poison'))
    assert (control_folder / 'final_arm9_ram.bin').read_bytes() == (poison_folder / 'final_arm9_ram.bin').read_bytes()
    assert [r['CPU128_hex'] for r in event_sets['control']['rows']] == [r['CPU128_hex'] for r in event_sets['poison']['rows']]
    # The fixture changes exactly the guarded raw input and no other observed state.
    fixture, = event_sets['poison']['fixture_writes']
    before, after = (Path(fixture[k]).read_bytes() for k in ('source_before_RAM', 'after_RAM'))
    assert sha(before) == fixture['source_before_RAM_sha256'] and sha(after) == fixture['after_RAM_sha256']
    expected = bytearray(before)
    expected[0x233040:0x233040 + 14144] = PATTERN
    assert after == expected and fixture['pattern_sha256'] == sha(PATTERN)
    assert fixture['changed_bytes'] == sum(a != b for a, b in zip(before, after, strict=True))
    for index, (control, poison) in enumerate(zip(event_sets['control']['rows'], event_sets['poison']['rows'], strict=True)):
        expected = bytearray(Path(control['RAM']).read_bytes())
        if index >= 8:
            expected[0x233040:0x233040 + 14144] = PATTERN
        assert Path(poison['RAM']).read_bytes() == expected
        assert Path(poison['DTCM']).read_bytes() == Path(control['DTCM']).read_bytes()
    sheet = Image.new('RGB', (768, 820), '#263238')
    draw = ImageDraw.Draw(sheet)
    for row, case in enumerate(('control', 'poison')):
        for col, frame in enumerate((1200, 1500, 2000)):
            draw.text((col * 256 + 5, row * 410 + 5), f'{case}: frame {frame}', fill='white')
            sheet.paste(shots[case][frame], (col * 256, row * 410 + 24))
    sp = ROOT / 'control_and_isolated_buffer_fixture.png'
    sheet.save(sp)
    save(ROOT / 'proof.json', {
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'], 'runs': runs,
        'two_terminal4000_frame_cold_boots21_whole_fixture_control_pairs21_retained_baseline_pairs_exact': True,
        'both_complete_terminal_main_RAM_states_equal_retained_V689': True,
        'all20_actual_event_CPU_prefixes_equal_between_cases': True,
        'exact_single_declared_fixture_write': fixture,
        'both873_instruction_original_initialization_remainders_no_raw_reads_or_writes': True,
        'first_sampled_portrait_and_confirmation_displays_do_not_depend_on_final_raw17_input': True,
        'sampled_frames_not_every_console_frame_other_consumers_or_global_nonuse_proof': True,
        'ROM_artwork_patch_registry_and_release_pointers_unchanged': True,
        'all18_plaques_incomplete22_original_requirements_other_graphics_gates_open': True,
        'review_sheet': str(sp), 'review_sheet_sha256': sha(sp.read_bytes()),
        'producer_sha256': pre['producer_sha256'],
        'replay_helper_sha256': sha(Path('scripts/replay_raw_portrait_tail_v689.py').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V690:complete original initialization return matches; isolated final raw replacement leaves21 full screens and terminal RAM exact.', flush=True)


if __name__ == '__main__':
    main()
