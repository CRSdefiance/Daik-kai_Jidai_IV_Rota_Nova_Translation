"""Scoped native-paper equipment hint and source-reviewed sailor skill labels."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_no_target import Assembly
from dk4tool.patch.two_screen_layout import tail
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "79636849c8581d65cef131bcd4c9224ba2ad2cd67e4e231a4dd727cd96a9bc35"
ROOT = Path("work/analysis/plaque_style_v247")


def paper_helper(address, state, previous, runs, count, width=88, height=16):
    a=Assembly()
    a.load(12,"state",state)
    a.emit(0xE59CC000)
    a.emit(0xE150000C)
    a.branch("original",1)
    # Apply the exact paper only to the verified 88x16 equipment heading.
    a.emit(0xE590C028); a.emit(0xE5901020); a.emit(0xE04CC001)
    if not 1<=width<=255 or not 1<=height<=255:
        raise ValueError("Paper helper dimensions exceed bounded ARM immediates")
    a.emit(0xE35C0000 | width); a.branch("original",1)
    a.emit(0xE590C02C); a.emit(0xE5901024); a.emit(0xE04CC001)
    a.emit(0xE35C0000 | height); a.branch("original",1)
    a.emit(0xE92D47F0)  # r4-r10/LR, eight words.
    a.emit(0xE24DD010)
    a.emit(0xE5907020); a.emit(0xE5908024); a.emit(0xE5909018)
    a.load(5,"runs",runs); a.load(6,"count",count)
    a.mark("loop")
    a.emit(0xE895000F)  # x,y,width,height
    a.emit(0xE0800007); a.emit(0xE0811008)
    a.emit(0xE88D000F)
    a.emit(0xE5951010)  # native BGR555 color
    a.emit(0xE1A00009); a.emit(0xE1A0200D); a.emit(0xE28D3008)
    a.emit(branch_link(address+len(a.words)*4,0x01FFAC18))
    a.emit(0xE2855014); a.emit(0xE2566001); a.branch("loop",1)
    a.emit(0xE28DD010); a.emit(0xE8BD87F0)
    a.mark("original")
    # r1 is ignored by the existing fill routine, which derives its rectangle.
    a.emit(tail(address+len(a.words)*4,previous))
    return a.finish()


def transform(source):
    if sha(source)!=SOURCE:
        raise ValueError("Exact complete V246 ARM9 required")
    code=MainCodeFile(source,BASE)
    before=[bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed=bytearray(before[3][:-48]); preserved=len(packed)
    names={}
    for old,new in ((0x0214833C,"Vigor"),(0x0214830C,"Speech"),(0x02148314,"Guile")):
        names[old]=POOL+len(packed);packed.extend(new.encode("ascii")+b"\0")
    packed.extend(bytes((-len(packed))%4))
    runs=POOL+len(packed);data=(ROOT/"tooltip_runs.bin").read_bytes();packed.extend(data)
    prior=json.loads(Path("work/analysis/two_screen_layout_v246/runtime_plan.json").read_text(encoding="utf-8"))
    entry=POOL+len(packed)
    helper=paper_helper(entry,prior["state_pointer"],prior["helpers"]["tooltip_fill"]["entry"],runs,len(data)//20)
    packed.extend(helper)
    changes=[]
    def replace(offset,expected,value):
        if struct.unpack_from("<I",source,offset)[0]!=expected:
            raise ValueError("Native source differs at "+hex(offset))
        struct.pack_into("<I",code.sections[0].data,offset,value)
        changes.append({"offset":offset,"before":expected,"after":value})
    for old,new in names.items():
        offsets=[i for i in range(0,len(before[0])-3,4) if struct.unpack_from("<I",before[0],i)[0]==old]
        required={0x0214833C:0x1483E4,0x0214830C:0x148400,0x02148314:0x148404}[old]
        if required not in offsets:
            raise ValueError("Reviewed native skill table pointer missing")
        for offset in offsets:
            replace(offset,old,new)
    if source[0x148334:0x14833C]!=b"Combat\0\0":
        raise ValueError("Original eight-byte swordsmanship caption differs")
    for offset,value in ((0x148334,int.from_bytes(b"Swor","little")),(0x148338,int.from_bytes(b"ds\0\0","little"))):
        replace(offset,struct.unpack_from("<I",source,offset)[0],value)
    # All skill names fit seven columns; the native getter clamps values to500.
    # Keep a ten-character row and reserve all three numeric digits.
    if source[0x148CC0:0x148CC8]!=b"%6s%4d\0\0":
        raise ValueError("Original skill row format differs")
    replace(0x148CC0,int.from_bytes(b"%6s%","little"),int.from_bytes(b"%7s%","little"))
    replace(0x148CC4,int.from_bytes(b"4d\0\0","little"),int.from_bytes(b"3d\0\0","little"))
    replace(0x6BDC,branch_link(BASE+0x6BDC,prior["helpers"]["tooltip_fill"]["entry"]),branch_link(BASE+0x6BDC,entry))
    packed.extend(bytes((-len(packed))%32));size=len(packed)+64
    if POOL+size>STAGE or STAGE+size+48>0x023F4000:
        raise ValueError("Plaque style exceeds owned arena")
    cache_entry,copy_entry=STAGE+len(packed),STAGE+size
    packed.extend(wrapper(cache_entry,copy_entry,size,source))
    code.sections[3].data=packed+before[3][-48:-4]+struct.pack("<I",size)
    replace(0x8E4,struct.unpack_from("<I",source,0x8E4)[0],branch_link(BASE+0x8E4,cache_entry))
    replace(0xE45DC,struct.unpack_from("<I",source,0xE45DC)[0],POOL+size)
    saved=bytes(code.save());loaded=MainCodeFile(saved,BASE)
    restored=bytearray(loaded.sections[0].data)
    for row in changes:
        o=row["offset"];restored[o:o+4]=before[0][o:o+4]
    o=code.codeSettingsOffs;restored[o:o+12]=before[0][o:o+12]
    if bytes(restored)!=before[0] or any(bytes(loaded.sections[n].data)!=before[n] for n in (1,2)) or bytes(loaded.sections[3].data[:preserved])!=before[3][:-48]:
        raise ValueError("Unrelated runtime bytes or inherited helpers changed")
    return saved,{"source_arm9_sha256":SOURCE,"target_arm9_sha256":sha(saved),"code_changes":changes,
                  "paper_helper_entry":entry,"previous_fill_entry":prior["helpers"]["tooltip_fill"]["entry"],
                  "state_pointer":prior["state_pointer"],"paper_runs":len(data)//20,"run_pointer":runs,
                  "skill_string_pointers":{hex(k):v for k,v in names.items()},"inherited_pool_bytes_preserved":preserved,
                  "cache":cache_plan(saved),"pool_payload_bytes":size,"unchanged_actual_stats_and_skill_values":True}


def apply_release(source,config_path):
    config=json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"]!="dk4-plaque-style-release-v1":
        raise ValueError("Unknown plaque style release")
    for path,digest in config["dependencies"].items():
        if sha(Path(path).read_bytes())!=digest:
            raise ValueError("Plaque dependency differs: "+path)
    saved,plan=transform(source)
    if sha(saved)!=config["target_arm9_sha256"]:
        raise ValueError("Plaque style target differs")
    plan["changed_records"]=["DK4_EQUIPMENT_NATIVE_TEXTURED_PAPER_V1","DK4_REVIEWED_SAILOR_SKILLS_AND_CREW_LIMITS_V1"]
    return saved,plan
