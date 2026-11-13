"""Bind the five-ship encounter, original loss/recovery and unresolved UI findings."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_full_fleet_proximity_v652 import apply_fixture
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.search_miniature_captures_v577 import scan_image, template
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/full_fleet_battle_v652')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def load(label, frames, digest):
    path = CAP / label / 'capture_report.json'
    report = read(path)
    assert report['frames'] == frames and report['ROM_sha256'] == digest
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    for row in report.get('read_only_capture_RAM_snapshots', []) + report.get('read_only_pause_RAM_snapshots', []):
        assert row['read_only_export'] and sha(Path(row['path']).read_bytes()) == row['sha256']
    return report, {'path': str(path), 'sha256': sha(path.read_bytes())}


def fleet_models(arm, raw, fleet_index):
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(offset, args=()):
        call(u, offset, args)
        return u.reg_read(UC_ARM_REG_R0)

    assert get(0x2E58C) == 1
    fleet = get(0xCB1A8) + 4 + fleet_index * 0x84
    result = []
    for slot in range(5):
        reference = fleet + 12 + slot * 8
        model, mobile = get(0x36C94, (reference,)), get(0x36C70, (reference,))
        if model:
            assert BASE <= model < BASE + len(raw) - 140
            if mobile:
                assert struct.unpack('<I', u.mem_read(mobile, 4))[0] == 0x02143A80
            result.append({'slot': slot, 'model': model,
                           'name': bytes(u.mem_read(model + 8, 24)).split(b'\0')[0].decode('ascii'),
                           'canonical_Hull_Crew': [get(0x183A0, (model,)), get(0x181BC, (model,))],
                           'mobile': mobile,
                           'live_Hull_Crew': [get(0x5543C, (mobile,)), get(0x55444, (mobile,))] if mobile else None})
    return result


def main():
    pre, staffing = read(ROOT / 'preflight.json'), read(ROOT / 'staffing_proof.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom = NdsImage.open(pre['candidate'])
    arm = rom.read_file('/__arm9__.bin')
    reports, receipts = {}, []
    for label, frames in (('full_fleet_staffing_v652_actual', 19600),
                          ('full_fleet_battle_v652_actual', 6000),
                          ('full_fleet_battle_v652_near_target', 23600),
                          ('full_fleet_loss_reload_v652', 3200)):
        reports[label], receipt = load(label, frames, pre['candidate_sha256'])
        receipts.append(receipt)
    actual = reports['full_fleet_battle_v652_near_target']
    assert actual['battery_save_preloaded']['source_sha256'] == staffing['prepared_save']['sha256']
    assert sha(Path(staffing['prepared_save']['path']).read_bytes()) == staffing['prepared_save']['sha256']
    for label, report in reports.items():
        if label != 'full_fleet_battle_v652_near_target':
            assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    snapshots = {r['frame']: r for r in actual['read_only_pause_RAM_snapshots']}
    fixtures = actual['synthetic_battle_recovery_proximity_fixtures']
    assert [(f['frame'], f['action']) for f in fixtures] == [(4800, 'approach'), (5200, 'approach')]
    for fixture in fixtures:
        raw = Path(snapshots[fixture['frame']]['path']).read_bytes()
        after, expected = apply_fixture(arm, raw, fixture['action'])
        assert {k: v for k, v in fixture.items() if k != 'frame'} == expected
        assert sha(after) == fixture['after_RAM_sha256']
        assert len(fixture['owned_bytes']) == 8 and len(fixture['changes']) == 4
        assert all(c['address'] in range(fixture['active_mobile_ship'] + 16,
                                        fixture['active_mobile_ship'] + 24) for c in fixture['changes'])
        assert fixture['persisted_named_model_remains_entirely_unchanged']
        assert fixture['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
    assert fixtures[0]['offscreen_saved_target']['persisted_Hull_Crew'] == [30, 13]
    assert fixtures[0]['enemy_mobile_ship_unchanged'] == 0
    assert fixtures[1]['enemy_mobile_ship_unchanged'] != 0
    states = []
    for frame in (4800, 5200, 13200, 14400, 16000, 23600):
        raw = Path(snapshots[frame]['path']).read_bytes()
        own, enemy = fleet_models(arm, raw, 1), fleet_models(arm, raw, 5)
        if frame <= 14400:
            assert len(own) == 5 and own[0]['name'] == 'Vestaros'
            assert [s['live_Hull_Crew'] for s in own[1:]] == [[25, 19]] * 4
        else:
            assert len(own) == 4 and all(s['name'] == 'Latina' and s['canonical_Hull_Crew'] == [25, 19] for s in own)
        if frame == 13200:
            assert own[0]['live_Hull_Crew'] == [60, 43] and len(enemy) == 3
        if frame == 14400:
            assert own[0]['live_Hull_Crew'] == [60, 0]
        states.append({'frame': frame, 'own_fleet': own, 'Speyer_fleet': enemy,
                       'RAM_sha256': snapshots[frame]['sha256']})
    reload = reports['full_fleet_loss_reload_v652']
    reload_raw = Path(reload['read_only_capture_RAM_snapshots'][0]['path']).read_bytes()
    reloaded_ships = fleet_models(arm, reload_raw, 1)
    assert len(reloaded_ships) == 4 and all(s['name'] == 'Latina' for s in reloaded_ships)
    source_save = Path(actual['battery_save_preloaded']['destination'])
    assert reload['battery_save_preloaded']['source_sha256'] == sha(source_save.read_bytes())
    pxl = PxlImage.from_bytes(rom.read_file('/_pxl/__frame.pxl'))
    batch = read('translations/frame_action_buttons_graphics_v7.json')
    templates = {r['text']: template(pxl, r['box']) for r in batch['records'][15:] if r['text'] not in ('M', 'D')}
    colors = set()
    for bank in range((pxl.pixels_offset - 20) // 32):
        w = struct.unpack_from('<H', pxl.source, 20 + bank * 32 + 18)[0]
        colors.add((w & 31, w >> 5 & 31, w >> 10 & 31))
    scans = []
    for label, report in reports.items():
        for shot in report['frames_captured']:
            scans.append({'run': label, 'frame': shot['frame'], 'path': shot['path'],
                          'PNG_sha256': shot['PNG_sha256'], 'matches': scan_image(shot['path'], templates, colors)})
    save(ROOT / 'near_target_inputs.json', actual['scripted_input_schedule'])
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'reports': receipts, 'all_four_runs_terminal': True,
        'ordinary_staffing_and_repair_proof_sha256': sha((ROOT / 'staffing_proof.json').read_bytes()),
        'ordinary125_crew_and_source60_49_named_ship_before_proximity': True,
        'coordinate_only_fixture_frames': [4800, 5200], 'actual_changed_coordinate_bytes_each': [4, 4],
        'no_recovery_enemy_fleet_or_battle_outcome_fixture': True,
        'original_visibility_constructs_Speyer_mobile_ship_after_approach': True,
        'original_fleet_getter_states': states,
        'actual_duel_and_first_ship_crew43_to0_loss_and_four_ship_Oslo_recovery': True,
        'victory_full_fleet_rewards_or_captured_ship_selection_not_reached': True,
        'post_loss_four_ship_save_cold_reload': {'path': str(source_save), 'sha256': sha(source_save.read_bytes()),
                                                'original_models': reloaded_ships},
        'five_miniature_complete_mask_search': scans,
        'miniature_mask_match_count': sum(len(s['matches']) for s in scans),
        'not_global_non_use_or_Confirm_parent_proof': True,
        'new_visible_wrapping_families': read(ROOT / 'new_graphics_followups.json'),
        'shared_role_portrait_renderer_repair_pending': True,
        'all18_plaques_incomplete_22_historical_scopes_exact': True,
        'ROM_patch_registry_and_release_pointers_unchanged': True, 'full_goal_complete': False,
        'scripts': {p: sha(Path(p).read_bytes()) for p in (
            'scripts/run_full_fleet_staffing_v652.py', 'scripts/verify_full_fleet_staffing_v652.py',
            'scripts/run_full_fleet_battle_v652.py', 'scripts/native_full_fleet_fixture_v652.py',
            'scripts/run_full_fleet_near_target_v652.py', 'scripts/native_full_fleet_proximity_v652.py',
            'scripts/verify_full_fleet_battle_v652.py')}}
    save(ROOT / 'battle_proof.json', proof)
    print(f'V652:four terminal runs;original5-to4 ship loss/recovery;{len(scans)}captures/{proof["miniature_mask_match_count"]}miniature leads;three wrapping families open.')


if __name__ == '__main__':
    main()
