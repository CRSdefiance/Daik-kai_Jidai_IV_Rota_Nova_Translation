"""Reuse the existing complete English item-role table for the shared selector."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, cache_plan

SOURCE = '257ffcea00bcec06186394eff58d77f3929a1eb2f43ffba4ba71f4ce64f5f69e'
FIELD, ORIGINAL, ENGLISH = 0x86334, 0x021197A0, 0x023889C8
JAPANESE = ('艦長', '副官', '参謀', '主計長', '測量士', '操帆手', '操舵手', '見張り',
            '斬込隊長', '砲撃手', '宣教師', '船医', '料理長', '船大工', '飼育員', '甲板要員')
LABELS = ('Captain', 'First Mate', 'Strategist', 'Purser', 'Surveyor', 'Sail Handler',
          'Helmsman', 'Lookout', 'Boarding Leader', 'Gunner', 'Missionary', 'Surgeon',
          'Chief Cook', 'Shipwright', 'Animal Keeper', 'Deckhand')


def transform(source, clean, canonical):
    if sha(source) != SOURCE:
        raise ValueError('Exact complete V324 ARM9 required')
    cache = cache_plan(source)
    payload = bytes(MainCodeFile(source, BASE).sections[3].data[:-48])
    pointers = struct.unpack_from('<16I', payload, ENGLISH - POOL)
    records = []
    for index, (japanese, english, target) in enumerate(zip(JAPANESE, LABELS, pointers)):
        table_field = ORIGINAL - BASE + index * 4
        original = struct.unpack_from('<I', source, table_field)[0]
        raw = japanese.encode('cp932') + b'\0'
        for arm in (source, clean, canonical):
            if struct.unpack_from('<I', arm, table_field)[0] != original or arm[original - BASE:original - BASE + len(raw)] != raw:
                raise ValueError('Original role table or Japanese source differs')
        expected = (english + (' ' if len(english) % 2 else '')).encode('ascii') + b'\0'
        if payload[target - POOL:target - POOL + len(expected)] != expected:
            raise ValueError('Existing complete English role label differs')
        records.append({'index': index, 'Japanese': japanese, 'English': english,
                        'stored': expected[:-1].decode('ascii'), 'original_pointer': original,
                        'existing_English_pointer': target})
    for arm in (source, clean, canonical):
        if struct.unpack_from('<I', arm, FIELD)[0] != ORIGINAL:
            raise ValueError('Shared role-selector table literal differs')
    target = bytearray(source)
    struct.pack_into('<I', target, FIELD, ENGLISH)
    saved = bytes(target)
    assert saved[:FIELD] == source[:FIELD] and saved[FIELD + 4:] == source[FIELD + 4:]
    assert cache_plan(saved) == cache
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'shared_selector': BASE + 0x86314, 'table_literal_field': FIELD,
                   'old_table': ORIGINAL, 'existing_English_table': ENGLISH, 'roles': records,
                   'one_table_literal_only_no_new_text_allocation_or_code_change': True,
                   'all_existing_tables_strings_pool_boot_cache_helpers_and_other_bytes_exact': True,
                   'changed_records': ['DK4_SHARED_CREW_ROLE_LABELS']}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-crew-role-labels-release-v1':
        raise ValueError('Unknown crew role label release')
    for filename, digest in config['verification_evidence_sha256'].items():
        if sha(Path(filename).read_bytes()) != digest:
            raise ValueError('Crew role native evidence differs')
    target, proof = transform(source, clean, canonical)
    if sha(target) != config['target_arm9_sha256']:
        raise ValueError('Crew role target differs')
    return target, proof
