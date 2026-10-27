"""Fit complete Refit help into three existing COMMON cache blocks.

Keep all unselected native message texts byte-exact. Do not grow the executable,
late-copy pool, allocator boundaries, cache buffers or native message count.
"""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.refit_help import PROFILE, compile_paragraph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.refit_help_release import IDS
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)

DIRECTORY = '99bbbb79a856466f52e89081c0bdf70189b3209bf7b041eae5b0f9f4d16a3d72'
DIRECTORY_V2 = '3d4d4ef8d37f87916522193b53bd4027d3d53ea11a3d1b5400b882e797c77555'


def transform(common, arm, manuscript):
    validate_natural_dialogue_batch(manuscript)
    ids = (1247, *IDS) if manuscript['format'] == 'dk4-refit-help-manuscript-v2' else IDS
    assert [r['message_id'] for r in manuscript['records']] == list(ids)
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    entries = common_message_entries(common, arm, clean=False)
    authored, layouts = {}, []
    for row in manuscript['records']:
        i = row['message_id']
        assert bytes.fromhex(row['clean_source_hex']) == source[i].text
        assert bytes.fromhex(row['canonical_source_hex']) == accepted[i].text
        compiled, lines = compile_paragraph(row['english'])
        authored[i] = compiled[:-1]
        layouts.append({'message_id': i, 'English': row['english'], 'lines': lines,
            'compiled_hex': compiled.hex(), 'profile': PROFILE})
    selected = [e for e in entries if 15 <= e.block <= 17]
    assert [e.message_id for e in selected] == list(range(1174, 1579))
    groups, body, group = [], bytearray(), []
    for entry in selected:
        text = authored.get(entry.message_id, entry.text) + b'\0'
        if len(body) + len(text) > 4096:
            groups.append((group, bytes(body)))
            body, group = bytearray(), []
        group.append((entry.message_id, len(body), text))
        body.extend(text)
    groups.append((group, bytes(body)))
    assert len(groups) == 3
    container = IlnkContainer.parse(common)
    old_blocks = list(container.blocks)
    target_arm = bytearray(arm)
    mappings, fields = [], []
    for block, (group, raw) in zip(range(15, 18), groups, strict=True):
        assert len(raw) <= 4096
        container.blocks[block] = raw
        field = DIRECTORY_OFFSET + block * 4
        struct.pack_into('<HH', target_arm, field, group[0][0], len(raw))
        fields.append((field, 4))
        for i, offset, text in group:
            field = TABLE_OFFSET + i * 2
            struct.pack_into('<H', target_arm, field, offset)
            fields.append((field, 2))
            mappings.append({'message_id': i, 'block': block, 'offset': offset, 'text_hex': text[:-1].hex()})
    result_arm, result_common = bytes(target_arm), container.to_bytes()
    directory = DIRECTORY_V2 if len(ids) == 31 else DIRECTORY
    assert sha(result_arm[DIRECTORY_OFFSET:TABLE_OFFSET]) == directory
    restored = bytearray(result_arm)
    for field, length in fields:
        restored[field:field + length] = arm[field:field + length]
    assert bytes(restored) == arm and len(result_arm) == len(arm)
    assert cache_plan(result_arm) == cache_plan(arm)
    assert all(container.blocks[i] == block for i, block in enumerate(old_blocks) if i not in (15, 16, 17))
    return result_common, result_arm, {'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
        'target_common_sha256': sha(result_common), 'target_arm9_sha256': sha(result_arm),
        'native_directory_sha256': directory, 'records': layouts, 'repacked_native_IDs': mappings,
        'block_groups': [{'block': b, 'first_id': g[0][0], 'last_id': g[-1][0], 'bytes': len(raw)}
            for b, (g, raw) in zip(range(15, 18), groups, strict=True)],
        'owned_ARM9_metadata_fields': fields,
        'all_unselected_native_message_text_bytes_preserved': True,
        'all38_other_COMMON_blocks_exact': True, 'all_executable_code_startup_pool_allocator_cache_fonts_and_sections_exact': True,
        'original4096_byte_cache_limit_and3668_native_IDs_preserved': True,
        'changed_records': [f'REFIT_HELP_{i}' for i in ids], 'experimental': True, 'full_goal_complete': False}


def apply_release(common, arm, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] in ('dk4-refit-help-repack-v1', 'dk4-refit-help-repack-v2')
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    for dependency, digest in config['dependencies'].items():
        assert sha(Path(dependency).read_bytes()) == digest
    target_common, target_arm, proof = transform(common, arm, json.loads(manuscript.read_text(encoding='utf-8')))
    assert sha(target_common) == config['target_common_sha256'] and sha(target_arm) == config['target_arm9_sha256']
    actual = common_message_entries(target_common, target_arm, clean=False)
    original = common_message_entries(common, arm, clean=False)
    replacements = {r['message_id']: bytes.fromhex(r['compiled_hex'])[:-1] for r in proof['records']}
    assert len(actual) == len(original) == 3668
    assert all(b.text == replacements.get(a.message_id, a.text) for a, b in zip(original, actual, strict=True))
    return target_common, target_arm, proof
