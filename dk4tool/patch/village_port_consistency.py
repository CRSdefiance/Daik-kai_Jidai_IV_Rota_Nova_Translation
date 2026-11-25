"""Unify existing village/port names and compile a consistent village-clue margin."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, cache_plan
from dk4tool.patch.village_portrait_wrap import PREFIX, paragraph
from scripts.verify_village_wrap_v608 import read

SOURCE = 'ab9f748b46388257c9fb847a65b9c06da7920146b985224f5bb0670459ae3fcc'
ALIASES = ((6, 0x1250E0, 0x0215BFF0, 0x0215ADF8, 'Cape Cod'),
           (12, 0x125398, 0x0215D028, 0x0215AE28, 'Dikson'),
           (16, 0x125568, 0x0215D064, 0x0215AE40, 'Leveque'),
           (21, 0x1257AC, 0x0215D76B, 0x0215AE60, 'Tiksi'),
           (22, 0x125820, 0x0215BEC8, 0x0215AE68, 'Korf'))


def aligned_paragraph(text):
    if not text or not text.isascii() or ' '.join(text.split()) != text:
        raise ValueError('Village clue must remain one unchanged ASCII paragraph')
    lines, current = [], ''
    for word in text.split(' '):
        if len(word) > 35:
            raise ValueError('Village clue word exceeds the portrait line budget')
        if current and len(current) + 1 + len(word) > 35:
            lines.append(current)
            current = ''
        current += (' ' if current else '') + word
    lines.append(current)
    if len(lines) > 3:
        raise ValueError('Village clue exceeds the verified three-row portrait field')
    return '\n  '.join(lines)


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Village consistency requires the exact complete V653 ARM9')
    code = MainCodeFile(source, BASE)
    assert bytes(code.save()) == source and len(code.sections) == 5
    before = [bytes(s.data) for s in code.sections]
    plan = cache_plan(source)
    assert plan and len(before[3]) == plan['payload_bytes'] + 48
    names = {r['index']: r['english'] for r in read('translations/village_ui_manuscript_v1.json')['records']
             if r['kind'] == 'name'}
    aliases = []
    for village, field, old, new, english in ALIASES:
        assert names[village] == english
        assert struct.unpack_from('<I', before[0], field)[0] == old
        assert before[0][new - BASE:new - BASE + len(english) + 1] == english.encode('ascii') + b'\0'
        struct.pack_into('<I', code.sections[0].data, field, new)
        aliases.append({'village': village, 'town': village + 90, 'field': field,
                        'old_pointer': old, 'existing_village_name_pointer': new, 'English': english})
    clues, changed = [], []
    for row in read('translations/village_promised_words_manuscript_v1.json')['records']:
        if row['kind'] != 'CLUE':
            continue
        pointer = struct.unpack_from('<I', before[0], row['field'])[0]
        offset = pointer - POOL
        assert 0 <= offset < plan['payload_bytes'] - 64
        old = before[3][offset:].split(b'\0', 1)[0]
        expanded = PREFIX + row['english'] + '.'
        old_expanded, new_expanded = paragraph(expanded), aligned_paragraph(expanded)
        assert old == old_expanded[len(PREFIX):-1].encode('ascii')
        assert ' '.join(new_expanded.split()) == ' '.join(old_expanded.split()) == expanded
        new = new_expanded[len(PREFIX):-1].encode('ascii')
        assert len(new) == len(old), 'This stage owns no storage growth or pointer relocation'
        assert [i % 2 for i, value in enumerate(new) if value == 10] == [
            i % 2 for i, value in enumerate(old) if value == 10
        ], 'Preserve existing packed-renderer line-break byte phase'
        if old != new:
            assert row['index'] in (4, 23)
            code.sections[3].data[offset:offset + len(old)] = new
            changed.append({'index': row['index'], 'pointer': pointer, 'pool_offset': offset,
                'old_hex': old.hex(), 'new_hex': new.hex(),
                'before_expanded': old_expanded, 'after_expanded': new_expanded,
                'unchanged_English': row['english']})
        clues.append({'index': row['index'], 'English': row['english'], 'unchanged_pointer': pointer,
                      'compiled_rows': new_expanded.splitlines(), 'first_and_continuation_budget': 35})
    assert len(clues) == 24 and [r['index'] for r in changed] == [4, 23]
    saved = bytes(code.save())
    after = MainCodeFile(saved, BASE)
    assert cache_plan(saved) == plan
    assert all(bytes(after.sections[i].data) == before[i] for i in (1, 2, 4))
    main_restored = bytearray(after.sections[0].data)
    for _, field, _, _, _ in ALIASES:
        main_restored[field:field + 4] = before[0][field:field + 4]
    assert bytes(main_restored) == before[0]
    pool_restored = bytearray(after.sections[3].data)
    for row in changed:
        at, old = row['pool_offset'], bytes.fromhex(row['old_hex'])
        pool_restored[at:at + len(old)] = old
    assert bytes(pool_restored) == before[3]
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
        'five_original_Town_name_pointer_aliases': aliases,
        'all24_machine_compiled_clue_contracts': clues, 'two_reflowed_clues': changed,
        'existing_name_string_bytes_answers_and_native_code_unchanged': True,
        'all_English_prose_words_and_punctuation_unchanged': True,
        'only_five_existing_metadata_words_and_two_existing_string_spans_owned': True,
        'no_growth_new_storage_fonts_graphics_or_arena_changes': True,
        'experimental': True, 'actual_new_candidate_gameplay_verification_pending': True,
        'full_goal_complete': False}


def apply_release(source, path):
    config = read(Path(path))
    assert config['format'] == 'dk4-village-port-consistency-v1'
    saved, proof = transform(source)
    if config['proof'] != proof:
        raise ValueError('Village consistency source, owned data or target differs')
    return saved, proof
