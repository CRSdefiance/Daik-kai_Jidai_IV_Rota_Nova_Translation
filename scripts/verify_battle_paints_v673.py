"""Bind actual encounter/result image inputs to baseline pixels and native state."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_graphic_paints_v669 import units
from scripts.native_battle_proximity_v673 import apply_fixture
from scripts.prepare_battle_paints_v673 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_frame_style_tiles_v584 import CELLS
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_graphic_paints_v669 import caller, intersecting, source_rect
from scripts.verify_village_wrap_v608 import read, save


def report(tag, pre, arm):
    folder = CAP / f'battle_paints_v673_{tag}'
    path = folder / 'capture_report.json'
    r = read(path)
    assert r['ROM_sha256'] == pre['candidate_sha256'] and r['frames'] == 28400
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert r['core_DLL_sha256'] == CORE_SHA
    assert r['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
    assert r['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert {k for k, v in r.items() if k.startswith('synthetic_') and v} == {'synthetic_battle_recovery_proximity_fixtures'}
    contract = read(folder / 'run_contract.json')
    assert contract['runner_sha256'] == sha(Path('scripts/run_battle_paints_v673.py').read_bytes())
    assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
    commands = read(folder / 'navigation_command_journal.json')['commands_received']
    assert all(row['validation_passed'] for row in commands)
    assert [row['command'] for row in commands] == read(pre['commands'])
    fixtures = r['synthetic_battle_recovery_proximity_fixtures']
    assert [(f['frame'], f['action']) for f in fixtures] == [(4800, 'approach'), (5200, 'approach')]
    retained = read(folder / 'fixture_receipts.json')['fixtures']
    assert len(retained) == 2
    for fixture, export in zip(fixtures, retained, strict=True):
        raw = Path(export['before_RAM_path']).read_bytes()
        assert sha(raw) == export['before_RAM_sha256'] == fixture['before_RAM_sha256']
        after, replay = apply_fixture(arm, raw, 'approach')
        assert replay == {k: v for k, v in fixture.items() if k != 'frame'}
        assert export['receipt'] == fixture and sha(after) == export['after_RAM_sha256']
        assert len(fixture['owned_bytes']) == 8 and len(fixture['changes']) == 4
        assert fixture['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
        assert funds(arm, raw) == 25975
    shots = {}
    for shot in r['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        if shot['frame'] in shots:
            assert shots[shot['frame']]['PNG_sha256'] == shot['PNG_sha256']
        shots[shot['frame']] = shot
    assert len(shots) == 82 and len(r['frames_captured']) == 84
    final = (folder / 'final_arm9_ram.bin').read_bytes()
    assert len(final) == 0x400000 and funds(arm, final) == 30250
    ships = fleet_models(arm, final, 1)
    assert len(ships) == 5 and [s['name'] for s in ships] == ['Vestaros'] + ['Latina'] * 4
    assert [s['live_Hull_Crew'] for s in ships] == [[60, 43]] + [[25, 19]] * 4
    return r, shots, retained, {'tag': tag, 'path': str(path), 'sha256': sha(path.read_bytes()),
        'frames': r['frames'], 'capture_records': len(r['frames_captured']), 'unique_frames': len(shots),
        'final_RAM_sha256': sha(final), 'final_native_funds': 30250, 'original_surviving_ships': ships}


def same_pixels(a, b, label, frame):
    x, y = [Image.open(p).convert('RGB') for p in (a, b)]
    if x.tobytes() != y.tobytes():
        save(ROOT / 'first_pixel_difference.json', {'comparison': label, 'frame': frame,
            'a': str(a), 'b': str(b), 'bounds': ImageChops.difference(x, y).getbbox()})
        raise AssertionError((label, frame))


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    for key in ('observer', 'observer_contract', 'fixture_wrapper', 'original_commands', 'previous_report'):
        assert sha(Path(pre[key]).read_bytes()) == pre[key + '_sha256']
    assert read(pre['commands']) == [{k: v for k, v in row.items() if k != 'export_native_state'}
                                  for row in read(pre['original_commands'])]
    rom = NdsImage.open(pre['candidate'])
    arm = rom.read_file('/__arm9__.bin')
    observed, shots, fixtures, a = report('observed', pre, arm)
    baseline, base_shots, base_fixtures, b = report('baseline', pre, arm)
    assert observed['scripted_input_schedule'] == baseline['scripted_input_schedule']
    assert shots.keys() == base_shots.keys()
    assert observed['synthetic_battle_recovery_proximity_fixtures'] == baseline['synthetic_battle_recovery_proximity_fixtures']
    assert [r['before_RAM_sha256'] for r in fixtures] == [r['before_RAM_sha256'] for r in base_fixtures]
    previous = read(pre['previous_report'])
    previous_shots = {s['frame']: s for s in previous['frames_captured']}
    assert previous_shots.keys() == shots.keys()
    for frame, shot in shots.items():
        same_pixels(shot['path'], base_shots[frame]['path'], 'current_observed_baseline', frame)
        old = previous_shots[frame]
        assert sha(Path(old['path']).read_bytes()) == old['PNG_sha256']
        same_pixels(shot['path'], old['path'], 'retained_V654_victory', frame)
    folder = CAP / 'battle_paints_v673_observed/observer'
    meta = read(folder / 'paint_observer.json')
    assert meta['script_sha256'] == pre['observer_sha256']
    assert meta['source_contract_sha256'] == pre['observer_contract_sha256']
    assert meta['original_slot_restored_and_DLL_file_unchanged'] and not meta['overflow'] and not meta['mismatch']
    data = Path(meta['path']).read_bytes()
    assert sha(data) == meta['sha256'] and len(data) == meta['records'] * 160
    targets = {r['PC']: r for r in read(pre['observer_contract'])['targets']}
    segments, originals = units(rom), units(NdsImage.open('work/clean.nds'))
    counts, guards, primitives, footprints, parents = Counter(), Counter(), Counter(), Counter(), Counter()
    hits, bindings = [], {}
    for row in struct.iter_unpack('<40I', data):
        frame, pc = row[:2]
        assert 1 <= frame <= 28400 and pc in targets
        assert row[2] == row[11] == targets[pc]['original_instruction']
        assert row[9] == pc + 8 and not row[10] & 32
        counts[row[37]] += 1
        guards[row[38]] += 1
        primitives[pc] += 1
        if row[37] in (1, 2, 6):
            assert row[38] == 0 and row[3] in (0, 1)
            rect = source_rect(row)
            assert rect[0] + rect[2] <= 256 and rect[1] + rect[3] <= 256
            assert row[5] < (1 if row[37] == 2 else 83)
            footprints[(row[37], pc, *rect, row[5])] += 1
            parents[(row[37], pc, row[8])] += 1
            # Preserve translated/indirect caller uncertainty explicitly.
            try:
                bindings[pc, row[8]] = caller(segments, originals, row[8], pc)
            except AssertionError:
                bindings[pc, row[8]] = {'PC': pc, 'LR': row[8], 'original_clean_caller_not_verified': True}
            selected = intersecting(rect, pc == 0x01FFAE70, CELLS) if row[37] == 1 else []
            if selected or row[37] == 2:
                hits.append({'frame': frame, 'PC': pc, 'LR': row[8], 'binding_ID': row[37],
                    'source_XYWH': list(rect), 'palette': row[5], 'miniature_intersections': selected,
                    'entry_source_selection_not_finished_display': True})
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'reports': [a, b], 'all82_current_whole_two_screen_pairs_exact': True,
        'all82_retained_V654_whole_two_screen_pairs_exact': True,
        'two_coordinate_only_fixture_events_exact_and_replayed_each_run': True,
        'original_funds25975_to30250_and_five_survivors_verified_not_written_by_fixture': True,
        'records': meta['records'], 'binding_counts': dict(counts), 'guard_counts': dict(guards),
        'primitive_counts': dict(primitives), 'target_control_source_hits': hits,
        'selected_target_footprints': [{'binding_ID': q[0], 'PC': q[1], 'XYWH': list(q[2:6]),
            'palette': q[6], 'entries': n} for q, n in sorted(footprints.items())],
        'target_parents': [{'binding_ID': b, 'PC': p, 'LR': lr, 'entries': n}
                          for (b, p, lr), n in sorted(parents.items())],
        'caller_bindings': list(bindings.values()),
        'no_individual_paint_retirement_or_full_destination_pixels_inferred_from_entry_trace': True,
        'all_other_contexts_primitives_and_six_actual_control_displays_still_require_evidence': True,
        'all18_plaques_incomplete22_scopes_preserved_no_ROM_changes': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V673 battle/victory source evidence:', meta['records'], 'entries;', len(hits), 'target hits;82+82 full pairs pass.', flush=True)


if __name__ == '__main__':
    main()
