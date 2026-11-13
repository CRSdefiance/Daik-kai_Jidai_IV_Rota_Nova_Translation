"""Translate three original Gallery labels without changing their native gates."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

BASE = 0x02000000
SOURCE = '3f620bb31b4465b5b500ba8cbe49730fd64f86e60e8eaca969f875d473e04cd5'
FIELDS = (('GALLERY_RUINS_MENU', 0x13894C, 8, 0x115718, '史跡', 'Ruins'),
          ('GALLERY_CHARACTERS_MENU', 0x1389EC, 12, 0x115728, '登場人物', 'Characters'),
          ('GALLERY_EVENT_SCENES_MENU', 0x138EFC, 16, 0x115738, 'イベントシーン', 'Event Scenes'))


def transform(source, clean, canonical):
    if sha(source) != SOURCE:
        raise ValueError('Exact complete V305 ARM9 required')
    target, changes = bytearray(source), []
    for ident, offset, capacity, field, japanese, english in FIELDS:
        original = (japanese.encode('cp932') + b'\0').ljust(capacity, b'\0')
        if any(arm[offset:offset + capacity] != original for arm in (source, clean, canonical)):
            raise ValueError('Gallery original/canonical/current string allocation differs')
        pointer = BASE + offset
        if any(struct.unpack_from('<I', arm, field)[0] != pointer for arm in (source, clean, canonical)):
            raise ValueError('Gallery table owner differs')
        word = struct.pack('<I', pointer)
        if [i for i in range(len(source) - 3) if source[i:i + 4] == word] != [field]:
            raise ValueError('Gallery label has unclassified pointer aliases')
        raw = english.encode('ascii') + b'\0'
        if len(raw) > capacity:
            raise ValueError('Complete Gallery label does not fit')
        target[offset:offset + capacity] = raw.ljust(capacity, b'\0')
        changes.append({'id': ident, 'offset': offset, 'capacity': capacity, 'table_field': field,
                        'source_Japanese': japanese, 'English': english, 'source_hex': original.hex(),
                        'target_hex': target[offset:offset + capacity].hex(),
                        'meaning': 'Historic sites' if english == 'Ruins' else english})
    restored = bytearray(target)
    for row in changes:
        at, length = row['offset'], row['capacity']
        restored[at:at + length] = source[at:at + length]
    if restored != source:
        raise ValueError('Unrelated Gallery code, table, gates or strings change')
    saved = bytes(target)
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved), 'records': changes,
                   'changed_records': [r['id'] for r in changes],
                   'all_native_gates_pointers_capacity_metadata_and_other_bytes_exact': True}


def apply_release(source, clean, canonical, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-gallery-menu-label-release-v1':
        raise ValueError('Unknown Gallery menu label release')
    for filename, digest in config.get('verification_evidence_sha256', {}).items():
        if sha(Path(filename).read_bytes()) != digest:
            raise ValueError('Gallery native verification evidence differs')
    saved, report = transform(source, clean, canonical)
    if sha(saved) != config['target_arm9_sha256']:
        raise ValueError('Gallery label target differs')
    return saved, report
