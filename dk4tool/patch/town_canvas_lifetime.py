"""Isolate the numeric bitmap and release town-only storage before movie setup."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_common_display_name_hook import branch_link

BASE=0x02000000
SOURCE='b03327187284a6ac560bf76ff442d75f9caa34c6b130438b582a44f2baf37c5b'
PRIVATE,CLEANUP,SLOT=0x01FFC828,0x01FFC504,0x01FFC8FC


def transform(source):
    if sha(source)!=SOURCE:
        raise ValueError('Town lifetime repair requires exact V484 ARM9')
    code=MainCodeFile(source,BASE)
    before=[bytes(s.data)for s in code.sections]
    assert len(before)==5 and code.sections[4].ramAddress==0x01FFC000 and len(before[4])==4096
    ks=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    changes=[]
    owned=[]
    for address,name,limit in ((PRIVATE,'town_canvas_private.asm',SLOT),(CLEANUP,'town_canvas_cleanup.asm',0x01FFC600)):
        text=Path(__file__).with_name(name).read_text(encoding='utf-8')
        blob=bytes(ks.asm(text,address)[0]);offset=address-0x01FFC000
        assert address+len(blob)<=limit and before[4][offset:offset+len(blob)]==bytes(len(blob))
        code.sections[4].data[offset:offset+len(blob)]=blob
        owned.append({'address':address,'bytes':len(blob),'assembly':name,'assembly_sha256':sha(text.encode('utf-8'))})
    assert before[4][SLOT-0x01FFC000:SLOT-0x01FFC000+4]==bytes(4)
    assert struct.unpack_from('<I',source,0xB5B00)[0]==0x022BD774
    for field,entry in ((0xB59AC,PRIVATE),(0xD2BDC,CLEANUP)):
        old=struct.unpack_from('<I',source,field)[0]
        if field==0xD2BDC:assert old==branch_link(BASE+field,BASE+0xD2E90)
        replacement=branch_link(BASE+field,entry)
        struct.pack_into('<I',code.sections[0].data,field,replacement)
        changes.append({'offset':field,'before':old,'after':replacement})
    target=bytes(code.save());parsed=MainCodeFile(target,BASE)
    restored=bytearray(parsed.sections[0].data)
    for row in changes:
        off=row['offset'];restored[off:off+4]=before[0][off:off+4]
    assert bytes(restored)==before[0] and all(bytes(parsed.sections[i].data)==before[i]for i in(1,2,3))
    restored=bytearray(parsed.sections[4].data)
    for row in owned:
        off=row['address']-0x01FFC000;restored[off:off+row['bytes']]=bytes(row['bytes'])
    assert bytes(restored)==before[4] and len(target)==len(source)
    return target,{'source_arm9_sha256':SOURCE,'target_arm9_sha256':sha(target),'changes':changes,'owned_code':owned,
                   'private_pointer_slot':SLOT,'shared_numeric_header':0x022BD774,'private_surface_size':[228,132],
                   'private_allocation_bytes':15104,'original_shared_header_size':[228,72],
                   'original_shared_header_and_VRAM_pixels_preserved':True,
                   'town_only_allocation_released_before_original_movie_heap_setup':True,
                   'all_section_sizes_startup_heap_boundary_and_cache_wrapper_exact':True,
                   'all124_commodity_names_and_all_prior_translation_payloads_preserved':True,
                   'changed_records':['TOWN_PRIVATE_NUMERIC_BITMAP_HEADER','TOWN_BITMAP_RELEASE_BEFORE_MOVIE'],
                   'full_goal_complete':False}


def apply_release(source,path):
    config=json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format']=='dk4-town-canvas-lifetime-v1' and sha(source)==config['source_arm9_sha256']
    target,report=transform(source)
    assert sha(target)==config['target_arm9_sha256']
    return target,report
