"""Source-reviewed duel prose, owned static renderer and escape speech contracts."""
import struct
from pathlib import Path
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.common_single_cache_v861 import entries, SINGLE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.sighting_grammar_editorial import current_entries as previous_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.duel_cache_front_v1142 import assemble as front_assemble, ADDRESS as FRONT, END
from scripts.duel_renderer_thumb_v1124 import assemble as renderer_assemble
from scripts.duel_editorial_layout_v1155 import IDS, ESCAPE_IDS, PROFILE, compiled
from scripts import duel_escape_runtime_v1152 as escape
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000
SOURCE_COMMON = 'c12d21c280dea311c7a97511778cf418bca5783418b9c153408086fdec5ed425'
SOURCE_ARM = 'aff137700915a3499d0d6f1b1b51e26cc8d56265b7430534d3fdf1f64793733d'
CONFIG = 'translations/duel_editorial_release_v1.json'
COMPONENT = Path('translations/runtime/duel_layout_pic_v1.bin')
COMPONENT_SHA = '64474a4c40ba1aeb655be68297ca676e79b9b090760b83e46dbb50140a3e7aac'


def owned_entries(common, arm, directory):
    blocks = IlnkContainer.parse(common).blocks
    component = COMPONENT.read_bytes()
    assert len(component) == 1480 and sha(component) == COMPONENT_SHA
    assert blocks[21][:1484] == component+bytes(4)
    result = entries(common, arm, directory)
    assert result[1931].block == 21 and result[1931].block_offset == 1484
    assert all(result[n].block == 21 for n in range(1931, 1951))
    assert all(row.block != 21 or row.block_offset >= 1484 for row in result)
    return result


def plan(common, arm, doc):
    assert sha(common) == SOURCE_COMMON and sha(arm) == SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
    assert doc['encoder'] == 'dialogue-relocatable-v1' and doc['consumer_layout_profile'] == PROFILE
    assert tuple(row['message_id'] for row in doc['records']) == IDS
    assert doc['current_COMMON_sha256'] == SOURCE_COMMON and doc['current_ARM9_sha256'] == SOURCE_ARM
    clean, accepted = map(NdsImage.open, ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds'))
    assert sha(Path('work/clean.nds').read_bytes()) == doc['source_clean_ROM_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    japanese = parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    canonical = parser.common_message_entries(accepted.read_file('/COMMON/MESFILE.DK4'), accepted.read_file('/__arm9__.bin'), clean=False)
    before = previous_entries(common, arm)
    authored = {}
    for row in doc['records']:
        n = row['message_id']
        assert row['source_hex'] == japanese[n].text.hex()
        assert row['canonical_source_hex'] == canonical[n].text.hex()
        assert row['current_text_hex'] == before[n].text.hex()
        assert row['native_argument_count'] == japanese[n].text.count(b'%s')
        assert row['source_native_macros'] == []
        value = compiled(row)
        assert value.hex() == row['compiled_hex'] and b'\n' not in value
        authored[n] = value
    component = COMPONENT.read_bytes()
    assert len(component) == 1480 and sha(component) == COMPONENT_SHA
    prefix = component+bytes(4)
    source = IlnkContainer.parse(common)
    rebuilt, target, fields, opaque = list(source.blocks), bytearray(arm), [], {}
    groups = {20: list(range(1756, 1931)), 21: list(range(1931, 1977)), 22: list(range(1977, 2100))}
    assert min(r.message_id for r in before if r.block == 20) == 1756
    assert min(r.message_id for r in before if r.block == 22) == 1977
    assert max(r.message_id for r in before if r.block == 22) == 2099
    for block, numbers in groups.items():
        body = bytearray(prefix if block == 21 else b'')
        for n in numbers:
            row = before[n]
            tail = source.blocks[row.block][row.block_offset+len(row.text)+1:row.copy_end]
            if set(tail)-{0, 32}:
                assert n not in authored
                value = source.blocks[row.block][row.block_offset:row.copy_end]
                opaque[n] = value
            else:
                value = authored.get(n, row.text)+b'\0'
            assert 0 < len(value) < 512
            at = parser.TABLE_OFFSET+n*2
            struct.pack_into('<H', target, at, len(body))
            fields.append((at, 2))
            body.extend(value)
        assert 0 < len(body) <= 8192
        rebuilt[block] = bytes(body)
        at = parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH', target, at, numbers[0], len(body))
        fields.append((at, 4))
    transcription = renderer_assemble(arm)
    front, assembly = front_assemble(len(component))
    assert len(transcription) == 200 and len(front) == 104
    target[0xDA28:0xDB5C] = transcription+bytes(108)
    target[FRONT-BASE:END-BASE] = front+bytes(END-FRONT-len(front))
    assembler = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    assert target[0xDA96:0xDA9A] == bytes(assembler.asm('blx 0x020d5404', BASE+0xDA96)[0])
    target[0xDA96:0xDA9A] = bytes(assembler.asm(f'bl {FRONT}', BASE+0xDA96)[0])
    # The same proven membership update as V1153, applied after the final
    # compiled message metadata. Public bank and status literal retain size.
    assert arm[escape.CONTRACTS-BASE:escape.CONTRACTS-BASE+184] == escape.previous.table()
    assert struct.unpack_from('<I', arm, escape.STATUS_LITERAL-BASE)[0] == escape.previous.PACKED_PHRASES
    packed = arm[escape.previous.PACKED_PHRASES-BASE:escape.previous.PACKED_PHRASES-BASE+24]
    assert arm[escape.previous.PACKED_PHRASES-BASE+24:escape.END-BASE] == bytes(4)
    public = escape.table()+packed
    assert len(public) == 212
    for at, value in ((escape.CONTRACTS-BASE, public),
                      (escape.STATUS_LITERAL-BASE, struct.pack('<I', escape.PACKED_PHRASES))):
        target[at:at+len(value)] = value
    c, a = IlnkContainer(rebuilt).to_bytes(), bytes(target)
    directory = sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    after = owned_entries(c, a, directory)
    assert len(before) == len(after) == 3668
    assert all(b.text == authored.get(e.message_id, e.text) for e, b in zip(before, after, strict=True))
    assert all(source.blocks[b] == rebuilt[b] for b in range(41) if b not in groups)
    for n, payload in opaque.items():
        row = after[n]
        assert rebuilt[row.block][row.block_offset:row.copy_end] == payload
    ranges = [(0xDA28, 0x134), (escape.CONTRACTS-BASE, 212), (escape.STATUS_LITERAL-BASE, 4)]
    restored = bytearray(a)
    for at, size in [*fields, *ranges]:
        restored[at:at+size] = arm[at:at+size]
    assert bytes(restored) == arm and a[0x535E0:0x535E8] == arm[0x535E0:0x535E8] == SINGLE
    old, new = MainCodeFile(arm, BASE), MainCodeFile(a, BASE)
    shape = lambda code: [(s.ramAddress, len(s.data), s.bssSize) for s in code.sections]
    assert shape(old) == shape(new) and cache_plan(arm) == cache_plan(a)
    assert all(old.sections[i].data == new.sections[i].data for i in (1, 2, 3, 4))
    assert len(new.sections[3].data)-48 == 123040
    return c, a, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS],
        'reviewed_native_IDs': list(IDS), 'metadata_fields': fields, 'owned_ARM9_fields': ranges,
        'directory_sha256': directory, 'repacked_block_range': [20, 22],
        'repacked_native_IDs': list(range(1756, 2100)),
        'repacked_block_lengths': [len(rebuilt[b]) for b in range(20, 23)],
        'opaque_payload_IDs': sorted(opaque), 'component_sha256': COMPONENT_SHA,
        'opaque_code_prefix': {'block': 21, 'carrier_ID': 1931, 'bytes': 1484, 'component_bytes': 1480,
            'existing_cache_address': 0x0228E70C, 'entry': 'duel_draw',
            'future_repackers_must_preserve_prefix_and_carrier': True},
        'front_assembly': assembly, 'all3635_unselected_strings_and_opaque_payloads_exact': True,
        'all38_other_blocks_exact': True, 'entire_boot_prefix_and_all_other_ARM9_bytes_exact': True,
        'all_sections_BSS_cache_allocations_arenas_and123040_staged_bytes_exact': True,
        'all33_one_paragraphs_and13_compiler_owned_speech_state_bytes': True,
        'actual_duel_cache_visibility_scene_dismissal_and_transitions_pending': True,
        'experimental': True, 'full_goal_complete': False}


def current_entries(common, arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return owned_entries(common, arm, config['directory_sha256'])


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-duel-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name, digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    doc = read(manuscript)
    for key in ('native_context_proof', 'source_context_supplement', 'native_consumer_path_proof',
                'resident_font_proof', 'escape_font_proof', 'native_runtime_proof', 'visual_review', 'supersedes_manuscript'):
        assert sha(Path(doc[key]).read_bytes()) == doc[key+'_sha256'], key
    draft = read(doc['supersedes_manuscript'])
    assert [(r['message_id'], r['english'], r['source_meaning']) for r in doc['records']] == [
        (r['message_id'], r['english'], r['source_meaning']) for r in draft['records']]
    fonts, escapes, visual = [read(doc[k]) for k in ('resident_font_proof', 'escape_font_proof', 'visual_review')]
    assert len(fonts['cases']) == 1356 and len(escapes['cases']) == 1417
    assert visual['full_first_last_letters_uniform_margins_complete_words_and_bounds_accepted']
    assert not visual['visual_review_pending']
    for row in visual['all_six_sheets_visually_inspected']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    rows = {r['message_id']: r for r in doc['records']}
    for row in fonts['cases']:
        assert row['full_first_last_glyphs_uniform_margins_no_overflow_or_crop_loss']
        template = rows[row['message_ID']]['english'].encode('ascii')
        assert template.replace(b'%s', bytes.fromhex(row['name_hex'])) == bytes.fromhex(row['expanded_hex'])
    for row in escapes['cases']:
        assert row['compiled_hex'] == compiled(rows[row['message_ID']]).hex()
        assert row['whole228x64_native_independent_font_and_neighbor_guards_exact']
        if row['weak_line_end_indices']:
            assert row['message_ID'] == 1954 and row['lines'][0].endswith('Come on,')
            assert row['lines'][1] == 'lads, cover them!' and not row['short_or_orphan_final_row']
    c, a, proof = plan(common, arm, doc)
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    assert proof['directory_sha256'] == config['directory_sha256']
    copies, audit = read(config['native_copy_proof']), read(config['native_consumer_audit'])
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    assert copies['COMMON_sha256'] == sha(c) and copies['ARM9_sha256'] == sha(a)
    assert copies['all_full_span_NUL8192_input_and_output_guard_checks_pass']
    assert copies['all_stack_and_callee_saved_native_ABI_checks_pass']
    assert audit['batch_sha256'] == sha(manuscript.read_bytes()) and len(audit['records']) == 33
    assert audit['target_COMMON_sha256'] == sha(c) and audit['target_ARM9_sha256'] == sha(a)
    assert audit['blocking_errors'] == audit['unwaived_warnings'] == 0
    return c, a, proof
