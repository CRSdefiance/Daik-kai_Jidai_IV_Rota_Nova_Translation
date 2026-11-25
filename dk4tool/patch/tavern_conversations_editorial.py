"""Source-locked31-entry Tavern prose layer with exact native provider roles."""

import re
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import tavern_coordinate_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.verify_village_wrap_v608 import read

IDS = tuple(range(820, 851))
OWNERSHIP = Path('work/analysis/tavern_coordinates_v766/owned_runtime_plan.json')
ARGUMENTS = {820: ['native_person_name', 'town_name', 'localized_force_profession'],
    821: ['native_person_name', 'town_name', 'localized_force_profession'],
    822: ['town_name'], 823: ['town_name'], 827: ['admiral_short_name'],
    **{n: ['item_name'] for n in (828, 830, 831, 832, 833, 846)},
    842: ['native_coordinate_text'],
    843: ['item_name', 'NS_distance_qualifier', 'NS_direction', 'EW_distance_qualifier', 'EW_direction'],
    844: ['item_name', 'distance_qualifier', 'direction'], 845: ['item_name', 'distance_qualifier', 'direction'],
    847: ['commodity_name'], 848: ['commodity_name'],
    849: ['town_name', 'commodity_name'], 850: ['town_name', 'commodity_name']}


def compile_text(row):
    n, text = row['message_id'], row['english'].removesuffix('{PAD}')
    if (n not in IDS or not text or len(text) >= 200 or text != ' '.join(text.split())
            or not text.isascii() or any(ord(c) < 32 or ord(c) >= 127 for c in text)
            or any(c in text for c in '{}')):
        raise ValueError('One ordinary ASCII paragraph required; no authored breaks or alignment')
    if text.count('%s') != len(ARGUMENTS.get(n, [])) or '%' in text.replace('%s', ''):
        raise ValueError('Preserve every reviewed native argument exactly once')
    if n == 842 and re.search(r'[NSEW] +[0-9]', text):
        raise ValueError('Coordinate compaction may affect only the native argument,not authored literal text')
    return b' ' + text.encode('ascii')


def runtime_transform(arm):
    assert sha(arm) == runtime.SOURCE
    evidence = read(OWNERSHIP)
    assert evidence['source_ARM9_sha256'] == runtime.SOURCE
    assert evidence['module_sha256'] == sha(Path(runtime.__file__).read_bytes())
    assert evidence['all57_prior_replacement_texts_verified_by_inventory']
    assert evidence['global_coordinate_formatter_source_bytes_unchanged']
    native = read('work/analysis/tavern_coordinates_v766/verification.json')
    assert native['owned_runtime_plan_sha256'] == sha(OWNERSHIP.read_bytes())
    assert native['all94_coordinate_pairs_intact'] and not native['native_bank_writes']
    expected = {p['address']: p for p in evidence['patches']}
    target, patches = bytearray(arm), []
    for at, blob in runtime.assemble().items():
        previous = arm[at - runtime.BASE:at - runtime.BASE + len(blob)]
        assert previous.hex() == expected[at]['source_hex'] and blob.hex() == expected[at]['target_hex']
        target[at - runtime.BASE:at - runtime.BASE + len(blob)] = blob
        patches.append(expected[at])
    target = bytes(target)
    old, new = [MainCodeFile(a, runtime.BASE).sections for a in (arm, target)]
    assert [len(s.data) for s in old] == [len(s.data) for s in new]
    assert all(bytes(a.data) == bytes(b.data) for a, b in zip(old[1:], new[1:], strict=True))
    assert cache_plan(arm) == cache_plan(target)
    assert sha(target) == evidence['target_ARM9_sha256']
    return target, {'source_ARM9_sha256': sha(arm), 'target_ARM9_sha256': sha(target), 'patches': patches,
        'no_section_pool_cache_startup_allocator_growth': True,
        'private_direction_distance_and_profession_resources_only': True}


def plan(common, arm, authored):
    assert tuple(sorted(authored)) == IDS
    before = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    selected = [e for e in before if 2 <= e.block <= 20]
    assert [e.message_id for e in selected] == list(range(164, 1977))
    opaque = {}
    for e in selected:
        tail = blocks[e.block][e.block_offset + len(e.text) + 1:e.copy_end]
        if set(tail) - {0, 32}:
            assert e.message_id in (1854, 1865) and e.message_id not in authored
            opaque[e.message_id] = blocks[e.block][e.block_offset:e.copy_end]
    assert set(opaque) == {1854, 1865}
    for k in range(2, 21):
        first = next(e for e in selected if e.block == k)
        assert set(blocks[k][:first.block_offset]) <= {0, 32}
    groups, group, body = [], [], bytearray()
    for entry in selected:
        text = opaque.get(entry.message_id, authored.get(entry.message_id, entry.text) + b'\0')
        if len(body) + len(text) > 4096:
            groups.append((group, bytes(body))); group, body = [], bytearray()
        group.append((entry.message_id, len(body), text)); body.extend(text)
    groups.append((group, bytes(body)))
    assert len(groups) == 19
    rebuilt, target, fields, mapping = list(blocks), bytearray(arm), [], []
    for block, (group, raw) in zip(range(2, 21), groups, strict=True):
        rebuilt[block] = raw
        at = DIRECTORY_OFFSET + block * 4
        struct.pack_into('<HH', target, at, group[0][0], len(raw)); fields.append((at, 4))
        for n, offset, text in group:
            at = TABLE_OFFSET + n * 2
            struct.pack_into('<H', target, at, offset); fields.append((at, 2))
            mapping.append({'id': n, 'block': block, 'offset': offset,
                            'text_hex': authored.get(n, before[n].text).hex(), 'complete_payload_hex': text.hex()})
    return IlnkContainer(rebuilt).to_bytes(), bytes(target), fields, mapping


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    clean, accepted = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(accepted.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    tables = [common_message_entries(r.read_file(path), r.read_file('/__arm9__.bin'), clean=(r is clean)) for r in (clean, accepted)]
    before, authored = common_message_entries(common, arm, clean=False), {}
    for row in manuscript['records']:
        n = row['message_id']
        assert tables[0][n].text.hex() == row['source_hex']
        assert tables[1][n].text.hex() == row['canonical_source_hex']
        assert before[n].text.hex() == row['current_text_hex']
        assert row['runtime_argument_contract'] == ARGUMENTS.get(n, [])
        authored[n] = compile_text(row)
        assert authored[n].count(b'%s') == tables[0][n].text.count(b'%s')
    patched, proof = runtime_transform(arm)
    common2, arm2, fields, mapping = plan(common, patched, authored)
    after = common_message_entries(common2, arm2, clean=False)
    assert all(b.text == authored.get(a.message_id, a.text) for a, b in zip(before, after, strict=True))
    old_blocks, new_blocks = [IlnkContainer.parse(c).blocks for c in (common, common2)]
    assert all(a == b for k, (a, b) in enumerate(zip(old_blocks, new_blocks, strict=True)) if k not in range(2, 21))
    for n in (1854, 1865):
        x, y = before[n], after[n]
        assert old_blocks[x.block][x.block_offset:x.copy_end] == new_blocks[y.block][y.block_offset:y.copy_end]
    restored = bytearray(arm2)
    for at, length in fields: restored[at:at + length] = patched[at:at + length]
    assert bytes(restored) == patched and cache_plan(arm2) == cache_plan(arm)
    return common2, arm2, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS], 'owned_runtime': proof,
        'metadata_fields': fields, 'complete1813_selection_map': mapping,
        'all3637_unselected_strings_and22_other_blocks_exact': True,
        'two_opaque_native_copy_spans_preserved_byte_exact': [1854, 1865],
        'experimental': True, 'actual_gameplay_pending': True}


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-tavern-conversations-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    for p, h in config['dependencies'].items(): assert sha(Path(p).read_bytes()) == h, p
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    c, a, proof = transform(common, arm, read(manuscript))
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    return c, a, proof
