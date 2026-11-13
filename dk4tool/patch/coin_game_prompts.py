"""Natural English coin-game prompts in existing source-owned ARM9 storage."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

BASE = 0x02000000
START, END = 0x145098, 0x1450DC
ROWS = [(0x145098, 0x639EC, '先攻後攻をきめようか'),
        (0x1450B0, 0x639F0, 'あんたの番からだぜ'),
        (0x1450C4, 0x639F4, '俺からいかせてもらうぜ')]


def transform(arm, manuscript):
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[START:END] == clean[START:END]
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    assert manuscript['target_locale'] == 'en-US'
    assert len(manuscript['records']) == 3
    result = bytearray(arm)
    position = START
    cases = []
    for row, (old, literal, japanese) in zip(manuscript['records'], ROWS):
        raw = clean[old:END].split(b'\0')[0]
        assert raw.decode('cp932') == row['japanese'] == japanese
        assert all(row['review'][g] is True for g in ['source', 'context', 'localization', 'naturalness', 'formatting'])
        assert all(row[k] for k in ['id', 'speaker', 'context', 'source_meaning', 'localization_note'])
        english = row['english']
        assert english == english.strip() and '\n' not in english and '{' not in english
        data = english.encode('ascii') + b'\0'
        capacity = (len(data) + 3) & ~3
        assert position + capacity <= END and len(english) <= 36
        needle = struct.pack('<I', BASE + old)
        references, offset = [], 0
        while (offset := arm.find(needle, offset)) >= 0:
            references.append(offset)
            offset += 1
        assert references == [literal], ('Unexpected source pointer references', japanese, references)
        result[position:position + capacity] = data.ljust(capacity, b'\0')
        struct.pack_into('<I', result, literal, BASE + position)
        cases.append({'id': row['id'], 'japanese': japanese, 'english': english,
                      'original_offset': old, 'compiled_offset': position,
                      'pointer_literal': literal, 'allocated_bytes': capacity})
        position += capacity
    result[position:END] = bytes(END - position)
    changed = [i for i, (a, b) in enumerate(zip(arm, result)) if a != b]
    assert all(START <= i < END or any(literal <= i < literal + 4 for _, literal, _ in ROWS) for i in changed)
    restored = bytearray(result)
    restored[START:END] = arm[START:END]
    for _, literal, _ in ROWS:
        restored[literal:literal + 4] = arm[literal:literal + 4]
    assert restored == arm and len(result) == len(arm)
    return bytes(result), {'changed_records': [r['id'] for r in cases], 'records': cases,
                           'owned_span': [START, END], 'used_bytes': position - START,
                           'free_bytes': END - position, 'changed_bytes': changed,
                           'only_owned_strings_and_guarded_pointer_literals_changed': True,
                           'code_section_extents_heap_startup_cache_and_unowned_data_unchanged': True,
                           'actual_native_message_mask_verification_required': True, 'status': 'experimental'}


def apply_release(arm, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-coin-game-prompts-v1'
    assert sha(arm) == config['source_arm9_sha256']
    manuscript_path = Path(config['manuscript'])
    assert sha(manuscript_path.read_bytes()) == config['manuscript_sha256']
    result, report = transform(arm, json.loads(manuscript_path.read_text(encoding='utf-8')))
    assert sha(result) == config['target_arm9_sha256']
    return result, report
