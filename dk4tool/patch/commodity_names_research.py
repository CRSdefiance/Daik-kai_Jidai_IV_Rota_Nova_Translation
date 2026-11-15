"""Source-locked full commodity names; layout remains a separate release gate."""

import struct

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

SOURCE = 'b8a5efa36f474faccc33589f0ac001f30b539e36c5ea8e77369965ed77def8be'
TABLE, COUNT, STRIDE = 0x15EF18, 124, 12


def transform(source, clean, manuscript):
    assert sha(source) == SOURCE
    rows = manuscript['records']
    assert len(rows) == COUNT and [r['index'] for r in rows] == list(range(COUNT))
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    changes, names = [], []
    for row in rows:
        field = TABLE + row['index'] * STRIDE
        assert row['pointer_field'] == field
        pointers = [struct.unpack_from('<I', arm, field)[0] for arm in (source, clean)]
        for arm, pointer, expected in zip((source, clean), pointers, (row['current'], row['Japanese'])):
            offset = pointer - BASE
            assert arm[offset:arm.index(0, offset)].decode('cp932') == expected
        assert source[field + 4:field + 12].hex() == row['metadata_hex']
        if row['change_required']:
            value = row['English'].encode('ascii') + b'\0'
            assert len(value) <= 32
            pointer = POOL + len(packed)
            packed.extend(value)
            changes.append({'offset': field, 'before': pointers[0], 'after': pointer})
            struct.pack_into('<I', code.sections[0].data, field, pointer)
        else:
            assert row['English'] == row['current']
            pointer = pointers[0]
        names.append({'index': row['index'], 'Japanese': row['Japanese'], 'English': row['English'],
                      'pointer': pointer, 'changed': row['change_required']})
    assert sum(row['changed'] for row in names) == 49
    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    assert POOL + size <= STAGE and STAGE + size + 48 <= 0x023F4000
    packed.extend(wrapper(STAGE + len(packed), STAGE + size, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    for field, value in [(0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64)), (0xE45DC, POOL + size)]:
        changes.append({'offset': field, 'before': struct.unpack_from('<I', source, field)[0], 'after': value})
        struct.pack_into('<I', code.sections[0].data, field, value)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for row in changes:
        off = row['offset']
        restored[off:off + 4] = before[0][off:off + 4]
    off = code.codeSettingsOffs
    restored[off:off + 12] = before[0][off:off + 12]
    assert bytes(restored) == before[0]
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2))
    assert bytes(parsed.sections[3].data[:preserved]) == before[3][:-48]
    return saved, {'names': names, 'changes': changes, 'inherited_payload_bytes_preserved': preserved,
                   'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved), 'cache': cache_plan(saved),
                   'all_prices_categories_production_fields_and_old_strings_preserved': True,
                   'actual_name_contexts_and_layout_not_yet_verified': True,
                   'not_a_registered_release': True, 'full_goal_complete': False}
