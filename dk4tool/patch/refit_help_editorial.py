"""Late source-locked Refit prose; preserve prior frozen release stages."""

import struct
from pathlib import Path
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile

from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.levelup_stat_format import current_entries as previous_entries
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.prepare_item_common_v788 import repack
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_village_wrap_v608 import read

IDS = (*range(1247, 1256), *range(1268, 1290))
SOURCE_COMMON = 'faea4ae2af84a02c1bf6f26f1815cef5ef228f29cb9342cea2a3e236a10bea3a'
SOURCE_ARM = 'c27c2b01ea689ef6cc15bffabb30138aaadecb1d8a14e8a2d85a0f4c09d643eb'
CONFIG = 'translations/refit_help_editorial_release_v1.json'


def plan(common, arm, manuscript):
    assert sha(common) == SOURCE_COMMON and sha(arm) == SOURCE_ARM
    validate_natural_dialogue_batch(manuscript)
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    assert manuscript['target_locale'] == 'en-US'
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    assert manuscript['current_common_sha256'] == SOURCE_COMMON
    assert manuscript['current_arm9_sha256'] == SOURCE_ARM
    clean, canonical = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    assert sha(Path('work/clean.nds').read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    jp = parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    accepted = parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    before = previous_entries(common, arm)
    authored, layouts = {}, []
    for row in manuscript['records']:
        i = row['message_id']
        assert row['clean_source_hex'] == jp[i].text.hex()
        assert row['canonical_source_hex'] == accepted[i].text.hex()
        assert row['current_text_hex'] == before[i].text.hex()
        compiled, lines = compile_paragraph(row['english'])
        assert len(lines[-1].split()) > 1
        authored[i] = compiled[:-1]
        layouts.append({'message_id': i, 'English': row['english'], 'lines': lines, 'compiled_hex': compiled.hex()})
    # Reuse the reviewed complete-selection/opaque-tail planner with the exact
    # current parser. This does not modify its globals or the generic parser.
    scoped = SimpleNamespace(common_message_entries=lambda c, a, clean=False: previous_entries(c, a))
    pack = FunctionType(repack.__code__, {**repack.__globals__, 'parser': scoped})
    before, blocks, first, last, selected, opaque, groups, attempts = pack(common, arm, authored)
    target, rebuilt, fields = bytearray(arm), list(blocks), []
    for block, (group, body) in zip(range(first, last + 1), groups, strict=True):
        assert len(body) <= 4096
        rebuilt[block] = body
        at = parser.DIRECTORY_OFFSET + block * 4
        struct.pack_into('<HH', target, at, group[0][0], len(body))
        fields.append((at, 4))
        for n, offset, payload in group:
            at = parser.TABLE_OFFSET + n * 2
            struct.pack_into('<H', target, at, offset)
            fields.append((at, 2))
    c, a = IlnkContainer(rebuilt).to_bytes(), bytes(target)
    directory = sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    after = local_entries(directory)(c, a, clean=False)
    assert len(before) == len(after) == 3668
    assert all(y.text == authored.get(x.message_id, x.text) for x, y in zip(before, after, strict=True))
    assert all(blocks[n] == rebuilt[n] for n in range(41) if not first <= n <= last)
    for n, payload in opaque.items():
        e = after[n]
        assert rebuilt[e.block][e.block_offset:e.copy_end] == payload
    assert all(before[n].text == after[n].text for n in (676, 677))
    restored = bytearray(a)
    for at, size in fields:
        restored[at:at + size] = arm[at:at + size]
    assert bytes(restored) == arm and cache_plan(a) == cache_plan(arm)
    old, new = [MainCodeFile(v, 0x02000000) for v in (arm, a)]
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in old.sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in new.sections]
    assert old.sections[3].data == new.sections[3].data and len(new.sections[3].data) - 48 == 123040
    changed = [i for i in IDS if before[i].text != after[i].text]
    assert len(changed) == 18
    return c, a, {
        'records': layouts, 'changed_records': [f'REFIT_HELP_{i}' for i in changed],
        'metadata_fields': fields, 'directory_sha256': directory,
        'repacked_block_range': [first, last], 'packing_attempts': attempts,
        'repacked_native_IDs': [e.message_id for e in selected], 'opaque_payload_IDs': sorted(opaque),
        'all3650_other_text_strings_exact': True, 'all31_reviewed_help_paragraphs_present': True,
        'unselected_blocks_and_opaque_payloads_exact': True,
        'all_code_fonts_layouts_sections_BSS_cache_and_staged123040_bytes_unchanged': True,
        'user676_677_formatting_templates_preserved': True,
        'experimental': True, 'full_goal_complete': False}


def current_entries(common, arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return local_entries(config['directory_sha256'])(common, arm, clean=False)


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-refit-help-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name, digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    c, a, proof = plan(common, arm, read(manuscript))
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    assert proof['directory_sha256'] == config['directory_sha256']
    assert read(config['native_copy_proof'])['target_common_sha256'] == sha(c)
    font = read(config['native_font_proof'])
    assert font['manuscript_sha256'] == config['manuscript_sha256'] and not font['visual_review_pending']
    assert [(r['message_id'], r['compiled_hex']) for r in font['records']] == [(r['message_id'], r['compiled_hex']) for r in proof['records']]
    return c, a, proof
