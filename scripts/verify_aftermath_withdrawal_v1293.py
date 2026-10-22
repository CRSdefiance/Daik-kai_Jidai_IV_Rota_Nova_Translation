"""Original town-distance withdrawal: whole fixture, glyph masks and sailing return."""
import struct
from pathlib import Path
from shutil import copy2
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_town_fixture_v1290 import ROM, apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/aftermath_withdrawal_verified_v1293')
RUN = Path('work/analysis/aftermath_town_v1291')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_town_v1291_1266')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1266 Town withdrawal')
BASE = 0x02000000


def main():
    assert not ROOT.exists() and not GUIDE.exists()
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert report['frames'] == 7510 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['ROM_sha256'] == digest
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k != 'synthetic_battle_recovery_proximity_fixtures')
    plan = read(RUN/'run_plan.json')
    donor_sha = '2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    assert sha(Path(plan['source_donor']).read_bytes()) == sha(Path(plan['disposable_donor']).read_bytes()) == donor_sha
    rom = NdsImage.open(ROM)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x6ED34,0x6EE90),(0x717F8,0x71968),(0x7251C,0x72BDC),
             (0x513D0,0x514C0),(0x519D4,0x51A28),(0x82BA8,0x82BD0)]
    assert all(arm[lo:hi] == clean[lo:hi] for lo,hi in spans)
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
    after, receipt = apply_fixture(arm,before,{'town_context':'SaoTomeFirstMate'})
    assert fixtures[0] == {**receipt,'frame':5000}
    owned = set(receipt['owned_bytes'])
    assert len(owned) == 18 and len(receipt['changes']) == 12
    assert all(BASE+i in owned for i,(a,b) in enumerate(zip(before,after,strict=True)) if a != b)
    assert receipt['all_actor_objects_IDs_health_towns_defenses_shares_diplomacy_RNG_and_events_exact']
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
            event = {'start':row['frame']+1,'duration':command.get('duration',12),'buttons':command.get('buttons',[])}
            if command.get('touch') is not None:
                event['touch'] = command['touch']
            schedule.append(event)
    assert schedule == report['scripted_input_schedule']
    assert not any(5910 <= event['start'] <= 7310 for event in schedule)
    entries = current_entries(common,arm)
    font_path = Path('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json')
    font = read(font_path)
    case = next(row for row in font['cases'] if row['message_id'] == 2114 and row['name_case'] is None)
    preview = Path(case['preview'])
    assert sha(preview.read_bytes()) == case['preview_sha256']
    plane = Image.open(preview).convert('L')
    assert plane.size == (228,64)
    owner, wrapped = [struct.unpack_from('<I',arm,off)[0] for off in [0x552A0,0x54450]]
    holds = []
    for frame in [7110,7310]:
        body = raw(frame)
        cpu,get = get_machine(arm,body)
        fleets,actors = get(0xCB1A8),get(0xCB184)
        identity = get(0x82478,fleets+0x2090,1)
        actor = get(0x82428,fleets+0x2090,1)
        assert identity == 18 and actor == actors+4+18*32 and get(0x7EE08,actor) == 18
        assert get(0x53F4C,actor,0x02117D00) == 2114
        assert body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0] == entries[2114].text
        assert body[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0].hex() == case['native_formatted_hex']
        image_path = CAP/f'frame_{frame:06d}_navigation.png'
        picture = Image.open(image_path).convert('RGB')
        assert picture.size == (256,384)
        expected = {(16+x,296+y) for y in range(64) for x in range(228) if plane.getpixel((x,y)) == 0}
        actual = {(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y)) == (0,8,0)}
        assert actual == expected,(frame,len(expected-actual),len(actual-expected))
        block = IlnkContainer.parse(common).blocks[entries[2114].block]
        assert body.count(block) == 1
        holds.append({'frame':frame,'message_ID':2114,'actual_source_actor_ID':18,'original_role_selector':1,
            'original_voice_table':0x02117D00,'original_parent':0x02053DB8,'lines':case['lines'],
            'stored_template_native_wrapping_and_unique_complete_resident_block_exact':True,
            'complete228x64_font_and_blank_paper_RGB_mask_equal':True,'matching_foreground_pixels':len(expected),
            'missing_or_unexpected_foreground_pixels':0,'uniform_margins_complete_leading_trailing_letters_bounds_pass':True,
            'capture':str(image_path),'capture_sha256':sha(image_path.read_bytes()),'RAM_sha256':sha(body)})
    states = []
    for frame in [5810,5910,6110,6510,6910,7110,7310,7410,7510]:
        cpu,get = get_machine(arm,raw(frame))
        fleets,world,towns = [get(fn) for fn in [0xCB1A8,0xCB19C,0xCB178]]
        town, mobile = towns+4+73*108,get(0x36C70,fleets+4+132+12)
        get(0x36A24,0x02470010,mobile)
        vt = struct.unpack('<I',cpu.mem_read(town,4))[0]
        get(struct.unpack('<I',cpu.mem_read(vt+0x20,4))[0]-BASE,0x02470000,town)
        center = list(struct.unpack('<2i',cpu.mem_read(0x02470000,8)))
        point = list(struct.unpack('<2i',cpu.mem_read(0x02470010,8)))
        distance = get(0x513D0,0x02470000,0x02470010,0)
        state = {'frame':frame,'mode8_12_16':list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),
            'town_battle_ID':struct.unpack('<I',cpu.mem_read(world+0x1360,4))[0],
            'own_live_Hull_Crew':[get(0x5543C,mobile),get(0x55444,mobile)],
            'town_defenses':get(0xB3FD4,town,1),'native_town_center':center,'own_live_map_point':point,
            'original513D0_distance_result':distance,'RAM_sha256':sha(raw(frame))}
        states.append(state)
    by_frame = {row['frame']:row for row in states}
    assert by_frame[5910]['mode8_12_16'] == [0,1,64] and by_frame[5910]['town_battle_ID'] == 73
    assert by_frame[7110]['original513D0_distance_result'] == by_frame[7310]['original513D0_distance_result'] == 2
    assert all(row['town_defenses'] == 100 for row in states)
    assert by_frame[5910]['own_live_Hull_Crew'] == [60,39]
    assert by_frame[7310]['own_live_Hull_Crew'] == by_frame[7410]['own_live_Hull_Crew'] == [59,33]
    assert by_frame[7410]['mode8_12_16'] == by_frame[7510]['mode8_12_16'] == [0,0,0]
    assert by_frame[7410]['town_battle_ID'] == by_frame[7510]['town_battle_ID'] == 115
    ROOT.mkdir(parents=True)
    GUIDE.mkdir(parents=True)
    screens = []
    for name,frame in [('original_withdrawal_announcement',7310),('ordinary_sailing_after_withdrawal',7510)]:
        source,target = CAP/f'frame_{frame:06d}_navigation.png',GUIDE/(name+'.png')
        copy2(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        screens.append({'path':str(target),'source':str(source),'frame':frame,'sha256':sha(target.read_bytes())})
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
        'terminal_frame':7510,'sole_prebattle_fixture_full4MiB_replay':receipt,'all_original_inputs_exact':True,
        'no_inputs_or_fixtures_from5910_through7310':True,'no_actor_ID_RNG_eligibility_battle_state_result_or_message_injection':True,
        'original_town_battle_distance_and_withdrawal_code_equal_clean':spans,
        'complete_actual_holds':holds,'original_town_battle_movement_withdrawal_and_return_states':states,
        'normal_A_dismissal_clears_battle_and_town_ID_and_returns_to_ordinary_sailing':True,
        'no_town_surrender_or_other_aftermath_outcome_claimed':True,'source_and_disposable_donors_unchanged':True,
        'source_donor_sha256':donor_sha,'guide_screenshots':screens,
        'family_scope2114_2121_only2114_has_individual_actual_activation':True,
        'all8_alternatives_have_prior_source_and_complete_native_font_review':True,
        'actual_reply_portrait_name_and_sailing_return_visually_reviewed':True,
        'targeted_headless_not_earned_travel_or_assignment_full_route_or_hardware_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'actual_withdrawal_verification.json',proof)
    save(GUIDE/'provenance.json',proof)
    print('Two full2114 glyph/RGB holds,original town-distance withdrawal and ordinary sailing return pass.',flush=True)


if __name__ == '__main__':
    main()
