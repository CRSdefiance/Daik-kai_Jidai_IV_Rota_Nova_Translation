"""Market-specific indicator crops and same-frame native source/cache evidence."""

import json
import struct
from pathlib import Path
from unittest.mock import patch

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R4, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_title_display_v229 as resources
from scripts.probe_button_prompt_native import STACK, call

ROOT=Path("work/analysis/market_indicator_v249")
CAPTURE=Path("work/emulation_v193/market_native_v249")
ROM=Path("out/all_routes_combined_v247_candidate.nds")


def main():
    rom=NdsImage.open(ROM);arm=rom.read_file("/__arm9__.bin");raw=rom.read_file("/_pxl/__frame.pxl")
    report=json.loads((CAPTURE/"capture_report.json").read_text(encoding="utf-8"))
    earlier=json.loads(Path("work/emulation_v193/market_indicator_v248/capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"]==earlier["ROM_sha256"]==sha(ROM.read_bytes())
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert [r["PNG_sha256"] for r in report["frames_captured"]]==[r["PNG_sha256"] for r in earlier["frames_captured"]]
    state=report["read_only_native_state"]
    assert sha(Path(state["path"]).read_bytes())==state["sha256"]
    assert state["serialized_RAM_matches_same_frame_direct_export"] and state["main_RAM_unchanged_by_export"]
    assert not state["state_loaded"]
    for region in state["regions"].values():assert sha(Path(region["path"]).read_bytes())==region["sha256"]
    ram=Path(report["read_only_RAM_snapshot"]["path"]).read_bytes()
    assert sha(ram)==report["read_only_RAM_snapshot"]["sha256"]
    regs=state["ARM9_registers"];base=0x02000000
    header=regs[5]-struct.unpack_from("<I",raw,16)[0]
    assert ram[header-base:header-base+len(raw)]==raw
    assert regs[6]==header+20+9*32
    source_box=list(struct.unpack_from("<4I",ram,regs[7]-base))
    assert source_box==[0,224,32,32]
    itcm=Path(state["regions"]["ITCM"]["path"]).read_bytes()
    assert state["ARM9_instruction_address"]==0x01FFAFB0 and regs[15]==0x01FFAFB8
    assert struct.unpack_from("<I",itcm,0x2FB0)[0]==0xE1A04224
    assert struct.unpack_from("<I",itcm,0x2FB8)[0]==0xBAFFFFE6
    machines=[];factory=resources.machine
    def retain(source):
        u=factory(source);machines.append(u);return u
    with patch.object(resources,"machine",side_effect=retain):
        loaded=resources.native_views(rom,expected_paths={"/_pxl/__frame.pxl"},owner_range=(0x02313F60,0x02313F74))
    u=machines[0];view=0x02460020;cases=[]
    for value in range(1,6):
        u.mem_write(view-16,b"\xa5"*80);call(u,0xD3BD4,(view,))
        context=bytearray(0x80)
        for offset,number in [(0x10,value),(0x20,104),(0x40,8),(0x44,9),(0x48,0),(0x4C,216)]:struct.pack_into("<I",context,offset,number)
        u.mem_write(STACK,bytes(context));u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_R4,view)
        u.emu_start(0x020C3A38,0x020C3A80,count=100000)
        assert u.reg_read(UC_ARM_REG_PC)==0x020C3A80 and u.reg_read(UC_ARM_REG_SP)==STACK
        f=list(struct.unpack("<12I",u.mem_read(view,48)))
        assert f[3]==0x02313F60 and f[7:9]==[80+8*(value-1),216]
        assert f[9]&0xFFFF==9 and f[10:12]==[8,8]
        assert bytes(u.mem_read(view-16,16))==b"\xa5"*16 and bytes(u.mem_read(view+48,16))==b"\xa5"*16
        cases.append({"input_native_slot_type":value,"source_origin":f[7:9],"palette_bank":f[9]&0xFFFF,"extent":f[10:12],"view_guard_bytes_preserved":32})
    clean=NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    assert arm[0xC37B0:0xC3BB8]==clean[0xC37B0:0xC3BB8]
    assert arm[0xBCB80:0xBCC34]==clean[0xBCB80:0xBCC34]
    proof={"format":"dk4-market-native-source-v249","ROM_sha256":report["ROM_sha256"],
           "native_market_method":0x020C37B0,"native_slot_getters":{"occupied":0x020BCB80,"goods_id":0x020BCC1C,"indicator_type":0x020BCC04},
           "market_crop_fragment":[0x020C3A38,0x020C3A80],"market_type_crop_cases":cases,
           "original_market_and_getter_code_unchanged":True,"original_native_resource_load":loaded,
           "live_rasterizer_instruction":state["ARM9_instruction_address"],"live_pipelined_PC":regs[15],"live_source_header":header,
           "live_source_palette_pointer":regs[6],"live_source_pixels_pointer":regs[5],
           "complete_live_resource_bytes_exact":len(raw),"live_palette_bank":9,
           "live_source_descriptor":source_box,"live_descriptor_is_general_frame_tile_not_indicator":True,
           "all_43_captures_identical_with_optional_state_export":True,"serialized_main_RAM_matches_direct_export_and_remains_unchanged":True,
           "ITCM_DTCM_IO_OAM_and_CPU_read_only_export":state,
           "market_fragment_input_context_supplied_not_runtime_dispatch_trace":True,
           "actual_indicator_dispatch_and_gameplay_meaning_pending":True,"ROM_modified":False,
           "all_17_plaques_and_equipment_heading_remain_incomplete":True,"full_goal_complete":False}
    (ROOT/"proof.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"market_specific_native_crop_cases":5,"live_source_bytes_exact":len(raw),"unchanged_frame_captures":43,"ROM_modified":False}))


if __name__=="__main__":
    main()
