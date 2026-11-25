"""Qualified odd-length FE padding replacement; preserve the complete native command extent."""
import struct


def replace_FE_text_parity_space_with_NUL(arm9,current,owner,inventory):
    assert isinstance(current,bytes)
    at=owner['command_offset'];compiled=bytes.fromhex(owner['compiled_hex'])
    old=bytes.fromhex(owner['stored_command_hex']);head=bytes.fromhex('0040ffff00')
    assert owner['source_complete_preamble_hex']=='0040ffff00fe'
    assert compiled[0]==254 and len(compiled)%2==1 and not compiled.endswith((b' ',b'\n'))
    assert b'\0' not in compiled and b'%' not in compiled
    assert old==head+compiled+b' \0' and len(old)%2==0
    replacement=head+compiled+b'\0\0';assert len(replacement)==len(old)
    assert current[at:at+len(old)]==old
    before,speeches=inventory(arm9,current)
    found=[c for c in speeches if c['offset']==at]
    assert len(found)==1 and found[0]['whole_command_hex']==old.hex() and found[0]['native_extent']==len(old)
    value=bytearray(current);index=at+len(head)+len(compiled)
    assert value[index:index+2]==b' \0';value[index]=0;target=bytes(value)
    after,final_speeches=inventory(arm9,target)
    assert len(after)==len(before) and len(final_speeches)==len(speeches)
    command_map=[];fixups=[]
    for previous,new in zip(before,after,strict=True):
        assert all(previous[k]==new[k] for k in ['offset','word','native_extent','ancestor_0100_offsets','native_result_hex'])
        if previous['offset']==at:assert new['whole_command_hex']==replacement.hex()
        else:assert previous['whole_command_hex']==new['whole_command_hex']
        command_map.append(dict(word=new['word'],old_offset=new['offset'],new_offset=new['offset'],
            old_extent=new['native_extent'],new_extent=new['native_extent']))
        if new['word'] in [0x100,0x200,0x300,0x400]:
            site=new['offset'];span=struct.unpack_from('<H',target,site+2)[0]
            fixups.append(dict(word=new['word'],old_offset=site,new_offset=site,old_span=span,new_span=span,
                old_target=site+4+span,new_target=site+4+span))
    end=8+struct.unpack_from('<H',current,4)[0]
    assert after[-1]['word']==0 and after[-1]['offset']+4==end
    inverse=bytearray(target);inverse[index]=32;assert bytes(inverse)==current
    assert [i for i,(a,b) in enumerate(zip(current,target,strict=True)) if a!=b]==[index]
    return target,dict(owner=owner,old_command_hex=old.hex(),new_command_hex=replacement.hex(),
        command_map=command_map,relative_fixups=fixups,all_target_commands=after,old_logical_end=end,new_logical_end=end,
        one_text_alignment_space_replaced_with_NUL=True,exact_changed_byte=index,
        source_controls_native_command_count_scopes_extents_andall_other_bytes_preserved=True,
        full_block_inverse_exact=True,new_editorial_credit=0)
