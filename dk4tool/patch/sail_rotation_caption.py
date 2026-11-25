"""Restore the source-faithful sail rotation verb in its original allocation."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = 'b43443ef5f6a4e7d47679ab7dcfa3e158f25cd5c27cdfe1a5b9d5e1c0fb52880'
OFFSET, OWNER = 0x147928, 0x119138


def transform(source, clean, canonical):
    if sha(source) != SOURCE:
        raise ValueError('Exact complete V322 ARM9 required')
    if clean[OFFSET:OFFSET + 8] != '帆回転'.encode('cp932') + b'\0\0':
        raise ValueError('Original sail-rotation text differs')
    if source[OFFSET:OFFSET + 8] != b'Sails \0\0' or canonical[OFFSET:OFFSET + 8] != b'Rotate\0\0':
        raise ValueError('Inherited or canonical rotation text differs')
    pointer = struct.pack('<I', 0x02000000 + OFFSET)
    for arm in (source, clean, canonical):
        if [i for i in range(len(arm) - 3) if arm[i:i + 4] == pointer] != [OWNER]:
            raise ValueError('Sail-rotation caption owner differs')
    target = bytearray(source)
    target[OFFSET:OFFSET + 8] = b'Rotate\0\0'
    saved = bytes(target)
    assert saved[:OFFSET] == source[:OFFSET] and saved[OFFSET + 8:] == source[OFFSET + 8:]
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'Japanese': '帆回転', 'English': 'Rotate', 'original_offset': OFFSET,
                   'original_capacity': 8, 'unchanged_unique_owner': OWNER,
                   'canonical_complete_English_restored': True,
                   'all_other_code_pointers_fonts_helpers_arenas_and_labels_exact': True,
                   'changed_records': ['DK4_SEA_ROTATE_SAILS_VERB']}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-sail-rotation-caption-release-v1':
        raise ValueError('Unknown rotation caption release')
    for filename, digest in config['verification_evidence_sha256'].items():
        if sha(Path(filename).read_bytes()) != digest:
            raise ValueError('Rotation caption native evidence differs')
    target, proof = transform(source, clean, canonical)
    if sha(target) != config['target_arm9_sha256']:
        raise ValueError('Rotation caption target differs')
    return target, proof
