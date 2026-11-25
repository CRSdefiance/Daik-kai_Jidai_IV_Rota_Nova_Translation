"""Create/release/recreate ABI and source isolation with allocator contracts."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_canvas_lifetime import BASE, CLEANUP, PRIVATE, SLOT, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROOT=Path('work/analysis/town_canvas_lifetime_v488')


def main():
    source=NdsImage.open('out/all_routes_combined_v484_candidate.nds').read_file('/__arm9__.bin')
    arm,plan=transform(source)
    assert arm==(ROOT/'research_arm9.bin').read_bytes()
    u=machine(arm);u.mem_map(0x06000000,0x40000)
    header,view,pixels=0x022BD774,0x02410020,0x0601BFC8
    pattern=bytes((i*17+5)%256 for i in range(8208))
    original=struct.pack('<5I',4,57,72,(0x02125A20-header)&0xffffffff,(pixels-header)&0xffffffff)
    u.mem_write(header,original);u.mem_write(pixels,pattern)
    blocks=[0x02420020,0x02424020]
    allocated=[];freed=[];heaps=[]
    fail=[False]

    def bridge(cpu,address,size,data):
        if address==0x02005154:
            assert cpu.reg_read(UC_ARM_REG_R0)==15104
            pointer=0 if fail[0] else blocks[len(allocated)]
            if pointer:
                allocated.append(pointer);cpu.mem_write(pointer-16,b'\xA5'*(15104+32))
            cpu.reg_write(UC_ARM_REG_R0,pointer)
        elif address==0x02005180:
            pointer=cpu.reg_read(UC_ARM_REG_R0)
            assert pointer in allocated and pointer not in freed
            freed.append(pointer)
        elif address==0x020D2E90:
            heaps.append([cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1)])
        else:return
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))

    hook=u.hook_add(UC_HOOK_CODE,bridge)
    call(u,0xD40B0,(view,))
    for generation in range(2):
        call(u,PRIVATE-BASE,(view,header,0,0))
        pointer=blocks[generation]
        assert struct.unpack('<I',u.mem_read(SLOT,4))[0]==pointer
        assert bytes(u.mem_read(header,20))==original and bytes(u.mem_read(pixels,8208))==pattern
        assert struct.unpack('<5I',u.mem_read(pointer,20))==(4,57,132,(0x02125A20-pointer)&0xffffffff,20)
        assert bytes(u.mem_read(pointer+20,8208))==pattern
        assert bytes(u.mem_read(pointer+20+8208,15048-8208))==bytes(15048-8208)
        assert bytes(u.mem_read(pointer-16,16))==bytes(u.mem_read(pointer+15104,16))==b'\xA5'*16
        call(u,PRIVATE-BASE,(view,header,0,0));assert len(allocated)==generation+1
        call(u,CLEANUP-BASE,(0x02440000,0x40000))
        assert struct.unpack('<I',u.mem_read(SLOT,4))[0]==0 and freed[-1]==pointer
        call(u,CLEANUP-BASE,(0x02440000,0x40000));assert len(freed)==generation+1
    fail[0]=True
    call(u,PRIVATE-BASE,(view,header,0,0))
    assert struct.unpack('<I',u.mem_read(SLOT,4))[0]==0 and bytes(u.mem_read(header,20))==original
    call(u,CLEANUP-BASE,(0x02440000,0x40000));assert len(freed)==2
    u.hook_del(hook)
    assert all(args==[0x02440000,0x40000]for args in heaps)
    proof={'target_arm9_sha256':sha(arm),'plan':plan,'create_release_recreate_cycles':2,
           'all8208_original_VRAM_pixels_and_shared_header_preserved':True,'private_header_and_blank_expansion_exact':True,
           'single_allocation_reuse_each_cycle':True,'free_once_and_pointer_cleared_before_original_heap_setup':True,
           'cleanup_without_live_surface_and_allocation_failure_safe':True,'complete_saved_register_stack_ABI_and_guards_pass':True,
           'allocation_free_and_heap_setup_are_explicit_isolated_endpoint_contracts':True,
           'actual_movie_and_town_lifetime_safety_require_separate_emulator_evidence':True}
    (ROOT/'native_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Two create/release/recreate cycles,OOM fallback,source isolation and ABI passed.')


if __name__=='__main__':
    main()
