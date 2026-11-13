"""Verify paper runs, original fallback, skill getters, and startup ABI."""

import json
import struct

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import ROOT, save
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute


def main():
    arm=(ROOT/"research_arm9.bin").read_bytes()
    plan=json.loads((ROOT/"runtime_plan.json").read_text(encoding="utf-8"))
    u=machine(arm);payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);u.mem_write(POOL,payload)
    runs=[];fallback=[]
    def intercept(uc,address,size,_):
        if address==0x01FFAC18:
            point=struct.unpack("<2I",uc.mem_read(uc.reg_read(UC_ARM_REG_R2),8))
            extent=struct.unpack("<2I",uc.mem_read(uc.reg_read(UC_ARM_REG_R3),8))
            runs.append([*point,*extent,uc.reg_read(UC_ARM_REG_R1)])
        elif address==BASE+0xD13F8:
            fallback.append([uc.reg_read(UC_ARM_REG_R2),uc.reg_read(UC_ARM_REG_R3),struct.unpack("<I",uc.mem_read(uc.reg_read(UC_ARM_REG_SP),4))[0]])
        else:
            return
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    hook=u.hook_add(UC_HOOK_CODE,intercept)
    manager=0x02450000
    u.mem_write(manager+0x18,struct.pack("<I",0x02451000))
    u.mem_write(plan["state_pointer"],struct.pack("<I",manager))
    def fill(obj,width):
        u.mem_write(obj+0x20,struct.pack("<4I",136,16,136+width,32))
        u.mem_write(STACK,struct.pack("<3I",255,0,0))
        call(u,plan["paper_helper_entry"]-BASE,(obj,0x02452000,255,255))
    fill(manager,88)
    expected=[list(struct.unpack_from("<5I",(ROOT/"tooltip_runs.bin").read_bytes(),i)) for i in range(0,plan["paper_runs"]*20,20)]
    actual=[[r[0]-136,r[1]-16,*r[2:]] for r in runs]
    assert actual==expected and not fallback
    coverage=[0]*(88*16)
    for x,y,w,h,_color in actual:
        assert h==1 and 0<=x<x+w<=88 and 0<=y<16
        for n in range(x,x+w):coverage[y*88+n]+=1
    assert set(coverage)=={1}
    fill(manager,84);assert fallback[-1]==[205,190,141]
    fill(manager+0x1000,88);assert fallback[-1]==[255,255,255]
    u.mem_write(plan["state_pointer"],bytes(4));fill(manager,88);assert fallback[-1]==[255,255,255]
    u.hook_del(hook)
    names=[]
    for index,expected in enumerate(["Vigor","Command","Sailing","Survey","Finance","Swords","Aim","Speech","Guile","Observe"]):
        call(u,0x7EEB0,(index,))
        pointer=u.reg_read(UC_ARM_REG_R0)
        actual=bytes(u.mem_read(pointer,24)).split(b"\0")[0].decode("ascii")
        assert actual==expected;names.append(actual)
    rom=NdsImage.open("out/all_routes_combined_v246_candidate.nds")
    format_cases=[]
    for text in names:
        u.mem_write(0x02410000,text.encode("ascii")+b"\0")
        for value in (0,9,97,107,500):
            u.mem_write(0x02411000,struct.pack("<2I",0x02410000,value))
            u.mem_write(0x02412000,b"\xa5"*64)
            call(u,0xCE898,(0x02412000,BASE+0x148CC0,0x02411000))
            actual=bytes(u.mem_read(0x02412000,64)).split(b"\0")[0].decode("ascii")
            assert actual==f"{text:>7}{value:3d}" and len(actual)==10
            assert bytes(u.mem_read(0x0241200B,53))==b"\xa5"*53
            format_cases.append([text,value,actual])
    boot=execute(arm,bytes(rom.rom.arm7),rom.rom.arm7RamAddress,repair_entry=plan["cache"]["entry"],expected_pool=payload)
    proof={"format":"dk4-plaque-runtime-native-v247","exact_paper_runs":len(runs),"coverage_pixels":len(coverage),
           "all_paper_pixels_covered_once_and_bounded":True,"equipment_other_width_prior_tan_preserved":True,
           "generic_tooltip_and_reset_white_preserved":True,"ABI_and_saved_registers_pass":True,
           "native_skill_getter_labels":names,"native_seven_letter_three_digit_format_cases":format_cases,
           "boot":boot,"arena":initialize(arm),
           "GPU_paper_and_live_label_spacing_pending":True}
    save(ROOT/"native_proof.json",proof)
    print("Native paper coverage, style isolation, all 10 skill getters and boot/cache checks passed.")


if __name__=="__main__":
    main()
