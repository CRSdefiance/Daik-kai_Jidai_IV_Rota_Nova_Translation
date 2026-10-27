"""Source-locked full item/diplomacy prose and no-growth runtime integration."""

import struct
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import item_diplomacy_runtime as runtime
from dk4tool.patch import tavern_schemes_editorial as previous
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.prepare_item_common_v788 import repack
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_village_wrap_v608 import read

ROOT = Path('work/analysis/item_diplomacy_integration_v788')
IDS = tuple(range(1070, 1146))
DIRECTORY = 'c58544bb0f8640c763007ff9a8abdc7e89723852602192ca990683761edf6afb'
NOMINAL = 'native_diplomatic_type_localized_as_nominal_phrase'
ARGUMENTS = {
    **{n: ['native_gold_coin_amount_without_unit'] for n in (1072, 1073, 1083, 1086, 1095)},
    **{n: [NOMINAL] for n in range(1098, 1103)},
    **{n: ['partner_faction_name', 'opponent_faction_name'] for n in range(1108, 1113)},
    **{n: ['recipient_faction_name', NOMINAL] for n in range(1113, 1117)},
    **{n: ['target_faction_name'] for n in range(1138, 1146)}}
compile_text = FunctionType(previous.compile_text.__code__, {**previous.__dict__, 'IDS': IDS, 'ARGUMENTS': ARGUMENTS})


def current_entries(common, arm):
    """Explicit versioned reader; the frozen shared parser is never modified."""
    assert sha(arm[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET]) == DIRECTORY
    return local_entries(DIRECTORY)(common, arm, clean=False)


def runtime_transform(arm):
    assert sha(arm) == runtime.SOURCE
    target = bytearray(arm)
    selector = read('work/analysis/item_diplomacy_runtime_v785/runtime_plan.json')
    names = read('work/analysis/item_diplomacy_context_v786/nominal_provider_research.json')
    width = read('work/analysis/scheme_name_width_v787/native_width_verification.json')
    assert runtime.code() == {r['address']: bytes.fromhex(r['target_hex']) for r in selector['patches']}
    assert len(selector['patches']) == 6 and len(names['patches']) == 11
    for proof, expected in ((selector, selector['research_ARM9_sha256']), (names, names['target_research_ARM9_sha256'])):
        for row in proof['patches']:
            at = row['address']-0x02000000
            before, after = bytes.fromhex(row['source_hex']), bytes.fromhex(row['target_hex'])
            assert len(before) == len(after) and bytes(target[at:at+len(before)]) == before
            target[at:at+len(after)] = after
        assert sha(target) == expected
    assert struct.unpack_from('<I', target, 0x9145C)[0] == 0xE3A0000A
    struct.pack_into('<I', target, 0x9145C, 0xE3A00018)
    assert width['reported_name_width_cells'] == 24 and width['paired_blank_terminal_cell_reserved'] == 1
    assert sha(target) == width['target_ARM9_sha256']
    assert cache_plan(bytes(target)) == cache_plan(arm)
    return bytes(target)


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    draft_path = Path(manuscript['reviewed_research_manuscript'])
    assert sha(draft_path.read_bytes()) == manuscript['reviewed_research_manuscript_sha256']
    draft = read(draft_path)
    for row, reviewed in zip(manuscript['records'], draft['records'], strict=True):
        assert row['message_id'] == reviewed['message_id'] and row['english'] == reviewed['english']
        assert row['source_meaning'] == reviewed['source_meaning']
    layout = read(ROOT/'production_layout/verification.json')
    assert layout['native_layouts'] == 2774 and not layout['findings']
    assert len(layout['all76_complete_native_font_planes_exact_to_visually_reviewed_images']) == 76
    assert layout['manuscript_sha256'] == sha(draft_path.read_bytes())
    consumer = read(ROOT/'consumer_routing.json')
    assert len(consumer['all1260_direct_Guild_wrapper_bindings']) == 1260
    assert len(consumer['ten_real_role_and_voice_provider_bindings']) == 10
    assert consumer['exact_argument_count_order_and_template_binding']
    copies = [read(ROOT/f'native_copies/native_copies_block_{n:02d}.json') for n in range(41)]
    assert {(r['message_id'], r['cold_cache']) for p in copies for r in p['cases']} == {(n, cold) for n in range(3668) for cold in (False, True)}
    assert all(r['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for p in copies for r in p['cases'])
    clean, canonical = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    path = '/COMMON/MESFILE.DK4'
    source = parser.common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = parser.common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    before = parser.common_message_entries(common, arm, clean=False)
    authored = {}
    for row in manuscript['records']:
        n = row['message_id']
        assert source[n].text.hex() == row['source_hex'] and accepted[n].text.hex() == row['canonical_source_hex']
        assert before[n].text.hex() == row['current_text_hex']
        assert source[n].text.count(b'%s') == len(ARGUMENTS.get(n, []))
        authored[n] = compile_text(row)
    patched = runtime_transform(arm)
    entries, blocks, first, last, selected, opaque, groups, attempts = repack(common, patched, authored)
    assert (first, last) == (14, 40)
    target, rebuilt, mapping, fields = bytearray(patched), list(blocks), [], []
    for block, (group, body) in zip(range(first, last+1), groups, strict=True):
        rebuilt[block] = body
        at = parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH', target, at, group[0][0], len(body))
        fields.append((at, 4))
        for n, offset, payload in group:
            at = parser.TABLE_OFFSET+n*2
            struct.pack_into('<H', target, at, offset)
            fields.append((at, 2))
            mapping.append({'id': n, 'block': block, 'offset': offset, 'text_hex': authored.get(n, before[n].text).hex(),
                            'complete_payload_hex': payload.hex()})
    c, a = IlnkContainer(rebuilt).to_bytes(), bytes(target)
    after = current_entries(c, a)
    assert all(y.text == authored.get(x.message_id, x.text) for x, y in zip(before, after, strict=True))
    assert all(blocks[b] == rebuilt[b] for b in range(14))
    for n, payload in opaque.items():
        e = after[n]
        assert rebuilt[e.block][e.block_offset:e.copy_end] == payload
    restored = bytearray(a)
    for at, size in fields: restored[at:at+size] = patched[at:at+size]
    assert bytes(restored) == patched and cache_plan(a) == cache_plan(arm)
    code = [MainCodeFile(v, 0x02000000) for v in (arm, a)]
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in code[0].sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in code[1].sections]
    assert bytes(code[1].save()) == a
    assert all(p['COMMON_sha256'] == sha(c) and p['ARM9_sha256'] == sha(a) for p in copies)
    return c, a, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS],
        'metadata_fields': fields, 'complete_selection_map': mapping,
        'all3592_other_strings_14_other_blocks_and_opaque_spans_preserved': True,
        'original_shop676_677_preserved': True, 'private_selector_nominal_names_and24_cell_width': True,
        'sections_BSS_cache_and_staged_payload_unchanged': True,
        'frozen_shared_parser_and_earlier_profiles_preserved': True,
        'experimental': True, 'actual_gameplay_and_full_eligibility_pending': True}


def apply_release(common, arm, path):
    cfg = read(path)
    assert cfg['format'] == 'dk4-item-diplomacy-editorial-v1'
    assert sha(common) == cfg['source_common_sha256'] and sha(arm) == cfg['source_arm9_sha256']
    for name, expected in cfg['dependencies'].items():
        assert sha(Path(name).read_bytes()) == expected, name
    manuscript = Path(cfg['manuscript'])
    assert sha(manuscript.read_bytes()) == cfg['manuscript_sha256']
    c, a, proof = transform(common, arm, read(manuscript))
    assert sha(c) == cfg['target_common_sha256'] and sha(a) == cfg['target_arm9_sha256']
    return c, a, proof
