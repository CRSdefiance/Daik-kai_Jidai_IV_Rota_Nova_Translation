"""Add source-owned FE continuation commands while preserving every other command and scope.

This is a byte planner. Native page rendering,stored dispatch,actual transitions and
registered release approval are separate gates. A continuation repeats the exact
source six-byte FE control;it cannot introduce another actor orchange game code.
"""
import struct


def insert_FE_continuations(arm9,current,owners,inventory):
    assert isinstance(current,bytes) and owners and len({o['source_ID'] for o in owners})==len(owners)
    end=8+struct.unpack_from('<H',current,4)[0]
    assert end<=len(current) and not any(current[end:])
    before,speeches=inventory(arm9,current)
    inserts=[]
    for owner in owners:
        at=owner['first_command_offset'];head=bytes.fromhex(owner['complete_source_preamble_hex'])
        assert head==bytes.fromhex('0040ffff00fe')
        matches=[c for c in speeches if c['offset']==at]
        assert len(matches)==1
        first=matches[0];raw=bytes.fromhex(first['whole_command_hex'])
        assert raw[:6]==head and raw[5:]==bytes.fromhex(owner['first_stored_hex'])+b'\0'
        child=bytes.fromhex(owner['continuation_encoded_hex'])
        assert child[0]==254 and child[1:] and b'\0' not in child[1:] and b'%' not in child[1:]
        # Every inserted command is even-sized. Its sole extra space,if needed,
        # is owned trailing alignment andmust receive fresh stored-native checks.
        stored=child+(b' ' if len(child)%2 else b'')
        value=head[:5]+stored+b'\0';assert len(value)%2==0
        point=at+first['native_extent'];assert point<=end
        assert [r['native_child_page'] for r in owner['pages']]==[1,2]
        assert ' '.join(r['logical_English'] for r in owner['pages'])==owner['unchanged_logical_English']
        assert owner['pages'][1]['encoded_hex']==child.hex()
        first_encoded=bytes.fromhex(owner['pages'][0]['encoded_hex'])
        assert first_encoded[0]==254 and owner['first_stored_hex'] in [first_encoded.hex(),(first_encoded+b' ').hex()]
        for page in owner['pages']:
            encoded=bytes.fromhex(page['encoded_hex'])
            assert encoded[0]==254 and b' '.join(encoded[1:].split()).decode('ascii')==page['logical_English']
        inserts.append(dict(point=point,value=value,owner=owner,first=first,stored=stored))
    inserts.sort(key=lambda r:r['point'])
    assert len({r['point'] for r in inserts})==len(inserts)
    def mapped(at):return at+sum(len(i['value']) for i in inserts if i['point']<=at)
    chunks=[];last=0
    for item in inserts:
        chunks.extend([current[last:item['point']],item['value']]);last=item['point']
    chunks.append(current[last:end]);logical=bytearray(b''.join(chunks))
    assert len(logical)==mapped(end)<0x2400
    boundaries={c['offset'] for c in before}|{end};fixups=[]
    for c in before:
        if c['word'] not in [0x100,0x200,0x300,0x400]:continue
        at=c['offset'];span=struct.unpack_from('<H',current,at+2)[0];target=at+4+span
        assert target in boundaries
        newat,newtarget=mapped(at),mapped(target);newspan=newtarget-newat-4
        assert 0<=newspan<=0xFFFF and newspan%2==0
        struct.pack_into('<H',logical,newat+2,newspan)
        fixups.append(dict(word=c['word'],old_offset=at,old_span=span,old_target=target,
            new_offset=newat,new_span=newspan,new_target=newtarget))
    struct.pack_into('<H',logical,4,len(logical)-8)
    result=bytes(logical)+bytes(-len(logical)%4)
    after,finalspeeches=inventory(arm9,result)
    assert len(after)==len(before)+len(inserts) and len(finalspeeches)==len(speeches)+len(inserts)
    byat={c['offset']:c for c in after};mapping=[]
    for c in before:
        newat=mapped(c['offset']);new=byat[newat]
        assert c['word']==new['word'] and new['ancestor_0100_offsets']==[mapped(v) for v in c['ancestor_0100_offsets']]
        if c['word'] in [0x100,0x200,0x300,0x400]:assert new['native_extent']==mapped(c['offset']+c['native_extent'])-newat
        else:assert new['native_extent']==c['native_extent']
        a,b=map(bytes.fromhex,[c['whole_command_hex'],new['whole_command_hex']])
        if c['word'] in [0x100,0x200,0x300,0x400]:assert a[:2]==b[:2]
        else:assert a==b
        mapping.append(dict(word=c['word'],old_offset=c['offset'],new_offset=newat,
            old_extent=c['native_extent'],new_extent=new['native_extent']))
    children=[]
    for item in inserts:
        at=mapped(item['point'])-len(item['value']);new=byat[at]
        assert new['word']==0x4000 and new['whole_command_hex']==item['value'].hex() and new['native_extent']==len(item['value'])
        assert new['ancestor_0100_offsets']==[mapped(v) for v in item['first']['ancestor_0100_offsets']]
        children.append(dict(source_ID=item['owner']['source_ID'],native_child_page=2,new_command_offset=at,
            first_command_offset=mapped(item['first']['offset']),complete_source_preamble_hex=item['owner']['complete_source_preamble_hex'],
            encoded_hex=item['owner']['continuation_encoded_hex'],stored_hex=item['stored'].hex(),
            command_hex=item['value'].hex(),command_bytes=len(item['value']),
            exact_same_original_conditional_ancestors=True,native_new_wait_requires_actual_transition_test=True))
    assert after[-1]['word']==0 and after[-1]['offset']+4==len(logical)
    inverse=bytearray(result[:len(logical)])
    for f in fixups:struct.pack_into('<H',inverse,f['new_offset']+2,f['old_span'])
    for child in reversed(children):del inverse[child['new_command_offset']:child['new_command_offset']+child['command_bytes']]
    inverse[:8]=current[:8]
    assert bytes(inverse)+current[end:]==current
    return result,dict(original_command_map=mapping,relative_fixups=fixups,continuations=children,
        all_original_nontext_bytes_andcomplete_speech_commands_preserved=True,
        every_child_repeats_exact_FE_control_andoriginal_conditional_scope=True,
        exact_complete_intermediate_block_inverse=True,old_logical_end=end,new_logical_end=len(logical),
        all_target_commands=after,new_native_command_count=len(inserts),new_source_editorial_credit=0)
