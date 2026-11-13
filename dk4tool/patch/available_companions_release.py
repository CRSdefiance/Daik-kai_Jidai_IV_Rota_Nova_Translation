"""Reviewed empty eligible-companion message with complete adjacent pool preservation."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = '5939d4730b0a30ae68f9dc4c98b9170a807b3f54d1af4670607148005b6d9ab8'
ENGLISH = 'No companions are available!'
OWNERS = [(0x13880C, 56, 0x3FD4C), (0x138844, 52, 0x3FDD0),
          (0x138878, 8, 0x408CC), (0x138880, 20, 0x40BF0)]


def transform(source, pool):
    if sha(source) != SOURCE or pool['source_span'] != [0x13880C, 0x138894]:
        raise ValueError('Companion release requires exact complete V146 source/pool')
    start, end = pool['source_span']
    expected_refs = [('arm9', field, at) for at, _, field in OWNERS]
    actual_refs = [('arm9', p, struct.unpack_from('<I', source, p)[0] - 0x02000000)
                   for p in range(len(source) - 3)
                   if start <= struct.unpack_from('<I', source, p)[0] - 0x02000000 < end]
    if actual_refs != expected_refs or pool['references'] != [list(r) for r in expected_refs]:
        raise ValueError('Complete companion pool reference set differs')
    if len(pool['moves']) != 4:
        raise ValueError('All four complete companion pool owners required')
    packed, moves = bytearray(), []
    saved = bytearray(source)
    for owner, (at, capacity, field) in zip(pool['moves'], OWNERS, strict=True):
        original = source[at:at + capacity]
        if (owner['old_offset'] != at or owner['source_capacity'] != capacity
                or owner['field_offset'] != field
                or bytes.fromhex(owner['original_allocation_hex']) != original):
            raise ValueError('Companion neighboring owner allocation differs')
        raw = original.split(b'\0', 1)[0] + b'\0'
        if any(original[len(raw):]):
            raise ValueError('Companion pool source padding differs')
        if at == 0x138880:
            raw = ENGLISH.encode('ascii') + b'\0'
        new = start + len(packed)
        if owner['new_offset'] != new or owner['complete_text'] != raw[:-1].decode('cp932'):
            raise ValueError('Companion full prose or preserved neighboring wording differs')
        moves.append({'old_offset': at, 'new_offset': new, 'field_offset': field})
        packed.extend(raw)
        packed.extend(b'\0' * (-len(packed) % 4))
        struct.pack_into('<I', saved, field, 0x02000000 + new)
    if len(packed) != 108 or pool['used_aligned_bytes'] != 108 or pool['owned_bytes'] != 136:
        raise ValueError('Complete companion aligned allocation differs')
    saved[start:end] = packed.ljust(end - start, b'\0')
    restored = bytearray(saved)
    restored[start:end] = source[start:end]
    for _, _, field in OWNERS:
        restored[field:field + 4] = source[field:field + 4]
    if bytes(restored) != source:
        raise ValueError('Companion release changes unrelated ARM9 bytes')
    return bytes(saved), moves


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-available-companions-release-v1' or sha(source) != SOURCE:
        raise ValueError('Companion release requires exact complete V146')
    required = {config['manuscript'], config['pool'], config['native_review']}
    if set(config['dependencies']) != required:
        raise ValueError('All companion release dependencies required')
    for path, digest in config['dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Companion manuscript/pool/native review changed')
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    if len(document['records']) != 1:
        raise ValueError('One complete companion source record required')
    row = document['records'][0]
    if (row['offset'] != 0x138880 or row['capacity'] != 20
            or row['english'] != ENGLISH + '{PAD}' or row['japanese'] != '仲間がいません！'):
        raise ValueError('Companion complete source/prose differs')
    for path, digest in [('work/clean.nds', 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'),
                         ('out/raphael_natural_v2_accepted_base.nds', '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe')]:
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Companion clean/canonical source differs')
        original = NdsImage.open(path).read_file('/__arm9__.bin')[0x138880:0x138894]
        if original != bytes.fromhex(row['source_hex']) or original != source[0x138880:0x138894]:
            raise ValueError('Companion clean Japanese allocation differs')
    review = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    visual = review['native_ink_visual_review']
    branch = review['native_empty_branch']
    if (review['status'] != 'reviewed-native-companion-layout-gameplay-pending'
            or len(review['inherited_options_cases']) != 10
            or len(review['native_options_response_cases']) != 20
            or len(review['native_parenthesized_format_cases']) != 6
            or len(review['pixel_cases']) != 2
            or visual['panels_reviewed'] != 1
            or visual['single_row_full_sentence_exclamation_and_leading_final_glyphs'] is not True
            or branch['complete_text'] != ENGLISH
            or any(branch[key] is not True for key in (
                'native_zero_count_branch_formatter_and_macros_verified',
                'native_empty_return_zero_and_stack_preserved', 'positive_count_bypasses_error'))):
        raise ValueError('Complete reviewed native companion evidence required')
    for lock in review['consumer_locks']:
        if sha(source[lock['start']:lock['end']]) != lock['sha256']:
            raise ValueError('Companion native consumer changed')
    pool = json.loads(Path(config['pool']).read_text(encoding='utf-8'))
    saved, moves = transform(source, pool)
    if sha(saved) != config['target_arm9_sha256'] or sha(saved) != review['research_arm9_sha256']:
        raise ValueError('Companion release differs from reviewed native bytes')
    return saved, {'status': 'pass-native-companion-release-gameplay-pending',
                   'arm9_sha256': sha(saved), 'moves': moves, 'used_aligned_bytes': 108,
                   'owned_bytes': 136, 'inherited_owners_preserved': 3,
                   'references_relocated': 4, 'all_other_arm9_bytes_preserved': True,
                   'runtime_verified': False}
