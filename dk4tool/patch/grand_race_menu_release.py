"""Build gates for the six complete, in-place native menu labels."""

import hashlib
import json
from pathlib import Path

SLOTS = {'GRAND_RACE_UI_' + name: (offset, size) for name, offset, size in (
    ('LIMITS', 0x13799C, 12), ('BASIC_RULES', 0x1379D8, 12),
    ('MAP_SUPPLIES', 0x137A38, 16), ('READ_RULES', 0x137A58, 16),
    ('ABOUT', 0x137AB8, 16), ('START', 0x137AF8, 20))}
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
LOCKS = ((0x14062C, 0x14066C), (0x293A0, 0x293A8), (0x522FC, 0x5231C),
         (0xACEA4, 0xACF1C), (0xACF7C, 0xAD018), (0xACB10, 0xACBEC),
         (0x521E8, 0x52228), (0xCF0A8, 0xCF208), (0xD5340, 0xD5404),
         (0x116438, 0x116448), (0xACC64, 0xACC9C),
         (0x115354, 0x115374), (0x1153A4, 0x1153E4),
         (0xAD608, 0xAD650), (0xD5404, 0xD5814))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compile_records(manuscript, source):
    if manuscript.get('translation_policy') != 'natural-dialogue-v2' or manuscript.get('target_locale') != 'en-US':
        raise ValueError('Menu labels require reviewed natural English policy')
    rows = manuscript.get('records', [])
    if len(rows) != 6 or {r.get('id') for r in rows} != set(SLOTS):
        raise ValueError('All six complete menu labels are required')
    records = []
    for row in rows:
        if any(row.get('review', {}).get(gate) is not True for gate in GATES):
            raise ValueError('Menu label has an incomplete review gate')
        offset, capacity = SLOTS[row['id']]
        parts = row['source_parts_in_reading_order']
        if len(parts) != 1 or parts[0]['offset'] != offset:
            raise ValueError('Menu source ownership differs')
        raw = bytes.fromhex(parts[0]['source_hex'])
        original = source[offset:offset + capacity]
        if not raw.endswith(b'\0') or original != raw.ljust(capacity, b'\0'):
            raise ValueError('Complete Japanese source/padding differs')
        if any(not row.get(key) for key in ('speaker', 'context', 'source_meaning', 'localization_note')):
            raise ValueError('Menu editorial context is missing')
        english = row['english']
        if not english or english != english.strip() or '  ' in english or any(not 32 <= ord(c) <= 126 for c in english):
            raise ValueError('Menu label must be one complete printable ASCII paragraph')
        if len(english.encode('ascii')) + 1 > capacity or len(english) > 14 or len(english) > 48:
            raise ValueError('Complete label exceeds native allocation/display bounds')
        records.append({**{key: row[key] for key in
                           ('id', 'english', 'speaker', 'context', 'source_meaning', 'localization_note', 'review')},
                        'offset': offset, 'source_hex': original.hex().upper(),
                        'presentation': 'native-centered-menu-ascii-v1'})
    return records


def validate_release_batch(batch, source):
    if batch.get('editorial_policy') != 'natural-dialogue-v2' or batch.get('target_locale') != 'en-US':
        raise ValueError('Menu batch requires per-record natural English gates')
    policy = batch['native_menu_labels']
    path = Path(policy['manuscript'])
    if sha(path.read_bytes()) != policy['manuscript_sha256']:
        raise ValueError('Menu manuscript changed after review')
    if compile_records(json.loads(path.read_text(encoding='utf-8')), source) != batch['records']:
        raise ValueError('Menu batch differs from complete reviewed manuscript')
    locks = policy['consumer_locks']
    if [(lock['start'], lock['end']) for lock in locks] != list(LOCKS):
        raise ValueError('Menu consumer coverage differs')
    if any(sha(source[r['start']:r['end']]) != r['sha256'] for r in locks):
        raise ValueError('Native menu caller/renderer/menu context changed')
