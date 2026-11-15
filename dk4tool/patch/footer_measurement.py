"""Count all ASCII footer cells while retaining original CP932 pair widths."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = '4bee6c9ed0de8f906e3d98dacd69eb009b6d92bd50c610bc98b07ecc7ba9397b'
CHANGES = ((0xCA7A8, 0xE1A010A0, 0xE0801080), (0xCA7B0, 0xE0040091, 0xE1A04081))
STOP, OWNER = 0x147A48, 0x11915C


def transform(source, clean, canonical):
    if sha(source) != SOURCE:
        raise ValueError('Exact complete V316 required')
    target = bytearray(source)
    for at, old, new in CHANGES:
        if any(struct.unpack_from('<I', arm, at)[0] != old for arm in (source, clean, canonical)):
            raise ValueError('Original footer measurement instructions differ')
        struct.pack_into('<I', target, at, new)
    if any(struct.unpack_from('<I', arm, 0xCA7AC)[0] != 0xE3A0000C for arm in (source, clean, canonical)):
        raise ValueError('Original footer surface height differs')
    original = ('自動移動停止'.encode('cp932') + b'\0').ljust(16, b'\0')
    for arm in (source, clean, canonical):
        if arm[STOP:STOP + 16] != original or struct.unpack_from('<I', arm, OWNER)[0] != 0x02000000 + STOP:
            raise ValueError('Original Stop Auto Move slot or owner differs')
    target[STOP:STOP + 16] = b'Stop Auto Move\0\0'
    restored = bytearray(target)
    for at, _, _ in CHANGES:
        restored[at:at + 4] = source[at:at + 4]
    restored[STOP:STOP + 16] = source[STOP:STOP + 16]
    assert restored == source
    saved = bytes(target)
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'measurement': 'byte_length*6; even CP932 pair widths unchanged',
                   'instruction_changes': [list(row) for row in CHANGES],
                   'surface_height12_original': True, 'complete_Stop_Auto_Move_slot_bytes': 16,
                   'all_other_bytes_pointers_helpers_and_arenas_preserved': True,
                   'changed_records': ['DK4_FOOTER_COMPLETE_ASCII_WIDTH', 'DK4_STOP_AUTO_MOVE_CAPTION']}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-footer-measurement-release-v1':
        raise ValueError('Unknown footer measurement release')
    for filename, digest in config['verification_evidence_sha256'].items():
        if sha(Path(filename).read_bytes()) != digest:
            raise ValueError('Footer verification evidence differs')
    saved, report = transform(source, clean, canonical)
    if sha(saved) != config['target_arm9_sha256']:
        raise ValueError('Footer target differs')
    return saved, report
