"""Preserve credited relocated context and prove the actual clean/current/target inverses."""
from copy import deepcopy
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block, verify_compound


def rebuild_credited_context(arm, clean, current, records, compiled, inventory, group, credited,
                             *, expected_context_objects, expected_context_speeches):
    assert records and not any(r.get('native_object_kind') for r in records)
    assert {r['block'] for r in records} == {group['block']}
    assert {r['file_path'] for r in records} == {group['file_path']}
    assert bytes.fromhex(group['clean_block_hex']) == clean
    full = group['complete_clean_context_records']
    context = [r for r in full if r['covered']]
    owned = [r for r in full if not r['covered']]
    assert len(context) == expected_context_objects
    assert len([r for r in context if r['kind']=='ordinary-speech']) == expected_context_speeches
    assert [r['id'] for r in owned] == [r['id'] for r in records]
    assert all(r['kind']=='ordinary-speech' and not r['exact_credited_source_bindings'] for r in owned)
    for row in context:
        assert len(row['exact_credited_source_bindings']) == 1
        binding = row['exact_credited_source_bindings'][0]
        assert (row['file_path'],binding['id']) in credited
        assert binding['block']==row['block'] and binding['offset']==row['source_reference']['offset']
        assert binding['source_hex']==row['source_hex']
        at = row['source_reference']['offset']
        raw = bytes.fromhex(row['source_hex'])
        assert clean[at:at+len(raw)+1] == raw+b'\0'
    source_commands, source_speeches = inventory(arm,clean)
    current_commands, current_speeches = inventory(arm,current)
    assert source_commands == group['all_source_commands']
    assert len(source_commands)==len(current_commands)
    assert len(source_speeches)==len(current_speeches)==len(records)+expected_context_speeches
    mapped = {a['offset']:b for a,b in zip(source_commands,current_commands,strict=True)}
    assert all(a['word']==b['word'] for a,b in zip(source_commands,current_commands,strict=True))
    aligned = bytearray(current)
    shadow_rows = []
    coordinates = []
    for row, source in zip(records,owned,strict=True):
        assert all(row[k]==source[k] for k in ['id','source_hex','source_reference','source_Japanese'])
        assert (row['file_path'],row['id']) not in credited
        at, original_at = row['current_reference']['offset'], row['source_reference']['offset']
        a,b = bytes.fromhex(row['source_hex']),bytes.fromhex(row['current_hex'])
        assert len(a)==len(b) and clean[original_at:original_at+len(a)+1]==a+b'\0'
        assert current[at:at+len(b)+1]==b+b'\0'
        assert mapped[original_at-5]['offset']==at-5
        assert clean[original_at-5:original_at+1]==current[at-5:at+1]==bytes.fromhex(row['source_complete_preamble_hex'])
        aligned[at:at+len(a)] = a
        shadow = deepcopy(row)
        shadow['source_reference'] = dict(row['source_reference'],offset=at,command_offset=at-5)
        shadow_rows.append(shadow)
        coordinates.append(dict(id=row['id'],clean_reference=row['source_reference'],current_reference=row['current_reference'],source_hex=a.hex()))
    preserved = []
    all_compiled = deepcopy(compiled)
    for row in context:
        source_at = row['source_reference']['command_offset']
        command = mapped[source_at]
        if row['kind']=='physical-style-alternative':
            assert command['word']==0x4100
            source_command = next(c for c in source_commands if c['offset']==source_at)
            verify_compound(0x4100,bytes.fromhex(source_command['whole_command_hex']),
                bytes.fromhex(command['whole_command_hex']),bytes.fromhex(command['whole_command_hex']))
            continue
        assert row['kind']=='ordinary-speech' and command['word']==0x4000
        at = command['offset']+5
        raw = current[at:current.index(0,at+1)]
        assert clean[row['source_reference']['offset']]==raw[0]
        shadow_rows.append(dict(id=row['id'],source_hex=raw.hex(),current_hex=raw.hex(),
            source_reference=dict(offset=at),current_reference=dict(offset=at),
            source_selector=raw[0],source_complete_preamble_hex=current[at-5:at+1].hex(),
            current_record_index=current[:at].count(b'\0')))
        all_compiled[row['id']] = dict(encoded_hex=raw.hex())
        preserved.append(dict(id=row['id'],actual_clean_reference=row['source_reference'],actual_clean_hex=row['source_hex'],
            current_reference=dict(offset=at),current_hex=raw.hex(),not_a_new_editorial_review=True))
    aligned = bytes(aligned)
    for row in shadow_rows:
        at = row['source_reference']['offset']
        row['source_record_index'] = aligned[:at].count(b'\0')
    shadow_rows.sort(key=lambda r:r['current_reference']['offset'])
    # The original complete allocator/inverses still run. The aligned source is
    # only a coordinate projection; its identity is never called the clean ROM.
    target, proof = rebuild_block(arm,aligned,current,shadow_rows,all_compiled,inventory)
    selected = {r['id'] for r in records}
    assert len(proof['text_records'])==len(records)+expected_context_speeches
    for text in proof['text_records']:
        if text['id'] not in selected:
            assert text['stored_hex']==text['compiled_hex']==text['current_hex'] and not text['parity_space_added']
            next(p for p in preserved if p['id']==text['id']).update(target_offset=text['new_offset'],target_hex=text['stored_hex'])
    proof['text_records'] = [r for r in proof['text_records'] if r['id'] in selected]
    after = proof['all_target_commands']
    assert len(after)==len(source_commands)
    # Exclusive command slices partition the byte stream. 0100 native extents
    # include child commands, so using their whole extents here would overlap.
    assert clean[:4]+clean[6:8]==current[:4]+current[6:8]==target[:4]+target[6:8]
    inverse = bytearray(target[:8])
    clean_end,current_end,target_end = [8+struct.unpack_from('<H',b,4)[0] for b in [clean,current,target]]
    for i,(a,b,c) in enumerate(zip(source_commands,current_commands,after,strict=True)):
        assert a['word']==b['word']==c['word']
        ends = [commands[i+1]['offset'] if i+1<len(commands) else end
                for commands,end in [(source_commands,clean_end),(current_commands,current_end),(after,target_end)]]
        source_bytes,previous,value = [raw[command['offset']:end] for raw,command,end in zip([clean,current,target],[a,b,c],ends,strict=True)]
        word = a['word']
        if word in (0x4000,0x4100):
            assert source_bytes[:6 if word==0x4000 else 2]==previous[:6 if word==0x4000 else 2]==value[:6 if word==0x4000 else 2]
            if word==0x4100:
                assert previous==value
                verify_compound(word,source_bytes,previous,value)
            inverse.extend(source_bytes)
        elif word in (0x100,0x200,0x300,0x400):
            assert len(source_bytes)==len(previous)==len(value)==4 and source_bytes[:2]==previous[:2]==value[:2]
            inverse.extend(value[:2]+source_bytes[2:])
        else:
            assert source_bytes==previous==value
            inverse.extend(value)
    struct.pack_into('<H',inverse,4,len(inverse)-8)
    inverse.extend(bytes(-len(inverse)%4))
    assert bytes(inverse)==clean
    proof.update(actual_clean_block_inverse_exact=True,actual_clean_block_sha256=sha(clean),
        current_parent_inverse_executed_by_original_complete_allocator=True,
        aligned_source_projection_sha256=sha(aligned),aligned_projection_is_not_canonical_Japanese_source=True,
        actual_source_to_current_selected_coordinates=coordinates,preserved_credited_context_speeches=preserved,
        preserved_credited_context_objects=context,credited_context_objects_not_new_reviews=len(context),
        full_canonical_clean_inverse_uses_exact_source_text_spans_andrelative_fields=True)
    return target,proof
