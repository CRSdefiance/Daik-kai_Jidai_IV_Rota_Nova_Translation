"""Source-reviewed15 fleet-sighting paragraphs and two native label repairs."""
import struct
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.reinforcement_sniping_editorial import current_entries as previous_entries
from dk4tool.patch.common_single_cache_v861 import SINGLE, entries, repack
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts import sighting_runtime_v1071 as runtime
from scripts.sighting_labels_v1083b import apply as apply_labels,FIELDS as LABEL_FIELDS
from scripts.sighting_layout_v1069 import IDS, PROFILE, compiled
from scripts.verify_village_wrap_v608 import read

SOURCE_COMMON = 'd0ad42d455a164f1f791d4ed3e3f40d6462a4fc037973f1e325871b7afa65152'
SOURCE_ARM = 'cd9a7d894047d655f72d6d6152d253aafeb9d5c2e5082a7b1e934d590e7fa028'
CONFIG = 'translations/sighting_editorial_release_v1.json'


def plan(common, arm, doc):
    assert sha(common) == SOURCE_COMMON and sha(arm) == SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
    assert doc['encoder'] == 'dialogue-relocatable-v1' and doc['consumer_layout_profile'] == PROFILE
    assert tuple(r['message_id'] for r in doc['records']) == IDS
    assert doc['current_COMMON_sha256'] == SOURCE_COMMON and doc['current_ARM9_sha256'] == SOURCE_ARM
    clean, canonical = map(NdsImage.open, ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds'))
    assert sha(Path('work/clean.nds').read_bytes()) == doc['source_clean_ROM_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    jp = parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    accepted = parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    before = previous_entries(common, arm)
    assert len(doc['native_label_records']) == 2
    for row, (at, old, new) in zip(doc['native_label_records'], LABEL_FIELDS, strict=True):
        assert row['offset'] == at and row['allocation_bytes'] == len(old) == len(new)
        assert row['source_hex'] == clean.read_file('/__arm9__.bin')[at:at+len(old)].hex()
        assert row['canonical_source_hex'] == canonical.read_file('/__arm9__.bin')[at:at+len(old)].hex()
        assert row['current_text_hex'] == old.hex() and row['replacement_hex'] == new.hex()
        assert all(row['review'][gate] for gate in ('source','context','localization','naturalness','formatting'))
    authored = {}
    for row in doc['records']:
        n = row['message_id']
        assert row['source_hex'] == jp[n].text.hex() and row['canonical_source_hex'] == accepted[n].text.hex()
        assert row['current_text_hex'] == before[n].text.hex()
        args = 2
        assert row['native_argument_count'] == jp[n].text.count(b'%s') == args
        assert row['source_native_macros'] == []
        assert row['source_family'] == ('fleet-sighting-battle-preparation' if n < 622 else 'fleet-sighting-under-attack')
        assert all(row['review'].get(gate) for gate in ('source', 'context', 'localization', 'naturalness', 'formatting'))
        payload = compiled(row)
        assert b'\n' not in payload and payload.hex() == row['compiled_hex']
        authored[n] = payload
    authored = {n: raw for n, raw in authored.items() if raw != before[n].text}
    pack = FunctionType(repack.__code__, {**repack.__globals__, 'previous_entries': previous_entries})
    before, blocks, first, last, selected, opaque, groups, attempts = pack(common, arm, authored)
    runtime_only, runtime_plan = runtime.apply(arm)
    runtime_arm, label_plan = apply_labels(runtime_only)
    # Native text metadata is independent of the three already-owned runtime
    # spans. Start from the exact verified runtime image,then update only native
    # table/directory fields emitted by the original single-cache repacker.
    target, rebuilt, fields = bytearray(runtime_arm), list(blocks), []
    for block, (group, body) in zip(range(first, last+1), groups, strict=True):
        rebuilt[block] = body
        at = parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH', target, at, group[0][0], len(body))
        fields.append((at, 4))
        for n, offset, payload in group:
            at = parser.TABLE_OFFSET+n*2
            struct.pack_into('<H', target, at, offset)
            fields.append((at, 2))
    c, a = IlnkContainer(rebuilt).to_bytes(), bytes(target)
    directory = sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    after = entries(c, a, directory)
    assert len(before) == len(after) == 3668
    assert all(b.text == authored.get(e.message_id, e.text) for e, b in zip(before, after, strict=True))
    assert all(blocks[b] == rebuilt[b] for b in range(41) if not first <= b <= last)
    for n, payload in opaque.items():
        row = after[n]
        assert rebuilt[row.block][row.block_offset:row.copy_end] == payload
    restored = bytearray(a)
    for at, size in fields:
        assert runtime_arm[at:at+size] == arm[at:at+size]
        restored[at:at+size] = runtime_arm[at:at+size]
    assert bytes(restored) == runtime_arm and cache_plan(a) == cache_plan(arm)
    old_code, new_code = MainCodeFile(arm, 0x02000000), MainCodeFile(a, 0x02000000)
    shape = lambda code: [(s.ramAddress, len(s.data), s.bssSize) for s in code.sections]
    assert shape(old_code) == shape(new_code)
    assert all(old_code.sections[n].data == new_code.sections[n].data for n in (1, 2, 3))
    assert len(new_code.sections[3].data)-48 == 123040
    return c, a, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS if before[n].text != after[n].text],
        'reviewed_native_IDs': list(IDS), 'metadata_fields': fields, 'directory_sha256': directory,
        'repacked_block_range': [first, last], 'packing_attempts': attempts,
        'repacked_native_IDs': [e.message_id for e in selected],
        'repacked_block_lengths': [len(rebuilt[b]) for b in range(first, last+1)],
        'runtime_source_and_exact_owned_changes': runtime_plan,
        'labels_source_and_exact_owned_changes': label_plan,
        'changed_ARM9_labels': ['CLOSE_RANGE_BEARING_LABEL','ARMED_LATINA_DEFAULT_SHIP_LABEL'],
        'all3653_unselected_message_strings_and_opaque_payloads_exact': True,
        'opaque_payload_IDs': sorted(opaque), 'all_unselected_blocks_exact': True,
        'all_other_ARM9_bytes_except_native_metadata_three_proven_runtime_spans_and_two_owned_labels_exact': True,
        'all15_paragraphs_have_no_LF_before_original_macro_or_literal_processing': True,
        'existing_single_cache_code_hex_preserved': SINGLE.hex(),
        'single8192_input_reuses_original_two4096_allocation': True,
        'output512_and216x36_Deck_crop_unchanged': True,
        'all_sections_BSS_cache_arenas_and_entire123040_staged_payload_unchanged': True,
        'actual_RGB_geometry_choices_and_gameplay_not_proven_by_this_stage': True,
        'experimental': True, 'full_goal_complete': False}


def current_entries(common, arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return entries(common, arm, config['directory_sha256'])


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-sighting-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name, digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    doc = read(manuscript)
    keys = ('reviewed_research_manuscript','native_context_proof','source_context_supplement',
            'native_font_proof','visual_review','native_runtime_proof','native_provider_proof','native_label_proof')
    for key in keys: assert sha(Path(doc[key]).read_bytes()) == doc[key+'_sha256'], key
    draft = read(doc['reviewed_research_manuscript'])
    assert [(r['message_id'],r['english'],r['source_meaning']) for r in doc['records']] == [(r['message_id'],r['english'],r['source_meaning']) for r in draft['records']]
    context, supplement, font, visual, rt, provider, labels = [read(doc[k]) for k in
        ('native_context_proof','source_context_supplement','native_font_proof','visual_review','native_runtime_proof','native_provider_proof','native_label_proof')]
    assert len(context['all208_original_actor_voice_selections']) == 208
    assert len(supplement['all208_original_attacked_voice_selections']) == 208
    assert context['native_argument_order'] == ['relative-bearing-label','complete-faction-label']
    assert len(context['original_bearing_getter_cases']) == 9
    assert len(font['cases']) == font['complete_native_font_cases'] == 2700
    assert font['unchanged_cases_inherited_exact'] == 2520 and font['changed_cases_rerendered'] == 180
    assert not visual['visual_review_pending'] and visual['blocking_errors'] == visual['unwaived_warnings'] == 0
    assert visual['all15_current_paragraphs_and_six_native_sheets_reviewed']
    assert len(visual['two_complete_native_label_and_capture_notice_previews_visually_reviewed']) == 2
    prior_visual = read(visual['reviewed_dialogue_visual_proof'])
    assert sha(Path(visual['reviewed_dialogue_visual_proof']).read_bytes()) == visual['reviewed_dialogue_visual_proof_sha256']
    assert len(prior_visual['fifteen_invalid_control_printf_and_source_contract_inputs_rejected']) == 15
    assert rt['old_and_new_complete_scope_cases_each'] == 56696 and rt['all3668_modal_outputs_and_wrap_choices_exact']
    assert rt['all140_status8MiB_ABI_guards_pass'] and rt['public212_and_ITCM128_byte_footprints_unchanged']
    assert len(provider['all81_original_getter_ABI_cases']) == len(labels['all81_bearing_getter_ABI_cases']) == 81
    assert labels['all153_other_initialized_ship_records_exact'] and labels['default_fixed_ship_index'] == 115
    assert labels['complete_Armed_Latina_and_NUL_survive_original_initializer']
    for case in labels['native_font_previews']: assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
    records = {r['message_id']:r for r in doc['records']}
    for case in font['cases']:
        assert compiled(records[case['message_ID']]).hex() == case['compiled_hex']
        assert case['whole228x64_native_and_independent_font_match']
        assert case['complete_leading_trailing_letters_and_uniform_native_margin']
        if 'preview' in case: assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
    c, a, proof = plan(common, arm, doc)
    assert proof['runtime_source_and_exact_owned_changes']['research_ARM9_sha256'] == rt['research_ARM9_sha256']
    assert proof['labels_source_and_exact_owned_changes']['research_ARM9_sha256'] == labels['research_ARM9_sha256']
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    assert proof['directory_sha256'] == config['directory_sha256']
    copies, audit = read(config['native_copy_proof']), read(config['native_consumer_audit'])
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 178
    assert copies['COMMON_sha256'] == sha(c) and copies['ARM9_sha256'] == sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass']
    assert copies['callee_saved_ABI_and_stack_pass']
    assert audit['batch_sha256'] == sha(manuscript.read_bytes())
    assert audit['blocking_errors'] == audit['unwaived_warnings'] == 0 and len(audit['records']) == 15
    assert audit['target_COMMON_sha256'] == sha(c) and audit['target_ARM9_sha256'] == sha(a)
    return c, a, proof
