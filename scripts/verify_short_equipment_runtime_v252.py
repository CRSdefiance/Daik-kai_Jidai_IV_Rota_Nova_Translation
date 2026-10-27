"""Native paper coverage, fallback isolation and inherited boot/cache checks."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.short_equipment_paper import ROOT
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import save
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute


def main():
    arm=(ROOT/"research_arm9.bin").read_bytes();plan=json.loads((ROOT/"runtime_plan.json").read_text(encoding="utf-8"))
    u=machine(arm);payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);u.mem_write(POOL,payload)
    runs=[];fills=[]
    def intercept(uc,address,size,_):
        if address==0x01FFAC18:
            point=struct.unpack("<2I",uc.mem_read(uc.reg_read(UC_ARM_REG_R2),8));extent=struct.unpack("<2I",uc.mem_read(uc.reg_read(UC_ARM_REG_R3),8))
            runs.append([*point,*extent,uc.reg_read(UC_ARM_REG_R1)])
        elif address==BASE+0xD13F8:
            fills.append([uc.reg_read(UC_ARM_REG_R2),uc.reg_read(UC_ARM_REG_R3),struct.unpack("<I",uc.mem_read(uc.reg_read(UC_ARM_REG_SP),4))[0]])
        else:return
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    hook=u.hook_add(UC_HOOK_CODE,intercept);manager=0x02450000;u.mem_write(manager+0x18,struct.pack("<I",0x02451000));cases=[]
    def invoke(width,height=16,obj=manager,active=True):
        runs.clear();fills.clear();u.mem_write(plan["state_pointer"],struct.pack("<I",manager if active else 0))
        u.mem_write(obj+0x20,struct.pack("<4I",16,16,16+width,16+height));u.mem_write(STACK,struct.pack("<3I",255,0,0))
        call(u,plan["dispatcher_entry"]-BASE,(obj,0x02452000,255,255))
    for name,width in [("Armor",34),("Weapon",40),("Equipped Items",88)]:
        invoke(width);path=(ROOT/(name.lower()+"_paper_runs.bin")) if width!=88 else Path("work/analysis/plaque_style_v247/tooltip_runs.bin")
        data=path.read_bytes();expected=[list(struct.unpack_from("<5I",data,n)) for n in range(0,len(data),20)]
        actual=[[x-16,y-16,w,h,c] for x,y,w,h,c in runs];assert actual==expected and not fills
        cover=[0]*(width*16)
        for x,y,w,h,_c in actual:
            assert h==1 and 0<=x<x+w<=width and 0<=y<16
            for col in range(x,x+w):cover[y*width+col]+=1
        assert set(cover)=={1};cases.append({"name":name,"width":width,"height":16,"exact_runs":len(runs),"all_pixels_once_and_bounded":len(cover)})
    for width,height,obj,active,color in [(34,15,manager,True,[205,190,141]),(40,17,manager,True,[205,190,141]),
                                         (50,16,manager,True,[205,190,141]),(34,16,manager+0x1000,True,[255,255,255]),
                                         (40,16,manager,False,[255,255,255]),(88,16,manager,False,[255,255,255])]:
        invoke(width,height,obj,active);assert not runs and fills==[color]
        cases.append({"width":width,"height":height,"same_manager":obj==manager,"theme_active":active,"original_fallback_RGB":color})
    u.hook_del(hook);rom=NdsImage.open("out/all_routes_combined_v251_candidate.nds")
    boot=execute(arm,bytes(rom.rom.arm7),rom.rom.arm7RamAddress,repair_entry=plan["cache"]["entry"],expected_pool=payload)
    save(ROOT/"native_proof.json",{"format":"dk4-short-equipment-native-v252","cases":cases,
                                  "full_saved_register_and_stack_ABI_pass":True,"boot":boot,"arena":initialize(arm),
                                  "GPU_actual_three_hint_geometries_pending":True,"all18_plaque_hint_audit_entries_incomplete":True})
    print("Native paper coverage for all3 hint sizes,6 isolated fallback cases and boot/cache/ARM7 checks passed.")


if __name__=="__main__":
    main()
