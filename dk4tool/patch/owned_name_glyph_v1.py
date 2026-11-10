"""Plan an exclusively owned, fixed-size name-data glyph correction; no ROM mutation."""
import struct
from ndspy.code import MainCodeFile
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha

def plan_arm9_name_glyph(arm,proposal):
    if sha(arm)!=proposal['runtime']['ARM9_sha256']:
        raise ValueError('Exact registered ARM9 name-data parent required')
    at=proposal['ARM9_physical_offset'];pointer=proposal['actual_RAM_pointer']
    old,new=[bytes.fromhex(proposal[k]) for k in ['source_hex','target_hex']]
    if not len(old)==len(new)==proposal['owned_bytes']==8 or arm[at:at+8]!=old or arm.count(old)!=1:
        raise ValueError('One exact eight-byte owned source name slot required')
    if old.decode('cp932').rstrip('\0').replace('Ｆ','F')!=new.decode('ascii').rstrip('\0'):
        raise ValueError('Only the declared normal-width F spelling may change')
    table=struct.unpack_from('<I',arm,0xCDAC0)[0];owners=[]
    for actor in range(207):
        for column in [0,4,8]:
            field=table+32*actor+column
            value=struct.unpack_from('<I',arm,field-BASE)[0]
            if pointer<=value<pointer+8:owners.append(dict(actor=actor,column=column,pointer=value))
    if owners!=proposal['all207_name_fields_interior_oralias_owners'] or owners!=[dict(actor=14,column=4,pointer=pointer)]:
        raise ValueError('Exclusive actor14 surname ownership including interior aliases required')
    if arm[at+8:at+16].hex()!=proposal['following8_Ferid_hex']:
        raise ValueError('Following complete Ferid slot must remain exact')
    before=MainCodeFile(arm,BASE).sections
    payload=bytes(before[3].data[:-48]);offset=pointer-POOL
    if len(payload)!=123264 or payload[offset:offset+8]!=old:
        raise ValueError('Complete original staged name-data mapping required')
    target=arm[:at]+new+arm[at+8:];after=MainCodeFile(target,BASE).sections
    if len(before)!=len(after) or len(target)!=len(arm):raise ValueError('Section or ARM9 size changed')
    for i,(a,b) in enumerate(zip(before,after,strict=True)):
        if a.ramAddress!=b.ramAddress or len(a.data)!=len(b.data):raise ValueError('Section allocation changed')
        expected=bytes(a.data)
        if i==3:expected=expected[:offset]+new+expected[offset+8:]
        if bytes(b.data)!=expected:raise ValueError('Unowned staged payload or other section changed')
    if target[:at]+old+target[at+8:]!=arm:raise ValueError('Complete name-data inverse failed')
    return target,dict(parent_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),physical_offset=at,
        RAM_pointer=pointer,exclusive_owners=owners,old_hex=old.hex(),new_hex=new.hex(),
        all_unowned_ARM9_bytes_sections_allocations_andpayload_size_exact=True,
        source_andtarget_executable_code_fonts_pointer_table_andstartup_unchanged=True,
        complete_parent_inverse_exact=True,no_ROM_mutation=True)
