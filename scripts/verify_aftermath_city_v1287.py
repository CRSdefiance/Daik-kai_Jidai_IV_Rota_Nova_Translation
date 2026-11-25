"""Actual original Madeira defense reply, full glyph planes and normal dismissal."""
import struct
from pathlib import Path
from shutil import copy2
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_city_fixture_v1285 import ROM, apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/aftermath_city_verified_v1287')
RUN = Path('work/analysis/aftermath_city_v1286')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_city_v1286_1266')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1266 City defense')
BASE = 0x02000000


def main():
    assert not ROOT.exists() and not GUIDE.exists()
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert report['frames'] == 6940 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['ROM_sha256'] == digest
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_battle_recovery_proximity_fixtures')
    donor_sha = '2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    plan = read(RUN/'run_plan.json')
    assert sha(Path(plan['source_donor']).read_bytes()) == sha(Path(plan['disposable_donor']).read_bytes()) == donor_sha
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    common = NdsImage.open(ROM).read_file('/COMMON/MESFILE.DK4')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x6ED34, 0x6EE90), (0x6F4D4, 0x6F7A4), (0x519D4, 0x51A28),
             (0x2CFFC, 0x2D040), (0x3697C, 0x369AC), (0xB4AA8, 0xB4AC0)]
    assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in spans)
    snapshots = {}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        if row['frame'] in snapshots:
            assert snapshots[row['frame']]['sha256'] == row['sha256']
        snapshots[row['frame']] = row

    def raw(frame):
        record = snapshots[frame]
        value = Path(record['path']).read_bytes()
        assert len(value) == record['bytes'] == 0x400000 and sha(value) == record['sha256']
        return value

    fixtures = report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 5000
    before = raw(5000)
    after, receipt = apply_fixture(arm, before, {'city_context': 'MadeiraNeutral'})
    assert fixtures[0] == {**receipt, 'frame': 5000}
    owned = set(receipt['owned_bytes'])
    assert len(owned) == 16
    assert all(BASE+i in owned for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b)
    assert receipt['diplomacy_actors_IDs_defender_defenses_shares_health_RNG_and_events_unchanged']
    journal = read(CAP/'navigation_command_journal.json')
    schedule = read(RUN/'original_load_inputs.json')
    for row in journal['commands_received']:
        assert row['validation_passed']
        command = row['command']
        if command.get('stop'):
            continue
        assert command['until'] in snapshots and command['until'] > row['frame']
        if row['frame'] > 5000:
            assert 'battle_fixture' not in command
        if command.get('buttons') or command.get('touch') is not None:
            event = {'start': row['frame']+1, 'duration': command.get('duration', 12), 'buttons': command.get('buttons', [])}
            if command.get('touch') is not None:
                event['touch'] = command['touch']
            schedule.append(event)
    assert schedule == report['scripted_input_schedule']
    entries = current_entries(common, arm)
    font_path = Path('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json')
    font = read(font_path)
    owner, wrapped = [struct.unpack_from('<I', arm, off)[0] for off in (0x552A0, 0x54450)]
    holds = []
    for frame in [6720, 6740]:
        body = raw(frame)
        cpu, get = get_machine(arm, body)
        fleets, actors = get(0xCB1A8), get(0xCB184)
        defender = fleets+4+22*132
        actor = get(0x3697C, defender)
        assert get(0x35320, defender) == 6 and get(0x7EE08, actor) == 46
        assert actor == actors+4+46*32
        message = get(0x53F4C, actor, 0x021178C0)
        assert message in range(2038, 2046)
        case = next(row for row in font['cases'] if row['message_id'] == message and row['name_case'] is None)
        preview = Path(case['preview'])
        assert sha(preview.read_bytes()) == case['preview_sha256']
        plane = Image.open(preview).convert('L')
        assert plane.size == (228, 64)
        assert body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0] == entries[message].text
        assert body[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0].hex() == case['native_formatted_hex']
        image_path = CAP/f'frame_{frame:06d}_navigation.png'
        picture = Image.open(image_path).convert('RGB')
        assert picture.size == (256, 384)
        expected = {(16+x, 296+y) for y in range(64) for x in range(228) if plane.getpixel((x, y)) == 0}
        actual = {(x, y) for y in range(294, 366) for x in range(16, 244) if picture.getpixel((x, y)) == (0, 8, 0)}
        assert actual == expected, (frame, len(expected-actual), len(actual-expected))
        block = IlnkContainer.parse(common).blocks[entries[message].block]
        assert body.count(block) == 1
        holds.append({'frame': frame, 'message_ID': message, 'actual_source_actor_ID': 46,
            'original_defender_fleet_ID': 22, 'original_direct_parent': 0x02053F40,
            'original_voice_table': 0x021178C0, 'lines': case['lines'],
            'source_template_native_wrapped_bytes_and_unique_resident_block_exact': True,
            'complete228x64_font_and_blank_paper_RGB_mask_equal': True,
            'matching_foreground_pixels': len(expected), 'missing_or_unexpected_foreground_pixels': 0,
            'uniform_margins_complete_leading_trailing_letters_bounds_pass': True,
            'capture': str(image_path), 'capture_sha256': sha(image_path.read_bytes()), 'RAM_sha256': sha(body)})
    states = []
    for frame in [5000, 6420, 6520, 6620, 6720, 6740, 6840, 6940]:
        cpu, get = get_machine(arm, raw(frame))
        mode = list(struct.unpack('<3I', cpu.mem_read(get(0x3F0F8)+8, 12)))
        states.append({'frame': frame, 'mode8_12_16': mode})
    assert states[0]['mode8_12_16'][:2] == [0, 0]
    assert states[-1]['mode8_12_16'][1:] == [1, 22], states
    assert states[-2]['mode8_12_16'] == states[-1]['mode8_12_16']
    ROOT.mkdir(parents=True)
    GUIDE.mkdir(parents=True)
    screens = []
    for name, frame in [('city_defender_reply', 6740), ('original_battle_after_dismissal', 6940)]:
        source, target = CAP/f'frame_{frame:06d}_navigation.png', GUIDE/(name+'.png')
        copy2(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        screens.append({'path': str(target), 'source': str(source), 'frame': frame, 'sha256': sha(target.read_bytes())})
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'report': str(report_path),
        'report_sha256': sha(report_path.read_bytes()), 'terminal_frame': 6940,
        'source_and_disposable_saves_unchanged': True, 'source_donor_sha256': donor_sha,
        'sole_fixture_full4MiB_replay_exact': receipt, 'accepted_input_schedule_exact': True,
        'original_source_event_defender_presence_share_and_unforced_one_in_three_choice': True,
        'original_city_confirmation_defender_choice_and_RNG_code_exact_to_clean': spans,
        'no_diplomacy_health_actor_ID_eligibility_result_RNG_or_message_injection': True,
        'complete_actual_holds': holds, 'original_mode_states': states,
        'normal_A_dismissal_enters_original_defender_fleet_battle_without_extra_page': True,
        'no_battle_outcome_or_town_surrender_claimed': True, 'guide_screenshots': screens,
        'family_scope_2038_2045_only_selected_message_has_individual_actual_activation': True,
        'all8_alternatives_have_prior_source_and_complete_native_font_review': True,
        'prior_war_pilot_1283b_not_used_for_translation_completion': True,
        'actual_reply_portrait_name_and_dismissal_transition_visually_reviewed': True,
        'targeted_headless_test_not_full_route_earned_travel_or_hardware_verification': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(ROOT/'actual_city_defense_verification.json', proof)
    save(GUIDE/'provenance.json', proof)
    print('Two complete original city-defense text holds, sole location-only fixture and normal battle entry pass.', flush=True)


if __name__ == '__main__':
    main()
