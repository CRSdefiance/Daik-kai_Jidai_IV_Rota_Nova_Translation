"""B23's shipped EV2 category, completed-event dependency and exact predicates."""
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_lessons_research_v1739 import ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_crew_trigger_v1751')
SNAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lessons_revised_v1741_RESEARCH_ONLY/final_arm9_ram.bin')
SCRATCH=0x02640000

if __name__=='__main__':
    assert not ROOT.exists()
    rom=NdsImage.open(ROM); clean=NdsImage.open('work/clean.nds')
    arm=rom.read_file('/__arm9__.bin'); original=clean.read_file('/__arm9__.bin')
    ev=rom.read_file('/data/EV2.DK4'); assert ev==clean.read_file('/data/EV2.DK4')
    ranges=[(0x21EAC,0x22E98),(0x23840,0x23A28),(0x24ADC,0x24C24),(0x25490,0x257C0),
            (0x2A690,0x2AAF8),(0x90E14,0x90E50)]
    assert all(arm[a:b]==original[a:b] for a,b in ranges)
    body=ev[96:]; counts=struct.unpack_from('<9H',ev,10); starts=struct.unpack_from('<9I',ev,40)
    events=[]
    for category,count in enumerate(counts):
        offset=starts[category]
        for local in range(count):
            words=struct.unpack_from('<2I',body,offset); length=(words[1]&255)*4
            assert length>=8
            events.append({'id':len(events),'category':category,'local':local,'body_offset':offset,
                'source_hex':body[offset:offset+length].hex(),'source_bytes':length,'action_index':(words[0]>>16)&0x3FFF})
            offset+=length
        assert offset==struct.unpack_from('<I',ev,44+category*4)[0]
    assert len(events)==336
    event=events[23]; assert event['category']==5 and event['body_offset']==428 and event['action_index']==24
    action_begin=struct.unpack_from('<I',ev,0x4C)[0]
    action=struct.unpack_from('<H',body,action_begin+event['action_index']*2)[0]
    assert action==0x2017
    current=SNAP.read_bytes(); assert len(current)==0x400000
    header=current.find(ev[:96]); assert header>=0 and current.find(ev[:96],header+1)<0
    owner=0x02000000+header-0x34; cpu,get=get_machine(arm,current)
    pointers={}
    for spec in events:
        get(0x23888,SCRATCH,owner+4,spec['id'])
        pointer=struct.unpack('<I',cpu.mem_read(SCRATCH,4))[0]
        assert pointer==0x02000000+header+96+spec['body_offset']
        loaded=bytes(cpu.mem_read(pointer,spec['source_bytes'])); source=bytes.fromhex(spec['source_hex'])
        assert loaded[4:]==source[4:]
        assert (struct.unpack_from('<I',loaded)[0]^struct.unpack_from('<I',source)[0])&~0xC0008000==0
        pointers[spec['id']]=pointer
    completed=get(0x23840,owner+4,120); assert completed==1
    assert bytes.fromhex(event['source_hex'])[8:12]==struct.pack('<2H',0x0100,120)
    conditions_offset=struct.unpack_from('<I',ev,0x54)[0]
    condition_rows=[]
    for condition,compare,wanted in [(15,0,0),(14,1,1)]:
        pointer=0x02000000+header+96+conditions_offset+condition*4
        word=struct.unpack_from('<I',body,conditions_offset+condition*4)[0]
        cpu.mem_write(SCRATCH,struct.pack('<2I',0x021343F8,pointer))
        value=get(0x256A0,SCRATCH)
        accepted=get(0x2A690,value,compare)
        assert value==wanted and accepted==1
        condition_rows.append({'condition_id':condition,'source_word':word,'native_value':value,
            'comparison_category':compare,'native_comparison_pass':True})
    assert [r['source_word'] for r in condition_rows]==[0x91020002,0x3000FE09]
    fleet_index=get(0x2E58C); assert fleet_index==get(0x7F244)==2
    fleet=get(0xCB1A8)+4+fleet_index*132
    assert get(0x34674,fleet)==0x73
    assert get(0x2A82C,2)==2
    assert bytes(cpu.mem_read(0x02000000,0x400000))==current
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM); code=[]
    for lo,hi in [(0x2235C,0x22430),(0x24B60,0x24B9C),(0x25538,0x25588),(0x90E14,0x90E50)]:
        code.extend({'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(arm[lo:hi],0x02000000+lo))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_bound_B23_trigger_and_original_predicates.json', {
        'research_ROM':str(ROM),'research_ROM_sha256':sha(ROM.read_bytes()),'EV2_sha256':sha(ev),
        'snapshot':str(SNAP),'snapshot_sha256':sha(current),'actual_EV2_owner':owner,
        'all336_original_native_event_getters_match_independent_table_walk':True,
        'runtime_EV2_differs_only_in_original_event_state_bits':True,
        'B23_event':event,'native_action_word':action,'required_completed_event120_actual_true':True,
        'native_condition_cases':condition_rows,
        'condition15':'Original type9/subtype1 resolves fleet2 and asks whether its current town equals Amsterdam2;comparison category0 requires false.',
        'condition14':'Original type3/FE queries actor9 through7DB14;comparison category1 requires true. The actual actor is Camille and is present.',
        'actual_sea_town_sentinel':0x73,'event_category':5,
        'source_category5_caller':'Original090E14-090E4C reads active fleet town byte3C,constructs23260 category5 andpasses original21D0C. Actual source category5 entry remains to exercise.',
        'no_direct_Deck_View_trigger_or_specific_Bruges_requirement_in_this_record':True,
        'original_source_instructions':code,'original_ARM9_ranges_exact_to_clean':ranges,
        'all_input4MiB_preserved_getters_only_no_RNG_event_flag_or_eligibility_override':True,
        'next':'Use an isolated location-only water approach to Bruges,then ordinary A docking/category5 handling. Do not set town/event-completion fields.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('B23 is category5/action24->SC2B23:completed120,not docked in Amsterdam2,Camille present. Both predicates pass actual sea state;ordinary category5 entry still needed.')
