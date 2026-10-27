"""Actual revised fire alert,complete glyph masks and original follow-up/battle return."""
import struct
from pathlib import Path
from shutil import copy2
from types import FunctionType
from PIL import Image
from dk4tool.patch.powder_fire_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.native_powder_fire_fixture_v1319 import ROM,apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_verified_v1322')
RUN = Path('work/analysis/powder_fire_scene_v1320')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/powder_fire_v1320_1316')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1316 Powder fire')
BASE = 0x02000000


def main():
    assert not ROOT.exists() and not GUIDE.exists()
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert report['frames'] == 7590 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['ROM_sha256'] == digest
    assert not report['goal_complete'] and not report['hardware_device_verification']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k != 'synthetic_battle_recovery_proximity_fixtures')
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    plan = read(RUN/'run_plan.json')
    donor_sha = '2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    assert sha(Path(plan['source_donor']).read_bytes()) == sha(Path(plan['disposable_donor']).read_bytes()) == donor_sha
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    spans = [(0x755CC,0x7564C),(0x55DC4,0x55E6C),(0x519D4,0x51A28),(0x6ED34,0x6EE90)]
    assert all(arm[lo:hi] == clean.read_file('/__arm9__.bin')[lo:hi] for lo,hi in spans)
    snapshots = {}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        if row['frame'] in snapshots:
            assert snapshots[row['frame']]['sha256'] == row['sha256']
        snapshots[row['frame']] = row

    def raw(frame):
        row = snapshots[frame]
        value = Path(row['path']).read_bytes()
        assert len(value) == row['bytes'] == 0x400000 and sha(value) == row['sha256']
        return value

    before = raw(5000)
    after,receipt = apply_fixture(arm,before,{'town_context':'SaoTomeGunnery'})
    assert report['synthetic_battle_recovery_proximity_fixtures'] == [{**receipt,'frame':5000}]
    owned = set(receipt['owned_bytes'])
    changes = [BASE+i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a != b]
    assert len(owned) == 24 and len(changes) == 16 and all(address in owned for address in changes)
    cpu,get = get_machine(arm,before)
    for root,length in [(get(0xCB184),0x1A04),(get(0xCB178),4+114*108),(get(0xCB160),4+21*76)]:
        assert before[root-BASE:root-BASE+length] == after[root-BASE:root-BASE+length]
    for offset in [0xD9858,0x51A20]:
        at = struct.unpack_from('<I',arm,offset)[0]
        assert not owned.intersection(range(at,at+4)) and before[at-BASE:at-BASE+4] == after[at-BASE:at-BASE+4]
    schedule = read(RUN/'original_load_inputs.json')
    for item in read(CAP/'navigation_command_journal.json')['commands_received']:
        assert item['validation_passed']
        command = item['command']
        if command.get('stop'):
            continue
        assert command['until'] in snapshots and command['until'] > item['frame']
        if item['frame'] > 5000:
            assert 'battle_fixture' not in command
        if command.get('buttons') or command.get('touch') is not None:
            event = {'start':item['frame']+1,'duration':command.get('duration',12),'buttons':command.get('buttons',[])}
            if command.get('touch') is not None:
                event['touch'] = command['touch']
            schedule.append(event)
    assert schedule == report['scripted_input_schedule']
    entries = current_entries(common,arm)
    font_path = Path('work/analysis/powder_fire_fonts_v1310/native_font_proof.json')
    font = read(font_path)
    case = next(row for row in font['cases'] if row['source_voice'] == 1)
    assert case['message_id'] == 2053
    owner,wrapped = [struct.unpack_from('<I',arm,offset)[0] for offset in [0x552A0,0x54450]]
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path) == 'out/all_routes_combined_v255_candidate.nds'
            return rom
    raster = FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    holds,states = [],[]
    for frame in [7210,7250,7350,7390]:
        body = raw(frame)
        cpu,get = get_machine(arm,body)
        fleets,actors,world = get(0xCB1A8),get(0xCB184),get(0xCB19C)
        template = body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]
        formatted = body[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0]
        if frame in [7210,7250]:
            actor = get(0x82428,fleets+0x2090,9)
            assert actor == actors+4+16*32 and get(0x53F4C,actor,0x02117980) == 2053
            assert template == entries[2053].text and formatted.hex() == case['native_formatted_hex']
            lines,selected = case['lines'],[2053]
            preview = Path(case['preview'])
            assert sha(preview.read_bytes()) == case['preview_sha256']
            plane = Image.open(preview).convert('L')
            mask = bytes(1 if value == 0 else 0 for value in plane.tobytes())
        else:
            selected = [entry.message_id for entry in entries if entry.text == template]
            assert selected == [585,586]
            lines = [line.strip().decode('ascii') for line in formatted.split(b'\n')]
            assert lines == ['Fire extinguished!']
            mask = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
            assert mask == independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
        picture_path = CAP/f'frame_{frame:06d}_navigation.png'
        picture = Image.open(picture_path).convert('RGB')
        expected = {(16+x,296+y) for y in range(64) for x in range(228) if mask[y*228+x]}
        actual = {(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y)) == (0,8,0)}
        assert actual == expected,(frame,len(expected-actual),len(actual-expected))
        block_id = entries[selected[0]].block
        assert body.count(IlnkContainer.parse(common).blocks[block_id]) == 1
        holds.append({'frame':frame,'native_message_IDs_matching_cached_template':selected,
            'new_fire_message':frame in [7210,7250],'actual_source_Gunner_ID':16 if frame in [7210,7250] else None,
            'lines':lines,'stored_template_native_wrapping_and_unique_resident_block_exact':True,
            'complete228x64_font_and_blank_paper_RGB_mask_equal':True,'matching_foreground_pixels':len(expected),
            'missing_or_unexpected_foreground_pixels':0,'uniform_margins_complete_first_final_letters_and_bounds_pass':True,
            'capture':str(picture_path),'capture_sha256':sha(picture_path.read_bytes()),'RAM_sha256':sha(body)})
    old_image = Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_gunnery_v1300_1266/frame_007210_navigation.png')
    a,b = [Image.open(path).convert('RGB') for path in [CAP/'frame_007210_navigation.png',old_image]]
    assert a.crop((0,0,256,294)).tobytes() == b.crop((0,0,256,294)).tobytes()
    for frame in [5810,5910,7210,7250,7350,7390,7490,7590]:
        cpu,get = get_machine(arm,raw(frame))
        fleets,world,towns = get(0xCB1A8),get(0xCB19C),get(0xCB178)
        mobile = get(0x36C70,fleets+4+132+12)
        states.append({'frame':frame,'mode8_12_16':list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),
            'town_ID':struct.unpack('<I',cpu.mem_read(world+0x1360,4))[0],
            'town_defenses':get(0xB3FD4,towns+4+73*108,1),'own_Hull_Crew':[get(0x5543C,mobile),get(0x55444,mobile)],
            'original_mobile_flag0E':bytes(cpu.mem_read(mobile+14,1))[0]})
    assert all(state['mode8_12_16'] == [0,1,64] and state['town_ID'] == 73 for state in states)
    assert states[0]['town_defenses'] == 100 and all(state['town_defenses'] == 99 for state in states[1:])
    assert all(state['original_mobile_flag0E'] & 1 for state in states if state['frame'] in [7210,7250])
    assert all(not state['original_mobile_flag0E'] & 1 for state in states if state['frame'] >= 7350)
    ROOT.mkdir(parents=True)
    GUIDE.mkdir(parents=True)
    screens = []
    for name,frame in [('powder_fire_revised_alert',7250),('original_fire_extinguished_response',7390),('original_sea_battle_return',7590)]:
        source,target = CAP/f'frame_{frame:06d}_navigation.png',GUIDE/(name+'.png')
        copy2(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        screens.append({'path':str(target),'source':str(source),'frame':frame,'sha256':sha(target.read_bytes())})
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
        'terminal_frame':7590,'sole_prebattle_fixture_entire4MiB_replayed':receipt,'all_accepted_inputs_exact':True,
        'no_actor_ID_RNG_eligibility_fire_flag_result_or_numeric_message_injection':True,
        'no_during_or_post_battle_fixtures':True,'source_unforced_powder_fire_and_gun_position_actor_code_exact_clean':spans,
        'complete_actual_holds':holds,'original_fire_and_followup_states':states,
        'source_Gerhard_portrait_name_and_whole_upper294_rows_exact_to_old_event':True,
        'source_header_reference':str(old_image),'source_header_reference_sha256':sha(old_image.read_bytes()),
        'normal_A_dismissals_preserve_extinguished_response_clear_fire_and_return_to_original_sea_battle':True,
        'no_town_surrender_battle_victory_or_other_aftermath_completion_claim':True,
        'source_and_disposable_donors_unchanged':True,'guide_screenshots':screens,
        'family_scope_six_2052_2057_only2053_has_individual_actual_activation':True,
        'all8_voice_native_pipelines_and6_unique_messages_have_prior_complete_native_fonts':True,
        'actual_revised_alert_followup_and_sea_battle_return_visually_reviewed':True,
        'targeted_headless_not_earned_prerequisites_full_route_or_hardware_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'actual_powder_fire_verification.json',proof)
    save(GUIDE/'provenance.json',proof)
    print('Two complete revised2053 and two preserved extinguished-response glyph/RGB holds plus original battle return pass.',flush=True)


if __name__ == '__main__':
    main()
