"""Regenerate source-locked race-help bytes at every integrated build."""

import hashlib
import json
import struct
from pathlib import Path

from dk4tool.dialogue.grand_race_help import format_page
from dk4tool.rom.nds import NdsImage

DESCRIPTORS = frozenset((0x1152AC, 0x1152B4, 0x1152BC, 0x1152C4,
                         0x1152CC, 0x1152D4, 0x1152DC, 0x1152EC, 0x1152FC))
REGION = (0x137B90, 0x138294)
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
PRESENTATION = 'grand-race-help-native-ascii-v1'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compile_records(manuscript, source, japanese):
    if manuscript.get('translation_policy') != 'natural-dialogue-v2' or manuscript.get('target_locale') != 'en-US':
        raise ValueError('Race help requires reviewed natural-dialogue-v2 en-US')
    if manuscript.get('source_arm9_sha256') != sha(japanese):
        raise ValueError('Race help clean Japanese component hash differs')
    rows = manuscript.get('records', [])
    if len(rows) != 9 or {r['descriptor_offset'] for r in rows} != DESCRIPTORS:
        raise ValueError('Race help requires all nine mapped pages')
    if len({r['id'] for r in rows}) != 9:
        raise ValueError('Race help contains duplicate page IDs')
    lo, hi = REGION
    if source[lo:hi] != japanese[lo:hi]:
        raise ValueError('Race help blob differs from complete clean source')
    region = bytearray(hi - lo)
    cursor = 0
    records, selections = [], []
    source_cursor = lo
    for row in sorted(rows, key=lambda r: r['source_offset']):
        if any(row.get('review', {}).get(gate) is not True for gate in GATES):
            raise ValueError(f"{row['id']}: race-help review gate is incomplete")
        for field in ('speaker', 'context', 'source_meaning', 'localization_note'):
            if not str(row.get(field, '')).strip():
                raise ValueError(f"{row['id']}: missing {field}")
        old, descriptor = row['source_offset'], row['descriptor_offset']
        raw_source = bytes.fromhex(row['source_hex'])
        if not raw_source.endswith(b'\0') or not lo <= old < old + len(raw_source) <= hi:
            raise ValueError('Race-help source span falls outside original blob')
        if old < source_cursor or any(japanese[source_cursor:old]):
            raise ValueError('Race-help source ownership or zero padding differs')
        source_cursor = old + len(raw_source)
        if japanese[old:source_cursor] != raw_source or raw_source[:-1].decode('cp932') != row['japanese']:
            raise ValueError('Race-help complete Japanese body differs')
        title_pointer, body_pointer = struct.unpack_from('<II', source, descriptor)
        if (title_pointer, body_pointer) != (0x02000000 + row['title_offset'], 0x02000000 + old):
            raise ValueError('Race-help descriptor differs')
        if source[descriptor:descriptor + 8] != japanese[descriptor:descriptor + 8]:
            raise ValueError('Race-help descriptor differs from Japanese source')
        markup, body, lines, _ = format_page(row['english'])
        if cursor + len(body) + 1 > len(region):
            raise ValueError('Complete formatted race help exceeds original shared allocation')
        region[cursor:cursor + len(body) + 1] = body + b'\0'
        pointer_field = descriptor + 4
        new_offset = lo + cursor
        records.append({'id': row['id'] + '_BODY_POINTER', 'offset': pointer_field,
                        'source_hex': source[pointer_field:pointer_field + 4].hex().upper(),
                        'replacement_hex': struct.pack('<I', 0x02000000 + new_offset).hex().upper()})
        title_offset = row['title_offset']
        japanese_title = japanese[title_offset:].split(b'\0', 1)[0] + b'\0'
        slot_bytes = (len(japanese_title) + 3) & ~3
        locked_slot = source[title_offset:title_offset + slot_bytes]
        clean_slot = japanese[title_offset:title_offset + slot_bytes]
        if any(clean_slot[len(japanese_title):]):
            raise ValueError('Heading alignment padding contains unrelated data')
        title = row['draft_english_title']
        if not title or any(not 32 <= ord(c) < 127 for c in title) or len(title) * 6 > 252:
            raise ValueError('Heading is not safe single-line ASCII')
        title_raw = title.encode('ascii') + b'\0'
        if len(title_raw) > slot_bytes:
            raise ValueError('Full English heading exceeds source-locked padded slot')
        if descriptor == 0x1152C4:
            # Existing Map layer owns this slot; retain it without overlap.
            if locked_slot.split(b'\0', 1)[0] != title.encode('ascii'):
                raise ValueError('Accepted Map heading differs')
        else:
            if locked_slot != clean_slot:
                raise ValueError('Heading differs from clean source')
            records.append({'id': row['id'] + '_TITLE', 'offset': title_offset,
                            'source_hex': locked_slot.hex().upper(), 'english': title,
                            'clean_japanese': japanese_title[:-1].decode('cp932')})
        selections.append({'id': row['id'], 'descriptor': descriptor, 'new_offset': new_offset,
                           'english': row['english'], 'title': title, 'title_slot_bytes': slot_bytes,
                           'encoded_hex': body.hex().upper(), 'formatted_markup': markup,
                           'visible_lines': lines})
        cursor += len(body) + 1
    if source_cursor != hi:
        raise ValueError('Race-help manuscript does not cover entire original blob')
    records.append({'id': 'DK4_GRAND_RACE_COMPLETE_HELP_BLOB', 'offset': lo,
                    'source_hex': source[lo:hi].hex().upper(), 'replacement_hex': region.hex().upper()})
    if len(records) != 18:
        raise ValueError('Race-help patch requires nine pointers, eight headings and one complete blob')
    return records, selections, cursor


def validate_release_batch(batch, source):
    policy = batch.get('native_text_repack', {})
    if policy.get('presentation') != PRESENTATION:
        raise ValueError('Unknown native text repack presentation')
    path = Path(policy['manuscript'])
    if sha(path.read_bytes()) != policy['manuscript_sha256']:
        raise ValueError('Race-help manuscript hash differs from reviewed batch')
    manuscript = json.loads(path.read_text(encoding='utf-8'))
    japanese = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    records, _, _ = compile_records(manuscript, source, japanese)
    if records != batch['records']:
        raise ValueError('Race-help bytes do not match complete automatically formatted manuscript')
    locks = policy['consumer_locks']
    expected_spans = ((0x3E8E8, 0x3EA04), (0x3F190, 0x3F3DC), (0x3F51C, 0x3F758),
                      (0xD4DA8, 0xD4FC8), (0xD5070, 0xD51AC), (0xD5404, 0xD5824),
                      (0xD596C, 0xD5AF8), (0x1603E4, 0x160408), (0x5CA8, 0x5D34),
                      (0xD1AAC, 0xD1ACC), (0xD1B14, 0xD1B3C), (0x10E120, 0x10E154),
                      (0x3E4D8, 0x3E6D0), (0x3EA38, 0x3EA54), (0xD43B0, 0xD4440),
                      (0xD3A1C, 0xD3A7C), (0xD4A7C, 0xD4B88), (0x160360, 0x160384))
    if [(r['start'], r['end']) for r in locks] != list(expected_spans):
        raise ValueError('Race-help consumer lock coverage differs')
    if any(sha(source[r['start']:r['end']]) != r['accepted_and_current_sha256'] for r in locks):
        raise ValueError('Race-help accepted renderer/geometry differs')
