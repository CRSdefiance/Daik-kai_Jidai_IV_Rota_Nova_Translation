"""Translate the complete original Characters gallery within its owned slots."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

BASE = 0x02000000
TABLE = 0x13A798
NAMES = (
    'Rafael', 'Hodram', 'Lil', 'Maria', 'Claudio', 'Janus', 'Julio', 'Arcadius',
    'Gerhard', 'Charles', 'Manuel', 'Sera', 'Camille', 'Fernando', 'Emilio',
    'Cristina', 'Angelo', 'Cesare', 'Al', 'Samwell', 'Carlo', 'Yifa', 'Julian',
    'Ian', 'Yukihisa', 'Jam', 'Xien', 'Aziza', 'Clifford', 'Valdes', 'Hayreddin',
    'Pasha', 'Uddin', 'Kuhn', 'Escante', 'Blanco', 'Simon', 'Charlotte', 'Mivor',
    'Sanghyeon', 'Sirwood', 'Bianca',
)


def rows(clean):
    result = [{'id': 'CHARACTERS_GALLERY_TITLE', 'offset': 0x138A4C, 'capacity': 12,
               'Japanese': '登場人物', 'English': 'Characters'},
              {'id': 'CHARACTERS_GALLERY_DESCRIPTION', 'offset': 0x139514, 'capacity': 24,
               'Japanese': '物語の主要な登場人物', 'English': "The story's main cast."}]
    for index, name in enumerate(NAMES):
        pointer = struct.unpack_from('<I', clean, TABLE + index * 4)[0]
        offset = pointer - BASE
        source = clean[offset:].split(b'\0')[0]
        text = source.decode('cp932')
        assert text.startswith(f'{index:02d} ')
        capacity = (len(source) + 1 + 3) // 4 * 4
        english = f'{index:02d} {name}'
        assert len(english.encode('ascii')) + 1 <= capacity
        assert 128 - len(english) * 3 >= 32 and 128 + len(english) * 3 <= 224
        result.append({'id': f'CHARACTERS_GALLERY_NAME_{index:02d}', 'index': index,
                       'offset': offset, 'capacity': capacity, 'pointer_field': TABLE + index * 4,
                       'Japanese': text, 'English': english})
    assert len(result) == 44 and struct.unpack_from('<I', clean, TABLE + 42 * 4)[0] == 0
    return result


def transform(arm):
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[TABLE:TABLE + 172] == clean[TABLE:TABLE + 172]
    result = bytearray(arm)
    translated = rows(clean)
    spans = []
    for row in translated:
        offset, capacity = row['offset'], row['capacity']
        expected = (row['Japanese'].encode('cp932') + b'\0').ljust(capacity, b'\0')
        assert clean[offset:offset + capacity] == expected
        assert arm[offset:offset + capacity] == expected
        assert not any(offset < hi and lo < offset + capacity for lo, hi in spans)
        text = (row['English'].encode('ascii') + b'\0').ljust(capacity, b'\0')
        assert len(text) == capacity
        result[offset:offset + capacity] = text
        spans.append((offset, offset + capacity))
    restored = bytearray(result)
    for lo, hi in spans:
        restored[lo:hi] = arm[lo:hi]
    assert restored == arm and len(result) == len(arm)
    return bytes(result), {'changed_records': [r['id'] for r in translated],
                           'translated_source_owned_slots': translated,
                           'all42_indexed_names_and_both_Gallery_text_fields_translated': True,
                           'original_numbers_pointers_code_palettes_borders_and_dimensions_unchanged': True,
                           'no_allocation_or_pool_growth': True,
                           'actual_cold_boot_all42_screen_masks_required': True,
                           'status': 'experimental'}


def apply_release(arm, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-characters-gallery-text-v1'
    assert config['translation_policy'] == 'natural-dialogue-v2'
    assert sha(arm) == config['source_arm9_sha256']
    result, report = transform(arm)
    assert sha(result) == config['target_arm9_sha256']
    return result, report
