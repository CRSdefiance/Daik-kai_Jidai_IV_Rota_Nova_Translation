"""Translate only source-exact legacy promotional names after native save load."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_no_target import Assembly
from scripts.probe_common_display_name_hook import branch_link

SOURCE = '6e5ff558fa1913732350b4f9952a6d7f5d044fba4dd3beb5797a5640f80dfe85'
HOOK = 0x102AF0


def cstring(data, pointer):
    offset = pointer - BASE
    return data[offset:data.index(0, offset)]


def dictionary(source, clean):
    rows = []
    tables = [struct.unpack_from('<I', data, 0x102E44)[0] for data in (clean, source)]
    formats = [struct.unpack_from('<I', data, 0x102E4C)[0] for data in (clean, source)]
    for index in range(10):
        names = [cstring(data, struct.unpack_from('<I', data, table - BASE + index * 8)[0])
                 for data, table in zip((clean, source), tables)]
        pairs = [names]
        for fragment in range(4):
            templates = [cstring(data, struct.unpack_from('<I', data, table - BASE + fragment * 4)[0])
                         for data, table in zip((clean, source), formats)]
            pairs.append([template.replace(b'%s', name) for template, name in zip(templates, names)])
        for fragment, (japanese, english) in enumerate(pairs):
            assert 0 < len(japanese) < 32 and 0 < len(english) < 32
            assert english.decode('ascii') and any(value >= 128 for value in japanese)
            rows.append({'base_index': index + 188, 'fragment': fragment,
                         'Japanese': japanese.decode('cp932'), 'English': english.decode('ascii')})
    assert len(rows) == len({row['Japanese'] for row in rows}) == 50
    return rows


def helper(table):
    a = Assembly()
    a.emit(0xE92D5FFF)  # Save r0-r12/LR.
    a.emit(0xE10FC000)  # Preserve condition flags.
    a.emit(0xE92D1000)
    a.emit(0xE24DD004)  # Keep stack 8-byte aligned.
    a.emit(0xE2846022)
    a.emit(0xE3A0901E)
    a.mark('field')
    a.load(7, 'dictionary', table)
    a.emit(0xE3A08032)
    a.mark('entry')
    a.emit(0xE5970000)
    a.emit(0xE1A01006)
    a.emit(0xE3A02020)
    a.mark('compare')
    a.emit(0xE4D03001)
    a.emit(0xE4D1C001)
    a.emit(0xE153000C)
    a.branch('next_entry', 1)
    a.emit(0xE3530000)
    a.branch('match', 0)
    a.emit(0xE2522001)
    a.branch('compare', 1)
    a.mark('next_entry')
    a.emit(0xE2877008)
    a.emit(0xE2588001)
    a.branch('entry', 1)
    a.branch('next_field')
    a.mark('match')
    a.emit(0xE5970004)
    a.emit(0xE1A01006)
    a.mark('copy')
    a.emit(0xE4D02001)
    a.emit(0xE4C12001)
    a.emit(0xE3520000)
    a.branch('copy', 1)
    a.mark('next_field')
    a.emit(0xE2866020)
    a.emit(0xE2599001)
    a.branch('field', 1)
    a.emit(0xE28DD004)
    a.emit(0xE8BD1000)
    a.emit(0xE128F00C)
    a.emit(0xE8BD5FFF)
    a.emit(0xE2846022)  # Original overwritten ADD r6,r4,#0x22.
    a.emit(0xE12FFF1E)
    return a.finish()


def transform(source, clean):
    assert sha(source) == SOURCE
    assert source[0x102AD0:0x102B84] == clean[0x102AD0:0x102B84]
    assert struct.unpack_from('<I', source, HOOK)[0] == 0xE2846022
    cache_plan(source)
    rows = dictionary(source, clean)
    code = MainCodeFile(source, BASE)
    before = [bytes(section.data) for section in code.sections]
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    pointers = []
    for row in rows:
        pair = []
        for key, encoding in [('Japanese', 'cp932'), ('English', 'ascii')]:
            pair.append(POOL + len(packed))
            packed.extend(row[key].encode(encoding) + b'\0')
        pointers.append(pair)
    packed.extend(bytes(-len(packed) % 4))
    table = POOL + len(packed)
    for pair in pointers:
        packed.extend(struct.pack('<2I', *pair))
    entry = POOL + len(packed)
    packed.extend(helper(table))
    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    assert POOL + size <= STAGE and STAGE + size + 48 <= 0x023F4000
    packed.extend(wrapper(STAGE + len(packed), STAGE + size, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    changes = []
    for offset, value in [(HOOK, branch_link(BASE + HOOK, entry)),
                          (0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64)),
                          (0xE45DC, POOL + size)]:
        changes.append({'offset': offset, 'before': struct.unpack_from('<I', source, offset)[0], 'after': value})
        struct.pack_into('<I', code.sections[0].data, offset, value)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for change in changes:
        off = change['offset']
        restored[off:off + 4] = before[0][off:off + 4]
    off = code.codeSettingsOffs
    restored[off:off + 12] = before[0][off:off + 12]
    assert bytes(restored) == before[0]
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2))
    assert bytes(parsed.sections[3].data[:preserved]) == before[3][:-48]
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(saved),
                   'helper': entry, 'helper_bytes': len(helper(table)), 'dictionary': rows,
                   'changes': changes, 'inherited_pool_bytes_preserved': preserved,
                   'cache': cache_plan(saved), 'name_field_bytes': 32, 'name_field_count': 30,
                   'source_exact_matches_only_unknown_custom_names_preserved': True,
                   'selected_item_ids_inventory_stats_flags_and_rng_unchanged': True,
                   'changed_records': ['DK4_LEGACY_SAVED_PROMOTIONAL_NAMES']}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-legacy-saved-item-names-release-v1'
    for name, digest in config['verification_evidence_sha256'].items():
        assert sha(Path(name).read_bytes()) == digest
    saved, plan = transform(source, clean)
    assert sha(saved) == config['target_arm9_sha256']
    return saved, plan
