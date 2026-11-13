"""Bind every observed numeric/range request to ROM tables and retained baselines."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.run_village_visits_v664 import CAP
from scripts.trace_file_ids_v683 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def frames(report):
    result = {}
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        image = Image.open(path).convert('RGB')
        if row['frame'] in result:
            assert result[row['frame']].tobytes() == image.tobytes()
        result[row['frame']] = image
    return result


def main():
    pre, source, configs = read(ROOT / 'preflight.json'), read(ROOT / 'source_contract.json'), read(ROOT / 'run_cases.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    producer_sha = sha(Path('scripts/trace_file_ids_v683.py').read_bytes())
    controls = read(ROOT / 'native_prefix_controls.json')
    assert controls['current_trace_source_sha256'] == producer_sha and controls['actual_shared_target_groups_tested']
    assert len(controls['native_host_cases']) == 15 and len(controls['read_policy_cases']) == 8
    assert len(controls['DTCM_precedence_boundary_and_mirror_cases']) == 10
    policy = source['ARM9_CPU_read_policy']
    assert sha(Path(policy['MMU_header']).read_bytes()) == policy['MMU_header_sha256']
    assert sha(Path(policy['SFORMAT_source']).read_bytes()) == policy['SFORMAT_source_sha256']
    assert sha(Path('scripts/observe_file_requests_v681.py').read_bytes()) == source['original_assembler_sha256']
    rom = NdsImage.open(ROM)
    raw = ROM.read_bytes()
    names = {str(i): p for p, i in rom.path_map().items()}
    assert names == source['file_IDs']
    fnt, fnt_size, fat, fat_size, overlay, overlay_size = struct.unpack_from('<6I', raw, 0x40)
    assert fat_size == 8 * len(rom.rom.files) and overlay_size == 32
    file_table = [struct.unpack_from('<2I', raw, fat + i * 8) for i in range(fat_size // 8)]
    for index, (lo, hi) in enumerate(file_table):
        assert raw[lo:hi] == rom.rom.files[index]
    overlay_record = struct.unpack_from('<8I', raw, overlay)
    assert overlay_record[0] == overlay_record[6] == 0 and overlay_record[2] == len(rom.rom.files[0]) == 6208
    special_ranges = {(fat, fat + fat_size): 'ROM FAT', (fnt, fnt + fnt_size): 'ROM FNT',
                      (overlay, overlay + overlay_size): 'ARM9 overlay table'}
    callers = {r['address'] + 4: r['target'] for r in source['direct_caller_census']['aligned_ARM_BL_calls']}
    targets = {t['PC']: t for t in source['targets']}
    case_proofs, all_images = [], {}
    for case, config in configs.items():
        folder = CAP / f'file_ids_v683_v2_{case}'
        path = folder / 'capture_report.json'
        report = read(path)
        baseline_path = Path(config['retained_unmodified_baseline_report'])
        assert sha(baseline_path.read_bytes()) == config['retained_baseline_report_sha256']
        baseline = read(baseline_path)
        for r in (report, baseline):
            assert r['ROM_sha256'] == pre['candidate_sha256'] and r['core_DLL_sha256'] == CORE_SHA
            assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
            assert r['frames'] == config['frames'] and r['scripted_input_schedule'] == read(config['inputs'])
        contract = read(folder / 'run_contract.json')
        assert contract['trace_source_sha256'] == producer_sha
        actual, expected = frames(report), frames(baseline)
        assert actual.keys() == expected.keys() and len(actual) == (16 if case == 'ordinary' else 177)
        assert all(im.tobytes() == expected[f].tobytes() for f, im in actual.items())
        assert (folder / 'final_arm9_ram.bin').read_bytes() == (baseline_path.parent / 'final_arm9_ram.bin').read_bytes()
        if case == 'gallery':
            fixture = read(config['fixture_manifest'])
            assert report['battery_save_preloaded']['source_sha256'] == fixture['fixture_save_sha256']
            assert sha(Path(fixture['fixture_save']).read_bytes()) == fixture['fixture_save_sha256']
            assert sha(Path(fixture['original_donor']).read_bytes()) == fixture['original_donor_sha256']
        else:
            assert not report.get('battery_save_preloaded')
            assert not any(k.startswith('synthetic_') and v for k, v in report.items())
        observed_path = folder / 'observer/SDK_entries.json'
        meta = read(observed_path)
        assert not meta['errors'] and not meta['mismatches'] and meta['callbacks'] == len(meta['rows'])
        assert meta['all_opcode_slots_restored_and_core_file_unchanged']
        assert meta['trace_source_sha256'] == producer_sha
        assert meta['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
        initial = read(CAP / f'file_ids_v683_{case}/observer/SDK_entries.json')
        assert len(initial['rows']) == len(meta['rows'])
        pending, names_seen, extras, ranges, resolved = None, [], [], [], []
        stack_domains = Counter()
        for row, initial_row in zip(meta['rows'], initial['rows'], strict=True):
            cpu = struct.unpack('<32I', bytes.fromhex(row['CPU128_hex']))
            target = targets[cpu[2]]
            assert cpu[1] == target['word'] and cpu[19] == cpu[2] + 8 and row['kind'] == target['name']
            assert row['args'] == list(cpu[4:8]) and row['LR'] == cpu[18]
            assert callers[row['LR']] == cpu[2]
            assert row['entire_CPU_prefix_and4MiB_WRAM_unchanged_by_observation']
            assert row['entire_DTCM_and_configuration_unchanged_by_observation']
            dtcm = bytes.fromhex(row['DTCM16384_hex'])
            base = row['DTCM_base']
            assert len(dtcm) == 16384 and sha(dtcm) == row['DTCM_sha256'] and base == 0x027E0000
            stack = bytes.fromhex(row['stack32_hex'])
            assert len(stack) == 32
            if base <= cpu[17] < base + len(dtcm):
                assert cpu[17] + 32 <= base + len(dtcm)
                assert stack == dtcm[cpu[17] - base:cpu[17] - base + 32]
                stack_domains['DTCM'] += 1
            else:
                assert 0x02000000 <= cpu[17] and cpu[17] + 32 <= 0x02400000
                assert row['entire_before_WRAM_sha256'] == initial_row['entire_before_WRAM_sha256']
                assert row['stack32_hex'] == initial_row['stack32_hex']
                stack_domains['main_RAM_fiber_stack'] += 1
            if base <= cpu[4] < base + len(dtcm):
                assert bytes.fromhex(row['file_object64_hex']) == dtcm[cpu[4] - base:cpu[4] - base + 64]
            if row['kind'] == 'filename':
                assert pending is None
                text = bytes.fromhex(row['filename128_hex']).split(b'\0')[0].decode('ascii')
                assert text == row['filename']
                pending = row
                names_seen.append((row['frame'], row['filename'], row['args'][0], row['LR']))
                continue
            assert bytes.fromhex(row['archive128_hex'])[:4] == b'rom\0'
            if row['kind'] == 'direct_range':
                assert row['file_ID'] == struct.unpack_from('<I', stack)[0] == 0xFFFFFFFF
                assert row['byte_range'] == list(cpu[6:8])
                span = tuple(row['byte_range'])
                assert span in special_ranges
                ranges.append({'frame': row['frame'], 'caller_return': row['LR'],
                    'range': list(span), 'source': special_ranges[span], 'complete_bytes_sha256': sha(raw[span[0]:span[1]])})
                continue
            index = row['file_ID']
            assert index == cpu[6] and 0 <= index < len(file_table)
            path_name = names[str(index)]
            if row['LR'] == 0x020DED7C:
                assert pending is not None and pending['args'][0] == row['args'][0]
                requested = '/' + pending['filename'].replace('\\', '/').lstrip('/')
                assert requested.casefold() == path_name.casefold()
                pending = None
            else:
                assert pending is None
                assert (index, row['LR']) in ((0, 0x020DF9BC), (0, 0x020DF76C),
                                                (2, 0x020EA8B8), (2, 0x020EC9A0))
                assert index == 0 or path_name == '/sound_data.sdat'
                extras.append({'frame': row['frame'], 'file_ID': index, 'path': path_name,
                    'caller_return': row['LR'], 'role': 'ARM9 overlay 0 code' if index == 0 else 'sound SDAT'})
            lo, hi = file_table[index]
            resolved.append({'file_ID': index, 'path': path_name, 'ROM_extent': [lo, hi],
                             'whole_file_sha256': sha(raw[lo:hi])})
        assert pending is None
        old_rows = read(CAP / f'file_requests_v681_{case}_observed/observer/requests.json')['rows']
        old_names = [(r['frame'], r['filename'], r['args'][0], r['LR']) for r in old_rows if 'filename' in r]
        assert names_seen == old_names
        assert [(r['frame'], r['kind'], r['args'], r['LR']) for r in meta['rows']] == [
            (r['frame'], r['kind'], r['args'], r['LR']) for r in initial['rows']]
        assert len(ranges) == 4 and Counter(r['source'] for r in ranges) == {
            'ROM FAT': 1, 'ROM FNT': 1, 'ARM9 overlay table': 2}
        case_proofs.append({'case': case, 'report': str(path), 'report_sha256': sha(path.read_bytes()),
            'retained_baseline_report': str(baseline_path), 'retained_baseline_sha256': sha(baseline_path.read_bytes()),
            'whole_RGB_screen_pairs': len(actual), 'terminal_RAM_exact': True,
            'observer_trace': str(observed_path), 'observer_trace_sha256': sha(observed_path.read_bytes()),
            'entry_counts': dict(Counter(r['kind'] for r in meta['rows'])),
            'all_filename_requests_exact_V681': True, 'extra_numeric_requests': extras,
            'all_numeric_IDs_resolve_exact_ROM_FAT_files': resolved, 'all_direct_ranges': ranges,
            'actual_stack_domains': dict(stack_domains),
            'DTCM_stack_fields_reconstructed_from_full_actual_DTCM_main_RAM_fiber_fields_repeat': True,
            'initial_trace_registers_repeat_but_its_main_RAM_stack_fields_rejected': True})
        all_images[case] = actual
    sheet = Image.new('RGB', (1024, 410), '#263238')
    draw = ImageDraw.Draw(sheet)
    for n, (case, frame) in enumerate((('ordinary', 1200), ('ordinary', 4000),
                                      ('gallery', 180), ('gallery', configs['gallery']['frames']))):
        draw.text((n * 256 + 4, 4), f'V678 {case} {frame}', fill='white')
        sheet.paste(all_images[case][frame], (n * 256, 24))
    review = ROOT / 'SDK_scope_review.png'
    sheet.save(review)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'cases': case_proofs, '15_grouped_prefix8_mirror10_DTCM_read_policy_controls_pass': True,
        'all193_whole_screen_pairs_and_two_terminal_RAM_pairs_match_retained_unmodified_baselines': True,
        'only_extra_numeric_IDs_are_overlay0_and_sound_data_in_these_sequences': True,
        'all8_direct_ranges_are_complete_original_ROM_FNT_FAT_or_overlay_tables': True,
        'numeric_ID_and_direct_range_entries_not_successful_open_returns_or_global_nonuse': True,
        'initial_diagnostic_wrong_stack_mapping_retained_corrected_before_claiming_stack_arguments': True,
        'all18_plaques_incomplete22_original_requirements_and_other_gates_open': True,
        'review_sheet': str(review), 'review_sheet_sha256': sha(review.read_bytes()),
        'producer_sha256': producer_sha, 'verifier_sha256': sha(Path(__file__).read_bytes()),
        'current_goal_turn_classification': 'progress', 'full_goal_complete': False})
    print('V683: all numeric IDs/ranges typed;193 full baseline pairs exact; no additional graphics path in these two sequences.', flush=True)


if __name__ == '__main__':
    main()
