"""Map eight individual enemy-ship capture reports from clean source and V1404."""
import struct
from dataclasses import asdict
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.battle_victory_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/enemy_capture_context_v1413')
ROM = Path('out/all_routes_combined_v1404_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_victory_v1409_1404')
BASE,TABLE = 0x02000000,0x02117B00
IDS = list(range(2082,2090))


if __name__=='__main__':
    assert not ROOT.exists()
    release = read('work/analysis/battle_victory_release_v1403/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    clean,rom = NdsImage.open('work/clean.nds'),NdsImage.open(ROM)
    source,arm = clean.read_file('/__arm9__.bin'),rom.read_file('/__arm9__.bin')
    common,original_common = rom.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/COMMON/MESFILE.DK4')
    jp,en = common_message_entries(original_common,source),current_entries(common,arm)
    ledger = read('translations/editorial_review_current_v1.json')
    complete = {n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not set(IDS)&(complete|set(ledger['reviewed_but_incomplete_COMMON_IDs']))
    actual = read('work/analysis/battle_victory_verified_v1410/actual_victory_and_return_verification.json')
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    assert sha(report_path.read_bytes())==actual['report_sha256']
    assert report['ROM_sha256']==release['candidate_sha256'] and report['frames']==13200
    snap = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==10700)
    raw_path = Path(snap['path'])
    raw = raw_path.read_bytes()
    assert len(raw)==0x400000 and sha(raw)==snap['sha256']
    picture = next(r for r in report['frames_captured'] if r['frame']==10700)
    capture = Path(picture['path'])
    assert sha(capture.read_bytes())==picture['PNG_sha256']
    before_picture = next(r for r in report['frames_captured'] if r['frame']==10600)
    assert sha(Path(before_picture['path']).read_bytes())==before_picture['PNG_sha256']
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.skipdata = True
    spans = [(0x73C00,0x74094),(0x55DC4,0x55E6C),(0x53F0C,0x53F9C),(0x36C70,0x36CB8)]
    preserved = []
    for lo,hi in spans:
        assert arm[lo:hi]==source[lo:hi]
        preserved.append({'span':[BASE+lo,BASE+hi],'sha256':sha(source[lo:hi]),
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
                for i in md.disasm(source[lo:hi],BASE+lo)]})
    assert list(struct.unpack_from('<8I',source,TABLE-BASE))==IDS
    assert arm[TABLE-BASE:TABLE-BASE+32]==source[TABLE-BASE:TABLE-BASE+32]
    literals = {BASE+o for o in range(0,len(source)-4,4) if struct.unpack_from('<I',source,o)[0]==TABLE}
    loads = []
    for o in range(0,0x130000,4):
        word = struct.unpack_from('<I',source,o)[0]
        if word&0x0F7F0000==0x051F0000:
            literal = BASE+o+8+(word&4095)*(1 if word&0x00800000 else -1)
            if literal in literals:
                loads.append(BASE+o)
    assert loads==[0x02074050]
    assert next(md.disasm(source[0x74030:0x74034],0x02074030)).op_str=='r1, #8'
    assert next(md.disasm(source[0x74034:0x74038],0x02074034)).op_str=='#0x2055dc4'
    assert next(md.disasm(source[0x74058:0x7405C],0x02074058)).op_str=='#0x2053f0c'
    cpu,get = get_machine(arm,raw)
    actors,fleets,captain = get(0xCB184),get(0xCB1A8),get(0x7F244)
    choices = []
    for identity in range(207):
        if identity==captain:
            continue
        actor = actors+4+identity*32
        voice,number = get(0x7E988,actor),get(0x53F4C,actor,TABLE)
        assert get(0x7EE08,actor)==identity and number==2082+voice
        choices.append({'existing_actor_ID':identity,'actor_object':actor,'source_voice':voice,'message_ID':number})
    assert len(choices)==206 and {r['source_voice'] for r in choices}==set(range(8))
    attacker = get(0x36C70,fleets+4+132+12)
    target = get(0x36C70,fleets+4+5*132+12)
    assert attacker and target and get(0x55444,target)==0 and get(0x5543C,target)>0
    actor = get(0x55DC4,attacker,8)
    assert get(0x7EE08,actor)==18 and get(0x7E988,actor)==0 and get(0x53F4C,actor,TABLE)==2082
    vt = struct.unpack('<I',cpu.mem_read(target,4))[0]
    name_method = struct.unpack('<I',cpu.mem_read(vt+4,4))[0]
    name_pointer = get(name_method-BASE,target)
    name = bytes(cpu.mem_read(name_pointer,64)).split(b'\0')[0]
    assert name==b'Hanse Cog'
    owner,wrapped = [struct.unpack_from('<I',arm,p)[0] for p in [0x552A0,0x54450]]
    assert raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==en[2082].text
    formatted = raw[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0]
    assert formatted==en[2082].text.replace(b'%s',name)==b'Enemy ship Hanse Cog captured!'
    records = []
    for number in range(2080,2092):
        if number in IDS:
            assert jp[number].text.count(b'%s')==en[number].text.count(b'%s')==1
        records.append({'message_id':number,'selected_for_review':number in IDS,
            'source_reference':{k:v for k,v in asdict(jp[number]).items() if k!='text'},
            'source_hex':jp[number].text.hex(),'source_Japanese':jp[number].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[number]).items() if k!='text'},
            'current_text_hex':en[number].text.hex(),'current_English':en[number].text.decode('cp932')})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_and_original_capture_context.json',{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_table':TABLE,'raw8_voice_table':IDS,'original_literal_load':loads[0],
        'original_call':0x02074058,'original_entry':0x02053F0C,'original_parent':0x02053F40,
        'selector_stack_offset':0x274,'original_attacker_actor_selector_helper':0x02055DC4,
        'original_attacker_actor_selector_argument':8,'all206_existing_actor_choices':choices,
        'unchanged_clean_code_spans':preserved,'records_and_immediate_neighbors':records,
        'original_context':'After original boarding/duel and crew-loss processing,the target crew getter is zero. The original source uses the attacker-side55DC4 selector8 officer,the target virtual name getter+4 and direct53F0C/table02117B00 to announce capture of the named enemy vessel. This is distinct from whole-flagship result2011-2015,ship sinking2058-2073,and own capture2074-2081.',
        'argument_contract':'Exactly one original target ship-name C string in r2;do not invent captain,company,casualty or reward arguments.',
        'prior_actual_2082':{'frame':10700,'capture':str(capture),'capture_sha256':sha(capture.read_bytes()),
            'snapshot':str(raw_path),'snapshot_sha256':sha(raw),'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
            'actual_actor_ID':18,'source_voice':0,'original_attacker_mobile':attacker,'original_target_mobile':target,
            'target_Hull_Crew':[get(0x5543C,target),get(0x55444,target)],'target_virtual_name_getter':name_method,
            'target_name_pointer':name_pointer,'target_name':name.decode('ascii'),'target_name_hex':name.hex(),
            'compiled_hex':en[2082].text.hex(),'native_formatted_hex':formatted.hex(),
            'visually_reviewed_Charles_capture_report_and_A_prompt':True,
            'earlier_actual_context_not_new_font_or_completion_approval':True},
        'frame10600_is_still_visible_duel_defeat_dialogue_not_a_capture_hold':True,
        'frame10600_reference':before_picture,'native_argument_count':1,
        'no_source_prose_formatting_release_or_completion_credit_yet':True,
        'all_read_only_existing_objects_no_actor_ID_RNG_result_or_new_fixture_edits':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight individual capture reports mapped:one original selector8/direct caller,206 voices,actual Charles2082/ship name. No review credit yet.',flush=True)
