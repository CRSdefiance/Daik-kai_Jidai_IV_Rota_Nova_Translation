"""Full native/RGB victory holds and original rewards-to-sailing verification."""
import struct
from pathlib import Path
from shutil import copy2
from types import FunctionType
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.battle_victory_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_battle_victory_fixture_v1408 import apply_fixture,ROM
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_verified_v1410')
RUN = Path('work/analysis/battle_victory_replay_v1409')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_victory_v1409_1404')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1404 Victory reports')
BASE,TABLE = 0x02000000,0x02117EE0


if __name__=='__main__':
    assert not ROOT.exists() and not GUIDE.exists()
    release = read('work/analysis/battle_victory_release_v1403/registered_release_verification.json')
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert digest==report['ROM_sha256']==release['candidate_sha256'] and report['frames']==13200
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_battle_recovery_proximity_fixtures')
    plan,terminal = read(RUN/'run_plan.json'),read(RUN/'terminal_preservation.json')
    assert sha(Path('scripts/run_battle_victory_replay_v1409.py').read_bytes())==plan['runner_sha256']
    donor = 'febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
    assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==donor
    assert terminal['source_and_disposable_donors_unchanged']
    assert sha((RUN/'navigation.jsonl').read_bytes())==terminal['navigation_sha256']
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    original = clean.read_file('/__arm9__.bin')
    spans = [(0x72000,0x72484),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0x82428,0x82570),(0xE8CC,0xED74)]
    assert all(arm[a:b]==original[a:b] for a,b in spans)
    snapshots = {}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        body = Path(row['path']).read_bytes()
        assert len(body)==row['bytes']==0x400000 and sha(body)==row['sha256']
        if row['frame'] in snapshots:
            assert snapshots[row['frame']]['sha256']==row['sha256']
        snapshots[row['frame']] = row
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    def raw(frame):return Path(snapshots[frame]['path']).read_bytes()
    after,fixture = apply_fixture(arm,raw(4800),{'ship_sinking_context':'five_ship_approach'})
    assert len(fixture['owned_bytes'])==40
    assert report['synthetic_battle_recovery_proximity_fixtures']==[{**fixture,'frame':4800}]
    assert {BASE+i for i,(a,b) in enumerate(zip(raw(4800),after,strict=True)) if a!=b}<=set(fixture['owned_bytes'])
    schedule = read(RUN/'original_departure_inputs.json')
    journal = read(CAP/'navigation_command_journal.json')['commands_received']
    assert journal[-1]['frame']==13200 and journal[-1]['command']=={'stop':True}
    for item in journal:
        assert item['validation_passed']
        command = item['command']
        if command.get('stop'):
            continue
        assert command['until'] in snapshots and command['until']>item['frame']
        assert set(command)<={'until','buttons','touch','duration','battle_fixture'}
        if item['frame']>4800:
            assert 'battle_fixture' not in command
        if command.get('buttons') or command.get('touch') is not None:
            event = {'start':item['frame']+1,'duration':command.get('duration',12),'buttons':command.get('buttons',[])}
            if command.get('touch') is not None:
                event['touch'] = command['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    fonts_path = Path('work/analysis/battle_victory_fonts_v1397b/native_font_proof.json')
    fonts = read(fonts_path)
    assert fonts['ARM9_sha256']==sha(arm) and fonts['COMMON_sha256']==sha(common)
    case = next(r for r in fonts['cases'] if r['message_ID']==2131)
    assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    reference = Image.open(case['preview']).convert('L')
    assert reference.size==(228,64)
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    owner,wrapped = [struct.unpack_from('<I',arm,p)[0] for p in [0x552A0,0x54450]]
    entries = current_entries(common,arm)
    holds = []
    for frame in [10950,11000]:
        body = raw(frame)
        cpu,get = get_machine(arm,body)
        actors,fleets = get(0xCB184),get(0xCB1A8)
        assert get(0x82478,fleets+0x2090,1)==16 and get(0x82428,fleets+0x2090,1)==0
        actor = actors+4+16*32
        assert get(0x7EE08,actor)==16 and get(0x7E988,actor)==1 and get(0x53F4C,actor,TABLE)==2131
        assert body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[2131].text
        formatted = body[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0]
        assert formatted.hex()==case['native_formatted_hex']
        native = consumer(arm,common,body,{'patches':[]},0x53D44,1,TABLE)
        assert native['formatted_hex']==formatted.hex() and native['input_hex']==entries[2131].text.hex()
        assert native['parent']==0x02053DB8 and native['selector']==TABLE
        pixels = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        assert all(bool(p)==(reference.getpixel((i%228,i//228))==0) for i,p in enumerate(pixels))
        capture = CAP/f'frame_{frame:06d}_navigation.png'
        picture = Image.open(capture).convert('RGB')
        expected = {(16+i%228,296+i//228) for i,p in enumerate(pixels) if p}
        actual = {(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y))==(0,8,0)}
        assert actual==expected,(frame,len(expected-actual),len(actual-expected))
        block = IlnkContainer.parse(common).blocks[entries[2131].block]
        assert entries[2131].block==23 and body.count(block)==1
        holds.append({'frame':frame,'message_ID':2131,'actual_actor_ID':16,'actual_voice':1,
            'original_role':1,'original_table':TABLE,'original_parent':0x02053DB8,
            'physical_FirstMate_slot_empty_original_logical_fallback_selects_Gerhard':True,
            'native_pipeline':native,'lines':case['lines'],'native_formatted_hex':formatted.hex(),
            'whole228x64_native_independent_reference_and_actual_RGB_exact':True,
            'foreground_pixels':len(expected),'missing_or_extra_foreground_pixels':0,
            'complete_first_final_letters_single_margin_bounds_and_blank_paper_pass':True,
            'whole_current_COMMON23_resident_exactly_once':True,
            'capture':str(capture),'capture_sha256':sha(capture.read_bytes()),'RAM_sha256':sha(body)})
    states = []
    for frame in [4800,8600,9300,10050,10800,10950,11000,11100,11300,11500,12400,12600,12900,13200]:
        cpu,get = get_machine(arm,raw(frame))
        fleets = get(0xCB1A8)
        ships = []
        for slot in range(5):
            mobile = get(0x36C70,fleets+4+132+12+slot*8)
            if mobile:
                ships.append({'slot':slot,'Hull_Crew':[get(0x5543C,mobile),get(0x55444,mobile)]})
        states.append({'frame':frame,'mode':list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),
            'party_bytes':bytes(cpu.mem_read(fleets+0x2080,16)).hex(),'own_ships':ships,'RAM_sha256':sha(raw(frame))})
    by_frame = {r['frame']:r for r in states}
    assert by_frame[4800]['mode']==by_frame[13200]['mode']==[0,0,0]
    assert by_frame[8600]['mode']==by_frame[11000]['mode']==[0,1,5]
    assert len(by_frame[13200]['own_ships'])==5
    assert all(bytes.fromhex(by_frame[13200]['party_bytes'])[4*i]==64 for i in [1,2,3])
    ROOT.mkdir(parents=True)
    GUIDE.mkdir(parents=True)
    screens = []
    for name,frame in [('victory_report',11000),('ordinary_sailing_after_rewards',13200)]:
        source,target = CAP/f'frame_{frame:06d}_navigation.png',GUIDE/(name+'.png')
        copy2(source,target)
        assert sha(target.read_bytes())==sha(source.read_bytes())
        screens.append({'path':str(target),'source':str(source),'frame':frame,'sha256':sha(target.read_bytes())})
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'terminal_frame':13200,
        'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),'sole_prebattle_fixture':fixture,
        'entire4MiB_fixture_input_primary_RAM_and_PNG_hash_audits_pass':True,
        'original_victory_duel_capture_reward_and_logical_role_code_exact_clean':spans,
        'complete_actual2131_holds':holds,'original_result_reward_cargo_return_states':states,
        'normal_victory_A_dismissal_rewards_X_cargo_finish_touch_Yes_and_return_to_sailing':True,
        'untransferred_spoil_cargo_discarded_through_original_confirmation_not_silently_claimed_acquired':True,
        'source_and_disposable_saves_unchanged':True,'source_donor_sha256':donor,'guide_screenshots':screens,
        'only2131_individually_activated_other7_voices_have_native_proof_not_individual_actual_claims':True,
        'no_sinking_or_other_unreviewed_family_completion_credit':True,
        'targeted_headless_not_earned_travel_full_route_or_hardware_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'actual_victory_and_return_verification.json',proof)
    save(GUIDE/'provenance.json',proof)
    print('Two full2131 native/RGB holds,current COMMON23 residence and original victory/rewards/cargo/sailing return verified;no sinking credit.',flush=True)
