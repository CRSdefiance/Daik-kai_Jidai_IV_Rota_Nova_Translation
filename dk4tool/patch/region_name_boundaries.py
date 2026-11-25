"""Own and terminate the complete shared region-name family without pool growth."""

import json
import struct
from itertools import pairwise
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

BASE, START, END, TABLE = 0x02000000, 0x14C79C, 0x14C7EC, 0x119B08
SOURCE = '1f6ed33c8ee91bdeb1667e3f7524f3731ac7b0ba89a07f4be4ee1422cd7851bb'
LABELS = ('N. Sea', 'Med.', 'Africa', 'Indian', 'SE Asia ', 'E Asia', 'Americas', 'Global')


def pointer_census(data):
    return [(at, struct.unpack_from('<I', data, at)[0]) for at in range(len(data) - 3)
            if BASE + START <= struct.unpack_from('<I', data, at)[0] < BASE + END]


def validate_names(data):
    rows = []
    for index, expected in enumerate(LABELS):
        field = TABLE + index * 52
        pointer = struct.unpack_from('<I', data, field)[0]
        at = pointer - BASE
        if not START <= at < END:
            raise ValueError('Region name points outside its owned span')
        end = data.find(b'\0', at, END)
        if end < 0 or data[at:end] != expected.encode('ascii'):
            raise ValueError(f'Region{index} has a missing terminator or joined label')
        if any(other['pointer'] <= pointer <= other['terminator'] for other in rows):
            raise ValueError('Independent region names overlap')
        rows.append({'index': index, 'field': field, 'pointer': pointer,
                     'terminator': BASE + end, 'English': expected})
    intervals = sorted((r['pointer'], r['terminator'] + 1) for r in rows)
    if any(a[1] > b[0] for a, b in pairwise(intervals)):
        raise ValueError('Region names share terminator or character storage')
    return rows


def transform(source, clean, config):
    if sha(source) != SOURCE:
        raise ValueError('Region-name repair requires the exact complete V636 ARM9')
    records = config['records']
    if len(records) != 8 or [r['index'] for r in records] != list(range(8)):
        raise ValueError('All eight original name owners are required')
    fields = {TABLE + i * 52 for i in range(8)}
    refs = pointer_census(source)
    if {at for at, _ in refs} != fields or len(refs) != 8:
        raise ValueError('A region-name interior alias or unknown owner exists')
    if source[END:END + 28] != clean[END:END + 28]:
        raise ValueError('Adjacent original integer array differs')
    if struct.unpack_from('<I', source, 0x94588)[0] != BASE + END:
        raise ValueError('Original integer-array pointer differs')
    result = bytearray(source)
    payload, moves = bytearray(), []
    for row in sorted(records, key=lambda r: r['source_offset']):
        index, old = row['index'], row['source_offset']
        field = TABLE + index * 52
        if struct.unpack_from('<I', source, field)[0] != BASE + old:
            raise ValueError('Region name owner pointer differs')
        jp_ptr = struct.unpack_from('<I', clean, field)[0] - BASE
        if clean[jp_ptr:clean.index(0, jp_ptr)].decode('cp932') != row['Japanese']:
            raise ValueError('Original Japanese name identity differs')
        if row['English'] != LABELS[index] or not all(row['review'].values()):
            raise ValueError('Region wording or boundary review differs')
        encoded = row['English'].encode('ascii') + b'\0'
        new = START + len(payload)
        payload.extend(encoded)
        payload.extend(bytes(-len(payload) % 4))
        struct.pack_into('<I', result, field, BASE + new)
        moves.append({'index': index, 'field': field, 'old_offset': old, 'new_offset': new,
                      'English': row['English'], 'independently_owned_terminator': BASE + new + len(encoded) - 1})
        if source[field + 4:field + 52] != clean[field + 4:field + 52]:
            raise ValueError('Original map geometry/metadata differs')
    if len(payload) != 72 or len(payload) > END - START:
        raise ValueError('Require complete terminated names in the original80-byte span')
    result[START:END] = payload + bytes(END - START - len(payload))
    names = validate_names(result)
    if pointer_census(result) != sorted((r['field'], r['pointer']) for r in names):
        raise ValueError('Final name references differ from the eight reviewed owners')
    restored = bytearray(result)
    restored[START:END] = source[START:END]
    for field in fields:
        restored[field:field + 4] = source[field:field + 4]
    if restored != source:
        raise ValueError('Unowned ARM9 bytes changed')
    a, b = MainCodeFile(source, BASE), MainCodeFile(bytes(result), BASE)
    if [(s.ramAddress, len(s.data), s.bssSize) for s in a.sections] != [(s.ramAddress, len(s.data), s.bssSize) for s in b.sections]:
        raise ValueError('Code section shape changed')
    if any(x.data != y.data for x, y in zip(a.sections[1:], b.sections[1:], strict=True)):
        raise ValueError('Staged code/data or ITCM changed')
    return bytes(result), {
        'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(result),
        'owned_name_span': [START, END], 'packed_name_bytes': len(payload),
        'all8_final_name_owners': names, 'all8_owner_moves': moves,
        'source_and_target_every_byte_pointer_census_exact8_owners': True,
        'adjacent_integer_array_at_END_and_its_original_pointer_preserved': True,
        'all_source_wording_geometry_metadata_code_palettes_and_other_bytes_preserved': True,
        'no_section_pool_or_startup_growth': True,
        'changed_records': ['ALL8_SHARED_REGION_NAME_OWNERS_AND_NUL_BOUNDARIES'],
    }


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-region-name-boundaries-v1' or config.get('status') != 'reviewed-native-previews-experimental':
        raise ValueError('Reviewed complete region-name configuration required')
    target, proof = transform(source, clean, config)
    if sha(target) != config['target_arm9_sha256']:
        raise ValueError('Region-name result differs from reviewed preview')
    return target, proof
