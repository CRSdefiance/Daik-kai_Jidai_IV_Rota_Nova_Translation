"""Source-bound removal of redundant FE text padding with complete native command inverses.

The ordinary compiler and historical rebuilders stay unchanged. Callers must
qualify the exact source/current owner and rerun stored, catalogue and loader
checks; this helper grants no display, gameplay, editorial or release approval.
"""
import struct


def remove_FE_text_parity_space(arm9,current,owner,inventory):
    assert isinstance(current,bytes)
    at=owner['command_offset'];compiled=bytes.fromhex(owner['compiled_hex'])
    old=bytes.fromhex(owner['stored_command_hex']);head=bytes.fromhex('0040ffff00')
    assert owner['source_complete_preamble_hex']=='0040ffff00fe'
    assert compiled[0]==254 and len(compiled)%2==0 and not compiled.endswith((b' ',b'\n'))
    assert b'\0' not in compiled and b'%' not in compiled
    assert old==head+compiled+b' \0\0'
    replacement=head+compiled+b'\0';assert len(old)-len(replacement)==2 and len(replacement)%2==0
    end=8+struct.unpack_from('<H',current,4)[0]
    assert current[at:at+len(old)]==old and not any(current[end:])
    before,speeches=inventory(arm9,current)
    matched=[c for c in speeches if c['offset']==at]
    assert len(matched)==1 and matched[0]['whole_command_hex']==old.hex() and matched[0]['native_extent']==len(old)
    stop=at+len(old)
    def mapped(pos):
        assert not at<pos<stop,'A reference enters the owned speech.'
        return pos-2 if pos>=stop else pos
    logical=bytearray(current[:at]+replacement+current[stop:end]);fixups=[]
    boundaries={c['offset'] for c in before}|{end}
    for c in before:
        if c['word'] not in [0x100,0x200,0x300,0x400]:continue
        site=c['offset'];span=struct.unpack_from('<H',current,site+2)[0];target=site+4+span
        assert target in boundaries
        new_site,new_target=mapped(site),mapped(target);new_span=new_target-new_site-4
        assert 0<=new_span<=65535 and new_span%2==0
        struct.pack_into('<H',logical,new_site+2,new_span)
        fixups.append(dict(word=c['word'],old_offset=site,old_span=span,old_target=target,
            new_offset=new_site,new_span=new_span,new_target=new_target))
    struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+bytes(-len(logical)%4)
    after,final_speeches=inventory(arm9,target)
    assert len(after)==len(before) and len(final_speeches)==len(speeches)
    command_map=[]
    for old_command,new in zip(before,after,strict=True):
        pos=old_command['offset'];assert new['offset']==mapped(pos) and new['word']==old_command['word']
        assert new['ancestor_0100_offsets']==[mapped(v) for v in old_command['ancestor_0100_offsets']]
        assert new['native_extent']==mapped(pos+old_command['native_extent'])-mapped(pos)
        a,b=map(bytes.fromhex,[old_command['whole_command_hex'],new['whole_command_hex']])
        if pos==at:assert b==replacement
        elif old_command['word'] in [0x100,0x200,0x300,0x400]:assert a[:2]==b[:2]
        else:assert a==b
        command_map.append(dict(word=new['word'],old_offset=pos,new_offset=new['offset'],
            old_extent=old_command['native_extent'],new_extent=new['native_extent']))
    assert after[-1]['word']==0 and after[-1]['offset']+4==len(logical)
    inverse=bytearray(target[:len(logical)])
    for f in fixups:struct.pack_into('<H',inverse,f['new_offset']+2,f['old_span'])
    inverse[at:at+len(replacement)]=old;inverse[:8]=current[:8]
    assert bytes(inverse)+current[end:]==current
    return target,dict(owner=owner,old_command_hex=old.hex(),new_command_hex=replacement.hex(),
        command_map=command_map,relative_fixups=fixups,all_target_commands=after,
        old_logical_end=end,new_logical_end=len(logical),one_text_space_andone_NUL_alignment_byte_removed=True,
        source_controls_native_command_count_scopes_andall_nontext_bytes_preserved=True,
        full_block_inverse_exact=True,new_editorial_credit=0)
