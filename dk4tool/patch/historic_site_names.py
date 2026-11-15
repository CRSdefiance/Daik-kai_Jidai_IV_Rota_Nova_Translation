"""Complete source-owned historic-site names in the existing cached main pool."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

TABLE = 0x11BC1C


def transform(arm, rows):
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert len(rows) == 21 and [r['site_id'] for r in rows] == list(range(21))
    assert arm[TABLE:TABLE + 84] == clean[TABLE:TABLE + 84]
    assert arm[0x87444:0x87484] == clean[0x87444:0x87484]
    assert arm[0xCD56C:0xCD57C] == clean[0xCD56C:0xCD57C]
    code = MainCodeFile(arm, BASE)
    before = [bytes(s.data) for s in code.sections]
    assert code.sections[3].ramAddress == STAGE and cache_plan(arm)
    packed = bytearray(before[3][:-48])
    translated = []
    for row in rows:
        field = TABLE + row['site_id'] * 4
        offset = struct.unpack_from('<I', clean, field)[0] - BASE
        source = clean[offset:].split(b'\0')[0]
        assert field == row['pointer_field'] and offset == row['source_offset']
        assert source.hex() == row['source_hex'] and source.decode('cp932') == row['japanese']
        assert arm[offset:offset + len(source) + 1] == source + b'\0'
        assert row['all_aligned_native_pointer_aliases'] == [field]
        assert all(row['review'][k] for k in ('source', 'context', 'localization', 'naturalness'))
        text = row['english'].encode('ascii')
        assert text and b'\0' not in text and len(text) * 6 <= 192
        packed.extend(bytes(-len(packed) % 4))
        pointer = POOL + len(packed)
        packed.extend(text + b'\0')
        struct.pack_into('<I', code.sections[0].data, field, pointer)
        translated.append({'id': row['id'], 'site_id': row['site_id'], 'pointer_field': field,
                           'source_offset': offset, 'Japanese': row['japanese'],
                           'English': row['english'], 'runtime_pointer': pointer})
    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    assert POOL + size < STAGE and STAGE + size + 48 < 0x023F4000
    packed.extend(wrapper(STAGE + len(packed), STAGE + size, size, arm))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    struct.pack_into('<I', code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for field in [*(r['pointer_field'] for r in rows), 0x8E4, 0xE45DC]:
        restored[field:field + 4] = before[0][field:field + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    assert restored == before[0]
    assert all(bytes(parsed.sections[n].data) == before[n] for n in (1, 2, 4))
    assert bytes(parsed.sections[3].data[:len(before[3]) - 48]) == before[3][:-48]
    return saved, {'changed_records': [r['id'] for r in rows], 'translated_names': translated,
                   'source_arm9_sha256': sha(arm), 'target_arm9_sha256': sha(saved),
                   'inherited_pool_prefix_bytes_exact': len(before[3]) - 48,
                   'new_pool_bytes': size - len(before[3]) + 48,
                   'remaining_before_stage': STAGE - POOL - size, 'cache': cache_plan(saved),
                   'all_original_Japanese_slots_and_all_original_getter_instructions_exact': True,
                   'only21_metadata_pointers_startup_copy_extent_heap_low_and_new_owned_payload_change': True,
                   'native_complete_list_map_and_gameplay_consumer_checks_required': True,
                   'status': 'experimental'}


def apply_release(arm, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] in ('dk4-historic-site-names-v1', 'dk4-historic-site-names-v2')
    assert config['translation_policy'] == 'natural-dialogue-v2' and config['target_locale'] == 'en-US'
    assert sha(arm) == config['source_arm9_sha256']
    result, report = (fixed_transform(arm, config['records']) if config['format'].endswith('v2')
                      else transform(arm, config['records']))
    assert sha(result) == config['target_arm9_sha256']
    return result, report


def fixed_transform(arm, rows):
    """Pack complete C strings only inside the 21 original owned name spans."""
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert len(rows) == 21 and [r['site_id'] for r in rows] == list(range(21))
    assert arm[TABLE:TABLE + 84] == clean[TABLE:TABLE + 84]
    spans = []
    for row in rows:
        field, offset = row['pointer_field'], row['source_offset']
        assert field == TABLE + row['site_id'] * 4
        assert struct.unpack_from('<I', clean, field)[0] == BASE + offset
        source = bytes.fromhex(row['source_hex'])
        assert source.decode('cp932') == row['japanese']
        capacity = (len(source) + 4) // 4 * 4
        expected = (source + b'\0').ljust(capacity, b'\0')
        assert capacity == row['original_aligned_capacity_candidate']
        assert clean[offset:offset + capacity] == arm[offset:offset + capacity] == expected
        assert all(row['review'][k] for k in ('source', 'context', 'localization', 'naturalness'))
        assert row['all_aligned_native_pointer_aliases'] == [field]
        spans.append((offset, offset + capacity))
    groups = []
    for lo, hi in sorted(spans):
        if groups and lo == groups[-1][1]:
            groups[-1][1] = hi
        else:
            assert not groups or lo > groups[-1][1]
            groups.append([lo, hi])
    # Any literal into a retired source allocation must be one of the owned
    # table fields and point to an original string start, never an interior byte.
    owners = {row['pointer_field']: BASE + row['source_offset'] for row in rows}
    for field in range(0, len(arm) - 3, 4):
        pointer = struct.unpack_from('<I', arm, field)[0]
        if any(BASE + lo <= pointer < BASE + hi for lo, hi in groups):
            assert owners.get(field) == pointer, (field, pointer)
    pending = sorted(rows, key=lambda r: (-len(r['english']), r['site_id']))
    cursors, targets = [lo for lo, _ in groups], {}
    for row in pending:
        raw = row['english'].encode('ascii') + b'\0'
        assert len(raw) > 1 and raw.count(b'\0') == 1 and (len(raw) - 1) * 6 <= 192
        eligible = [(hi - cursors[n], n) for n, (_, hi) in enumerate(groups)
                    if hi - cursors[n] >= len(raw)]
        assert eligible, row['id']
        _, n = min(eligible)
        targets[row['site_id']] = (cursors[n], raw)
        cursors[n] += len(raw)
    result = bytearray(arm)
    for lo, hi in groups:
        result[lo:hi] = bytes(hi - lo)
    translated = []
    for row in rows:
        offset, raw = targets[row['site_id']]
        result[offset:offset + len(raw)] = raw
        struct.pack_into('<I', result, row['pointer_field'], BASE + offset)
        translated.append({'id': row['id'], 'site_id': row['site_id'],
                           'pointer_field': row['pointer_field'], 'source_offset': row['source_offset'],
                           'Japanese': row['japanese'], 'English': row['english'],
                           'runtime_pointer': BASE + offset, 'target_offset': offset})
    restored = bytearray(result)
    for lo, hi in groups:
        restored[lo:hi] = arm[lo:hi]
    restored[TABLE:TABLE + 84] = arm[TABLE:TABLE + 84]
    assert restored == arm and len(result) == len(arm)
    source_code, target_code = [MainCodeFile(blob, BASE) for blob in (arm, bytes(result))]
    assert all(bytes(a.data) == bytes(b.data) for a, b in zip(source_code.sections[1:], target_code.sections[1:], strict=True))
    assert cache_plan(arm) == cache_plan(result)
    return bytes(result), {'changed_records': [r['id'] for r in rows], 'translated_names': translated,
                           'owned_source_groups': groups, 'owned_bytes': sum(hi - lo for lo, hi in groups),
                           'complete_English_bytes': sum(len(raw) for _, raw in targets.values()),
                           'all_unowned_bytes_and_all_section_extents_exact': True,
                           'all_startup_copy_heap_cache_and_original_getter_instructions_exact': True,
                           'no_pool_growth': True, 'native_unaligned_C_string_and_complete_display_checks_required': True,
                           'status': 'experimental'}
