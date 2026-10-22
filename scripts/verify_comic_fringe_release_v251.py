"""Preservation, native whole-block readback and exact combined patch checks."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_native_archive_io_v191 import (
    BUFFER,
    CHUNK,
    NAME,
    OBJECT,
    SDK_CLOSE,
    SDK_OPEN,
    SDK_READ,
    SDK_SEEK,
)

ROOT=Path("work/analysis/comic_fidelity_v251")
ROM=Path("out/all_routes_combined_v251_candidate.nds")
PATH="/GRP/SLACKIMG.DK4"


def native_block(rom):
    arm=rom.read_file("/__arm9__.bin");original=NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/__arm9__.bin")
    for lo,hi in [(0xD0170,0xD051C),(0xD0590,0xD060C),(0xD1EE0,0xD2128)]:assert arm[lo:hi]==original[lo:hi]
    u=machine(arm);data=rom.read_file(PATH);archive=IlnkContainer.parse(data);handles={};events=[]
    def bridge(uc,address,size,_):
        if address not in (SDK_OPEN,SDK_READ,SDK_SEEK,SDK_CLOSE):return
        obj=uc.reg_read(UC_ARM_REG_R0)
        if address==SDK_OPEN:
            name=bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1),96)).split(b"\0")[0].decode("ascii")
            assert "/"+name.replace("\\","/").lstrip("/")==PATH and obj not in handles
            handles[obj]=0;uc.mem_write(obj+0x20,struct.pack("<2I",0,len(data)));result=1
        elif address==SDK_SEEK:
            offset=uc.reg_read(UC_ARM_REG_R1);assert uc.reg_read(UC_ARM_REG_R2)==0 and 0<=offset<=len(data)
            handles[obj]=offset;result=1
        elif address==SDK_READ:
            start=handles[obj];dest=uc.reg_read(UC_ARM_REG_R1);count=uc.reg_read(UC_ARM_REG_R2)
            assert start+count<=len(data);uc.mem_write(dest,data[start:start+count]);handles[obj]+=count;result=count
        else:
            del handles[obj];result=1
        events.append({"native_SDK_operation":address,"result":result})
        uc.reg_write(UC_ARM_REG_R0,result);uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    hook=u.hook_add(UC_HOOK_CODE,bridge);chunks=[];received=bytearray()
    try:
        u.mem_write(NAME,PATH.encode("ascii")+b"\0");u.mem_write(OBJECT-16,b"\xa5"*80)
        call(u,0xD2100,(OBJECT,));call(u,0xD2018,(OBJECT,NAME))
        assert u.reg_read(UC_ARM_REG_R0)==1
        assert struct.unpack("<I",u.mem_read(OBJECT+0x28,4))[0]==len(archive.blocks)
        expected=archive.blocks[19]
        for offset in range(0,len(expected),CHUNK):
            count=min(CHUNK,len(expected)-offset);u.mem_write(BUFFER-16,b"\xa5"*(count+32));u.mem_write(STACK,struct.pack("<I",count))
            trace=call(u,0xD1EF0,(OBJECT,BUFFER,19,offset));payload=bytes(u.mem_read(BUFFER,count))
            assert payload==expected[offset:offset+count] and u.reg_read(UC_ARM_REG_R0)==count
            assert bytes(u.mem_read(BUFFER-16,16))==bytes(u.mem_read(BUFFER+count,16))==b"\xa5"*16
            assert 0x020D1F50 in trace and 0x020D0170 in trace
            received.extend(payload);chunks.append({"offset":offset,"bytes":count})
        call(u,0xD2004,(OBJECT,));call(u,0xD20E0,(OBJECT,))
        assert not handles and bytes(received)==expected
        assert bytes(u.mem_read(OBJECT-16,16))==bytes(u.mem_read(OBJECT+44,16))==b"\xa5"*16
    finally:
        u.hook_del(hook)
    return {"block":19,"bytes":len(received),"sha256":sha(received),"chunks":chunks,"events":events,
            "native_directory_offsets_copies_return_ABI_and_canaries_pass":True,"all_handles_closed":True,
            "SDK_IO_bridged_to_exact_ROM":True,"generic_read_with_controlled_buffers_not_gallery_GPU_proof":True}


def main():
    prior=Path("out/all_routes_combined_v247_candidate.nds");assert (ROOT/"v247_reproduction.nds").read_bytes()==prior.read_bytes()
    old,new=NdsImage.open(prior),NdsImage.open(ROM);a={p:bytes(d) for _,p,d in old.iter_files()};b={p:bytes(d) for _,p,d in new.iter_files()}
    assert sorted(p for p in a if a[p]!=b[p])==[PATH]
    assert old.read_file("/__arm9__.bin")==new.read_file("/__arm9__.bin") and old.rom.arm7==new.rom.arm7
    assert old.rom.arm9OverlayTable==new.rom.arm9OverlayTable
    expected=(ROOT/"new_fringe_target.bin").read_bytes()
    assert IlnkContainer.parse(b[PATH]).blocks[19]==IlnkContainer.parse(expected).blocks[19]
    changed=[n for n,(x,y) in enumerate(zip(a[PATH],b[PATH],strict=True)) if x!=y];assert len(changed)==86
    before,after=IlnkContainer.parse(a[PATH]).blocks,IlnkContainer.parse(b[PATH]).blocks
    assert all(x==y for n,(x,y) in enumerate(zip(before,after,strict=True)) if n!=19)
    assert all(not((x^y)&0x8000) for (x,),(y,) in zip(struct.iter_unpack("<H",before[19]),struct.iter_unpack("<H",after[19]),strict=True))
    oldm=json.loads(prior.with_suffix(".manifest.json").read_text(encoding="utf-8"));m=json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    norm=lambda s:s.replace("\\","/")
    assert [norm(p) for p in m["batches"]]==["translations/gallery_chase_fringe_raw_art_v8.json" if norm(p)=="translations/gallery_reveal_comic_raw_art_v7.json" else norm(p) for p in oldm["batches"]]
    assert len(m["batches"])==467 and m["required_batches"]==oldm["required_batches"]
    for path,ids in oldm["changed_records"].items():assert set(ids)<=set(m["changed_records"][path])
    assert m["candidate_sha256"]==sha(ROM.read_bytes()) and m["release_stack_sha256"]==sha(Path("translations/release_stack.json").read_bytes())
    patch=ROM.with_suffix(".xdelta");clean=Path("work/clean.nds")
    assert sha(clean.read_bytes())=="f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,ROOT/"exact_patch_reconstruction.nds")
    assert (ROOT/"exact_patch_reconstruction.nds").read_bytes()==ROM.read_bytes()
    proof={"format":"dk4-comic-fringe-combined-v251","candidate":str(ROM),"candidate_sha256":sha(ROM.read_bytes()),"patch":str(patch),"patch_sha256":sha(patch.read_bytes()),
           "profile":m["profile"],"base_sha256":m["base_sha256"],"changed_internal_paths_vs_V247":[PATH],"changed_bytes":86,"changed_pixels":43,
           "complete_V247_reproduction_exact":True,"all467_batches_required_layers_records_and_terminal_stages_preserved":True,
           "all_route_scripts_ARM9_ARM7_overlay_and_other_graphics_unchanged":True,"all_color_flags_and_archive_allocation_unchanged":True,
           "exact_clean_patch_reconstruction":True,"native_changed_block":native_block(new),"cold_boot_regressions_pending":True,
           "raw_gallery_native_display_still_unproved":True,"all18_plaque_hint_audit_entries_incomplete":True,"full_goal_complete":False}
    (ROOT/"release_proof.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"candidate_sha256":proof["candidate_sha256"],"patch_sha256":proof["patch_sha256"],"native_block_bytes":proof["native_changed_block"]["bytes"],"changed_pixels":43}))


if __name__=="__main__":
    main()
