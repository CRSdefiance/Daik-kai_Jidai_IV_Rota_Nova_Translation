"""Exact original voice dispatch,roles and distinct name-argument consumers."""
import struct
import unicodedata
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

BASE=0x02000000
ROOT=Path('work/analysis/reinforcement_sniping_v1022b')
ROM=Path('out/all_routes_combined_v997_candidate.nds')
SNAPSHOT=Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_declaration_v1018_997_KnownJanus/frame_006360_arm9_ram.bin')
TABLES={'reinforcement':(0x021173E0,(1911,-1,1912,-1,1913,1914,1915,1916),1),
        'covering_fire':(0x021173C0,(1917,1918,1919,-1,1920,1921,1922,1923),1),
        'admiral_shot':(0x02117300,(1924,-1,1925,1926,1927,1928,1929,1930),7)}
REPS={0:4,1:16,2:9,3:7,4:5,5:6,6:14,7:19}
TEXT,SHIM,TAIL=0x02465000,0x02470000,0x02470100


def ptr(cpu,address):return struct.unpack('<I',cpu.mem_read(address,4))[0]
def string(cpu,address):return bytes(cpu.mem_read(address,512)).split(b'\0')[0]


def assign(cpu,get,actor,role):
    controller=get(0xCB1A8)+0x2090;model=get(0x82E04,controller)
    room=get(0x7B60,role);slot=12 if role==1 else 3
    assert room==(6 if role==1 else 1)
    before=bytes(cpu.mem_read(BASE,0x400000))
    for i in range(31):
        if get(0x132C0,model,i)==room or get(0x82BC4,controller,i)==actor:
            cpu.mem_write(controller+6+i,b'\xD0')
    cpu.mem_write(model+0x1E+slot,bytes([room]));cpu.mem_write(controller+6+slot,bytes([actor]))
    selected=get(0x82478,controller,role);assert selected==actor
    after=bytes(cpu.mem_read(BASE,0x400000))
    changes=[{'address':BASE+i,'before':a,'after':b} for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]
    assert all(controller+6<=c['address']<controller+37 or c['address']==model+0x1E+slot for c in changes)
    return {'actor_ID':actor,'role':role,'room':room,'slot':slot,'selected_actor':selected,
            'only_CPU_assignment_fields_changed':changes,'no_actual_gameplay_or_earned_assignment':True}


def bridge(cpu,japanese,events):
    selected=[None]
    def loader(u,pc,size,unused):
        n=u.reg_read(UC_ARM_REG_R0);assert n in range(1911,1931)
        selected[0]=n;u.mem_write(TEXT,japanese[n].text+b'\0')
        u.reg_write(UC_ARM_REG_R0,TEXT);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    def popup(u,pc,size,unused):
        kind,actor,message,args=[u.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)]
        n=selected[0];assert message==TEXT and string(u,message)==japanese[n].text
        count=japanese[n].text.count(b'%s');assert count in (0,1)
        arguments=[ptr(u,args+4*i) for i in range(count)]
        events.append({'message_ID':n,'kind':kind,'actor_object':actor,
            'source_text_hex':japanese[n].text.hex(),'argument_pointers':arguments,
            'argument_hex':[string(u,p).hex() for p in arguments],
            'wrapper_return_parent':u.reg_read(UC_ARM_REG_LR)})
        u.reg_write(UC_ARM_REG_R0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    return [cpu.hook_add(UC_HOOK_CODE,loader,begin=BASE+0x5528C,end=BASE+0x5528C),
            cpu.hook_add(UC_HOOK_CODE,popup,begin=BASE+0x54058,end=BASE+0x54058)]


def fragment(arm,raw,japanese,family,actor,object_address,source_start,source_end):
    cpu,get=get_machine(arm,raw)
    role=TABLES[family][2];fixture=assign(cpu,get,actor,role)
    if family=='reinforcement':setup=f'ldr r7,={object_address}; mov r4,#1; '
    elif family=='covering_fire':setup=f'ldr r8,={object_address}; '
    else:setup=''
    ks=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    code=bytes(ks.asm('push {r4-r10,lr}; '+setup+f'b {source_start}',SHIM)[0])
    cpu.mem_write(SHIM,code);cpu.mem_write(TAIL,bytes(ks.asm('pop {r4-r10,pc}',TAIL)[0]))
    events=[];hooks=bridge(cpu,japanese,events)
    def end(u,pc,size,unused):u.reg_write(UC_ARM_REG_PC,TAIL)
    hooks.append(cpu.hook_add(UC_HOOK_CODE,end,begin=source_end,end=source_end))
    try:call(cpu,SHIM-BASE,(),instruction_limit=2000000)
    finally:
        for h in hooks:cpu.hook_del(h)
    assert len(events)==1 and events[0]['kind']==0
    event=events[0];obj=get(0xCB184)+4+actor*32
    assert event['actor_object']==obj
    event.update(family=family,CPU_assignment=fixture,original_fragment=[source_start,source_end],
                 complete_original_speech_wrapper_and_ABI=True,only_loader_and_UI_boundary_bridged=True,
                 not_full_branch_eligibility_or_actual_scene=True)
    return event


def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1199
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    rom,clean=map(NdsImage.open,(ROM,'work/clean.nds'));arm,source=[r.read_file('/__arm9__.bin') for r in (rom,clean)]
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    raw=SNAPSHOT.read_bytes();report_path=SNAPSHOT.parent/'capture_report.json';report=read(report_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and report['ROM_sha256']==sha(ROM.read_bytes())
    snap=next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==6360)
    assert snap['sha256']==sha(raw)
    spans=((0x53D44,0x53DCC),(0x53F4C,0x53FE4),(0x7E988,0x7E9A0),
           (0x36914,0x369D0),(0x70BF8,0x71088),(0x774BC,0x7777C),
           (0x7777C,0x77A58),(0x73B18,0x73C10),(0x82478,0x825E4))
    dis=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    source_code=[]
    for lo,hi in spans:
        assert arm[lo:hi]==source[lo:hi]
        source_code.append({'start':BASE+lo,'end':BASE+hi,'sha256':sha(source[lo:hi]),
            'disassembly':[f'{x.address:08X} {x.mnemonic} {x.op_str}' for x in dis.disasm(source[lo:hi],BASE+lo)]})
    save(ROOT/'original_source_fragments.json',source_code)
    cpu,get=get_machine(arm,raw);actors,companies,fleets=get(0xCB184),get(0xCB160),get(0xCB1A8)
    captain=get(0x7F244);assert captain==1
    dispatch=[];nulls=[]
    for family,(table,ids,role) in TABLES.items():
        assert tuple(struct.unpack_from('<8i',source,table-BASE))==ids
        for actor in range(208):
            obj=actors+0x19E4 if actor==captain else actors+4+actor*32
            voice=get(0x7E988,obj);assert 0<=voice<8
            n=get(0x53F4C,obj,table);expected=ids[voice] if ids[voice]!=-1 else next(n for n in ids if n!=-1)
            assert n==expected
            dispatch.append({'family':family,'actor_ID':actor,'voice':voice,'message_ID':n,'source_minus1_fallback':ids[voice]==-1})
        n=get(0x53F4C,0,table);assert n==ids[0];nulls.append({'family':family,'null_actor_ID':n})
    assert len(dispatch)==624 and {r['message_ID'] for r in dispatch}==set(range(1911,1931))
    wrappers=[]
    for family,(table,ids,role) in TABLES.items():
        for voice,actor in REPS.items():
            u,g=get_machine(arm,raw);fixture=assign(u,g,actor,role);events=[];hooks=bridge(u,jp,events)
            try:call(u,0x53D44,(role,table,TEXT+0x300) if family!='admiral_shot' else (role,table),instruction_limit=2000000)
            finally:
                for h in hooks:u.hook_del(h)
            assert len(events)==1
            n=ids[voice] if ids[voice]!=-1 else ids[0]
            assert events[0]['message_ID']==n and events[0]['actor_object']==actors+4+actor*32
            wrappers.append({'family':family,'voice':voice,'fixture':fixture,'original_wrapper':events[0]})
    company_names=[];reinforcement=[]
    for company_id in range(20):
        obj=companies+4+company_id*76;fn=ptr(cpu,ptr(cpu,obj)+8)
        value=string(cpu,get(fn-BASE,obj))
        company_names.append({'company_ID':company_id,'object':obj,'name_hex':value.hex(),
            'name':unicodedata.normalize('NFKC',value.decode('cp932')),'original_name_getter':fn})
        for start,end in ((0x020775EC,0x0207760C),(0x020778D4,0x020778F4)):
            proof=fragment(arm,raw,jp,'reinforcement',4,obj,start,end)
            assert proof['argument_hex']==[value.hex()]
            reinforcement.append({'company_ID':company_id,'proof':proof})
    commanders=[];cover=[]
    for index in range(63):
        obj=fleets+4+index*132;actor_obj=get(0x3697C,obj)
        if not actor_obj:continue
        fn=ptr(cpu,ptr(cpu,actor_obj)+0x20);value=string(cpu,get(fn-BASE,actor_obj))
        name=unicodedata.normalize('NFKC',value.decode('cp932'))
        commanders.append({'fleet_ID':index,'object':obj,'commander_object':actor_obj,'name_hex':value.hex(),
            'name':name,'original_name_getter':fn,'player_faction':get(0x36914,obj),
            'active_player_fleet':get(0x36948,obj)})
        proof=fragment(arm,raw,jp,'covering_fire',4,obj,0x02070E4C,0x02070E70)
        assert proof['argument_hex']==[value.hex()]
        cover.append({'fleet_ID':index,'proof':proof})
    shot=fragment(arm,raw,jp,'admiral_shot',4,0,0x02073BA0,0x02073BAC)
    assert shot['argument_hex']==[] and shot['message_ID']==1924
    proof={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_snapshot':snap,'source_capture_report':str(report_path),'source_capture_report_sha256':sha(report_path.read_bytes()),
        'tables':{k:{'address':v[0],'voice_IDs':list(v[1]),'speaker_role':v[2]} for k,v in TABLES.items()},
        'all624_actor_voice_selections':dispatch,'all3_null_controls':nulls,'all24_original_role_wrapper_cases':wrappers,
        'all20_native_complete_company_labels':company_names,'all_original_reinforcement_argument_fragments':reinforcement,
        'all_nonnull63_fleet_commander_labels':commanders,'all_original_covering_fire_argument_fragments':cover,
        'original_sniping_fragment':shot,
        'reinforcement_substitution_is_complete_faction_label_not_leader_first_name':True,
        'covering_fire_substitution_is_fleet_commanders_native_full_name_not_faction':True,
        'covering_fire_source_scan_requires_other_player_faction_fleet_and_original_join_predicates':True,
        'sniping_speaker_is_role7_Lookout_and_critical_chance_uses_role7_stat6_greater_than150':True,
        'source_rng2000_comparison_against_stat_divided_by10_and_original_outcome_after_message_not_overridden':True,
        'source_call_predecessor_reinforcement_notice_table':{'address':0x02118560,'IDs':list(range(614,622)),
            'text':[{ 'id':n,'japanese':jp[n].text.decode('cp932'),'hex':jp[n].text.hex()} for n in range(614,622)]},
        'original_source_fragments':str(ROOT/'original_source_fragments.json'),
        'no_ROM_live_fixture_or_outcome_changes':True,'not_actual_scene_or_complete_branch_eligibility_proof':True,
        'source_prose_or_completed_entry_credit_added':0,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'source_context_packet.json',proof)
    print('624 voice selections,24 original role wrappers,40 company argument fragments,'+str(len(cover))+' commander arguments and original Lookout shot fragment pass. No actual-scene or prose credit.',flush=True)


if __name__=='__main__':main()
