"""Actual ARM category lookup ABI for all callers, compact labels and sentinels."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_SP,
)

from dk4tool.patch.category_dialogue_lookup import BASE, GETTER, OLD_NAMES, OUTER, POOL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import SAVED, STACK, call, machine
from scripts.verify_square_caption_cells_v483 import native as caption_raster
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/category_dialogue_v754')
UI_RETURNS=(0x020BE804,0x020BEF18,0x020C3DEC,0x020C3F68,0x020F202C)


def cpu_for(arm):
    cpu=machine(arm);cpu.mem_write(POOL,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]));return cpu


def getter(cpu,index,return_pc):
    cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_LR,return_pc);cpu.reg_write(UC_ARM_REG_R0,index&0xffffffff)
    saved={r:0xA5A50000+n for n,r in enumerate(SAVED)}
    for r,v in saved.items():cpu.reg_write(r,v)
    cpu.emu_start(GETTER,return_pc,count=1000)
    assert cpu.reg_read(UC_ARM_REG_PC)==return_pc and cpu.reg_read(UC_ARM_REG_SP)==STACK
    assert all(cpu.reg_read(r)==v for r,v in saved.items())
    return cpu.reg_read(UC_ARM_REG_R0)


def string(cpu,pointer):
    return bytes(cpu.mem_read(pointer,80)).split(b'\0')[0].decode('ascii')


def main():
    old=NdsImage.open('out/all_routes_combined_v753_candidate.nds').read_file('/__arm9__.bin')
    new=(ROOT/'lookup_research_ARM9.bin').read_bytes()
    a,b=cpu_for(old),cpu_for(new);checks=[]
    expected=list(OLD_NAMES)
    for i,s in {1:'Seasonings',2:'Delicacy',6:'Precious Metals',11:'Jewelry',13:'Medicine',17:'Sundries'}.items():expected[i]=s
    for return_pc in (*UI_RETURNS,0x0205FC48):
        for i in range(18):
            before,after=getter(a,i,return_pc),getter(b,i,return_pc)
            old_text,new_text=string(a,before),string(b,after)
            assert old_text==OLD_NAMES[i]
            assert new_text==(expected[i] if return_pc==0x0205FC48 else old_text)
            checks.append({'category':i,'native_return_PC':return_pc,'before':old_text,'after':new_text,'ABI_return_stack_saved_registers_pass':True})
    square=[]
    for i in range(18):
        results=[]
        for cpu in (a,b):
            call(cpu,OUTER-BASE,(i,));results.append(string(cpu,cpu.reg_read(UC_ARM_REG_R0)))
        assert results[0]==results[1]
        square.append({'category':i,'before_and_after_complete_caption_category':results[0]})
    sentinels=[]
    for return_pc in (*UI_RETURNS,0x0205FC48):
        for i in (-1,-2,-3,18,19,255):
            p,q=getter(a,i,return_pc),getter(b,i,return_pc);assert p==q
            sentinels.append({'index':i,'native_return_PC':return_pc,'same_original_return_value':p})
    fleet=[]
    for field in (0x15163C,0x151640,0x151644):
        old_ptr,new_ptr=(struct.unpack_from('<I',arm,field)[0] for arm in (old,new))
        assert string(a,old_ptr)==string(b,new_ptr)=='Fleet'
        for cpu,pointer in ((a,old_ptr),(b,new_ptr)):
            cpu.mem_write(0x02420000,b'%s\0');cpu.mem_write(0x02420100,b'\xA5'*32)
            call(cpu,0xD7720,(0x02420100,0x02420000,pointer))
            assert bytes(cpu.mem_read(0x02420100,6))==b'Fleet\0'
        fleet.append({'field':field,'old_pointer':old_ptr,'new_pointer':new_ptr,'complete_native_printf_copy_with_unaligned_UI_suffix_pass':True})
    captions=[]
    for row in square:
        text=row['before_and_after_complete_caption_category']+' Shop'
        old_pixels,old_ctx,_=caption_raster(old,text)
        new_pixels,new_ctx,_=caption_raster(new,text)
        assert old_pixels==new_pixels and old_ctx==new_ctx
        captions.append({'category':row['category'],'text':text,'all768_native_palette_indices_and_context_exact':True})
    fallbacks=[]
    for width,origin in ((48,(0,0)),(64,(1,0)),(64,(0,1)),(80,(0,0))):
        old_pixels,old_ctx,_=caption_raster(old,'Food Shop',width,origin)
        new_pixels,new_ctx,_=caption_raster(new,'Food Shop',width,origin)
        assert (old_pixels,old_ctx)==(new_pixels,new_ctx)
        fallbacks.append({'width':width,'origin':origin,'full_fallback_indices_and_context_exact':True})
    arguments=[]
    for i in range(18):
        u=cpu_for(new);u.mem_write(0x0245000C,bytes((i,)))
        u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_R5,0x02450100);u.reg_write(UC_ARM_REG_R6,0x02450000)
        seen=[]
        def stop(cpu,address,size,unused,seen=seen):
            if address==BASE+0x53FE4:
                assert cpu.reg_read(UC_ARM_REG_R1)==730 and cpu.reg_read(UC_ARM_REG_R0)==0x02450100
                seen.append(string(cpu,cpu.reg_read(UC_ARM_REG_R2)));cpu.emu_stop()
        h=u.hook_add(UC_HOOK_CODE,stop)
        try:u.emu_start(BASE+0x5FC40,BASE+0x5FC5C,count=1000)
        finally:u.hook_del(h)
        assert seen==[expected[i]]
        arguments.append({'category':i,'original730_caller_argument':seen[0],'original_direct_portrait_call_reached':True})
    save(ROOT/'lookup_native_ABI.json',{'source_ARM9_sha256':sha(old),'target_ARM9_sha256':sha(new),
        'all108_getter_cases':checks,'all18_existing_Square_labels_exact':square,'all36_negative_and_sentinel_cases_exact':sentinels,
        'three_Fleet_header_fields_complete_native_copies':fleet,'full_name_730_source_call_site_unchanged':old[0x5FC40:0x5FC5C]==new[0x5FC40:0x5FC5C],
        'all18_original_Square_caption_planes_exact':captions,'all4_caption_fallbacks_exact':fallbacks,
        'all18_original730_caller_arguments':arguments,
        'ownership_report_sha256':sha((ROOT/'lookup_ownership.json').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'actual_GPU_gameplay_pending':True,'full_goal_complete':False})
    print('108 native category calls,18 unchanged Square labels,36 sentinels and3 Fleet header copies pass.',flush=True)


if __name__=='__main__':main()
