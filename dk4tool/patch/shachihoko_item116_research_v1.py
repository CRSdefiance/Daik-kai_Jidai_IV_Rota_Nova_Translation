"""Coordinated source-bound item116 storage research;expanded pool requires actual boot proof."""
import struct,textwrap
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shachihoko_item_name_data_v1 import transform as title_transform,STORAGE,NEW
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL,STAGE,cache_plan,wrapper
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.probe_common_display_name_hook import branch_link

def transform(source,common,clean,doc,binding):
    assert sha(source)==doc['current_ARM9_sha256']==binding['ARM9_sha256'] and sha(common)==doc['current_COMMON_sha256']==binding['COMMON_sha256']
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and len(doc['records'])==2
    title,description=doc['records'];assert description['message_id']==2931 and description['item_ID']==116
    for row in doc['records']:
        assert all(row['review'][k] is True for k in ['source','context','localization','naturalness'])
        assert not any(c in row['english'] for c in ['\n','\r','{','%']) and row['english'].encode('ascii').decode('ascii')==row['english']
    titled,title_plan=title_transform(source,clean,title)
    entries=owned_entries(common,source,binding['COMMON_directory_sha256']);selected=entries[2931]
    assert selected.text.hex()==description['current_text_hex'] and selected.block==32
    blocks=IlnkContainer.parse(common).blocks;oldblock=blocks[32];oldspan=oldblock[selected.block_offset:selected.copy_end]
    raw=description['english'].encode('ascii');newspan=raw+b'\0';delta=len(newspan)-len(oldspan)
    newblock=oldblock[:selected.block_offset]+newspan+oldblock[selected.copy_end:];assert 0<len(newblock)<=8192
    assert newblock[:selected.block_offset]+oldspan+newblock[selected.block_offset+len(newspan):]==oldblock
    rebuilt=list(blocks);rebuilt[32]=newblock;newcommon=IlnkContainer(rebuilt).to_bytes();assert IlnkContainer.parse(newcommon).blocks==rebuilt
    code=MainCodeFile(titled,BASE);before=MainCodeFile(source,BASE);original_parts=[bytes(s.data) for s in before.sections]
    assert len(code.sections)==5 and bytes(before.save())==source
    fields=[]
    for entry in entries:
        if entry.block==32 and entry.message_id>2931:
            at=entry.table_offset;value=entry.block_offset+delta;assert value<8192
            struct.pack_into('<H',code.sections[0].data,at,value);fields.append((at,2))
    directory_field=DIRECTORY_OFFSET+32*4;first,size=struct.unpack_from('<HH',source,directory_field);assert size==len(oldblock)
    struct.pack_into('<HH',code.sections[0].data,directory_field,first,len(newblock));fields.append((directory_field,4))
    lines=textwrap.wrap(description['english'],width=47,break_long_words=False,break_on_hyphens=False)
    assert 1<=len(lines)<=3 and all(0<len(s)<=47 for s in lines) and ' '.join(lines)==description['english']
    compiled=b'\0'.join(s.encode('ascii') for s in lines)+b'\0\0'
    oldpayload=original_parts[3][:-48];assert len(oldpayload)==123040 and cache_plan(source)['payload_bytes']==len(oldpayload)
    active_field=binding['item116_active_pointer_field_payload_offset'];assert struct.unpack_from('<I',oldpayload,active_field)[0]==binding['item116_old_compiled_pointer']
    packed=bytearray(oldpayload);pointer=POOL+len(packed);packed.extend(compiled);struct.pack_into('<I',packed,active_field,pointer)
    packed.extend(bytes(-len(packed)%32));size=len(packed)+64;entry,copy_entry=STAGE+len(packed),STAGE+size
    packed.extend(wrapper(entry,copy_entry,size,source));assert len(packed)==size
    code.sections[3].data=packed+original_parts[3][-48:-4]+struct.pack('<I',size)
    assert struct.unpack_from('<I',source,0xE45DC)[0]==POOL+len(oldpayload)
    struct.pack_into('<I',code.sections[0].data,0x8E4,branch_link(BASE+0x8E4,entry));struct.pack_into('<I',code.sections[0].data,0xE45DC,POOL+size)
    saved=bytes(code.save());after=MainCodeFile(saved,BASE);assert len(after.sections)==5 and cache_plan(saved)['payload_bytes']==size
    allowed=[(STORAGE,len(NEW)),*fields,(0x8E4,4),(0xE45DC,4),(before.codeSettingsOffs,12)]
    restored=bytearray(after.sections[0].data)
    for at,n in allowed:restored[at:at+n]=original_parts[0][at:at+n]
    assert bytes(restored)==original_parts[0]
    for i in [1,2,4]:assert bytes(after.sections[i].data)==original_parts[i]
    for a,b in zip(before.sections,after.sections,strict=True):assert (a.ramAddress,a.bssSize)==(b.ramAddress,b.bssSize)
    prefix=bytearray(after.sections[3].data[:len(oldpayload)]);prefix[active_field:active_field+4]=oldpayload[active_field:active_field+4];assert bytes(prefix)==oldpayload
    assert bytes(after.sections[3].data[-48:-4])==original_parts[3][-48:-4]
    inverse=MainCodeFile(saved,BASE)
    for section,data in zip(inverse.sections,original_parts,strict=True):section.data=bytearray(data)
    assert bytes(inverse.save())==source
    directory=sha(saved[DIRECTORY_OFFSET:TABLE_OFFSET]);final_entries=owned_entries(newcommon,saved,directory)
    assert final_entries[2931].text==raw and len(final_entries)==len(entries)
    assert all(a.text==b.text for a,b in zip(entries,final_entries,strict=True) if a.message_id!=2931)
    assert [i for i,(a,b) in enumerate(zip(blocks,rebuilt,strict=True)) if a!=b]==[32]
    return saved,newcommon,dict(source_ARM9_sha256=sha(source),target_ARM9_sha256=sha(saved),source_COMMON_sha256=sha(common),target_COMMON_sha256=sha(newcommon),
        title_data_plan=title_plan,message_ID=2931,item_ID=116,description=description['english'],compiled_rows=lines,compiled_paragraph_hex=compiled.hex(),
        old_COMMON_block_bytes=len(oldblock),new_COMMON_block_bytes=len(newblock),COMMON_delta=delta,COMMON_owned_original_span=[selected.block_offset,selected.copy_end],old_COMMON_span_hex=oldspan.hex(),new_COMMON_span_hex=newspan.hex(),
        COMMON_metadata_fields=[list(x) for x in fields],new_directory_sha256=directory,old_compiled_pointer=binding['item116_old_compiled_pointer'],new_compiled_pointer=pointer,active_compiled_pointer_field_payload_offset=active_field,
        original_payload_bytes=len(oldpayload),new_payload_bytes=size,newly_appended_source_owned_text_span=[pointer-POOL,pointer-POOL+len(compiled)],
        original_payload_except_single_live_advice_pointer_preserved=True,old_compiled_paragraph_and_unreferenced198_table_preserved=True,
        all_other_COMMON_messages_blocks_and_all_native_code_fonts_except_declared_startup_metadata_preserved=True,
        section0_allowed_owned_fields=[list(x) for x in allowed],decoded_sections_BSS_unowned_bytes_and_exact_serialized_inverse_pass=True,
        new_cache_plan=cache_plan(saved),new_staging_span=[STAGE,STAGE+size+48],
        known_V609_growth_regression_requires_fresh_cold_boot_input_and_native_allocation_checks=True,
        research_only_not_registered_candidate_or_release_parent=True,full_goal_complete=False)
