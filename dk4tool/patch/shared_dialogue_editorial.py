"""Source-locked shared prose and exact existing-bank dispatcher integration."""

import struct
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import scheme_followup_editorial as previous
from dk4tool.patch import shared_dialogue_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.verify_village_wrap_v608 import read

ROOT = Path('work/analysis/shared_integration_v782')
IDS = tuple(range(1020, 1070))
ARGUMENTS = {**{n: ['native_village_coordinate_text'] for n in (1028, 1029)},
             **{n: ['native_town_name'] for n in range(1030, 1035)},
             **{n: ['required_crew_shortfall'] for n in range(1035, 1042)},
             **{n: ['remaining_crew_capacity'] for n in range(1042, 1049)}}
compile_text = FunctionType(previous.compile_text.__code__, {**previous.compile_text.__globals__, 'IDS': IDS, 'ARGUMENTS': ARGUMENTS})
runtime_transform = FunctionType(previous.runtime_transform.__code__, {**previous.__dict__, 'ROOT': ROOT, 'runtime': runtime})


def plan(common, arm, authored):
    assert tuple(sorted(authored)) == IDS
    before = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    selected = [e for e in before if 13 <= e.block <= 40]
    assert [e.message_id for e in selected] == list(range(1007, 3668))
    opaque = {}
    for e in selected:
        tail = blocks[e.block][e.block_offset+len(e.text)+1:e.copy_end]
        if set(tail)-{0, 32}:
            assert e.message_id in (1854, 1865) and e.message_id not in authored
            opaque[e.message_id] = blocks[e.block][e.block_offset:e.copy_end]
    assert set(opaque) == {1854, 1865}
    for block in range(13, 41):
        first = next(e for e in selected if e.block == block)
        assert set(blocks[block][:first.block_offset]) <= {0, 32}
    groups, group, body = [], [], bytearray()
    for e in selected:
        payload = opaque.get(e.message_id, authored.get(e.message_id, e.text)+b'\0')
        if len(body)+len(payload) > 4096:
            groups.append((group, bytes(body)))
            group, body = [], bytearray()
        group.append((e.message_id, len(body), payload))
        body.extend(payload)
    groups.append((group, bytes(body)))
    assert len(groups) == 28
    rebuilt, target, fields, mapping = list(blocks), bytearray(arm), [], []
    for block, (group, body) in zip(range(13, 41), groups, strict=True):
        assert len(body) <= 4096
        rebuilt[block] = body
        at = DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH', target, at, group[0][0], len(body))
        fields.append((at, 4))
        for n, offset, payload in group:
            at = TABLE_OFFSET+n*2
            struct.pack_into('<H', target, at, offset)
            fields.append((at, 2))
            mapping.append({'id': n, 'block': block, 'offset': offset,
                            'text_hex': authored.get(n, before[n].text).hex(), 'complete_payload_hex': payload.hex()})
    return IlnkContainer(rebuilt).to_bytes(), bytes(target), fields, mapping


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    assert sha(arm) == runtime.SOURCE
    filters, consumer = [read(manuscript[k]) for k in ('caller_filter_proof', 'consumer_routing_proof')]
    assert len(filters['all150_complete_original_village_selector_cases']) == 150
    assert len(filters['warning_threshold_branches']) == 616 and len(filters['crew_shortfall_capacity_and_funds_conditions']) == 204
    assert consumer['source_callers_select_nonnull_portrait_core_for_these_families']
    assert len(consumer['all114_immutable_city_role13_mappings']) == 114
    layouts = read(manuscript['production_layout_proof'])
    assert layouts['native_layouts'] == 857 and not layouts['findings']
    assert len(layouts['all83_complete_native_font_planes_exact_to_visually_reviewed_images']) == 83
    reviewed = Path(manuscript['reviewed_research_manuscript'])
    assert sha(reviewed.read_bytes()) == manuscript['reviewed_research_manuscript_sha256'] == layouts['manuscript_sha256']
    research = read(reviewed)
    for row, draft in zip(manuscript['records'], research['records'], strict=True):
        assert row['english'] == draft['english'] and row['message_id'] == draft['message_id']
    clean, canonical = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    path = '/COMMON/MESFILE.DK4'
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    before = common_message_entries(common, arm, clean=False)
    authored = {}
    for row in manuscript['records']:
        n = row['message_id']
        assert source[n].text.hex() == row['source_hex'] and accepted[n].text.hex() == row['canonical_source_hex']
        assert before[n].text.hex() == row['current_text_hex']
        assert source[n].text.count(b'%s') == len(ARGUMENTS.get(n, []))
        authored[n] = compile_text(row)
    patched, proof = runtime_transform(arm)
    c, a, fields, mapping = plan(common, patched, authored)
    after = common_message_entries(c, a, clean=False)
    assert all(y.text == authored.get(x.message_id, x.text) for x, y in zip(before, after, strict=True))
    old, new = [IlnkContainer.parse(v).blocks for v in (common, c)]
    assert all(x == y for i, (x, y) in enumerate(zip(old, new, strict=True)) if i < 13)
    for n in (1854, 1865):
        x, y = before[n], after[n]
        assert old[x.block][x.block_offset:x.copy_end] == new[y.block][y.block_offset:y.copy_end]
    restored = bytearray(a)
    for at, size in fields:
        restored[at:at+size] = patched[at:at+size]
    assert bytes(restored) == patched and cache_plan(a) == cache_plan(arm)
    return c, a, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS], 'private_runtime': proof,
                  'metadata_fields': fields, 'complete2661_selection_map': mapping,
                  'all3618_other_strings_and13_other_blocks_exact': True,
                  'opaque1854_1865_complete_native_payloads_exact': True,
                  'experimental': True, 'actual_gameplay_pending': True}


def apply_release(common, arm, path):
    cfg = read(path)
    assert cfg['format'] == 'dk4-shared-dialogue-editorial-v1'
    assert sha(common) == cfg['source_common_sha256'] and sha(arm) == cfg['source_arm9_sha256']
    for p, h in cfg['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    manuscript = Path(cfg['manuscript'])
    assert sha(manuscript.read_bytes()) == cfg['manuscript_sha256']
    c, a, proof = transform(common, arm, read(manuscript))
    assert sha(c) == cfg['target_common_sha256'] and sha(a) == cfg['target_arm9_sha256']
    return c, a, proof
