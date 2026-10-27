"""Original fled-victory holds,31 full fixture audits and normal sea return."""
import struct
from pathlib import Path
from shutil import copy2
from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_battle_fixture_v1269 import ROM,apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/aftermath_victory_verified_v1271')
RUN = Path('work/analysis/aftermath_victory_v1270')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_victory_v1270_1266')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1266 Battle aftermath')
BASE = 0x02000000


def main():
    assert not ROOT.exists() and not GUIDE.exists()
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    digest = sha(ROM.read_bytes())
    assert report['frames'] == 11782 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['ROM_sha256'] == digest
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k != 'synthetic_battle_recovery_proximity_fixtures')
    donor = report['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == '2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'
    rom = NdsImage.open(ROM)
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0xE8CC,0x11000),(0xD458,0xD540),(0x717F8,0x718D4),(0x72368,0x723C4),
        (0x7DF58,0x7E1A4),(0x7E750,0x7E788),(0x7E944,0x7E950),(0x519D4,0x51A28),(0xD9824,0xD9868))
    for lo,hi in spans:
        assert arm[lo:hi] == clean[lo:hi]
    snapshots = {}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        if r['frame'] in snapshots:
            assert snapshots[r['frame']]['sha256'] == r['sha256']
        snapshots[r['frame']] = r
    def raw(frame):
        r = snapshots[frame]
        value = Path(r['path']).read_bytes()
        assert len(value) == r['bytes'] == 0x400000 and sha(value) == r['sha256']
        return value
    fixtures = report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures) == 31 and max(r['frame'] for r in fixtures) == 5770
    rng = [struct.unpack_from('<I',arm,off)[0] for off in (0xD9858,0x51A20)]
    audits = []
    for r in fixtures:
        request = {'sighting_context':'compassAttack8'} if r['context'] == 'compassAttack8' else {'duel_context':'healthyContact'}
        before = raw(r['frame'])
        after,receipt = apply_fixture(arm,before,request)
        assert r == {**receipt,'frame':r['frame']}
        owned = set(r['owned_bytes'])
        changes = [BASE+i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a != b]
        assert all(at in owned for at in changes)
        for at in rng:
            assert not owned.intersection(range(at,at+4)) and before[at-BASE:at-BASE+4] == after[at-BASE:at-BASE+4]
        _,bg = get_machine(arm,before)
        _,ag = get_machine(arm,after)
        assert [bg(o) for o in (0x7F244,0x2E58C)] == [ag(o) for o in (0x7F244,0x2E58C)] == [1,1]
        actors = bg(0xCB184)
        assert ag(0xCB184) == actors
        objects = [actors+4+i*32 for i in range(207)]+[actors+0x19E4]
        assert [bg(0x7EE08,o) for o in objects] == [ag(0x7EE08,o) for o in objects]
        if r['context'] == 'longHealthLuckContact':
            assert r['original_unforced_special_random_chance_percent'] == 10
            assert all(v['attributes_after'][0:2] == [1,1] and v['attributes_after'][4:6] == [100,100]
                and v['positive_HP_and_native_maximum'][0] == v['positive_HP_and_native_maximum'][1] > 0
                for v in r['native_pre_duel_attribute_changes'])
        audits.append({'frame':r['frame'],'context':r['context'],'owned_bytes':len(owned),
            'actual_changed_bytes':len(changes),'before_RAM_sha256':sha(before),'after_RAM_sha256':sha(after),
            'full4MiB_delta_all208_actor_IDs_original_RNG_and_event_words_pass':True})
        if len(audits)%10 == 0:
            print(len(audits),'entire pre-duel fixture/identity/RNG audits pass.',flush=True)
    journal = read(CAP/'navigation_command_journal.json')
    assert all(r['validation_passed'] for r in journal['commands_received'])
    schedule = read(RUN/'original_load_inputs.json')
    for r in journal['commands_received']:
        c = r['command']
        if c.get('stop'):
            continue
        assert c['until'] in snapshots and c['until'] > r['frame']
        if r['frame'] >= 5772:
            assert 'battle_fixture' not in c
        if c.get('buttons') or c.get('touch') is not None:
            event = {'start':r['frame']+1,'duration':c.get('duration',12),'buttons':c.get('buttons',[])}
            if c.get('touch') is not None:
                event['touch'] = c['touch']
            schedule.append(event)
    assert schedule == report['scripted_input_schedule']
    assert not any(5773 <= e['start'] <= 10982 for e in schedule)
    entries = current_entries(common,arm)
    font_path = Path('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json')
    font = read(font_path)
    case = next(r for r in font['cases'] if r['message_id'] == 2046 and r['name_case'] is None)
    preview = Path(case['preview'])
    assert sha(preview.read_bytes()) == case['preview_sha256']
    plane = Image.open(preview).convert('L')
    assert plane.size == (228,64)
    owner,wrapped = [struct.unpack_from('<I',arm,off)[0] for off in (0x552A0,0x54450)]
    holds = []
    for frame in (10942,10982):
        body = raw(frame)
        cpu,get = get_machine(arm,body)
        fleets,actors = get(0xCB1A8),get(0xCB184)
        identity = get(0x82478,fleets+0x2090,1)
        actor = actors+0x19E4 if identity == get(0x7F244) else actors+4+identity*32
        assert identity == 18 and get(0x7EE08,actor) == 18 and get(0x53F4C,actor,0x02117900) == 2046
        assert body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0] == entries[2046].text
        assert body[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0].hex() == case['native_formatted_hex']
        image_path = CAP/f'frame_{frame:06d}_navigation.png'
        image = Image.open(image_path).convert('RGB')
        assert image.size == (256,384)
        expected = {(16+x,296+y) for y in range(64) for x in range(228) if plane.getpixel((x,y)) == 0}
        actual = {(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y)) == (0,8,0)}
        assert actual == expected,(frame,len(expected-actual),len(actual-expected))
        block = IlnkContainer.parse(common).blocks[entries[2046].block]
        assert body.count(block) == 1
        holds.append({'frame':frame,'message_ID':2046,'source_role_selector':1,'actual_source_actor_ID':18,
            'original_voice_table':0x02117900,'source_template_and_native_wrapped_bytes_exact':True,
            'complete228x64_font_foreground_and_blank_paper_RGB_mask_equal':True,
            'matching_foreground_pixels':len(expected),'missing_or_unexpected_foreground_pixels':0,
            'uniform_visible_margins_all_leading_trailing_letters_and_bounds_pass':True,
            'unique_complete_resident_block_exact':True,'lines':case['lines'],
            'capture':str(image_path),'capture_sha256':sha(image_path.read_bytes()),'RAM_sha256':sha(body)})
    states = []
    for frame,hp,mode in ((5782,[87,90],[0,1,8]),(8622,[87,0],[0,1,8]),
                          (10982,[87,0],[0,1,8]),(11782,[87,0],[0,0,0])):
        body = raw(frame)
        cpu,get = get_machine(arm,body)
        actors = get(0xCB184)
        actual_hp = [get(0x7E19C,o) for o in (actors+0x19E4,actors+4+32*32)]
        actual_mode = list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))
        assert actual_hp == hp and actual_mode == mode,(frame,actual_hp,actual_mode)
        states.append({'frame':frame,'own_enemy_HP':hp,'original_battle_mode_fields8_12_16':mode,'RAM_sha256':sha(body)})
    final_path = CAP/'frame_011782_navigation.png'
    reference = Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224/frame_011782_navigation.png')
    assert Image.open(final_path).tobytes() == Image.open(reference).tobytes()
    ROOT.mkdir(parents=True)
    GUIDE.mkdir(parents=True)
    screens = []
    for name,frame in (('flagship_fled_victory',10982),('ordinary_sailing_after_dismissal',11782)):
        source = CAP/f'frame_{frame:06d}_navigation.png'
        target = GUIDE/(name+'.png')
        copy2(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        screens.append({'path':str(target),'source':str(source),'frame':frame,'sha256':sha(target.read_bytes())})
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'report':str(report_path),
        'report_sha256':sha(report_path.read_bytes()),'terminal_frame':11782,'all31_fixture_replays':audits,
        'all_fixtures_before_duel5772_last5770':True,'no_during_or_post_duel_fixtures':True,
        'no_actor_ID_numeric_message_RNG_eligibility_flag_or_result_injection':True,
        'native_attribute_health_equipment_prerequisites_are_disclosed_testing_state_not_earned_progression':True,
        'all_accepted_inputs_match_report_original_random_and_combat_functions_exact':True,
        'complete_actual_holds':holds,'original_natural_combat_outcome_and_dismissal_states':states,
        'normal_A_dismissal_returns_to_source_mode0_and_ordinary_sailing_without_extra_page':True,
        'final_whole_screen_exact_to_prior_original_return':str(reference),'reference_sha256':sha(reference.read_bytes()),
        'source_fled_result_code_matches_clean_Japanese_ARM9':[[a,b] for a,b in spans],
        'source_and_disposable_saves_unchanged':True,'guide_screenshots':screens,
        'family_evidence_for2046_2051_only2046_has_individual_actual_activation':True,
        'other_aftermath_surrender_defense_withdrawal_gameplay_families_remain_pending':True,
        'targeted_headless_emulator_not_complete_route_or_hardware_verification':True,
        'actual_victory_text_portrait_name_and_sailing_return_visually_reviewed':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'actual_fled_victory_verification.json',proof)
    save(GUIDE/'provenance.json',proof)
    print('31 full fixture audits,two full actual2046 glyph/RGB holds and original victory-to-sailing transition pass.',flush=True)


if __name__ == '__main__':
    main()
