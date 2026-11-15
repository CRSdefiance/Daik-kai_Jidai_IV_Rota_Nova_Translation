"""Verify actual2011 full glyphs,prebattle fixture and original sailing return."""
import struct
from pathlib import Path
from shutil import copy2
from types import FunctionType
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_sinking_editorial import current_entries
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.native_ship_sinking_fixture_v1352 import apply_fixture
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/flagship_capture_verified_v1354')
RUN = Path('work/analysis/ship_sinking_live_v1353')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_v1353_1344')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1344 Flagship capture')
ROM = Path('out/all_routes_combined_v1344_candidate.nds')
BASE,TABLE = 0x02000000,0x02117740


def main():
    assert not ROOT.exists() and not GUIDE.exists()
    release = read('work/analysis/ship_sinking_release_v1343/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256']==release['candidate_sha256'] and report['frames']==13200
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_battle_recovery_proximity_fixtures')
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    run = read(RUN/'run_plan.json')
    donor = 'febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
    assert sha(Path(run['source_donor']).read_bytes())==sha(Path(run['disposable_donor']).read_bytes())==donor
    rom = NdsImage.open(ROM)
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x72368,0x72484),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0xE8CC,0xED74)]
    assert all(arm[lo:hi]==clean[lo:hi] for lo,hi in spans)
    snapshots = {}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        value = Path(row['path']).read_bytes()
        assert len(value)==row['bytes']==0x400000 and sha(value)==row['sha256']
        if row['frame'] in snapshots:
            assert snapshots[row['frame']]['sha256']==row['sha256']
        snapshots[row['frame']] = row
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    def raw(frame):
        return Path(snapshots[frame]['path']).read_bytes()
    after,receipt = apply_fixture(arm,raw(4800),{'ship_sinking_context':'five_ship_approach'})
    assert report['synthetic_battle_recovery_proximity_fixtures']==[{**receipt,'frame':4800}]
    assert len(receipt['owned_bytes'])==40
    assert {BASE+i for i,(a,b) in enumerate(zip(raw(4800),after,strict=True)) if a!=b}<set(receipt['owned_bytes'])
    schedule = read(RUN/'original_departure_inputs.json')
    journal = read(CAP/'navigation_command_journal.json')
    for item in journal['commands_received']:
        assert item['validation_passed']
        command = item['command']
        if command.get('stop'):
            continue
        assert command['until'] in snapshots and command['until']>item['frame']
        if item['frame']>4800:
            assert 'battle_fixture' not in command
        if command.get('buttons') or command.get('touch') is not None:
            event = {'start':item['frame']+1,'duration':command.get('duration',12),'buttons':command.get('buttons',[])}
            if command.get('touch') is not None:
                event['touch'] = command['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    entries = current_entries(common,arm)
    old_font_path = Path('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json')
    old_case = next(r for r in read(old_font_path)['cases'] if r['message_id']==2011 and r['name_case'] is None)
    assert old_case['compiled_hex']==entries[2011].text.hex()
    assert sha(Path(old_case['preview']).read_bytes())==old_case['preview_sha256']
    reference = Image.open(old_case['preview']).convert('L')
    assert reference.size==(228,64)
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    owner,wrapped = [struct.unpack_from('<I',arm,o)[0] for o in [0x552A0,0x54450]]
    holds = []
    for frame in [10800,10850]:
        body = raw(frame)
        cpu,get = get_machine(arm,body)
        fleets,actors = get(0xCB1A8),get(0xCB184)
        actor = get(0x82428,fleets+0x2090,1)
        assert get(0x82478,fleets+0x2090,1)==16 and actor==actors+4+16*32
        assert get(0x7E988,actor)==1 and get(0x53F4C,actor,TABLE)==2011
        assert struct.unpack_from('<I',clean,TABLE-BASE+4)[0]==0xFFFFFFFF
        assert body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[2011].text
        formatted = body[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0]
        assert formatted.hex()==old_case['native_formatted_hex']
        native = consumer(arm,common,body,{'patches':[]},0x53D44,1,TABLE)
        assert native['parent']==0x02053DB8 and native['selector']==TABLE
        assert native['formatted_hex']==formatted.hex()
        pixels = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),old_case['lines'])
        assert all(bool(p)==(reference.getpixel((i%228,i//228))==0) for i,p in enumerate(pixels))
        image = CAP/f'frame_{frame:06d}_navigation.png'
        picture = Image.open(image).convert('RGB')
        expected = {(16+i%228,296+i//228) for i,p in enumerate(pixels) if p}
        actual = {(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y))==(0,8,0)}
        assert actual==expected,(frame,len(expected-actual),len(actual-expected))
        block = IlnkContainer.parse(common).blocks[entries[2011].block]
        assert body.count(block)==1
        holds.append({'frame':frame,'message_ID':2011,'actual_actor_ID':16,'actual_voice':1,
            'original_role_selector':1,'original_table':TABLE,'original_parent':0x02053DB8,
            'source_FFFFFFFF_voice1_falls_back_to2011':True,'native_pipeline':native,'lines':old_case['lines'],
            'whole228x64_native_independent_reference_and_actual_RGB_mask_exact':True,
            'matching_foreground_pixels':len(expected),'missing_or_extra_pixels':0,
            'complete_leading_trailing_letters_uniform_margins_bounds_and_blank_paper_pass':True,
            'capture':str(image),'capture_sha256':sha(image.read_bytes()),'RAM_sha256':sha(body)})
    states = []
    for frame in [4800,5000,8500,8600,9000,9300,10050,10600,10800,10950,11100,11300,11500,12900,13200]:
        cpu,get = get_machine(arm,raw(frame))
        fleets,actors = get(0xCB1A8),get(0xCB184)
        own,enemy = fleets+4+132,fleets+4+5*132
        ships = []
        for fleet_id,fleet in [(1,own),(5,enemy)]:
            for slot in range(5):
                mobile = get(0x36C70,fleet+12+slot*8)
                if mobile:
                    ships.append({'fleet_ID':fleet_id,'slot':slot,'Hull_Crew':[get(0x5543C,mobile),get(0x55444,mobile)],
                        'state0D':bytes(cpu.mem_read(mobile+13,1))[0]})
        mode = list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))
        states.append({'frame':frame,'mode8_12_16':mode,'parties_hex':bytes(cpu.mem_read(fleets+0x2080,16)).hex(),
            'original_captain_HP':[get(0x7E19C,actors+0x19E4),get(0x7E19C,actors+4+29*32)],
            'ships':ships,'RAM_sha256':sha(raw(frame))})
    by_frame = {r['frame']:r for r in states}
    assert by_frame[4800]['mode8_12_16']==by_frame[5000]['mode8_12_16']==[0,0,0]
    assert by_frame[8600]['mode8_12_16']==by_frame[10800]['mode8_12_16']==[0,1,5]
    assert by_frame[13200]['mode8_12_16']==[0,0,0]
    assert all(bytes.fromhex(by_frame[13200]['parties_hex'])[4*i]==64 for i in [1,2,3])
    assert len([s for s in by_frame[13200]['ships'] if s['fleet_ID']==1])==5
    ROOT.mkdir(parents=True)
    GUIDE.mkdir(parents=True)
    screens = []
    for name,frame in [('revised_flagship_capture_report',10850),('ordinary_sailing_after_capture',13200)]:
        source,target = CAP/f'frame_{frame:06d}_navigation.png',GUIDE/(name+'.png')
        copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        screens.append({'path':str(target),'source':str(source),'frame':frame,'sha256':sha(target.read_bytes())})
    proof = {'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'report':str(report_path),
        'report_sha256':sha(report_path.read_bytes()),'terminal_frame':13200,'sole_fixture':receipt,
        'all4MiB_fixture_input_schedule_primary_RAM_and_PNG_hash_audits_pass':True,
        'original_duel_victory_capture_and_return_code_exact_clean':spans,
        'complete_actual2011_holds':holds,'original_encounter_duel_capture_reward_and_return_states':states,
        'normal_A_dialogue_X_cargo_finish_touch_Yes_and_reward_dismissal_return_to_sailing':True,
        'source_and_disposable_saves_unchanged':True,'source_donor_sha256':donor,'guide_screenshots':screens,
        'only2011_individually_activated_other_voice_alternatives_need_final_review':True,
        'no_ship_sinking_or_other_new_translation_completion_claim':True,
        'targeted_headless_not_earned_travel_full_route_or_hardware_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'actual_flagship_capture_verification.json',proof)
    save(GUIDE/'provenance.json',proof)
    print('Two complete2011 native/independent/actual RGB holds and original capture-reward-cargo-sailing return verified;no sinking credit.',flush=True)


if __name__=='__main__':
    main()
