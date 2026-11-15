"""Preserve an inventoried scene while replacing explicitly reviewed speech only."""
from dk4tool.script.reviewed_scene_rebuild import rebuild_block


def rebuild_sparse_block(arm, clean, current, file_path, block, changes, inventory):
    commands, speeches = inventory(arm, current)
    source_commands, source_speeches = inventory(arm, clean)
    assert len(commands) == len(source_commands) and len(speeches) == len(source_speeches)
    records, compiled, selected = [], {}, set()
    for command, original in zip(speeches, source_speeches, strict=True):
        at, source_at = command['offset'] + 5, original['offset'] + 5
        assert at == source_at
        raw = current[at:current.index(0, at + 1)]
        source = clean[source_at:clean.index(0, source_at + 1)]
        index = clean[:source_at].count(b'\0')
        ident = f'DK4_MES_B{block:02d}_R{index:04d}'
        row = dict(id=ident, source_hex=source.hex(), current_hex=raw.hex(),
                   source_selector=source[0], source_complete_preamble_hex=clean[source_at - 5:source_at + 1].hex(),
                   source_reference=dict(offset=source_at), current_reference=dict(offset=at),
                   source_record_index=index, current_record_index=current[:at].count(b'\0'))
        if ident in changes:
            change = changes[ident]
            assert bytes.fromhex(change['source_hex']) == source and bytes.fromhex(change['current_hex']) == raw
            assert change['file_path'] == file_path and change['block'] == block
            value = change['compiled_hex']
            selected.add(ident)
        else:
            value = raw.hex()
        records.append(row)
        compiled[ident] = dict(encoded_hex=value)
    assert selected == set(changes) and selected
    target, proof = rebuild_block(arm, clean, current, records, compiled, inventory)
    for row in proof['text_records']:
        if row['id'] not in selected:
            assert row['stored_hex'] == row['compiled_hex'] == row['current_hex']
            assert not row['parity_space_added']
    proof.update(reviewed_changed_IDs=sorted(selected),
                 other_speech_bytes_preserved_not_editorial_retention_credit=True)
    return target, proof
