"""Complete city-status names in existing source-owned string allocations."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

BASE = 0x02000000
NAMES = ['War', 'Plague', 'Famine', 'Boom', 'Slump', 'Seasoning Shortage',
         'Spice Shortage', 'Luxury Shortage', 'Alcohol Shortage',
         'Fiber Shortage', 'Dye Shortage', 'Ore Shortage', 'Normal']
SPANS = [(0x15633C, 132), (0x1565D0, 16)]
TABLE = 0x156430
GENERIC_FIELDS = [0x8D848, 0xB6420, 0xB171C]


def transform(source):
    target = bytearray(source)
    original_table = list(struct.unpack_from('<13I', source, TABLE))
    owners = []
    for lo, size in SPANS:
        refs = [field for field in range(0, len(source) - 3, 4)
                if BASE + lo <= struct.unpack_from('<I', source, field)[0] < BASE + lo + size]
        expected = list(range(TABLE, TABLE + 52, 4)) if lo == SPANS[0][0] else [0xB171C, 0xB2D90]
        if refs != sorted(expected):
            raise ValueError('Status storage pointer ownership differs')
        owners.append({'offset': lo, 'bytes': size, 'pointer_owners': refs,
                       'before_hex': source[lo:lo + size].hex()})
        target[lo:lo + size] = bytes(size)
    pointers, cursor = {}, SPANS[0][0]
    for index, text in enumerate(NAMES):
        if index == 11:
            continue
        encoded = text.encode('ascii') + b'\0'
        if cursor + len(encoded) > SPANS[0][0] + SPANS[0][1]:
            raise ValueError('Complete names exceed primary allocation')
        target[cursor:cursor + len(encoded)] = encoded
        pointers[index] = BASE + cursor
        cursor += len(encoded)
    # One complete13-byte name occupies the old generic/fallback16-byte block.
    ore = NAMES[11].encode('ascii') + b'\0'
    target[SPANS[1][0]:SPANS[1][0] + len(ore)] = ore
    pointers[11] = BASE + SPANS[1][0]
    generic = pointers[6] + len('Spice ')
    assert target[generic - BASE:generic - BASE + 9] == b'Shortage\0'
    changes = []
    for index in range(13):
        field = TABLE + index * 4
        changes.append({'field': field, 'before': original_table[index], 'after': pointers[index]})
    for field in GENERIC_FIELDS:
        before = struct.unpack_from('<I', source, field)[0]
        old_text = source[before - BASE:].split(b'\0')[0].decode('cp932')
        if old_text != '品不足':
            raise ValueError('Original compact shortage label differs')
        changes.append({'field': field, 'before': before, 'after': generic})
    changes.append({'field': 0xB2D90, 'before': struct.unpack_from('<I', source, 0xB2D90)[0],
                    'after': pointers[12]})
    # The length-output helper must return the actual ASCII label length.
    if struct.unpack_from('<I', source, 0xB1708)[0] != 0xA3A00006:
        raise ValueError('Original compact length instruction differs')
    changes.append({'field': 0xB1708, 'before': 0xA3A00006, 'after': 0xA3A00008})
    for row in changes:
        struct.pack_into('<I', target, row['field'], row['after'])
    restored = bytearray(target)
    for lo, size in SPANS:
        restored[lo:lo + size] = source[lo:lo + size]
    for row in changes:
        struct.pack_into('<I', restored, row['field'], row['before'])
    if restored != source:
        raise ValueError('Unowned ARM9 bytes change')
    saved = bytes(target)
    before_code, after_code = MainCodeFile(source, BASE), MainCodeFile(saved, BASE)
    if len(saved) != len(source) or [(s.ramAddress, len(s.data)) for s in before_code.sections] != [(s.ramAddress, len(s.data)) for s in after_code.sections]:
        raise ValueError('Memory section extents change')
    assert all(bytes(a.data) == bytes(b.data) for a, b in zip(before_code.sections[1:], after_code.sections[1:]))
    return saved, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(saved),
                    'source_owned_spans': owners, 'changes': changes,
                    'status_names': [{'index': i, 'text': text, 'pointer': pointers[i]} for i, text in enumerate(NAMES)],
                    'compact_Shortage_pointer': generic, 'no_file_section_pool_or_arena_growth': True,
                    'changed_records': [f'CITY_STATUS_{i}' for i in range(13)] + ['CITY_COMPACT_SHORTAGE_LABEL_LENGTH']}


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-city-status-labels-v1' or sha(source) != config['source_arm9_sha256']:
        raise ValueError('City-status source/config differs')
    target, report = transform(source)
    if sha(target) != config['target_arm9_sha256']:
        raise ValueError('Reviewed city-status target differs')
    return target, report
