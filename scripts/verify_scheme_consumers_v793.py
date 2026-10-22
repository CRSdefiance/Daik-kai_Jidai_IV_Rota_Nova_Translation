"""Source-bound ordinary selector subjects; do not invent document-menu playback."""

import re
import struct
from pathlib import Path

from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn.arm_const import (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,
    UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,
    UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_item_runtime_storage_v785 import census
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_village_wrap_v608 import read,save
from scripts.inventory_map_tooltip_classes import execute_class

ROOT=Path('work/analysis/scheme_consumer_scope_v793')
ROM=Path('out/all_routes_combined_v792_candidate.nds')
RAM=Path('E:/Rota Nova translations/Generated/work/emulation_v193/arrival_v792_delivery/frame_020000_arm9_ram.bin')
OBJECT,ARRAY=0x02479000,0x0247A000


def types(arm):
    word=lambda off:struct.unpack_from('<I',arm,off)[0]
    result={}
    for off in range(0,len(arm)-16,4):
        vt=word(off)
        if vt not in (0x0212FD9C,0x0212FDAC,0x0212FDBC):continue
        p=word(off+4)-BASE
        if not 0<=p<len(arm):continue
        name=arm[p:p+256].split(b'\0')[0]
        if not re.fullmatch(rb'[0-9A-Za-z_]+',name):continue
        if vt==0x0212FD9C:
            count=word(off+12);assert count<16
            parents=[word(off+16+8*i) for i in range(count)]
        elif vt==0x0212FDAC:parents=[word(off+8)]
        else:parents=[]
        result[BASE+off]={'name':name.decode(),'vtable':vt,'parents':parents}
    assert len(result)==366
    assert all(p in result for r in result.values() for p in r['parents'])
    return result


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    clean=NdsImage.open('work/clean.nds');current=NdsImage.open(ROM)
    source,arm=[r.read_file('/__arm9__.bin') for r in (clean,current)]
    graph=types(source)
    def derives(at,parent,seen=()):
        assert at not in seen
        return at==parent or any(derives(p,parent,seen+(at,)) for p in graph[at]['parents'])
    map_type=0x0214C9E4
    admitted={at:r for at,r in graph.items() if derives(at,map_type)}
    assert set(admitted)=={0x0214C93C,0x0214C984,0x0214C99C,0x0214C9E4}
    # Every pointer to this base is accounted for:three original subclass edges,
    # original RTTI/vtable groups and the original dynamic_cast literal.
    refs=[]
    for raw in (source,arm):
        refs.append([BASE+n for n in range(0,len(raw)-3,4) if struct.unpack_from('<I',raw,n)[0]==map_type])
    assert refs[0]==refs[1]
    expected_refs=[0x2096B20,0x214C94C,0x214C994,0x214C9AC,0x214D66C,0x214D6AC,0x214D6F0,
        0x214D714,0x214D750,0x214D7F8,0x214D818,0x214D858,0x214D89C,0x214D8C0,0x214D8FC,0x214D9A4]
    assert refs[0]==expected_refs
    for at,r in admitted.items():
        size=16+len(r['parents'])*8
        assert source[at-BASE:at-BASE+size]==arm[at-BASE:at-BASE+size]
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    spans=((0x21478,0x21644),(0x406E4,0x40814),(0x4AB40,0x4AB9C),
        (0x94BC0,0x94BF4),(0x949D0,0x94A08),(0x95188,0x951C0),
        (0x9460C,0x9462C),(0x9663C,0x967E8),(0x96A00,0x96B24),
        (0x97910,0x97950),(0x9AC54,0x9ACBC),(0x9AEF4,0x9AF5C),
        (0x9B144,0x9B1AC),(0x9B36C,0x9B3A8),(0xCACAC,0xCACBC))
    disassembly=[]
    for lo,hi in spans:
        assert source[lo:hi]==arm[lo:hi]
        disassembly.append({'span':[BASE+lo,BASE+hi],'sha256':sha(source[lo:hi]),
            'instructions':[{'pc':i.address,'instruction':i.mnemonic+' '+i.op_str} for i in cs.disasm(source[lo:hi],BASE+lo)]})
    edges={0x0204F0AC:(0x0204EF40,0x0204EFC0,0x0209B39C),0x0204EF0C:(0x020967C4,),
        0x0204EF6C:(0x020407BC,0x0204AB98),0x0209B36C:(0x0209ACB4,0x0209AF54,0x0209B1A4),
        0x02096704:(0x020966B8,),0x02021478:(0x02040764,0x0204AB5C,0x0209678C,0x0209793C,0x0209AC8C,0x0209AF2C,0x0209B17C)}
    alias=execute_class(arm,35)
    assert alias['pointer_field']==0x11CF50 and bytes.fromhex(alias['full_text_hex'])==b'Giant Squid\0'
    assert arm[0x11CF51:0x11CF55]==struct.pack('<I',0x02021478)
    assert arm[0x11CF54:0x11CF58]==source[0x11CF54:0x11CF58]
    reference=[]
    for target,callers in edges.items():
        expected=[['ARM_branch','section0',at,target,False] for at in callers]
        for name,rom in (('clean',clean),('V792',current)):
            got=census(rom,[[target,target+4]],[])
            allowed=expected+([['absolute','section0',0x0211CF51,target,False]] if name=='V792' and target==0x02021478 else [])
            assert sorted(got)==sorted(allowed),(name,hex(target),got)
            reference.append({'version':name,'target':target,'incoming_references':got})
    raw=RAM.read_bytes();cpu=machine(arm);cpu.mem_write(BASE,raw)
    def get(fn,args=()):
        call(cpu,fn,args,instruction_limit=200000);return cpu.reg_read(UC_ARM_REG_R0)
    def word(at):return struct.unpack('<I',cpu.mem_read(at,4))[0]
    def info(obj):
        vt=word(obj)
        return {'object':obj,'kind':get(word(vt)-BASE,(obj,)),'index':get(word(vt+4)-BASE,(obj,))}
    kinds=[]
    for getter,label,kind in ((0xCB160,'company',4),(0xCB1A8,'fleet',8),(0xCB178,'town',5),
        (0xCB184,'actor',1),(0xCB190,'item',3),(0xCB130,'scheme',13)):
        r=info(get(getter)+4);assert r['kind']==kind
        kinds.append({'native_manager_getter':BASE+getter,'label':label,**r})
    before=bytes(cpu.mem_read(BASE,0x800000));providers=[]
    for label,vt,bias,count,kind in (('fleet',0x214D9C8,143,63,8),('town',0x214DB74,29,114,5),
                                  ('village-map-record',0x214D4C4,119,24,19)):
        vbase=struct.unpack('<i',cpu.mem_read(vt-20,4))[0]
        for n in range(count):
            cpu.mem_write(OBJECT,bytes(1024));cpu.mem_write(OBJECT,struct.pack('<I',vt))
            cpu.mem_write(OBJECT+vbase+28,struct.pack('<I',n+bias))
            fn=word(vt+36);obj=get(fn-BASE,(OBJECT,));r=info(obj)
            assert r['kind']==kind and r['index']==n
            providers.append({'class':label,'vtable':vt,'provider':fn,'source_index':n,**r})
    # The source base provider is NULL;no CScheme fallback is substituted.
    assert get(0x9460C,(OBJECT,))==0
    after=bytes(cpu.mem_read(BASE,0x800000))
    def unowned(data):
        r=bytearray(data)
        for lo,hi in ((OBJECT,OBJECT+1024),(STACK-4096,STACK+4096)):r[lo-BASE:hi-BASE]=bytes(hi-lo)
        return r
    assert unowned(before)==unowned(after)
    lists=[]
    for fn,end,kind in ((0x9AC54,0x9ACB4,8),(0x9AEF4,0x9AF54,4),(0x9B144,0x9B1A4,5)):
        for supplied in (0,1,20,21):
            cpu.mem_write(OBJECT,bytes(1024));cpu.mem_write(ARRAY,struct.pack('<21I',*range(21)))
            for reg,v in ((UC_ARM_REG_R0,OBJECT),(UC_ARM_REG_R1,ARRAY),(UC_ARM_REG_R2,supplied),(UC_ARM_REG_R3,0),
                (UC_ARM_REG_SP,STACK),(UC_ARM_REG_LR,STOP)):cpu.reg_write(reg,v)
            cpu.emu_start(BASE+fn,BASE+end,count=200000)
            assert cpu.reg_read(UC_ARM_REG_PC)==BASE+end
            count=word(OBJECT+0x26C);assert count==min(supplied,20)
            ids=list(struct.unpack('<'+'I'*count,cpu.mem_read(OBJECT+0x21C,4*count))) if count else []
            assert ids==[(kind<<24)|n for n in range(count)]
            lists.append({'source_prefix':BASE+fn,'stop_before_generic_selector':BASE+end,'supplied_count':supplied,
                'count':count,'typed_kind':kind,'encoded_IDs':ids,'original_encoder_executes':True})
    item_prefix=[]
    for count in (0,1,218):
        cpu.mem_write(ARRAY,struct.pack('<218I',*range(218)))
        for reg,v in ((UC_ARM_REG_R6,count),(UC_ARM_REG_R10,ARRAY),(UC_ARM_REG_SP,STACK),(UC_ARM_REG_LR,STOP)):cpu.reg_write(reg,v)
        cpu.emu_start(BASE+0x4AB40,BASE+0x4AB70,count=100000)
        assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x4AB70
        ids=list(struct.unpack('<'+'I'*count,cpu.mem_read(STACK+12,4*count))) if count else []
        assert ids==[(3<<24)|n for n in range(count)]
        item_prefix.append({'count':count,'encoded_IDs':ids,'original_item_prefix':0x0204AB40,
            'declared_R6_count_R10_array_CPU_inputs_not_inventory_or_full_function':True})
    # The remaining producer's default is a literal fleet kind8.
    cpu.mem_write(OBJECT+0x6890,struct.pack('<I',0xFFFFFFFF))
    cpu.reg_write(UC_ARM_REG_R0,OBJECT);cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
    cpu.emu_start(BASE+0x97910,BASE+0x97940,count=100000)
    default_id=cpu.reg_read(UC_ARM_REG_R0)
    assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x97940 and default_id>>24==8
    # Execute the dynamic map loop with all three genuine provider classes.
    expected_ids=[];container=OBJECT+0x5000;view_ptrs=[]
    for k,(vt,bias,index,kind) in enumerate(((0x214D9C8,143,0,8),(0x214DB74,29,22,5),(0x214D4C4,119,0,19))):
        obj=OBJECT+0x1000+k*1024;cpu.mem_write(obj,bytes(1024));cpu.mem_write(obj,struct.pack('<I',vt))
        offset=struct.unpack('<i',cpu.mem_read(vt-20,4))[0];cpu.mem_write(obj+offset+28,struct.pack('<I',index+bias))
        view_ptrs.append(obj);expected_ids.append((kind<<24)|index)
    cpu.mem_write(container,struct.pack('<5I',0,3,*view_ptrs))
    cpu.reg_write(UC_ARM_REG_R0,container);cpu.reg_write(UC_ARM_REG_R1,OBJECT)
    cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,STOP)
    cpu.emu_start(BASE+0x96704,BASE+0x967A4,count=100000)
    sp=cpu.reg_read(UC_ARM_REG_SP)
    assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x967A4
    assert list(struct.unpack('<3I',cpu.mem_read(sp+16,12)))==expected_ids
    save(ROOT/'source_and_native_scope.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'clean_ARM9_sha256':sha(source),'current_ARM9_sha256':sha(arm),'complete366_type_RTTI_graph':graph,
        'map_cast_admitted_classes':admitted,'all_map_base_pointer_references':refs[0],
        'all_original_constructor_and_typed_ID_reference_edges':reference,'source_disassembly':disassembly,
        'qualified_unaligned_data_alias':{'address':0x0211CF51,'native_creature_initializer':alias,
            'meaning':'Overlapping bytes of the aligned Giant Squid name pointer and its unchanged adjacent numeric field;not an additional callable factory entry.'},
        'native_class_numbers':kinds,'all201_original_map_object_provider_cases':providers,
        'provider_8MiB_outside_declared_CPU_object_and_callstack_exact':True,'twelve_original_fixed_kind_list_prefixes':lists,
        'three_original_item_selector_prefix_cases':item_prefix,'original_default_map_target_ID':default_id,
        'original_dynamic_map_loop_encoded_IDs':expected_ids,
        'dynamic_map_loop_three_real_virtual_providers_kind_getters_index_getters_encoder_execute':True,
        'ordinary_selectors_have_no_discovered_CSchemes_kind13_source':True,
        'scope':'Complete discovered static constructor and typed-ID entry edges,closed original map RTTI family and native providers;not unbounded indirect jumps,corrupted data,debug instrumentation or an actual document-name GPU menu.',
        'earlier_actor_class3_assumption_corrected':'Class3 is item;actual actor manager reports class1. Fleet8,town5,company4,scheme13,village-map-record19 are executed native results.',
        'CPU_field_inputs_not_real_inventory_or_actual_map_menu_playback':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('366 original RTTI types;201 native map-provider cases;12 fixed-kind selector prefixes;all ordinary constructor/typed-ID reference edges close without a kind13 document list.',flush=True)


if __name__=='__main__':main()
