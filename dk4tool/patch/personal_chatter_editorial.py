"""Source-locked Deck comments and their existing paper-window source crop."""

import struct
from pathlib import Path
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.refit_dialogue_editorial import current_entries as previous_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.personal_chatter_layout_v837 import compiled
from scripts.prepare_item_common_v788 import repack
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_village_wrap_v608 import read

IDS = tuple(range(1361, 1386))
SOURCE_COMMON = '5dfda4ee96ce589fa11c0f5403b37913668f9ac153b09942e5b746d739174861'
SOURCE_ARM = '6db703ba4db4919c16c9f4d3ed6c7eaaf8f18d113ad9fde8445dcde3f3c40a6f'
CONFIG = 'translations/personal_chatter_editorial_release_v1.json'
CROP = 0x1147B8


def expanded_crop(arm):
    assert struct.unpack_from('<7I', arm, CROP - 20) == (0xFFFFFFFF, 16, 112, 0, 60, 144, 24)
    target = bytearray(arm)
    struct.pack_into('<2I', target, CROP, 216, 36)
    return bytes(target)


def plan(common, arm, doc):
    assert sha(common) == SOURCE_COMMON and sha(arm) == SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
    assert doc['encoder'] == 'dialogue-relocatable-v1'
    assert doc['consumer_layout_profile'] == 'deck-personnel-visible-v1'
    assert tuple(r['message_id'] for r in doc['records']) == IDS
    assert doc['current_COMMON_sha256'] == SOURCE_COMMON and doc['current_ARM9_sha256'] == SOURCE_ARM
    clean, canonical = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    assert sha(Path('work/clean.nds').read_bytes()) == doc['source_clean_ROM_sha256']
    jp = parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    accepted = parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    before = previous_entries(common, arm)
    authored = {}
    for row in doc['records']:
        n = row['message_id']
        assert row['source_hex'] == jp[n].text.hex()
        assert row['canonical_source_hex'] == accepted[n].text.hex()
        assert row['current_text_hex'] == before[n].text.hex()
        assert row['native_argument_count'] == 0
        authored[n] = compiled(row)
    scoped = SimpleNamespace(common_message_entries=lambda c, a, clean=False: previous_entries(c, a))
    pack = FunctionType(repack.__code__, {**repack.__globals__, 'parser': scoped})
    before, blocks, first, last, selected, opaque, groups, attempts = pack(common, arm, authored)
    patched = expanded_crop(arm)
    target, rebuilt, fields = bytearray(patched), list(blocks), []
    for block, (group, body) in zip(range(first, last + 1), groups, strict=True):
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
    assert all(b.text == authored.get(e.message_id, e.text) for e, b in zip(before, after, strict=True))
    assert all(blocks[n] == rebuilt[n] for n in range(41) if not first <= n <= last)
    for n, payload in opaque.items():
        e = after[n]
        assert rebuilt[e.block][e.block_offset:e.copy_end] == payload
    assert all(before[n].text == after[n].text for n in (64, 292, 346, 347, 348, 676, 677))
    restored = bytearray(a)
    for at, size in fields:
        restored[at:at + size] = patched[at:at + size]
    assert bytes(restored) == patched
    restored[CROP:CROP + 8] = arm[CROP:CROP + 8]
    assert bytes(restored) == arm and cache_plan(a) == cache_plan(arm)
    old, new = MainCodeFile(arm, 0x02000000), MainCodeFile(a, 0x02000000)
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in old.sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in new.sections]
    assert old.sections[3].data == new.sections[3].data and len(new.sections[3].data) - 48 == 123040
    return c, a, {'changed_records': [f'COMMON_MESSAGE_{i}' for i in IDS if before[i].text != after[i].text],
                  'reviewed_native_IDs': list(IDS), 'metadata_fields': fields, 'directory_sha256': directory,
                  'repacked_block_range': [first, last], 'packing_attempts': attempts,
                  'repacked_native_IDs': [e.message_id for e in selected],
                  'all3643_other_message_strings_exact': True, 'opaque_payload_IDs': sorted(opaque),
                  'all_opaque_payloads_and_unselected_blocks_exact': True,
                  'crop_owned_fields': [CROP, CROP + 4], 'crop_source': [144, 24], 'crop_target': [216, 36],
                  'all_other_ARM9_bytes_except_native_metadata_exact': True,
                  'all_section_BSS_cache_and123040_staged_bounds_unchanged': True,
                  'actual_RGB_activity_and_gameplay_not_claimed_by_this_stage': True,
                  'experimental': True, 'full_goal_complete': False}


def current_entries(common, arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return local_entries(config['directory_sha256'])(common, arm, clean=False)


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-personal-chatter-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name, digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    doc = read(manuscript)
    draft = Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes()) == doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'], r['english'], r['source_meaning']) for r in doc['records']] == [
        (r['message_id'], r['english'], r['source_meaning']) for r in read(draft)['records']]
    projection = Path(doc['native_projection_proof'])
    assert sha(projection.read_bytes()) == doc['native_projection_proof_sha256']
    fonts = read(projection)
    assert fonts['manuscript_sha256'] == sha(draft.read_bytes()) and not fonts['visual_review_pending']
    assert fonts['source_ARM9_sha256'] == SOURCE_ARM
    assert fonts['proposed_parent_ARM9_sha256'] == sha(expanded_crop(arm))
    assert fonts['exact_owned_parent_data_fields'] == [CROP, CROP + 4]
    assert fonts['source_values'] == [144, 24] and fonts['target_values'] == [216, 36]
    assert fonts['all_frame_portrait_header_draws_destinations_palettes_unchanged']
    cases = fonts['all25_compiled_visible_word_and_native_font_cases']
    assert len(cases) == 25 and len(fonts['all144_visible_width_phase_cases']) == 144
    for row, case in zip(doc['records'], cases, strict=True):
        assert row['message_id'] == case['message_id'] and compiled(row).hex() == case['text_hex']
        assert case['full252x96_native_and_independent_canvas_equal']
        assert case['all_body_ink_inside_actual_parent_crop']
    c, a, proof = plan(common, arm, doc)
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    assert proof['directory_sha256'] == config['directory_sha256']
    copies = read(config['native_copy_proof'])
    assert copies['COMMON_sha256'] == sha(c) and copies['ARM9_sha256'] == sha(a)
    assert len(copies['all3668_native_IDs_warm_and_cold7336_complete_copies']) == 3668
    return c, a, proof
