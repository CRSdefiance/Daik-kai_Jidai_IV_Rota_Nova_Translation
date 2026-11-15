"""75 connected aftermath lines; original town exchange and caller frames.

CPU research only. Event prefixes stop before outcomes; audio/UI construction
and successful file I/O are explicit boundaries. No emulator state is changed.
"""
from pathlib import Path
from dataclasses import asdict
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR,UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_special_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.research_battle_aftermath_inventory_v1247 import TABLES as PREVIOUS_TABLES
from scripts.probe_escape_direct_source_v1186 import machine as portrait_machine
from scripts.verify_personal_gameplay_v841 import get_machine,rtti
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_aftermath_context_v1248')
BASE=0x02000000
TABLES=(*PREVIOUS_TABLES,('battle_withdrawal',0x02117D00,2114,2122),
        ('own_flagship_defeat',0x02117F00,2138,2146))
IDS=(*range(1994,2052),*range(2114,2122),*range(2138,2146),2192)
REGS=(UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)


def source_prefix(arm,raw,entry,args,end):
    cpu,get=get_machine(arm,raw);calls=[]
    def observe(u,pc,size,unused):
        if pc==end:
            u.emu_stop();return
        if pc==BASE+0x1097DC:
            u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR));return
        calls.append({'entry':pc,'original_return':u.reg_read(UC_ARM_REG_LR),
                      'arguments':[u.reg_read(r) for r in REGS]})
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    for pc in (BASE+0x1097DC,BASE+0x53F0C,BASE+0x53D44,BASE+0x53FE4,end):
        cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
    for reg,value in zip(REGS,args):cpu.reg_write(reg,value)
    cpu.emu_start(BASE+entry,STOP,count=100000)
    assert cpu.reg_read(UC_ARM_REG_PC)==end
    return calls,cpu,get


def consumer(arm,common,raw,entry,actor_or_role,key,argument=0):
    cpu,get,provider=portrait_machine(arm,common,raw,{'patches':[]});seen={}
    def observe(u,pc,size,unused):
        if pc==BASE+0x5408C:
            u.reg_write(UC_ARM_REG_PC,BASE+0x54144)
        elif pc==0x01FFCF3C:
            sp=u.reg_read(UC_ARM_REG_SP)
            parent=struct.unpack('<I',u.mem_read(sp+0x264,4))[0]
            off=0x27C if entry==0x53D44 else 0x274
            seen.update(saved_parent=parent,saved_selector_offset=off,
                saved_selector=struct.unpack('<I',u.mem_read(sp+off,4))[0],
                input_hex=bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1),512)).split(b'\0')[0].hex(),
                output=u.reg_read(UC_ARM_REG_R0))
        else:
            seen['formatted_hex']=bytes(u.mem_read(seen['output'],512)).split(b'\0')[0].hex()
            u.emu_stop()
    for pc in (BASE+0x5408C,0x01FFCF3C,BASE+0x54164):
        cpu.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)
    cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
    for reg,value in zip(REGS,(actor_or_role,key,argument,0)):cpu.reg_write(reg,value)
    cpu.emu_start(BASE+entry,STOP,count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x54164
    parent={0x53D44:0x02053DB8,0x53F0C:0x02053F40,0x53FE4:0x02054014}[entry]
    assert seen['saved_parent']==parent and seen['saved_selector']==key
    return {**seen,'original_entry':BASE+entry,'file_reads':provider.reads,
        'original_lookup_loader_printf_macro_and_formatter_execute':True,
        'UI_constructor_and_successful_file_IO_are_CPU_boundaries_not_actual_gameplay':True}


def main():
    assert not ROOT.exists()
    current_path=Path('out/all_routes_combined_v1224_candidate.nds');rom=NdsImage.open(current_path)
    clean=NdsImage.open('work/clean.nds');arm=rom.read_file('/__arm9__.bin');source=clean.read_file('/__arm9__.bin')
    common=rom.read_file('/COMMON/MESFILE.DK4');en=current_entries(common,arm)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    prior_path=Path('work/analysis/battle_aftermath_source_v1247/source_context_inventory.json');prior=read(prior_path)
    assert sha(current_path.read_bytes())==prior['current_ROM_sha256'] and sha(arm)==prior['current_ARM9_sha256']
    snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224/frame_005770_arm9_ram.bin')
    raw=snapshot.read_bytes();cpu,get=get_machine(arm,raw)
    for lo,hi in ((0x53D44,0x54170),(0x71968,0x71A40),(0x717F8,0x718D4),
                  (0x72368,0x723C4),(0xB2B60,0xB2C08),(0x7251C,0x7257C)):
        assert arm[lo:hi]==source[lo:hi]
    actor_root,fleet_root,town_root=get(0xCB184),get(0xCB1A8),get(0xCB178)
    objects=[actor_root+4+i*32 for i in range(207)]+[actor_root+0x19E4]
    role_ID=get(0x82478,fleet_root+0x2090,1)
    role_actor=actor_root+0x19E4 if role_ID==get(0x7F244) else actor_root+4+role_ID*32
    assert get(0x7EE08,role_actor)==role_ID==18
    tables=list(prior['voice_tables']);new_tables=[]
    for family,table,first,end in TABLES[-2:]:
        assert arm[table-BASE:table-BASE+32]==source[table-BASE:table-BASE+32]
        values=struct.unpack_from('<8i',source,table-BASE)
        assert values==tuple(range(first,end));choices=[]
        for slot,obj in enumerate(objects):
            n=get(0x53F4C,obj,table);voice=get(0x7E988,obj)
            assert n==values[voice]
            choices.append({'actor_slot':slot,'actor_ID':get(0x7EE08,obj),'actor_object':obj,'voice_class':voice,'message_ID':n})
        assert {r['message_ID'] for r in choices}==set(range(first,end))
        new_tables.append({'family':family,'table':table,'native_message_IDs':list(range(first,end)),
            'source_eight_signed_members':list(values),'all208_original_selections':choices,
            'null_actor_original_fallback':get(0x53F4C,0,table)})
    tables+=new_tables
    assert sum(len(t['all208_original_selections']) for t in tables)==2288
    town_cases=[]
    for index in range(115):
        town=town_root+4+index*108;vtable=struct.unpack('<I',cpu.mem_read(town,4))[0]
        assert rtti(raw,vtable)=='5CTown'
        name_getter=struct.unpack('<I',cpu.mem_read(vtable+8,4))[0]
        name_pointer=get(name_getter-BASE,town)
        name=bytes(cpu.mem_read(name_pointer,96)).split(b'\0')[0]
        speaker=get(0xB2B60,town)
        assert speaker
        calls,pcpu,pget=source_prefix(arm,raw,0x71968,(0,town),BASE+0x719F8)
        assert [(r['entry'],r['arguments'][1]) for r in calls]==[
            (BASE+0x53F0C,0x021177E0),(BASE+0x53FE4,2192),(BASE+0x53F0C,0x02117640)]
        assert [r['arguments'][0] for r in calls]==[role_actor,speaker,role_actor]
        assert calls[-1]['arguments'][2]==name_pointer
        town_cases.append({'town_index':index,'town_object':town,'native_RTTI':'5CTown',
            'native_name_getter':name_getter,'town_name_pointer':name_pointer,'town_name_hex':name.hex(),
            'town_name':name.decode('cp932'),'native_town_speaker_actor_ID':get(0x7EE08,speaker),
            'original_calls':calls,'entire_original_surrender_exchange_prefix_executes':True,
            'no_emulator_or_real_town_surrender_claim':True})
    branch_cases=[]
    for entry,end,expected in ((0x72368,BASE+0x723C4,(0x02117740,0x021176A0,0x02117900)),
                               (0x717F8,BASE+0x718D4,(0x02117760,0x021176E0,0x02117D00))):
        for mode,table in enumerate(expected):
            calls,_,_=source_prefix(arm,raw,entry,(0,mode),end)
            assert calls[0]['entry']==BASE+0x53D44 and calls[0]['arguments'][:2]==[1,table]
            if entry==0x717F8 and mode in (0,1):
                assert len(calls)==2 and calls[1]['arguments'][:2]==[1,0x02117F00]
            else:assert len(calls)==1
            branch_cases.append({'original_entry':BASE+entry,'source_mode':mode,'calls':calls,
                'prefix_stops_before_event_outcomes_CPU_only':True})
    records=[]
    for family,table,first,end in TABLES:
        for n in range(first,end):
            records.append({'message_ID':n,'source_family':family,'source_voice_table':table,
                'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},
                'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
                'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},
                'current_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932'),
                'native_argument_kind':'original-town-name' if first==1994 else 'none',
                'native_argument_count':1 if first==1994 else 0})
    n=2192
    records.append({'message_ID':n,'source_family':'town_white_flag_reply','source_numeric_call':BASE+0x719B0,
        'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},'source_hex':jp[n].text.hex(),
        'source_Japanese':jp[n].text.decode('cp932'),
        'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},'current_hex':en[n].text.hex(),
        'current_English':en[n].text.decode('cp932'),'native_argument_count':0,'native_argument_kind':'none'})
    assert len(records)==len({r['message_ID'] for r in records})==75
    name_pointer=town_cases[0]['town_name_pointer'];name=bytes.fromhex(town_cases[0]['town_name_hex'])
    pipelines=[]
    for family,table,first,end in TABLES:
        case=consumer(arm,common,raw,0x53D44,1,table,name_pointer)
        n=get(0x53F4C,role_actor,table)
        assert case['input_hex']==en[n].text.replace(b'%s',name).hex()
        pipelines.append({'message_ID':n,'family':family,'source_role':1,'source_actor_ID':18,**case})
    # Every voice alternative also executes the direct original consumer, with
    # existing actor objects. No actor ID is rewritten in this CPU-only binding.
    for t in tables:
        representatives={}
        for c in t['all208_original_selections']:representatives.setdefault(c['message_ID'],c['actor_object'])
        for n,actor in representatives.items():
            case=consumer(arm,common,raw,0x53F0C,actor,t['table'],name_pointer)
            assert case['input_hex']==en[n].text.replace(b'%s',name).hex()
            pipelines.append({'message_ID':n,'family':t['family'],'source_actor_ID':get(0x7EE08,actor),**case})
    speaker=get(0xB2B60,town_root+4)
    case=consumer(arm,common,raw,0x53FE4,speaker,2192)
    assert case['input_hex']==en[2192].text.hex()
    pipelines.append({'message_ID':2192,'family':'town_white_flag_reply','source_actor_ID':get(0x7EE08,speaker),**case})
    assert len(pipelines)==86
    ROOT.mkdir(parents=True)
    proof=ROOT/'source_context_and_consumer_frames.json'
    save(proof,{'source_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'current_ROM':str(current_path),'current_ROM_sha256':sha(current_path.read_bytes()),
        'current_COMMON_sha256':sha(common),'current_ARM9_sha256':sha(arm),
        'snapshot':str(snapshot),'snapshot_sha256':sha(raw),
        'supersedes_inventory':str(prior_path),'supersedes_inventory_sha256':sha(prior_path.read_bytes()),
        'native_message_IDs':list(IDS),'records':records,'voice_tables':tables,
        'prior1872_and_new416_native_voice_selections':2288,
        'all115_original_town_surrender_exchange_prefixes':town_cases,
        'town_name_placeholder_type_confirmed_by_original_caller_CB178_stride108_RTTI_and_virtual_getter':True,
        'six_original_outcome_branch_prefixes':branch_cases,'original_consumer_pipelines':pipelines,
        'source_role1_actor_ID_in_this_snapshot':18,
        'role_frame':[0x02053DB8,0x27C],'direct_frame':[0x02053F40,0x274],
        'numeric_reply_frame':[0x02054014,0x274,2192],
        'city_defense_and_ship_surrender_enclosing_callers_require_additional_binding':True,
        'no_new_prose_native_format_approval_ROM_or_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1260 and ledger['records_with_source_and_prose_pass']==1298
    ledger['next_battle_aftermath_context_v1248']={'proof':str(proof),'native_message_IDs':list(IDS),
        'source_records':75,'native_voice_choices':2288,'consumer_pipelines':86,
        'source_and_prose_review_not_yet_counted':True,'completed_entries':0}
    save('translations/editorial_review_current_v1.json',ledger)
    print('75 connected source records;115 town exchanges,2288 voice choices,86 original consumer/frame pipelines pass;no prose credit.',flush=True)


if __name__=='__main__':main()
