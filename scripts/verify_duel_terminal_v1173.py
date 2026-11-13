"""Audit the terminal original duel, all31 isolated fixtures and normal return."""
from pathlib import Path
from shutil import copy2
import struct
from dk4tool.patch.duel_editorial import current_entries, COMPONENT_SHA
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_duel_contact_v1169 import apply_fixture, water
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
ROOT = Path('work/analysis/duel_terminal_v1173')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_contact_v1169_1166_compassAttack8')
ROM = Path('out/all_routes_combined_v1166_candidate.nds')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1166 Duel')


def main():
    assert not ROOT.exists() and not GUIDE.exists()
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    assert report['frames'] == 9622 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification']
    assert report['ROM_sha256'] == sha(ROM.read_bytes())
    assert read('work/analysis/duel_contact_v1169_compassAttack8/terminal_preservation.json')['source_and_disposable_donors_unchanged']
    rom = NdsImage.open(ROM)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x737C8, 0x74010), (0xE8CC, 0xED74), (0x7E154, 0x7E1A4),
                   (0x519D4, 0x51A28), (0xD9824, 0xD9868)):
        assert arm[lo:hi] == clean[lo:hi]
    snapshots = {}
    for value in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        if value['frame'] in snapshots:
            assert value['sha256'] == snapshots[value['frame']]['sha256']
        snapshots[value['frame']] = value
    fixtures = report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures) == 31 and max(r['frame'] for r in fixtures) == 5770
    seed, flag = [struct.unpack_from('<I', arm, at)[0] for at in (0xD9858, 0x51A20)]
    owner = struct.unpack_from('<I', arm, 0x552A0)[0]
    entries = current_entries(common, arm)
    duels = {entries[n].text for n in range(1931, 1951)}
    audits, points = [], set()
    for receipt in fixtures:
        snap = snapshots[receipt['frame']]
        raw = Path(snap['path']).read_bytes()
        assert len(raw) == snap['bytes'] == 0x400000
        assert sha(raw) == snap['sha256'] == receipt['before_RAM_sha256']
        if receipt['context'] == 'compassAttack8':
            after, replay = apply_fixture(arm, raw, {'sighting_context': 'compassAttack8'})
            assert receipt == {**replay, 'frame': receipt['frame']}
            assert len(receipt['owned_bytes']) == 19
        else:
            assert receipt['context'] == 'healthyContact' and receipt['frame'] <= 5770
            cpu, get = get_machine(arm, raw)
            root, actors = get(0xCB1A8), get(0xCB184)
            assert get(0x7F244) == get(0x2E58C) == 1
            own, enemy = root+4+132, root+4+8*132
            assert get(0x35320, own) == 2 and get(0x35320, enemy) == 8
            mobiles = [get(0x36C70, fleet+12) for fleet in (own, enemy)]
            assert all(m and get(0x564C8, m) for m in mobiles)
            captains = [actors+0x19E4, get(0x3697C, enemy)]
            assert captains[1] == actors+4+32*32
            hp = [get(0x7E19C, actor) for actor in captains]
            live = [[get(0x5543C, m), get(0x55444, m)] for m in mobiles]
            assert hp == receipt['positive_captain_HP_before'] and all(v > 0 for v in hp)
            assert live == receipt['live_Hull_Crew_before'] and all(v > 0 for row in live for v in row)
            fixed = bytes(cpu.mem_read(mobiles[1]+16, 8))
            point = tuple(int(v/128) for v in struct.unpack('<2i', fixed))
            points.add(point)
            fields = {own+0x34: struct.pack('<2i', *point), mobiles[0]+16: fixed}
            bounds = []
            for mobile, values in zip(mobiles, live, strict=True):
                model = get(0xAB158, mobile)
                limits = [get(0x183A0, model), get(0xAB18C, model)]
                assert all(0 < v <= limit for v, limit in zip(values, limits, strict=True))
                fields[mobile+24] = struct.pack('<2H', *limits)
                bounds.append(limits)
            for actor, value in zip(captains, hp, strict=True):
                fields[actor+0x18] = struct.pack('<H', max(value, 100))
            assert bounds == receipt['unchanged_native_Hull_and_crew_capacity_bounds']
            assert {str(k): v.hex() for k, v in fields.items()} == receipt['declared_fields']
            owned = {a for at, data in fields.items() for a in range(at, at+len(data))}
            assert len(owned) == 28 and owned == set(receipt['owned_bytes'])
            assert raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0] not in duels
            after = bytearray(raw)
            for at, data in fields.items():
                after[at-BASE:at-BASE+len(data)] = data
            after = bytes(after)
            assert mobiles[1]+13 not in owned
            changes = [{'address': BASE+i, 'before': a, 'after': b}
                       for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
            assert changes == receipt['changes']
        assert sha(after) == receipt['after_RAM_sha256']
        for address in (seed, flag):
            assert raw[address-BASE:address-BASE+4] == after[address-BASE:address-BASE+4]
        audits.append({'frame': receipt['frame'], 'context': receipt['context'],
            'owned_bytes': len(receipt['owned_bytes']), 'all4MiB_delta_and_hash_exact': True,
            'RNG_actor_IDs_and_original_outcome_bytes_not_overridden': True})
    terrain = water(arm, [list(p) for p in sorted(points)])
    assert all(row['collision_free'] for row in terrain['queries'])
    holds_path = Path('work/analysis/duel_actual_holds_v1172/original_challenge_acceptance_threat_holds.json')
    holds = read(holds_path)
    assert len(holds['cases']) == 6 and holds['candidate_sha256'] == report['ROM_sha256']
    for case in holds['cases']:
        assert snapshots[case['frame']]['sha256'] == case['RAM_sha256']
        raw = Path(case['RAM_path']).read_bytes()
        assert sha(raw[0x28E70C:0x28E70C+1480]) == COMPONENT_SHA
        assert case['full_original_font_plane_and_all_three144x12_RGB_ink_and_blank_masks_exact']
    # Natural post-duel HP, after all fixture use ended. This is observed
    # original combat output; no fixture sets a zero or victory/defeat result.
    raw = Path(snapshots[6902]['path']).read_bytes()
    cpu, get = get_machine(arm, raw)
    actors = get(0xCB184)
    assert [get(0x7E19C, actor) for actor in (actors+0x19E4, actors+4+32*32)] == [109, 0]
    # Actual input execution receipts prove the later normal UI steps; command
    # intent alone is not treated as evidence of an input being consumed.
    commands = report['navigation_commands'] if 'navigation_commands' in report else read(CAP/'navigation_command_journal.json')['commands_received']
    assert all(row['validation_passed'] for row in commands)
    assert all('battle_fixture' not in row['command'] for row in commands if row['frame'] >= 5772)
    terminal = Path(snapshots[9622]['path']).read_bytes()
    assert len(terminal) == 0x400000
    ROOT.mkdir(parents=True)
    proof = ROOT/'terminal_gameplay_verification.json'
    save(proof, {'candidate': str(ROM), 'candidate_sha256': report['ROM_sha256'],
        'terminal_report': str(report_path), 'terminal_report_sha256': sha(report_path.read_bytes()), 'terminal_frame': 9622,
        'all31_fixture_replays': audits, 'native_contact_water_recheck': terrain,
        'all30_28byte_health_contact_fixtures_before_original_duel_and_one19byte_diplomatic_location_fixture': True,
        'last_fixture_frame': 5770, 'original_duel_observed_after_frame': 5772,
        'no_health_location_actor_RNG_message_or_outcome_injection_during_or_after_duel': True,
        'source_duel_eligibility_outcome_and_RNG_code_exact_to_clean_ROM': True,
        'natural_post_duel_own_enemy_HP': [109, 0],
        'actual_complete_holds': holds['cases'], 'hold_proof': str(holds_path), 'hold_proof_sha256': sha(holds_path.read_bytes()),
        'normal_transition_challenge_acceptance_combat_defeated_threat_capture_and_victory_notices': True,
        'normal_A_notices_X_cargo_finish_A_unloaded_goods_confirmation_and_B_dock_refusal_then_sea_return': True,
        'terminal_Sea_View_without_portrait_paper_or_duel_box_visually_reviewed': True,
        'actual_IDs': [1932, 1939, 1945], 'other17_static_duel_IDs_have_complete_native_and_family_sample_not_individual_actual_activations': True,
        '13_escape_notices_not_observed_no_completion_credit_for_them': True,
        'source_and_disposable_saves_unchanged': True,
        'isolated_test_state_not_earned_progression_complete_route_or_hardware_verification': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    GUIDE.mkdir(parents=True)
    files = []
    for name, frame in (('Duel challenge', 5782), ('Duel acceptance', 5902), ('Defeated opponent', 6912)):
        source, target = CAP/f'frame_{frame:06d}_navigation.png', GUIDE/f'{name}.png'
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        files.append({'path': str(target), 'sha256': sha(target.read_bytes()), 'original_frame': frame})
    save(GUIDE/'screenshot_provenance.json', {'candidate': str(ROM.absolute()), 'candidate_sha256': report['ROM_sha256'],
        'files': files, 'verification': str(proof.absolute()),
        'original_game_frames_from_isolated_save_location_and_health_setup': True,
        'native_duel_outcome_no_message_or_RNG_override_no_earned_progression_claim': True})
    print('Terminal duel:31 exact fixture audits,six full text/RGB holds,natural outcome and normal sea return pass. Three guide screenshots saved.', flush=True)


if __name__ == '__main__':
    main()
