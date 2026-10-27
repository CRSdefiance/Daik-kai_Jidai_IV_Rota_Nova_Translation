"""Name the actual at-sea target-information action in its original slot."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = '5deb83d45a56f2594140640fd06bd1edd17cd358451987c25dcbd809c395e409'
OFFSET, CAPACITY = 0x11B514, 8
OWNERS = (0x119140, 0x119158)


def transform(source, clean, canonical):
    if sha(source) != SOURCE:
        raise ValueError('Exact complete V318 ARM9 required')
    original = ('洋上'.encode('cp932') + b'\0').ljust(CAPACITY, b'\0')
    if clean[OFFSET:OFFSET + CAPACITY] != original:
        raise ValueError('Original at-sea caption differs')
    for arm in (source, canonical):
        if arm[OFFSET:OFFSET + CAPACITY] != b'Sea Map\0':
            raise ValueError('Inherited at-sea caption differs')
    pointer = struct.pack('<I', 0x02000000 + OFFSET)
    for arm in (source, clean, canonical):
        aliases = [i for i in range(len(arm) - 3) if arm[i:i + 4] == pointer]
        if aliases != list(OWNERS):
            raise ValueError('At-sea caption owners differ')
    target = bytearray(source)
    target[OFFSET:OFFSET + CAPACITY] = b'Inspect\0'
    saved = bytes(target)
    assert saved[:OFFSET] == source[:OFFSET] and saved[OFFSET + CAPACITY:] == source[OFFSET + CAPACITY:]
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'Japanese': '洋上', 'English': 'Inspect', 'original_offset': OFFSET,
                   'original_capacity': CAPACITY, 'unchanged_owner_fields': list(OWNERS),
                   'all_other_code_pointers_fonts_helpers_and_arenas_exact': True,
                   'changed_records': ['DK4_SEA_TARGET_INSPECT_CAPTION']}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-sea-inspect-caption-release-v1':
        raise ValueError('Unknown at-sea inspect-caption release')
    for filename, digest in config['verification_evidence_sha256'].items():
        if sha(Path(filename).read_bytes()) != digest:
            raise ValueError('Inspect caption verification evidence differs')
    target, proof = transform(source, clean, canonical)
    if sha(target) != config['target_arm9_sha256']:
        raise ValueError('Inspect caption target differs')
    return target, proof
