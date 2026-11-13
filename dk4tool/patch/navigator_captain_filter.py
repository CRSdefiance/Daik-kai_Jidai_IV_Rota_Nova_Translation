"""Localize the original shared navigator Captain filter in its owned slot."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

OFFSET, FIELD = 0x14F33C, 0x14F470
JAPANESE, ENGLISH = '艦長', 'Captain'
BEFORE = JAPANESE.encode('cp932') + bytes(4)
AFTER = ENGLISH.encode('ascii') + b'\0'


def transform(source, clean):
    assert len(BEFORE) == len(AFTER) == 8
    if source[OFFSET:OFFSET + 8] != BEFORE or clean[OFFSET:OFFSET + 8] != BEFORE:
        raise ValueError('Original complete eight-byte Captain filter slot differs')
    if any(struct.unpack_from('<2I', data, FIELD) != (0x02000000 + OFFSET, 1)
           for data in (source, clean)):
        raise ValueError('Original enabled Captain filter descriptor differs')
    result = bytearray(source)
    result[OFFSET:OFFSET + 8] = AFTER
    assert result[:OFFSET] == source[:OFFSET] and result[OFFSET + 8:] == source[OFFSET + 8:]
    return bytes(result), {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(result),
        'changed_records': ['DK4_NAVIGATOR_FILTER_CAPTAIN'], 'source_Japanese': JAPANESE,
        'English': ENGLISH, 'original_allocation': [OFFSET, OFFSET + 8],
        'original_descriptor': FIELD, 'all_other_ARM9_bytes_identical': True,
        'no_code_pointer_palette_pool_size_or_gameplay_change': True,
        'status': 'experimental', 'full_goal_complete': False}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-navigator-captain-filter-v1'
    assert sha(source) == config['source_arm9_sha256']
    result, report = transform(source, clean)
    assert sha(result) == config['target_arm9_sha256']
    return result, report
