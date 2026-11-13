"""Scoped Square caption canvases preserve complete natural shop labels."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_no_target import Assembly, mov_immediate
from dk4tool.patch.two_screen_layout import tail
from scripts.probe_common_display_name_hook import branch_link

SOURCE="b42d52c95f7c8773c757c604a66629ab00038cbd54df452f2a43f4c962208c6c"
ROOT=Path("work/analysis/occupied_equipment_v253")
SLOT_BYTES=416


def canvas_helper(address,buffers):
    a=Assembly();a.emit(0xE92D43F0);a.emit(0xE24DD014)
    a.emit(0xE1A09004);a.emit(0xE1A06000);a.emit(0xE1A07001);a.emit(0xE1A08002);a.emit(0xE1A05003)
    a.emit(branch_link(address+len(a.words)*4,BASE+0xCB124))
    a.emit(0xE0800209);a.emit(0xE5D09010);a.emit(0xE3590012);a.branch("fallback",10)
    a.load(12,"buffers",buffers);a.emit(mov_immediate(4,SLOT_BYTES));a.emit(0xE024C499)
    a.emit(0xE897100F);a.emit(0xE0833007);a.emit(0xE0433004)
    a.emit(0xE3A01010);a.emit(0xE3A0C014);a.emit(0xE884100F)
    a.emit(0xE59D1034);a.emit(0xE59D2038);a.emit(0xE59D303C);a.emit(0xE3A00040);a.emit(0xE88D000F)
    a.emit(0xE1A00006);a.emit(0xE1A01004);a.branch("construct")
    a.mark("fallback")
    a.emit(0xE28DC030);a.emit(0xE89C000F);a.emit(0xE88D000F)
    a.emit(0xE1A00006);a.emit(0xE1A01007)
    a.mark("construct")
    a.emit(0xE1A02008);a.emit(0xE1A03005)
    a.emit(branch_link(address+len(a.words)*4,BASE+0xD3AFC))
    a.emit(0xE28DD014);a.emit(0xE8BD83F0)
    return a.finish()


def category_helper(address,jewelry):
    a=Assembly();a.emit(0xE92D4010);a.emit(branch_link(address+len(a.words)*4,BASE+0xC5BA0))
    a.load(1,"old",BASE+0x15A0FC);a.emit(0xE1500001);a.branch("done",1)
    a.load(0,"jewelry",jewelry);a.mark("done");a.emit(0xE8BD8010)
    return a.finish()


def paint_helper(address):
    # Generic text context+1C is glyph tracking; +44 belongs to the derived
    # bitmap renderer and must retain its original constructor value.
    return struct.pack("<3I",0xE3E0C000,0xE580C01C,tail(address+8,BASE+0xD5404))


def transform(source):
    if sha(source)!=SOURCE:raise ValueError("Exact full V252 ARM9 required")
    code=MainCodeFile(source,BASE);before=[bytes(s.data) for s in code.sections];cache_plan(source)
    packed=bytearray(before[3][:-48]);preserved=len(packed);buffers=POOL+len(packed);packed.extend(bytes(SLOT_BYTES*18))
    jewelry=POOL+len(packed);packed.extend(b"Jewelry\0");packed.extend(bytes((-len(packed))%4));helpers={}
    for name,factory in [("canvas",lambda at:canvas_helper(at,buffers)),("category",lambda at:category_helper(at,jewelry)),("paint",paint_helper)]:
        entry=POOL+len(packed);blob=factory(entry);helpers[name]={"entry":entry,"bytes":len(blob)};packed.extend(blob)
    changes=[]
    def replace(offset,expected,new):
        if struct.unpack_from("<I",source,offset)[0]!=expected:raise ValueError("Square source differs at "+hex(offset))
        struct.pack_into("<I",code.sections[0].data,offset,new);changes.append({"offset":offset,"before":expected,"after":new})
    for off,original,name in [(0x5FD80,0xD3AFC,"canvas"),(0x5FDA8,0xC5BA0,"category"),(0x5FDC4,0xD5404,"paint")]:
        replace(off,branch_link(BASE+off,BASE+original),branch_link(BASE+off,helpers[name]["entry"]))
    packed.extend(bytes((-len(packed))%32));size=len(packed)+64
    if POOL+size>STAGE or STAGE+size+48>0x023F4000:raise ValueError("Square label storage exceeds owned arena")
    entry,copy=STAGE+len(packed),STAGE+size;packed.extend(wrapper(entry,copy,size,source));code.sections[3].data=packed+before[3][-48:-4]+struct.pack("<I",size)
    replace(0x8E4,struct.unpack_from("<I",source,0x8E4)[0],branch_link(BASE+0x8E4,entry));replace(0xE45DC,struct.unpack_from("<I",source,0xE45DC)[0],POOL+size)
    saved=bytes(code.save());loaded=MainCodeFile(saved,BASE);restored=bytearray(loaded.sections[0].data)
    for row in changes:o=row["offset"];restored[o:o+4]=before[0][o:o+4]
    o=code.codeSettingsOffs;restored[o:o+12]=before[0][o:o+12]
    if bytes(restored)!=before[0] or any(bytes(loaded.sections[n].data)!=before[n] for n in (1,2)) or bytes(loaded.sections[3].data[:preserved])!=before[3][:-48]:raise ValueError("Unrelated code/data or inherited payload changed")
    return saved,{"source_arm9_sha256":SOURCE,"target_arm9_sha256":sha(saved),"helpers":helpers,"buffers":buffers,"slot_bytes":SLOT_BYTES,"slots":18,"new_canvas":[64,12],"changes":changes,"cache":cache_plan(saved),"payload_bytes":size,"inherited_pool_bytes_preserved":preserved,
                  "only_square_caption_uses_Jewelry_term_and_five_pixel_tracking":True,"original_menu_borders_and_shared_category_names_unchanged":True}


def apply_release(source,path):
    config=json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"]!="dk4-square-shop-label-release-v1":raise ValueError("Unknown Square label release")
    for file,digest in config["dependencies"].items():
        if sha(Path(file).read_bytes())!=digest:raise ValueError("Square label dependency differs: "+file)
    saved,plan=transform(source)
    if sha(saved)!=config["target_arm9_sha256"]:raise ValueError("Square label target differs")
    plan["changed_records"]=["DK4_SQUARE_COMPLETE_SHOP_CAPTIONS_V1"]
    return saved,plan
