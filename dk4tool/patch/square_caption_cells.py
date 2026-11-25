"""Private 68-pixel render surface, copied into the original 64-pixel caption.

The native six-pixel glyph cell can otherwise suppress a final letter whose ink
fits a 64-pixel caption. Only Square's exact 64x12, 4-bit contract is handled.
"""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, target, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = 'c425bd54d4158a342f38a3950a02160d264eb645bd946cabf84dbe24aeaea2ce'


def assemble(text, address):
    return bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(text, address)[0])


def paint(address, buffer, original):
    return assemble(f'''
push {{r4-r10,lr}}
mov r4,r0
mov r10,r1
ldr r5,[r4,#44]
cmp r5,#0
beq fallback
ldr r6,[r5,#16]
cmp r6,#0
beq fallback
ldr r2,[r6]
cmp r2,#4
bne fallback
ldr r2,[r6,#4]
cmp r2,#16
bne fallback
ldr r2,[r6,#8]
cmp r2,#12
bne fallback
ldr r2,[r5,#40]
cmp r2,#64
bne fallback
ldr r2,[r5,#44]
cmp r2,#12
bne fallback
ldr r2,[r4,#4]
ldr r3,[r4,#8]
orr r2,r2,r3
ldr r3,[r4,#36]
orr r2,r2,r3
ldr r3,[r4,#40]
orrs r2,r2,r3
bne fallback
ldr r2,[r4,#12]
cmp r2,#64
bne fallback
ldr r2,[r4,#16]
cmp r2,#12
bne fallback
ldr r7,[r6,#16]
add r7,r6,r7
ldr r8,buffer_address
mov r2,#4
str r2,[r8]
mov r2,#17
str r2,[r8,#4]
mov r2,#12
str r2,[r8,#8]
ldr r2,[r6,#12]
add r2,r6,r2
sub r2,r2,r8
str r2,[r8,#12]
mov r2,#20
str r2,[r8,#16]
mov r0,r7
add r1,r8,#20
mov r2,#12
copy_in_row:
mov r3,#16
copy_in_halfword:
ldrh r9,[r0],#2
strh r9,[r1],#2
subs r3,r3,#1
bne copy_in_halfword
mov r9,#0
strh r9,[r1],#2
subs r2,r2,#1
bne copy_in_row
str r8,[r5,#16]
mov r2,#68
str r2,[r5,#40]
str r2,[r4,#12]
mov r0,r4
mov r1,r10
bl {original}
mov r10,r0
str r6,[r5,#16]
mov r2,#64
str r2,[r5,#40]
str r2,[r4,#12]
add r0,r8,#20
mov r1,r7
mov r2,#12
copy_out_row:
mov r3,#16
copy_out_halfword:
ldrh r9,[r0],#2
strh r9,[r1],#2
subs r3,r3,#1
bne copy_out_halfword
add r0,r0,#2
subs r2,r2,#1
bne copy_out_row
mov r0,r10
pop {{r4-r10,pc}}
fallback:
mov r0,r4
mov r1,r10
pop {{r4-r10,lr}}
b {original}
buffer_address: .word {buffer}
''', address)


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Square caption repair requires exact V474 ARM9')
    code = MainCodeFile(source,BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    buffer = POOL + len(packed)
    packed.extend(bytes(448))
    name = POOL + len(packed)
    packed.extend(b'Delicacy\0')
    packed.extend(bytes((-len(packed))%4))
    category_entry = POOL + len(packed)
    old_category = target(source,0x5FDA8)
    category = assemble(f'''push {{r4,lr}}
mov r4,r0
bl {old_category}
cmp r4,#2
ldreq r0,name_address
pop {{r4,pc}}
name_address: .word {name}''',category_entry)
    packed.extend(category)
    paint_entry = POOL + len(packed)
    old_paint = target(source,0x5FDC4)
    body = paint(paint_entry,buffer,old_paint)
    packed.extend(body)
    changes = []

    def replace(offset,value):
        old = struct.unpack_from('<I',source,offset)[0]
        struct.pack_into('<I',code.sections[0].data,offset,value)
        changes.append({'offset':offset,'before':old,'after':value})

    replace(0x5FDA8,branch_link(BASE+0x5FDA8,category_entry))
    replace(0x5FDC4,branch_link(BASE+0x5FDC4,paint_entry))
    packed.extend(bytes((-len(packed))%32))
    size = len(packed)+64
    if POOL+size > STAGE or STAGE+size+48 > 0x023F4000:
        raise ValueError('Square caption helper exceeds owned arena')
    cache_entry,copy = STAGE+len(packed),STAGE+size
    packed.extend(wrapper(cache_entry,copy,size,source))
    code.sections[3].data = packed+before[3][-48:-4]+struct.pack('<I',size)
    replace(0x8E4,branch_link(BASE+0x8E4,cache_entry))
    replace(0xE45DC,POOL+size)
    result = bytes(code.save())
    parsed = MainCodeFile(result,BASE)
    restored = bytearray(parsed.sections[0].data)
    for row in changes:
        off=row['offset'];restored[off:off+4]=before[0][off:off+4]
    off=code.codeSettingsOffs;restored[off:off+12]=before[0][off:off+12]
    assert bytes(restored)==before[0]
    assert all(bytes(parsed.sections[i].data)==before[i] for i in (1,2,4))
    assert bytes(parsed.sections[3].data[:preserved])==before[3][:-48]
    return result,{'source_arm9_sha256':SOURCE,'target_arm9_sha256':sha(result),'changes':changes,
                   'private_buffer':buffer,'private_buffer_bytes':448,'paint_entry':paint_entry,
                   'original_paint':old_paint,'category_entry':category_entry,'original_category':old_category,
                   'name_address':name,'inherited_pool_bytes_preserved':preserved,'cache':cache_plan(result),
                   'visible_caption_size':[64,12],'private_render_size':[68,12],
                   'changed_records':['SQUARE_CAPTION_FINAL_GLYPH_CELL','SQUARE_CATEGORY_2_DELICACY'],
                   'all_other_shared_category_names_unchanged':True,'goal_complete':False}


def apply_release(source,path):
    config=json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] in ('dk4-square-caption-cells-v1','dk4-square-caption-cells-v2') and sha(source)==config['source_arm9_sha256']
    result,report=(fixed_transform(source) if config['format'].endswith('v2') else transform(source))
    assert sha(result)==config['target_arm9_sha256']
    return result,report


def fixed_transform(source):
    """Reuse the documented zero gap after the market helper; no section growth.

    The market helper ends at C19C, its vtable begins at C600 and persistent
    pointer lives at C680. Its pixel surface is heap-allocated, not in this gap.
    """
    if sha(source)!=SOURCE:
        raise ValueError('Fixed Square repair requires exact V474 ARM9')
    code=MainCodeFile(source,BASE)
    before=[bytes(s.data) for s in code.sections]
    assert len(before)==5 and code.sections[4].ramAddress==0x01FFC000 and len(before[4])==4096
    start,end=0x01FFC1A0,0x01FFC600
    offset=start-0x01FFC000
    assert before[4][offset:end-0x01FFC000]==bytes(end-start)
    # No existing aligned literal points into the owned gap.
    assert not [(off,struct.unpack_from('<I',source,off)[0]) for off in range(0,len(source)-3,4)
                if start<=struct.unpack_from('<I',source,off)[0]<end]
    buffer=start
    packed=bytearray(448)
    name=start+len(packed)
    packed.extend(b'Delicacy\0');packed.extend(bytes((-len(packed))%4))
    category_entry=start+len(packed)
    old_category=target(source,0x5FDA8)
    packed.extend(assemble(f'''push {{r4,lr}}
mov r4,r0
bl {old_category}
cmp r4,#2
ldreq r0,name_address
pop {{r4,pc}}
name_address: .word {name}''',category_entry))
    paint_entry=start+len(packed)
    old_paint=target(source,0x5FDC4)
    packed.extend(paint(paint_entry,buffer,old_paint))
    assert start+len(packed)<=end
    code.sections[4].data[offset:offset+len(packed)]=packed
    changes=[]
    for field,entry in ((0x5FDA8,category_entry),(0x5FDC4,paint_entry)):
        old=struct.unpack_from('<I',source,field)[0]
        replacement=branch_link(BASE+field,entry)
        struct.pack_into('<I',code.sections[0].data,field,replacement)
        changes.append({'offset':field,'before':old,'after':replacement})
    result=bytes(code.save())
    parsed=MainCodeFile(result,BASE)
    restored=bytearray(parsed.sections[0].data)
    for row in changes:
        off=row['offset'];restored[off:off+4]=before[0][off:off+4]
    assert bytes(restored)==before[0] and all(bytes(parsed.sections[i].data)==before[i] for i in (1,2,3))
    restored=bytearray(parsed.sections[4].data);restored[offset:offset+len(packed)]=bytes(len(packed))
    assert bytes(restored)==before[4] and len(result)==len(source)
    return result,{'source_arm9_sha256':SOURCE,'target_arm9_sha256':sha(result),'changes':changes,
                   'private_buffer':buffer,'private_buffer_bytes':448,'paint_entry':paint_entry,
                   'original_paint':old_paint,'category_entry':category_entry,'original_category':old_category,
                   'name_address':name,'owned_zero_gap':[start,end],'owned_bytes_written':len(packed),
                   'inherited_pool_bytes_preserved':len(before[3])-48,'cache':cache_plan(result),
                   'all_section_extents_startup_heap_and_cache_wrapper_exact':True,
                   'visible_caption_size':[64,12],'private_render_size':[68,12],
                   'changed_records':['SQUARE_CAPTION_FINAL_GLYPH_CELL','SQUARE_CATEGORY_2_DELICACY'],
                   'all_other_shared_category_names_unchanged':True,'goal_complete':False}
