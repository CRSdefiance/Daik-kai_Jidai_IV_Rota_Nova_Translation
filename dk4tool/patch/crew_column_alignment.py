"""Align the existing shared sailor headings with their numeric columns."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

BASE = 0x02000000
POINT = 0x114E90
DRAW = 0x1E510
DRAW_HEX = '0600a0e1004090e510119fe510319fe5044094e50020a0e3011087e034ff2fe1'


def transform(source):
    if source[POINT:POINT + 16] != bytes.fromhex('7400000000000000820000006d000000'):
        raise ValueError('Original shared header point or adjacent geometry differs')
    if source[DRAW:DRAW + 32] != bytes.fromhex(DRAW_HEX):
        raise ValueError('Original crew header draw call differs')
    if source[0x133FBC:0x133FBC + 17] != b'Need   Now   Max\0':
        raise ValueError('Inherited complete crew headings differ')
    refs = [p for p in range(0, len(source) - 3, 4)
            if struct.unpack_from('<I', source, p)[0] == BASE + POINT]
    if refs != [0x1E634]:
        raise ValueError('Header point has another native owner')
    target = bytearray(source)
    struct.pack_into('<I', target, POINT, 136)
    restored = bytearray(target)
    struct.pack_into('<I', restored, POINT, 116)
    assert restored == source and len(target) == len(source)
    before = MainCodeFile(source, BASE)
    after = MainCodeFile(bytes(target), BASE)
    assert [(s.ramAddress, len(s.data)) for s in before.sections] == [(s.ramAddress, len(s.data)) for s in after.sections]
    assert all(bytes(a.data) == bytes(b.data) for a, b in zip(before.sections[1:], after.sections[1:]))
    return bytes(target), {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(bytes(target)),
                           'shared_point_offset': POINT, 'point_before': [116, 0], 'point_after': [136, 0],
                           'unique_native_pointer_owner': refs[0], 'all_heading_text_and_number_columns_preserved': True,
                           'expected_heading_right_edges': [160, 196, 232],
                           'no_file_section_pool_or_arena_growth': True,
                           'changed_records': ['CREW_SHARED_COLUMN_HEADER_ORIGIN']}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-crew-column-alignment-v1' or sha(source) != config['source_arm9_sha256']:
        raise ValueError('Reviewed crew header source/config differs')
    target, report = transform(source)
    if sha(target) != config['target_arm9_sha256']:
        raise ValueError('Reviewed crew header target differs')
    return target, report
