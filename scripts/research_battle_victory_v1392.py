"""Bind eight unreviewed victory reports to clean Japanese and original gameplay."""
import struct
from dataclasses import asdict
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.flagship_capture_precision import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_context_v1392')
ROM = Path('out/all_routes_combined_v1364_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/flagship_capture_v1369_1364')
BASE,TABLE = 0x02000000,0x02117EE0
IDS = list(range(2130,2138))


def main():
    assert not ROOT.exists()
    release = read('work/analysis/flagship_precision_release_v1363/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm,source = rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    common,source_common = rom.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/COMMON/MESFILE.DK4')
    en,jp = current_entries(common,arm),common_message_entries(source_common,source)
    ledger = read('translations/editorial_review_current_v1.json')
    complete = {n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not (set(IDS)&(complete|set(ledger['reviewed_but_incomplete_COMMON_IDs'])))
    actual = read('work/analysis/flagship_capture_verified_v1370/actual_flagship_capture_verification.json')
    report_path = CAP/'capture_report.json'
    report = read(report_path)
    assert sha(report_path.read_bytes())==actual['report_sha256'] and report['ROM_sha256']==release['candidate_sha256']
    ram_row = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==11000)
    raw_path = Path(ram_row['path'])
    raw = raw_path.read_bytes()
    assert len(raw)==0x400000 and sha(raw)==ram_row['sha256']
    image = CAP/'frame_011000_navigation.png'
    picture = next(r for r in report['frames_captured'] if r['frame']==11000)
    assert sha(image.read_bytes())==picture['PNG_sha256']
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.skipdata = True
    spans = [(0x72000,0x72368),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0x82428,0x82570)]
    preserved = []
    for lo,hi in spans:
        assert arm[lo:hi]==source[lo:hi]
        preserved.append({'span':[BASE+lo,BASE+hi],'sha256':sha(source[lo:hi]),
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
                for i in md.disasm(source[lo:hi],BASE+lo)]})
    assert list(struct.unpack_from('<8I',source,TABLE-BASE))==IDS
    assert arm[TABLE-BASE:TABLE-BASE+32]==source[TABLE-BASE:TABLE-BASE+32]
    literals = {BASE+o for o in range(0,len(source)-4,4) if struct.unpack_from('<I',source,o)[0]==TABLE}
    callers = []
    for offset in range(0,0x130000,4):
        word = struct.unpack_from('<I',source,offset)[0]
        if word&0x0F7F0000==0x051F0000:
            literal = BASE+offset+8+(word&4095)*(1 if word&0x00800000 else -1)
            if literal in literals:
                callers.append(BASE+offset)
    assert callers==[0x02072168]
    assert next(md.disasm(source[0x7216C:0x72170],0x0207216C)).op_str=='r0, #1'
    assert next(md.disasm(source[0x72170:0x72174],0x02072170)).op_str=='#0x2053d44'
    cpu,get = get_machine(arm,raw)
    actors,fleets,captain = get(0xCB184),get(0xCB1A8),get(0x7F244)
    choices = []
    for identity in range(207):
        if identity==captain:
            continue
        actor = actors+4+32*identity
        voice = get(0x7E988,actor)
        assert get(0x7EE08,actor)==identity and 0<=voice<8
        number = get(0x53F4C,actor,TABLE)
        assert number==2130+voice
        choices.append({'existing_actor_ID':identity,'actor_object':actor,'source_voice':voice,'message_ID':number})
    assert len(choices)==206 and {r['source_voice'] for r in choices}==set(range(8))
    identity = get(0x82478,fleets+0x2090,1)
    assert identity==16 and get(0x82428,fleets+0x2090,1)==0
    actor = actors+4+identity*32
    assert get(0x7E988,actor)==1 and get(0x53F4C,actor,TABLE)==2131
    owner,wrapped = [struct.unpack_from('<I',arm,p)[0] for p in [0x552A0,0x54450]]
    assert raw[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]==en[2131].text
    formatted = raw[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0]
    assert formatted==en[2131].text==b'Admiral, victory is ours!'
    records = []
    for number in range(2128,2140):
        records.append({'message_id':number,'selected_for_review':number in IDS,
            'source_reference':{k:v for k,v in asdict(jp[number]).items() if k!='text'},
            'source_hex':jp[number].text.hex(),'source_Japanese':jp[number].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[number]).items() if k!='text'},
            'current_text_hex':en[number].text.hex(),'current_English':en[number].text.decode('cp932')})
    assert jp[2132].text.count(b'IC')==1 and 'ICたち' in jp[2132].text.decode('cp932')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_and_original_victory_context.json',{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_table':TABLE,'raw8_voice_table':IDS,'original_literal_load':callers[0],
        'original_call':0x02072170,'original_entry':0x02053D44,'original_parent':0x02053DB8,
        'original_role':1,'selector_stack_offset':0x27C,'all206_existing_actor_choices':choices,
        'unchanged_clean_code_spans':preserved,'records_and_immediate_neighbors':records,
        'original_context':'Original battle result processing calls role1 First Mate and table02117EE0 to announce our victory. Earlier actual V1364 wins after a flagship capture;do not imply that every enemy ship was destroyed or every enemy crew member died.',
        'source2132_pronoun_note':'Genuine IC first-person command plus plural tachi means our collective victory. Idiomatic English uses we;it is not a personal name. Compare earlier source1561 IC-ra to our ship,documented in gunnery_deck_editorial_manuscript_v2.',
        'prior_actual_2131':{'frame':11000,'capture':str(image),'capture_sha256':sha(image.read_bytes()),
            'snapshot':str(raw_path),'snapshot_sha256':sha(raw),'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
            'existing_logical_FirstMate_actor_ID':16,'physical_FirstMate_slot_empty':True,'source_voice':1,
            'compiled_hex':en[2131].text.hex(),'native_formatted_hex':formatted.hex(),
            'visually_reviewed_Gerhard_portrait_complete_single_line_and_A_prompt':True,
            'earlier_actual_context_not_new_font_or_scene_completion_credit':True},
        'native_argument_count':0,'no_new_source_prose_formatting_or_completion_credit_yet':True,
        'no_actor_identity_RNG_result_or_live_fixture_changes':True,'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    print('Eight victory reports mapped:clean Japanese,one original role1 caller,206 voice choices,actual Gerhard2131 and genuine IC plural. No editorial credit yet.',flush=True)


if __name__=='__main__':
    main()
