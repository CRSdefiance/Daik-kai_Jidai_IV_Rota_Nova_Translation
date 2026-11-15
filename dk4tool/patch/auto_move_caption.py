"""Translate the observed Auto Move confirmation in its original12-byte slot."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = '423e95311bcf2e1de375c366a3ac21832fb926630c6ac382dfdf2dcc836afa65'
OFFSET, FIELD, CAPACITY = 0x14DD10, 0x119DA4, 12


def transform(source, clean, canonical):
    if sha(source) != SOURCE:
        raise ValueError('Exact complete V309 ARM9 required')
    original = ('自動移動'.encode('cp932') + b'\0').ljust(CAPACITY, b'\0')
    pointer = struct.pack('<I', 0x02000000 + OFFSET)
    for arm in (source, clean, canonical):
        if arm[OFFSET:OFFSET + CAPACITY] != original or arm[FIELD:FIELD + 4] != pointer:
            raise ValueError('Original Auto Move label or descriptor differs')
    if [n for n in range(len(source) - 3) if source[n:n + 4] == pointer] != [FIELD]:
        raise ValueError('Auto Move label has an unclassified pointer alias')
    target = bytearray(source)
    target[OFFSET:OFFSET + CAPACITY] = b'Auto Move\0\0\0'
    saved = bytes(target)
    assert saved[:OFFSET] == source[:OFFSET] and saved[OFFSET + CAPACITY:] == source[OFFSET + CAPACITY:]
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'source_Japanese': '自動移動', 'English': 'Auto Move', 'offset': OFFSET,
                   'capacity': CAPACITY, 'descriptor_field': FIELD,
                   'all_code_pointers_descriptors_and_other_bytes_exact': True,
                   'changed_records': ['DK4_AUTO_MOVE_CONFIRMATION_LABEL']}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-auto-move-caption-release-v1':
        raise ValueError('Unknown Auto Move caption release')
    for filename, digest in config['verification_evidence_sha256'].items():
        if sha(Path(filename).read_bytes()) != digest:
            raise ValueError('Auto Move native evidence differs')
    saved, proof = transform(source, clean, canonical)
    if sha(saved) != config['target_arm9_sha256']:
        raise ValueError('Auto Move target differs')
    return saved, proof
