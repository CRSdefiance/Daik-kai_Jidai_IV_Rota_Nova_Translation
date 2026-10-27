"""Complete native/RGB capture holds and original dismissal/rewards/sailing audit."""
import inspect
import struct
from pathlib import Path
from shutil import copy2
from types import FunctionType
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.enemy_capture_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_enemy_capture_fixture_v1433 import apply_fixture,ROM
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save
from scripts import verify_battle_victory_replay_v1410 as prior_audit

ROOT = Path('work/analysis/enemy_capture_verified_v1435')
RUN = Path('work/analysis/enemy_capture_replay_v1434')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/enemy_capture_v1434_1430')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1430 Enemy ship capture')
BASE,TABLE = 0x02000000,0x02117B00

if __name__=='__main__':
    # Reuse the complete original report/4MiB/fixture/input/donor audit,including
    # all callback/cold-boot/terminal assertions,without reusing victory claims.
    source = Path(prior_audit.__file__).read_text(encoding='utf-8')
    body = source[source.index("    assert not ROOT.exists() and not GUIDE.exists()"):
        source.index("    fonts_path = Path(")]
    for old,new in [
        ('work/analysis/battle_victory_release_v1403/registered_release_verification.json','work/analysis/enemy_capture_release_v1429/registered_release_verification.json'),
        ('scripts/run_battle_victory_replay_v1409.py','scripts/run_enemy_capture_replay_v1434.py'),
        ('[(0x72000,0x72484),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0x82428,0x82570),(0xE8CC,0xED74)]',
         '[(0x73C00,0x74094),(0x53F0C,0x53F9C),(0x55DC4,0x55E6C),(0x36C70,0x36CB8),(0xE8CC,0xED74)]')]:
        assert body.count(old)==1,old
        body = body.replace(old,new)
    exec(compile('if True:\n'+body,__file__,'exec'),globals())
    fonts_path = Path('work/analysis/enemy_capture_fonts_v1424/native_font_research.json')
    fonts = read(fonts_path)
    assert fonts['ARM9_sha256']==sha(arm) and fonts['COMMON_sha256']==sha(common)
    case = next(r for r in fonts['cases'] if r['message_ID']==2082 and r['variant']==0)
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
    for frame in [10750,10780]:
        body = raw(frame)
        cpu,get = get_machine(arm,body)
        actors,fleets = get(0xCB184),get(0xCB1A8)
        attacker = get(0x36C70,fleets+4+132+12)
        target = get(0x36C70,fleets+4+5*132+12)
        actor = get(0x55DC4,attacker,8)
        assert actor==actors+4+18*32 and get(0x7EE08,actor)==18 and get(0x7E988,actor)==0
        assert get(0x53F4C,actor,TABLE)==2082
        assert target and get(0x55444,target)==0 and get(0x5543C,target)==30
        vtable = struct.unpack('<I',cpu.mem_read(target,4))[0]
        getter = struct.unpack('<I',cpu.mem_read(vtable+4,4))[0]
        pointer = get(getter-BASE,target)
        name = bytes(cpu.mem_read(pointer,64)).split(b'\0')[0]
        assert name==b'Hanse Cog'
        assert body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==entries[2082].text
        formatted = body[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0]
        assert formatted.hex()==case['native_pipeline']['formatted_hex']
        native = consumer(arm,common,body,{'patches':[]},0x53F0C,actor,TABLE,name)
        assert native['formatted_hex']==formatted.hex() and native['input_hex']==entries[2082].text.replace(b'%s',name).hex()
        assert native['parent']==0x02053F40 and native['selector']==TABLE
        pixels = raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        assert all(bool(p)==(reference.getpixel((i%228,i//228))==0) for i,p in enumerate(pixels))
        capture = CAP/f'frame_{frame:06d}_navigation.png'
        picture = Image.open(capture).convert('RGB')
        expected = {(16+i%228,296+i//228) for i,p in enumerate(pixels) if p}
        actual = {(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y))==(0,8,0)}
        assert actual==expected,(frame,len(expected-actual),len(actual-expected))
        block = IlnkContainer.parse(common).blocks[entries[2082].block]
        assert entries[2082].block==22 and body.count(block)==1
        holds.append({'frame':frame,'message_ID':2082,'actual_actor_ID':18,'actual_voice':0,
            'original_attacker_selector_argument':8,'original_table':TABLE,'original_parent':0x02053F40,
            'target_original_virtual_name':name.decode('ascii'),'target_Hull_Crew':[30,0],
            'native_pipeline':native,'lines':case['lines'],'native_formatted_hex':formatted.hex(),
            'whole228x64_native_independent_reference_and_actual_RGB_exact':True,
            'foreground_pixels':len(expected),'missing_or_extra_foreground_pixels':0,
            'complete_first_final_letters_uniform_margin_bounds_and_blank_paper_pass':True,
            'whole_current_COMMON22_resident_exactly_once':True,
            'capture':str(capture),'capture_sha256':sha(capture.read_bytes()),'RAM_sha256':sha(body)})
    states = []
    for frame in [4800,8600,9300,10050,10750,10780,10850,11000,11200,11400,11600,12400,12600,12900,13200]:
        cpu,get = get_machine(arm,raw(frame));fleets = get(0xCB1A8)
        ships = []
        for slot in range(5):
            mobile = get(0x36C70,fleets+4+132+12+slot*8)
            if mobile:
                ships.append({'slot':slot,'Hull_Crew':[get(0x5543C,mobile),get(0x55444,mobile)]})
        states.append({'frame':frame,'mode':list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),
            'party_bytes':bytes(cpu.mem_read(fleets+0x2080,16)).hex(),'own_ships':ships,'RAM_sha256':sha(raw(frame))})
    by_frame = {r['frame']:r for r in states}
    assert by_frame[4800]['mode']==by_frame[13200]['mode']==[0,0,0]
    assert by_frame[8600]['mode']==by_frame[10780]['mode']==[0,1,5]
    assert len(by_frame[13200]['own_ships'])==5
    assert all(bytes.fromhex(by_frame[13200]['party_bytes'])[4*i]==64 for i in [1,2,3])
    # Extra ordinary no-button holds display the longer report before A. All
    # subsequent whole screens must still match the proven original outcome.
    old = read('work/analysis/battle_victory_verified_v1410/actual_victory_and_return_verification.json')
    old_report = read(old['report']);assert sha(Path(old['report']).read_bytes())==old['report_sha256']
    previous_frames = {r['frame']:r for r in old_report['frames_captured']}
    unchanged = []
    for frame in [10850,11000,11200,11400,11600,12400,12600,12900,13000,13200]:
        source_picture = Path(previous_frames[frame]['path'])
        assert sha(source_picture.read_bytes())==previous_frames[frame]['PNG_sha256']
        picture = CAP/f'frame_{frame:06d}_navigation.png'
        assert Image.open(picture).convert('RGB').tobytes()==Image.open(source_picture).convert('RGB').tobytes(),frame
        unchanged.append({'frame':frame,'whole_RGB_equal_to_V1404':True,'source':str(source_picture),'source_sha256':sha(source_picture.read_bytes())})
    ROOT.mkdir(parents=True);GUIDE.mkdir(parents=True)
    screens = []
    for name,frame in [('enemy_ship_capture',10780),('ordinary_sailing_after_rewards',13200)]:
        source,target = CAP/f'frame_{frame:06d}_navigation.png',GUIDE/(name+'.png')
        copy2(source,target);assert sha(target.read_bytes())==sha(source.read_bytes())
        screens.append({'path':str(target),'source':str(source),'frame':frame,'sha256':sha(target.read_bytes())})
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'terminal_frame':13200,
        'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),'sole_prebattle_fixture':fixture,
        'entire4MiB_fixture_input_primary_RAM_and_PNG_hash_audits_pass':True,
        'original_capture_duel_reward_and_actor_selection_code_exact_clean':spans,
        'complete_actual2082_holds':holds,'original_result_reward_cargo_return_states':states,
        'later10_whole_reward_cargo_and_sailing_screens_exact_to_V1404':unchanged,
        'normal_capture_A_dismissal_flagship_victory_rewards_X_cargo_finish_touch_Yes_and_return_to_sailing':True,
        'extra_no_button_capture_holds_at10750_and10780_before_original_A':True,
        'untransferred_spoil_cargo_discarded_through_original_confirmation_not_silently_claimed_acquired':True,
        'source_and_disposable_saves_unchanged':True,'source_donor_sha256':donor,'guide_screenshots':screens,
        'only2082_individually_activated_other7_voices_have_native_proof_not_individual_actual_claims':True,
        'no_sinking_or_other_unreviewed_family_completion_credit':True,
        'targeted_headless_not_earned_travel_full_route_or_hardware_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'actual_capture_and_return_verification.json',proof);save(GUIDE/'provenance.json',proof)
    print('Two complete2082 native/RGB holds,current COMMON22 and original capture/reward/cargo/sailing return verified.',flush=True)
