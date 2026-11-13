"""Original ceremony speakers,selections,site and result arguments;no ROM edits."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.inn_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ceremony_context_v806')
ROM=Path('out/all_routes_combined_v803_candidate.nds')
RAM=Path('E:/Rota Nova translations/Generated/work/emulation_v193/inn_v803_stays/frame_003200_arm9_ram.bin')
TABLES={0x02116480:(1238,1239,1240,1241),0x02116590:(1205,-1,1206,-1),
    0x021165F0:(1228,-1,1229,-1),0x02116700:(1208,-1,1209,-1),
    0x02116750:(1211,1212,1213,1214),0x021167B0:(1216,-1,1217,-1),
    0x02116830:(1223,-1,1224,-1),0x02116840:(1233,1234,1235,1236)}
IDS=tuple(sorted({64,289,290,291,293,294,295,*range(1200,1245)}))


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    r=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds')
    arm=r.read_file('/__arm9__.bin');jp_arm=clean.read_file('/__arm9__.bin');raw=RAM.read_bytes()
    assert sha(ROM.read_bytes())=='7c6c8bb3c89973af2f789488e51bff395d871be6a461490d62b3f5c8d860daad'
    spans=((0x53BD8,0x53CB0),(0x546B8,0x546F8),(0x610FC,0x61C18),(0x7EB0C,0x7EB3C))
    assert all(arm[a:b]==jp_arm[a:b] for a,b in spans)
    assert struct.unpack_from('<2I',jp_arm,0x61C10)==(0x92492493,28)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),jp_arm)
    en=current_entries(r.read_file('/COMMON/MESFILE.DK4'),arm)
    u=machine(arm);u.mem_write(BASE,raw)
    def get(fn,args=()):call(u,fn,args,instruction_limit=300000);return u.reg_read(UC_ARM_REG_R0)
    def ptr(p):return struct.unpack('<I',u.mem_read(p,4))[0]
    def text(p):return bytes(u.mem_read(p,512)).split(b'\0')[0]
    def name(ob):return text(get(ptr(ptr(ob)+8)-BASE,(ob,)))
    actor_root=get(0xCB184);town_root=get(0xCB178);site_root=get(0xCB16C)
    hero_at=struct.unpack_from('<I',arm,0x7F250)[0]+0x48
    facility_at=struct.unpack_from('<I',arm,0x61870)[0]+0x10
    hero_names=[]
    for i in range(4):
        ob=actor_root+4+i*32;record=get(0x7EB24,(ob,));p=struct.unpack_from('<I',jp_arm,record-BASE)[0]
        hero_names.append(dict(index=i,Japanese=jp_arm[p-BASE:].split(b'\0')[0].decode('cp932'),current_name=name(ob).decode('ascii'),source_name_record=record))
    assert [h['Japanese'] for h in hero_names]==['ラファエル','ホドラム','リル','マリア']
    selections=[];selection={}
    for table,values in TABLES.items():
        assert tuple(struct.unpack_from('<4i',arm,table-BASE))==values and arm[table-BASE:table-BASE+16]==jp_arm[table-BASE:table-BASE+16]
        for hero in range(4):
            u.mem_write(hero_at,struct.pack('<I',hero));assert get(0x7F244)==hero
            selected=get(0x53C6C,(table,));expected=values[hero] if values[hero]!=-1 else next(n for n in values if n!=-1)
            assert selected==expected
            selection[table,hero]=selected;selections.append(dict(table=table,hero_index=hero,selected_message=selected,native_fallback_to_first_valid=values[hero]==-1))
    u.mem_write(BASE,raw)
    NPCs=[]
    for town_id in range(90):
        town=town_root+4+town_id*108
        for role in (9,10,11):
            actor=get(0xB2CD8,(town,role));i=get(0xB2D28,(town,role));assert actor and i!=208
            source_record=get(0x7EB24,(actor,));p=struct.unpack_from('<I',jp_arm,source_record-BASE)[0]
            NPCs.append(dict(town_ID=town_id,role=role,actor_ID=i,actor_pointer=actor,
                clean_name=jp_arm[p-BASE:].split(b'\0')[0].decode('cp932'),current_name=name(actor).decode('ascii'),source_name_record=source_record,
                inventory_not_claimed_all_town_facility_combinations_visitable=True))
    sites=[]
    for i in range(21):
        ob=site_root+4+i*8;sites.append(dict(index=i,object=ob,name_hex=name(ob).hex(),name=name(ob).decode('ascii')))
    assert sites[8]['name']=='Cappadocia'
    # Exercise the complete original hero wrapper to its IO/UI boundaries.
    wrapper=[];dummy=0x02470000;u.mem_write(dummy,b'CONTEXT_IO_ONLY\0');selected=[]
    def wrapper_IO(c,pc,size,data):
        if pc==BASE+0x5528C:
            selected.append(c.reg_read(UC_ARM_REG_R0));c.reg_write(UC_ARM_REG_R0,dummy)
        else:
            assert c.reg_read(UC_ARM_REG_R0)==0 and c.reg_read(UC_ARM_REG_R1)==actor_root+0x19E4
            assert c.reg_read(UC_ARM_REG_R2)==dummy
        c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
    hooks=[u.hook_add(UC_HOOK_CODE,wrapper_IO,begin=BASE+f,end=BASE+f) for f in (0x5528C,0x54058)]
    try:
        for table in TABLES:
            for hero in range(4):
                u.mem_write(hero_at,struct.pack('<I',hero));selected.clear();get(0x53BD8,(table,))
                assert selected==[selection[table,hero]]
                wrapper.append(dict(table=table,hero_index=hero,message=selected[0],speaker_actor=actor_root+0x19E4,original_return_parent=BASE+0x53C14,ABI_SP_LR_pass=True))
    finally:
        for h in hooks:u.hook_del(h)
    cases=[];window=0x02460000
    def run(fn,day,start,site,facility,hero,accept):
        u.mem_write(BASE,raw);u.mem_write(window,struct.pack('<2I',0,window+0x100))
        u.mem_write(hero_at,struct.pack('<I',hero));u.mem_write(facility_at,struct.pack('<I',facility))
        events=[]
        def observe(c,pc,size,data):
            regs=[c.reg_read(reg) for reg in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)]
            if pc in (BASE+0x53FE4,BASE+0x53F9C):
                n=regs[1];assert n in IDS
                args=[text(regs[2]).decode('cp932')] if jp[n].text.count(b'%s') else []
                assert len(args)==jp[n].text.count(b'%s')
                events.append(dict(kind='NPC_yes_no' if pc==BASE+0x53F9C else 'NPC_dialogue',message=n,speaker_actor=regs[0],arguments=args))
                c.reg_write(UC_ARM_REG_R0,int(accept) if pc==BASE+0x53F9C else 0)
            elif pc==BASE+0x53BD8:
                table=regs[0];assert table in TABLES
                events.append(dict(kind='protagonist_reaction',table=table,message=selection[table,hero],speaker_actor=actor_root+0x19E4,hero_index=hero,arguments=[]))
                c.reg_write(UC_ARM_REG_R0,0)
            elif pc==BASE+0x546B8:
                n=regs[0];assert n in IDS
                args=[text(regs[1]).decode('cp932')] if jp[n].text.count(b'%s') else []
                events.append(dict(kind='system_result_notice',message=n,speaker_actor=None,arguments=args,source_name_provider='custom admiral virtual+0x20' if args else None))
                c.reg_write(UC_ARM_REG_R0,0)
            else:
                events.append(dict(kind={BASE+0x1096F8:'action_animation_boundary',BASE+0x610FC:'crew_effect_boundary',BASE+0xB7630:'time_boundary'}[pc],source_callee=pc,R0_R1_R2_R3=regs))
                c.reg_write(UC_ARM_REG_R0,0)
            c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
        hooks=[u.hook_add(UC_HOOK_CODE,observe,begin=BASE+f,end=BASE+f) for f in (0x53FE4,0x53F9C,0x53BD8,0x546B8,0x1096F8,0x610FC,0xB7630)]
        try:
            get(fn,(window,day,start,site) if fn==0x61570 else (window,day,start))
        finally:
            for h in hooks:u.hook_del(h)
        case=dict(source_function=BASE+fn,day=day,ceremony_start_day=start,site_index=site,facility_role=facility,
            hero_index=hero,yes_no_input=accept,events=events,
            scope='Original branching/providers and supplied choices. UI,animation,crew-effect and time boundaries intercepted;not actual gameplay or outcome proof.')
        cases.append(case);return case
    for hero in range(4):
        for day in (24,25):run(0x619A0,day,day,8,9,hero,True)
        run(0x619A0,24,24,8,9,hero,False);run(0x619A0,23,24,8,9,hero,True)
        run(0x618E4,24,24,8,10,hero,True);run(0x618E4,24,24,8,10,hero,False);run(0x618E4,23,24,8,10,hero,True)
        for rite in range(5):
            day=4+rite;case=run(0x61570,day,day,8,11,hero,True)
            effect=next(e['R0_R1_R2_R3'][1] for e in case['events'] if e['kind']=='crew_effect_boundary')
            assert effect==3+rite
        run(0x61570,24,24,8,11,hero,False);run(0x61570,23,24,8,11,hero,True);run(0x61570,27,24,8,11,hero,True)
    for site in range(21):
        case=run(0x61570,24,24,site,11,1,False)
        question=next(e for e in case['events'] if e.get('message')==1219)
        assert question['arguments']==[sites[site]['name']]
    # Bind the real dispatcher to native day/site providers for every Town/type.
    u.mem_write(BASE,raw);parent_cases=[];active=[None]
    decoded=window+0x300;get(0xCC9C8,(get(0xCB1B4),decoded,decoded+4,decoded+8))
    native_date=list(struct.unpack('<3I',u.mem_read(decoded,12)))
    expected_day=native_date[1]+1
    def dispatch_boundary(c,pc,size,data):
        town_id,kind=active[0]
        if pc==BASE+0xB6618:c.reg_write(UC_ARM_REG_R0,town_root+4+town_id*108)
        elif pc==BASE+0xB65E4:c.reg_write(UC_ARM_REG_R0,town_id)
        else:
            expected={9:0x619A0,10:0x618E4,11:0x61570}[kind];assert pc==BASE+expected
            parent_cases.append(dict(town_ID=town_id,facility_type=kind,source_target=pc,
                day=c.reg_read(UC_ARM_REG_R1),ceremony_start=c.reg_read(UC_ARM_REG_R2),site_index=c.reg_read(UC_ARM_REG_R3) if kind==11 else None))
        c.reg_write(UC_ARM_REG_PC,c.reg_read(UC_ARM_REG_LR))
    hooks=[u.hook_add(UC_HOOK_CODE,dispatch_boundary,begin=BASE+f,end=BASE+f) for f in (0xB6618,0xB65E4,0x619A0,0x618E4,0x61570)]
    try:
        for town_id in range(90):
            for kind in (9,10,11):
                active[0]=(town_id,kind);get(0x61B44,(window,kind))
                assert parent_cases[-1]['day']==expected_day and parent_cases[-1]['ceremony_start']==((town_id+1)%28)+1,parent_cases[-1]
    finally:
        for h in hooks:u.hook_del(h)
    called={e['message'] for case in cases for e in case['events'] if 'message' in e}
    assert called==set(IDS),(sorted(set(IDS)-called),sorted(called-set(IDS)))
    all_rows=[]
    for n in IDS:
        all_rows.append(dict(message_id=n,japanese=jp[n].text.decode('cp932'),source_hex=jp[n].text.hex(),
            source_reference={k:v for k,v in vars(jp[n]).items() if k!='text'},
            current_English=en[n].text.decode('cp932'),current_hex=en[n].text.hex(),
            current_reference={k:v for k,v in vars(en[n]).items() if k!='text'}))
    save(ROOT/'native_context.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        source_ARM9_sha256=sha(jp_arm),current_ARM9_sha256=sha(arm),source_RAM=str(RAM),source_RAM_sha256=sha(raw),
        unchanged_source_code_spans=[dict(start=a,end=b) for a,b in spans],source_rows=all_rows,
        hero_names=hero_names,hero_table_selections=selections,complete_hero_wrapper_ABI_cases=wrapper,
        town_role_name_mappings=NPCs,site_name_catalog=sites,source_branch_cases=cases,parent_dispatch_cases=parent_cases,
        every52_source_ID_bound_to_original_caller=True,parent_native_calendar_values=native_date,
        original_feast_day_formula='((TownID+1) mod28)+1;original magic92492493/divisor28 verified,not a30-day assumption',
        additional_scope=dict(shared_refusal=64,result_notices=[289,290,291,293,294,295],excluded_unrelated_trade_discovery_notice=292),
        actual_hero_date_site_and_facility_eligibility_not_claimed_for_every_supplied_combination=True,
        UI_IO_and_mutation_interception_not_gameplay_verification=True,
        no_new_English_authored=True,ROM_changed=False,new_completion_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'Ceremony52 source callers:32 hero selectors/32 full wrapper ABI cases,270 NPC role/name mappings,21 site names,{len(cases)} source branches/270 parent-date-site bindings pass. Actual scenes/prose remain next.',flush=True)


if __name__=='__main__':main()
