"""Source-locked retail/business prose, compiled for the existing COMMON painter.

No executable code, bitmap dimensions or cache allocations are changed.
"""

from dataclasses import replace
from pathlib import Path

from dk4tool.dialogue.layout import format_markup
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from dk4tool.script.common_native_repack import repack_native_records
from scripts.verify_village_wrap_v608 import read

IDS = (657, 658, 682, 683, 684, 686, 687)
PROFILE = replace(get_dialogue_profile('shared'), name='COMMON-portrait-generated-guarded-lines-v1',
                  window_width_px=210, guard_linebreaks=False, balanced_wrapping=True,
                  pair_phase_safe_breaks=True)


def compile_paragraph(english):
    text = english.removesuffix('{PAD}')
    if (not text or not text.isascii() or text != ' '.join(text.split())
            or any(c in text for c in '{}%')):
        raise ValueError('Retail/business prose requires one ASCII paragraph without commands or substitutions')
    # This consumer has the V255 native literal-I/F guard. It is not the
    # progressive story macro parser, so do not encode English I as a pronoun.
    if any(macro in text for macro in ('FI', 'FA', 'FO', 'FU', 'IC')):
        raise ValueError('A source command-like pair needs explicit native expansion review')
    weak = {'a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with'}
    candidates = []
    for width in range(PROFILE.window_width_px, 143, -6):
        candidate = format_markup(text, replace(PROFILE, window_width_px=width)).split('{LB}')
        if len(candidate) > 4:
            continue
        if any(s.split()[-1].strip('.,!?;:').lower() in weak for s in candidate[:-1]):
            continue
        if len(candidate) > 1 and len(candidate[-1]) <= 8:
            continue
        candidates.append(candidate)
    if not candidates:
        raise ValueError('No complete readable four-row layout without dangling wrap words')
    lines = candidates[0]
    if (' '.join(lines) != text or not 1 <= len(lines) <= 4
            or any(len(s) > (35 if i == len(lines) - 1 else 34) for i, s in enumerate(lines))):
        raise ValueError('Complete paragraph exceeds the verified four-row portrait surface')
    result = bytearray(b'  ')
    phase = 0  # Two generated initial guard bytes keep the initial phase even.
    for index, line in enumerate(lines):
        result.extend(line.encode('ascii'))
        phase = (phase + len(line)) & 1
        if index < len(lines) - 1:
            if phase:
                result.extend(b' ')
                phase = 0
            result.extend(b'\n  ')
    return bytes(result), lines


def transform(common, arm, manuscript):
    if manuscript.get('translation_policy') != 'natural-dialogue-v2':
        raise ValueError('New editorial work requires natural-dialogue-v2')
    validate_natural_dialogue_batch(manuscript)
    if tuple(r['message_id'] for r in manuscript['records']) != IDS:
        raise ValueError('Retail/business release must contain its complete reviewed family')
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    before = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
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
        prefixes[owner] = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
        layouts.append({'message_id': i, 'paragraph': row['english'].removesuffix('{PAD}'),
                        'lines': lines, 'encoded_hex': raw.hex()})
    result = repack_native_records(common, arm, authored, prefixes, generated_linebreaks=True)
    assert len(common) == len(result.common) and len(arm) == len(result.arm9)
    assert arm[DIRECTORY_OFFSET:TABLE_OFFSET] == result.arm9[DIRECTORY_OFFSET:TABLE_OFFSET]
    allowed = {n for offset in result.changed_offsets for n in (offset, offset + 1)}
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(arm, result.arm9, strict=True)))
    for a, b in zip(before, result.entries, strict=True):
        assert (a.message_id, a.block, a.record_index) == (b.message_id, b.block, b.record_index)
        if a.message_id in authored:
            assert b.text.rstrip(b' ') == authored[a.message_id]
        else:
            assert b.text.rstrip(b' ') == a.text.rstrip(b' ')
    original_blocks = IlnkContainer.parse(common).blocks
    new_blocks = IlnkContainer.parse(result.common).blocks
    assert all(a == b for i, (a, b) in enumerate(zip(original_blocks, new_blocks, strict=True)) if i != 8)
    return result.common, result.arm9, {
        'records': layouts, 'changed_records': [f'COMMON_MESSAGE_{i}' for i in IDS],
        'changed_native_offset_fields': sorted(result.changed_offsets),
        'all3668_native_IDs_and_NUL_owner_identities_preserved': True,
        'all_unselected_meaning_and_control_bytes_preserved_except_terminal_padding_donors': True,
        'all40_other_blocks_and_all_native_cache_allocations_exact': True,
        'all_ARM9_code_fonts_startup_pools_and_sections_preserved': True,
        'generated_layout_only_no_authored_breaks': True, 'experimental': True,
    }


def apply_release(common, arm, config_path):
    config = read(config_path)
    assert config['format'] == 'dk4-shop-business-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest
    common, arm, report = transform(common, arm, read(manuscript))
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common, arm, report
