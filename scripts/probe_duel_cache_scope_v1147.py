"""Execute the real COMMON loader,scoped front,PIC draw and native cache loops.

File open/read,SDK clear,UI registration and (in this scope test) font entry are
explicit CPU boundaries. No numeric messages are injected into an emulator.
"""
from pathlib import Path
from types import FunctionType, SimpleNamespace
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,
                               UC_ARM_REG_PC,UC_ARM_REG_LR,UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_postmacro_layout_v1134 import layout
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import STACK
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

BASE=0x02000000
FRONT,CACHE,OWNER=0x0200DAF0,0x0228E70C,0x0228E6DC
TABLES=(0x02117340,0x02117360,0x021174E0)
ROOT=Path('work/analysis/duel_cache_scope_v1147')
PLAN_PATH=Path('work/analysis/duel_cache_payload_v1144/cache_prefix_research_plan.json')


def pipeline(arm,common,raw):
    source=NdsImage.open('out/all_routes_combined_v1105_candidate.nds').read_file('/__arm9__.bin')
    cpu,initial_get=get_machine(arm,raw)
    # The live snapshot preserves globals. Patch only declared changed code or
    # immutable metadata,never replace the complete live initialized-data range.
    plan=read(PLAN_PATH)
    spans=[*plan['metadata_fields'],[0xDA28,0x134]]
    for at,size in spans:
        assert bytes(cpu.mem_read(BASE+at,size))==source[at:at+size]
        cpu.mem_write(BASE+at,arm[at:at+size])
    component=plan['new_code_prefix']
    state={'front':[],'gets':[],'component_entries':0,'component_returns':0,
           'font_entries':[],'data_lines':[],'instruction_lines':[],'drains':0,'active':False}
    provider=SimpleNamespace(owner=OWNER,common=common,opens=[],reads=[],executed=set())
    io=FunctionType(Loader.code.__code__,{**Loader.code.__globals__,'STACK':STACK})

    def file_boundary(u,pc,size,data):
        assert not state['active'],'COMMON file I/O while executing the cached component'
        io(provider,u,pc,size,data)

    for pc in (0x534F4,0x53628,0x535E0,0xCEC74,0xD2018,0xD1EF0,0xD1F50,0xD1EE0,0xD0398,0xD0170):
        cpu.hook_add(UC_HOOK_CODE,file_boundary,begin=BASE+pc,end=BASE+pc)

    def front(u,pc,size,data):
        context,pointer=u.reg_read(UC_ARM_REG_R0),u.reg_read(UC_ARM_REG_R1)
        sp=u.reg_read(UC_ARM_REG_SP)
        assert context==sp+0x410 and pointer==sp+16
        parent=struct.unpack('<I',u.mem_read(context+108,4))[0]
        table=struct.unpack('<I',u.mem_read(context+148,4))[0]
        state['front'].append({'parent':parent,'table':table,'context':context,'pointer':pointer,
            'expanded_hex':bytes(u.mem_read(pointer,128)).split(b'\0')[0].hex(),
            'eligible':parent==BASE+0xD4BC and table in TABLES})

    cpu.hook_add(UC_HOOK_CODE,front,begin=FRONT,end=FRONT)

    def getter(u,pc,size,data):
        assert not state['active'],'COMMON getter reentered while cached code is active'
        state['gets'].append({'message_ID':u.reg_read(UC_ARM_REG_R0),'return':u.reg_read(UC_ARM_REG_LR)})

    cpu.hook_add(UC_HOOK_CODE,getter,begin=BASE+0x5528C,end=BASE+0x5528C)

    def enter(u,pc,size,data):
        assert state['front'][-1]['eligible'] and not state['active']
        assert bytes(u.mem_read(OWNER+0x2C,1))==b'\x15'
        assert sha(bytes(u.mem_read(CACHE,component['component_bytes'])))==component['component_sha256']
        assert u.reg_read(UC_ARM_REG_R0)==state['front'][-1]['context']
        assert u.reg_read(UC_ARM_REG_R1)==state['front'][-1]['pointer']
        state['active']=True;state['component_entries']+=1
        state['component_return_PC']=u.reg_read(UC_ARM_REG_LR)&~1

    cpu.hook_add(UC_HOOK_CODE,enter,begin=CACHE,end=CACHE)
    # The front's BLX r6 is at offset64. Its following POP is the caller return
    # point;derive the actual address from the pinned instruction bytes below.
    from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
    front_code=bytes(cpu.mem_read(FRONT,104))
    calls=[i for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(front_code[:84],FRONT)
           if i.mnemonic=='blx' and i.op_str=='r6']
    assert len(calls)==1
    returned_PC=calls[0].address+calls[0].size

    def returned(u,pc,size,data):
        assert state['active'] and pc==state['component_return_PC']
        assert sha(bytes(u.mem_read(CACHE,component['component_bytes'])))==component['component_sha256']
        state['active']=False;state['component_returns']+=1

    cpu.hook_add(UC_HOOK_CODE,returned,begin=returned_PC,end=returned_PC)

    def readonly(u,access,address,size,value,data):
        assert not state['active'],f'Cached code modified during execution:{address:#x}'

    cpu.hook_add(UC_HOOK_MEM_WRITE,readonly,begin=CACHE,end=CACHE+component['component_bytes']-1)

    def cache_operation(u,pc,size,data):
        assert not state['active']
        if pc==BASE+0xE443C:state['drains']+=1
        elif pc==BASE+0xE4440:state['data_lines'].append(u.reg_read(UC_ARM_REG_R0))
        else:state['instruction_lines'].append(u.reg_read(UC_ARM_REG_R0))
        u.reg_write(UC_ARM_REG_PC,pc+4)

    for pc in (0xE443C,0xE4440,0xE4484):
        cpu.hook_add(UC_HOOK_CODE,cache_operation,begin=BASE+pc,end=BASE+pc)

    def get(at,*args):
        call(cpu,at,args,instruction_limit=3000000)
        return cpu.reg_read(UC_ARM_REG_R0)

    state['file_provider']=provider
    return cpu,get,state


def execute(arm,common,raw,actor,name,family,table,number,text,*,direct=False):
    cpu,get,state=pipeline(arm,common,raw)
    controller,argument=0x02460000,0x02469000
    widget=controller+0x214
    cpu.mem_write(controller,bytes(0x600))
    cpu.mem_write(controller+0x34,struct.pack('<2I',actor,actor))
    cpu.mem_write(argument,name+b'\0')
    get(0xE14C,widget)

    def bypass(u):u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    def registration(u,pc,size,data):
        assert u.reg_read(UC_ARM_REG_R0)==widget
        bypass(u)
    handle=cpu.hook_add(UC_HOOK_CODE,registration,begin=BASE+0xD351C,end=BASE+0xD351C)
    try:get(0xDEF4,widget)
    finally:cpu.hook_del(handle)
    header=struct.unpack('<I',cpu.mem_read(widget+0x3C+16,4))[0]
    h=struct.unpack('<5I',cpu.mem_read(header,20));assert h[:3]==(4,52,36)
    def clear(u,pc,size,data):
        assert u.reg_read(UC_ARM_REG_R0)==header
        cpu.mem_write((header+h[4])&0xffffffff,bytes(208*36//2));bypass(u)
    def font(u,pc,size,data):
        context,pointer=u.reg_read(UC_ARM_REG_R0),u.reg_read(UC_ARM_REG_R1)
        before=state['front'][-1]
        original=text.replace(b'%s',name)
        assert before['expanded_hex']==original.hex()
        expected,lines=layout(original) if before['eligible'] else (original,[original.decode('cp932')])
        actual=bytes(u.mem_read(pointer,1024)).split(b'\0')[0]
        assert actual==expected
        assert context==before['context'] and pointer==before['pointer']
        assert state['active']==before['eligible']
        if before['eligible']:
            assert struct.unpack('<i',u.mem_read(context+40,4))[0]==(12 if len(lines)==1 else 0)
        state['font_entries'].append({'context':context,'text_hex':actual.hex(),'lines':lines,
            'compiled_component_active':state['active']})
        u.reg_write(UC_ARM_REG_R0,pointer+len(actual));bypass(u)
    hooks=[cpu.hook_add(UC_HOOK_CODE,clear,begin=0x01FFB2DC,end=0x01FFB2DC),
           cpu.hook_add(UC_HOOK_CODE,font,begin=BASE+0xD5404,end=BASE+0xD5404)]
    cpu.mem_write(STACK,struct.pack('<I',argument))
    side=0 if family=='challenge' else 1
    try:get(0xD4D0 if direct else 0xD458,controller,side,60,number if direct else table)
    finally:
        for handle in hooks:cpu.hook_del(handle)
    eligible=not direct and table in TABLES
    assert len(state['front'])==len(state['font_entries'])==1
    assert state['front'][0]['eligible']==eligible
    assert state['component_entries']==state['component_returns']==int(eligible) and not state['active']
    assert [row['message_ID'] for row in state['gets']]==([number,1931] if eligible else [number])
    plan=read(PLAN_PATH);size=plan['new_code_prefix']['component_bytes']
    lines=list(range(CACHE&~31,(CACHE+size+31)&~31,32))
    assert state['data_lines']==state['instruction_lines']==(lines if eligible else [])
    assert state['drains']==(len(lines) if eligible else 0)
    assert bytes(cpu.mem_read(argument,len(name)+1))==name+b'\0'
    return {'family':family,'message_ID':number,'direct':direct,'eligible':eligible,
        'source_getter_IDs':[row['message_ID'] for row in state['gets']],
        'source_front':state['front'][0],'font_boundary':state['font_entries'][0],
        'native_data_flush_lines':state['data_lines'],'native_instruction_invalidate_lines':state['instruction_lines'],
        'native_drain_count':state['drains'],'all_expected_component_cache_lines_covered':True,
        'no_COMMON_getter_IO_or_component_write_while_PIC_code_active':True,
        'original_selector_printf_macro_native_cache_loader_front_and_full_stack_register_ABI_pass':True,
        'file_read_count':len(state['file_provider'].reads),'font_entry_is_a_boundary_not_actual_font_raster':True}


def main():
    assert not ROOT.exists()
    plan=read(PLAN_PATH)
    arm,common=Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    catalog=read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    raw=Path(catalog['snapshot']).read_bytes();assert sha(raw)==catalog['snapshot_sha256']
    records={row['message_id']:row for row in read('translations/duel_editorial_manuscript_v3.json')['records']}
    tables={'challenge':TABLES[0],'acceptance':TABLES[1],'threat':TABLES[2],
            'named_escape_negative':0x02117500,'admiral_escape_negative':0x02117620}
    cpu,get=get_machine(arm,raw);representatives={}
    for row in catalog['names']:
        for family,table in tables.items():
            n=get(0x53F4C,row['object'],table)
            representatives.setdefault((family,n),(row['object'],bytes.fromhex(row['name_hex'])))
    results=[]
    ROOT.mkdir(parents=True)
    for (family,number),(actor,name) in sorted(representatives.items()):
        results.append(execute(arm,common,raw,actor,name,family,tables[family],number,
                               records[number]['english'].encode('ascii')))
    actor,name=representatives[('challenge',1931)]
    for number in range(1931,1951):
        results.append(execute(arm,common,raw,actor,name,'direct_negative',0,number,
                               records[number]['english'].encode('ascii'),direct=True))
    assert len(results)==53 and sum(row['eligible'] for row in results)==20
    proof=ROOT/'original_loader_scoped_cache_component.json'
    save(proof,{'target_plan':str(PLAN_PATH),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'cases':results,'all20_original_voice_selections_enter_correct_native_PIC_component':True,
        'all13_other_tables_and20_direct_numeric_controls_skip_component':True,
        'original_native_file_container_cache_load_copy_printf_macro_and_front_execute':True,
        'each_selected_case_flushes_and_invalidates_all47_required_cache_lines':True,
        'component_bytes_immutable_and_no_COMMON_reentry_until_component_returns':True,
        'font_callback_and_hardware_MCR_effects_are_explicit_boundaries_not_full_display_or_cache_hardware_proof':True,
        'actual_emulator_boot_fonts_and_scene_transitions_still_pending':True,
        'no_registered_ROM_or_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    path=Path('translations/editorial_review_current_v1.json');ledger=read(path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    ledger['duel_prose_v1103'].update(cache_component_scope=str(proof),
        cache_component_research_plan=str(PLAN_PATH),
        formatting_status='existing-cache-PIC-placement-and-real-selector-front-pass;full-resident-fonts13-escape-integration-actual-open')
    save(path,ledger)
    print('53 original loader/front/PIC scope cases pass:20 selected,33 excluded;47 native flush/invalidate lines each;no allocation growth.')


if __name__=='__main__':main()

