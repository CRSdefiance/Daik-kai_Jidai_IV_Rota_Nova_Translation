"""Build gates for the two complete, in-place wireless transition statuses."""

import hashlib
import json
from pathlib import Path

SLOTS = {'GRAND_RACE_UI_WAIT_REGISTRATION': (0x16B9B4, 40),
         'GRAND_RACE_UI_HOST_STARTING': (0x16BA08, 28)}
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
LOCKS = ((0xF8A00, 0xF8B4C), (0xF8CCC, 0xF8D00), (0xF912C, 0xF9174),
         (0xF98FC, 0xF9A6C), (0xF9F54, 0xF9F90), (0xFA0CC, 0xFA11C),
         (0x12ECF4, 0x12ECFC), (0x12EC84, 0x12EC8C),
         (0x16B9DC, 0x16B9E0), (0x16BA24, 0x16BA28),
         (0xFAFFC, 0xFB038), (0xF37D8, 0xF3830),
         (0xD1604, 0xD1850), (0x16B290, 0x16B29C))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compile_records(manuscript, source):
    if manuscript.get('translation_policy') != 'natural-dialogue-v2' or manuscript.get('target_locale') != 'en-US':
        raise ValueError('Transition statuses require reviewed natural English policy')
    rows = manuscript.get('records', [])
    if len(rows) != 2 or {r.get('id') for r in rows} != set(SLOTS):
        raise ValueError('Both complete transition statuses are required')
    records = []
    for row in rows:
        if any(row.get('review', {}).get(gate) is not True for gate in GATES):
            raise ValueError('Transition status has an incomplete review gate')
        offset, capacity = SLOTS[row['id']]
        parts = row['source_parts_in_reading_order']
        if len(parts) != 1 or parts[0]['offset'] != offset:
            raise ValueError('Transition source ownership differs')
        raw = bytes.fromhex(parts[0]['source_hex'])
        original = source[offset:offset + capacity]
        if not raw.endswith(b'\0') or original != raw.ljust(capacity, b'\0'):
            raise ValueError('Complete Japanese source/padding differs')
        english = row['english']
        if not english or english != english.strip() or '  ' in english or any(not 32 <= ord(c) <= 126 for c in english):
            raise ValueError('Status must be one complete printable ASCII paragraph')
        if len(english.encode('ascii')) + 1 > capacity or 16 + len(english) * 6 > 256:
            raise ValueError('Complete status exceeds native allocation/display bounds')
        records.append({**{key: row[key] for key in
                           ('id', 'english', 'speaker', 'context', 'source_meaning', 'localization_note', 'review')},
                        'offset': offset, 'source_hex': original.hex().upper(),
                        'presentation': 'wireless-immediate-ascii-body-v1'})
    return records


def validate_release_batch(batch, source):
    if batch.get('editorial_policy') != 'natural-dialogue-v2' or batch.get('target_locale') != 'en-US':
        raise ValueError('Transition batch requires per-record natural English gates')
    policy = batch['native_wireless_status']
    path = Path(policy['manuscript'])
    if sha(path.read_bytes()) != policy['manuscript_sha256']:
        raise ValueError('Transition manuscript changed after review')
    if compile_records(json.loads(path.read_text(encoding='utf-8')), source) != batch['records']:
        raise ValueError('Transition batch differs from complete reviewed manuscript')
    locks = policy['consumer_locks']
    if [(lock['start'], lock['end']) for lock in locks] != list(LOCKS):
        raise ValueError('Transition consumer coverage differs')
    if any(sha(source[r['start']:r['end']]) != r['sha256'] for r in locks):
        raise ValueError('Native transition caller/renderer/clear rows changed')
