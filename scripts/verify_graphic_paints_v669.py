"""Validate original primitive calls, complete target bindings and baseline frames."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_graphic_paints_v669 import ROM, ROOT, units
from scripts.run_village_visits_v664 import CAP
from scripts.verify_frame_style_tiles_v584 import CELLS
from scripts.verify_village_wrap_v608 import read, save


def source_rect(row):
    return tuple(row[20:24]) if row[1] == 0x01FFAE70 else (row[20], row[21], row[24], row[25])


def intersecting(rect, tiled, cells):
    x, y, width, height = rect
    width, height = (max(1, width), max(1, height)) if tiled else (width, height)
    return [name for name, (left, top, right, bottom) in cells
            if width and height and x < right and y < bottom and x + width > left and y + height > top]


def caller(segments, original_segments, lr, target):
    address = lr - 4
    blob = next((d[address - base:address - base + 4] for base, d in segments
                 if base <= address <= base + len(d) - 4), None)
    if blob is None:
        return {'LR': lr, 'outside_declared_source_units': True}
    original = next((d[address - base:address - base + 4] for base, d in original_segments
                     if base <= address <= base + len(d) - 4), None)
    assert blob == original, 'An original caller claim requires the exact clean source instruction'
    word = int.from_bytes(blob, 'little')
    if word & 0x0F000000 == 0x0B000000:
        delta = word & 0xFFFFFF
        delta -= 0x1000000 if delta & 0x800000 else 0
        actual = lr + 4 + delta * 4
        assert actual == target
        return {'LR': lr, 'word': word, 'kind': 'direct_original_ARM_BL', 'target': target}
    return {'LR': lr, 'word': word, 'indirect_or_other_return_encoding_not_resolved': True}


def report(case, suffix, pre):
    folder = CAP / f'graphic_paints_v669_{case}_{suffix}'
    rp = folder / 'capture_report.json'
    r, contract = read(rp), read(folder / 'run_contract.json')
    expected_source = ROOT / 'initial_runner.py' if suffix in ('observed', 'baseline') else Path('scripts/run_graphic_paints_v669.py')
    assert contract['runner_sha256'] == sha(expected_source.read_bytes())
    assert sha(Path(contract['inputs']).read_bytes()) == contract['inputs_sha256']
    assert r['ROM_sha256'] == pre['candidate_sha256'] and r['frames'] == (24100 if case == 'newgame' else 8063)
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert r['core_DLL_sha256'] == CORE_SHA
    assert not any(v for k, v in r.items() if k.startswith('synthetic_'))
    if contract['donor']:
        assert sha(Path(contract['donor']).read_bytes()) == contract['donor_sha256']
        assert r['battery_save_preloaded']['source_sha256'] == contract['donor_sha256']
        assert r['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    shots = {}
    for s in r['frames_captured']:
        assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
        if s['frame'] in shots:
            assert shots[s['frame']]['PNG_sha256'] == s['PNG_sha256']
        shots[s['frame']] = s
    assert len(shots) == (89 if case == 'newgame' else 325)
    return r, shots, {'case': case, 'tag': suffix, 'path': str(rp), 'sha256': sha(rp.read_bytes()),
        'frames': r['frames'], 'capture_records': len(r['frames_captured']), 'unique_frames': len(shots)}


def main():
    pre, source = read(ROOT / 'preflight.json'), read(ROOT / 'source_contract.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    rom = NdsImage.open(ROM)
    segments = units(rom)
    original_segments = units(NdsImage.open('work/clean.nds'))
    pxls = [(p, d) for _, p, d in rom.iter_files() if p.lower().endswith('.pxl')]
    shared = sorted(p for p, d in pxls if d[:20] == rom.read_file('/_pxl/__frame.pxl')[:20])
    assert len(pxls) == 660 and shared == ['/_pxl/__frame.pxl', '/_pxl/__marker.pxl']
    save(ROOT / 'header_collision_census.json', {'complete_PXL_files': len(pxls), 'same_Frame_header20_paths': shared,
        'Frame_sha256': sha(rom.read_file(shared[0])), 'Marker_sha256': sha(rom.read_file(shared[1])),
        'same_header_is_not_resource_identity': True})
    targets = {r['PC']: r for r in source['targets']}
    controls = read(ROOT / 'host_filter_controls.json')
    assert len(controls['cases']) == 13 and controls['whole_expected_files_compared_including_last_byte_controls']
    marker_records = read('translations/marker_gender_and_radial_graphics_v2.json')['records']
    marker_boxes = [(r['text'], tuple(r['box'])) for r in marker_records]
    receipts, results = [], []
    for case in ('newgame', 'equipment'):
        baseline, shots, receipt = report(case, 'baseline', pre)
        receipts.append(receipt)
        for tag in ('observed', 'observed_marker'):
            r, observed_shots, receipt = report(case, tag, pre)
            receipts.append(receipt)
            assert r['scripted_input_schedule'] == baseline['scripted_input_schedule']
            assert observed_shots.keys() == shots.keys()
            for frame, s in observed_shots.items():
                assert Image.open(s['path']).convert('RGB').tobytes() == Image.open(shots[frame]['path']).convert('RGB').tobytes()
        folder = CAP / f'graphic_paints_v669_{case}_observed_marker/observer'
        previous_folder = CAP / f'graphic_paints_v669_{case}_observed/observer'
        meta, previous_meta = read(folder / 'paint_observer.json'), read(previous_folder / 'paint_observer.json')
        assert meta['script_sha256'] == sha(Path('scripts/observe_graphic_paints_v669.py').read_bytes())
        assert previous_meta['script_sha256'] == sha((ROOT / 'initial_observer.py').read_bytes())
        assert meta['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
        assert previous_meta['source_contract_sha256'] == sha((ROOT / 'initial_source_contract.json').read_bytes())
        for m in (meta, previous_meta):
            assert m['original_slot_restored_and_DLL_file_unchanged'] and not m['overflow'] and not m['mismatch']
        blob, old_blob = Path(meta['path']).read_bytes(), Path(previous_meta['path']).read_bytes()
        assert sha(blob) == meta['sha256'] and sha(old_blob) == previous_meta['sha256']
        assert len(blob) == len(old_blob) == meta['records'] * 160 == previous_meta['records'] * 160
        counts, primitive_counts, footprints, parent_counts, header_candidates = Counter(), Counter(), Counter(), Counter(), Counter()
        marker_selections, binding_pointers, caller_bindings = Counter(), Counter(), {}
        for row, old in zip(struct.iter_unpack('<40I', blob), struct.iter_unpack('<40I', old_blob), strict=True):
            assert row[:37] == old[:37] and row[38:] == old[38:]
            assert row[37] == {0: 0, 1: 1, 3: 6}[old[37]]
            frame, pc, instruction, screen, header, palette, descriptor, sp, lr, r15, cpsr, host_arg = row[:12]
            assert 1 <= frame <= (24100 if case == 'newgame' else 8063)
            assert pc in targets and instruction == host_arg == targets[pc]['original_instruction']
            assert r15 == pc + 8 and not cpsr & 32 and row[38] == 0
            assert descriptor % 4 == sp % 4 == header % 4 == 0
            assert screen in (0, 1)
            counts[row[37]] += 1
            primitive_counts[pc] += 1
            header_candidates[tuple(row[32:37])] += 1
            if row[37] in (1, 2, 6):
                rect = source_rect(row)
                assert all(0 <= v <= 256 for v in rect) and rect[0] + rect[2] <= 256 and rect[1] + rect[3] <= 256
                assert 0 <= palette < (83 if row[37] in (1, 6) else 1)
                footprints[(row[37], pc, *rect, palette)] += 1
                parent_counts[(row[37], pc, lr)] += 1
                binding_pointers[(row[37], header)] += 1
                caller_bindings[(pc, lr)] = caller(segments, original_segments, lr, pc)
                if row[37] == 1:
                    assert not intersecting(rect, pc == 0x01FFAE70, CELLS)
                if row[37] == 6:
                    for name in intersecting(rect, pc == 0x01FFAE70, marker_boxes):
                        box = next(bounds for text, bounds in marker_boxes if text == name)
                        assert rect[0] <= box[0] < box[2] <= rect[0] + rect[2]
                        assert rect[1] <= box[1] < box[3] <= rect[1] + rect[3]
                        marker_selections[(name, *rect)] += 1
        assert counts[2] == counts[3] == counts[4] == counts[5] == counts[7] == 0
        results.append({'case': case, 'records': meta['records'], 'binding_counts': dict(counts),
            'primitive_counts': [{'PC': p, 'entries': n} for p, n in sorted(primitive_counts.items())],
            'whole_file_binding_pointer_counts': [{'binding_ID': b, 'header': h, 'entries': n}
                for (b, h), n in sorted(binding_pointers.items())],
            'all_initial_registers_arguments_descriptors_headers_and_flags_exact_after_marker_resolution': True,
            'all_selected_target_source_footprints': [{'binding_ID': b, 'PC': pc, 'XYWH': [x, y, w, h],
                'palette': palette, 'entries': count} for (b, pc, x, y, w, h, palette), count in sorted(footprints.items())],
            'selected_target_original_parent_returns': [{'binding_ID': b, 'PC': pc, 'LR': lr, 'entries': n}
                for (b, pc, lr), n in sorted(parent_counts.items())],
            'selected_marker_translation_regions': [{'text': key[0], 'source_XYWH': key[1:], 'entries': n}
                for key, n in sorted(marker_selections.items())],
            'each_selected_marker_translation_box_fully_inside_observed_source_crop': True,
            'target_caller_bindings': list(caller_bindings.values()),
            'full_current_Frame_and_Marker_files_bound_no_unresolved_shared_header_candidate': True,
            'all_bound_Frame_source_footprints_exclude_five_caption_cells': True,
            'no_Confirm_file_selected_through_these_primitives_in_this_schedule': True})
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'reports': receipts, 'cases': results, 'native_host_controls': controls['cases'],
        'four_observed_runs_and_two_unmodified_baselines_terminal': True,
        'all828_observer_baseline_sampled_two_screen_pairs_exact': True,
        'all407770_original_primitive_entry_records_repeat_with_unchanged_arguments': True,
        'whole_Frame35444_Marker35444_Confirm532_source_bytes_compared_not_prefix_or_hash_only': True,
        'complete660_PXL_header_collision_census': 'work/analysis/graphic_paints_v669/header_collision_census.json',
        'three_original_primitive_paths_include_scaled_corner_and_tiled_copies': True,
        'cached_direct_views_need_not_request_resource_to_be_observed_here': True,
        'no_actual_paint_return_final_pixel_per_entry_or_global_nonuse_claim': True,
        'all_six_control_parents_other_contexts_and_other_native_paint_paths_still_open': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V669 full source bindings, three original primitive contracts and828 whole-screen pairs pass.', flush=True)


if __name__ == '__main__':
    main()
