"""Reviewed Missionary confirmation/announcement wording in existing COMMON slots."""

import json
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from dk4tool.script.common_native_repack import repack_native_records

IDS = (660, 662, 663, 664, 665, 668, 671)
CONFIRM_TABLE = 0x021184C0
ANNOUNCE_TABLE = 0x021184A0


def transform(common, arm, manuscript):
    if manuscript.get('translation_policy') != 'natural-dialogue-v2':
        raise ValueError('Giveaway editorial work requires natural-dialogue-v2')
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    before = common_message_entries(common, arm, clean=False)
    original = IlnkContainer.parse(common)
    authored, prefixes, layouts = {}, {}, []
    for row in manuscript['records']:
        i = row['message_id']
        assert bytes.fromhex(row['source_hex']) == source[i].text
        assert bytes.fromhex(row['canonical_source_hex']) == accepted[i].text
        assert bytes.fromhex(row['current_text_hex']) == before[i].text
        assert '%' not in source[i].text.decode('cp932')
        raw, lines = compile_paragraph(row['english'])
        authored[i] = raw
        owner = before[i].block, before[i].record_index
        first = next(e for e in before if (e.block, e.record_index) == owner)
        prefixes[owner] = original.blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
        layouts.append({'message_id': i, 'paragraph': row['english'].removesuffix('{PAD}'),
                        'lines': lines, 'encoded_hex': raw.hex()})
    result = repack_native_records(common, arm, authored, prefixes, generated_linebreaks=True)
    after = result.entries
    assert len(common) == len(result.common) and len(arm) == len(result.arm9)
    assert arm[DIRECTORY_OFFSET:TABLE_OFFSET] == result.arm9[DIRECTORY_OFFSET:TABLE_OFFSET]
    allowed = {n for offset in result.changed_offsets for n in (offset, offset + 1)}
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(arm, result.arm9, strict=True)))
    for a, b in zip(before, after, strict=True):
        assert (a.message_id, a.block, a.record_index) == (b.message_id, b.block, b.record_index)
        assert b.text.rstrip(b' ') == authored.get(a.message_id, a.text).rstrip(b' ')
    target = IlnkContainer.parse(result.common)
    assert all(a == b for i, (a, b) in enumerate(zip(original.blocks, target.blocks, strict=True)) if i != 8)
    return result.common, result.arm9, {
        'records': layouts, 'changed_records': [f'COMMON_MESSAGE_{i}' for i in IDS],
        'changed_native_offset_fields': sorted(result.changed_offsets),
        'native3668_IDs_NUL_owners_all_cache_sizes_preserved': True,
        'all40_other_blocks_and_executable_startup_fonts_unchanged': True,
        'prior_seven_revised_business_paragraphs_preserved': True,
        'all_other_visible_texts_preserved_except_terminal_padding_donors': True,
        'generated_layout_no_authored_breaks': True, 'experimental': True,
    }


def apply_release(common, arm, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-giveaway-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest
    common, arm, report = transform(common, arm, json.loads(manuscript.read_text(encoding='utf-8')))
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common, arm, report
