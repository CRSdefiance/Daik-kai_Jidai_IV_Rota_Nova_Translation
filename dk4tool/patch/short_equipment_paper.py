"""Versioned extension of the paper theme to observed Weapon/Armor hints."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.plaque_style import paper_helper
from dk4tool.patch.sailing_no_target import Assembly
from dk4tool.patch.two_screen_layout import tail
from scripts.probe_common_display_name_hook import branch_link

SOURCE="c43cae4f902c024c2502499f3748ad3f27098c83d98d456dcfbb22684a4fe870"
ROOT=Path("work/analysis/plaque_coverage_v252")


def transform(source):
    if sha(source)!=SOURCE:
        raise ValueError("Exact complete V251 ARM9 required")
    code=MainCodeFile(source,BASE);before=[bytes(s.data) for s in code.sections];cache_plan(source)
    prior=json.loads(Path("work/analysis/plaque_style_v247/runtime_plan.json").read_text(encoding="utf-8"))
    state=prior["state_pointer"];old_entry=prior["paper_helper_entry"]
    packed=bytearray(before[3][:-48]);preserved=len(packed);helpers={}
    for name,width in (("Armor",34),("Weapon",40)):
        data=(ROOT/(name.lower()+"_paper_runs.bin")).read_bytes()
        runs=POOL+len(packed);packed.extend(data);entry=POOL+len(packed)
        packed.extend(paper_helper(entry,state,old_entry,runs,len(data)//20,width=width))
        helpers[name]={"entry":entry,"width":width,"height":16,"run_pointer":runs,"runs":len(data)//20}
    dispatcher=POOL+len(packed);a=Assembly();a.load(12,"state",state)
    a.emit(0xE59CC000);a.emit(0xE150000C);a.branch("original",1)
    a.emit(0xE590C028);a.emit(0xE5901020);a.emit(0xE04CC001)
    for name in ("Armor","Weapon"):
        a.emit(0xE35C0000 | helpers[name]["width"])
        a.emit(tail(dispatcher+len(a.words)*4,helpers[name]["entry"]) & 0x0FFFFFFF)
    a.mark("original");a.emit(tail(dispatcher+len(a.words)*4,old_entry));packed.extend(a.finish())
    changes=[]
    def replace(offset,expected,value):
        if struct.unpack_from("<I",source,offset)[0]!=expected:
            raise ValueError("Short equipment source differs at "+hex(offset))
        struct.pack_into("<I",code.sections[0].data,offset,value);changes.append({"offset":offset,"before":expected,"after":value})
    replace(0x6BDC,branch_link(BASE+0x6BDC,old_entry),branch_link(BASE+0x6BDC,dispatcher))
    packed.extend(bytes((-len(packed))%32));size=len(packed)+64
    if POOL+size>STAGE or STAGE+size+48>0x023F4000:
        raise ValueError("Short equipment theme exceeds owned arena")
    entry,copy_entry=STAGE+len(packed),STAGE+size;packed.extend(wrapper(entry,copy_entry,size,source))
    code.sections[3].data=packed+before[3][-48:-4]+struct.pack("<I",size)
    replace(0x8E4,struct.unpack_from("<I",source,0x8E4)[0],branch_link(BASE+0x8E4,entry))
    replace(0xE45DC,struct.unpack_from("<I",source,0xE45DC)[0],POOL+size)
    saved=bytes(code.save());loaded=MainCodeFile(saved,BASE);restored=bytearray(loaded.sections[0].data)
    for row in changes:
        o=row["offset"];restored[o:o+4]=before[0][o:o+4]
    o=code.codeSettingsOffs;restored[o:o+12]=before[0][o:o+12]
    if bytes(restored)!=before[0] or any(bytes(loaded.sections[n].data)!=before[n] for n in (1,2)) or bytes(loaded.sections[3].data[:preserved])!=before[3][:-48]:
        raise ValueError("Inherited code/data or other runtime bytes changed")
    return saved,{"source_arm9_sha256":SOURCE,"target_arm9_sha256":sha(saved),"dispatcher_entry":dispatcher,
                  "old_paper_entry":old_entry,"state_pointer":state,"helpers":helpers,"changes":changes,
                  "inherited_pool_bytes_preserved":preserved,"payload_bytes":size,"cache":cache_plan(saved),
                  "only_two_observed_short_hint_geometries_added":True}


def apply_release(source,config_path):
    config=json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"]!="dk4-short-equipment-paper-release-v1":
        raise ValueError("Unknown short equipment paper release")
    for path,digest in config["dependencies"].items():
        if sha(Path(path).read_bytes())!=digest:
            raise ValueError("Short paper dependency differs: "+path)
    saved,plan=transform(source)
    if sha(saved)!=config["target_arm9_sha256"]:
        raise ValueError("Short equipment target differs")
    plan["changed_records"]=["DK4_SHORT_WEAPON_ARMOR_PAPER_V1"]
    return saved,plan
