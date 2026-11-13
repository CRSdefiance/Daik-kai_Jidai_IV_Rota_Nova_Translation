"""Full names only for the original730 caller; preserve all compact menu names.

Reuse the original18-word lookup table,140-byte string family and existing
Square helper code. Two duplicate Fleet labels and Dock B point to complete
existing immutable UI strings before their owned slots receive code.
"""

import struct

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL, cache_plan
from dk4tool.patch.town_stock_rows import scatter
from dk4tool.rom.nds import NdsImage

BASE=0x02000000
TABLE=0x11B444
FAMILY=(0x15A090,0x15A11C)
GETTER=BASE+0xC5BA0
OUTER,INNER=0x01FFC36C,0x0239AFC8
FLEET_B,FLEET_C,DOCK_B=0x151730,0x15174C,0x151760
FLEET_ALIAS,DOCK_ALIAS=BASE+0x143C43,BASE+0x151728
ADDRESS_BASE=0x01800000
OLD_NAMES=('Food','Cond.','Delic.','Spices','Treats','Liquor','Metals','Crafts','Fiber','Luxury','Scents','Jewels','Gems','Med','Dyes','Arms','Ore','Goods')


def transform(arm):
    code=MainCodeFile(arm,BASE)
    before=[bytes(s.data) for s in code.sections]
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert code.sections[4].ramAddress==0x01FFC000 and len(before[4])==4096
    assert arm[FLEET_ALIAS-BASE-7:FLEET_ALIAS-BASE+6]==b'Create Fleet\0'
    assert arm[DOCK_ALIAS-BASE:DOCK_ALIAS-BASE+5]==b'Dock\0'
    assert arm[FLEET_B:FLEET_B+20]==arm[FLEET_C:FLEET_C+20]==b'Fleet\0'+bytes(14)
    assert arm[DOCK_B:DOCK_B+8]==b'Dock\0'+bytes(3)
    for start in (FLEET_B,FLEET_C):
        assert clean[start:start+20]=='隊列　　　　　　　　'.encode('cp932')
    assert clean[DOCK_B:DOCK_B+8]=='ドック'.encode('cp932')+bytes(2)
    pointers=struct.unpack_from('<18I',arm,TABLE)
    assert tuple(arm[p-BASE:arm.index(0,p-BASE)].decode('ascii') for p in pointers)==OLD_NAMES
    # All literal/unaligned word owners are explicit. The inner Square helper
    # has the sole extra category-string pointer, its old Jewels comparison.
    category_owners=[];label_owners=[];table_owners=[]
    for si,s in enumerate(code.sections):
        for at in range(len(s.data)-3):
            value=struct.unpack_from('<I',s.data,at)[0]
            if BASE+FAMILY[0]<=value<BASE+FAMILY[1]:category_owners.append((si,at,value))
            if value==BASE+TABLE:table_owners.append((si,at))
            for lo,hi,alias in ((FLEET_B,FLEET_B+20,FLEET_ALIAS),(FLEET_C,FLEET_C+20,FLEET_ALIAS),(DOCK_B,DOCK_B+8,DOCK_ALIAS)):
                if BASE+lo<=value<BASE+hi:
                    assert value==BASE+lo,(si,at,value)
                    label_owners.append((si,at,value,alias))
    expected={(0,TABLE+i*4,pointers[i]) for i in range(18)}
    expected.add((3,INNER-POOL+28,pointers[11]))
    assert set(category_owners)==expected and table_owners==[(0,0xC5BB4)]
    assert [(si,at,value) for si,at,value,_ in label_owners]==[
        (0,0x15163C,BASE+FLEET_B),(0,0x151640,BASE+FLEET_B),(0,0x151644,BASE+FLEET_C)]
    # Dock B is already an unreferenced duplicate; Dock A remains untouched.
    old_outer=before[4][OUTER-0x01FFC000:OUTER-0x01FFC000+28]
    old_inner=before[3][INNER-POOL:INNER-POOL+36]
    assert struct.unpack_from('<I',old_outer,24)[0]==0x01FFC360
    assert struct.unpack_from('<I',old_inner,28)[0]==pointers[11]
    jewelry=struct.unpack_from('<I',old_inner,32)[0]
    def memory(address,size):
        if POOL<=address and address+size<=POOL+len(before[3])-48:return before[3][address-POOL:address-POOL+size]
        for si,s in enumerate(code.sections):
            if s.ramAddress<=address and address+size<=s.ramAddress+len(s.data):return before[si][address-s.ramAddress:address-s.ramAddress+size]
        raise AssertionError(hex(address))
    assert memory(0x01FFC360,9)==b'Delicacy\0' and memory(jewelry,8)==b'Jewelry\0'
    medicine=BASE+0x15EBA8;assert memory(medicine,9)==b'Medicine\0'
    assert arm[0xC5BA0:0xC5BB8]==clean[0xC5BA0:0xC5BB8]
    ks=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    expected_outer=bytes(ks.asm(f'push {{r4,lr}}; mov r4,r0; bl {INNER}; cmp r4,#2; ldreq r0,name; pop {{r4,pc}}; name: .word 0x01FFC360',OUTER)[0])
    expected_inner=bytes(ks.asm(f'push {{r4,lr}}; bl {GETTER}; ldr r1,old; cmp r0,r1; bne done; ldr r0,jewelry; done: pop {{r4,pc}}; old: .word {pointers[11]}; jewelry: .word {jewelry}',INNER)[0])
    assert old_outer==expected_outer and old_inner==expected_inner
    branch_owners=[];absolute_code_owners=[]
    ranges=((GETTER,GETTER+24),(OUTER,OUTER+28),(INNER,INNER+36),(BASE+FLEET_B,BASE+FLEET_B+20),(BASE+FLEET_C,BASE+DOCK_B+8))
    for si,s in enumerate(code.sections):
        runtime=POOL if si==3 else s.ramAddress
        for at in range(len(s.data)-3):
            value=struct.unpack_from('<I',s.data,at)[0]
            if any(lo<=value<hi for lo,hi in ranges[:3]):absolute_code_owners.append((si,at,value))
            if at%4==0 and value&0x0E000000==0x0A000000:
                delta=value&0xffffff;delta=delta-(1<<24) if delta&(1<<23) else delta
                target=runtime+at+8+delta*4
                if any(lo<=target<hi for lo,hi in ranges):branch_owners.append((runtime+at,target))
    assert absolute_code_owners==[]
    assert set(branch_owners)=={(BASE+site,GETTER) for site in (0x5FC44,0xBE800,0xBEF14,0xC3DE8,0xC3F64,0xF2028)}|{(INNER+4,GETTER),(INNER+16,INNER+24),(BASE+0x5FDA8,OUTER),(OUTER+8,INNER)},branch_owners
    # Preserve exact compact words. Share the complete Metals suffix of the
    # new Precious Metals string; every selected pointer still ends at NUL.
    names=set(OLD_NAMES)|{'Seasonings','Precious Metals','Sundries'}
    roots=sorted((s for s in names if not any(t.endswith(' '+s) for t in names)),key=lambda s:(-len(s),s))
    payload=bytearray();addresses={}
    for text in roots:
        addresses[text]=BASE+FAMILY[0]+len(payload);payload.extend(text.encode('ascii')+b'\0')
    for text in names:
        if text not in addresses:
            root=next(s for s in roots if s.endswith(' '+text));addresses[text]=addresses[root]+len(root)-len(text)
    assert len(payload)==138 and all(0<=addresses[s]-BASE-FAMILY[0]<256 for s in OLD_NAMES)
    full=[addresses[s] for s in OLD_NAMES]
    for i,p in {1:addresses['Seasonings'],2:0x01FFC360,6:addresses['Precious Metals'],11:jewelry,13:medicine,17:addresses['Sundries']}.items():full[i]=p
    code.sections[0].data[FAMILY[0]:FAMILY[1]]=payload+bytes(FAMILY[1]-FAMILY[0]-len(payload))
    for i,p in enumerate(full):
        assert 0<=p-ADDRESS_BASE<0x1000000
        packed=(addresses[OLD_NAMES[i]]-BASE-FAMILY[0])<<24 | (p-ADDRESS_BASE)
        struct.pack_into('<I',code.sections[0].data,TABLE+i*4,packed)
    for si,at,_,alias in label_owners:struct.pack_into('<I',code.sections[si].data,at,alias)
    square=bytes(ks.asm(f'''push {{r4,lr}}; mov r4,r0; bl {GETTER}; cmp r4,#2; ldreq r0,delicacy; cmp r4,#11; ldreq r0,jewelry; pop {{r4,pc}}; delicacy: .word 0x01FFC360; jewelry: .word {jewelry}''',OUTER)[0])
    assert len(square)==40
    square_patches,_=scatter(square,32,OUTER,[(OUTER,OUTER+28),(INNER,INNER+16)])
    # Keep negative/sentinel behavior before decoding the packed positive row.
    # Only the exact original730 return PC selects the full pointer.
    getter=bytes(ks.asm(f'''cmp r0,#18; movge r0,#0; bxge lr
ldr r1,table; cmp r0,#0; ldr r1,[r1,r0,lsl #2]; movlt r0,r1; bxlt lr
ldr r0,dialogue_return; cmp lr,r0
biceq r0,r1,#0xff000000; addeq r0,r0,#{ADDRESS_BASE}
movne r0,r1,lsr #24; ldrne r1,family; addne r0,r1,r0; bx lr
table: .word {BASE+TABLE}
dialogue_return: .word 0x0205FC48
family: .word {BASE+FAMILY[0]}''',GETTER)[0])
    assert len(getter)==76
    blocks=[(GETTER,GETTER+24),(BASE+FLEET_B,BASE+FLEET_B+20),(BASE+FLEET_C,BASE+DOCK_B+8),(INNER+16,INNER+36)]
    getter_patches,_=scatter(getter,64,GETTER,blocks)
    changed=[]
    for address,data in (*square_patches,*getter_patches):
        if POOL<=address and address+len(data)<=POOL+len(before[3])-48:si,at=3,address-POOL
        elif 0x01FFC000<=address<0x01FFD000:si,at=4,address-0x01FFC000
        else:si,at=0,address-BASE
        code.sections[si].data[at:at+len(data)]=data;changed.append((si,at,len(data)))
    target=bytes(code.save());parsed=MainCodeFile(target,BASE)
    restored=[bytearray(s.data) for s in parsed.sections]
    for si,at,size in changed:restored[si][at:at+size]=before[si][at:at+size]
    for si,at,_,_ in label_owners:restored[si][at:at+4]=before[si][at:at+4]
    restored[0][FAMILY[0]:FAMILY[1]]=before[0][FAMILY[0]:FAMILY[1]]
    restored[0][TABLE:TABLE+72]=before[0][TABLE:TABLE+72]
    assert all(bytes(a)==b for a,b in zip(restored,before,strict=True))
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in parsed.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in code.sections]
    assert cache_plan(arm)==cache_plan(target)
    return target,{'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),
        'packed_original18_word_table':TABLE,'category_family':list(FAMILY),'used_family_bytes':len(payload),
        'original_category_pointer_owners':[list(r) for r in category_owners],
        'existing_code_branch_owners':[list(r) for r in branch_owners],
        'no_absolute_or_interior_code_aliases':True,
        'rebound_duplicate_Fleet_Dock_label_owners':[list(r) for r in label_owners],
        'existing_immutable_Fleet_suffix':'Create Fleet','full_pointers':full,
        'compact_pointers':[addresses[s] for s in OLD_NAMES],
        'existing_code_and_owned_label_patch_spans':[list(r) for r in changed],
        'only_full_name_caller_return':0x0205FC48,'all_mutable_caption_buffers_startup_pool_cache_shapes_preserved':True,
        'native_ABI_menu_and_dialogue_verification_pending':True,'full_goal_complete':False}
