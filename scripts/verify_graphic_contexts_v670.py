"""Verify wider ordinary/fixture UI source selections without global non-use claims."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_port_consistency import transform
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_graphic_paints_v669 import units
from scripts.prepare_graphic_contexts_v670 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_frame_style_tiles_v584 import CELLS
from scripts.verify_graphic_paints_v669 import caller, intersecting, source_rect
from scripts.verify_village_wrap_v608 import read, save


def load(case, baseline, config, pre):
    tag = 'baseline' if baseline else 'observed'
    folder = CAP / f'graphic_contexts_v670_{case}_{tag}'
    rp = folder / 'capture_report.json'
    r, contract = read(rp), read(folder / 'run_contract.json')
    assert contract['runner_sha256'] == sha(Path('scripts/run_graphic_contexts_v670.py').read_bytes())
    assert contract['config'] == config
    assert r['ROM_sha256'] == pre['candidate_sha256'] and r['frames'] == config['frames']
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert r['core_DLL_sha256'] == CORE_SHA
    assert r['battery_save_preloaded']['source_sha256'] == config['donor_sha256']
    assert r['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert r['scripted_input_schedule'] == read(config['inputs'])
    expected_synthetic = {'synthetic_gallery_fixtures'} if case == 'race' else set()
    assert {k for k, v in r.items() if k.startswith('synthetic_') and v} == expected_synthetic
    shots = {}
    for shot in r['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        if shot['frame'] in shots:
            assert shots[shot['frame']]['PNG_sha256'] == shot['PNG_sha256']
        shots[shot['frame']] = shot
    events = read(folder / 'fixture_events.json')
    assert events['final_frame'] == config['frames']
    assert not events['wireless_or_race_outcome_verified']
    if case == 'crew':
        assert events['events'] == []
    else:
        assert len(events['events']) == 201
        fields = {(0x0237BBC0 + i * 512, 212) for i in range(4)} | {(0x0237D9F0, 2)}
        assert set(events['originals']) == {hex(a) for a, n in fields}
        for index, row in enumerate(events['events']):
            assert row['before_frame'] == 4401 + index
            assert row['only_declared_ring_payloads_and_readiness_halfword_changed']
            assert {(r['address'], r['bytes']) for r in row['writes']} == fields
        restored = events['events'][-1]['writes']
        assert all(q['after_sha256'] == sha(bytes.fromhex(events['originals'][hex(q['address'])])) for q in restored)
    return r, shots, events, {'case': case, 'tag': tag, 'path': str(rp), 'sha256': sha(rp.read_bytes()),
        'frames': r['frames'], 'capture_records': len(r['frames_captured']), 'unique_frames': len(shots)}


def main():
    pre = read(ROOT / 'preflight.json')
    configs = read(ROOT / 'run_cases.json')['cases']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    assert sha(Path(pre['observer_source']).read_bytes()) == pre['observer_source_sha256']
    assert sha(Path(pre['observer_contract']).read_bytes()) == pre['observer_contract_sha256']
    contracts = read(pre['observer_contract'])
    assert pre['candidate_sha256'] == read('work/analysis/graphic_paints_v669/proof.json')['candidate_sha256']
    current_arm = NdsImage.open(pre['candidate']).read_file('/__arm9__.bin')
    previous_arm = NdsImage.open('out/all_routes_combined_v653_candidate.nds').read_file('/__arm9__.bin')
    assert current_arm == transform(previous_arm)[0]
    targets = {r['PC']: r for r in contracts['targets']}
    segments, originals = units(NdsImage.open(pre['candidate'])), units(NdsImage.open('work/clean.nds'))
    cases, receipts, baseline_pairs, retained_pairs = [], [], 0, 0
    for case, config in configs.items():
        assert sha(Path(config['donor']).read_bytes()) == config['donor_sha256']
        observed, shots, events, receipt = load(case, False, config, pre)
        receipts.append(receipt)
        base, base_shots, base_events, receipt = load(case, True, config, pre)
        receipts.append(receipt)
        assert observed['scripted_input_schedule'] == base['scripted_input_schedule']
        assert shots.keys() == base_shots.keys() and events == base_events
        for frame, shot in shots.items():
            assert Image.open(shot['path']).convert('RGB').tobytes() == Image.open(base_shots[frame]['path']).convert('RGB').tobytes()
            baseline_pairs += 1
        old_path = Path(config['previous_report'])
        assert sha(old_path.read_bytes()) == config['previous_report_sha256']
        old = read(old_path)
        old_shots = {s['frame']: s for s in old['frames_captured']}
        assert old_shots.keys() == shots.keys()
        for frame, shot in old_shots.items():
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            assert Image.open(shot['path']).convert('RGB').tobytes() == Image.open(shots[frame]['path']).convert('RGB').tobytes()
            retained_pairs += 1
        folder = CAP / f'graphic_contexts_v670_{case}_observed/observer'
        meta = read(folder / 'paint_observer.json')
        assert meta['script_sha256'] == pre['observer_source_sha256']
        assert meta['source_contract_sha256'] == pre['observer_contract_sha256']
        assert meta['original_slot_restored_and_DLL_file_unchanged'] and not meta['overflow'] and not meta['mismatch']
        data = Path(meta['path']).read_bytes()
        assert sha(data) == meta['sha256'] and len(data) == meta['records'] * 160
        counts, primitives, footprints, parents = Counter(), Counter(), Counter(), Counter()
        bindings = {}
        for row in struct.iter_unpack('<40I', data):
            frame, pc, instruction, screen, header, palette, descriptor, sp, lr, r15, cpsr, host_arg = row[:12]
            assert 1 <= frame <= config['frames'] and pc in targets
            assert instruction == host_arg == targets[pc]['original_instruction']
            assert r15 == pc + 8 and not cpsr & 32 and row[38] == 0
            assert screen in (0, 1) and header % 4 == descriptor % 4 == sp % 4 == 0
            counts[row[37]] += 1
            primitives[pc] += 1
            if row[37] in (1, 2, 6):
                rect = source_rect(row)
                assert all(0 <= q <= 256 for q in rect)
                assert rect[0] + rect[2] <= 256 and rect[1] + rect[3] <= 256
                assert 0 <= palette < (83 if row[37] != 2 else 1)
                footprints[(row[37], pc, *rect, palette)] += 1
                parents[(row[37], pc, lr)] += 1
                bindings[(pc, lr)] = caller(segments, originals, lr, pc)
                if row[37] == 1:
                    assert not intersecting(rect, pc == 0x01FFAE70, CELLS)
        assert all(counts[k] == 0 for k in (2, 3, 4, 5, 7))
        cases.append({'case': case, 'records': meta['records'], 'binding_counts': dict(counts),
            'primitive_counts': [{'PC': p, 'entries': n} for p, n in sorted(primitives.items())],
            'selected_target_source_footprints': [{'binding_ID': b, 'PC': p, 'XYWH': [x, y, w, h],
                'palette': pal, 'entries': n} for (b, p, x, y, w, h, pal), n in sorted(footprints.items())],
            'original_target_parent_returns': [{'binding_ID': b, 'PC': p, 'LR': lr, 'entries': n}
                for (b, p, lr), n in sorted(parents.items())], 'caller_bindings': list(bindings.values()),
            'all_Frame_footprints_exclude_five_miniature_cells': True,
            'Confirm_not_selected_through_these_primitives_in_this_schedule': True,
            'no_unresolved_shared_header_file_candidate': True,
            'UI_fixture_scope': 'ordinary crew inputs' if case == 'crew' else 'local receive-ring and readiness fixture, no wireless/outcome credit'})
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'reports': receipts, 'cases': cases, 'observer_baseline_whole_two_screen_pairs': baseline_pairs,
        'retained_V657_V661_whole_two_screen_pairs': retained_pairs,
        'all_original_fixture_events_exact_between_observed_and_baseline_and_restored': True,
        'four_runs_terminal_no_savestate': True, 'primitive_entries': sum(c['records'] for c in cases),
        'race_is_disclosed_local_UI_fixture_not_wireless_or_race_completion': True,
        'whole_Frame_and_Marker_files_bound_with_original_primitive_inputs': True,
        'no_individual_paint_retirement_or_full_pixel_per_entry_credit_from_trace': True,
        'six_controls_other_contexts_primitives_and_full_graphics_goal_still_open': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V670 ordinary crew and fixture roster: full source bindings, baseline/retained frames and fixture restoration pass.', flush=True)


if __name__ == '__main__':
    main()
