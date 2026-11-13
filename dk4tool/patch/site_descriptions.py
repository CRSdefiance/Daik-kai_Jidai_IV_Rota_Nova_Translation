"""Complete Gallery prose packed into owned text allocations; no heap growth."""

import json
import struct
import textwrap
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from dk4tool.patch.characters_gallery_text import rows as character_rows
from dk4tool.patch.gallery_caption_bounds import validate
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.historic_site_names import BASE, TABLE
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.compile_scene_caption_allocation import pack
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references, merge_ranges

DESCRIPTION_TABLE = 0x139BF4
IMAGE_TABLE = 0x115748


def formatted(text, profile='static-site-gallery-pending-flush-v3'):
    assert text == text.strip() and '\n' not in text and '  ' not in text
    width = 42 if profile.endswith('v1') else 41
    assert profile in ('static-site-gallery-42-columns-v1', 'static-site-gallery-pair-phase-v2',
                       'static-site-gallery-pending-flush-v3')
    lines = textwrap.wrap(text, width, break_long_words=False, break_on_hyphens=False)
    assert 1 <= len(lines) <= 11 and all(len(line) <= width for line in lines)
    assert ' '.join(lines) == text
    if profile.endswith('v1'):
        return '\n'.join(lines).encode('ascii') + b'\0', lines
    # The virtual painter buffers printable glyphs in pairs; LF itself is
    # handled by D5404 without flushing that buffer. Finish an odd line with
    # an empty glyph so no letter remains pending when its coordinates move.
    # v2 is preserved solely for the rejected raw-byte-parity experiment.
    compiled = bytearray()
    for index, line in enumerate(lines):
        compiled.extend(line.encode('ascii'))
        if index < len(lines) - 1:
            needs_cell = len(line) % 2 == 1 if profile.endswith('v3') else len(compiled) % 2 == 0
            if needs_cell:
                compiled.extend(b' ')
            compiled.extend(b'\n')
    if profile.endswith('v3'):
        assert all(len(line) % 2 == 0 for line in compiled.split(b'\n')[:-1])
    else:
        assert all(i % 2 == 1 for i, value in enumerate(compiled) if value == 10)
    assert [line.rstrip(b' ').decode('ascii') for line in compiled.split(b'\n')] == lines
    assert all(len(line) <= 42 for line in compiled.split(b'\n'))
    return bytes(compiled) + b'\0', lines


def transform(arm, manuscript, *, formatting_profile='static-site-gallery-pending-flush-v3'):
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    names = json.loads(Path('translations/historic_site_names_v2.json').read_text(encoding='utf-8'))
    site_stage = json.loads(Path('work/analysis/historic_sites_v528/transform_proof.json').read_text(encoding='utf-8'))
    records = manuscript['records']
    assert manuscript['translation_policy'] == 'natural-dialogue-v2' and manuscript['target_locale'] == 'en-US'
    assert [r['site_id'] for r in records] == [i for i in range(21) if i not in (1, 4)]
    assert arm[IMAGE_TABLE:IMAGE_TABLE + 84] == clean[IMAGE_TABLE:IMAGE_TABLE + 84]
    source_spans, entries, owners, old_pointers, layouts = [], {}, {}, {}, []
    for row in records:
        assert all(row['review'][k] for k in ('source', 'context', 'localization', 'naturalness'))
        offset, capacity = row['source_offset'], row['source_aligned_capacity']
        source = bytes.fromhex(row['source_hex'])
        assert source.decode('cp932') == row['japanese']
        assert clean[offset:offset + capacity] == arm[offset:offset + capacity] == (source + b'\0').ljust(capacity, b'\0')
        field = DESCRIPTION_TABLE + row['site_id'] * 4
        assert row['pointer_field'] == field and struct.unpack_from('<I', arm, field)[0] == BASE + offset
        entries[row['id']], lines = formatted(row['english'], formatting_profile)
        source_spans.append((offset, offset + capacity))
        owners[field], old_pointers[field] = row['id'], BASE + offset
        layouts.append({'id': row['id'], 'site_id': row['site_id'], 'English': row['english'], 'lines': lines,
                        'origin': [0, 212], 'tracking': 6, 'line_height': 12, 'all_lines_same_left_margin': True,
                        'formatting_profile': formatting_profile,
                        'all_LF_bytes_second_in_native_ASCII_pairs': formatting_profile.endswith('v2'),
                        'all_printable_line_glyph_counts_even_before_LF': formatting_profile.endswith('v3')})
    for row in names['records']:
        field = TABLE + row['site_id'] * 4
        pointer = struct.unpack_from('<I', arm, field)[0]
        raw = row['english'].encode('ascii') + b'\0'
        assert arm[pointer - BASE:pointer - BASE + len(raw)] == raw
        entries[row['id']], owners[field], old_pointers[field] = raw, row['id'], pointer
    source_spans.extend(tuple(g) for g in site_stage['owned_source_groups'])
    for row in character_rows(clean):
        if 'index' not in row:
            continue
        offset, capacity, field = row['offset'], row['capacity'], row['pointer_field']
        raw = row['English'].encode('ascii') + b'\0'
        assert arm[offset:offset + capacity] == raw.ljust(capacity, b'\0')
        assert struct.unpack_from('<I', arm, field)[0] == BASE + offset
        entries[row['id']], owners[field], old_pointers[field] = raw, row['id'], BASE + offset
        source_spans.append((offset, offset + capacity))
    ranges = merge_ranges(source_spans)
    references = byte_pointer_references(arm, ranges)
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    excluded_patterns = []
    for field, relative in references.items():
        if field in owners:
            assert relative + BASE == old_pointers[field]
            continue
        # These byte patterns cross two executable ARM instructions, rather
        # than representing an address literal. Pin both complete instructions.
        assert field % 4 and field < 0x110000
        lo = field & ~3
        instructions = list(decoder.disasm(arm[lo:lo + 8], BASE + lo))
        assert len(instructions) == 2 and all(i.size == 4 for i in instructions)
        assert instructions[0].mnemonic.startswith('mov')
        assert instructions[1].mnemonic.startswith(('mov', 'add', 'b', 'str'))
        excluded_patterns.append({'byte_offset': field, 'apparent_relative_pointer': relative,
                                  'instruction_offset': lo, 'exact_instruction_hex': arm[lo:lo + 8].hex(),
                                  'instructions': [f'{i.mnemonic} {i.op_str}' for i in instructions]})
    assert len(owners) == 82 and set(owners) <= set(references)
    offsets, unused = pack(entries, ranges)
    result = bytearray(arm)
    for lo, hi in ranges:
        result[lo:hi] = bytes(hi - lo)
    for key, offset in offsets.items():
        result[offset:offset + len(entries[key])] = entries[key]
    for field, key in owners.items():
        struct.pack_into('<I', result, field, BASE + offsets[key])
    restored = bytearray(result)
    for lo, hi in ranges:
        restored[lo:hi] = arm[lo:hi]
    for field in owners:
        restored[field:field + 4] = arm[field:field + 4]
    assert restored == arm and len(result) == len(arm)
    assert validate(result) == validate(arm) and cache_plan(result) == cache_plan(arm)
    for field, key in owners.items():
        pointer = struct.unpack_from('<I', result, field)[0] - BASE
        assert result[pointer:pointer + len(entries[key])] == entries[key]
    return bytes(result), {'changed_records': list(entries), 'description_layouts': layouts,
                           'owned_ranges': ranges, 'owned_bytes': sum(hi - lo for lo, hi in ranges),
                           'complete_compiled_bytes': sum(map(len, entries.values())), 'unused_ranges': unused,
                           'pointer_bindings': [{'field': f, 'id': key, 'offset': offsets[key]} for f, key in owners.items()],
                           'all42_Characters_labels_and21_site_names_preserved_complete': True,
                           'all164_Event_Scenes_captions_and_bounds_unchanged': True,
                           'unaligned_cross_instruction_patterns_classified': excluded_patterns,
                           'all_unowned_bytes_section_extents_startup_heap_and_cache_exact': True,
                           'unsupported_image_slots_1_4_and_placeholders_unchanged': True,
                           'native_complete_paragraph_masks_and_relocated_name_consumers_required': True,
                           'status': 'experimental'}


def apply_release(arm, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-site-descriptions-v1' and sha(arm) == config['source_arm9_sha256']
    manuscript_path = Path(config['manuscript'])
    assert sha(manuscript_path.read_bytes()) == config['manuscript_sha256']
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    assert all(row['review']['formatting'] for row in manuscript['records'])
    result, report = transform(arm, manuscript, formatting_profile=config['formatting_profile'])
    assert sha(result) == config['target_arm9_sha256']
    return result, report
