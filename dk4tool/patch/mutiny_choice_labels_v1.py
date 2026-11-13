"""Localize the three original mutiny response labels in the owned literal section."""

import struct

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha


BASE = 0x02000000
SOURCE = '8b4cfc476a79e43ff46f4683f87769cdcbc02ff01f1996c10c6f25f436eed924'
TABLE = 0x1150B8


def transform(source, labels):
    if sha(source) != SOURCE:
        raise ValueError('Exact registered sailing-alert ARM9 required')
    assert len(labels) == 3
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 6
    tail = code.sections[-1]
    assert not tail.bssSize
    preserved = len(tail.data)
    payload, changes = bytearray(), []
    for index, row in enumerate(labels):
        field = TABLE + index * 4
        before = struct.unpack_from('<I', source, field)[0]
        original = bytes.fromhex(row['source_hex'])
        start = before - BASE
        assert row['choice_index'] == index and row['source_reference']['pointer_field'] == BASE + field
        assert row['source_reference']['literal_offset'] == start
        assert source[start:start + len(original)] == original and original.endswith(b'\0')
        assert original == bytes.fromhex(row['current_hex'])
        raw_pointer = struct.pack('<I', before)
        assert [i for i in range(0, len(source) - 3, 4) if source[i:i + 4] == raw_pointer] == [field]
        text = row['english'].encode('ascii') + b'\0'
        assert b'\0' not in text[:-1] and 1 < len(text) < 37
        target = tail.ramAddress + preserved + len(payload)
        assert target % 4 == 0
        payload.extend(text)
        payload.extend(bytes(-len(payload) % 4))
        struct.pack_into('<I', code.sections[0].data, field, target)
        changes.append(dict(id=row['id'], index=index, field=field, original_pointer=before,
            target_pointer=target, source_terminated_hex=original.hex(), target_terminated_hex=text.hex()))
    start, stop = tail.ramAddress + preserved, tail.ramAddress + preserved + len(payload)
    assert stop <= BASE and all(section.ramAddress + len(section.data) + section.bssSize <= start
                               or stop <= section.ramAddress for section in code.sections)
    tail.data.extend(payload)
    target = bytes(code.save())

    inverse = MainCodeFile(target, BASE)
    assert bytes(inverse.sections[-1].data[preserved:]) == payload
    del inverse.sections[-1].data[preserved:]
    for row in changes:
        struct.pack_into('<I', inverse.sections[0].data, row['field'], row['original_pointer'])
    assert bytes(inverse.save()) == source
    return target, dict(source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        changes=changes, initialized_literal_start=start, initialized_literal_end=stop,
        complete_serialized_ARM9_parent_inverse=True)
