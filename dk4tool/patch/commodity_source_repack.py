"""Repack source-owned commodity name allocations without runtime pool growth."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = 'b8a5efa36f474faccc33589f0ac001f30b539e36c5ea8e77369965ed77def8be'
TABLE, COUNT = 0x15EF18, 124


def transform(source, clean, manuscript, allocation):
    assert sha(source) == SOURCE
    target = bytearray(source)
    names = {r['index']: r for r in manuscript['records']}
    fields = {r['pointer_field'] for r in names.values()}
    assert len(names) == COUNT
    regions, records = [], []
    for group in allocation['bins']:
        lo, hi = group['start'], group['end']
        assert 0x150000 <= lo < hi <= 0x170000
        regions.append([lo, hi])
        target[lo:hi] = bytes(hi - lo)
        for item in group['names']:
            row = names[item['index']]
            field = TABLE + row['index'] * 12
            assert field == row['pointer_field']
            for arm, expected in [(source, row['current']), (clean, row['Japanese'])]:
                off = struct.unpack_from('<I', arm, field)[0] - 0x02000000
                assert arm[off:arm.index(0, off)].decode('cp932') == expected
            off = item['offset']
            value = row['English'].encode('ascii') + b'\0'
            assert item['English'] == row['English'] and lo <= off < off + len(value) <= hi
            target[off:off + len(value)] = value
            struct.pack_into('<I', target, field, 0x02000000 + off)
            records.append({'index': row['index'], 'English': row['English'], 'offset': off,
                            'field': field, 'source_Japanese': row['Japanese']})
    # The one shared source string is frozen, preserving its separate owner.
    frozen = allocation['frozen_shared_names']
    assert len(frozen) == 1 and frozen[0]['index'] == 106
    assert target[TABLE + 106 * 12:TABLE + 107 * 12] == source[TABLE + 106 * 12:TABLE + 107 * 12]
    assert target[frozen[0]['start']:frozen[0]['end']] == source[frozen[0]['start']:frozen[0]['end']]
    # Validate all aligned start/interior references to the reused regions.
    for field in range(0, len(source) - 3, 4):
        ptr = struct.unpack_from('<I', source, field)[0] - 0x02000000
        if any(lo <= ptr < hi for lo, hi in regions):
            assert field in fields, ('Additional source-string owner', hex(field), hex(ptr))
    restored = bytearray(target)
    for lo, hi in regions:
        restored[lo:hi] = source[lo:hi]
    for field in fields:
        restored[field:field + 4] = source[field:field + 4]
    assert bytes(restored) == source
    for i in range(COUNT):
        field = TABLE + i * 12
        assert target[field + 4:field + 12] == source[field + 4:field + 12]
    return bytes(target), {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(target),
                           'records': records, 'source_string_regions': regions,
                           'original_pool_heap_cache_startup_code_and_all_other_bytes_exact': True,
                           'all124_metadata_fields_preserved': True, 'shared_Whale_name_frozen': True,
                           'all49_remaining_Japanese_names_localized': True,
                           'actual_all_name_layouts_pending': True, 'full_goal_complete': False}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-commodity-source-name-repack-release-v1'
    for name, digest in config['verification_evidence_sha256'].items():
        assert sha(Path(name).read_bytes()) == digest
    manuscript = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    allocation = json.loads(Path(config['allocation']).read_text(encoding='utf-8'))
    target, plan = transform(source, clean, manuscript, allocation)
    assert sha(target) == config['target_arm9_sha256']
    plan['changed_records'] = ['DK4_COMMODITY_COMPLETE_NAME_' + str(row['index']) for row in plan['records']]
    return target, plan
