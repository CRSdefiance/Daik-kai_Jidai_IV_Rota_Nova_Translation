"""Rebuild a fully inventoried native scene without changing nontext commands.

This byte planner does not grant editorial, gameplay or release approval. Callers
must bind the source/current inventories and supply reviewed compiled records.
"""
import struct


def rebuild_block(arm9, clean, current, records, compiled, inventory):
    old_end = 8 + struct.unpack_from('<H', current, 4)[0]
    clean_end = 8 + struct.unpack_from('<H', clean, 4)[0]
    assert old_end == clean_end and current[:8] == clean[:8]
    assert len(current) == len(clean) and current[old_end:] == clean[clean_end:]
    assert not any(current[old_end:])
    before, speeches = inventory(arm9, current)
    source_commands, source_speeches = inventory(arm9, clean)
    assert len(before) == len(source_commands) and len(speeches) == len(source_speeches) == len(records)
    patches = []
    for row in records:
        at, source_at = row['current_reference']['offset'], row['source_reference']['offset']
        previous, original = bytes.fromhex(row['current_hex']), bytes.fromhex(row['source_hex'])
        value = bytes.fromhex(compiled[row['id']]['encoded_hex'])
        assert at == source_at and len(previous) == len(original)
        assert current[at:at + len(previous) + 1] == previous + b'\0'
        assert clean[at:at + len(original) + 1] == original + b'\0'
        assert current[at - 5:at + 1].hex() == clean[at - 5:at + 1].hex() == row['source_complete_preamble_hex']
        assert value[0] == previous[0] == original[0] == row['source_selector']
        assert value[1:] and b'\0' not in value[1:] and b'%' not in value[1:]
        assert all(original[1:].count(m) == value[1:].count(m) for m in (b'FI', b'FA', b'FO'))
        assert current[:at].count(b'\0') == row['current_record_index']
        assert clean[:source_at].count(b'\0') == row['source_record_index']
        parity_space = len(value) % 2 != len(previous) % 2
        stored = value + (b' ' if parity_space else b'')
        patches.append(dict(id=row['id'], start=at, end=at + len(previous),
                            old=previous, original=original, value=stored,
                            compiled=value, parity_space=parity_space,
                            preamble=row['source_complete_preamble_hex']))
    patches.sort(key=lambda p: p['start'])
    assert all(a['end'] <= b['start'] for a, b in zip(patches, patches[1:]))
    assert {p['start'] - 5 for p in patches} == {c['offset'] for c in speeches}

    def mapped(at):
        delta = 0
        for patch in patches:
            if at < patch['start']:
                break
            assert not patch['start'] < at < patch['end'], 'Reference enters replaced speech.'
            if at == patch['start']:
                return at + delta
            delta += len(patch['value']) - len(patch['old'])
        return at + delta

    chunks, last = [], 0
    for patch in patches:
        chunks.extend((current[last:patch['start']], patch['value']))
        last = patch['end']
    chunks.append(current[last:old_end])
    logical = bytearray(b''.join(chunks))
    assert len(logical) == mapped(old_end) < 0x2400
    boundaries = {c['offset'] for c in before} | {old_end}
    fixups = []
    for command, original in zip(before, source_commands, strict=True):
        assert command['offset'] == original['offset'] and command['word'] == original['word']
        if command['word'] not in (0x100, 0x200, 0x300, 0x400):
            continue
        at = command['offset']
        span = struct.unpack_from('<H', current, at + 2)[0]
        end = at + 4 + span
        assert end in boundaries and current[at:at + 4] == clean[at:at + 4]
        new_at, new_end = mapped(at), mapped(end)
        new_span = new_end - new_at - 4
        assert 0 <= new_span <= 0xFFFF and new_span % 2 == 0
        struct.pack_into('<H', logical, new_at + 2, new_span)
        fixups.append(dict(word=command['word'], old_offset=at, old_span=span,
                           old_target=end, new_offset=new_at, new_span=new_span, new_target=new_end))
    struct.pack_into('<H', logical, 4, len(logical) - 8)
    target = bytes(logical) + bytes(-len(logical) % 4)
    after, final_speeches = inventory(arm9, target)
    assert len(after) == len(before) and len(final_speeches) == len(speeches)
    command_map = []
    for old, new, source_command in zip(before, after, source_commands, strict=True):
        at, new_at, word = old['offset'], new['offset'], old['word']
        assert new_at == mapped(at) and new['word'] == word
        assert new['native_extent'] == mapped(at + old['native_extent']) - new_at
        assert new['ancestor_0100_offsets'] == [mapped(a) for a in old['ancestor_0100_offsets']]
        a, b, c = [bytes.fromhex(q['whole_command_hex']) for q in (old, new, source_command)]
        if word == 0x4000:
            assert a[:6] == b[:6] == c[:6]
        elif word in (0x100, 0x200, 0x300, 0x400):
            assert a[:2] == b[:2] == c[:2]
        else:
            assert a == b == c
        command_map.append(dict(word=word, old_offset=at, new_offset=new_at,
                                old_extent=old['native_extent'], new_extent=new['native_extent']))
    assert after[-1]['word'] == 0 and after[-1]['native_extent'] == 4
    assert after[-1]['offset'] + 4 == len(logical)
    texts = []
    for patch in patches:
        at = mapped(patch['start'])
        assert target[at:at + len(patch['value']) + 1] == patch['value'] + b'\0'
        assert target[at - 5:at + 1].hex() == patch['preamble']
        texts.append(dict(id=patch['id'], old_offset=patch['start'], new_offset=at,
                          current_hex=patch['old'].hex(), source_hex=patch['original'].hex(),
                          compiled_hex=patch['compiled'].hex(), stored_hex=patch['value'].hex(),
                          parity_space_added=patch['parity_space'],
                          new_record_index=target[:at].count(b'\0')))
    for source_version, original in ((False, current), (True, clean)):
        inverse = bytearray(target[:len(logical)])
        inverse[:8] = original[:8]
        for fix in fixups:
            struct.pack_into('<H', inverse, fix['new_offset'] + 2, fix['old_span'])
        for patch in reversed(patches):
            at = mapped(patch['start'])
            inverse[at:at + len(patch['value'])] = patch['original'] if source_version else patch['old']
        assert bytes(inverse) + original[old_end:] == original
    return target, dict(text_records=texts, relative_fixups=fixups, command_map=command_map,
                        all_current_commands=before, all_target_commands=after,
                        source_current_andclean_block_inverse_exact=True,
                        old_logical_end=old_end, new_logical_end=len(logical),
                        old_tail_hex=current[old_end:].hex(), new_tail_hex=target[len(logical):].hex())
